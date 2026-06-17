#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "label_audit" / "label_audit_maintainer_public_preview_handoff_summary_v0_1.json"
MARKDOWN = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_MAINTAINER_PUBLIC_PREVIEW_HANDOFF_SUMMARY_V0_1.md"

REQUIRED_HANDOFF_IDS = {"LAPH001", "LAPH002", "LAPH003", "LAPH004", "LAPH005"}
REQUIRED_DECISION_IDS = {"LAMP001", "LAMP002", "LAMP003", "LAMP004", "LAMP005"}
REQUIRED_FILES = [
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_PUBLIC_PREVIEW_HANDOFF_SUMMARY_V0_1.md",
    "docs/label_audit/label_audit_maintainer_public_preview_handoff_summary_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_PUBLIC_PREVIEW_DECISION_LOG_V0_1.md",
    "docs/label_audit/label_audit_maintainer_public_preview_decision_log_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_RELEASE_CANDIDATE_SUMMARY_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
    "Makefile",
]
REQUIRED_PHRASES = [
    "Label audit maintainer public preview handoff summary v0.1",
    "Handoff rows: 5",
    "Decision rows represented: 5",
    "Candidate summary rows represented: 5",
    "Audit trail rows represented: 5",
    "Evidence rows represented: 5",
    "Readiness rows represented: 5",
    "Closeout rows represented: 5",
    "Handoff rows represented: 5",
    "Contributor digest rows represented: 5",
    "Release index surface rows represented: 9",
    "Previous public issue represented: 37",
    "current public preview route only",
    "ready_for_maintainer_public_preview_review",
    "Synthetic boundary handoff",
    "Intake pattern handoff",
    "Public wording handoff",
    "Release surface handoff",
    "Validation handoff",
    "dataset quality proof",
    "clinical readiness",
    "clinical validation",
    "clinical deployment",
    "model safety proof",
    "model ranking",
    "official endorsement",
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
    "make label_audit_maintainer_public_preview_handoff_summary",
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
    if data.get("handoff_row_count") != 5:
        errors.append("handoff_row_count must be 5")
    if data.get("decision_rows_represented") != 5:
        errors.append("decision_rows_represented must be 5")
    if data.get("candidate_summary_rows_represented") != 5:
        errors.append("candidate_summary_rows_represented must be 5")
    if data.get("audit_trail_rows_represented") != 5:
        errors.append("audit_trail_rows_represented must be 5")
    if data.get("evidence_rows_represented") != 5:
        errors.append("evidence_rows_represented must be 5")
    if data.get("readiness_rows_represented") != 5:
        errors.append("readiness_rows_represented must be 5")
    if data.get("closeout_rows_represented") != 5:
        errors.append("closeout_rows_represented must be 5")
    if data.get("handoff_rows_represented") != 5:
        errors.append("handoff_rows_represented must be 5")
    if data.get("contributor_digest_rows_represented") != 5:
        errors.append("contributor_digest_rows_represented must be 5")
    if data.get("release_index_surface_rows_represented") != 9:
        errors.append("release_index_surface_rows_represented must be 9")
    if data.get("previous_public_issue_number") != 37:
        errors.append("previous_public_issue_number must be 37")
    if data.get("public_preview_handoff") != "ready_for_maintainer_public_preview_review":
        errors.append("public_preview_handoff must be ready_for_maintainer_public_preview_review")
    if data.get("maintainer_review_scope") != "current public preview route only":
        errors.append("maintainer_review_scope must be current public preview route only")
    if len(rows) != 5:
        errors.append(f"Expected 5 handoff rows, found {len(rows)}")

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

    handoff_ids = {str(row.get("handoff_id")) for row in rows}
    if handoff_ids != REQUIRED_HANDOFF_IDS:
        errors.append("handoff id set must match required ids")
    decision_ids = {str(row.get("source_decision_id")) for row in rows}
    if decision_ids != REQUIRED_DECISION_IDS:
        errors.append("source decision id set must match required ids")
    if {str(row.get("handoff_state")) for row in rows} != {"ready_for_maintainer_public_preview_review"}:
        errors.append("all handoff states must be ready_for_maintainer_public_preview_review")

    for row in rows:
        handoff_id = str(row.get("handoff_id", ""))
        for key in ["handoff_name", "source_decision_id", "handoff_owner", "next_reviewer_action", "handoff_state", "handoff_boundary", "blocked_claims"]:
            if key not in row:
                errors.append(f"{handoff_id}: missing {key}")

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
        errors.append("Generated outward facing maintainer public preview handoff summary must not contain hyphen characters")

    if errors:
        print("FAIL label audit maintainer public preview handoff summary validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit maintainer public preview handoff summary validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"handoff_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
