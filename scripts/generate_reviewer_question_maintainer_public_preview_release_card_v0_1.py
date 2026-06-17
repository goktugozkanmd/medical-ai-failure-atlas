#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NAVIGATION = ROOT / "docs" / "reviewer_question_maintainer_public_preview_repository_navigation_note_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_release_card_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_RELEASE_CARD_V0_1.md"

CARD_ROWS = [
    {
        "card_id": "RQPR001",
        "source_navigation_id": "RQPN001",
        "card_name": "Boundary release card row",
        "card_note": "show the synthetic only and not for clinical use boundary first",
    },
    {
        "card_id": "RQPR002",
        "source_navigation_id": "RQPN002",
        "card_name": "Reviewer question route card row",
        "card_note": "show the reviewer question route as source facing public preview infrastructure",
    },
    {
        "card_id": "RQPR003",
        "source_navigation_id": "RQPN003",
        "card_name": "Wording discipline card row",
        "card_note": "show that wording gates block validation, compatibility, endpoint, and endorsement claims",
    },
    {
        "card_id": "RQPR004",
        "source_navigation_id": "RQPN004",
        "card_name": "Release surface card row",
        "card_note": "show release surfaces as trace material without route access or official endorsement",
    },
    {
        "card_id": "RQPR005",
        "source_navigation_id": "RQPN005",
        "card_name": "Validation card row",
        "card_note": "show the runnable checks that maintain the public preview boundary",
    },
    {
        "card_id": "RQPR006",
        "source_navigation_id": "RQPN006",
        "card_name": "Next build card row",
        "card_note": "show the next public build as contributor route material inside the same boundary",
    },
]


def main() -> None:
    navigation = json.loads(NAVIGATION.read_text(encoding="utf-8"))
    navigation_ids = {row["navigation_id"] for row in navigation["rows"]}
    rows: list[dict[str, Any]] = []
    for row in CARD_ROWS:
        if row["source_navigation_id"] not in navigation_ids:
            raise ValueError(f"missing source navigation id: {row['source_navigation_id']}")
        rows.append(
            {
                **row,
                "card_state": "ready_for_public_preview_release_card",
                "card_boundary": "synthetic only and not for clinical use",
                "card_decision": "publish release card only",
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
        "version": "reviewer_question_maintainer_public_preview_release_card_v0_1",
        "status": "public_preview",
        "date": "2026 06 18",
        "source": "docs/reviewer_question_maintainer_public_preview_repository_navigation_note_v0_1.json",
        "release_card_row_count": len(rows),
        "navigation_rows_represented": navigation["navigation_row_count"],
        "rollup_rows_represented": navigation["rollup_rows_represented"],
        "archive_rows_represented": navigation["archive_rows_represented"],
        "closure_rows_represented": navigation["closure_rows_represented"],
        "handoff_rows_represented": navigation["handoff_rows_represented"],
        "decision_rows_represented": navigation["decision_rows_represented"],
        "candidate_summary_rows_represented": navigation["candidate_summary_rows_represented"],
        "audit_trail_rows_represented": navigation["audit_trail_rows_represented"],
        "evidence_rows_represented": navigation["evidence_rows_represented"],
        "readiness_rows_represented": navigation["readiness_rows_represented"],
        "closeout_rows_represented": navigation["closeout_rows_represented"],
        "contributor_digest_rows_represented": navigation["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": navigation["release_index_surface_rows_represented"],
        "issue_history_rows_represented": navigation["issue_history_rows_represented"],
        "previous_public_issue_number": 67,
        "public_preview_release_card": "ready_for_public_preview_release_card",
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
        "# Reviewer question maintainer public preview release card v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 18",
        "",
        "This release card gives one compact public entry point for the reviewer question maintainer public preview route.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Release card rows: {len(rows)}",
        "",
        f"Navigation rows represented: {data['navigation_rows_represented']}",
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
        "Public preview release card: `ready_for_public_preview_release_card`",
        "",
        "## Release card rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['card_id']}",
                "",
                f"Card name: {row['card_name']}",
                "",
                f"Source navigation row: `{row['source_navigation_id']}`",
                "",
                f"Card note: {row['card_note']}",
                "",
                f"Card state: `{row['card_state']}`",
                "",
                f"Card decision: {row['card_decision']}",
                "",
                f"Card boundary: {row['card_boundary']}",
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
            "make reviewer_question_maintainer_public_preview_release_card",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview contributor route note without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"release_card_rows={len(rows)}")


if __name__ == "__main__":
    main()
