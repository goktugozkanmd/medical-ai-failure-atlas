#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "reviewer_question_public_release_packet_v0_1.json"
CHANGELOG = ROOT / "docs" / "reviewer_question_public_changelog_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_public_release_index_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_PUBLIC_RELEASE_INDEX_V0_1.md"

INDEX_SURFACES = [
    {
        "surface_id": "RQRPI001",
        "surface_name": "Benchmark style reviewer questions",
        "public_file": "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
        "role": "defines public reviewer questions for source support and safety review",
    },
    {
        "surface_id": "RQRPI002",
        "surface_name": "Contributor issue template reviewer questions",
        "public_file": "docs/CONTRIBUTOR_ISSUE_TEMPLATE_REVIEWER_QUESTIONS_V0_1.md",
        "role": "adds reviewer question fields to public intake templates",
    },
    {
        "surface_id": "RQRPI003",
        "surface_name": "Reviewer question intake examples",
        "public_file": "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
        "role": "shows synthetic reviewer question intake examples",
    },
    {
        "surface_id": "RQRPI004",
        "surface_name": "Reviewer question intake triage board",
        "public_file": "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
        "role": "maps intake examples to maintainer action and owner roles",
    },
    {
        "surface_id": "RQRPI005",
        "surface_name": "Reviewer question public wording decision log",
        "public_file": "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "role": "records blocked wording and required public wording",
    },
    {
        "surface_id": "RQRPI006",
        "surface_name": "Reviewer question release gate checklist",
        "public_file": "docs/REVIEWER_QUESTION_RELEASE_GATE_CHECKLIST_V0_1.md",
        "role": "turns wording decisions into pass or block checks",
    },
    {
        "surface_id": "RQRPI007",
        "surface_name": "Reviewer question release gate outcome dashboard",
        "public_file": "docs/REVIEWER_QUESTION_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
        "role": "summarizes current pass and block outcomes",
    },
    {
        "surface_id": "RQRPI008",
        "surface_name": "Reviewer question public release packet",
        "public_file": "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_PACKET_V0_1.md",
        "role": "packages reviewer question public surfaces into one release packet",
    },
    {
        "surface_id": "RQRPI009",
        "surface_name": "Reviewer question public changelog",
        "public_file": "docs/REVIEWER_QUESTION_PUBLIC_CHANGELOG_V0_1.md",
        "role": "records the chronological maintainer sequence",
    },
]

ISSUE_HISTORY = [
    (45, "Roadmap: benchmark style reviewer questions", "reviewer questions", "benchmark style reviewer questions added"),
    (46, "Roadmap: reviewer question issue template fields", "reviewer questions", "issue template fields added"),
    (47, "Roadmap: reviewer question intake examples", "reviewer questions", "intake examples added"),
    (48, "Roadmap: reviewer question intake triage board", "reviewer questions", "intake triage board added"),
    (49, "Roadmap: reviewer question wording decision log", "reviewer questions", "wording decision log added"),
    (50, "Roadmap: reviewer question release gate checklist", "reviewer questions", "release gate checklist added"),
    (51, "Roadmap: reviewer question gate outcome dashboard", "reviewer questions", "gate outcome dashboard added"),
    (52, "Roadmap: reviewer question public release packet", "reviewer questions", "public release packet added"),
    (53, "Roadmap: reviewer question public changelog", "reviewer questions", "public changelog added"),
    (54, "Roadmap: reviewer question public release index", "reviewer questions", "public release index added"),
    (55, "Roadmap: reviewer question public contributor digest", "reviewer questions", "public contributor digest added"),
]


def main() -> int:
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    changelog = json.loads(CHANGELOG.read_text(encoding="utf-8"))
    surfaces: list[dict[str, Any]] = [
        {
            **surface,
            "index_status": "included_in_public_release_index",
            "next_action": "keep linked surface current during public preview",
        }
        for surface in INDEX_SURFACES
    ]
    issues: list[dict[str, Any]] = [
        {
            "issue_number": number,
            "issue_title": title,
            "issue_state": "closed",
            "public_label": label,
            "public_value": value,
        }
        for number, title, label, value in ISSUE_HISTORY
    ]

    data: dict[str, Any] = {
        "version": "reviewer_question_public_release_index_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "sources": [
            "docs/reviewer_question_public_release_packet_v0_1.json",
            "docs/reviewer_question_public_changelog_v0_1.json",
        ],
        "index_surface_count": len(surfaces),
        "issue_history_count": len(issues),
        "release_packet_rows_represented": packet["packet_surface_count"],
        "changelog_rows_represented": changelog["change_row_count"],
        "index_decision": "ready_for_public_preview",
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
        "surfaces": surfaces,
        "issue_history": issues,
    }
    JSON_OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Reviewer question public release index v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This index is the durable public entry point for the reviewer question route, release packet, changelog, validation commands, and public issue history.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Index surface rows: {len(surfaces)}",
        "",
        f"Issue history rows: {len(issues)}",
        "",
        f"Release packet rows represented: {data['release_packet_rows_represented']}",
        "",
        f"Changelog rows represented: {data['changelog_rows_represented']}",
        "",
        "Index decision: `ready_for_public_preview`",
        "",
        "## Public surfaces",
        "",
    ]

    for surface in surfaces:
        lines.extend(
            [
                f"### {surface['surface_id']}",
                "",
                f"Surface name: {surface['surface_name']}",
                "",
                f"Public file: `{surface['public_file']}`",
                "",
                f"Role: {surface['role']}",
                "",
                f"Index status: `{surface['index_status']}`",
                "",
                f"Next action: {surface['next_action']}",
                "",
            ]
        )

    lines.extend(["## Public issue history", ""])
    for issue in issues:
        lines.extend(
            [
                f"### Issue {issue['issue_number']}",
                "",
                f"Title: {issue['issue_title']}",
                "",
                f"State: {issue['issue_state']}",
                "",
                f"Public label: {issue['public_label']}",
                "",
                f"Public value: {issue['public_value']}",
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
            "make reviewer_question_release_index",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer audit trail packet without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"index_surface_rows={len(surfaces)}")
    print(f"issue_history_rows={len(issues)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
