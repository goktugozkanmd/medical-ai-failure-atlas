#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "label_audit" / "label_audit_release_note_packet_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_public_changelog_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_PUBLIC_CHANGELOG_V0_1.md"

CHANGE_ROWS = [
    {
        "change_id": "LAC001",
        "date": "2026 06 16",
        "surface_name": "Public contributor route",
        "public_file": "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
        "public_value": "opened a synthetic label audit issue route",
    },
    {
        "change_id": "LAC002",
        "date": "2026 06 16",
        "surface_name": "Example intake rows",
        "public_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "public_value": "added synthetic examples for provenance and label review",
    },
    {
        "change_id": "LAC003",
        "date": "2026 06 17",
        "surface_name": "Example dashboard",
        "public_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md",
        "public_value": "summarized intake rows by role and blocked claim type",
    },
    {
        "change_id": "LAC004",
        "date": "2026 06 17",
        "surface_name": "Maintainer triage board",
        "public_file": "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md",
        "public_value": "mapped each dashboard row to a maintainer action",
    },
    {
        "change_id": "LAC005",
        "date": "2026 06 17",
        "surface_name": "Public wording decision log",
        "public_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "public_value": "recorded blocked wording and safer public wording",
    },
    {
        "change_id": "LAC006",
        "date": "2026 06 17",
        "surface_name": "Release gate checklist",
        "public_file": "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md",
        "public_value": "converted wording decisions into release checks",
    },
    {
        "change_id": "LAC007",
        "date": "2026 06 17",
        "surface_name": "Release gate outcome dashboard",
        "public_file": "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
        "public_value": "summarized current pass and block outcomes",
    },
    {
        "change_id": "LAC008",
        "date": "2026 06 17",
        "surface_name": "Release note packet",
        "public_file": "docs/label_audit/LABEL_AUDIT_RELEASE_NOTE_PACKET_V0_1.md",
        "public_value": "packaged the label audit route into one public release note surface",
    },
]


def main() -> None:
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for row in CHANGE_ROWS:
        rows.append(
            {
                **row,
                "change_status": "public_preview_added",
                "boundary": "synthetic only and not for clinical use",
                "next_action": "keep linked surface current during public preview",
            }
        )

    data: dict[str, Any] = {
        "version": "label_audit_public_changelog_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_release_note_packet_v0_1.json",
        "change_row_count": len(rows),
        "release_note_packet_rows_represented": packet["packet_surface_count"],
        "latest_change_id": rows[-1]["change_id"],
        "changelog_decision": "ready_for_public_preview",
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
        "# Label audit public changelog v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This changelog gives a chronological public maintainer record for the label audit contributor route, intake rows, dashboard, triage board, wording log, release gate checklist, outcome dashboard, and release note packet.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Change rows: {len(rows)}",
        "",
        f"Release note packet rows represented: {data['release_note_packet_rows_represented']}",
        "",
        f"Latest change id: `{data['latest_change_id']}`",
        "",
        "Changelog decision: `ready_for_public_preview`",
        "",
        "## Change rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['change_id']}",
                "",
                f"Date: {row['date']}",
                "",
                f"Surface name: {row['surface_name']}",
                "",
                f"Public file: `{row['public_file']}`",
                "",
                f"Public value: {row['public_value']}",
                "",
                f"Change status: `{row['change_status']}`",
                "",
                f"Boundary: {row['boundary']}",
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
            "make label_audit_changelog",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"change_rows={len(rows)}")


if __name__ == "__main__":
    main()
