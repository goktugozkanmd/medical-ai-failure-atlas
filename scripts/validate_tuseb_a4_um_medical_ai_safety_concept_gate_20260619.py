#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUSEB_A4_UM_MEDICAL_AI_SAFETY_CONCEPT_GATE_20260619.md"
DATA = ROOT / "docs" / "tuseb_a4_um_medical_ai_safety_concept_gate_20260619.json"


REQUIRED_DOC_PHRASES = [
    "TÜSEB A4 UM Medical AI Safety Concept Gate",
    "public concept gate for a possible TÜSEB A4 UM aligned health AI safety route, not an application",
    "not a TÜSEB proposal",
    "not a TBYS submission",
    "not a TÜYZE partnership",
    "TÜSEB A4 UM expert call notice",
    "16 June 2026",
    "compulsory state service",
    "TÜSEB A group project support page",
    "at least doctorate or medical specialty degrees",
    "TÜYZE health data and AI route surface",
    "Büyük Veri Birimi",
    "Tıbbi Karar Destek Sistemleri Birimi",
    "Sağlık Veri Organizasyonu Bilim Kurulu",
    "Yapay Zeka Bilim Kurulu",
    "TÜBİTAK 1711 open call contrast",
    "15 June 2026 to 18 September 2026",
    "Fit lane 1: Turkish medical LLM safety evaluation",
    "Fit lane 2: clinician AI safety literacy",
    "Fit lane 3: health data quality and label audit",
    "Eligibility unknown",
    "Submission blocked",
    "No TÜSEB submission.",
    "No TBYS submission.",
    "No patient data.",
    "No clinical validation claim.",
    "make tuseb_a4_um_medical_ai_safety_concept_gate",
]

FORBIDDEN_PHRASES = [
    "tuseb approved",
    "tuyze approved",
    "official role granted",
    "route access granted",
    "partner confirmed",
    "application submitted",
    "proposal submitted",
    "patient data used",
    "clinical deployment ready",
    "clinical validation complete",
    "score certification complete",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "claims_tuseb_submission": False,
    "claims_tbys_submission": False,
    "claims_tuyze_proposal": False,
    "claims_official_role": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_budget": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_medical_advice": False,
    "claims_endorsement": False,
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
    if len(payload.get("source_signals", [])) != 4:
        errors.append("Expected 4 source signals")
    if len(payload.get("concept_lanes", [])) != 3:
        errors.append("Expected 3 concept lanes")
    if len(payload.get("proposal_blockers", [])) != 10:
        errors.append("Expected 10 proposal blockers")
    if payload.get("next_outward_action") != "prepare one page TUSEB route fit question if no route owner replies":
        errors.append("Unexpected next outward action")

    if errors:
        print("FAIL TÜSEB A4 UM medical AI safety concept gate validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜSEB A4 UM medical AI safety concept gate validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(payload.get('source_signals', []))}")
    print(f"lanes={len(payload.get('concept_lanes', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
