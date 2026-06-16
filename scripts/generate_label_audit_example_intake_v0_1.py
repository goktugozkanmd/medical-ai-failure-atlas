#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_example_intake_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md"


DATA: dict[str, Any] = {
    "version": "label_audit_example_intake_v0_1",
    "status": "public_preview",
    "date": "2026 06 17",
    "example_count": 5,
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
    "linked_role_ids": ["LAR001", "LAR002", "LAR003", "LAR004"],
    "linked_audit_ids": ["LAA001", "LAA002", "LAA003", "LAA004", "LAA005"],
    "linked_issue_template": ".github/ISSUE_TEMPLATE/label_audit_review.yml",
    "linked_public_guide": "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
    "linked_role_table": "docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md",
    "linked_health_data_card": "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
    "linked_counts": {
        "synthetic_scenario_rows": 150,
        "prompt_rows": 70,
        "pilot_inter_rater_rows": 24,
        "turkish_synthetic_risk_rows": 14,
        "source_claim_review_queue_rows": 12,
    },
    "examples": [
        {
            "example_id": "LAE001",
            "title": "Synthetic provenance overclaim",
            "audit_surface": "synthetic provenance",
            "suggested_role_id": "LAR001",
            "linked_audit_id": "LAA001",
            "exact_boundary_to_review": "Public text implies real care record coverage or unclear provenance.",
            "required_checks": [
                "synthetic_provenance",
                "patient_data_absence",
                "direct_identifier_absence",
                "public_boundary_state",
            ],
            "proposed_public_action": "rewrite_public_wording",
            "review_state": "synthetic_preview_only",
        },
        {
            "example_id": "LAE002",
            "title": "Label definition drift",
            "audit_surface": "label definition lock",
            "suggested_role_id": "LAR002",
            "linked_audit_id": "LAA002",
            "exact_boundary_to_review": "A label explanation no longer matches the locked rubric version.",
            "required_checks": [
                "label_lock_match",
                "rubric_version_match",
                "unsure_rule_state",
                "clinical_validation_boundary",
            ],
            "proposed_public_action": "route_to_clinician_review",
            "review_state": "needs_clinician_review",
        },
        {
            "example_id": "LAE003",
            "title": "Pilot subset overinterpretation",
            "audit_surface": "pilot inter rater subset",
            "suggested_role_id": "LAR003",
            "linked_audit_id": "LAA003",
            "exact_boundary_to_review": "A 24 row pilot subset is framed as if it measured population performance.",
            "required_checks": [
                "pilot_subset_framing",
                "no_agreement_statistic",
                "sampling_reason",
                "no_population_prevalence",
            ],
            "proposed_public_action": "add_protocol_testing_wording",
            "review_state": "needs_adjudication",
        },
        {
            "example_id": "LAE004",
            "title": "Raw output exclusion boundary",
            "audit_surface": "raw output exclusion",
            "suggested_role_id": "LAR004",
            "linked_audit_id": "LAA004",
            "exact_boundary_to_review": "A public summary could be read as releasing raw model outputs.",
            "required_checks": [
                "raw_output_exclusion",
                "redistribution_terms_state",
                "private_output_absence",
                "public_release_boundary",
            ],
            "proposed_public_action": "keep_raw_outputs_withheld",
            "review_state": "not_for_public_summary",
        },
        {
            "example_id": "LAE005",
            "title": "Dataset quality proof boundary",
            "audit_surface": "public release boundary",
            "suggested_role_id": "LAR004",
            "linked_audit_id": "LAA005",
            "exact_boundary_to_review": "A public card sounds as if it proves dataset quality or readiness.",
            "required_checks": [
                "dataset_quality_proof_boundary",
                "clinical_deployment_boundary",
                "model_ranking_boundary",
                "formal_approval_boundary",
            ],
            "proposed_public_action": "block_stronger_public_claim",
            "review_state": "not_for_public_summary",
        },
    ],
}


def numbered(values: list[str]) -> list[str]:
    lines: list[str] = []
    for index, value in enumerate(values, start=1):
        lines.extend([f"{index}. `{value}`", ""])
    return lines


def main() -> None:
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text(json.dumps(DATA, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    counts: dict[str, int] = DATA["linked_counts"]
    examples: list[dict[str, Any]] = DATA["examples"]
    lines: list[str] = [
        "# Label audit example intake v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This file gives synthetic label audit example intake rows for public maintainer review.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Label audit examples: {len(examples)}",
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
        "## Public links",
        "",
        "1. Public issue template: `.github/ISSUE_TEMPLATE/label_audit_review.yml`",
        "2. Public contributor guide: `docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md`",
        "3. Reviewer role table: `docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md`",
        "4. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`",
        "5. JSON source: `docs/label_audit/label_audit_example_intake_v0_1.json`",
        "",
        "## Example rows",
        "",
    ]

    for row in examples:
        lines.extend(
            [
                f"### {row['example_id']}: {row['title']}",
                "",
                f"Audit surface: {row['audit_surface']}",
                "",
                f"Suggested reviewer role: `{row['suggested_role_id']}`",
                "",
                f"Linked audit row: `{row['linked_audit_id']}`",
                "",
                f"Exact boundary to review: {row['exact_boundary_to_review']}",
                "",
                f"Review state: `{row['review_state']}`",
                "",
                f"Proposed public action: `{row['proposed_public_action']}`",
                "",
                "Required checks:",
                "",
            ]
        )
        lines.extend(numbered(row["required_checks"]))

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. The examples are synthetic only.",
            "2. Patient data is not used.",
            "3. Raw model outputs are not released.",
            "4. The examples do not prove dataset quality.",
            "5. The examples do not create clinical validation.",
            "6. The examples do not support clinical deployment.",
            "7. The examples do not rank models.",
            "8. The examples do not claim regulatory approval.",
            "9. The examples do not claim official endorsement.",
            "",
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make label_audit_examples",
            "```",
            "",
        ]
    )

    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"examples={len(examples)}")


if __name__ == "__main__":
    main()
