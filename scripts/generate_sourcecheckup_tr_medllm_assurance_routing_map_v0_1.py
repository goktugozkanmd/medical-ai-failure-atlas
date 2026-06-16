#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "sourcecheckup_tr_medllm_assurance_routing_map_v0_1.json"
OUTPUT = ROOT / "docs" / "SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md"


def flatten(routes: list[dict[str, Any]], key: str) -> list[str]:
    values: list[str] = []
    for route in routes:
        values.extend(str(value) for value in route.get(key, []))
    return values


def joined(values: list[str]) -> str:
    return ", ".join(values)


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    routes: list[dict[str, Any]] = data["routes"]
    queue_rows = sorted(set(flatten(routes, "sourcecheckup_queue_ids")))
    tr_cases = sorted(set(flatten(routes, "tr_medllm_case_ids")))
    assurance_examples = sorted(set(flatten(routes, "assurance_example_ids")))
    source_surfaces = sorted(set(flatten(routes, "source_surfaces")))
    risk_axes = sorted(set(flatten(routes, "risk_axes")))
    gate_levels = sorted(set(flatten(routes, "release_gate_levels")))
    decisions = Counter(str(route["routing_decision"]) for route in routes)

    lines: list[str] = [
        "# SourceCheckup TR MedLLM assurance routing map v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 16",
        "",
        "This map connects SourceCheckup queue rows, Turkish synthetic risk rows, and assurance release gate examples. It shows which synthetic source claim problems should flow to source review, clinician review, assurance gates, or blocked public wording.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Routes: {len(routes)}",
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
        f"Routing decisions represented: {len(decisions)}",
        "",
        "## Routing decision coverage",
        "",
    ]
    for decision, count in sorted(decisions.items()):
        lines.extend([f"{decision}: {count}", ""])

    lines.extend(["## Source surface coverage", ""])
    for surface in source_surfaces:
        lines.extend([surface, ""])

    lines.extend(["## Risk axis coverage", ""])
    for axis in risk_axes:
        lines.extend([axis, ""])

    lines.extend(["## Route map", ""])
    for route in routes:
        lines.extend(
            [
                f"### {route['route_id']}: {route['title']}",
                "",
                f"SourceCheckup rows: {joined(route['sourcecheckup_queue_ids'])}",
                "",
                f"TR MedLLM rows: {joined(route['tr_medllm_case_ids'])}",
                "",
                f"Assurance examples: {joined(route['assurance_example_ids'])}",
                "",
                f"Source surfaces: {joined(route['source_surfaces'])}",
                "",
                f"Risk axes: {joined(route['risk_axes'])}",
                "",
                f"Release gate levels: {joined(route['release_gate_levels'])}",
                "",
                f"Routing decision: {route['routing_decision']}",
                "",
                f"Claim hazard: {route['claim_hazard']}",
                "",
                f"Public use boundary: {route['public_use_boundary']}",
                "",
                f"Track A value: {route['track_a_value']}",
                "",
                f"Track B value: {route['track_b_value']}",
                "",
                f"Next public action: {route['next_public_action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. Every route uses synthetic examples only.",
            "2. Patient data is not used.",
            "3. Local routing is not clinical truth, source truth, model safety, or deployment readiness.",
            "4. Policy, sandbox, pilot, official route, and deployment language remains blocked without written evidence and explicit clearance.",
            "5. SourceCheckup routing is a review path, not proof that a source or medical claim is true.",
            "6. This map does not rank models and does not claim benchmark compatibility.",
            "",
            "## Public files",
            "",
            "1. JSON source: `docs/sourcecheckup_tr_medllm_assurance_routing_map_v0_1.json`",
            "2. Generated map: `docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md`",
            "3. Validator: `scripts/validate_sourcecheckup_tr_medllm_assurance_routing_map_v0_1.py`",
            "4. Runnable target: `make sourcecheckup_tr_medllm_routing`",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"routes={len(routes)}")
    print(f"sourcecheckup_rows={len(queue_rows)}")
    print(f"tr_cases={len(tr_cases)}")
    print(f"assurance_examples={len(assurance_examples)}")
    print(f"source_surfaces={len(source_surfaces)}")
    print(f"risk_axes={len(risk_axes)}")
    print(f"gate_levels={len(gate_levels)}")


if __name__ == "__main__":
    main()
