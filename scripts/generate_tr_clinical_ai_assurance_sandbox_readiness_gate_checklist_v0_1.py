#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TR_CLINICAL_AI_ASSURANCE_SANDBOX_READINESS_GATE_CHECKLIST_V0_1.md"
DATA = ROOT / "docs" / "tr_clinical_ai_assurance_sandbox_readiness_gate_checklist_v0_1.json"


GATES = [
    {
        "gate_id": "TRSBRG001",
        "gate_name": "Intended use boundary",
        "gate_question": "Is the public wording limited to sandbox readiness discussion only",
        "readiness_signal": "Scope says public preview and not for clinical use",
        "blocked_claim": "clinical deployment",
        "required_next_evidence": "owner reviewed outward wording before any external route",
    },
    {
        "gate_id": "TRSBRG002",
        "gate_name": "Data boundary",
        "gate_question": "Does the artifact avoid patient data and live care records",
        "readiness_signal": "Synthetic only statement is visible in the artifact",
        "blocked_claim": "patient data use",
        "required_next_evidence": "separate data governance review before any real data discussion",
    },
    {
        "gate_id": "TRSBRG003",
        "gate_name": "Clinician oversight boundary",
        "gate_question": "Are human review roles and escalation paths stated before any pilot language",
        "readiness_signal": "Clinician review is described as a required gate",
        "blocked_claim": "autonomous clinical use",
        "required_next_evidence": "named review role and escalation record after owner clearance",
    },
    {
        "gate_id": "TRSBRG004",
        "gate_name": "Ethics and governance boundary",
        "gate_question": "Is ethics status described as a source checked gate rather than approval",
        "readiness_signal": "Ethics wording blocks approval and national rule claims",
        "blocked_claim": "ethics approval",
        "required_next_evidence": "source verified ethics route before submission language",
    },
    {
        "gate_id": "TRSBRG005",
        "gate_name": "Technical evidence boundary",
        "gate_question": "Are audit logs, source support, and failure modes separated from endpoint results",
        "readiness_signal": "Evidence fields are listed without endpoint result language",
        "blocked_claim": "endpoint performance",
        "required_next_evidence": "read only validation log for each public artifact",
    },
    {
        "gate_id": "TRSBRG006",
        "gate_name": "Release decision boundary",
        "gate_question": "Is any public action kept below application, access, or endorsement language",
        "readiness_signal": "Owner clearance is required before external contact or sandbox application",
        "blocked_claim": "route access",
        "required_next_evidence": "explicit owner decision before any application step",
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
        "artifact": "tr_clinical_ai_assurance_sandbox_readiness_gate_checklist_v0_1",
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
        "no_official_role_claim": True,
        "no_route_access_claim": True,
        "no_submission_claim": True,
        "no_partner_claim": True,
        "no_terms_acceptance": True,
        "no_payment": True,
        "no_endorsement_claim": True,
        "gate_count": len(GATES),
        "gates": GATES,
        "boundaries": BOUNDARIES,
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines: list[str] = [
        "# TR clinical AI assurance sandbox readiness gate checklist v0.1",
        "",
        "Date: 2026 06 18",
        "",
        "Status: public preview.",
        "",
        "This checklist turns the Turkish clinical AI assurance lab lane into a public sandbox readiness gate. It is for infrastructure review only.",
        "",
        "It does not claim sandbox access, ethics approval, official role, partner status, submission, clinical validation, clinical deployment, endpoint result, score report, model ranking, benchmark compatibility, payment, terms acceptance, or endorsement.",
        "",
        "## Boundary",
        "",
    ]
    lines.extend(f"{index}. {boundary}" for index, boundary in enumerate(BOUNDARIES, start=1))
    lines.extend(
        [
            "",
            "## Gate checklist",
            "",
        ]
    )
    for gate in GATES:
        lines.extend(
            [
                f"### {gate['gate_id']}: {gate['gate_name']}",
                "",
                f"Gate question: {gate['gate_question']}.",
                "",
                f"Readiness signal: {gate['readiness_signal']}.",
                "",
                f"Blocked claim: {gate['blocked_claim']}.",
                "",
                f"Required next evidence: {gate['required_next_evidence']}.",
                "",
            ]
        )
    lines.extend(
        [
            "## Public use",
            "",
            "Allowed use: cite this artifact as a public preview readiness checklist for discussion.",
            "",
            "Blocked use: do not cite this artifact as clinical validation, sandbox access, ethics approval, official role, endpoint result, score report, model ranking, benchmark compatibility, partner status, submission, terms acceptance, payment, or endorsement.",
            "",
            "## Files",
            "",
            "1. JSON source: `docs/tr_clinical_ai_assurance_sandbox_readiness_gate_checklist_v0_1.json`",
            "2. Markdown note: `docs/TR_CLINICAL_AI_ASSURANCE_SANDBOX_READINESS_GATE_CHECKLIST_V0_1.md`",
            "3. Validator: `scripts/validate_tr_clinical_ai_assurance_sandbox_readiness_gate_checklist_v0_1.py`",
            "4. Runnable target: `make tr_clinical_ai_assurance_sandbox_readiness_gate`",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_json()
    write_doc()
    print(f"generated={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"gates={len(GATES)}")


if __name__ == "__main__":
    main()
