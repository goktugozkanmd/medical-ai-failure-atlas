#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "label_audit" / "label_audit_example_dashboard_v0_1.json"
MARKDOWN = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md"

REQUIRED_ROLES = {"LAR001", "LAR002", "LAR003", "LAR004"}
REQUIRED_AUDITS = {"LAA001", "LAA002", "LAA003", "LAA004", "LAA005"}
REQUIRED_REVIEW_STATES = {
    "needs_adjudication",
    "needs_clinician_review",
    "not_for_public_summary",
    "synthetic_preview_only",
}
REQUIRED_CLAIM_TYPES = {
    "clinical validation claim",
    "dataset quality proof claim",
    "population performance claim",
    "raw model output release claim",
    "real care record coverage claim",
}
REQUIRED_FILES = [
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md",
    "docs/label_audit/label_audit_example_dashboard_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    "docs/label_audit/label_audit_example_intake_v0_1.json",
    "docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md",
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
]
REQUIRED_PHRASES = [
    "Label audit example dashboard v0.1",
    "Label audit example dashboard rows: 5",
    "Reviewer roles represented: 4",
    "Audit rows represented: 5",
    "Review states represented: 4",
    "Blocked public claim types represented: 5",
    "Synthetic provenance reviewer",
    "Label definition reviewer",
    "Pilot subset reviewer",
    "Public release boundary reviewer",
    "Synthetic provenance audit",
    "Label definition lock audit",
    "Pilot inter rater subset audit",
    "Raw output exclusion audit",
    "Public release boundary audit",
    "real care record coverage claim",
    "clinical validation claim",
    "population performance claim",
    "raw model output release claim",
    "dataset quality proof claim",
    "not proof of dataset quality",
    "not clinical advice",
    "not patient data",
    "not raw model output release",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not regulatory approval",
    "not an official endorsement",
    "make label_audit_dashboard",
]
FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "officially endorsed",
    "regulatory approved",
    "sandbox access granted",
    "patient data used",
    "model is safe",
    "best model",
    "proves data quality",
]


def main() -> int:
    errors: list[str] = []
    if not SOURCE.exists():
        errors.append(f"Missing source JSON: {SOURCE.relative_to(ROOT)}")
        data: dict[str, Any] = {"rows": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    rows = data.get("rows", [])
    if not isinstance(rows, list):
        errors.append("rows must be a list")
        rows = []
    if data.get("example_count") != 5:
        errors.append("example_count must be 5")
    if len(rows) != 5:
        errors.append(f"Expected 5 dashboard rows, found {len(rows)}")
    if data.get("role_count") != 4:
        errors.append("role_count must be 4")
    if data.get("audit_row_count") != 5:
        errors.append("audit_row_count must be 5")
    if data.get("review_state_count") != 4:
        errors.append("review_state_count must be 4")
    if data.get("blocked_public_claim_type_count") != 5:
        errors.append("blocked_public_claim_type_count must be 5")

    for field in [
        "contains_patient_data",
        "synthetic_examples_only",
        "not_for_clinical_use",
        "no_raw_model_output_release",
        "no_clinical_deployment_claim",
        "no_clinical_validation_claim",
        "no_model_safety_claim",
        "no_model_ranking",
        "no_dataset_quality_proof",
        "no_official_endorsement_claim",
    ]:
        expected = False if field == "contains_patient_data" else True
        if data.get(field) is not expected:
            errors.append(f"{field} must be {expected}")

    roles = set(map(str, data.get("role_counts", {}).keys()))
    audits = set(map(str, data.get("audit_counts", {}).keys()))
    states = set(map(str, data.get("review_state_counts", {}).keys()))
    claims = set(map(str, data.get("blocked_public_claim_type_counts", {}).keys()))
    if roles != REQUIRED_ROLES:
        errors.append("role_counts must represent all 4 required roles")
    if audits != REQUIRED_AUDITS:
        errors.append("audit_counts must represent all 5 required audit rows")
    if states != REQUIRED_REVIEW_STATES:
        errors.append("review_state_counts must represent all 4 required states")
    if claims != REQUIRED_CLAIM_TYPES:
        errors.append("blocked_public_claim_type_counts must represent all 5 claim types")

    for row in rows:
        row_id = str(row.get("example_id", ""))
        for key in [
            "title",
            "role_id",
            "role_name",
            "audit_id",
            "audit_name",
            "review_state",
            "blocked_public_claim_type",
            "required_check_count",
        ]:
            if key not in row:
                errors.append(f"{row_id}: missing {key}")
        if row.get("required_check_count") != 4:
            errors.append(f"{row_id}: required_check_count must be 4")

    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).exists():
            errors.append(f"Referenced file does not exist: {relative_path}")

    if not MARKDOWN.exists():
        errors.append(f"Missing generated Markdown: {MARKDOWN.relative_to(ROOT)}")
        text = ""
    else:
        text = MARKDOWN.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Generated Markdown missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing dashboard must not contain hyphen characters")

    if errors:
        print("FAIL label audit example dashboard validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit example dashboard validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"dashboard_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
