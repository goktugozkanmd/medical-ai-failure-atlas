#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_issue_template_route_note_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_maintainer_acceptance_checklist_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_MAINTAINER_ACCEPTANCE_CHECKLIST_V0_1.md"

ACCEPTANCE_ROWS = [
    {
        "acceptance_check_id": "RQPA001",
        "source_template_route_id": "RQPI001",
        "acceptance_check_name": "Boundary acceptance check row",
        "acceptance_check_note": "accept only synthetic only and not for clinical use wording",
    },
    {
        "acceptance_check_id": "RQPA002",
        "source_template_route_id": "RQPI002",
        "acceptance_check_name": "Reviewer question acceptance check row",
        "acceptance_check_note": "accept reviewer question proposals only when the public fields are complete",
    },
    {
        "acceptance_check_id": "RQPA003",
        "source_template_route_id": "RQPI003",
        "acceptance_check_name": "Blocked wording acceptance check row",
        "acceptance_check_note": "accept only if blocked wording is clearly separated from publishable wording",
    },
    {
        "acceptance_check_id": "RQPA004",
        "source_template_route_id": "RQPI004",
        "acceptance_check_name": "Public surface acceptance check row",
        "acceptance_check_note": "accept only if public surface references avoid access and endorsement claims",
    },
    {
        "acceptance_check_id": "RQPA005",
        "source_template_route_id": "RQPI005",
        "acceptance_check_name": "Validation acceptance check row",
        "acceptance_check_note": "accept only if local generated artifact checks pass before public maintainer review",
    },
    {
        "acceptance_check_id": "RQPA006",
        "source_template_route_id": "RQPI006",
        "acceptance_check_name": "Next build acceptance check row",
        "acceptance_check_note": "accept only if next maintainer material stays inside the same public preview boundary",
    },
]


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    template_route_ids = {row["template_route_id"] for row in source["rows"]}
    rows: list[dict[str, Any]] = []
    for row in ACCEPTANCE_ROWS:
        if row["source_template_route_id"] not in template_route_ids:
            raise ValueError(f"missing source template route id: {row['source_template_route_id']}")
        rows.append(
            {
                **row,
                "acceptance_check_state": "ready_for_public_preview_maintainer_acceptance_checklist",
                "acceptance_boundary": "synthetic only and not for clinical use",
                "acceptance_decision": "publish maintainer acceptance checklist only",
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
        "version": "reviewer_question_maintainer_public_preview_maintainer_acceptance_checklist_v0_1",
        "status": "public_preview",
        "date": "2026 06 18",
        "source": "docs/reviewer_question_maintainer_public_preview_issue_template_route_note_v0_1.json",
        "maintainer_acceptance_checklist_row_count": len(rows),
        "issue_template_route_note_rows_represented": source["issue_template_route_note_row_count"],
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
        "previous_public_issue_number": 70,
        "public_preview_maintainer_acceptance_checklist": "ready_for_public_preview_maintainer_acceptance_checklist",
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
        "# Reviewer question maintainer public preview maintainer acceptance checklist v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 18",
        "",
        "This maintainer acceptance checklist gives a compact public acceptance path for reviewer question proposal fields after the issue template route note.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Maintainer acceptance checklist rows: {len(rows)}",
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
        "Public preview maintainer acceptance checklist: `ready_for_public_preview_maintainer_acceptance_checklist`",
        "",
        "## Maintainer acceptance checklist rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['acceptance_check_id']}",
                "",
                f"Acceptance check name: {row['acceptance_check_name']}",
                "",
                f"Source issue template route row: `{row['source_template_route_id']}`",
                "",
                f"Acceptance check note: {row['acceptance_check_note']}",
                "",
                f"Acceptance check state: `{row['acceptance_check_state']}`",
                "",
                f"Acceptance decision: {row['acceptance_decision']}",
                "",
                f"Acceptance boundary: {row['acceptance_boundary']}",
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
            "make reviewer_question_maintainer_public_preview_maintainer_acceptance_checklist",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview acceptance closeout digest without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"maintainer_acceptance_checklist_rows={len(rows)}")


if __name__ == "__main__":
    main()
