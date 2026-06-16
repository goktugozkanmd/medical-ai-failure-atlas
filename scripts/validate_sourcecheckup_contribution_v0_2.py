#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "sourcecheckup" / "examples" / "sourcecheckup_contribution_examples_v0_2.jsonl"

REQUIRED_FIELDS = [
    "contribution_id",
    "source_surface",
    "synthetic_answer_excerpt",
    "exact_claim_text",
    "central_to_answer",
    "declared_sources",
    "required_evidence_checks",
    "proposed_public_action",
    "maintainer_review_status",
    "contains_patient_data",
    "external_actions_executed",
    "outward_use_allowed",
]

ALLOWED_SURFACES = {
    "doi",
    "pmid",
    "url",
    "guideline",
    "policy",
    "broad_source_language",
    "none",
}

ALLOWED_CHECKS = {
    "locator_format",
    "source_exists",
    "metadata_match",
    "exact_claim_support",
    "guideline_scope",
    "policy_jurisdiction",
    "rewrite_without_source_claim",
}

ALLOWED_REVIEW_STATUS = {
    "pending_maintainer_review",
    "maintainer_format_checked",
    "maintainer_rejected",
}

FORBIDDEN_PHRASES = [
    "patient name",
    "date of birth",
    "clinically validated",
    "safe for clinical use",
    "officially approved",
    "verified external truth",
    "source proves",
]


def load_rows(errors: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not INPUT.exists():
        errors.append(f"Missing input: {INPUT}")
        return rows
    for line_number, line in enumerate(INPUT.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"Line {line_number}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"Line {line_number}: row must be an object")
            continue
        rows.append(row)
    return rows


def main() -> int:
    errors: list[str] = []
    rows = load_rows(errors)
    if len(rows) < 4:
        errors.append("Expected at least 4 contribution examples")

    seen_ids: set[str] = set()
    surfaces: set[str] = set()
    evidence_checks_seen: set[str] = set()

    for index, row in enumerate(rows, start=1):
        contribution_id = str(row.get("contribution_id", ""))
        if not contribution_id.startswith("SCV2_"):
            errors.append(f"Row {index}: contribution_id must start with SCV2_")
        if contribution_id in seen_ids:
            errors.append(f"Row {index}: duplicate contribution_id {contribution_id}")
        seen_ids.add(contribution_id)

        for field in REQUIRED_FIELDS:
            if field not in row:
                errors.append(f"Row {index}: missing {field}")
            elif isinstance(row[field], str) and not str(row[field]).strip():
                errors.append(f"Row {index}: empty {field}")

        source_surface = str(row.get("source_surface", ""))
        surfaces.add(source_surface)
        if source_surface not in ALLOWED_SURFACES:
            errors.append(f"Row {index}: invalid source_surface {source_surface}")

        if row.get("contains_patient_data") is not False:
            errors.append(f"Row {index}: contains_patient_data must be false")
        if row.get("external_actions_executed") is not False:
            errors.append(f"Row {index}: external_actions_executed must be false")
        if row.get("outward_use_allowed") is not False:
            errors.append(f"Row {index}: outward_use_allowed must be false")
        if row.get("central_to_answer") is not True:
            errors.append(f"Row {index}: examples must use central claims")

        declared_sources = row.get("declared_sources")
        if not isinstance(declared_sources, list):
            errors.append(f"Row {index}: declared_sources must be a list")
        checks = row.get("required_evidence_checks")
        if not isinstance(checks, list) or not checks:
            errors.append(f"Row {index}: required_evidence_checks must be a non empty list")
            checks = []
        for check in checks:
            check_text = str(check)
            evidence_checks_seen.add(check_text)
            if check_text not in ALLOWED_CHECKS:
                errors.append(f"Row {index}: invalid evidence check {check_text}")

        if source_surface in {"doi", "pmid", "url"} and not declared_sources:
            errors.append(f"Row {index}: locator surfaces require declared_sources")
        if source_surface in {"guideline", "policy", "broad_source_language"} and "exact_claim_support" not in checks:
            errors.append(f"Row {index}: source claim requires exact_claim_support")

        review_status = str(row.get("maintainer_review_status", ""))
        if review_status not in ALLOWED_REVIEW_STATUS:
            errors.append(f"Row {index}: invalid maintainer_review_status")

        row_text = " ".join(str(value).lower() for value in row.values())
        for phrase in FORBIDDEN_PHRASES:
            if phrase in row_text:
                errors.append(f"Row {index}: forbidden phrase {phrase!r}")

    if len(surfaces) < 4:
        errors.append("Expected at least 4 distinct source surfaces")
    if "rewrite_without_source_claim" not in evidence_checks_seen:
        errors.append("Expected rewrite_without_source_claim coverage")

    if errors:
        print("FAIL SourceCheckup contribution v0.2 validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup contribution v0.2 validation")
    print(f"rows={len(rows)}")
    print(f"source_surfaces={len(surfaces)}")
    print(f"input={INPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
