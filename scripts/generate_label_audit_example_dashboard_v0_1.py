#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "docs" / "label_audit" / "label_audit_example_intake_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_example_dashboard_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md"

ROLE_NAMES = {
    "LAR001": "Synthetic provenance reviewer",
    "LAR002": "Label definition reviewer",
    "LAR003": "Pilot subset reviewer",
    "LAR004": "Public release boundary reviewer",
}

AUDIT_NAMES = {
    "LAA001": "Synthetic provenance audit",
    "LAA002": "Label definition lock audit",
    "LAA003": "Pilot inter rater subset audit",
    "LAA004": "Raw output exclusion audit",
    "LAA005": "Public release boundary audit",
}

BLOCKED_CLAIMS = {
    "LAE001": "real care record coverage claim",
    "LAE002": "clinical validation claim",
    "LAE003": "population performance claim",
    "LAE004": "raw model output release claim",
    "LAE005": "dataset quality proof claim",
}


def load_intake() -> dict[str, Any]:
    return json.loads(INTAKE.read_text(encoding="utf-8"))


def count_by(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[field]) for row in rows).items()))


def main() -> None:
    intake = load_intake()
    examples: list[dict[str, Any]] = intake["examples"]
    rows: list[dict[str, Any]] = []
    for example in examples:
        example_id = str(example["example_id"])
        role_id = str(example["suggested_role_id"])
        audit_id = str(example["linked_audit_id"])
        rows.append(
            {
                "example_id": example_id,
                "title": example["title"],
                "role_id": role_id,
                "role_name": ROLE_NAMES[role_id],
                "audit_id": audit_id,
                "audit_name": AUDIT_NAMES[audit_id],
                "review_state": example["review_state"],
                "blocked_public_claim_type": BLOCKED_CLAIMS[example_id],
                "required_check_count": len(example["required_checks"]),
            }
        )

    data: dict[str, Any] = {
        "version": "label_audit_example_dashboard_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_example_intake_v0_1.json",
        "example_count": len(rows),
        "role_count": len(count_by(rows, "role_id")),
        "audit_row_count": len(count_by(rows, "audit_id")),
        "review_state_count": len(count_by(rows, "review_state")),
        "blocked_public_claim_type_count": len(count_by(rows, "blocked_public_claim_type")),
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
        "role_counts": count_by(rows, "role_id"),
        "audit_counts": count_by(rows, "audit_id"),
        "review_state_counts": count_by(rows, "review_state"),
        "blocked_public_claim_type_counts": count_by(rows, "blocked_public_claim_type"),
        "rows": rows,
    }
    JSON_OUTPUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Label audit example dashboard v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This dashboard summarizes the public synthetic label audit example intake rows by reviewer role, audit row, review state, and blocked public claim type.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Label audit example dashboard rows: {len(rows)}",
        "",
        f"Reviewer roles represented: {data['role_count']}",
        "",
        f"Audit rows represented: {data['audit_row_count']}",
        "",
        f"Review states represented: {data['review_state_count']}",
        "",
        f"Blocked public claim types represented: {data['blocked_public_claim_type_count']}",
        "",
        "## Role summary",
        "",
    ]

    for role_id, count in data["role_counts"].items():
        lines.extend([f"1. `{role_id}` {ROLE_NAMES[role_id]}: {count}", ""])

    lines.extend(["## Audit row summary", ""])
    for audit_id, count in data["audit_counts"].items():
        lines.extend([f"1. `{audit_id}` {AUDIT_NAMES[audit_id]}: {count}", ""])

    lines.extend(["## Review state summary", ""])
    for state, count in data["review_state_counts"].items():
        lines.extend([f"1. `{state}`: {count}", ""])

    lines.extend(["## Blocked public claim types", ""])
    for claim_type, count in data["blocked_public_claim_type_counts"].items():
        lines.extend([f"1. {claim_type}: {count}", ""])

    lines.extend(["## Dashboard rows", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['example_id']}: {row['title']}",
                "",
                f"Reviewer role: `{row['role_id']}` {row['role_name']}",
                "",
                f"Audit row: `{row['audit_id']}` {row['audit_name']}",
                "",
                f"Review state: `{row['review_state']}`",
                "",
                f"Blocked public claim type: {row['blocked_public_claim_type']}",
                "",
                f"Required check count: {row['required_check_count']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Public files",
            "",
            "1. Intake rows: `docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md`",
            "2. Intake JSON: `docs/label_audit/label_audit_example_intake_v0_1.json`",
            "3. Dashboard JSON: `docs/label_audit/label_audit_example_dashboard_v0_1.json`",
            "4. Reviewer role table: `docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md`",
            "5. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`",
            "",
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make label_audit_dashboard",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"dashboard_rows={len(rows)}")


if __name__ == "__main__":
    main()
