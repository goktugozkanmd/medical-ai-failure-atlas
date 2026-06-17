#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_intake_triage_board_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md"

REQUIRED_ACTIONS = {
    "route to source support queue",
    "route to policy wording review",
    "route to escalation boundary review",
    "route to medication safety review",
}
REQUIRED_DECISIONS = {
    "say locator is not evidence",
    "say policy source is required",
    "say escalation remains visible",
    "say individualized medication advice is blocked",
}
REQUIRED_ROLES = {"RQTR001", "RQTR002", "RQTR003", "RQTR004"}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
    "docs/reviewer_question_intake_triage_board_v0_1.json",
    "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
    "docs/reviewer_question_intake_examples_v0_1.json",
    "docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md",
    "failure_atlas/public/CASE_INTAKE_CHECKLIST_V0_1.md",
]
REQUIRED_PHRASES = [
    "Reviewer question intake triage board v0.1",
    "Maintainer triage rows: 4",
    "Owner roles represented: 4",
    "Maintainer actions represented: 4",
    "Public wording decisions represented: 4",
    "Triage status values represented: 1",
    "ready_for_maintainer_review",
    "route to source support queue",
    "route to policy wording review",
    "route to escalation boundary review",
    "route to medication safety review",
    "say locator is not evidence",
    "say policy source is required",
    "say escalation remains visible",
    "say individualized medication advice is blocked",
    "not clinical advice",
    "not patient data",
    "not raw model output",
    "not clinical deployment",
    "not clinical validation",
    "not a benchmark compatibility claim",
    "not a benchmark equivalence claim",
    "not a score report",
    "not a model ranking",
    "not an endpoint result",
    "not an official endorsement",
    "make reviewer_question_intake_triage",
    "Add a public wording decision log for reviewer question intake triage without scoring",
]
FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "official approval",
    "official acceptance",
    "sandbox access granted",
    "patient data used",
    "model is safe",
    "best model",
    "proves safety",
    "benchmark compatible",
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
    if data.get("triage_row_count") != 4:
        errors.append("triage_row_count must be 4")
    if len(rows) != 4:
        errors.append(f"Expected 4 triage rows, found {len(rows)}")
    if data.get("owner_role_count") != 4:
        errors.append("owner_role_count must be 4")
    if data.get("maintainer_action_count") != 4:
        errors.append("maintainer_action_count must be 4")
    if data.get("public_wording_decision_count") != 4:
        errors.append("public_wording_decision_count must be 4")
    if data.get("triage_status_count") != 1:
        errors.append("triage_status_count must be 1")

    for field in [
        "contains_patient_data",
        "synthetic_examples_only",
        "not_for_clinical_use",
        "no_raw_model_output_release",
        "no_endpoint_result",
        "no_score_report",
        "no_model_ranking",
        "no_benchmark_compatibility_claim",
        "no_benchmark_equivalence_claim",
        "no_clinical_deployment_claim",
        "no_clinical_validation_claim",
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
        row_id = str(row.get("intake_id", ""))
        for key in [
            "template",
            "benchmark_reviewer_question_id",
            "owner_role_id",
            "owner_role_name",
            "review_state",
            "blocked_public_claim_type",
            "maintainer_action",
            "triage_status",
            "public_wording_decision",
            "next_public_surface",
            "track_a_value",
            "track_b_value",
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
        print("FAIL reviewer question intake triage board validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question intake triage board validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"triage_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
