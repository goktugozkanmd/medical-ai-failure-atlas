#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUSEB_A4_UM_TUYZE_NON_PATIENT_DATA_CONCEPT_NOTE_20260619.md"
DATA = ROOT / "docs" / "tuseb_a4_um_tuyze_non_patient_data_concept_note_20260619.json"


REQUIRED_DOC_PHRASES = [
    "TÜSEB A4 UM TÜYZE Non Patient Data Concept Note",
    "public one page concept note for a medical AI safety readiness package",
    "not a TÜSEB application",
    "not a TBYS submission",
    "not a TÜYZE proposal",
    "TÜSEB A4 UM expert call notice",
    "16 June 2026",
    "compulsory state service",
    "TÜSEB A group project support page",
    "doctorate or medical specialty degrees",
    "TÜYZE health data and AI route surface",
    "Büyük Veri Birimi",
    "Tıbbi Karar Destek Sistemleri Birimi",
    "Yapay Zeka Bilim Kurulu",
    "TÜBİTAK open calls contrast",
    "15 June 2026 to 18 September 2026",
    "Türkiye Medical AI Safety Readiness Package",
    "Turkish medical LLM safety evaluation readiness",
    "Clinician AI literacy and responsible use micro module",
    "Health data quality and label audit worksheet",
    "No ranking safety report template",
    "No patient data.",
    "No clinical validation claim.",
    "The route question e mail to TÜSEB has been sent and is waiting for a reply.",
    "make tuseb_a4_um_tuyze_non_patient_data_concept_note",
]

FORBIDDEN_PHRASES = [
    "tuseb approved",
    "tuyze approved",
    "official role granted",
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
    "claims_tuseb_application": False,
    "claims_tbys_submission": False,
    "claims_tuyze_proposal": False,
    "claims_partner": False,
    "claims_official_role": False,
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
    if len(payload.get("scope", [])) != 5:
        errors.append("Expected 5 scope items")
    if len(payload.get("deliverables", [])) != 8:
        errors.append("Expected 8 deliverables")
    if payload.get("route_question_thread_active") is not True:
        errors.append("Expected active route question thread marker")

    if errors:
        print("FAIL TÜSEB A4 UM TÜYZE non patient data concept note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜSEB A4 UM TÜYZE non patient data concept note validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(payload.get('source_signals', []))}")
    print(f"scope_items={len(payload.get('scope', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
