#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORDING = ROOT / "docs" / "label_audit" / "label_audit_public_wording_decision_log_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_release_gate_checklist_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md"

GATE_DETAILS = {
    "LAE001": {
        "release_gate_id": "LARG001",
        "gate_name": "Synthetic provenance gate",
        "gate_question": "Does public wording clearly say the row is synthetic only",
        "required_check": "synthetic provenance is explicit",
        "pass_state": "public wording may proceed",
        "block_state": "block wording that suggests real care records",
    },
    "LAE002": {
        "release_gate_id": "LARG002",
        "gate_name": "Label definition review gate",
        "gate_question": "Does public wording avoid clinical validation language",
        "required_check": "clinician review status is pending",
        "pass_state": "public wording may proceed",
        "block_state": "block wording that suggests clinically validated labels",
    },
    "LAE003": {
        "release_gate_id": "LARG003",
        "gate_name": "Pilot subset scope gate",
        "gate_question": "Does public wording say the row is for protocol testing only",
        "required_check": "pilot subset limitation is explicit",
        "pass_state": "public wording may proceed",
        "block_state": "block wording that suggests deployment performance",
    },
    "LAE004": {
        "release_gate_id": "LARG004",
        "gate_name": "Raw output release gate",
        "gate_question": "Does public wording state that raw outputs are withheld",
        "required_check": "raw output exclusion is explicit",
        "pass_state": "public wording may proceed",
        "block_state": "block wording that suggests raw outputs are public",
    },
    "LAE005": {
        "release_gate_id": "LARG005",
        "gate_name": "Dataset quality proof gate",
        "gate_question": "Does public wording deny dataset quality proof",
        "required_check": "dataset quality proof is not claimed",
        "pass_state": "public wording may proceed",
        "block_state": "block wording that suggests dataset quality proof",
    },
}


def main() -> None:
    wording = json.loads(WORDING.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for item in wording["rows"]:
        example_id = str(item["example_id"])
        gate = GATE_DETAILS[example_id]
        rows.append(
            {
                **gate,
                "example_id": example_id,
                "reviewer_role_id": item["reviewer_role_id"],
                "reviewer_role_name": item["reviewer_role_name"],
                "blocked_wording": item["blocked_wording"],
                "required_public_wording": item["proposed_public_wording"],
                "current_state": "pass",
                "release_decision": "allowed_for_public_preview",
                "evidence_surface": item["next_public_surface"],
            }
        )

    data: dict[str, Any] = {
        "version": "label_audit_release_gate_checklist_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_public_wording_decision_log_v0_1.json",
        "release_gate_count": len(rows),
        "pass_state_count": sum(1 for row in rows if row["current_state"] == "pass"),
        "block_state_count": sum(1 for row in rows if row["current_state"] == "block"),
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
        "# Label audit release gate checklist v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This checklist converts label audit wording decisions into release gate checks with required pass or block states.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Release gate rows: {len(rows)}",
        "",
        f"Pass state rows: {data['pass_state_count']}",
        "",
        f"Block state rows: {data['block_state_count']}",
        "",
        "Release decision: `allowed_for_public_preview`",
        "",
        "## Gate rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['release_gate_id']}",
                "",
                f"Gate name: {row['gate_name']}",
                "",
                f"Example id: `{row['example_id']}`",
                "",
                f"Reviewer role: `{row['reviewer_role_id']}` {row['reviewer_role_name']}",
                "",
                f"Gate question: {row['gate_question']}",
                "",
                f"Required check: {row['required_check']}",
                "",
                f"Blocked wording: {row['blocked_wording']}",
                "",
                f"Required public wording: {row['required_public_wording']}",
                "",
                f"Current state: `{row['current_state']}`",
                "",
                f"Pass state: {row['pass_state']}",
                "",
                f"Block state: {row['block_state']}",
                "",
                f"Evidence surface: {row['evidence_surface']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Public files",
            "",
            "1. Checklist JSON: `docs/label_audit/label_audit_release_gate_checklist_v0_1.json`",
            "2. Public wording decision log: `docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md`",
            "3. Maintainer triage board: `docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md`",
            "4. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`",
            "",
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make label_audit_release_gates",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"release_gate_rows={len(rows)}")


if __name__ == "__main__":
    main()
