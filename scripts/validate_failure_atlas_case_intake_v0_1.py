#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUTS = [
    ROOT / "failure_atlas" / "public" / "case_intake_examples_v0_1.jsonl",
    ROOT / "tr_medllm_safetybench" / "synthetic_risk_pack_v0_1.jsonl",
    ROOT / "failure_atlas" / "public" / "case_intake_expansion_cardio_emerg_endo_v0_1.jsonl",
    ROOT / "failure_atlas" / "public" / "case_intake_expansion_neuro_nephro_gi_obgyn_geri_v0_1.jsonl",
]
TAXONOMY_MAP = ROOT / "failure_atlas" / "public" / "taxonomy_map_v0_1.json"

REQUIRED_FIELDS = [
    "case_id",
    "clinical_domain",
    "setting",
    "synthetic_case_summary",
    "failure_pattern",
    "taxonomy_pattern_ids",
    "risk_axis",
    "sourcecheckup_needed",
    "clinician_review_needed",
    "safe_answer_expectation",
    "release_gate",
    "track_a_relevance",
    "track_b_relevance",
    "synthetic_only",
    "patient_data_used",
    "clinical_use_allowed",
]

ALLOWED_RISK_AXES = {
    "false_reassurance",
    "medication_safety",
    "source_support",
    "missing_context",
    "rare_danger",
    "over_treatment",
    "communication_risk",
    "bias_or_premature_closure",
    "workflow_mismatch",
    "privacy_or_provenance",
}

ALLOWED_RELEASE_GATES = {
    "synthetic_preview_only",
    "needs_source_review",
    "needs_clinician_review",
    "not_for_public_summary",
}

FORBIDDEN_PHRASES = [
    "real patient",
    "clinical validation",
    "validated for clinical use",
    "safe for clinical use",
    "approved by",
    "official endorsement",
    "model is safe",
    "best model",
]


def load_taxonomy_ids(errors: list[str]) -> set[str]:
    if not TAXONOMY_MAP.exists():
        errors.append(f"Missing taxonomy map: {TAXONOMY_MAP}")
        return set()
    try:
        data = json.loads(TAXONOMY_MAP.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid taxonomy map JSON: {exc}")
        return set()
    patterns = data.get("patterns", [])
    if not isinstance(patterns, list):
        errors.append("taxonomy map patterns must be a list")
        return set()
    ids: set[str] = set()
    for item in patterns:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            ids.add(str(item["id"]))
    if len(ids) < 10:
        errors.append("taxonomy map should expose all ten preview pattern IDs")
    return ids


def load_rows(path: Path, errors: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not path.exists():
        errors.append(f"Missing input: {path}")
        return rows
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)} line {line_number}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"{path.relative_to(ROOT)} line {line_number}: row must be an object")
            continue
        rows.append(row)
    return rows


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--input", action="append", help="JSONL input to validate. May be repeated.")
    args = parser.parse_args()

    errors: list[str] = []
    taxonomy_ids = load_taxonomy_ids(errors)
    inputs = [ROOT / item for item in args.input] if args.input else [path for path in DEFAULT_INPUTS if path.exists()]

    rows: list[dict[str, object]] = []
    for path in inputs:
        rows.extend(load_rows(path, errors))

    if len(rows) < 5:
        errors.append("Expected at least 5 synthetic intake examples")

    seen_ids: set[str] = set()
    risk_axes: set[str] = set()
    track_a_seen = False
    track_b_seen = False
    sourcecheckup_seen = False
    tr_pack_seen = False
    taxonomy_seen: set[str] = set()

    for index, row in enumerate(rows, start=1):
        case_id = str(row.get("case_id", ""))
        if case_id in seen_ids:
            errors.append(f"Row {index}: duplicate case_id {case_id}")
        seen_ids.add(case_id)

        for field in REQUIRED_FIELDS:
            if field not in row:
                errors.append(f"Row {index}: missing {field}")
            elif isinstance(row[field], str) and not str(row[field]).strip():
                errors.append(f"Row {index}: empty {field}")

        if row.get("synthetic_only") is not True:
            errors.append(f"Row {index}: synthetic_only must be true")
        if row.get("patient_data_used") is not False:
            errors.append(f"Row {index}: patient_data_used must be false")
        if row.get("clinical_use_allowed") is not False:
            errors.append(f"Row {index}: clinical_use_allowed must be false")
        if not isinstance(row.get("sourcecheckup_needed"), bool):
            errors.append(f"Row {index}: sourcecheckup_needed must be boolean")
        if not isinstance(row.get("clinician_review_needed"), bool):
            errors.append(f"Row {index}: clinician_review_needed must be boolean")

        risk_axis = str(row.get("risk_axis", ""))
        risk_axes.add(risk_axis)
        if risk_axis not in ALLOWED_RISK_AXES:
            errors.append(f"Row {index}: invalid risk_axis {risk_axis}")
        release_gate = str(row.get("release_gate", ""))
        if release_gate not in ALLOWED_RELEASE_GATES:
            errors.append(f"Row {index}: invalid release_gate {release_gate}")
        if row.get("sourcecheckup_needed") is True:
            sourcecheckup_seen = True
            if "T03" not in row.get("taxonomy_pattern_ids", []):
                errors.append(f"Row {index}: SourceCheckup rows should include taxonomy pattern T03")
        if str(row.get("track_a_relevance", "")).strip():
            track_a_seen = True
        if str(row.get("track_b_relevance", "")).strip():
            track_b_seen = True

        pattern_ids = row.get("taxonomy_pattern_ids")
        if not isinstance(pattern_ids, list) or not pattern_ids:
            errors.append(f"Row {index}: taxonomy_pattern_ids must be a non empty list")
        else:
            local_seen: set[str] = set()
            for pattern_id in pattern_ids:
                if not isinstance(pattern_id, str):
                    errors.append(f"Row {index}: taxonomy_pattern_ids must contain strings")
                    continue
                if pattern_id in local_seen:
                    errors.append(f"Row {index}: duplicate taxonomy pattern {pattern_id}")
                local_seen.add(pattern_id)
                taxonomy_seen.add(pattern_id)
                if taxonomy_ids and pattern_id not in taxonomy_ids:
                    errors.append(f"Row {index}: unknown taxonomy pattern {pattern_id}")

        if case_id.startswith("TRFAI"):
            tr_pack_seen = True
            if row.get("language") != "tr":
                errors.append(f"Row {index}: TRFAI rows must set language to tr")
            if not str(row.get("turkish_prompt_seed", "")).strip():
                errors.append(f"Row {index}: TRFAI rows need a turkish_prompt_seed")

        row_text = " ".join(str(value).lower() for value in row.values())
        for phrase in FORBIDDEN_PHRASES:
            if phrase in row_text:
                errors.append(f"Row {index}: forbidden phrase {phrase!r}")

    if len(risk_axes) < 5:
        errors.append("Expected at least 5 distinct risk axes")
    if not sourcecheckup_seen:
        errors.append("Expected at least one SourceCheckup row")
    if not track_a_seen:
        errors.append("Expected Track A relevance")
    if not track_b_seen:
        errors.append("Expected Track B relevance")
    if not tr_pack_seen:
        errors.append("Expected at least one Turkish synthetic risk pack row")
    if taxonomy_ids and not taxonomy_ids.issubset(taxonomy_seen):
        missing = ", ".join(sorted(taxonomy_ids - taxonomy_seen))
        errors.append(f"Expected coverage of every taxonomy pattern; missing {missing}")

    if errors:
        print("FAIL Failure Atlas case intake validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Failure Atlas case intake validation")
    print(f"rows={len(rows)}")
    print(f"risk_axes={len(risk_axes)}")
    print(f"taxonomy_patterns={len(taxonomy_seen)}")
    print("inputs=" + ",".join(str(path.relative_to(ROOT)) for path in inputs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
