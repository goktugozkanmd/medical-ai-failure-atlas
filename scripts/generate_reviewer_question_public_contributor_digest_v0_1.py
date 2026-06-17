#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RELEASE_INDEX = ROOT / "docs" / "reviewer_question_public_release_index_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_public_contributor_digest_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_PUBLIC_CONTRIBUTOR_DIGEST_V0_1.md"

DIGEST_STEPS = [
    {
        "step_id": "RQCD001",
        "step_name": "Read the reviewer question release index",
        "public_file": "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_INDEX_V0_1.md",
        "contributor_action": "start from the public route index",
    },
    {
        "step_id": "RQCD002",
        "step_name": "Choose the matching reviewer question surface",
        "public_file": "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
        "contributor_action": "select a source support, escalation, medication safety, missing context, policy wording, or warning sign question",
    },
    {
        "step_id": "RQCD003",
        "step_name": "Match an intake example",
        "public_file": "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
        "contributor_action": "match the proposed contribution to a synthetic intake example",
    },
    {
        "step_id": "RQCD004",
        "step_name": "Check wording boundaries",
        "public_file": "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "contributor_action": "avoid score, compatibility, endpoint, patient data, clinical validation, and endorsement wording",
    },
    {
        "step_id": "RQCD005",
        "step_name": "Run the release index check",
        "public_file": "Makefile",
        "contributor_action": "run make reviewer_question_release_index before opening or updating an issue",
    },
]


def main() -> int:
    release_index = json.loads(RELEASE_INDEX.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = [
        {
            **row,
            "digest_status": "included_in_public_contributor_digest",
            "boundary": "synthetic only and not for clinical use",
        }
        for row in DIGEST_STEPS
    ]

    data: dict[str, Any] = {
        "version": "reviewer_question_public_contributor_digest_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_public_release_index_v0_1.json",
        "digest_step_count": len(rows),
        "release_index_surface_rows_represented": release_index["index_surface_count"],
        "issue_history_rows_represented": release_index["issue_history_count"],
        "digest_decision": "ready_for_public_preview",
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
        "# Reviewer question public contributor digest v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This digest gives contributors a short orientation path for using the reviewer question release index before opening or updating a synthetic SourceCheckup or Failure Atlas issue.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Digest step rows: {len(rows)}",
        "",
        f"Release index surface rows represented: {data['release_index_surface_rows_represented']}",
        "",
        f"Issue history rows represented: {data['issue_history_rows_represented']}",
        "",
        "Digest decision: `ready_for_public_preview`",
        "",
        "## Contributor steps",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['step_id']}",
                "",
                f"Step name: {row['step_name']}",
                "",
                f"Public file: `{row['public_file']}`",
                "",
                f"Contributor action: {row['contributor_action']}",
                "",
                f"Digest status: `{row['digest_status']}`",
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
            "make reviewer_question_contributor_digest",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer release candidate summary without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"digest_step_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
