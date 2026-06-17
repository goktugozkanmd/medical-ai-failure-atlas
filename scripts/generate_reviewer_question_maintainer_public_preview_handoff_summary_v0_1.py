#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DECISION_LOG = ROOT / "docs" / "reviewer_question_maintainer_public_preview_decision_log_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_handoff_summary_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_HANDOFF_SUMMARY_V0_1.md"

HANDOFF_ROWS = [
    {
        "handoff_id": "RQPH001",
        "source_decision_id": "RQMP001",
        "handoff_name": "Synthetic boundary handoff",
        "handoff_owner": "maintainer reviewer",
        "next_reviewer_action": "confirm synthetic only boundary text before public preview update",
    },
    {
        "handoff_id": "RQPH002",
        "source_decision_id": "RQMP002",
        "handoff_name": "Reviewer question lane handoff",
        "handoff_owner": "reviewer question maintainer",
        "next_reviewer_action": "confirm reviewer question lane links stay source facing and do not imply benchmark scoring",
    },
    {
        "handoff_id": "RQPH003",
        "source_decision_id": "RQMP003",
        "handoff_name": "Public wording handoff",
        "handoff_owner": "public wording reviewer",
        "next_reviewer_action": "confirm public wording blocks clinical validation, compatibility, endpoint, and endorsement claims",
    },
    {
        "handoff_id": "RQPH004",
        "source_decision_id": "RQMP004",
        "handoff_name": "Release surface handoff",
        "handoff_owner": "release surface reviewer",
        "next_reviewer_action": "confirm release note and dashboard links expose the decision route without official role claims",
    },
    {
        "handoff_id": "RQPH005",
        "source_decision_id": "RQMP005",
        "handoff_name": "Validation handoff",
        "handoff_owner": "validator maintainer",
        "next_reviewer_action": "confirm runnable checks fail when decision rows or safety boundaries are missing",
    },
]


def main() -> None:
    decision_log = json.loads(DECISION_LOG.read_text(encoding="utf-8"))
    decision_ids = {row["decision_id"] for row in decision_log["rows"]}
    rows: list[dict[str, Any]] = []
    for row in HANDOFF_ROWS:
        if row["source_decision_id"] not in decision_ids:
            raise ValueError(f"missing source decision id: {row['source_decision_id']}")
        rows.append(
            {
                **row,
                "handoff_state": "ready_for_maintainer_public_preview_review",
                "handoff_boundary": "synthetic only and not for clinical use",
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
                ],
            }
        )

    data: dict[str, Any] = {
        "version": "reviewer_question_maintainer_public_preview_handoff_summary_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_maintainer_public_preview_decision_log_v0_1.json",
        "handoff_row_count": len(rows),
        "decision_rows_represented": decision_log["decision_row_count"],
        "candidate_summary_rows_represented": decision_log["candidate_summary_rows_represented"],
        "audit_trail_rows_represented": decision_log["audit_trail_rows_represented"],
        "evidence_rows_represented": decision_log["evidence_rows_represented"],
        "readiness_rows_represented": decision_log["readiness_rows_represented"],
        "closeout_rows_represented": decision_log["closeout_rows_represented"],
        "handoff_rows_represented": decision_log["handoff_rows_represented"],
        "contributor_digest_rows_represented": decision_log["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": decision_log["release_index_surface_rows_represented"],
        "issue_history_rows_represented": decision_log["issue_history_rows_represented"],
        "previous_public_issue_number": 62,
        "public_preview_handoff": "ready_for_maintainer_public_preview_review",
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
        "# Reviewer question maintainer public preview handoff summary v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This handoff summary turns the maintainer public preview decision log into reviewer actions for the next public preview update.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Handoff rows: {len(rows)}",
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
        "Public preview handoff: `ready_for_maintainer_public_preview_review`",
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
                f"Source decision row: `{row['source_decision_id']}`",
                "",
                f"Handoff owner: {row['handoff_owner']}",
                "",
                f"Next reviewer action: {row['next_reviewer_action']}",
                "",
                f"Handoff state: `{row['handoff_state']}`",
                "",
                f"Handoff boundary: {row['handoff_boundary']}",
                "",
                "Blocked claims: benchmark scoring, benchmark compatibility, benchmark equivalence, endpoint result, patient data, clinical validation, clinical deployment, model ranking, official endorsement",
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
            "make reviewer_question_maintainer_public_preview_handoff_summary",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview closure checklist without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"handoff_rows={len(rows)}")


if __name__ == "__main__":
    main()
