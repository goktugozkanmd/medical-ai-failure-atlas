#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_release_gate_outcome_dashboard_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md"

REQUIRED_OUTCOME_IDS = {"RQRGO001", "RQRGO002", "RQRGO003", "RQRGO004"}
REQUIRED_GATE_IDS = {"RQRG001", "RQRG002", "RQRG003", "RQRG004"}
REQUIRED_GATE_NAMES = {
    "Source support wording gate",
    "Policy wording source gate",
    "Escalation boundary wording gate",
    "Medication advice boundary gate",
}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
    "docs/reviewer_question_release_gate_outcome_dashboard_v0_1.json",
    "docs/REVIEWER_QUESTION_RELEASE_GATE_CHECKLIST_V0_1.md",
    "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
    "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
]
REQUIRED_PHRASES = [
    "Reviewer question release gate outcome dashboard v0.1",
    "Outcome rows: 4",
    "Pass state rows: 4",
    "Block state rows: 0",
    "Release decision values represented: 1",
    "allowed_for_public_preview",
    "Source support wording gate",
    "Policy wording source gate",
    "Escalation boundary wording gate",
    "Medication advice boundary gate",
    "locator format still needs source support",
    "policy source and clause are required",
    "escalation boundary remains under review",
    "individualized medication advice is blocked",
    "keep public preview wording",
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
    "make reviewer_question_gate_outcomes",
    "Add a reviewer question public release packet without scoring",
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
    "benchmark compatible",
    "score improved",
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
    if data.get("outcome_row_count") != 4:
        errors.append("outcome_row_count must be 4")
    if data.get("pass_state_count") != 4:
        errors.append("pass_state_count must be 4")
    if data.get("block_state_count") != 0:
        errors.append("block_state_count must be 0")
    if data.get("release_decision_count") != 1:
        errors.append("release_decision_count must be 1")
    if len(rows) != 4:
        errors.append(f"Expected 4 outcome rows, found {len(rows)}")

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

    outcome_ids = {str(row.get("outcome_id")) for row in rows}
    gate_ids = {str(row.get("release_gate_id")) for row in rows}
    gate_names = {str(row.get("gate_name")) for row in rows}
    states = {str(row.get("current_state")) for row in rows}
    decisions = {str(row.get("release_decision")) for row in rows}
    next_actions = {str(row.get("next_action")) for row in rows}
    if outcome_ids != REQUIRED_OUTCOME_IDS:
        errors.append("outcome id set must match required ids")
    if gate_ids != REQUIRED_GATE_IDS:
        errors.append("release gate id set must match required ids")
    if gate_names != REQUIRED_GATE_NAMES:
        errors.append("release gate name set must match required names")
    if states != {"pass"}:
        errors.append("all current states must be pass")
    if decisions != {"allowed_for_public_preview"}:
        errors.append("release decision must be allowed_for_public_preview")
    if next_actions != {"keep public preview wording"}:
        errors.append("next action must be keep public preview wording")

    for row in rows:
        outcome_id = str(row.get("outcome_id", ""))
        for key in [
            "release_gate_id",
            "gate_name",
            "intake_id",
            "benchmark_reviewer_question_id",
            "current_state",
            "release_decision",
            "required_public_wording",
            "blocked_wording",
            "evidence_surface",
            "track_a_value",
            "track_b_value",
            "next_action",
        ]:
            if key not in row:
                errors.append(f"{outcome_id}: missing {key}")

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
        errors.append("Generated outward facing outcome dashboard must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question release gate outcome dashboard validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question release gate outcome dashboard validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"outcome_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
