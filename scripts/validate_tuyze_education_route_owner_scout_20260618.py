#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUYZE_EDUCATION_ROUTE_OWNER_SCOUT_20260618.md"
DATA = ROOT / "docs" / "tuyze_education_route_owner_scout_20260618.json"


REQUIRED_DOC_PHRASES = [
    "TÜYZE Education Route Owner Scout",
    "route owner scout, not an application",
    "info@tuseb.gov.tr",
    "tuseb@hs01.kep.tr",
    "Do not ask for a TÜBİTAK application submission.",
    "Do not ask for a TÜSEB proposal submission.",
    "No application submission.",
    "No proposal submission.",
    "No patient data.",
    "No clinical validation claim.",
    "make tuyze_education_route_owner_scout",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "proposal submitted",
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
    "kep_not_used": True,
    "contains_patient_data": False,
    "claims_submission": False,
    "claims_proposal": False,
    "claims_intent_declaration": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_health_priority_fit": False,
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
    if payload.get("target_contact") != "info@tuseb.gov.tr":
        errors.append("target contact must be TÜSEB general information route")
    if len(payload.get("route_gates", [])) != 4:
        errors.append("Expected four route gates")

    if errors:
        print("FAIL TÜYZE education route owner scout validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜYZE education route owner scout validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"route_gates={len(payload.get('route_gates', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
