#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "docs" / "label_audit" / "label_audit_example_dashboard_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_maintainer_triage_board_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md"

MAINTAINER_ACTIONS = {
    "LAE001": "rewrite provenance wording",
    "LAE002": "route to clinician wording review",
    "LAE003": "add pilot subset limitation note",
    "LAE004": "keep raw outputs withheld",
    "LAE005": "block dataset quality proof wording",
}

PUBLIC_WORDING_DECISIONS = {
    "LAE001": "say synthetic example only",
    "LAE002": "say pending clinician review",
    "LAE003": "say protocol testing only",
    "LAE004": "say raw outputs are withheld",
    "LAE005": "say dataset quality is not proven",
}

NEXT_PUBLIC_SURFACES = {
    "LAE001": "Health data quality card",
    "LAE002": "Label definition lock",
    "LAE003": "Platform dashboard",
    "LAE004": "Public release boundary",
    "LAE005": "Release note",
}


def main() -> None:
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for item in dashboard["rows"]:
        example_id = str(item["example_id"])
        rows.append(
            {
                "example_id": example_id,
                "title": item["title"],
                "owner_role_id": item["role_id"],
                "owner_role_name": item["role_name"],
                "audit_id": item["audit_id"],
                "review_state": item["review_state"],
                "blocked_public_claim_type": item["blocked_public_claim_type"],
                "maintainer_action": MAINTAINER_ACTIONS[example_id],
                "triage_status": "ready_for_maintainer_review",
                "public_wording_decision": PUBLIC_WORDING_DECISIONS[example_id],
                "next_public_surface": NEXT_PUBLIC_SURFACES[example_id],
            }
        )

    data: dict[str, Any] = {
        "version": "label_audit_maintainer_triage_board_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_example_dashboard_v0_1.json",
        "triage_row_count": len(rows),
        "owner_role_count": len(set(row["owner_role_id"] for row in rows)),
        "maintainer_action_count": len(set(row["maintainer_action"] for row in rows)),
        "public_wording_decision_count": len(set(row["public_wording_decision"] for row in rows)),
        "triage_status_count": len(set(row["triage_status"] for row in rows)),
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
        "owner_role_counts": dict(sorted(Counter(row["owner_role_id"] for row in rows).items())),
        "triage_status_counts": dict(sorted(Counter(row["triage_status"] for row in rows).items())),
        "rows": rows,
    }
    JSON_OUTPUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Label audit maintainer triage board v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This board turns the synthetic label audit dashboard rows into maintainer actions, owner roles, triage status values, and next public wording decisions.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Maintainer triage rows: {len(rows)}",
        "",
        f"Owner roles represented: {data['owner_role_count']}",
        "",
        f"Maintainer actions represented: {data['maintainer_action_count']}",
        "",
        f"Public wording decisions represented: {data['public_wording_decision_count']}",
        "",
        f"Triage status values represented: {data['triage_status_count']}",
        "",
        "## Owner role summary",
        "",
    ]
    for role_id, count in data["owner_role_counts"].items():
        role_name = next(row["owner_role_name"] for row in rows if row["owner_role_id"] == role_id)
        lines.extend([f"1. `{role_id}` {role_name}: {count}", ""])

    lines.extend(["## Triage status summary", ""])
    for status, count in data["triage_status_counts"].items():
        lines.extend([f"1. `{status}`: {count}", ""])

    lines.extend(["## Triage rows", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['example_id']}: {row['title']}",
                "",
                f"Owner role: `{row['owner_role_id']}` {row['owner_role_name']}",
                "",
                f"Audit row: `{row['audit_id']}`",
                "",
                f"Review state: `{row['review_state']}`",
                "",
                f"Blocked public claim type: {row['blocked_public_claim_type']}",
                "",
                f"Maintainer action: {row['maintainer_action']}",
                "",
                f"Triage status: `{row['triage_status']}`",
                "",
                f"Public wording decision: {row['public_wording_decision']}",
                "",
                f"Next public surface: {row['next_public_surface']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Public files",
            "",
            "1. Triage board JSON: `docs/label_audit/label_audit_maintainer_triage_board_v0_1.json`",
            "2. Example dashboard: `docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md`",
            "3. Example intake rows: `docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md`",
            "4. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`",
            "5. Reviewer role table: `docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md`",
            "",
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make label_audit_triage",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"triage_rows={len(rows)}")


if __name__ == "__main__":
    main()
