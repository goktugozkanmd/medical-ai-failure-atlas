#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TEKNOFEST_HEALTH_AI_DETAIL_REPORT_FINAL_GATE_20260618.md"
DATA = ROOT / "docs" / "teknofest_health_ai_detail_report_final_gate_20260618.json"


REQUIRED_DOC_PHRASES = [
    "TEKNOFEST Health AI Detail Report Final Gate",
    "time sensitive public final gate",
    "not an official TEKNOFEST document",
    "predicting whether genetic variants are pathogenic or benign",
    "29 June 2026 at 17:00",
    "Gate 1: data permission and privacy",
    "Gate 2: label provenance",
    "Gate 3: leakage check",
    "Gate 4: missingness and representation",
    "Gate 5: source support",
    "Gate 6: human review handoff",
    "Gate 7: failure mode examples",
    "Gate 8: no ranking and no validation",
    "Gate 9: public claim hygiene",
    "No official TEKNOFEST endorsement claim.",
    "No clinical deployment claim.",
    "No clinical validation claim.",
    "No model ranking.",
    "make teknofest_health_ai_detail_report_final_gate",
]

FORBIDDEN_PHRASES = [
    "official teknofest endorsement granted",
    "official teknofest role granted",
    "teknofest approved",
    "partner confirmed",
    "submitted to teknofest",
    "clinical deployment ready",
    "clinically validated",
    "patient data used",
    "score certification complete",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "claims_official_teknofest_role": False,
    "claims_official_endorsement": False,
    "claims_submission": False,
    "claims_application": False,
    "claims_partner": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_terms_acceptance": False,
    "claims_payment": False,
}


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


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
    if "-" in text_without_urls(text):
        errors.append("Doc contains non URL hyphen character")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    if len(payload.get("source_signals", [])) != 3:
        errors.append("Expected 3 source signals")
    if len(payload.get("gates", [])) != 9:
        errors.append("Expected 9 final gates")
    if len(payload.get("decision_states", [])) != 3:
        errors.append("Expected 3 decision states")

    if errors:
        print("FAIL TEKNOFEST health AI detail report final gate validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TEKNOFEST health AI detail report final gate validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"gates={len(payload.get('gates', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
