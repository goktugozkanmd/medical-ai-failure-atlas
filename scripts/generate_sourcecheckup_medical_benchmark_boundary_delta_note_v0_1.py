#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SOURCECHECKUP_MEDICAL_BENCHMARK_BOUNDARY_DELTA_NOTE_V0_1.md"
DATA = ROOT / "docs" / "sourcecheckup_medical_benchmark_boundary_delta_note_v0_1.json"


DELTAS = [
    {
        "delta_id": "SCBBD001",
        "source_surface": "HealthBench public awareness",
        "boundary_delta": "Use as external source awareness only",
        "public_use": "rubric discipline discussion without compatibility wording",
        "blocked_claim": "HealthBench compatibility",
        "next_review_action": "keep reviewer questions separate from score fields",
    },
    {
        "delta_id": "SCBBD002",
        "source_surface": "MedHELM public awareness",
        "boundary_delta": "Use as workflow concept comparison only",
        "public_use": "task family orientation without equivalence wording",
        "blocked_claim": "MedHELM equivalence",
        "next_review_action": "map task language to source support questions only",
    },
    {
        "delta_id": "SCBBD003",
        "source_surface": "Open medical model family awareness",
        "boundary_delta": "Use as model landscape awareness only",
        "public_use": "document boundary questions without use or endorsement wording",
        "blocked_claim": "model endorsement",
        "next_review_action": "avoid naming any model as preferred or safer",
    },
    {
        "delta_id": "SCBBD004",
        "source_surface": "Source support queue",
        "boundary_delta": "Use as source claim review queue before report language",
        "public_use": "ask whether each answer has source support and uncertainty handling",
        "blocked_claim": "source truth certification",
        "next_review_action": "route central claims to source review before public summary",
    },
    {
        "delta_id": "SCBBD005",
        "source_surface": "Reviewer question route",
        "boundary_delta": "Use reviewer questions instead of scores",
        "public_use": "collect contributor questions that do not rank systems",
        "blocked_claim": "score report",
        "next_review_action": "hold scoring language outside public preview artifacts",
    },
    {
        "delta_id": "SCBBD006",
        "source_surface": "Public release route",
        "boundary_delta": "Use public preview wording only",
        "public_use": "state limits before any external collaboration text",
        "blocked_claim": "clinical validation",
        "next_review_action": "require owner clearance before external contact or submission",
    },
]


BOUNDARIES = [
    "No patient data.",
    "Synthetic only.",
    "Not for clinical use.",
    "No endpoint result.",
    "No score report.",
    "No model ranking.",
    "No benchmark compatibility claim.",
    "No benchmark equivalence claim.",
    "No clinical validation claim.",
    "No clinical deployment claim.",
    "No official role claim.",
    "No route access claim.",
    "No submission claim.",
    "No partner claim.",
    "No terms acceptance.",
    "No payment.",
    "No endorsement claim.",
]


def write_json() -> None:
    payload = {
        "artifact": "sourcecheckup_medical_benchmark_boundary_delta_note_v0_1",
        "date": "2026 06 18",
        "status": "public preview",
        "contains_patient_data": False,
        "synthetic_only": True,
        "not_for_clinical_use": True,
        "no_endpoint_result": True,
        "no_score_report": True,
        "no_model_ranking": True,
        "no_benchmark_compatibility_claim": True,
        "no_benchmark_equivalence_claim": True,
        "no_clinical_validation_claim": True,
        "no_clinical_deployment_claim": True,
        "no_official_role_claim": True,
        "no_route_access_claim": True,
        "no_submission_claim": True,
        "no_partner_claim": True,
        "no_terms_acceptance": True,
        "no_payment": True,
        "no_endorsement_claim": True,
        "delta_count": len(DELTAS),
        "deltas": DELTAS,
        "boundaries": BOUNDARIES,
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines: list[str] = [
        "# SourceCheckup Medical benchmark boundary delta note v0.1",
        "",
        "Date: 2026 06 18",
        "",
        "Status: public preview.",
        "",
        "This note records what SourceCheckup Medical can borrow from benchmark style review and what it must block in public wording.",
        "",
        "It is a boundary delta note, not a benchmark report.",
        "",
        "It does not claim benchmark compatibility, benchmark equivalence, endpoint result, score report, model ranking, clinical validation, clinical deployment, patient data use, official role, route access, partner status, submission, terms acceptance, payment, or endorsement.",
        "",
        "## Boundary",
        "",
    ]
    lines.extend(f"{index}. {boundary}" for index, boundary in enumerate(BOUNDARIES, start=1))
    lines.extend(
        [
            "",
            "## Delta rows",
            "",
        ]
    )
    for delta in DELTAS:
        lines.extend(
            [
                f"### {delta['delta_id']}: {delta['source_surface']}",
                "",
                f"Boundary delta: {delta['boundary_delta']}.",
                "",
                f"Public use: {delta['public_use']}.",
                "",
                f"Blocked claim: {delta['blocked_claim']}.",
                "",
                f"Next review action: {delta['next_review_action']}.",
                "",
            ]
        )
    lines.extend(
        [
            "## Public use",
            "",
            "Allowed use: cite this artifact as a SourceCheckup Medical boundary delta note for benchmark style literacy.",
            "",
            "Blocked use: do not cite this artifact as a benchmark compatibility claim, benchmark equivalence claim, endpoint result, score report, model ranking, clinical validation, clinical deployment, official role, route access, partner status, submission, terms acceptance, payment, or endorsement.",
            "",
            "## Files",
            "",
            "1. JSON source: `docs/sourcecheckup_medical_benchmark_boundary_delta_note_v0_1.json`",
            "2. Markdown note: `docs/SOURCECHECKUP_MEDICAL_BENCHMARK_BOUNDARY_DELTA_NOTE_V0_1.md`",
            "3. Validator: `scripts/validate_sourcecheckup_medical_benchmark_boundary_delta_note_v0_1.py`",
            "4. Runnable target: `make sourcecheckup_medical_benchmark_boundary_delta`",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_json()
    write_doc()
    print(f"generated={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"deltas={len(DELTAS)}")


if __name__ == "__main__":
    main()
