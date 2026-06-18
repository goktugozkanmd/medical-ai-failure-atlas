#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUYZE_HEALTH_AI_SAFETY_READINESS_COMPANION_20260618.md"
DATA = ROOT / "docs" / "tuyze_health_ai_safety_readiness_companion_20260618.json"


REQUIRED_DOC_PHRASES = [
    "TUYZE Health AI Safety Readiness Companion",
    "public field readiness companion",
    "Türkiye Sağlık Veri Araştırmaları ve Yapay Zeka Uygulamaları Enstitüsü",
    "Büyük Veri Birimi",
    "Tıbbi Karar Destek Sistemleri Birimi",
    "Akıllı Medikal Cihaz Teknolojileri Birimi",
    "Sağlık Veri Organizasyonu Bilim Kurulu",
    "Yapay Zeka Bilim Kurulu",
    "Sağlıkta Yapay Zeka Seminerleri",
    "data fitness",
    "decision support limits",
    "source support",
    "Turkish clinical context",
    "failure mode disclosure",
    "data governance route",
    "public claim hygiene",
    "No official TÜYZE claim",
    "No official TÜSEB claim",
    "No patient data included",
    "make tuyze_health_ai_safety_readiness_companion",
]

FORBIDDEN_PHRASES = [
    "official tuyze partner",
    "official tuseb partner",
    "tuyze endorsed",
    "tuseb endorsed",
    "application submitted",
    "submission made",
    "patient data used for",
    "medical advice provided",
    "clinical deployment ready",
    "clinically validated for",
]

REQUIRED_FLAGS = {
    "claims_official_tuyze_status": False,
    "claims_official_tuseb_status": False,
    "claims_endorsement": False,
    "claims_partner_relationship": False,
    "claims_application": False,
    "claims_submission": False,
    "contains_patient_data": False,
    "claims_medical_advice": False,
    "claims_clinical_deployment": False,
    "claims_clinical_validation": False,
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
    source_facts = payload.get("source_facts", [])
    readiness_checks = payload.get("readiness_checks", [])
    if payload.get("source_fact_count") != 5 or len(source_facts) != 5:
        errors.append("Expected 5 source facts")
    if payload.get("readiness_check_count") != 7 or len(readiness_checks) != 7:
        errors.append("Expected 7 readiness checks")

    if errors:
        print("FAIL TUYZE health AI safety readiness companion validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TUYZE health AI safety readiness companion validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_facts={len(source_facts)}")
    print(f"readiness_checks={len(readiness_checks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
