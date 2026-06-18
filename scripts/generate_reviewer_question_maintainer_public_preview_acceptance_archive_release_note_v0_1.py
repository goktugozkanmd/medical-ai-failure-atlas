#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_index_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_release_note_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ACCEPTANCE_ARCHIVE_RELEASE_NOTE_V0_1.md"

RELEASE_NOTE_ROWS = [
    {
        "release_note_id": "RQPN001",
        "source_archive_index_id": "RQPX001",
        "release_note_name": "Boundary release note row",
        "release_note_note": "release only when synthetic only and not for clinical use wording remains visible",
    },
    {
        "release_note_id": "RQPN002",
        "source_archive_index_id": "RQPX002",
        "release_note_name": "Reviewer question release note row",
        "release_note_note": "release only when reviewer question proposal fields are complete and bounded",
    },
    {
        "release_note_id": "RQPN003",
        "source_archive_index_id": "RQPX003",
        "release_note_name": "Blocked wording release note row",
        "release_note_note": "release only when blocked wording stays separated from publishable wording",
    },
    {
        "release_note_id": "RQPN004",
        "source_archive_index_id": "RQPX004",
        "release_note_name": "Public surface release note row",
        "release_note_note": "release only when public surface references avoid access and endorsement claims",
    },
    {
        "release_note_id": "RQPN005",
        "source_archive_index_id": "RQPX005",
        "release_note_name": "Validation release note row",
        "release_note_note": "release only when generated artifact checks are recorded before public maintainer review",
    },
    {
        "release_note_id": "RQPN006",
        "source_archive_index_id": "RQPX006",
        "release_note_name": "Next build release note row",
        "release_note_note": "release only when next maintainer material stays inside the same public preview boundary",
    },
]


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    archive_index_ids = {row["archive_index_id"] for row in source["rows"]}
    rows: list[dict[str, Any]] = []
    for row in RELEASE_NOTE_ROWS:
        if row["source_archive_index_id"] not in archive_index_ids:
            raise ValueError(f"missing source archive index id: {row['source_archive_index_id']}")
        rows.append(
            {
                **row,
                "release_note_state": "ready_for_public_preview_acceptance_archive_release_note",
                "archive_boundary": "synthetic only and not for clinical use",
                "archive_decision": "publish acceptance archive release note only",
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
        "version": "reviewer_question_maintainer_public_preview_acceptance_archive_release_note_v0_1",
        "status": "public_preview",
        "date": "2026 06 18",
        "source": "docs/reviewer_question_maintainer_public_preview_acceptance_archive_index_v0_1.json",
        "acceptance_archive_release_note_row_count": len(rows),
        "acceptance_archive_index_rows_represented": source["acceptance_archive_index_row_count"],
        "issue_template_route_note_rows_represented": source["issue_template_route_note_rows_represented"],
        "contributor_route_note_rows_represented": source["contributor_route_note_rows_represented"],
        "release_card_rows_represented": source["release_card_rows_represented"],
        "navigation_rows_represented": source["navigation_rows_represented"],
        "rollup_rows_represented": source["rollup_rows_represented"],
        "archive_rows_represented": source["archive_rows_represented"],
        "closure_rows_represented": source["closure_rows_represented"],
        "handoff_rows_represented": source["handoff_rows_represented"],
        "decision_rows_represented": source["decision_rows_represented"],
        "candidate_summary_rows_represented": source["candidate_summary_rows_represented"],
        "audit_trail_rows_represented": source["audit_trail_rows_represented"],
        "evidence_rows_represented": source["evidence_rows_represented"],
        "readiness_rows_represented": source["readiness_rows_represented"],
        "closeout_rows_represented": source["closeout_rows_represented"],
        "contributor_digest_rows_represented": source["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": source["release_index_surface_rows_represented"],
        "issue_history_rows_represented": source["issue_history_rows_represented"],
        "previous_public_issue_number": 73,
        "public_preview_acceptance_archive_release_note": "ready_for_public_preview_acceptance_archive_release_note",
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
        "# Reviewer question maintainer public preview acceptance archive release note v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 18",
        "",
        "This acceptance archive release note gives a compact public archive path for reviewer question maintainer acceptance checks.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Acceptance archive release note rows: {len(rows)}",
        "",
        f"Acceptance archive index rows represented: {data['acceptance_archive_index_rows_represented']}",
        "",
        f"Issue template route note rows represented: {data['issue_template_route_note_rows_represented']}",
        "",
        f"Contributor route note rows represented: {data['contributor_route_note_rows_represented']}",
        "",
        f"Release card rows represented: {data['release_card_rows_represented']}",
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
        "Public preview acceptance archive release note: `ready_for_public_preview_acceptance_archive_release_note`",
        "",
        "## Acceptance archive release note rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['release_note_id']}",
                "",
                f"Release note name: {row['release_note_name']}",
                "",
                f"Source archive index row: `{row['source_archive_index_id']}`",
                "",
                f"Release note note: {row['release_note_note']}",
                "",
                f"Release note state: `{row['release_note_state']}`",
                "",
                f"Archive decision: {row['archive_decision']}",
                "",
                f"Archive boundary: {row['archive_boundary']}",
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
            "make reviewer_question_maintainer_public_preview_acceptance_archive_release_note",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview acceptance archive closure note without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"acceptance_archive_release_note_rows={len(rows)}")


if __name__ == "__main__":
    main()
