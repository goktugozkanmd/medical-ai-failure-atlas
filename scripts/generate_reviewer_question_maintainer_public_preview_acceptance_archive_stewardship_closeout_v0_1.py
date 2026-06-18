#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_steward_index_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_stewardship_closeout_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ACCEPTANCE_ARCHIVE_STEWARDSHIP_CLOSEOUT_V0_1.md"

STEWARDSHIP_CLOSEOUT_ROWS = [
    {
        "stewardship_closeout_id": "RQPSC001",
        "source_steward_index_id": "RQPSI001",
        "stewardship_closeout_name": "Boundary stewardship closeout row",
        "stewardship_closeout_note": "close out boundary review only when synthetic only and not for clinical use wording remains visible",
    },
    {
        "stewardship_closeout_id": "RQPSC002",
        "source_steward_index_id": "RQPSI002",
        "stewardship_closeout_name": "Reviewer question stewardship closeout row",
        "stewardship_closeout_note": "close out reviewer question completeness checks without scoring or endpoint claims",
    },
    {
        "stewardship_closeout_id": "RQPSC003",
        "source_steward_index_id": "RQPSI003",
        "stewardship_closeout_name": "Blocked wording stewardship closeout row",
        "stewardship_closeout_note": "close out blocked wording separation before maintainer visible updates",
    },
    {
        "stewardship_closeout_id": "RQPSC004",
        "source_steward_index_id": "RQPSI004",
        "stewardship_closeout_name": "Public surface stewardship closeout row",
        "stewardship_closeout_note": "close out public surface wording only when access and endorsement boundaries remain explicit",
    },
    {
        "stewardship_closeout_id": "RQPSC005",
        "source_steward_index_id": "RQPSI005",
        "stewardship_closeout_name": "Validation stewardship closeout row",
        "stewardship_closeout_note": "close out generated artifact validation before public maintainer archive updates",
    },
    {
        "stewardship_closeout_id": "RQPSC006",
        "source_steward_index_id": "RQPSI006",
        "stewardship_closeout_name": "Next build stewardship closeout row",
        "stewardship_closeout_note": "close out the next public preview handoff only inside the same bounded archive route",
    },
]


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    steward_index_ids = {row["steward_index_id"] for row in source["rows"]}
    rows: list[dict[str, Any]] = []
    for row in STEWARDSHIP_CLOSEOUT_ROWS:
        if row["source_steward_index_id"] not in steward_index_ids:
            raise ValueError(f"missing source steward index id: {row['source_steward_index_id']}")
        rows.append(
            {
                **row,
                "stewardship_closeout_state": "ready_for_public_preview_acceptance_archive_stewardship_closeout",
                "stewardship_closeout_boundary": "synthetic only and not for clinical use",
                "stewardship_closeout_decision": "publish acceptance archive stewardship closeout only",
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
        "version": "reviewer_question_maintainer_public_preview_acceptance_archive_stewardship_closeout_v0_1",
        "status": "public_preview",
        "date": "2026 06 18",
        "source": "docs/reviewer_question_maintainer_public_preview_acceptance_archive_steward_index_v0_1.json",
        "acceptance_archive_stewardship_closeout_row_count": len(rows),
        "acceptance_archive_steward_index_rows_represented": source["acceptance_archive_steward_index_row_count"],
        "acceptance_archive_steward_note_rows_represented": source["acceptance_archive_steward_note_rows_represented"],
        "acceptance_archive_handoff_packet_rows_represented": source["acceptance_archive_handoff_packet_rows_represented"],
        "acceptance_archive_final_index_rows_represented": source["acceptance_archive_final_index_rows_represented"],
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
        "issue_history_rows_represented": source["issue_history_rows_represented"] + 1,
        "previous_public_issue_number": 79,
        "public_preview_acceptance_archive_stewardship_closeout": "ready_for_public_preview_acceptance_archive_stewardship_closeout",
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
        "# Reviewer question maintainer public preview acceptance archive stewardship closeout v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 18",
        "",
        "This acceptance archive stewardship closeout gives a compact public closeout layer for reviewer question maintainer archive stewardship checks.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Acceptance archive stewardship closeout rows: {len(rows)}",
        "",
        f"Acceptance archive steward index rows represented: {data['acceptance_archive_steward_index_rows_represented']}",
        "",
        f"Acceptance archive steward note rows represented: {data['acceptance_archive_steward_note_rows_represented']}",
        "",
        f"Acceptance archive handoff packet rows represented: {data['acceptance_archive_handoff_packet_rows_represented']}",
        "",
        f"Acceptance archive final index rows represented: {data['acceptance_archive_final_index_rows_represented']}",
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
        "Public preview acceptance archive stewardship closeout: `ready_for_public_preview_acceptance_archive_stewardship_closeout`",
        "",
        "## Acceptance archive stewardship closeout rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['stewardship_closeout_id']}",
                "",
                f"Stewardship closeout name: {row['stewardship_closeout_name']}",
                "",
                f"Source acceptance archive steward index row: `{row['source_steward_index_id']}`",
                "",
                f"Stewardship closeout note: {row['stewardship_closeout_note']}",
                "",
                f"Stewardship closeout state: `{row['stewardship_closeout_state']}`",
                "",
                f"Stewardship closeout decision: {row['stewardship_closeout_decision']}",
                "",
                f"Stewardship closeout boundary: {row['stewardship_closeout_boundary']}",
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
            "make reviewer_question_maintainer_public_preview_acceptance_archive_stewardship_closeout",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview acceptance archive stewardship digest without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"acceptance_archive_stewardship_closeout_rows={len(rows)}")


if __name__ == "__main__":
    main()
