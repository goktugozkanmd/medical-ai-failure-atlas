#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "reviewer_question_public_release_packet_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_public_changelog_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_PUBLIC_CHANGELOG_V0_1.md"

CHANGE_ROWS = [
    {
        "change_id": "RQRC001",
        "date": "2026 06 17",
        "surface_name": "Benchmark style reviewer questions",
        "public_file": "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
        "public_value": "opened public reviewer questions for source support and safety review",
    },
    {
        "change_id": "RQRC002",
        "date": "2026 06 17",
        "surface_name": "Contributor issue template reviewer questions",
        "public_file": "docs/CONTRIBUTOR_ISSUE_TEMPLATE_REVIEWER_QUESTIONS_V0_1.md",
        "public_value": "added reviewer question fields to public issue templates",
    },
    {
        "change_id": "RQRC003",
        "date": "2026 06 17",
        "surface_name": "Reviewer question intake examples",
        "public_file": "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
        "public_value": "added synthetic reviewer question intake examples",
    },
    {
        "change_id": "RQRC004",
        "date": "2026 06 17",
        "surface_name": "Reviewer question intake triage board",
        "public_file": "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
        "public_value": "mapped intake examples to maintainer action and owner roles",
    },
    {
        "change_id": "RQRC005",
        "date": "2026 06 17",
        "surface_name": "Reviewer question public wording decision log",
        "public_file": "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "public_value": "recorded blocked wording and required public wording",
    },
    {
        "change_id": "RQRC006",
        "date": "2026 06 17",
        "surface_name": "Reviewer question release gate checklist",
        "public_file": "docs/REVIEWER_QUESTION_RELEASE_GATE_CHECKLIST_V0_1.md",
        "public_value": "converted wording decisions into release checks",
    },
    {
        "change_id": "RQRC007",
        "date": "2026 06 17",
        "surface_name": "Reviewer question release gate outcome dashboard",
        "public_file": "docs/REVIEWER_QUESTION_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
        "public_value": "summarized current pass and block outcomes",
    },
    {
        "change_id": "RQRC008",
        "date": "2026 06 17",
        "surface_name": "Reviewer question public release packet",
        "public_file": "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_PACKET_V0_1.md",
        "public_value": "packaged the reviewer question route into one public release surface",
    },
]


def main() -> int:
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for row in CHANGE_ROWS:
        rows.append(
            {
                **row,
                "change_status": "public_preview_added",
                "boundary": "synthetic only and not for clinical use",
                "next_action": "keep linked surface current during public preview",
            }
        )

    data: dict[str, Any] = {
        "artifact": "reviewer_question_public_changelog_v0_1",
        "status": "generated public preview",
        "date": "2026 06 17",
        "source_artifact": "reviewer_question_public_release_packet_v0_1",
        "change_row_count": len(rows),
        "release_packet_rows_represented": packet["packet_surface_count"],
        "latest_change_id": rows[-1]["change_id"],
        "changelog_decision": "ready_for_public_preview",
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
        "# Reviewer question public changelog v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This changelog gives a chronological public maintainer record for benchmark style reviewer questions, contributor issue fields, intake examples, triage, wording decisions, release gate checks, outcome rows, and the public release packet.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Change rows: {len(rows)}",
        "",
        f"Release packet rows represented: {data['release_packet_rows_represented']}",
        "",
        f"Latest change id: `{data['latest_change_id']}`",
        "",
        "Changelog decision: `ready_for_public_preview`",
        "",
        "## Change rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['change_id']}",
                "",
                f"Date: {row['date']}",
                "",
                f"Surface name: {row['surface_name']}",
                "",
                f"Public file: `{row['public_file']}`",
                "",
                f"Public value: {row['public_value']}",
                "",
                f"Change status: `{row['change_status']}`",
                "",
                f"Boundary: {row['boundary']}",
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
            "make reviewer_question_changelog",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer audit trail packet without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {MD_OUTPUT.relative_to(ROOT)}")
    print(f"wrote {JSON_OUTPUT.relative_to(ROOT)}")
    print(f"change_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
