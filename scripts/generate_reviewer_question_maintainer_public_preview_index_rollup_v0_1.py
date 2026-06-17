#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_archive_digest_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_index_rollup_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_INDEX_ROLLUP_V0_1.md"

ROLLUP_ROWS = [
    {
        "rollup_id": "RQPI001",
        "source_archive_id": "RQPA001",
        "rollup_name": "Synthetic boundary entry point",
        "rollup_note": "surface the synthetic only boundary as the first maintainer index item",
    },
    {
        "rollup_id": "RQPI002",
        "source_archive_id": "RQPA002",
        "rollup_name": "Reviewer question lane entry point",
        "rollup_note": "surface the reviewer question lane without benchmark scoring or compatibility claims",
    },
    {
        "rollup_id": "RQPI003",
        "source_archive_id": "RQPA003",
        "rollup_name": "Public wording entry point",
        "rollup_note": "surface blocked wording for validation, compatibility, endpoint, and endorsement claims",
    },
    {
        "rollup_id": "RQPI004",
        "source_archive_id": "RQPA004",
        "rollup_name": "Release surface entry point",
        "rollup_note": "surface release links without official endorsement or route access claims",
    },
    {
        "rollup_id": "RQPI005",
        "source_archive_id": "RQPA005",
        "rollup_name": "Validation entry point",
        "rollup_note": "surface the runnable checks for public preview rows and safety boundaries",
    },
    {
        "rollup_id": "RQPI006",
        "source_archive_id": "RQPA005",
        "rollup_name": "Next build entry point",
        "rollup_note": "surface the next safe repository navigation note without endpoint or patient data claims",
    },
]


def main() -> None:
    archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
    archive_ids = {row["archive_id"] for row in archive["rows"]}
    rows: list[dict[str, Any]] = []
    for row in ROLLUP_ROWS:
        if row["source_archive_id"] not in archive_ids:
            raise ValueError(f"missing source archive id: {row['source_archive_id']}")
        rows.append(
            {
                **row,
                "rollup_state": "indexed_for_public_preview_navigation",
                "rollup_boundary": "synthetic only and not for clinical use",
                "rollup_decision": "index public preview item only",
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
        "version": "reviewer_question_maintainer_public_preview_index_rollup_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_maintainer_public_preview_archive_digest_v0_1.json",
        "rollup_row_count": len(rows),
        "archive_rows_represented": archive["archive_row_count"],
        "closure_rows_represented": archive["closure_rows_represented"],
        "handoff_rows_represented": archive["handoff_rows_represented"],
        "decision_rows_represented": archive["decision_rows_represented"],
        "candidate_summary_rows_represented": archive["candidate_summary_rows_represented"],
        "audit_trail_rows_represented": archive["audit_trail_rows_represented"],
        "evidence_rows_represented": archive["evidence_rows_represented"],
        "readiness_rows_represented": archive["readiness_rows_represented"],
        "closeout_rows_represented": archive["closeout_rows_represented"],
        "contributor_digest_rows_represented": archive["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": archive["release_index_surface_rows_represented"],
        "issue_history_rows_represented": archive["issue_history_rows_represented"],
        "previous_public_issue_number": 65,
        "public_preview_index": "indexed_for_public_preview_navigation",
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
        "# Reviewer question maintainer public preview index rollup v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This index rollup gives one maintainer navigation surface for the reviewer question public preview route.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Rollup rows: {len(rows)}",
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
        "Public preview index: `indexed_for_public_preview_navigation`",
        "",
        "## Maintainer index rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['rollup_id']}",
                "",
                f"Rollup name: {row['rollup_name']}",
                "",
                f"Source archive row: `{row['source_archive_id']}`",
                "",
                f"Rollup note: {row['rollup_note']}",
                "",
                f"Rollup state: `{row['rollup_state']}`",
                "",
                f"Rollup decision: {row['rollup_decision']}",
                "",
                f"Rollup boundary: {row['rollup_boundary']}",
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
            "make reviewer_question_maintainer_public_preview_index_rollup",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview repository navigation note without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"rollup_rows={len(rows)}")


if __name__ == "__main__":
    main()
