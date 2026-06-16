#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "label_audit_reviewer_role_table_v0_1.json"
TABLE = ROOT / "docs" / "LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md"

REQUIRED_ROLES = {"LAR001", "LAR002", "LAR003", "LAR004"}
REQUIRED_AUDITS = {"LAA001", "LAA002", "LAA003", "LAA004", "LAA005"}
REQUIRED_REVIEW_STATES = {
    "synthetic_preview_only",
    "needs_clinician_review",
    "needs_adjudication",
    "not_for_public_summary",
}
REQUIRED_DECISIONS = {
    "synthetic_preview_only",
    "needs_clinician_review",
    "needs_adjudication",
    "not_for_public_summary",
}
REQUIRED_REVIEW_LANES = {
    "provenance_review",
    "privacy_boundary_review",
    "label_definition_review",
    "clinician_review",
    "inter_rater_review",
    "label_quality_review",
    "public_release_boundary_review",
    "data_quality_review",
}
REQUIRED_PUBLIC_FILES = {
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
    "DATASET_EVALUATION_CARD_V0_1_DRAFT.md",
    "DATA_DICTIONARY.md",
    "LABELING.md",
    "docs/LABEL_DEFINITION_LOCK_V0_1.md",
    "docs/LABELING_PACKAGE_INDEX_V0_1.md",
    "data/inter_rater_review_subset_v0_1.tsv",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    "docs/label_audit/label_audit_example_intake_v0_1.json",
}
REQUIRED_COUNTS = {
    "synthetic_scenario_rows": 150,
    "prompt_rows": 70,
    "pilot_inter_rater_rows": 24,
    "turkish_synthetic_risk_rows": 14,
    "source_claim_review_queue_rows": 12,
}

REQUIRED_PHRASES = [
    "Label audit reviewer role table v0.1",
    "Status: generated public preview.",
    "Label audit reviewer roles: 4",
    "Label audit escalation gate rows: 5",
    "Synthetic scenario rows: 150",
    "Prompt rows: 70",
    "Pilot inter rater rows: 24",
    "Turkish synthetic risk rows: 14",
    "Source claim review queue rows: 12",
    "Synthetic provenance reviewer",
    "Label definition reviewer",
    "Pilot subset reviewer",
    "Public release boundary reviewer",
    "Synthetic provenance audit",
    "Label definition lock audit",
    "Pilot inter rater subset audit",
    "Raw output exclusion audit",
    "Public release boundary audit",
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
    "Passing this table is not clinical validation",
    "make label_audit_role_table",
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
    "docs/CLINICIAN_REVIEW_PROTOCOL_V0_1.md",
    "Label audit example intake rows",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    "docs/label_audit/label_audit_example_intake_v0_1.json",
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


def flatten(items: list[dict[str, Any]], key: str) -> set[str]:
    values: set[str] = set()
    for item in items:
        values.update(str(value) for value in item.get(key, []))
    return values


def main() -> int:
    errors: list[str] = []
    if not SOURCE.exists():
        errors.append(f"Missing source JSON: {SOURCE.relative_to(ROOT)}")
        data: dict[str, Any] = {"roles": [], "audit_rows": [], "linked_counts": {}}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    roles = data.get("roles", [])
    audit_rows = data.get("audit_rows", [])
    if not isinstance(roles, list):
        errors.append("roles must be a list")
        roles = []
    if not isinstance(audit_rows, list):
        errors.append("audit_rows must be a list")
        audit_rows = []
    if data.get("role_count") != 4:
        errors.append("role_count must be 4")
    if data.get("audit_row_count") != 5:
        errors.append("audit_row_count must be 5")
    if len(roles) != 4:
        errors.append(f"Expected 4 roles, found {len(roles)}")
    if len(audit_rows) != 5:
        errors.append(f"Expected 5 audit rows, found {len(audit_rows)}")

    for field in [
        "contains_patient_data",
        "synthetic_examples_only",
        "not_for_clinical_use",
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

    public_files = set(map(str, data.get("linked_public_files", [])))
    missing_files = sorted(REQUIRED_PUBLIC_FILES - public_files)
    if missing_files:
        errors.append(f"Missing public file links: {', '.join(missing_files)}")
    for relative_path in public_files:
        if not (ROOT / relative_path).exists():
            errors.append(f"Linked public file does not exist: {relative_path}")

    counts = data.get("linked_counts", {})
    for key, expected in REQUIRED_COUNTS.items():
        if counts.get(key) != expected:
            errors.append(f"{key} must be {expected}")

    review_states = set(map(str, data.get("linked_review_states", [])))
    missing_states = sorted(REQUIRED_REVIEW_STATES - review_states)
    if missing_states:
        errors.append(f"Missing review states: {', '.join(missing_states)}")

    found_roles = {str(role.get("role_id")) for role in roles}
    missing_roles = sorted(REQUIRED_ROLES - found_roles)
    if missing_roles:
        errors.append(f"Missing roles: {', '.join(missing_roles)}")
    found_audits = {str(row.get("audit_id")) for row in audit_rows}
    missing_audits = sorted(REQUIRED_AUDITS - found_audits)
    if missing_audits:
        errors.append(f"Missing audit rows: {', '.join(missing_audits)}")

    for role in roles:
        role_id = str(role.get("role_id", ""))
        for key in [
            "role_name",
            "purpose",
            "required_fields",
            "escalation_triggers",
            "release_gate_decision",
            "review_lanes",
        ]:
            if key not in role:
                errors.append(f"{role_id}: missing {key}")
        if len(role.get("required_fields", [])) < 7:
            errors.append(f"{role_id}: must include at least 7 required fields")
        if len(role.get("escalation_triggers", [])) < 4:
            errors.append(f"{role_id}: must include at least 4 escalation triggers")
        if str(role.get("release_gate_decision")) not in REQUIRED_DECISIONS:
            errors.append(f"{role_id}: unsupported release gate decision")

    found_lanes = flatten(roles, "review_lanes")
    missing_lanes = sorted(REQUIRED_REVIEW_LANES - found_lanes)
    if missing_lanes:
        errors.append(f"Missing review lanes: {', '.join(missing_lanes)}")

    for row in audit_rows:
        audit_id = str(row.get("audit_id", ""))
        for key in ["title", "linked_ids", "required_role_ids", "review_state", "required_outcome"]:
            if key not in row:
                errors.append(f"{audit_id}: missing {key}")
        if str(row.get("review_state")) not in REQUIRED_REVIEW_STATES:
            errors.append(f"{audit_id}: unsupported review state")
        for role_id in row.get("required_role_ids", []):
            if str(role_id) not in REQUIRED_ROLES:
                errors.append(f"{audit_id}: unknown required role {role_id}")

    if not TABLE.exists():
        errors.append(f"Missing generated table: {TABLE.relative_to(ROOT)}")
        text = ""
    else:
        text = TABLE.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Generated table missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing role table must not contain hyphen characters")

    if errors:
        print("FAIL label audit reviewer role table validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit reviewer role table validation")
    print(f"table={TABLE.relative_to(ROOT)}")
    print(f"roles={len(roles)}")
    print(f"audit_rows={len(audit_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
