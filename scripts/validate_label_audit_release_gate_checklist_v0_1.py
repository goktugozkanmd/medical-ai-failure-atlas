#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "label_audit" / "label_audit_release_gate_checklist_v0_1.json"
MARKDOWN = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md"

REQUIRED_GATE_IDS = {"LARG001", "LARG002", "LARG003", "LARG004", "LARG005"}
REQUIRED_GATE_NAMES = {
    "Synthetic provenance gate",
    "Label definition review gate",
    "Pilot subset scope gate",
    "Raw output release gate",
    "Dataset quality proof gate",
}
REQUIRED_PUBLIC_WORDING = {
    "synthetic example only",
    "pending clinician review",
    "protocol testing only",
    "raw outputs are withheld",
    "dataset quality is not proven",
}
REQUIRED_FILES = [
    "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md",
    "docs/label_audit/label_audit_release_gate_checklist_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md",
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
]
REQUIRED_PHRASES = [
    "Label audit release gate checklist v0.1",
    "Release gate rows: 5",
    "Pass state rows: 5",
    "Block state rows: 0",
    "allowed_for_public_preview",
    "Synthetic provenance gate",
    "Label definition review gate",
    "Pilot subset scope gate",
    "Raw output release gate",
    "Dataset quality proof gate",
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
    "make label_audit_release_gates",
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
    "dataset quality is proven",
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
    if data.get("release_gate_count") != 5:
        errors.append("release_gate_count must be 5")
    if data.get("pass_state_count") != 5:
        errors.append("pass_state_count must be 5")
    if data.get("block_state_count") != 0:
        errors.append("block_state_count must be 0")
    if len(rows) != 5:
        errors.append(f"Expected 5 gate rows, found {len(rows)}")

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

    gate_ids = {str(row.get("release_gate_id")) for row in rows}
    gate_names = {str(row.get("gate_name")) for row in rows}
    public_wording = {str(row.get("required_public_wording")) for row in rows}
    states = {str(row.get("current_state")) for row in rows}
    decisions = {str(row.get("release_decision")) for row in rows}
    if gate_ids != REQUIRED_GATE_IDS:
        errors.append("release gate id set must match required ids")
    if gate_names != REQUIRED_GATE_NAMES:
        errors.append("release gate name set must match required gate names")
    if public_wording != REQUIRED_PUBLIC_WORDING:
        errors.append("required public wording set must match wording log")
    if states != {"pass"}:
        errors.append("all current states must be pass")
    if decisions != {"allowed_for_public_preview"}:
        errors.append("release decision must be allowed_for_public_preview")

    for row in rows:
        gate_id = str(row.get("release_gate_id", ""))
        for key in [
            "example_id",
            "reviewer_role_id",
            "reviewer_role_name",
            "gate_question",
            "required_check",
            "blocked_wording",
            "required_public_wording",
            "current_state",
            "pass_state",
            "block_state",
            "evidence_surface",
        ]:
            if key not in row:
                errors.append(f"{gate_id}: missing {key}")

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
        errors.append("Generated outward facing release gate checklist must not contain hyphen characters")

    if errors:
        print("FAIL label audit release gate checklist validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit release gate checklist validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"release_gate_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
