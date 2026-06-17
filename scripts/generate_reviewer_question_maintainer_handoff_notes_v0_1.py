#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DIGEST = ROOT / "docs" / "reviewer_question_public_contributor_digest_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_handoff_notes_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_HANDOFF_NOTES_V0_1.md"

HANDOFF_ROWS = [
    {
        "handoff_id": "RQMH001",
        "handoff_name": "Confirm synthetic scope",
        "public_file": "docs/REVIEWER_QUESTION_PUBLIC_CONTRIBUTOR_DIGEST_V0_1.md",
        "maintainer_action": "reject or rewrite any proposal that could describe a real patient",
    },
    {
        "handoff_id": "RQMH002",
        "handoff_name": "Check reviewer question fit",
        "public_file": "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
        "maintainer_action": "map the proposal to a public reviewer question lane",
    },
    {
        "handoff_id": "RQMH003",
        "handoff_name": "Check intake and triage route",
        "public_file": "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
        "maintainer_action": "confirm owner role, review state, and public wording decision",
    },
    {
        "handoff_id": "RQMH004",
        "handoff_name": "Check blocked wording",
        "public_file": "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "maintainer_action": "block score, compatibility, endpoint, patient data, clinical validation, and endorsement wording",
    },
    {
        "handoff_id": "RQMH005",
        "handoff_name": "Run maintainer checks",
        "public_file": "Makefile",
        "maintainer_action": "run make reviewer_question_maintainer_handoff before public closeout",
    },
]


def main() -> int:
    digest = json.loads(DIGEST.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = [
        {
            **row,
            "handoff_status": "included_in_public_maintainer_handoff",
            "boundary": "synthetic only and not for clinical use",
            "closeout_state": "maintainer_review_required",
        }
        for row in HANDOFF_ROWS
    ]

    data: dict[str, Any] = {
        "version": "reviewer_question_maintainer_handoff_notes_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_public_contributor_digest_v0_1.json",
        "handoff_row_count": len(rows),
        "contributor_digest_rows_represented": digest["digest_step_count"],
        "release_index_surface_rows_represented": digest["release_index_surface_rows_represented"],
        "issue_history_rows_represented": digest["issue_history_rows_represented"],
        "handoff_decision": "ready_for_public_preview",
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
    JSON_OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Reviewer question maintainer handoff notes v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "These handoff notes give maintainers a short checklist for reviewing synthetic reviewer question contributor proposals before public closeout.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Handoff rows: {len(rows)}",
        "",
        f"Contributor digest rows represented: {data['contributor_digest_rows_represented']}",
        "",
        f"Release index surface rows represented: {data['release_index_surface_rows_represented']}",
        "",
        f"Issue history rows represented: {data['issue_history_rows_represented']}",
        "",
        "Handoff decision: `ready_for_public_preview`",
        "",
        "## Maintainer handoff rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['handoff_id']}",
                "",
                f"Handoff name: {row['handoff_name']}",
                "",
                f"Public file: `{row['public_file']}`",
                "",
                f"Maintainer action: {row['maintainer_action']}",
                "",
                f"Handoff status: `{row['handoff_status']}`",
                "",
                f"Closeout state: `{row['closeout_state']}`",
                "",
                f"Boundary: {row['boundary']}",
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
            "make reviewer_question_maintainer_handoff",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer release readiness digest without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"handoff_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
