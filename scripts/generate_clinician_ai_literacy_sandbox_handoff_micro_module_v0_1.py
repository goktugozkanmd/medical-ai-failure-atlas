#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "CLINICIAN_AI_LITERACY_SANDBOX_HANDOFF_MICRO_MODULE_V0_1.md"
DATA = ROOT / "docs" / "clinician_ai_literacy_sandbox_handoff_micro_module_v0_1.json"


STEPS = [
    {
        "step_id": "CLSH001",
        "title": "Public preview boundary",
        "minutes": 3,
        "learner_task": "Name what this public preview can and cannot claim",
        "handoff_signal": "Reader can repeat no patient data and not for clinical use",
        "blocked_claim": "clinical deployment",
        "next_evidence": "owner reviewed public wording before any external route",
    },
    {
        "step_id": "CLSH002",
        "title": "Sandbox readiness question",
        "minutes": 3,
        "learner_task": "Turn a sandbox idea into a readiness question",
        "handoff_signal": "Question asks for governance, review role, and evidence",
        "blocked_claim": "sandbox access",
        "next_evidence": "source checked route details before any application language",
    },
    {
        "step_id": "CLSH003",
        "title": "Source support gate",
        "minutes": 3,
        "learner_task": "Separate citation presence from source support",
        "handoff_signal": "Reader can identify missing support without scoring a model",
        "blocked_claim": "source truth certification",
        "next_evidence": "SourceCheckup row linked to a claim specific review question",
    },
    {
        "step_id": "CLSH004",
        "title": "Clinician review handoff",
        "minutes": 3,
        "learner_task": "Assign clinician review before any practical use language",
        "handoff_signal": "Reader can state why local pass is not clinical validation",
        "blocked_claim": "clinical validation",
        "next_evidence": "named human review role after owner clearance",
    },
    {
        "step_id": "CLSH005",
        "title": "Public wording repair",
        "minutes": 3,
        "learner_task": "Rewrite unsafe public wording into bounded preview wording",
        "handoff_signal": "Wording removes access, approval, partner, and endorsement claims",
        "blocked_claim": "official role",
        "next_evidence": "wording decision log before external use",
    },
    {
        "step_id": "CLSH006",
        "title": "Next action gate",
        "minutes": 3,
        "learner_task": "Choose the next safe public build without outreach",
        "handoff_signal": "Next action is documentation or validation only",
        "blocked_claim": "submission",
        "next_evidence": "explicit owner decision before contact, terms, payment, or submission",
    },
]


BOUNDARIES = [
    "No patient data.",
    "Synthetic only.",
    "Not for clinical use.",
    "No clinical validation claim.",
    "No clinical deployment claim.",
    "No endpoint result.",
    "No score report.",
    "No model ranking.",
    "No benchmark compatibility claim.",
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
        "artifact": "clinician_ai_literacy_sandbox_handoff_micro_module_v0_1",
        "date": "2026 06 18",
        "status": "public preview",
        "contains_patient_data": False,
        "synthetic_only": True,
        "not_for_clinical_use": True,
        "no_clinical_validation_claim": True,
        "no_clinical_deployment_claim": True,
        "no_endpoint_result": True,
        "no_score_report": True,
        "no_model_ranking": True,
        "no_benchmark_compatibility_claim": True,
        "no_route_access_claim": True,
        "no_official_role_claim": True,
        "no_partner_claim": True,
        "no_submission_claim": True,
        "no_terms_acceptance": True,
        "no_payment": True,
        "no_endorsement_claim": True,
        "step_count": len(STEPS),
        "total_minutes": sum(step["minutes"] for step in STEPS),
        "steps": STEPS,
        "boundaries": BOUNDARIES,
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines: list[str] = [
        "# Clinician AI literacy sandbox handoff micro module v0.1",
        "",
        "Date: 2026 06 18",
        "",
        "Status: public preview.",
        "",
        "This micro module turns sandbox readiness into a short clinician literacy handoff. It is documentation for public review only.",
        "",
        "It does not claim sandbox access, route access, official role, partner status, submission, terms acceptance, payment, clinical validation, clinical deployment, endpoint result, score report, model ranking, benchmark compatibility, patient data use, or endorsement.",
        "",
        "## Boundary",
        "",
    ]
    lines.extend(f"{index}. {boundary}" for index, boundary in enumerate(BOUNDARIES, start=1))
    lines.extend(
        [
            "",
            "## Micro module steps",
            "",
            f"Total minutes: {sum(step['minutes'] for step in STEPS)}",
            "",
            f"Steps: {len(STEPS)}",
            "",
        ]
    )
    for step in STEPS:
        lines.extend(
            [
                f"### {step['step_id']}: {step['title']}",
                "",
                f"Minutes: {step['minutes']}",
                "",
                f"Learner task: {step['learner_task']}.",
                "",
                f"Handoff signal: {step['handoff_signal']}.",
                "",
                f"Blocked claim: {step['blocked_claim']}.",
                "",
                f"Next evidence: {step['next_evidence']}.",
                "",
            ]
        )
    lines.extend(
        [
            "## Public use",
            "",
            "Allowed use: cite this artifact as a public preview clinician literacy handoff module for sandbox readiness discussion.",
            "",
            "Blocked use: do not cite this artifact as sandbox access, clinical validation, clinical deployment, route access, official role, partner status, submission, terms acceptance, payment, score, ranking, endpoint result, benchmark compatibility, patient data use, or endorsement.",
            "",
            "## Files",
            "",
            "1. JSON source: `docs/clinician_ai_literacy_sandbox_handoff_micro_module_v0_1.json`",
            "2. Markdown module: `docs/CLINICIAN_AI_LITERACY_SANDBOX_HANDOFF_MICRO_MODULE_V0_1.md`",
            "3. Validator: `scripts/validate_clinician_ai_literacy_sandbox_handoff_micro_module_v0_1.py`",
            "4. Runnable target: `make clinician_ai_literacy_sandbox_handoff_micro_module`",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_json()
    write_doc()
    print(f"generated={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"steps={len(STEPS)}")
    print(f"minutes={sum(step['minutes'] for step in STEPS)}")


if __name__ == "__main__":
    main()
