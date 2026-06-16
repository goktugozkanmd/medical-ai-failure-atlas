#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "red_flag_warning_checklist_v0_1.json"
MAP = ROOT / "docs" / "RED_FLAG_WARNING_CHECKLIST_V0_1.md"

REQUIRED_CHECKLISTS = {"RFW001", "RFW002", "RFW003"}
REQUIRED_ROUTES = {"STM003"}
REQUIRED_SOURCECHECKUP_ROWS = {"SCQ_003"}
REQUIRED_TR_CASES = {"TRFAI003", "TRFAI009"}
REQUIRED_ASSURANCE_EXAMPLES = {"ARG001"}
REQUIRED_TAXONOMY_PATTERNS = {"T01", "T03", "T05", "T07"}
REQUIRED_RISK_AXES = {"false_reassurance", "rare_danger", "communication_risk", "source_support"}
REQUIRED_GATE_LEVELS = {"L1", "L2"}
REQUIRED_REVIEW_LANES = {
    "clinician_review",
    "warning_sign_wording_review",
    "source_locator_review",
    "assurance_boundary_review",
    "clinician_source_review",
}

REQUIRED_PHRASES = [
    "Red flag source locator and warning sign checklist v0.1",
    "Status: generated public preview.",
    "Checklists: 3",
    "SourceCheckup TR MedLLM routes covered: 1",
    "SourceCheckup queue rows covered: 1",
    "TR MedLLM cases covered: 2",
    "Assurance release gate examples covered: 1",
    "Failure Atlas taxonomy patterns covered: 4",
    "Risk axes represented: 4",
    "Release gate levels represented: 2",
    "Review lanes represented: 5",
    "Partial negative evidence red flag checklist",
    "Symptom fluctuation rare danger checklist",
    "Source locator triage claim checklist",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not source truth certification",
    "not regulatory approval",
    "not an official endorsement",
    "Red flag wording review is not clinical triage",
    "A source locator is not proof of safety",
    "Passing this checklist is not clinical validation",
    "Public wording must keep unresolved danger variables visible",
    "make red_flag_warning_checklist",
    "docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md",
    "docs/SOURCE_REVIEW_WORKSHEETS_V0_1.md",
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
    "source proves",
    "model is safe",
    "best model",
]


def flatten(checklists: list[dict[str, Any]], key: str) -> set[str]:
    values: set[str] = set()
    for checklist in checklists:
        values.update(str(value) for value in checklist.get(key, []))
    return values


def main() -> int:
    errors: list[str] = []
    if not SOURCE.exists():
        errors.append(f"Missing source JSON: {SOURCE.relative_to(ROOT)}")
        data: dict[str, Any] = {"checklists": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    checklists = data.get("checklists", [])
    if not isinstance(checklists, list):
        errors.append("checklists must be a list")
        checklists = []
    if data.get("checklist_count") != 3:
        errors.append("checklist_count must be 3")
    if len(checklists) != 3:
        errors.append(f"Expected 3 checklists, found {len(checklists)}")

    for field in [
        "contains_patient_data",
        "synthetic_examples_only",
        "not_for_clinical_use",
        "no_clinical_deployment_claim",
        "no_clinical_validation_claim",
        "no_model_safety_claim",
        "no_model_ranking",
        "no_source_truth_certification",
        "no_official_endorsement_claim",
    ]:
        expected = False if field == "contains_patient_data" else True
        if data.get(field) is not expected:
            errors.append(f"{field} must be {expected}")

    seen_ids: set[str] = set()
    for index, checklist in enumerate(checklists, start=1):
        checklist_id = str(checklist.get("checklist_id", ""))
        if not checklist_id.startswith("RFW"):
            errors.append(f"Checklist {index}: checklist_id must start with RFW")
        if checklist_id in seen_ids:
            errors.append(f"Duplicate checklist_id: {checklist_id}")
        seen_ids.add(checklist_id)
        for key in [
            "title",
            "linked_route_ids",
            "linked_sourcecheckup_queue_ids",
            "linked_tr_medllm_case_ids",
            "linked_assurance_example_ids",
            "linked_taxonomy_pattern_ids",
            "risk_axes",
            "review_lanes",
            "release_gate_levels",
            "blocked_patterns",
            "minimum_review_fields",
            "review_questions",
            "safe_wording_expectation",
            "allowed_public_output",
            "blocked_public_output",
            "track_a_value",
            "track_b_value",
            "next_public_action",
        ]:
            if key not in checklist:
                errors.append(f"{checklist_id}: missing {key}")
        if len(checklist.get("blocked_patterns", [])) < 5:
            errors.append(f"{checklist_id}: must include at least 5 blocked patterns")
        if len(checklist.get("minimum_review_fields", [])) < 10:
            errors.append(f"{checklist_id}: must include at least 10 minimum review fields")
        if len(checklist.get("review_questions", [])) < 5:
            errors.append(f"{checklist_id}: must include at least 5 review questions")

    checks = [
        ("checklists", REQUIRED_CHECKLISTS, {str(checklist.get("checklist_id", "")) for checklist in checklists}),
        ("routes", REQUIRED_ROUTES, flatten(checklists, "linked_route_ids")),
        ("SourceCheckup rows", REQUIRED_SOURCECHECKUP_ROWS, flatten(checklists, "linked_sourcecheckup_queue_ids")),
        ("TR MedLLM cases", REQUIRED_TR_CASES, flatten(checklists, "linked_tr_medllm_case_ids")),
        ("Assurance examples", REQUIRED_ASSURANCE_EXAMPLES, flatten(checklists, "linked_assurance_example_ids")),
        ("Taxonomy patterns", REQUIRED_TAXONOMY_PATTERNS, flatten(checklists, "linked_taxonomy_pattern_ids")),
        ("Risk axes", REQUIRED_RISK_AXES, flatten(checklists, "risk_axes")),
        ("Release gate levels", REQUIRED_GATE_LEVELS, flatten(checklists, "release_gate_levels")),
        ("Review lanes", REQUIRED_REVIEW_LANES, flatten(checklists, "review_lanes")),
    ]
    for label, required, found in checks:
        missing = sorted(required - found)
        if missing:
            errors.append(f"Missing {label}: {', '.join(missing)}")

    if not MAP.exists():
        errors.append(f"Missing generated checklist: {MAP.relative_to(ROOT)}")
        text = ""
    else:
        text = MAP.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Checklist missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing checklist must not contain hyphen characters")

    if errors:
        print("FAIL red flag warning checklist validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS red flag warning checklist validation")
    print(f"checklist={MAP.relative_to(ROOT)}")
    print(f"checklists={len(checklists)}")
    print(f"routes={len(flatten(checklists, 'linked_route_ids'))}")
    print(f"sourcecheckup_rows={len(flatten(checklists, 'linked_sourcecheckup_queue_ids'))}")
    print(f"tr_cases={len(flatten(checklists, 'linked_tr_medllm_case_ids'))}")
    print(f"review_lanes={len(flatten(checklists, 'review_lanes'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
