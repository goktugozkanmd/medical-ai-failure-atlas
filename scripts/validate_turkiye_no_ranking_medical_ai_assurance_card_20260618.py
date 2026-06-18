#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_NO_RANKING_MEDICAL_AI_ASSURANCE_CARD_20260618.md"
DATA = ROOT / "docs" / "turkiye_no_ranking_medical_ai_assurance_card_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Türkiye No Ranking Medical AI Assurance Card",
    "public no ranking assurance card, not a comparison table",
    "not clinical validation, and not a deployment package",
    "Why no ranking",
    "This card does not decide which model should be preferred.",
    "State A: not reviewable",
    "State B: source support review needed",
    "State C: clinician review needed",
    "State D: public wording cleared",
    "State E: blocked",
    "Check 1: patient data boundary",
    "Check 2: source support",
    "Check 3: human review",
    "Check 4: no ranking",
    "Check 5: public claim hygiene",
    "Current gate: L1.",
    "It does not rank models.",
    "No patient data was used.",
    "No clinical validation exists.",
    "make turkiye_no_ranking_medical_ai_assurance_card",
]

FORBIDDEN_PHRASES = [
    "best model",
    "winner model",
    "leaderboard rank",
    "performance score",
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "official approval",
    "official acceptance",
    "institutional endorsement",
    "real patient data used",
    "model is safe",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "claims_model_ranking": False,
    "claims_best_model": False,
    "claims_application": False,
    "claims_proposal": False,
    "claims_congress_submission": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_endorsement": False,
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
    if payload.get("current_gate") != "L1":
        errors.append("current gate must be L1")
    if len(payload.get("decision_states", [])) != 5:
        errors.append("Expected five decision states")
    if len(payload.get("checks", [])) != 5:
        errors.append("Expected five checks")
    if len(payload.get("release_gates", [])) != 6:
        errors.append("Expected six release gates")

    if errors:
        print("FAIL Türkiye no ranking medical AI assurance card validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye no ranking medical AI assurance card validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"states={len(payload.get('decision_states', []))}")
    print(f"checks={len(payload.get('checks', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
