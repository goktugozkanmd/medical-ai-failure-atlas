#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "HACETTEPE_HEALTH_MANAGEMENT_AI_OUTREACH_PACKET_20260618.md"
DATA = ROOT / "docs" / "hacettepe_health_management_ai_outreach_packet_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Hacettepe Health Management AI Outreach Packet",
    "named target outreach packet",
    "Not sent",
    "Sağlık Yönetimi Bölümü",
    "Sağlık Yönetiminde Yapay Zeka",
    "Doç. Dr. Gamze Yorgancıoğlu Tarcan",
    "gamze@hacettepe.edu.tr",
    "Exact Turkish message candidate",
    "No email sent",
    "No contact made",
    "No official Hacettepe role claimed",
    "No partnership claimed",
    "No patient data used",
    "No clinical deployment claimed",
    "No clinical validation claimed",
    "make hacettepe_health_management_ai_outreach_packet",
]

FORBIDDEN_PHRASES = [
    "email sent",
    "contact made",
    "official hacettepe role confirmed",
    "endorsed by",
    "partnership confirmed",
    "application submitted",
    "submission made",
    "patient data used for",
    "clinical deployment ready",
    "clinically validated for",
]

REQUIRED_FLAGS = {
    "claims_email_sent": False,
    "claims_contact_made": False,
    "claims_official_role": False,
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
        if phrase in lower_text and f"no {phrase}" not in lower_text:
            errors.append(f"Doc contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append("Doc contains non URL hyphen character")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    if payload.get("source_count") != 4:
        errors.append("Expected source_count 4")
    if payload.get("message_count") != 1:
        errors.append("Expected message_count 1")
    if payload.get("primary_public_email_route") != "gamze@hacettepe.edu.tr":
        errors.append("Primary public email route mismatch")

    if errors:
        print("FAIL Hacettepe health management AI outreach packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Hacettepe health management AI outreach packet validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"sources={len(payload.get('sources', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
