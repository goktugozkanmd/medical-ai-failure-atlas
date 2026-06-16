#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "source_review_worksheets_v0_1.json"
OUTPUT = ROOT / "docs" / "SOURCE_REVIEW_WORKSHEETS_V0_1.md"


def flatten(worksheets: list[dict[str, Any]], key: str) -> list[str]:
    values: list[str] = []
    for worksheet in worksheets:
        values.extend(str(value) for value in worksheet.get(key, []))
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
    worksheets: list[dict[str, Any]] = data["worksheets"]
    route_ids = sorted(set(flatten(worksheets, "linked_route_ids")))
    queue_rows = sorted(set(flatten(worksheets, "linked_sourcecheckup_queue_ids")))
    tr_cases = sorted(set(flatten(worksheets, "linked_tr_medllm_case_ids")))
    assurance_examples = sorted(set(flatten(worksheets, "linked_assurance_example_ids")))
    source_surfaces = sorted(set(flatten(worksheets, "source_surfaces")))
    risk_axes = sorted(set(flatten(worksheets, "risk_axes")))
    gate_levels = sorted(set(flatten(worksheets, "release_gate_levels")))
    review_lanes = sorted(set(flatten(worksheets, "review_lanes")))
    decisions = Counter(str(worksheet["routing_decision"]) for worksheet in worksheets)

    lines: list[str] = [
        "# Source review worksheets v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 16",
        "",
        "These worksheets turn the highest risk medication safety and policy wording routes into concrete public review steps. They are designed for synthetic SourceCheckup and TR MedLLM examples before any external reuse.",
        "",
        "They use synthetic examples only. They are not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Worksheets: {len(worksheets)}",
        "",
        f"SourceCheckup TR MedLLM routes covered: {len(route_ids)}",
        "",
        f"SourceCheckup queue rows covered: {len(queue_rows)}",
        "",
        f"TR MedLLM cases covered: {len(tr_cases)}",
        "",
        f"Assurance release gate examples covered: {len(assurance_examples)}",
        "",
        f"Source surfaces represented: {len(source_surfaces)}",
        "",
        f"Risk axes represented: {len(risk_axes)}",
        "",
        f"Release gate levels represented: {len(gate_levels)}",
        "",
        f"Review lanes represented: {len(review_lanes)}",
        "",
        f"Routing decisions represented: {len(decisions)}",
        "",
        "## Routing decision coverage",
        "",
    ]
    for decision, count in sorted(decisions.items()):
        lines.extend([f"{decision}: {count}", ""])

    lines.extend(["## Review lane coverage", ""])
    for lane in review_lanes:
        lines.extend([lane, ""])

    lines.extend(["## Worksheets", ""])
    for worksheet in worksheets:
        lines.extend(
            [
                f"### {worksheet['worksheet_id']}: {worksheet['title']}",
                "",
                f"Linked routes: {joined(worksheet['linked_route_ids'])}",
                "",
                f"SourceCheckup rows: {joined(worksheet['linked_sourcecheckup_queue_ids'])}",
                "",
                f"TR MedLLM rows: {joined(worksheet['linked_tr_medllm_case_ids'])}",
                "",
                f"Assurance examples: {joined(worksheet['linked_assurance_example_ids'])}",
                "",
                f"Source surfaces: {joined(worksheet['source_surfaces'])}",
                "",
                f"Risk axes: {joined(worksheet['risk_axes'])}",
                "",
                f"Release gate levels: {joined(worksheet['release_gate_levels'])}",
                "",
                f"Routing decision: {worksheet['routing_decision']}",
                "",
                f"Review lanes: {joined(worksheet['review_lanes'])}",
                "",
                "Blocked claim patterns:",
                "",
            ]
        )
        lines.extend(numbered(worksheet["blocked_claim_patterns"]))
        lines.extend(["Minimum evidence fields:", ""])
        lines.extend(numbered(worksheet["minimum_evidence_fields"]))
        lines.extend(["Review questions:", ""])
        lines.extend(numbered(worksheet["review_questions"]))
        lines.extend(
            [
                f"Allowed public output: {worksheet['allowed_public_output']}",
                "",
                f"Blocked public output: {worksheet['blocked_public_output']}",
                "",
                f"Pass condition: {worksheet['pass_condition']}",
                "",
                f"Fail condition: {worksheet['fail_condition']}",
                "",
                f"Track A value: {worksheet['track_a_value']}",
                "",
                f"Track B value: {worksheet['track_b_value']}",
                "",
                f"Next public action: {worksheet['next_public_action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. Every worksheet uses synthetic examples only.",
            "2. Patient data is not used.",
            "3. Passing a worksheet is not clinical truth, source truth, model safety, or deployment readiness.",
            "4. Medication advice remains blocked when source support or clinical variables are missing.",
            "5. Policy, sandbox, pilot, official route, and deployment language remains blocked without written evidence and explicit clearance.",
            "6. These worksheets do not rank models and do not claim benchmark compatibility.",
            "",
            "## Public files",
            "",
            "1. JSON source: `docs/source_review_worksheets_v0_1.json`",
            "2. Generated worksheets: `docs/SOURCE_REVIEW_WORKSHEETS_V0_1.md`",
            "3. Validator: `scripts/validate_source_review_worksheets_v0_1.py`",
            "4. Runnable target: `make source_review_worksheets`",
            "5. Upstream routing map: `docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md`",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"worksheets={len(worksheets)}")
    print(f"routes={len(route_ids)}")
    print(f"sourcecheckup_rows={len(queue_rows)}")
    print(f"tr_cases={len(tr_cases)}")
    print(f"assurance_examples={len(assurance_examples)}")
    print(f"review_lanes={len(review_lanes)}")


if __name__ == "__main__":
    main()
