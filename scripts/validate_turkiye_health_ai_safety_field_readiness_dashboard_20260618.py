#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_HEALTH_AI_SAFETY_FIELD_READINESS_DASHBOARD_20260618.md"
DATA = ROOT / "docs" / "turkiye_health_ai_safety_field_readiness_dashboard_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Türkiye Health AI Safety Field Readiness Dashboard",
    "public field readiness dashboard, not an application",
    "Current signal level: early field discovery.",
    "Current strongest signal: one acknowledged health informatics review route.",
    "Current largest blocker: no substantive route owner reply yet.",
    "Lane A: clinician AI literacy",
    "Lane B: assurance and evaluation",
    "Lane C: data quality and label audit",
    "Lane D: smart education and TÜBİTAK 1711 adjacent route",
    "Lane E: ethics and public claim hygiene",
    "No application has been submitted.",
    "No patient data was used.",
    "No clinical validation exists.",
    "make turkiye_health_ai_safety_field_readiness_dashboard",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "proposal submitted",
    "congress submitted",
    "partner confirmed",
    "official role confirmed",
    "endorsement confirmed",
    "clinical deployment ready",
    "clinically validated",
    "patient data used",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
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
    lanes = payload.get("lanes", [])
    if len(lanes) != 5:
        errors.append("Expected five readiness lanes")
    if payload.get("signal_level") != "early field discovery":
        errors.append("signal level must be early field discovery")

    if errors:
        print("FAIL Türkiye health AI safety field readiness dashboard validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye health AI safety field readiness dashboard validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"lanes={len(lanes)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
