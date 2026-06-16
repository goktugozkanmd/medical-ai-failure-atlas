#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "failure_atlas" / "public" / "case_intake_examples_v0_1.jsonl"

REQUIRED_FIELDS = [
    "case_id",
    "clinical_domain",
    "setting",
    "synthetic_case_summary",
    "failure_pattern",
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
    if len(rows) < 5:
        errors.append("Expected at least 5 synthetic intake examples")

    seen_ids: set[str] = set()
    risk_axes: set[str] = set()
    track_a_seen = False
    track_b_seen = False
    sourcecheckup_seen = False

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
        if str(row.get("track_a_relevance", "")).strip():
            track_a_seen = True
        if str(row.get("track_b_relevance", "")).strip():
            track_b_seen = True

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

    if errors:
        print("FAIL Failure Atlas case intake validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Failure Atlas case intake validation")
    print(f"rows={len(rows)}")
    print(f"risk_axes={len(risk_axes)}")
    print(f"input={INPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
