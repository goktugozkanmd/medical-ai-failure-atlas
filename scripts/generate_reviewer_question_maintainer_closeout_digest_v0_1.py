#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "reviewer_question_maintainer_handoff_notes_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_closeout_digest_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md"

CLOSEOUT_ROWS = [
    {
        "closeout_id": "RQMC001",
        "closeout_name": "Synthetic scope closeout",
        "evidence_file": "docs/REVIEWER_QUESTION_PUBLIC_CONTRIBUTOR_DIGEST_V0_1.md",
        "closeout_action": "record that proposed reviewer question contributions stay synthetic only",
    },
    {
        "closeout_id": "RQMC002",
        "closeout_name": "Reviewer question fit closeout",
        "evidence_file": "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
        "closeout_action": "record that the contribution maps to a public reviewer question lane",
    },
    {
        "closeout_id": "RQMC003",
        "closeout_name": "Intake route closeout",
        "evidence_file": "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
        "closeout_action": "record owner role, review state, and public wording decision",
    },
    {
        "closeout_id": "RQMC004",
        "closeout_name": "Blocked wording closeout",
        "evidence_file": "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "closeout_action": "record that blocked public wording remains excluded",
    },
    {
        "closeout_id": "RQMC005",
        "closeout_name": "Validation closeout",
        "evidence_file": "Makefile",
        "closeout_action": "run make reviewer_question_maintainer_closeout_digest before public issue closure",
    },
]


def main() -> int:
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = [
        {
            **row,
            "closeout_status": "included_in_public_maintainer_closeout_digest",
            "closeout_state": "current_preview_closed",
            "boundary": "synthetic only and not for clinical use",
        }
        for row in CLOSEOUT_ROWS
    ]

    data: dict[str, Any] = {
        "version": "reviewer_question_maintainer_closeout_digest_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_maintainer_handoff_notes_v0_1.json",
        "closeout_row_count": len(rows),
        "handoff_rows_represented": handoff["handoff_row_count"],
        "contributor_digest_rows_represented": handoff["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": handoff["release_index_surface_rows_represented"],
        "issue_history_rows_represented": handoff["issue_history_rows_represented"],
        "previous_public_issue_number": 56,
        "closeout_decision": "ready_for_public_preview",
        "maintainer_review_scope": "current public preview route only",
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
        "# Reviewer question maintainer closeout digest v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This digest gives maintainers a compact closeout trail for synthetic reviewer question public preview updates after handoff review.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Closeout rows: {len(rows)}",
        "",
        f"Handoff rows represented: {data['handoff_rows_represented']}",
        "",
        f"Contributor digest rows represented: {data['contributor_digest_rows_represented']}",
        "",
        f"Release index surface rows represented: {data['release_index_surface_rows_represented']}",
        "",
        f"Issue history rows represented: {data['issue_history_rows_represented']}",
        "",
        f"Previous public issue represented: {data['previous_public_issue_number']}",
        "",
        "Maintainer review scope: current public preview route only",
        "",
        "Closeout decision: `ready_for_public_preview`",
        "",
        "## Maintainer closeout rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['closeout_id']}",
                "",
                f"Closeout name: {row['closeout_name']}",
                "",
                f"Evidence file: `{row['evidence_file']}`",
                "",
                f"Closeout action: {row['closeout_action']}",
                "",
                f"Closeout status: `{row['closeout_status']}`",
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
            "make reviewer_question_maintainer_closeout_digest",
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
    print(f"closeout_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
