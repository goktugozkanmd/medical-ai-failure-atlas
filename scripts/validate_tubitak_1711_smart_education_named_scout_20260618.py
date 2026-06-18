#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUBITAK_1711_SMART_EDUCATION_NAMED_SCOUT_20260618.md"
DATA = ROOT / "docs" / "tubitak_1711_smart_education_named_scout_20260618.json"


REQUIRED_DOC_PHRASES = [
    "TÜBİTAK 1711 Smart Education Named Scout",
    "named route scout, not an application",
    "Direct health AI fit remains weak",
    "smart education technologies",
    "SEBİT",
    "SEBİT LMS",
    "SEBİT AI",
    "Acibadem CASE",
    "TÜYZE",
    "No application submission.",
    "No intent declaration.",
    "No partner commitment.",
    "No health priority fit claim.",
    "make tubitak_1711_smart_education_named_scout",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "intent declaration submitted",
    "partner confirmed",
    "official role confirmed",
    "endorsement confirmed",
    "health priority fit confirmed",
    "clinical deployment ready",
    "clinically validated",
    "patient data used",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "all_scout_gates_open": False,
    "contains_patient_data": False,
    "claims_submission": False,
    "claims_intent_declaration": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_health_priority_fit": False,
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
    if payload.get("direct_health_fit") != "weak":
        errors.append("direct_health_fit must be weak")
    if payload.get("only_priority_fit") != "smart education technologies":
        errors.append("only priority fit must be smart education technologies")
    if len(payload.get("named_surfaces", [])) != 3:
        errors.append("Expected three named surfaces")
    if len(payload.get("scout_gates", [])) != 4:
        errors.append("Expected four scout gates")

    if errors:
        print("FAIL TÜBİTAK 1711 smart education named scout validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜBİTAK 1711 smart education named scout validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"named_surfaces={len(payload.get('named_surfaces', []))}")
    print(f"scout_gates={len(payload.get('scout_gates', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
