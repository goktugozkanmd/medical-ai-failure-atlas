#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT = ROOT / "docs" / "reviewer_question_maintainer_closeout_digest_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_release_readiness_digest_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_RELEASE_READINESS_DIGEST_V0_1.md"

READINESS_ROWS = [
    {
        "readiness_id": "RQMR001",
        "readiness_name": "Synthetic boundary readiness",
        "evidence_file": "docs/REVIEWER_QUESTION_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md",
        "readiness_action": "confirm closeout keeps public reviewer question rows synthetic only",
    },
    {
        "readiness_id": "RQMR002",
        "readiness_name": "Reviewer question lane readiness",
        "evidence_file": "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
        "readiness_action": "confirm public reviewer question lanes remain bounded and source facing",
    },
    {
        "readiness_id": "RQMR003",
        "readiness_name": "Public wording readiness",
        "evidence_file": "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "readiness_action": "confirm blocked score, endpoint, compatibility, validation, and endorsement wording stays out",
    },
    {
        "readiness_id": "RQMR004",
        "readiness_name": "Release surface readiness",
        "evidence_file": "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
        "readiness_action": "confirm release surfaces mention boundaries and runnable checks",
    },
    {
        "readiness_id": "RQMR005",
        "readiness_name": "Validation readiness",
        "evidence_file": "Makefile",
        "readiness_action": "run make reviewer_question_maintainer_release_readiness_digest before public issue closure",
    },
]


def main() -> int:
    closeout = json.loads(CLOSEOUT.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = [
        {
            **row,
            "readiness_status": "included_in_public_maintainer_release_readiness_digest",
            "readiness_state": "current_preview_ready",
            "boundary": "synthetic only and not for clinical use",
        }
        for row in READINESS_ROWS
    ]

    data: dict[str, Any] = {
        "version": "reviewer_question_maintainer_release_readiness_digest_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_maintainer_closeout_digest_v0_1.json",
        "readiness_row_count": len(rows),
        "closeout_rows_represented": closeout["closeout_row_count"],
        "handoff_rows_represented": closeout["handoff_rows_represented"],
        "contributor_digest_rows_represented": closeout["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": closeout["release_index_surface_rows_represented"],
        "issue_history_rows_represented": closeout["issue_history_rows_represented"],
        "previous_public_issue_number": 57,
        "readiness_decision": "ready_for_public_preview",
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
        "# Reviewer question maintainer release readiness digest v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This digest gives maintainers a compact public preview readiness trail after reviewer question closeout review.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Readiness rows: {len(rows)}",
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
        "Readiness decision: `ready_for_public_preview`",
        "",
        "## Maintainer readiness rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['readiness_id']}",
                "",
                f"Readiness name: {row['readiness_name']}",
                "",
                f"Evidence file: `{row['evidence_file']}`",
                "",
                f"Readiness action: {row['readiness_action']}",
                "",
                f"Readiness status: `{row['readiness_status']}`",
                "",
                f"Readiness state: `{row['readiness_state']}`",
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
            "make reviewer_question_maintainer_release_readiness_digest",
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
    print(f"readiness_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
