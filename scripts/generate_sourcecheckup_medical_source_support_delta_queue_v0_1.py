#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SOURCECHECKUP_MEDICAL_SOURCE_SUPPORT_DELTA_QUEUE_V0_1.md"
DATA = ROOT / "docs" / "sourcecheckup_medical_source_support_delta_queue_v0_1.json"


ROWS = [
    {
        "row_id": "SCSSDQ001",
        "claim_surface": "Citation presence",
        "delta_question": "Does the answer merely cite a source or does the source support the exact claim",
        "minimum_review": "claim specific source support review",
        "blocked_claim": "source truth certification",
        "next_action": "keep citation presence separate from claim support",
    },
    {
        "row_id": "SCSSDQ002",
        "claim_surface": "Guideline scope",
        "delta_question": "Does guideline wording match population, setting, and clinical variables",
        "minimum_review": "scope and applicability review",
        "blocked_claim": "clinical advice",
        "next_action": "route missing variables to clinician review",
    },
    {
        "row_id": "SCSSDQ003",
        "claim_surface": "Policy wording",
        "delta_question": "Does public wording imply route access, approval, or official role",
        "minimum_review": "policy and public wording review",
        "blocked_claim": "route access",
        "next_action": "rewrite as public preview only",
    },
    {
        "row_id": "SCSSDQ004",
        "claim_surface": "Medication safety",
        "delta_question": "Does the claim need dosing, contraindication, interaction, or renal function context",
        "minimum_review": "clinician source review",
        "blocked_claim": "safe medication recommendation",
        "next_action": "block recommendation language until source and context review",
    },
    {
        "row_id": "SCSSDQ005",
        "claim_surface": "Benchmark wording",
        "delta_question": "Does the text imply score, ranking, compatibility, or equivalence",
        "minimum_review": "benchmark boundary review",
        "blocked_claim": "benchmark compatibility",
        "next_action": "replace score language with reviewer question language",
    },
    {
        "row_id": "SCSSDQ006",
        "claim_surface": "Release route",
        "delta_question": "Is the next public action documentation only and below outreach threshold",
        "minimum_review": "owner clearance gate review",
        "blocked_claim": "submission",
        "next_action": "require owner decision before contact, terms, payment, or submission",
    },
]


BOUNDARIES = [
    "No patient data.",
    "Synthetic only.",
    "Not for clinical use.",
    "No source truth certification.",
    "No clinical validation claim.",
    "No clinical deployment claim.",
    "No endpoint result.",
    "No score report.",
    "No model ranking.",
    "No benchmark compatibility claim.",
    "No benchmark equivalence claim.",
    "No route access claim.",
    "No official role claim.",
    "No partner claim.",
    "No submission claim.",
    "No terms acceptance.",
    "No payment.",
    "No endorsement claim.",
]


def write_json() -> None:
    payload = {
        "artifact": "sourcecheckup_medical_source_support_delta_queue_v0_1",
        "date": "2026 06 18",
        "status": "public preview",
        "contains_patient_data": False,
        "synthetic_only": True,
        "not_for_clinical_use": True,
        "no_source_truth_certification": True,
        "no_clinical_validation_claim": True,
        "no_clinical_deployment_claim": True,
        "no_endpoint_result": True,
        "no_score_report": True,
        "no_model_ranking": True,
        "no_benchmark_compatibility_claim": True,
        "no_benchmark_equivalence_claim": True,
        "no_route_access_claim": True,
        "no_official_role_claim": True,
        "no_partner_claim": True,
        "no_submission_claim": True,
        "no_terms_acceptance": True,
        "no_payment": True,
        "no_endorsement_claim": True,
        "row_count": len(ROWS),
        "rows": ROWS,
        "boundaries": BOUNDARIES,
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines: list[str] = [
        "# SourceCheckup Medical source support delta queue v0.1",
        "",
        "Date: 2026 06 18",
        "",
        "Status: public preview.",
        "",
        "This queue turns SourceCheckup Medical source support review into delta rows that can be inspected before any external use.",
        "",
        "It does not claim source truth certification, clinical validation, clinical deployment, endpoint result, score report, model ranking, benchmark compatibility, benchmark equivalence, route access, official role, partner status, submission, terms acceptance, payment, patient data use, or endorsement.",
        "",
        "## Boundary",
        "",
    ]
    lines.extend(f"{index}. {boundary}" for index, boundary in enumerate(BOUNDARIES, start=1))
    lines.extend(
        [
            "",
            "## Delta queue rows",
            "",
            f"Rows: {len(ROWS)}",
            "",
        ]
    )
    for row in ROWS:
        lines.extend(
            [
                f"### {row['row_id']}: {row['claim_surface']}",
                "",
                f"Delta question: {row['delta_question']}.",
                "",
                f"Minimum review: {row['minimum_review']}.",
                "",
                f"Blocked claim: {row['blocked_claim']}.",
                "",
                f"Next action: {row['next_action']}.",
                "",
            ]
        )
    lines.extend(
        [
            "## Public use",
            "",
            "Allowed use: cite this artifact as a public preview source support delta queue for SourceCheckup Medical.",
            "",
            "Blocked use: do not cite this artifact as source truth certification, clinical validation, clinical deployment, endpoint result, score report, model ranking, benchmark compatibility, benchmark equivalence, route access, official role, partner status, submission, terms acceptance, payment, patient data use, or endorsement.",
            "",
            "## Files",
            "",
            "1. JSON source: `docs/sourcecheckup_medical_source_support_delta_queue_v0_1.json`",
            "2. Markdown queue: `docs/SOURCECHECKUP_MEDICAL_SOURCE_SUPPORT_DELTA_QUEUE_V0_1.md`",
            "3. Validator: `scripts/validate_sourcecheckup_medical_source_support_delta_queue_v0_1.py`",
            "4. Runnable target: `make sourcecheckup_medical_source_support_delta_queue`",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_json()
    write_doc()
    print(f"generated={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"rows={len(ROWS)}")


if __name__ == "__main__":
    main()
