#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "assurance_release_gate_example_map_v0_1.json"
OUTPUT = ROOT / "docs" / "ASSURANCE_RELEASE_GATE_EXAMPLE_MAP_V0_1.md"


def flatten(examples: list[dict[str, Any]], key: str) -> list[str]:
    values: list[str] = []
    for example in examples:
        values.extend(str(value) for value in example.get(key, []))
    return values


def bullet_list(values: list[str]) -> str:
    return ", ".join(values)


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    examples: list[dict[str, Any]] = data["examples"]
    tr_cases = sorted(set(flatten(examples, "tr_medllm_case_ids")))
    source_rows = sorted(set(flatten(examples, "sourcecheckup_queue_ids")))
    sections = sorted(set(flatten(examples, "assurance_card_sections")))
    gate_levels = sorted(set(flatten(examples, "release_gate_levels")))
    decisions = Counter(str(example["release_gate_decision"]) for example in examples)

    lines: list[str] = [
        "# Assurance release gate example map v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 16",
        "",
        "This map turns the assurance card template into concrete release gate examples. It connects clinician literacy lessons, Turkish synthetic risk rows, SourceCheckup queue rows, assurance card sections, and public action boundaries.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Examples: {len(examples)}",
        "",
        f"TR MedLLM cases covered: {len(tr_cases)}",
        "",
        f"SourceCheckup queue rows covered: {len(source_rows)}",
        "",
        f"Assurance card sections covered: {len(sections)}",
        "",
        f"Release gate levels represented: {len(gate_levels)}",
        "",
        f"Release gate decisions represented: {len(decisions)}",
        "",
        "## Release gate decision coverage",
        "",
    ]
    for decision, count in sorted(decisions.items()):
        lines.extend([f"{decision}: {count}", ""])

    lines.extend(["## Assurance card section coverage", ""])
    for section in sections:
        lines.extend([section, ""])

    lines.extend(["## Example map", ""])
    for example in examples:
        lines.extend(
            [
                f"### {example['example_id']}: {example['title']}",
                "",
                f"Linked lessons: {bullet_list(example['linked_lesson_ids'])}",
                "",
                f"TR MedLLM rows: {bullet_list(example['tr_medllm_case_ids'])}",
                "",
                f"SourceCheckup rows: {bullet_list(example['sourcecheckup_queue_ids'])}",
                "",
                f"Assurance card sections: {bullet_list(example['assurance_card_sections'])}",
                "",
                f"Release gate levels: {bullet_list(example['release_gate_levels'])}",
                "",
                f"Release gate decision: {example['release_gate_decision']}",
                "",
                f"Minimum required review: {example['minimum_required_review']}",
                "",
                f"Main blocker: {example['main_blocker']}",
                "",
                f"Allowed public phrase: {example['allowed_public_phrase']}",
                "",
                f"Blocked public phrase: {example['blocked_public_phrase']}",
                "",
                f"Track A value: {example['track_a_value']}",
                "",
                f"Track B value: {example['track_b_value']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. Every example uses synthetic examples only.",
            "2. Patient data is not used.",
            "3. Local validation does not mean clinical truth, source truth, model safety, or deployment readiness.",
            "4. L4 external pilot language requires separate explicit clearance.",
            "5. Assurance gate L5 remains blocked in this automation.",
            "6. Official role, sandbox access, clinical deployment, clinical validation, and model safety claims remain blocked.",
            "",
            "## Public files",
            "",
            "1. JSON source: `docs/assurance_release_gate_example_map_v0_1.json`",
            "2. Generated map: `docs/ASSURANCE_RELEASE_GATE_EXAMPLE_MAP_V0_1.md`",
        "3. Validator: `scripts/validate_assurance_release_gate_example_map_v0_1.py`",
        "4. Runnable target: `make assurance_release_gate_map`",
        "5. SourceCheckup TR MedLLM assurance routing map: `docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md`",
        "",
    ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"examples={len(examples)}")
    print(f"tr_cases={len(tr_cases)}")
    print(f"sourcecheckup_rows={len(source_rows)}")
    print(f"assurance_sections={len(sections)}")
    print(f"gate_levels={len(gate_levels)}")


if __name__ == "__main__":
    main()
