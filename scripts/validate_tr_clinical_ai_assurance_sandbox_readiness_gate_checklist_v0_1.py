#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TR_CLINICAL_AI_ASSURANCE_SANDBOX_READINESS_GATE_CHECKLIST_V0_1.md"
DATA = ROOT / "docs" / "tr_clinical_ai_assurance_sandbox_readiness_gate_checklist_v0_1.json"

REQUIRED_DOC_PHRASES = [
    "TR clinical AI assurance sandbox readiness gate checklist v0.1",
    "public sandbox readiness gate",
    "infrastructure review only",
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
    "TRSBRG001",
    "TRSBRG002",
    "TRSBRG003",
    "TRSBRG004",
    "TRSBRG005",
    "TRSBRG006",
    "make tr_clinical_ai_assurance_sandbox_readiness_gate",
]

REQUIRED_JSON_FLAGS = {
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
}

FORBIDDEN_PHRASES = [
    "sandbox access granted",
    "ethics approval granted",
    "official role confirmed",
    "partner confirmed",
    "submitted application",
    "clinically validated",
    "validated for clinical use",
    "clinical deployment ready",
    "endpoint result reported",
    "score report completed",
    "model ranking report",
    "benchmark compatible",
    "payment completed",
    "terms accepted",
    "endorsed by",
    "patient data used",
]


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"Missing doc: {DOC.relative_to(ROOT)}")
    if not DATA.exists():
        errors.append(f"Missing data: {DATA.relative_to(ROOT)}")

    text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    lower_text = text.lower()
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Doc contains forbidden phrase: {phrase}")
    if "-" in text:
        errors.append("Doc contains hyphen character")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_JSON_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    gates = payload.get("gates", [])
    if payload.get("gate_count") != 6 or len(gates) != 6:
        errors.append("Expected 6 sandbox readiness gates")
    required_ids = {f"TRSBRG{index:03d}" for index in range(1, 7)}
    found_ids = {gate.get("gate_id") for gate in gates}
    missing_ids = sorted(required_ids - found_ids)
    if missing_ids:
        errors.append(f"Missing gate ids: {', '.join(missing_ids)}")
    for gate in gates:
        for field in ["gate_name", "gate_question", "readiness_signal", "blocked_claim", "required_next_evidence"]:
            if not gate.get(field):
                errors.append(f"{gate.get('gate_id')}: missing {field}")

    if errors:
        print("FAIL TR clinical AI assurance sandbox readiness gate checklist validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TR clinical AI assurance sandbox readiness gate checklist validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"gates={len(gates)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
