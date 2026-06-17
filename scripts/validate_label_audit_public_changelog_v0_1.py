#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "label_audit" / "label_audit_public_changelog_v0_1.json"
MARKDOWN = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_PUBLIC_CHANGELOG_V0_1.md"

REQUIRED_CHANGE_IDS = {"LAC001", "LAC002", "LAC003", "LAC004", "LAC005", "LAC006", "LAC007", "LAC008"}
REQUIRED_FILES = [
    "docs/label_audit/LABEL_AUDIT_PUBLIC_CHANGELOG_V0_1.md",
    "docs/label_audit/label_audit_public_changelog_v0_1.json",
    "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_RELEASE_NOTE_PACKET_V0_1.md",
]
REQUIRED_PHRASES = [
    "Label audit public changelog v0.1",
    "Change rows: 8",
    "Release note packet rows represented: 7",
    "Latest change id: `LAC008`",
    "ready_for_public_preview",
    "Public contributor route",
    "Example intake rows",
    "Example dashboard",
    "Maintainer triage board",
    "Public wording decision log",
    "Release gate checklist",
    "Release gate outcome dashboard",
    "Release note packet",
    "public_preview_added",
    "synthetic only and not for clinical use",
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
    "make label_audit_changelog",
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
    if data.get("change_row_count") != 8:
        errors.append("change_row_count must be 8")
    if data.get("release_note_packet_rows_represented") != 7:
        errors.append("release_note_packet_rows_represented must be 7")
    if data.get("latest_change_id") != "LAC008":
        errors.append("latest_change_id must be LAC008")
    if data.get("changelog_decision") != "ready_for_public_preview":
        errors.append("changelog_decision must be ready_for_public_preview")
    if len(rows) != 8:
        errors.append(f"Expected 8 change rows, found {len(rows)}")

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

    change_ids = {str(row.get("change_id")) for row in rows}
    statuses = {str(row.get("change_status")) for row in rows}
    if change_ids != REQUIRED_CHANGE_IDS:
        errors.append("change id set must match required ids")
    if statuses != {"public_preview_added"}:
        errors.append("all change statuses must be public_preview_added")

    for row in rows:
        change_id = str(row.get("change_id", ""))
        for key in ["date", "surface_name", "public_file", "public_value", "change_status", "boundary", "next_action"]:
            if key not in row:
                errors.append(f"{change_id}: missing {key}")

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
        errors.append("Generated outward facing changelog must not contain hyphen characters")

    if errors:
        print("FAIL label audit public changelog validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit public changelog validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"change_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
