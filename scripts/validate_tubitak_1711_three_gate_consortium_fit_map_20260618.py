#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUBITAK_1711_THREE_GATE_CONSORTIUM_FIT_MAP_20260618.md"
DATA = ROOT / "docs" / "tubitak_1711_three_gate_consortium_fit_map_20260618.json"


REQUIRED_DOC_PHRASES = [
    "TÜBİTAK 1711 Three Gate Consortium Fit Map",
    "live fit map, not an application",
    "Demand side gate.",
    "Education technology provider gate.",
    "Research route gate.",
    "health is not listed as a 2026 priority area",
    "Private Gmail threads were checked before this public package.",
    "SEBİT route owner thread `19edb2e645ca1f6d`: checked, no reply.",
    "Acibadem CASE demand side thread `19edb491af3d687b`: checked, no reply.",
    "TÜYZE or TÜSEB education route owner thread `19edb64c4ae9fec6`: checked, no reply.",
    "Do not claim that a TÜBİTAK 1711 application exists.",
    "Do not claim that health is a 1711 priority area.",
    "No patient data.",
    "No clinical validation claim.",
    "make tubitak_1711_three_gate_consortium_fit_map",
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
    "contains_patient_data": False,
    "claims_application": False,
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
    if len(payload.get("gates", [])) != 4:
        errors.append("Expected four gates")
    if len(payload.get("gmail_threads_checked", [])) != 6:
        errors.append("Expected six Gmail threads checked")
    if "19edb64c4ae9fec6" not in payload.get("gmail_threads_checked", []):
        errors.append("TÜYZE or TÜSEB thread must be listed")
    if payload.get("reply_state", {}).get("outside_threads") != "no separate route owner reply found":
        errors.append("Outside thread reply state must be explicit")

    if errors:
        print("FAIL TÜBİTAK 1711 three gate consortium fit map validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜBİTAK 1711 three gate consortium fit map validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"gates={len(payload.get('gates', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
