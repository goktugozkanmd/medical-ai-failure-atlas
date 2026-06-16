#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_OUTPUT = ROOT / "docs" / "label_audit_reviewer_role_table_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md"


DATA: dict[str, Any] = {
    "version": "label_audit_reviewer_role_table_v0_1",
    "status": "public_preview",
    "date": "2026 06 16",
    "role_count": 4,
    "audit_row_count": 5,
    "contains_patient_data": False,
    "synthetic_examples_only": True,
    "not_for_clinical_use": True,
    "no_clinical_deployment_claim": True,
    "no_clinical_validation_claim": True,
    "no_model_safety_claim": True,
    "no_model_ranking": True,
    "no_dataset_quality_proof": True,
    "no_official_endorsement_claim": True,
    "linked_public_files": [
        "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
        "DATASET_EVALUATION_CARD_V0_1_DRAFT.md",
        "DATA_DICTIONARY.md",
        "LABELING.md",
        "docs/LABEL_DEFINITION_LOCK_V0_1.md",
        "docs/LABELING_PACKAGE_INDEX_V0_1.md",
        "data/inter_rater_review_subset_v0_1.tsv",
        "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "docs/label_audit/label_audit_example_intake_v0_1.json",
    ],
    "linked_counts": {
        "synthetic_scenario_rows": 150,
        "prompt_rows": 70,
        "pilot_inter_rater_rows": 24,
        "turkish_synthetic_risk_rows": 14,
        "source_claim_review_queue_rows": 12,
    },
    "linked_review_states": [
        "synthetic_preview_only",
        "needs_clinician_review",
        "needs_adjudication",
        "not_for_public_summary",
    ],
    "roles": [
        {
            "role_id": "LAR001",
            "role_name": "Synthetic provenance reviewer",
            "purpose": "Confirm that every public dataset surface stays synthetic and excludes patient data.",
            "required_fields": [
                "dataset surface",
                "provenance statement",
                "patient data absent",
                "direct identifier absent",
                "real record absent",
                "raw output absent",
                "public boundary state",
            ],
            "escalation_triggers": [
                "Patient data status is unclear",
                "Synthetic provenance is missing",
                "Identifier review is incomplete",
                "Real record language appears",
            ],
            "release_gate_decision": "synthetic_preview_only",
            "review_lanes": ["provenance_review", "privacy_boundary_review"],
        },
        {
            "role_id": "LAR002",
            "role_name": "Label definition reviewer",
            "purpose": "Check that labels match the locked rubric version and do not claim clinical validation.",
            "required_fields": [
                "label version",
                "label lock file",
                "rubric file",
                "binary gate mapping",
                "final label mapping",
                "unsure rule state",
                "review status wording",
            ],
            "escalation_triggers": [
                "Label version is missing",
                "Label lock is edited silently",
                "Clinical validation wording appears",
                "Unsure rule is bypassed",
            ],
            "release_gate_decision": "needs_clinician_review",
            "review_lanes": ["label_definition_review", "clinician_review"],
        },
        {
            "role_id": "LAR003",
            "role_name": "Pilot subset reviewer",
            "purpose": "Keep the pilot inter rater subset framed as protocol testing rather than an agreement study.",
            "required_fields": [
                "subset row count",
                "sampling reason",
                "agreement statistic state",
                "reviewer bias reduction note",
                "model identity limitation",
                "pilot status wording",
                "next review need",
            ],
            "escalation_triggers": [
                "Pilot subset is described as powered",
                "Agreement statistic is implied",
                "Model identity is overclaimed",
                "Population prevalence is implied",
            ],
            "release_gate_decision": "needs_adjudication",
            "review_lanes": ["inter_rater_review", "label_quality_review"],
        },
        {
            "role_id": "LAR004",
            "role_name": "Public release boundary reviewer",
            "purpose": "Check that release language blocks raw output release, deployment claims, and dataset quality proof language.",
            "required_fields": [
                "allowed public use",
                "not allowed public use",
                "raw output boundary",
                "dataset quality proof boundary",
                "clinical deployment boundary",
                "model ranking boundary",
                "official endorsement boundary",
            ],
            "escalation_triggers": [
                "Raw model output release is implied",
                "Dataset quality proof is implied",
                "Clinical deployment readiness is implied",
                "Formal approval wording appears",
            ],
            "release_gate_decision": "not_for_public_summary",
            "review_lanes": ["public_release_boundary_review", "data_quality_review"],
        },
    ],
    "audit_rows": [
        {
            "audit_id": "LAA001",
            "title": "Synthetic provenance audit",
            "linked_ids": ["LAR001", "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md"],
            "required_role_ids": ["LAR001"],
            "review_state": "synthetic_preview_only",
            "required_outcome": "Keep synthetic provenance and patient data absence visible.",
        },
        {
            "audit_id": "LAA002",
            "title": "Label definition lock audit",
            "linked_ids": ["LAR002", "docs/LABEL_DEFINITION_LOCK_V0_1.md", "data/scoring_rubric_v0_1.json"],
            "required_role_ids": ["LAR002"],
            "review_state": "needs_clinician_review",
            "required_outcome": "Block silent label definition drift and clinical validation wording.",
        },
        {
            "audit_id": "LAA003",
            "title": "Pilot inter rater subset audit",
            "linked_ids": ["LAR003", "data/inter_rater_review_subset_v0_1.tsv"],
            "required_role_ids": ["LAR003"],
            "review_state": "needs_adjudication",
            "required_outcome": "Keep the 24 row subset framed as protocol testing only.",
        },
        {
            "audit_id": "LAA004",
            "title": "Raw output exclusion audit",
            "linked_ids": ["LAR004", "PUBLIC_RELEASE_BOUNDARY_V0_1.md"],
            "required_role_ids": ["LAR004"],
            "review_state": "not_for_public_summary",
            "required_outcome": "Keep raw model outputs excluded unless redistribution is cleared.",
        },
        {
            "audit_id": "LAA005",
            "title": "Public release boundary audit",
            "linked_ids": ["LAR001", "LAR002", "LAR003", "LAR004"],
            "required_role_ids": ["LAR004"],
            "review_state": "not_for_public_summary",
            "required_outcome": "Block dataset quality proof, clinical deployment, model ranking, and formal approval language.",
        },
    ],
}


def joined(values: list[str]) -> str:
    return ", ".join(values)


def numbered(values: list[str]) -> list[str]:
    lines: list[str] = []
    for index, value in enumerate(values, start=1):
        lines.extend([f"{index}. {value}", ""])
    return lines


def main() -> None:
    JSON_OUTPUT.write_text(json.dumps(DATA, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    roles: list[dict[str, Any]] = DATA["roles"]
    audit_rows: list[dict[str, Any]] = DATA["audit_rows"]
    counts: dict[str, int] = DATA["linked_counts"]

    lines: list[str] = [
        "# Label audit reviewer role table v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 16",
        "",
        "This table turns health data quality and label audit review into explicit reviewer roles and escalation gate audit rows.",
        "",
        "It uses synthetic examples only. It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Label audit reviewer roles: {len(roles)}",
        "",
        f"Label audit escalation gate rows: {len(audit_rows)}",
        "",
        f"Synthetic scenario rows: {counts['synthetic_scenario_rows']}",
        "",
        f"Prompt rows: {counts['prompt_rows']}",
        "",
        f"Pilot inter rater rows: {counts['pilot_inter_rater_rows']}",
        "",
        f"Turkish synthetic risk rows: {counts['turkish_synthetic_risk_rows']}",
        "",
        f"Source claim review queue rows: {counts['source_claim_review_queue_rows']}",
        "",
        "## Reviewer roles",
        "",
    ]

    for role in roles:
        lines.extend(
            [
                f"### {role['role_id']}: {role['role_name']}",
                "",
                f"Purpose: {role['purpose']}",
                "",
                f"Release gate decision: `{role['release_gate_decision']}`",
                "",
                f"Review lanes: {joined(role['review_lanes'])}",
                "",
                "Required fields:",
                "",
            ]
        )
        lines.extend(numbered(role["required_fields"]))
        lines.extend(["Escalation triggers:", ""])
        lines.extend(numbered(role["escalation_triggers"]))

    lines.extend(["## Escalation gate audit rows", ""])
    for row in audit_rows:
        lines.extend(
            [
                f"### {row['audit_id']}: {row['title']}",
                "",
                f"Linked IDs: {joined(row['linked_ids'])}",
                "",
                f"Required roles: {joined(row['required_role_ids'])}",
                "",
                f"Review state: `{row['review_state']}`",
                "",
                f"Required outcome: {row['required_outcome']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. Every role uses synthetic examples only.",
            "2. Patient data is not used.",
            "3. Reviewer roles do not prove dataset quality.",
            "4. Label audit rows do not create clinical validation.",
            "5. Public release boundaries block raw model outputs unless redistribution is cleared.",
            "6. Passing this table is not clinical validation, model safety, dataset quality proof, model ranking, or deployment readiness.",
            "",
            "## Public files",
            "",
            "1. JSON source: `docs/label_audit_reviewer_role_table_v0_1.json`",
            "2. Generated role table: `docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md`",
            "3. Validator: `scripts/validate_label_audit_reviewer_role_table_v0_1.py`",
            "4. Runnable target: `make label_audit_role_table`",
            "5. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`",
            "6. Clinician review protocol: `docs/CLINICIAN_REVIEW_PROTOCOL_V0_1.md`",
            "7. Label audit example intake rows: `docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md`",
            "8. Label audit example intake JSON: `docs/label_audit/label_audit_example_intake_v0_1.json`",
            "",
        ]
    )

    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"roles={len(roles)}")
    print(f"audit_rows={len(audit_rows)}")


if __name__ == "__main__":
    main()
