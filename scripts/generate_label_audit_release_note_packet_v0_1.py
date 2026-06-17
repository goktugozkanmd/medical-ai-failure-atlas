#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTCOME = ROOT / "docs" / "label_audit" / "label_audit_release_gate_outcome_dashboard_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_release_note_packet_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_RELEASE_NOTE_PACKET_V0_1.md"

PACKET_SURFACES = [
    {
        "surface_id": "LARP001",
        "surface_name": "Public contributor route",
        "public_file": "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
        "role": "opens synthetic label audit review route",
    },
    {
        "surface_id": "LARP002",
        "surface_name": "Example intake rows",
        "public_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "role": "collects synthetic provenance and label review examples",
    },
    {
        "surface_id": "LARP003",
        "surface_name": "Example dashboard",
        "public_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md",
        "role": "summarizes role, audit row, review state, and blocked claim type",
    },
    {
        "surface_id": "LARP004",
        "surface_name": "Maintainer triage board",
        "public_file": "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md",
        "role": "assigns maintainer action and next public wording decision",
    },
    {
        "surface_id": "LARP005",
        "surface_name": "Public wording decision log",
        "public_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "role": "records blocked wording and required public wording",
    },
    {
        "surface_id": "LARP006",
        "surface_name": "Release gate checklist",
        "public_file": "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md",
        "role": "turns wording decisions into pass or block checks",
    },
    {
        "surface_id": "LARP007",
        "surface_name": "Release gate outcome dashboard",
        "public_file": "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
        "role": "summarizes current pass and block outcomes",
    },
]


def main() -> None:
    outcome = json.loads(OUTCOME.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for item in PACKET_SURFACES:
        rows.append(
            {
                **item,
                "packet_status": "included_in_public_preview",
                "next_action": "keep linked public surface current",
            }
        )

    data: dict[str, Any] = {
        "version": "label_audit_release_note_packet_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_release_gate_outcome_dashboard_v0_1.json",
        "packet_surface_count": len(rows),
        "outcome_row_count": outcome["outcome_row_count"],
        "pass_state_count": outcome["pass_state_count"],
        "block_state_count": outcome["block_state_count"],
        "packet_decision": "ready_for_public_preview",
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
        "# Label audit release note packet v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This packet gives one public release note surface for the label audit contributor route, intake rows, dashboard, triage board, wording log, release gate checklist, and outcome dashboard.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Packet surface rows: {len(rows)}",
        "",
        f"Outcome rows represented: {data['outcome_row_count']}",
        "",
        f"Pass state rows represented: {data['pass_state_count']}",
        "",
        f"Block state rows represented: {data['block_state_count']}",
        "",
        "Packet decision: `ready_for_public_preview`",
        "",
        "## Packet rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['surface_id']}",
                "",
                f"Surface name: {row['surface_name']}",
                "",
                f"Public file: `{row['public_file']}`",
                "",
                f"Role: {row['role']}",
                "",
                f"Packet status: `{row['packet_status']}`",
                "",
                f"Next action: {row['next_action']}",
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
            "make label_audit_release_packet",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"packet_surface_rows={len(rows)}")


if __name__ == "__main__":
    main()
