#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SURFACE_EXAMPLES = ROOT / "sourcecheckup" / "examples" / "source_surface_examples_v0_2.jsonl"
CONTRIBUTION_EXAMPLES = ROOT / "sourcecheckup" / "examples" / "sourcecheckup_contribution_examples_v0_2.jsonl"
REVIEW_QUEUE = ROOT / "sourcecheckup" / "review_queue" / "source_claim_review_queue_v0_1.jsonl"
SOURCE_REPORT = ROOT / "sourcecheckup" / "build" / "source_surface_examples_v0_2_report.json"
OUTPUT = ROOT / "sourcecheckup" / "build" / "source_claim_example_expansion_v0_2.md"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def main() -> None:
    surface_rows = load_jsonl(SURFACE_EXAMPLES)
    contribution_rows = load_jsonl(CONTRIBUTION_EXAMPLES)
    queue_rows = load_jsonl(REVIEW_QUEUE)
    report = json.loads(SOURCE_REPORT.read_text(encoding="utf-8")) if SOURCE_REPORT.exists() else {}

    surface_counts = Counter(str(row["source_surface"]) for row in contribution_rows)
    queue_surface_counts = Counter(str(row["source_surface"]) for row in queue_rows)
    gate_counts = Counter(str(row["release_gate"]) for row in queue_rows)
    connected_projects = Counter(str(row["connected_project"]) for row in queue_rows)
    report_gates = report.get("summary", {}).get("gate_counts", {})
    report_flags = report.get("summary", {}).get("flag_counts", {})

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# SourceCheckup source claim example expansion v0.2",
        "",
        "Status: generated public preview.",
        "",
        "This dashboard summarizes the expanded synthetic SourceCheckup example set, contributor examples, and source claim review queue.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"SourceCheckup v0.2 answer examples: {len(surface_rows)}",
        "",
        f"SourceCheckup contributor examples: {len(contribution_rows)}",
        "",
        f"Source claim review queue rows: {len(queue_rows)}",
        "",
        f"Contribution source surfaces represented: {len(surface_counts)}",
        "",
        f"Review queue source surfaces represented: {len(queue_surface_counts)}",
        "",
        f"Review queue release gates represented: {len(gate_counts)}",
        "",
        f"SourceCheckup report verification queue items: {report.get('summary', {}).get('verification_queue_items', 0)}",
        "",
        "## SourceCheckup report gate counts",
        "",
    ]
    for gate, count in sorted(report_gates.items()):
        lines.extend([f"{gate}: {count}", ""])

    lines.extend(["## SourceCheckup report flag counts", ""])
    for flag, count in sorted(report_flags.items()):
        lines.extend([f"{flag}: {count}", ""])

    lines.extend(["## Contribution source surfaces", ""])
    for surface, count in sorted(surface_counts.items()):
        lines.extend([f"{surface}: {count}", ""])

    lines.extend(["## Review queue source surfaces", ""])
    for surface, count in sorted(queue_surface_counts.items()):
        lines.extend([f"{surface}: {count}", ""])

    lines.extend(["## Review queue release gates", ""])
    for gate, count in sorted(gate_counts.items()):
        lines.extend([f"{gate}: {count}", ""])

    lines.extend(["## Connected project coverage", ""])
    for project, count in sorted(connected_projects.items()):
        lines.extend([f"{project}: {count}", ""])

    lines.extend(["## New expansion rows", ""])
    for row in surface_rows:
        answer_id = str(row["answer_id"])
        try:
            suffix = int(answer_id.rsplit("_", 1)[1])
        except (IndexError, ValueError):
            suffix = 0
        if suffix < 6:
            continue
        lines.extend(
            [
                f"### {answer_id}",
                "",
                f"Prompt: {row['prompt']}",
                "",
                f"Declared source count: {len(row.get('declared_sources') or [])}",
                "",
                f"Declared claim count: {len(row.get('declared_claims') or [])}",
                "",
            ]
        )

    lines.extend(["## Track A value", ""])
    lines.extend(
        [
            "1. Adds Turkish medical LLM source discipline examples for medication safety, benchmark wording, national route wording, and data provenance.",
            "2. Keeps official route, sandbox, patient data, and clinical deployment claims blocked unless exact written evidence exists.",
            "3. Gives clinician literacy and assurance lab modules concrete source claim exercises.",
            "4. Routes the source claim queue into the SourceCheckup TR MedLLM assurance routing map.",
            "",
            "## Track B value",
            "",
            "1. Expands SourceCheckup Medical from a parser preview into a public source review queue surface.",
            "2. Links source support, benchmark compatibility wording, Failure Atlas rows, and health data quality boundaries.",
            "3. Keeps source review separate from source truth certification, model ranking, and clinical validation.",
            "4. Adds a bridge into `docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md`.",
            "",
            "## Boundary checks",
            "",
            "1. Every example is synthetic.",
            "2. Patient data is not used.",
            "3. External action readiness is false for review queue rows.",
            "4. Outward use is not allowed until maintainer review and exact source support checks are complete.",
            "5. Passing local SourceCheckup only means no local source claim risk was triggered.",
            "6. This dashboard does not certify any source, guideline, policy, benchmark, or medical claim.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"surface_examples={len(surface_rows)}")
    print(f"contribution_examples={len(contribution_rows)}")
    print(f"queue_rows={len(queue_rows)}")
    print(f"queue_surfaces={len(queue_surface_counts)}")
    print(f"queue_gates={len(gate_counts)}")


if __name__ == "__main__":
    main()
