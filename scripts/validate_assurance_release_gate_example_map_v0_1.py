#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "assurance_release_gate_example_map_v0_1.json"
MAP = ROOT / "docs" / "ASSURANCE_RELEASE_GATE_EXAMPLE_MAP_V0_1.md"

REQUIRED_TR_CASES = {f"TRFAI{index:03d}" for index in range(1, 15)}
REQUIRED_SOURCECHECKUP_ROWS = {f"SCQ_{index:03d}" for index in range(1, 13)}
REQUIRED_SECTIONS = {
    "card_identity",
    "model_card",
    "patient_data_and_privacy_boundary",
    "risk_card",
    "data_card",
    "source_support_card",
    "human_review_card",
    "audit_trail",
    "release_gate_levels",
    "public_action_checklist",
}
REQUIRED_GATE_LEVELS = {"L0", "L1", "L2", "L3", "L4", "L5"}
REQUIRED_DECISIONS = {
    "needs_clinician_review",
    "needs_source_review",
    "synthetic_preview_only",
    "public_candidate_boundary_ready",
    "blocked_clinical_deployment",
}

REQUIRED_PHRASES = [
    "Assurance release gate example map v0.1",
    "Status: generated public preview.",
    "Examples: 6",
    "TR MedLLM cases covered: 14",
    "SourceCheckup queue rows covered: 12",
    "Assurance card sections covered: 10",
    "Release gate levels represented: 6",
    "Release gate decisions represented: 5",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not source truth certification",
    "not regulatory approval",
    "not an official endorsement",
    "L4 external pilot language requires separate explicit clearance",
    "Assurance gate L5 remains blocked",
    "make assurance_release_gate_map",
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


def flatten(examples: list[dict[str, Any]], key: str) -> set[str]:
    values: set[str] = set()
    for example in examples:
        values.update(str(value) for value in example.get(key, []))
    return values


def main() -> int:
    errors: list[str] = []
    if not SOURCE.exists():
        errors.append(f"Missing source JSON: {SOURCE.relative_to(ROOT)}")
        data: dict[str, Any] = {"examples": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    examples = data.get("examples", [])
    if not isinstance(examples, list):
        errors.append("examples must be a list")
        examples = []
    if data.get("example_count") != 6:
        errors.append("example_count must be 6")
    if len(examples) != 6:
        errors.append(f"Expected 6 examples, found {len(examples)}")

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
    for index, example in enumerate(examples, start=1):
        example_id = str(example.get("example_id", ""))
        if not example_id.startswith("ARG"):
            errors.append(f"Example {index}: example_id must start with ARG")
        if example_id in seen_ids:
            errors.append(f"Duplicate example_id: {example_id}")
        seen_ids.add(example_id)
        for key in [
            "title",
            "linked_lesson_ids",
            "tr_medllm_case_ids",
            "sourcecheckup_queue_ids",
            "assurance_card_sections",
            "release_gate_levels",
            "release_gate_decision",
            "minimum_required_review",
            "main_blocker",
            "allowed_public_phrase",
            "blocked_public_phrase",
            "track_a_value",
            "track_b_value",
        ]:
            if key not in example:
                errors.append(f"{example_id}: missing {key}")
        for blocked_phrase in ["clinically validated", "safe dose recommendation", "official sandbox role"]:
            if blocked_phrase in str(example.get("allowed_public_phrase", "")).lower():
                errors.append(f"{example_id}: allowed_public_phrase contains unsafe phrase")

    tr_cases = flatten(examples, "tr_medllm_case_ids")
    source_rows = flatten(examples, "sourcecheckup_queue_ids")
    sections = flatten(examples, "assurance_card_sections")
    levels = flatten(examples, "release_gate_levels")
    decisions = {str(example.get("release_gate_decision", "")) for example in examples}

    missing_tr_cases = sorted(REQUIRED_TR_CASES - tr_cases)
    if missing_tr_cases:
        errors.append(f"Missing TR MedLLM cases: {', '.join(missing_tr_cases)}")
    missing_source_rows = sorted(REQUIRED_SOURCECHECKUP_ROWS - source_rows)
    if missing_source_rows:
        errors.append(f"Missing SourceCheckup rows: {', '.join(missing_source_rows)}")
    missing_sections = sorted(REQUIRED_SECTIONS - sections)
    if missing_sections:
        errors.append(f"Missing assurance card sections: {', '.join(missing_sections)}")
    missing_levels = sorted(REQUIRED_GATE_LEVELS - levels)
    if missing_levels:
        errors.append(f"Missing release gate levels: {', '.join(missing_levels)}")
    missing_decisions = sorted(REQUIRED_DECISIONS - decisions)
    if missing_decisions:
        errors.append(f"Missing release gate decisions: {', '.join(missing_decisions)}")

    if not MAP.exists():
        errors.append(f"Missing generated map: {MAP.relative_to(ROOT)}")
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
        errors.append("Generated outward facing map must not contain hyphen characters")

    if errors:
        print("FAIL assurance release gate example map validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS assurance release gate example map validation")
    print(f"map={MAP.relative_to(ROOT)}")
    print(f"examples={len(examples)}")
    print(f"tr_cases={len(tr_cases)}")
    print(f"sourcecheckup_rows={len(source_rows)}")
    print(f"assurance_sections={len(sections)}")
    print(f"gate_levels={len(levels)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
