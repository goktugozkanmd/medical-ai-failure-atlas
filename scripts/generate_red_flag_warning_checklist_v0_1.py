#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "red_flag_warning_checklist_v0_1.json"
OUTPUT = ROOT / "docs" / "RED_FLAG_WARNING_CHECKLIST_V0_1.md"


def flatten(checklists: list[dict[str, Any]], key: str) -> list[str]:
    values: list[str] = []
    for checklist in checklists:
        values.extend(str(value) for value in checklist.get(key, []))
    return values


def joined(values: list[str]) -> str:
    return ", ".join(values)


def numbered(values: list[str]) -> list[str]:
    lines: list[str] = []
    for index, value in enumerate(values, start=1):
        lines.extend([f"{index}. {value}", ""])
    return lines


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    checklists: list[dict[str, Any]] = data["checklists"]
    route_ids = sorted(set(flatten(checklists, "linked_route_ids")))
    queue_rows = sorted(set(flatten(checklists, "linked_sourcecheckup_queue_ids")))
    tr_cases = sorted(set(flatten(checklists, "linked_tr_medllm_case_ids")))
    assurance_examples = sorted(set(flatten(checklists, "linked_assurance_example_ids")))
    taxonomy_patterns = sorted(set(flatten(checklists, "linked_taxonomy_pattern_ids")))
    risk_axes = sorted(set(flatten(checklists, "risk_axes")))
    gate_levels = sorted(set(flatten(checklists, "release_gate_levels")))
    review_lanes = sorted(set(flatten(checklists, "review_lanes")))
    lane_counts = Counter(flatten(checklists, "review_lanes"))

    lines: list[str] = [
        "# Red flag source locator and warning sign checklist v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 16",
        "",
        "This checklist turns the red flag escalation route into concrete public review steps for partial negative evidence, symptom fluctuation, and source locator claims.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Checklists: {len(checklists)}",
        "",
        f"SourceCheckup TR MedLLM routes covered: {len(route_ids)}",
        "",
        f"SourceCheckup queue rows covered: {len(queue_rows)}",
        "",
        f"TR MedLLM cases covered: {len(tr_cases)}",
        "",
        f"Assurance release gate examples covered: {len(assurance_examples)}",
        "",
        f"Failure Atlas taxonomy patterns covered: {len(taxonomy_patterns)}",
        "",
        f"Risk axes represented: {len(risk_axes)}",
        "",
        f"Release gate levels represented: {len(gate_levels)}",
        "",
        f"Review lanes represented: {len(review_lanes)}",
        "",
        "## Review lane coverage",
        "",
    ]
    for lane, count in sorted(lane_counts.items()):
        lines.extend([f"{lane}: {count}", ""])

    lines.extend(["## Checklist map", ""])
    for checklist in checklists:
        lines.extend(
            [
                f"### {checklist['checklist_id']}: {checklist['title']}",
                "",
                f"Linked routes: {joined(checklist['linked_route_ids'])}",
                "",
                f"SourceCheckup rows: {joined(checklist['linked_sourcecheckup_queue_ids'])}",
                "",
                f"TR MedLLM rows: {joined(checklist['linked_tr_medllm_case_ids'])}",
                "",
                f"Assurance examples: {joined(checklist['linked_assurance_example_ids'])}",
                "",
                f"Taxonomy patterns: {joined(checklist['linked_taxonomy_pattern_ids'])}",
                "",
                f"Risk axes: {joined(checklist['risk_axes'])}",
                "",
                f"Release gate levels: {joined(checklist['release_gate_levels'])}",
                "",
                f"Review lanes: {joined(checklist['review_lanes'])}",
                "",
                "Blocked patterns:",
                "",
            ]
        )
        lines.extend(numbered(checklist["blocked_patterns"]))
        lines.extend(["Minimum review fields:", ""])
        lines.extend(numbered(checklist["minimum_review_fields"]))
        lines.extend(["Review questions:", ""])
        lines.extend(numbered(checklist["review_questions"]))
        lines.extend(
            [
                f"Safe wording expectation: {checklist['safe_wording_expectation']}",
                "",
                f"Allowed public output: {checklist['allowed_public_output']}",
                "",
                f"Blocked public output: {checklist['blocked_public_output']}",
                "",
                f"Track A value: {checklist['track_a_value']}",
                "",
                f"Track B value: {checklist['track_b_value']}",
                "",
                f"Next public action: {checklist['next_public_action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. Every checklist uses synthetic examples only.",
            "2. Patient data is not used.",
            "3. Red flag wording review is not clinical triage.",
            "4. A source locator is not proof of safety.",
            "5. Passing this checklist is not clinical validation, model safety, source truth, or deployment readiness.",
            "6. Public wording must keep unresolved danger variables visible before comfort language.",
            "7. Public wording must route unresolved danger or source support to clinician review.",
            "",
            "## Public files",
            "",
            "1. JSON source: `docs/red_flag_warning_checklist_v0_1.json`",
            "2. Generated checklist: `docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md`",
            "3. Validator: `scripts/validate_red_flag_warning_checklist_v0_1.py`",
            "4. Runnable target: `make red_flag_warning_checklist`",
            "5. Upstream routing map: `docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md`",
            "6. Upstream source review worksheets: `docs/SOURCE_REVIEW_WORKSHEETS_V0_1.md`",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"checklists={len(checklists)}")
    print(f"routes={len(route_ids)}")
    print(f"sourcecheckup_rows={len(queue_rows)}")
    print(f"tr_cases={len(tr_cases)}")
    print(f"taxonomy_patterns={len(taxonomy_patterns)}")
    print(f"review_lanes={len(review_lanes)}")


if __name__ == "__main__":
    main()
