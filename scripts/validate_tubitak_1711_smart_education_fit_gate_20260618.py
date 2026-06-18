#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUBITAK_1711_SMART_EDUCATION_FIT_GATE_20260618.md"
DATA = ROOT / "docs" / "tubitak_1711_smart_education_fit_gate_20260618.json"


REQUIRED_DOC_PHRASES = [
    "TÜBİTAK 1711 Smart Education Fit Gate",
    "live call fit gate",
    "Direct health AI fit is weak",
    "smart education technologies",
    "15 June 2026",
    "18 September 2026",
    "14 September 2026 at 17:30",
    "customer organization",
    "technology provider",
    "research route",
    "No application submission.",
    "No intent declaration.",
    "No partner commitment.",
    "No health priority fit claim.",
    "make tubitak_1711_smart_education_fit_gate",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "intent declaration submitted",
    "partner confirmed",
    "official role confirmed",
    "health priority fit confirmed",
    "clinical deployment ready",
    "clinically validated",
    "patient data used",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "blocks_application": True,
    "blocks_intent_declaration": True,
    "blocks_partner_commitment": True,
    "contains_patient_data": False,
    "claims_submission": False,
    "claims_partner": False,
    "claims_official_role": False,
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
    if payload.get("only_adjacent_route_to_scout") != "smart education technologies":
        errors.append("only adjacent route must be smart education technologies")
    if len(payload.get("official_priority_areas", [])) != 5:
        errors.append("Expected five official priority areas")
    if len(payload.get("fit_gates", [])) != 5:
        errors.append("Expected five fit gates")

    if errors:
        print("FAIL TÜBİTAK 1711 smart education fit gate validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜBİTAK 1711 smart education fit gate validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"priority_areas={len(payload.get('official_priority_areas', []))}")
    print(f"fit_gates={len(payload.get('fit_gates', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
