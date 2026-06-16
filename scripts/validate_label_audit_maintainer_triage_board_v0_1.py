#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "label_audit" / "label_audit_maintainer_triage_board_v0_1.json"
MARKDOWN = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md"

REQUIRED_ACTIONS = {
    "add pilot subset limitation note",
    "block dataset quality proof wording",
    "keep raw outputs withheld",
    "rewrite provenance wording",
    "route to clinician wording review",
}
REQUIRED_DECISIONS = {
    "say dataset quality is not proven",
    "say pending clinician review",
    "say protocol testing only",
    "say raw outputs are withheld",
    "say synthetic example only",
}
REQUIRED_ROLES = {"LAR001", "LAR002", "LAR003", "LAR004"}
REQUIRED_FILES = [
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md",
    "docs/label_audit/label_audit_maintainer_triage_board_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
    "docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md",
]
REQUIRED_PHRASES = [
    "Label audit maintainer triage board v0.1",
    "Maintainer triage rows: 5",
    "Owner roles represented: 4",
    "Maintainer actions represented: 5",
    "Public wording decisions represented: 5",
    "Triage status values represented: 1",
    "ready_for_maintainer_review",
    "rewrite provenance wording",
    "route to clinician wording review",
    "add pilot subset limitation note",
    "keep raw outputs withheld",
    "block dataset quality proof wording",
    "say synthetic example only",
    "say pending clinician review",
    "say protocol testing only",
    "say raw outputs are withheld",
    "say dataset quality is not proven",
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
    "make label_audit_triage",
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
    if data.get("triage_row_count") != 5:
        errors.append("triage_row_count must be 5")
    if len(rows) != 5:
        errors.append(f"Expected 5 triage rows, found {len(rows)}")
    if data.get("owner_role_count") != 4:
        errors.append("owner_role_count must be 4")
    if data.get("maintainer_action_count") != 5:
        errors.append("maintainer_action_count must be 5")
    if data.get("public_wording_decision_count") != 5:
        errors.append("public_wording_decision_count must be 5")
    if data.get("triage_status_count") != 1:
        errors.append("triage_status_count must be 1")

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

    actions = {str(row.get("maintainer_action")) for row in rows}
    decisions = {str(row.get("public_wording_decision")) for row in rows}
    roles = {str(row.get("owner_role_id")) for row in rows}
    statuses = {str(row.get("triage_status")) for row in rows}
    if actions != REQUIRED_ACTIONS:
        errors.append("maintainer actions must match required action set")
    if decisions != REQUIRED_DECISIONS:
        errors.append("public wording decisions must match required decision set")
    if roles != REQUIRED_ROLES:
        errors.append("owner roles must represent all required roles")
    if statuses != {"ready_for_maintainer_review"}:
        errors.append("triage status must be ready_for_maintainer_review")

    for row in rows:
        row_id = str(row.get("example_id", ""))
        for key in [
            "title",
            "owner_role_id",
            "owner_role_name",
            "audit_id",
            "review_state",
            "blocked_public_claim_type",
            "maintainer_action",
            "triage_status",
            "public_wording_decision",
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
        errors.append("Generated outward facing triage board must not contain hyphen characters")

    if errors:
        print("FAIL label audit maintainer triage board validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit maintainer triage board validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"triage_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
