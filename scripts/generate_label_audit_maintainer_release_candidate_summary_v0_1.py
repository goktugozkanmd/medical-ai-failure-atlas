#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRAIL = ROOT / "docs" / "label_audit" / "label_audit_maintainer_audit_trail_packet_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_maintainer_release_candidate_summary_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_MAINTAINER_RELEASE_CANDIDATE_SUMMARY_V0_1.md"

SUMMARY_ROWS = [
    {
        "summary_id": "LAMC001",
        "summary_name": "Synthetic boundary candidate",
        "source_trail_id": "LAMT001",
        "candidate_surface": "docs/label_audit/LABEL_AUDIT_MAINTAINER_AUDIT_TRAIL_PACKET_V0_1.md",
        "maintainer_decision": "candidate remains synthetic only",
    },
    {
        "summary_id": "LAMC002",
        "summary_name": "Intake pattern candidate",
        "source_trail_id": "LAMT002",
        "candidate_surface": "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "maintainer_decision": "candidate keeps intake patterns inspectable",
    },
    {
        "summary_id": "LAMC003",
        "summary_name": "Public wording candidate",
        "source_trail_id": "LAMT003",
        "candidate_surface": "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "maintainer_decision": "candidate keeps blocked claims out of public wording",
    },
    {
        "summary_id": "LAMC004",
        "summary_name": "Release surface candidate",
        "source_trail_id": "LAMT004",
        "candidate_surface": "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
        "maintainer_decision": "candidate surfaces remain linked from public release notes",
    },
    {
        "summary_id": "LAMC005",
        "summary_name": "Validation candidate",
        "source_trail_id": "LAMT005",
        "candidate_surface": "Makefile",
        "maintainer_decision": "candidate keeps runnable validation before issue closeout",
    },
]


def main() -> None:
    trail = json.loads(TRAIL.read_text(encoding="utf-8"))
    trail_ids = {row["trail_id"] for row in trail["rows"]}
    rows: list[dict[str, Any]] = []
    for row in SUMMARY_ROWS:
        if row["source_trail_id"] not in trail_ids:
            raise ValueError(f"missing source trail id: {row['source_trail_id']}")
        rows.append(
            {
                **row,
                "candidate_status": "public_preview_release_candidate_summary",
                "candidate_state": "current_preview_candidate",
                "boundary": "synthetic only and not for clinical use",
            }
        )

    data: dict[str, Any] = {
        "version": "label_audit_maintainer_release_candidate_summary_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_maintainer_audit_trail_packet_v0_1.json",
        "candidate_summary_row_count": len(rows),
        "audit_trail_rows_represented": trail["audit_trail_row_count"],
        "evidence_rows_represented": trail["evidence_rows_represented"],
        "readiness_rows_represented": trail["readiness_rows_represented"],
        "closeout_rows_represented": trail["closeout_rows_represented"],
        "handoff_rows_represented": trail["handoff_rows_represented"],
        "contributor_digest_rows_represented": trail["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": trail["release_index_surface_rows_represented"],
        "previous_public_issue_number": 35,
        "release_candidate_decision": "public_preview_candidate_only",
        "maintainer_review_scope": "current public preview route only",
        "contains_patient_data": False,
        "synthetic_examples_only": True,
        "not_for_clinical_use": True,
        "no_raw_model_output_release": True,
        "no_clinical_deployment_claim": True,
        "no_clinical_validation_claim": True,
        "no_model_safety_claim": True,
        "no_model_ranking": True,
        "no_dataset_quality_proof": True,
        "no_official_endorsement_claim": True,
        "rows": rows,
    }
    JSON_OUTPUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Label audit maintainer release candidate summary v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This release candidate summary gives maintainers a compact public preview candidate view after audit trail packet review.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Candidate summary rows: {len(rows)}",
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
        f"Previous public issue represented: {data['previous_public_issue_number']}",
        "",
        "Maintainer review scope: current public preview route only",
        "",
        "Release candidate decision: `public_preview_candidate_only`",
        "",
        "## Maintainer candidate rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['summary_id']}",
                "",
                f"Summary name: {row['summary_name']}",
                "",
                f"Source trail row: `{row['source_trail_id']}`",
                "",
                f"Candidate surface: `{row['candidate_surface']}`",
                "",
                f"Maintainer decision: {row['maintainer_decision']}",
                "",
                f"Candidate status: `{row['candidate_status']}`",
                "",
                f"Candidate state: `{row['candidate_state']}`",
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
            "make label_audit_maintainer_release_candidate_summary",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"candidate_summary_rows={len(rows)}")


if __name__ == "__main__":
    main()
