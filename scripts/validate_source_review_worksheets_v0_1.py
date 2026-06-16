#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "source_review_worksheets_v0_1.json"
MAP = ROOT / "docs" / "SOURCE_REVIEW_WORKSHEETS_V0_1.md"

REQUIRED_WORKSHEETS = {"SRW001", "SRW002"}
REQUIRED_ROUTES = {"STM002", "STM004"}
REQUIRED_SOURCECHECKUP_ROWS = {"SCQ_002", "SCQ_005", "SCQ_009", "SCQ_011"}
REQUIRED_TR_CASES = {"TRFAI001", "TRFAI006", "TRFAI008", "TRFAI010", "TRFAI011", "TRFAI014"}
REQUIRED_ASSURANCE_EXAMPLES = {"ARG002", "ARG006"}
REQUIRED_SOURCE_SURFACES = {"doi", "guideline", "policy"}
REQUIRED_RISK_AXES = {"medication_safety", "missing_context", "over_treatment", "workflow_mismatch"}
REQUIRED_GATE_LEVELS = {"L1", "L2", "L3", "L4", "L5"}
REQUIRED_REVIEW_LANES = {
    "source_locator_review",
    "clinician_source_review",
    "medication_safety_review",
    "policy_claim_review",
    "assurance_boundary_review",
    "public_wording_review",
}
REQUIRED_DECISIONS = {
    "needs_clinician_source_review",
    "blocked_official_or_deployment_claim",
}

REQUIRED_PHRASES = [
    "Source review worksheets v0.1",
    "Status: generated public preview.",
    "Worksheets: 2",
    "SourceCheckup TR MedLLM routes covered: 2",
    "SourceCheckup queue rows covered: 4",
    "TR MedLLM cases covered: 6",
    "Assurance release gate examples covered: 2",
    "Source surfaces represented: 3",
    "Risk axes represented: 4",
    "Release gate levels represented: 5",
    "Review lanes represented: 6",
    "Routing decisions represented: 2",
    "Medication safety source review worksheet",
    "Policy wording source review worksheet",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not source truth certification",
    "not regulatory approval",
    "not an official endorsement",
    "Medication advice remains blocked",
    "Policy, sandbox, pilot, official route, and deployment language remains blocked",
    "make source_review_worksheets",
    "docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md",
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


def flatten(worksheets: list[dict[str, Any]], key: str) -> set[str]:
    values: set[str] = set()
    for worksheet in worksheets:
        values.update(str(value) for value in worksheet.get(key, []))
    return values


def main() -> int:
    errors: list[str] = []
    if not SOURCE.exists():
        errors.append(f"Missing source JSON: {SOURCE.relative_to(ROOT)}")
        data: dict[str, Any] = {"worksheets": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    worksheets = data.get("worksheets", [])
    if not isinstance(worksheets, list):
        errors.append("worksheets must be a list")
        worksheets = []
    if data.get("worksheet_count") != 2:
        errors.append("worksheet_count must be 2")
    if len(worksheets) != 2:
        errors.append(f"Expected 2 worksheets, found {len(worksheets)}")

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
    for index, worksheet in enumerate(worksheets, start=1):
        worksheet_id = str(worksheet.get("worksheet_id", ""))
        if not worksheet_id.startswith("SRW"):
            errors.append(f"Worksheet {index}: worksheet_id must start with SRW")
        if worksheet_id in seen_ids:
            errors.append(f"Duplicate worksheet_id: {worksheet_id}")
        seen_ids.add(worksheet_id)
        for key in [
            "title",
            "linked_route_ids",
            "linked_sourcecheckup_queue_ids",
            "linked_tr_medllm_case_ids",
            "linked_assurance_example_ids",
            "source_surfaces",
            "risk_axes",
            "release_gate_levels",
            "routing_decision",
            "review_lanes",
            "blocked_claim_patterns",
            "minimum_evidence_fields",
            "review_questions",
            "allowed_public_output",
            "blocked_public_output",
            "pass_condition",
            "fail_condition",
            "track_a_value",
            "track_b_value",
            "next_public_action",
        ]:
            if key not in worksheet:
                errors.append(f"{worksheet_id}: missing {key}")
        if len(worksheet.get("blocked_claim_patterns", [])) < 5:
            errors.append(f"{worksheet_id}: must include at least 5 blocked claim patterns")
        if len(worksheet.get("minimum_evidence_fields", [])) < 10:
            errors.append(f"{worksheet_id}: must include at least 10 minimum evidence fields")
        if len(worksheet.get("review_questions", [])) < 5:
            errors.append(f"{worksheet_id}: must include at least 5 review questions")

    checks = [
        ("worksheets", REQUIRED_WORKSHEETS, {str(worksheet.get("worksheet_id", "")) for worksheet in worksheets}),
        ("routes", REQUIRED_ROUTES, flatten(worksheets, "linked_route_ids")),
        ("SourceCheckup rows", REQUIRED_SOURCECHECKUP_ROWS, flatten(worksheets, "linked_sourcecheckup_queue_ids")),
        ("TR MedLLM cases", REQUIRED_TR_CASES, flatten(worksheets, "linked_tr_medllm_case_ids")),
        ("Assurance examples", REQUIRED_ASSURANCE_EXAMPLES, flatten(worksheets, "linked_assurance_example_ids")),
        ("Source surfaces", REQUIRED_SOURCE_SURFACES, flatten(worksheets, "source_surfaces")),
        ("Risk axes", REQUIRED_RISK_AXES, flatten(worksheets, "risk_axes")),
        ("Release gate levels", REQUIRED_GATE_LEVELS, flatten(worksheets, "release_gate_levels")),
        ("Review lanes", REQUIRED_REVIEW_LANES, flatten(worksheets, "review_lanes")),
        ("Routing decisions", REQUIRED_DECISIONS, {str(worksheet.get("routing_decision", "")) for worksheet in worksheets}),
    ]
    for label, required, found in checks:
        missing = sorted(required - found)
        if missing:
            errors.append(f"Missing {label}: {', '.join(missing)}")

    if not MAP.exists():
        errors.append(f"Missing generated worksheets: {MAP.relative_to(ROOT)}")
        text = ""
    else:
        text = MAP.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Map missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing worksheets must not contain hyphen characters")

    if errors:
        print("FAIL source review worksheets validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS source review worksheets validation")
    print(f"worksheets={MAP.relative_to(ROOT)}")
    print(f"worksheet_count={len(worksheets)}")
    print(f"routes={len(flatten(worksheets, 'linked_route_ids'))}")
    print(f"sourcecheckup_rows={len(flatten(worksheets, 'linked_sourcecheckup_queue_ids'))}")
    print(f"tr_cases={len(flatten(worksheets, 'linked_tr_medllm_case_ids'))}")
    print(f"review_lanes={len(flatten(worksheets, 'review_lanes'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
