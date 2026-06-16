#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "label_audit" / "label_audit_public_wording_decision_log_v0_1.json"
MARKDOWN = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md"

REQUIRED_BLOCKED_WORDING = {
    "clinically validated labels",
    "covers real care records",
    "proves dataset quality",
    "raw outputs are available in public",
    "representative of deployment performance",
}
REQUIRED_PROPOSED_WORDING = {
    "dataset quality is not proven",
    "pending clinician review",
    "protocol testing only",
    "raw outputs are withheld",
    "synthetic example only",
}
REQUIRED_FILES = [
    "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/label_audit/label_audit_public_wording_decision_log_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md",
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
]
REQUIRED_PHRASES = [
    "Label audit public wording decision log v0.1",
    "Public wording decision rows: 5",
    "Blocked wording examples: 5",
    "Proposed public wording examples: 5",
    "Decision status values represented: 1",
    "safe_public_wording_ready",
    "covers real care records",
    "clinically validated labels",
    "representative of deployment performance",
    "raw outputs are available in public",
    "proves dataset quality",
    "synthetic example only",
    "pending clinician review",
    "protocol testing only",
    "raw outputs are withheld",
    "dataset quality is not proven",
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
    "make label_audit_wording_log",
]
FORBIDDEN_PHRASES = [
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "officially endorsed",
    "regulatory approved",
    "sandbox access granted",
    "patient data used",
    "model is safe",
    "best model",
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
    if data.get("decision_row_count") != 5:
        errors.append("decision_row_count must be 5")
    if len(rows) != 5:
        errors.append(f"Expected 5 decision rows, found {len(rows)}")
    if data.get("blocked_wording_count") != 5:
        errors.append("blocked_wording_count must be 5")
    if data.get("proposed_public_wording_count") != 5:
        errors.append("proposed_public_wording_count must be 5")
    if data.get("decision_status_count") != 1:
        errors.append("decision_status_count must be 1")

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

    blocked = {str(row.get("blocked_wording")) for row in rows}
    proposed = {str(row.get("proposed_public_wording")) for row in rows}
    statuses = {str(row.get("decision_status")) for row in rows}
    if blocked != REQUIRED_BLOCKED_WORDING:
        errors.append("blocked wording set must match required examples")
    if proposed != REQUIRED_PROPOSED_WORDING:
        errors.append("proposed wording set must match required examples")
    if statuses != {"safe_public_wording_ready"}:
        errors.append("decision status must be safe_public_wording_ready")

    for row in rows:
        row_id = str(row.get("example_id", ""))
        for key in [
            "reviewer_role_id",
            "reviewer_role_name",
            "blocked_wording",
            "proposed_public_wording",
            "decision_status",
            "maintainer_action",
            "next_public_surface",
        ]:
            if key not in row:
                errors.append(f"{row_id}: missing {key}")

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
        errors.append("Generated outward facing wording decision log must not contain hyphen characters")

    if errors:
        print("FAIL label audit public wording decision log validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit public wording decision log validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"decision_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
