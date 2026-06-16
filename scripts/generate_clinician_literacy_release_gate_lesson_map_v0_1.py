#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "clinician_literacy_release_gate_lesson_map_v0_1.json"
OUTPUT = ROOT / "docs" / "CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten(lessons: list[dict[str, Any]], key: str) -> list[str]:
    values: list[str] = []
    for lesson in lessons:
        values.extend(str(value) for value in lesson.get(key, []))
    return values


def main() -> None:
    data = load_json(SOURCE)
    lessons = data["lessons"]
    tr_cases = sorted(set(flatten(lessons, "tr_medllm_case_ids")))
    source_rows = sorted(set(flatten(lessons, "sourcecheckup_queue_ids")))
    review_states = sorted(set(flatten(lessons, "clinician_review_states")))
    release_gates = sorted(set(flatten(lessons, "release_gate_decisions")))
    assurance_gates = sorted(set(flatten(lessons, "assurance_gate_levels")))
    gate_counts = Counter(flatten(lessons, "release_gate_decisions"))

    lines: list[str] = [
        "# Clinician literacy release gate lesson map v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 16",
        "",
        "This map turns clinician AI literacy into release gate training. It links synthetic Turkish medical language model rows, SourceCheckup review queue rows, clinician review states, and assurance gate levels.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Lessons: {len(lessons)}",
        "",
        f"Total minutes: {data['total_minutes']}",
        "",
        f"TR MedLLM cases covered: {len(tr_cases)}",
        "",
        f"SourceCheckup queue rows covered: {len(source_rows)}",
        "",
        f"Clinician review states represented: {len(review_states)}",
        "",
        f"Release gate decisions represented: {len(release_gates)}",
        "",
        f"Assurance gate levels represented: {len(assurance_gates)}",
        "",
        "## Release gate coverage",
        "",
    ]
    for gate, count in sorted(gate_counts.items()):
        lines.extend([f"{gate}: {count}", ""])

    lines.extend(["## Lesson outlines", ""])
    for lesson in lessons:
        lines.extend(
            [
                f"### {lesson['lesson_id']}: {lesson['title']}",
                "",
                f"Minutes: {lesson['minutes']}",
                "",
                f"Learning goal: {lesson['learning_goal']}",
                "",
                f"TR MedLLM rows: {', '.join(lesson['tr_medllm_case_ids'])}",
                "",
                f"SourceCheckup rows: {', '.join(lesson['sourcecheckup_queue_ids'])}",
                "",
                f"Clinician review states: {', '.join(lesson['clinician_review_states'])}",
                "",
                f"Release gate decisions: {', '.join(lesson['release_gate_decisions'])}",
                "",
                f"Assurance gate levels: {', '.join(lesson['assurance_gate_levels'])}",
                "",
                f"Learner task: {lesson['learner_task']}",
                "",
                f"Facilitator check: {lesson['facilitator_check']}",
                "",
                f"Track A value: {lesson['track_a_value']}",
                "",
                f"Track B value: {lesson['track_b_value']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. Every lesson uses synthetic examples only.",
            "2. Patient data is not used.",
            "3. Local pass does not mean clinical truth, source truth, model safety, or deployment readiness.",
            "4. SourceCheckup rows are review queue rows, not proof that a medical claim is true.",
            "5. Assurance gate L5 remains blocked for this automation.",
            "6. External workshop, institutional use, endpoint run, or clinical deployment requires separate explicit clearance.",
            "",
            "## Public files",
            "",
            "1. JSON source: `docs/clinician_literacy_release_gate_lesson_map_v0_1.json`",
            "2. Generated map: `docs/CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md`",
            "3. Validator: `scripts/validate_clinician_literacy_release_gate_lesson_map_v0_1.py`",
            "4. Runnable target: `make clinician_literacy_map`",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"lessons={len(lessons)}")
    print(f"minutes={data['total_minutes']}")
    print(f"tr_cases={len(tr_cases)}")
    print(f"sourcecheckup_rows={len(source_rows)}")
    print(f"release_gates={len(release_gates)}")


if __name__ == "__main__":
    main()
