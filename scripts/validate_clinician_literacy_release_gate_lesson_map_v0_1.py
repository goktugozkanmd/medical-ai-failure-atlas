#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "clinician_literacy_release_gate_lesson_map_v0_1.json"
MAP = ROOT / "docs" / "CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md"

REQUIRED_TR_CASES = {f"TRFAI{index:03d}" for index in range(1, 15)}
REQUIRED_SOURCECHECKUP_ROWS = {f"SCQ_{index:03d}" for index in range(1, 13)}
REQUIRED_REVIEW_STATES = {
    "synthetic_preview_only",
    "needs_clinician_review",
    "needs_source_review",
}
REQUIRED_RELEASE_GATES = {
    "needs_clinician_review",
    "needs_source_review",
    "synthetic_preview_only",
    "blocked_missing_source_support",
    "blocked_pending_source_verification",
    "pass_local_sourcecheckup",
}
REQUIRED_ASSURANCE_GATES = {"L0", "L1", "L2", "L3", "L5"}

REQUIRED_PHRASES = [
    "Clinician literacy release gate lesson map v0.1",
    "Status: generated public preview.",
    "Lessons: 6",
    "Total minutes: 30",
    "TR MedLLM cases covered: 14",
    "SourceCheckup queue rows covered: 12",
    "Clinician review states represented: 3",
    "Release gate decisions represented: 6",
    "Assurance gate levels represented: 5",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not source truth certification",
    "not regulatory approval",
    "not an official endorsement",
    "SourceCheckup rows are review queue rows",
    "Assurance gate L5 remains blocked",
    "make clinician_literacy_map",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "officially endorsed",
    "regulatory approved",
    "sandbox access granted",
    "patient data used",
    "source proves",
    "model is safe",
    "best model",
]


def flatten(lessons: list[dict[str, Any]], key: str) -> set[str]:
    values: set[str] = set()
    for lesson in lessons:
        values.update(str(value) for value in lesson.get(key, []))
    return values


def main() -> int:
    errors: list[str] = []
    if not SOURCE.exists():
        errors.append(f"Missing source JSON: {SOURCE.relative_to(ROOT)}")
        data: dict[str, Any] = {"lessons": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))
    lessons = data.get("lessons", [])
    if not isinstance(lessons, list):
        errors.append("lessons must be a list")
        lessons = []

    if data.get("lesson_count") != 6:
        errors.append("lesson_count must be 6")
    if len(lessons) != 6:
        errors.append(f"Expected 6 lessons, found {len(lessons)}")
    if data.get("total_minutes") != 30:
        errors.append("total_minutes must be 30")
    if sum(int(lesson.get("minutes", 0)) for lesson in lessons) != 30:
        errors.append("Lesson minutes must sum to 30")

    for field in [
        "contains_patient_data",
        "synthetic_examples_only",
        "not_for_clinical_use",
        "no_clinical_deployment_claim",
        "no_clinical_validation_claim",
        "no_model_safety_claim",
        "no_model_ranking",
        "no_official_endorsement_claim",
    ]:
        expected = False if field == "contains_patient_data" else True
        if data.get(field) is not expected:
            errors.append(f"{field} must be {expected}")

    seen_ids: set[str] = set()
    for index, lesson in enumerate(lessons, start=1):
        lesson_id = str(lesson.get("lesson_id", ""))
        if not lesson_id.startswith("CLRG"):
            errors.append(f"Lesson {index}: lesson_id must start with CLRG")
        if lesson_id in seen_ids:
            errors.append(f"Duplicate lesson_id: {lesson_id}")
        seen_ids.add(lesson_id)
        for key in [
            "title",
            "learning_goal",
            "tr_medllm_case_ids",
            "sourcecheckup_queue_ids",
            "clinician_review_states",
            "release_gate_decisions",
            "assurance_gate_levels",
            "learner_task",
            "facilitator_check",
            "track_a_value",
            "track_b_value",
        ]:
            if key not in lesson:
                errors.append(f"{lesson_id}: missing {key}")
        if not lesson.get("tr_medllm_case_ids"):
            errors.append(f"{lesson_id}: at least one TR MedLLM case is required")
        if not lesson.get("release_gate_decisions"):
            errors.append(f"{lesson_id}: at least one release gate decision is required")

    tr_cases = flatten(lessons, "tr_medllm_case_ids")
    source_rows = flatten(lessons, "sourcecheckup_queue_ids")
    review_states = flatten(lessons, "clinician_review_states")
    release_gates = flatten(lessons, "release_gate_decisions")
    assurance_gates = flatten(lessons, "assurance_gate_levels")

    missing_tr_cases = sorted(REQUIRED_TR_CASES - tr_cases)
    if missing_tr_cases:
        errors.append(f"Missing TR MedLLM cases: {', '.join(missing_tr_cases)}")
    missing_source_rows = sorted(REQUIRED_SOURCECHECKUP_ROWS - source_rows)
    if missing_source_rows:
        errors.append(f"Missing SourceCheckup rows: {', '.join(missing_source_rows)}")
    for required in REQUIRED_REVIEW_STATES:
        if required not in review_states:
            errors.append(f"Missing review state: {required}")
    for required in REQUIRED_RELEASE_GATES:
        if required not in release_gates:
            errors.append(f"Missing release gate decision: {required}")
    for required in REQUIRED_ASSURANCE_GATES:
        if required not in assurance_gates:
            errors.append(f"Missing assurance gate level: {required}")

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
        print("FAIL clinician literacy release gate lesson map validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS clinician literacy release gate lesson map validation")
    print(f"map={MAP.relative_to(ROOT)}")
    print(f"lessons={len(lessons)}")
    print(f"minutes={data['total_minutes']}")
    print(f"tr_cases={len(tr_cases)}")
    print(f"sourcecheckup_rows={len(source_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
