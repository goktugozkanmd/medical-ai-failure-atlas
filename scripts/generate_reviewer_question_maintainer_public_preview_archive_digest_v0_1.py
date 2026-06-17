#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLOSURE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_closure_checklist_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_archive_digest_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ARCHIVE_DIGEST_V0_1.md"

ARCHIVE_ROWS = [
    {
        "archive_id": "RQPA001",
        "source_closure_id": "RQPC001",
        "archive_name": "Synthetic boundary archive",
        "archive_note": "archive the synthetic only boundary as a closed public preview check",
    },
    {
        "archive_id": "RQPA002",
        "source_closure_id": "RQPC002",
        "archive_name": "Reviewer question lane archive",
        "archive_note": "archive the source facing reviewer question lane check without benchmark scoring",
    },
    {
        "archive_id": "RQPA003",
        "source_closure_id": "RQPC003",
        "archive_name": "Public wording archive",
        "archive_note": "archive the blocked public wording checks for validation, compatibility, endpoint, and endorsement claims",
    },
    {
        "archive_id": "RQPA004",
        "source_closure_id": "RQPC004",
        "archive_name": "Release surface archive",
        "archive_note": "archive release surface checks without official endorsement or route access claims",
    },
    {
        "archive_id": "RQPA005",
        "source_closure_id": "RQPC005",
        "archive_name": "Validation archive",
        "archive_note": "archive the runnable check requirement for closure rows and safety boundaries",
    },
]


def main() -> None:
    closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
    closure_ids = {row["closure_id"] for row in closure["rows"]}
    rows: list[dict[str, Any]] = []
    for row in ARCHIVE_ROWS:
        if row["source_closure_id"] not in closure_ids:
            raise ValueError(f"missing source closure id: {row['source_closure_id']}")
        rows.append(
            {
                **row,
                "archive_state": "archived_for_public_preview_trace",
                "archive_boundary": "synthetic only and not for clinical use",
                "archive_decision": "archive public preview checklist item only",
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
        "version": "reviewer_question_maintainer_public_preview_archive_digest_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_maintainer_public_preview_closure_checklist_v0_1.json",
        "archive_row_count": len(rows),
        "closure_rows_represented": closure["closure_row_count"],
        "handoff_rows_represented": closure["handoff_rows_represented"],
        "decision_rows_represented": closure["decision_rows_represented"],
        "candidate_summary_rows_represented": closure["candidate_summary_rows_represented"],
        "audit_trail_rows_represented": closure["audit_trail_rows_represented"],
        "evidence_rows_represented": closure["evidence_rows_represented"],
        "readiness_rows_represented": closure["readiness_rows_represented"],
        "closeout_rows_represented": closure["closeout_rows_represented"],
        "contributor_digest_rows_represented": closure["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": closure["release_index_surface_rows_represented"],
        "issue_history_rows_represented": closure["issue_history_rows_represented"],
        "previous_public_issue_number": 64,
        "public_preview_archive": "archived_for_public_preview_trace",
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
        "# Reviewer question maintainer public preview archive digest v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This archive digest records the closed reviewer question maintainer public preview checklist items as a compact trace.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Archive rows: {len(rows)}",
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
        "Public preview archive: `archived_for_public_preview_trace`",
        "",
        "## Maintainer archive rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['archive_id']}",
                "",
                f"Archive name: {row['archive_name']}",
                "",
                f"Source closure row: `{row['source_closure_id']}`",
                "",
                f"Archive note: {row['archive_note']}",
                "",
                f"Archive state: `{row['archive_state']}`",
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
            "make reviewer_question_maintainer_public_preview_archive_digest",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview index rollup without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"archive_rows={len(rows)}")


if __name__ == "__main__":
    main()
