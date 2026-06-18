#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_HEALTH_AI_SAFETY_READINESS_KIT_20260618.md"
DATA = ROOT / "docs" / "turkiye_health_ai_safety_readiness_kit_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Türkiye Health AI Safety Readiness Kit",
    "field readiness public preview",
    "TÜYZE",
    "Türkiye Sağlık Veri Araştırmaları ve Yapay Zeka Uygulamaları Enstitüsü",
    "Sağlıkta Yapay Zeka Seminerleri",
    "Marmara University Faculty of Medicine",
    "08 April to 20 May 2026",
    "Public health AI safety brief",
    "Clinician AI literacy micro module",
    "Source support delta queue",
    "Health data quality handoff",
    "Sandbox readiness boundary",
    "First outreach packet",
    "No patient data.",
    "No clinical deployment claim.",
    "No clinical validation claim.",
    "No official role claim.",
    "No partner claim.",
    "No submission claim.",
    "make turkiye_health_ai_safety_readiness_kit",
]

FORBIDDEN_PHRASES = [
    "official role confirmed",
    "partner confirmed",
    "endorsed by",
    "submitted to",
    "clinical deployment ready",
    "clinically validated",
    "patient data used",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "requires_goktug_clearance_before_outreach": True,
    "contains_patient_data": False,
    "claims_official_role": False,
    "claims_partner": False,
    "claims_endorsement": False,
    "claims_submission": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
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
    source_signals = payload.get("source_signals", [])
    modules = payload.get("modules", [])
    if len(source_signals) != 3:
        errors.append("Expected 3 source signals")
    if payload.get("module_count") != 6 or len(modules) != 6:
        errors.append("Expected 6 kit modules")
    required_ids = {f"THAIK{index:03d}" for index in range(1, 7)}
    found_ids = {module.get("module_id") for module in modules}
    missing_ids = sorted(required_ids - found_ids)
    if missing_ids:
        errors.append(f"Missing module ids: {', '.join(missing_ids)}")

    if errors:
        print("FAIL Türkiye health AI safety readiness kit validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye health AI safety readiness kit validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"modules={len(modules)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
