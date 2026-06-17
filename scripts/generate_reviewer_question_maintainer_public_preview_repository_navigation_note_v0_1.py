#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INDEX_ROLLUP = ROOT / "docs" / "reviewer_question_maintainer_public_preview_index_rollup_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_repository_navigation_note_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_REPOSITORY_NAVIGATION_NOTE_V0_1.md"

NAVIGATION_ROWS = [
    {
        "navigation_id": "RQPN001",
        "source_rollup_id": "RQPI001",
        "navigation_name": "Boundary first navigation",
        "navigation_note": "start with the synthetic only boundary before reading any reviewer question route",
    },
    {
        "navigation_id": "RQPN002",
        "source_rollup_id": "RQPI002",
        "navigation_name": "Reviewer question route navigation",
        "navigation_note": "read the reviewer question lane as source facing infrastructure without scoring",
    },
    {
        "navigation_id": "RQPN003",
        "source_rollup_id": "RQPI003",
        "navigation_name": "Public wording navigation",
        "navigation_note": "check wording gates before using public language about validation or compatibility",
    },
    {
        "navigation_id": "RQPN004",
        "source_rollup_id": "RQPI004",
        "navigation_name": "Release surface navigation",
        "navigation_note": "use release surfaces as public trace material without endorsement or route access claims",
    },
    {
        "navigation_id": "RQPN005",
        "source_rollup_id": "RQPI005",
        "navigation_name": "Validation navigation",
        "navigation_note": "run the maintainer checks before updating public preview navigation",
    },
    {
        "navigation_id": "RQPN006",
        "source_rollup_id": "RQPI006",
        "navigation_name": "Next build navigation",
        "navigation_note": "keep the next public build inside synthetic repository navigation boundaries",
    },
]


def main() -> None:
    rollup = json.loads(INDEX_ROLLUP.read_text(encoding="utf-8"))
    rollup_ids = {row["rollup_id"] for row in rollup["rows"]}
    rows: list[dict[str, Any]] = []
    for row in NAVIGATION_ROWS:
        if row["source_rollup_id"] not in rollup_ids:
            raise ValueError(f"missing source rollup id: {row['source_rollup_id']}")
        rows.append(
            {
                **row,
                "navigation_state": "ready_for_public_preview_navigation",
                "navigation_boundary": "synthetic only and not for clinical use",
                "navigation_decision": "publish repository navigation only",
                "blocked_claims": [
                    "benchmark scoring",
                    "benchmark compatibility",
                    "benchmark equivalence",
                    "endpoint result",
                    "patient data",
                    "clinical validation",
                    "clinical deployment",
                    "model ranking",
                    "official endorsement",
                    "route access",
                ],
            }
        )

    data: dict[str, Any] = {
        "version": "reviewer_question_maintainer_public_preview_repository_navigation_note_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_maintainer_public_preview_index_rollup_v0_1.json",
        "navigation_row_count": len(rows),
        "rollup_rows_represented": rollup["rollup_row_count"],
        "archive_rows_represented": rollup["archive_rows_represented"],
        "closure_rows_represented": rollup["closure_rows_represented"],
        "handoff_rows_represented": rollup["handoff_rows_represented"],
        "decision_rows_represented": rollup["decision_rows_represented"],
        "candidate_summary_rows_represented": rollup["candidate_summary_rows_represented"],
        "audit_trail_rows_represented": rollup["audit_trail_rows_represented"],
        "evidence_rows_represented": rollup["evidence_rows_represented"],
        "readiness_rows_represented": rollup["readiness_rows_represented"],
        "closeout_rows_represented": rollup["closeout_rows_represented"],
        "contributor_digest_rows_represented": rollup["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": rollup["release_index_surface_rows_represented"],
        "issue_history_rows_represented": rollup["issue_history_rows_represented"],
        "previous_public_issue_number": 66,
        "public_preview_navigation": "ready_for_public_preview_navigation",
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
        "no_route_access_claim": True,
        "rows": rows,
    }
    JSON_OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Reviewer question maintainer public preview repository navigation note v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This repository navigation note gives maintainers one ordered route through the reviewer question public preview materials.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Navigation rows: {len(rows)}",
        "",
        f"Rollup rows represented: {data['rollup_rows_represented']}",
        "",
        f"Archive rows represented: {data['archive_rows_represented']}",
        "",
        f"Closure rows represented: {data['closure_rows_represented']}",
        "",
        f"Handoff rows represented: {data['handoff_rows_represented']}",
        "",
        f"Decision rows represented: {data['decision_rows_represented']}",
        "",
        f"Candidate summary rows represented: {data['candidate_summary_rows_represented']}",
        "",
        f"Audit trail rows represented: {data['audit_trail_rows_represented']}",
        "",
        f"Evidence rows represented: {data['evidence_rows_represented']}",
        "",
        f"Readiness rows represented: {data['readiness_rows_represented']}",
        "",
        f"Closeout rows represented: {data['closeout_rows_represented']}",
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
        "Public preview navigation: `ready_for_public_preview_navigation`",
        "",
        "## Maintainer navigation rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['navigation_id']}",
                "",
                f"Navigation name: {row['navigation_name']}",
                "",
                f"Source rollup row: `{row['source_rollup_id']}`",
                "",
                f"Navigation note: {row['navigation_note']}",
                "",
                f"Navigation state: `{row['navigation_state']}`",
                "",
                f"Navigation decision: {row['navigation_decision']}",
                "",
                f"Navigation boundary: {row['navigation_boundary']}",
                "",
                "Blocked claims: benchmark scoring, benchmark compatibility, benchmark equivalence, endpoint result, patient data, clinical validation, clinical deployment, model ranking, official endorsement, route access",
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
            "make reviewer_question_maintainer_public_preview_repository_navigation_note",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview release card without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"navigation_rows={len(rows)}")


if __name__ == "__main__":
    main()
