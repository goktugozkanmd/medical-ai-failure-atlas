#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRIAGE = ROOT / "docs" / "label_audit" / "label_audit_maintainer_triage_board_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_public_wording_decision_log_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md"

BLOCKED_WORDING = {
    "LAE001": "covers real care records",
    "LAE002": "clinically validated labels",
    "LAE003": "representative of deployment performance",
    "LAE004": "raw outputs are available in public",
    "LAE005": "proves dataset quality",
}

PROPOSED_WORDING = {
    "LAE001": "synthetic example only",
    "LAE002": "pending clinician review",
    "LAE003": "protocol testing only",
    "LAE004": "raw outputs are withheld",
    "LAE005": "dataset quality is not proven",
}


def main() -> None:
    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for item in triage["rows"]:
        example_id = str(item["example_id"])
        rows.append(
            {
                "example_id": example_id,
                "reviewer_role_id": item["owner_role_id"],
                "reviewer_role_name": item["owner_role_name"],
                "blocked_wording": BLOCKED_WORDING[example_id],
                "proposed_public_wording": PROPOSED_WORDING[example_id],
                "decision_status": "safe_public_wording_ready",
                "maintainer_action": item["maintainer_action"],
                "next_public_surface": item["next_public_surface"],
            }
        )

    data: dict[str, Any] = {
        "version": "label_audit_public_wording_decision_log_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_maintainer_triage_board_v0_1.json",
        "decision_row_count": len(rows),
        "blocked_wording_count": len(set(row["blocked_wording"] for row in rows)),
        "proposed_public_wording_count": len(set(row["proposed_public_wording"] for row in rows)),
        "decision_status_count": len(set(row["decision_status"] for row in rows)),
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
        "# Label audit public wording decision log v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This log records blocked wording, proposed public wording, reviewer role, decision status, maintainer action, and next public surface for each synthetic label audit triage row.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Public wording decision rows: {len(rows)}",
        "",
        f"Blocked wording examples: {data['blocked_wording_count']}",
        "",
        f"Proposed public wording examples: {data['proposed_public_wording_count']}",
        "",
        f"Decision status values represented: {data['decision_status_count']}",
        "",
        "Decision status: `safe_public_wording_ready`",
        "",
        "## Decision rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['example_id']}",
                "",
                f"Reviewer role: `{row['reviewer_role_id']}` {row['reviewer_role_name']}",
                "",
                f"Blocked wording: {row['blocked_wording']}",
                "",
                f"Proposed public wording: {row['proposed_public_wording']}",
                "",
                f"Decision status: `{row['decision_status']}`",
                "",
                f"Maintainer action: {row['maintainer_action']}",
                "",
                f"Next public surface: {row['next_public_surface']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Public files",
            "",
            "1. Decision log JSON: `docs/label_audit/label_audit_public_wording_decision_log_v0_1.json`",
            "2. Maintainer triage board: `docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md`",
            "3. Example dashboard: `docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md`",
            "4. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`",
            "",
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make label_audit_wording_log",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"decision_rows={len(rows)}")


if __name__ == "__main__":
    main()
