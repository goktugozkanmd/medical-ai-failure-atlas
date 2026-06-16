#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "label_audit" / "label_audit_example_intake_v0_1.json"
MARKDOWN = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md"

REQUIRED_ROLES = {"LAR001", "LAR002", "LAR003", "LAR004"}
REQUIRED_AUDITS = {"LAA001", "LAA002", "LAA003", "LAA004", "LAA005"}
REQUIRED_EXAMPLES = {"LAE001", "LAE002", "LAE003", "LAE004", "LAE005"}
REQUIRED_CHECKS = {
    "synthetic_provenance",
    "patient_data_absence",
    "label_lock_match",
    "pilot_subset_framing",
    "raw_output_exclusion",
    "dataset_quality_proof_boundary",
    "clinical_validation_boundary",
    "public_release_boundary",
}
REQUIRED_COUNTS = {
    "synthetic_scenario_rows": 150,
    "prompt_rows": 70,
    "pilot_inter_rater_rows": 24,
    "turkish_synthetic_risk_rows": 14,
    "source_claim_review_queue_rows": 12,
}
REQUIRED_FILES = [
    ".github/ISSUE_TEMPLATE/label_audit_review.yml",
    "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
    "docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md",
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
    "docs/label_audit/label_audit_example_intake_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
]
REQUIRED_PHRASES = [
    "Label audit example intake v0.1",
    "Label audit examples: 5",
    "Synthetic scenario rows: 150",
    "Prompt rows: 70",
    "Pilot inter rater rows: 24",
    "Turkish synthetic risk rows: 14",
    "Source claim review queue rows: 12",
    "Synthetic provenance overclaim",
    "Label definition drift",
    "Pilot subset overinterpretation",
    "Raw output exclusion boundary",
    "Dataset quality proof boundary",
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
    "make label_audit_examples",
    ".github/ISSUE_TEMPLATE/label_audit_review.yml",
    "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
    "docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md",
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
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
        data: dict[str, Any] = {"examples": [], "linked_counts": {}}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    examples = data.get("examples", [])
    if not isinstance(examples, list):
        errors.append("examples must be a list")
        examples = []
    if data.get("example_count") != 5:
        errors.append("example_count must be 5")
    if len(examples) != 5:
        errors.append(f"Expected 5 examples, found {len(examples)}")

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

    roles = set(map(str, data.get("linked_role_ids", [])))
    audits = set(map(str, data.get("linked_audit_ids", [])))
    if REQUIRED_ROLES - roles:
        errors.append(f"Missing linked roles: {', '.join(sorted(REQUIRED_ROLES - roles))}")
    if REQUIRED_AUDITS - audits:
        errors.append(f"Missing linked audits: {', '.join(sorted(REQUIRED_AUDITS - audits))}")

    counts = data.get("linked_counts", {})
    for key, expected in REQUIRED_COUNTS.items():
        if counts.get(key) != expected:
            errors.append(f"{key} must be {expected}")

    found_examples = {str(row.get("example_id")) for row in examples}
    if REQUIRED_EXAMPLES - found_examples:
        errors.append(f"Missing examples: {', '.join(sorted(REQUIRED_EXAMPLES - found_examples))}")

    found_checks: set[str] = set()
    for row in examples:
        example_id = str(row.get("example_id", ""))
        for key in [
            "title",
            "audit_surface",
            "suggested_role_id",
            "linked_audit_id",
            "exact_boundary_to_review",
            "required_checks",
            "proposed_public_action",
            "review_state",
        ]:
            if key not in row:
                errors.append(f"{example_id}: missing {key}")
        if str(row.get("suggested_role_id")) not in REQUIRED_ROLES:
            errors.append(f"{example_id}: unknown role")
        if str(row.get("linked_audit_id")) not in REQUIRED_AUDITS:
            errors.append(f"{example_id}: unknown audit")
        checks = set(map(str, row.get("required_checks", [])))
        if len(checks) < 4:
            errors.append(f"{example_id}: must include at least 4 required checks")
        found_checks.update(checks)

    if REQUIRED_CHECKS - found_checks:
        errors.append(f"Missing required checks: {', '.join(sorted(REQUIRED_CHECKS - found_checks))}")

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
        errors.append("Generated outward facing example intake must not contain hyphen characters")

    if errors:
        print("FAIL label audit example intake validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit example intake validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"examples={len(examples)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
