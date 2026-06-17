#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTCOME = ROOT / "docs" / "reviewer_question_release_gate_outcome_dashboard_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_public_release_packet_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_PUBLIC_RELEASE_PACKET_V0_1.md"


PACKET_SURFACES = [
    {
        "surface_id": "RQRLP001",
        "surface_name": "Benchmark style reviewer questions",
        "public_file": "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
        "role": "defines public reviewer questions for source support and safety review",
    },
    {
        "surface_id": "RQRLP002",
        "surface_name": "Contributor issue template reviewer questions",
        "public_file": "docs/CONTRIBUTOR_ISSUE_TEMPLATE_REVIEWER_QUESTIONS_V0_1.md",
        "role": "adds reviewer question fields to public intake templates",
    },
    {
        "surface_id": "RQRLP003",
        "surface_name": "Reviewer question intake examples",
        "public_file": "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
        "role": "shows synthetic reviewer question intake examples",
    },
    {
        "surface_id": "RQRLP004",
        "surface_name": "Reviewer question intake triage board",
        "public_file": "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
        "role": "maps intake examples to maintainer action and owner roles",
    },
    {
        "surface_id": "RQRLP005",
        "surface_name": "Reviewer question public wording decision log",
        "public_file": "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "role": "records blocked wording and required public wording",
    },
    {
        "surface_id": "RQRLP006",
        "surface_name": "Reviewer question release gate checklist",
        "public_file": "docs/REVIEWER_QUESTION_RELEASE_GATE_CHECKLIST_V0_1.md",
        "role": "turns wording decisions into pass or block checks",
    },
    {
        "surface_id": "RQRLP007",
        "surface_name": "Reviewer question release gate outcome dashboard",
        "public_file": "docs/REVIEWER_QUESTION_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
        "role": "summarizes current pass and block outcomes",
    },
]


def main() -> int:
    outcome = json.loads(OUTCOME.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for item in PACKET_SURFACES:
        rows.append(
            {
                **item,
                "packet_status": "included_in_public_preview",
                "next_action": "keep linked public surface current",
            }
        )

    data: dict[str, Any] = {
        "artifact": "reviewer_question_public_release_packet_v0_1",
        "status": "generated public preview",
        "date": "2026 06 17",
        "source_artifact": "reviewer_question_release_gate_outcome_dashboard_v0_1",
        "packet_surface_count": len(rows),
        "outcome_row_count": outcome["outcome_row_count"],
        "pass_state_count": outcome["pass_state_count"],
        "block_state_count": outcome["block_state_count"],
        "packet_decision": "ready_for_public_preview",
        "contains_patient_data": False,
        "synthetic_examples_only": True,
        "not_for_clinical_use": True,
        "no_raw_model_output_release": True,
        "no_endpoint_result": True,
        "no_score_report": True,
        "no_model_ranking": True,
        "no_benchmark_compatibility_claim": True,
        "no_benchmark_equivalence_claim": True,
        "no_clinical_deployment_claim": True,
        "no_clinical_validation_claim": True,
        "no_official_endorsement_claim": True,
        "rows": rows,
    }
    JSON_OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Reviewer question public release packet v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This packet gives one public release surface for benchmark style reviewer questions, contributor issue fields, intake examples, maintainer triage, wording decisions, release gate checks, and outcome rows.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Packet surface rows: {len(rows)}",
        "",
        f"Outcome rows represented: {data['outcome_row_count']}",
        "",
        f"Pass state rows represented: {data['pass_state_count']}",
        "",
        f"Block state rows represented: {data['block_state_count']}",
        "",
        "Packet decision: `ready_for_public_preview`",
        "",
        "## Packet rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['surface_id']}",
                "",
                f"Surface name: {row['surface_name']}",
                "",
                f"Public file: `{row['public_file']}`",
                "",
                f"Role: {row['role']}",
                "",
                f"Packet status: `{row['packet_status']}`",
                "",
                f"Next action: {row['next_action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make reviewer_question_release_packet",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer release candidate summary without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {MD_OUTPUT.relative_to(ROOT)}")
    print(f"wrote {JSON_OUTPUT.relative_to(ROOT)}")
    print(f"packet_surface_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
