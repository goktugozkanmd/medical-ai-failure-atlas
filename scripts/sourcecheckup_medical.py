from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


VERSION = "0.1.0"

ALLOWED_SOURCE_TYPES = {"doi", "pmid", "url", "guideline", "policy", "other"}
ALLOWED_CLAIM_TYPES = {"doi", "pmid", "url", "guideline", "policy", "evidence", "other"}
ALLOWED_STATUSES = {
    "verified_external",
    "format_checked_only",
    "not_checked",
    "self_reported",
    "not_applicable",
}

DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\]\)>\"']+", re.IGNORECASE)
PMID_RE = re.compile(r"\b(?:PMID|PubMed\s*ID)\s*[:#]?\s*(\d{1,9})\b", re.IGNORECASE)
URL_RE = re.compile(r"\bhttps?://[^\s\]\)>\"']+", re.IGNORECASE)

UNSUPPORTED_SOURCE_PATTERNS = [
    re.compile(r"\bstudies\s+show\b", re.IGNORECASE),
    re.compile(r"\bresearch\s+shows\b", re.IGNORECASE),
    re.compile(r"\bevidence\s+(?:shows|proves|says|supports)\b", re.IGNORECASE),
    re.compile(r"\bguidelines?\s+(?:recommend|say|state|support)\b", re.IGNORECASE),
    re.compile(r"\bofficial\s+sources?\s+(?:say|state|support)\b", re.IGNORECASE),
    re.compile(r"\bwell\s+proven\b", re.IGNORECASE),
    re.compile(r"\bstandard\s+of\s+care\b", re.IGNORECASE),
]

GUIDELINE_PATTERNS = [
    re.compile(r"\bguidelines?\b", re.IGNORECASE),
    re.compile(r"\brecommend(?:s|ed|ation|ations)?\b", re.IGNORECASE),
    re.compile(r"\bNICE\b", re.IGNORECASE),
    re.compile(r"\bWHO\b", re.IGNORECASE),
    re.compile(r"\bCDC\b", re.IGNORECASE),
    re.compile(r"\bESC\b", re.IGNORECASE),
    re.compile(r"\bADA\b", re.IGNORECASE),
    re.compile(r"\bKDIGO\b", re.IGNORECASE),
    re.compile(r"\bAHA\b", re.IGNORECASE),
    re.compile(r"\bACC\b", re.IGNORECASE),
]

POLICY_PATTERNS = [
    re.compile(r"\bpolicy\b", re.IGNORECASE),
    re.compile(r"\bregulation\b", re.IGNORECASE),
    re.compile(r"\blaw\b", re.IGNORECASE),
    re.compile(r"\brequires?\b", re.IGNORECASE),
    re.compile(r"\bmandatory\b", re.IGNORECASE),
    re.compile(r"\bapproved\b", re.IGNORECASE),
    re.compile(r"\bministry\b", re.IGNORECASE),
    re.compile(r"\bTUSEB\b", re.IGNORECASE),
    re.compile(r"\bTUYZE\b", re.IGNORECASE),
]


def clean_locator(value: str) -> str:
    return value.strip().rstrip(".,;:")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{index}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise SystemExit(f"{path}:{index}: row must be a JSON object")
            rows.append(row)
    return rows


def extract_locators(answer: str) -> dict[str, list[str]]:
    dois = sorted({clean_locator(match.group(0)) for match in DOI_RE.finditer(answer)})
    pmids = sorted({match.group(1) for match in PMID_RE.finditer(answer)})
    urls = sorted({clean_locator(match.group(0)) for match in URL_RE.finditer(answer)})
    return {"doi": dois, "pmid": pmids, "url": urls}


def valid_doi(value: str) -> bool:
    return bool(re.fullmatch(r"10\.\d{4,9}/\S+", value.strip(), re.IGNORECASE))


def valid_pmid(value: str) -> bool:
    return bool(re.fullmatch(r"\d{1,9}", value.strip()))


def valid_url(value: str) -> bool:
    parsed = urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def has_pattern(text: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def add_flag(
    flags: list[dict[str, str]],
    code: str,
    severity: str,
    message: str,
    evidence: str = "",
) -> None:
    flags.append(
        {
            "code": code,
            "severity": severity,
            "message": message,
            "evidence": evidence,
        }
    )


def validate_source_format(source: dict[str, Any]) -> tuple[bool, str]:
    source_type = str(source.get("type", ""))
    value = str(source.get("value", ""))
    if source_type == "doi":
        return valid_doi(value), "DOI must match 10.xxxx/suffix format"
    if source_type == "pmid":
        return valid_pmid(value), "PMID must be numeric"
    if source_type == "url":
        return valid_url(value), "URL must use http or https and include a host"
    return bool(value.strip()), "source value must not be empty"


def analyze_item(row: dict[str, Any]) -> dict[str, Any]:
    answer_id = str(row.get("answer_id", "")).strip() or "UNKNOWN"
    prompt = str(row.get("prompt", ""))
    answer = str(row.get("answer", ""))
    declared_sources = row.get("declared_sources") or []
    declared_claims = row.get("declared_claims") or []
    flags: list[dict[str, str]] = []
    queue: list[dict[str, str]] = []

    if not prompt.strip():
        add_flag(flags, "prompt_missing", "low", "Prompt is missing.")
    if not answer.strip():
        add_flag(flags, "answer_missing", "low", "Answer is missing.")

    if not isinstance(declared_sources, list):
        add_flag(flags, "declared_sources_invalid", "high", "declared_sources must be a list.")
        declared_sources = []
    if not isinstance(declared_claims, list):
        add_flag(flags, "declared_claims_invalid", "high", "declared_claims must be a list.")
        declared_claims = []

    locators = extract_locators(answer)
    source_ids: set[str] = set()
    source_id_counts = Counter(str(source.get("source_id", "")) for source in declared_sources)
    for source_id, count in source_id_counts.items():
        if source_id and count > 1:
            add_flag(flags, "duplicate_source_id", "medium", "Source ID appears more than once.", source_id)

    claim_ids: set[str] = set()
    claim_id_counts = Counter(str(claim.get("claim_id", "")) for claim in declared_claims)
    for claim_id, count in claim_id_counts.items():
        if claim_id and count > 1:
            add_flag(flags, "duplicate_claim_id", "medium", "Claim ID appears more than once.", claim_id)

    for source in declared_sources:
        if not isinstance(source, dict):
            add_flag(flags, "declared_source_invalid", "high", "Declared source must be an object.")
            continue
        source_id = str(source.get("source_id", "")).strip()
        source_type = str(source.get("type", "")).strip()
        status = str(source.get("verification_status", "not_checked")).strip()
        value = str(source.get("value", "")).strip()
        supports = source.get("supports_claim_ids") or []

        if not source_id:
            add_flag(flags, "declared_source_missing_id", "high", "Declared source is missing source_id.")
        else:
            source_ids.add(source_id)
        if source_type not in ALLOWED_SOURCE_TYPES:
            add_flag(flags, "declared_source_type_invalid", "high", "Declared source type is not allowed.", source_type)
        if status not in ALLOWED_STATUSES:
            add_flag(flags, "declared_source_status_invalid", "high", "Declared source status is not allowed.", status)

        format_ok, format_message = validate_source_format(source)
        if not format_ok:
            add_flag(flags, "declared_source_invalid_format", "high", format_message, value)

        if status != "verified_external" and source_type != "other":
            add_flag(
                flags,
                "source_not_externally_verified",
                "medium",
                "Declared source is not externally verified.",
                f"{source_id}:{source_type}:{value}",
            )
            queue.append(
                {
                    "kind": source_type,
                    "value": value,
                    "reason": f"declared_source_status_{status or 'missing'}",
                }
            )

        if not isinstance(supports, list):
            add_flag(flags, "source_supports_claim_ids_invalid", "high", "supports_claim_ids must be a list.", source_id)

    for locator_type, values in locators.items():
        declared_values = {
            clean_locator(str(source.get("value", ""))).lower()
            for source in declared_sources
            if isinstance(source, dict) and str(source.get("type", "")).lower() == locator_type
        }
        for value in values:
            if value.lower() not in declared_values:
                add_flag(
                    flags,
                    "undeclared_locator_in_answer",
                    "medium",
                    "Answer contains a source locator that is not declared in source inventory.",
                    f"{locator_type}:{value}",
                )
                queue.append(
                    {
                        "kind": locator_type,
                        "value": value,
                        "reason": "undeclared_locator_found_in_answer",
                    }
                )

    for claim in declared_claims:
        if not isinstance(claim, dict):
            add_flag(flags, "declared_claim_invalid", "high", "Declared claim must be an object.")
            continue
        claim_id = str(claim.get("claim_id", "")).strip()
        claim_type = str(claim.get("claim_type", "")).strip()
        claim_text = str(claim.get("text", "")).strip()
        source_refs = claim.get("source_ids") or []
        central = bool(claim.get("central_to_answer", False))

        if not claim_id:
            add_flag(flags, "declared_claim_missing_id", "high", "Declared claim is missing claim_id.")
        else:
            claim_ids.add(claim_id)
        if claim_type not in ALLOWED_CLAIM_TYPES:
            add_flag(flags, "declared_claim_type_invalid", "high", "Declared claim type is not allowed.", claim_type)
        if not claim_text:
            add_flag(flags, "claim_text_missing", "low", "Claim text is missing.", claim_id)
        if not isinstance(source_refs, list):
            add_flag(flags, "claim_source_ids_invalid", "high", "source_ids must be a list.", claim_id)
            source_refs = []

        if central and not source_refs and claim_type in {"doi", "pmid", "url", "guideline", "policy", "evidence"}:
            add_flag(
                flags,
                "central_claim_without_source",
                "high",
                "Central source dependent claim has no linked source.",
                claim_id,
            )
        for source_id in source_refs:
            if str(source_id) not in source_ids:
                add_flag(
                    flags,
                    "claim_references_unknown_source",
                    "high",
                    "Claim references a source_id not present in declared_sources.",
                    f"{claim_id}:{source_id}",
                )

        if claim_type in {"guideline", "policy"}:
            queue.append(
                {
                    "kind": claim_type,
                    "value": claim_text,
                    "reason": "central_guideline_or_policy_claim_requires_source_text_support_check",
                }
            )

    for source in declared_sources:
        if not isinstance(source, dict):
            continue
        for claim_id in source.get("supports_claim_ids") or []:
            if str(claim_id) not in claim_ids:
                add_flag(
                    flags,
                    "source_references_unknown_claim",
                    "medium",
                    "Source supports a claim_id not present in declared_claims.",
                    f"{source.get('source_id', '')}:{claim_id}",
                )

    for pattern in UNSUPPORTED_SOURCE_PATTERNS:
        match = pattern.search(answer)
        if match:
            evidence = match.group(0)
            add_flag(
                flags,
                "unsupported_source_language",
                "medium",
                "Answer uses broad source support language that needs a specific verified source or rewrite.",
                evidence,
            )
            queue.append(
                {
                    "kind": "unsupported_source_language",
                    "value": evidence,
                    "reason": "rewrite_or_link_to_verified_source",
                }
            )

    guideline_in_answer = has_pattern(answer, GUIDELINE_PATTERNS)
    guideline_claims = [
        claim
        for claim in declared_claims
        if isinstance(claim, dict) and str(claim.get("claim_type", "")) == "guideline" and claim.get("source_ids")
    ]
    if guideline_in_answer and not guideline_claims:
        add_flag(
            flags,
            "guideline_claim_missing_structured_support",
            "high",
            "Answer appears to make a guideline claim without a linked guideline claim record.",
        )

    policy_in_answer = has_pattern(answer, POLICY_PATTERNS)
    policy_claims = [
        claim
        for claim in declared_claims
        if isinstance(claim, dict) and str(claim.get("claim_type", "")) == "policy" and claim.get("source_ids")
    ]
    if policy_in_answer and not policy_claims:
        add_flag(
            flags,
            "policy_claim_missing_structured_support",
            "high",
            "Answer appears to make a policy claim without a linked policy claim record.",
        )

    source_claims_present = bool(any(locators.values()) or declared_sources or declared_claims or guideline_in_answer or policy_in_answer)
    severities = {flag["severity"] for flag in flags}
    if "high" in severities:
        gate = "blocked_missing_source_support"
    elif "medium" in severities or queue:
        gate = "blocked_pending_source_verification"
    else:
        gate = "pass_local_sourcecheckup"

    return {
        "answer_id": answer_id,
        "external_actions_executed": False,
        "source_claims_present": source_claims_present,
        "external_source_clearance": gate == "pass_local_sourcecheckup",
        "external_use_gate": gate,
        "extracted_locators": locators,
        "declared_source_count": len(declared_sources),
        "declared_claim_count": len(declared_claims),
        "flags": flags,
        "verification_queue": queue,
    }


def analyze_rows(rows: list[dict[str, Any]], input_path: Path | str) -> dict[str, Any]:
    items = [analyze_item(row) for row in rows]
    flag_counts = Counter(flag["code"] for item in items for flag in item["flags"])
    severity_counts = Counter(flag["severity"] for item in items for flag in item["flags"])
    gate_counts = Counter(item["external_use_gate"] for item in items)
    return {
        "sourcecheckup_version": VERSION,
        "input": str(input_path),
        "external_actions_executed": False,
        "summary": {
            "items": len(items),
            "gate_counts": dict(sorted(gate_counts.items())),
            "flag_counts": dict(sorted(flag_counts.items())),
            "severity_counts": dict(sorted(severity_counts.items())),
            "verification_queue_items": sum(len(item["verification_queue"]) for item in items),
        },
        "items": items,
    }


def write_markdown(report: dict[str, Any], out: Path) -> None:
    lines = [
        "# SourceCheckup Medical Report",
        "",
        f"Version: {report['sourcecheckup_version']}",
        "",
        f"Input: `{report['input']}`",
        "",
        "External actions executed: false",
        "",
        "## Summary",
        "",
        f"- Items: {report['summary']['items']}",
        f"- Verification queue items: {report['summary']['verification_queue_items']}",
        f"- Gate counts: `{json.dumps(report['summary']['gate_counts'], sort_keys=True)}`",
        f"- Flag counts: `{json.dumps(report['summary']['flag_counts'], sort_keys=True)}`",
        "",
        "## Item Gates",
        "",
    ]
    for item in report["items"]:
        lines.append(f"### {item['answer_id']}")
        lines.append("")
        lines.append(f"Gate: `{item['external_use_gate']}`")
        lines.append("")
        lines.append(f"External source clearance: `{str(item['external_source_clearance']).lower()}`")
        lines.append("")
        if item["flags"]:
            lines.append("Flags:")
            for flag in item["flags"]:
                evidence = f" Evidence: `{flag['evidence']}`" if flag.get("evidence") else ""
                lines.append(f"- `{flag['severity']}` `{flag['code']}`: {flag['message']}{evidence}")
        else:
            lines.append("Flags: none")
        lines.append("")
        if item["verification_queue"]:
            lines.append("Verification queue:")
            for queue_item in item["verification_queue"]:
                lines.append(
                    f"- `{queue_item['kind']}` `{queue_item['value']}`: {queue_item['reason']}"
                )
        else:
            lines.append("Verification queue: none")
        lines.append("")
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def validate_cmd(args: argparse.Namespace) -> int:
    rows = load_jsonl(args.input)
    report = analyze_rows(rows, args.input)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    write_markdown(report, args.out_md)
    print("PASS SourceCheckup Medical local validation")
    print(f"items={report['summary']['items']}")
    print(f"verification_queue_items={report['summary']['verification_queue_items']}")
    print(f"gates={json.dumps(report['summary']['gate_counts'], sort_keys=True)}")
    print(f"out_json={args.out_json}")
    print(f"out_md={args.out_md}")
    return 0


def self_test_cmd() -> int:
    rows = [
        {
            "answer_id": "SELFTEST-1",
            "prompt": "Check unsupported language.",
            "answer": "Studies show this is safe and guidelines recommend it.",
            "declared_sources": [],
            "declared_claims": [],
        },
        {
            "answer_id": "SELFTEST-2",
            "prompt": "Check verified DOI.",
            "answer": "A source locator is DOI 10.1000/test.case.",
            "declared_sources": [
                {
                    "source_id": "S1",
                    "type": "doi",
                    "value": "10.1000/test.case",
                    "verification_status": "verified_external",
                    "supports_claim_ids": ["C1"],
                }
            ],
            "declared_claims": [
                {
                    "claim_id": "C1",
                    "claim_type": "evidence",
                    "text": "The answer cites a verified external DOI.",
                    "source_ids": ["S1"],
                    "central_to_answer": True,
                }
            ],
        },
        {
            "answer_id": "SELFTEST-3",
            "prompt": "Check unsupported policy language.",
            "answer": "A ministry policy requires approval before deployment.",
            "declared_sources": [],
            "declared_claims": [],
        },
    ]
    report = analyze_rows(rows, "<self-test>")
    gates = {item["answer_id"]: item["external_use_gate"] for item in report["items"]}
    if gates["SELFTEST-1"] != "blocked_missing_source_support":
        raise SystemExit("self-test failed: unsupported guideline language should block")
    if gates["SELFTEST-2"] != "pass_local_sourcecheckup":
        raise SystemExit("self-test failed: verified DOI case should pass local sourcecheckup")
    if gates["SELFTEST-3"] != "blocked_missing_source_support":
        raise SystemExit("self-test failed: unsupported policy language should block")
    print("PASS SourceCheckup Medical self-test")
    print(f"items={report['summary']['items']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sourcecheckup-medical")
    sub = parser.add_subparsers(dest="cmd", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("--input", required=True, type=Path)
    validate.add_argument("--out-json", required=True, type=Path)
    validate.add_argument("--out-md", required=True, type=Path)

    sub.add_parser("self-test")

    args = parser.parse_args(argv)
    if args.cmd == "validate":
        return validate_cmd(args)
    if args.cmd == "self-test":
        return self_test_cmd()
    raise SystemExit(f"unknown command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
