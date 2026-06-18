#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUBITAK_1711_AI_ASSURANCE_SIDECAR_20260618.md"
DATA = ROOT / "docs" / "tubitak_1711_ai_assurance_sidecar_20260618.json"


REQUIRED_DOC_PHRASES = [
    "TÜBİTAK 1711 AI Assurance Sidecar",
    "field readiness public preview",
    "Direct health fit is weak",
    "15 June 2026",
    "18 September 2026",
    "14 September 2026 at 17:30",
    "smart production systems",
    "smart agriculture",
    "financial technologies",
    "climate change and sustainability",
    "smart education technologies",
    "customer organization",
    "technology provider",
    "research lab",
    "No health priority fit claim.",
    "No application submission.",
    "make tubitak_1711_ai_assurance_sidecar",
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
    "contains_patient_data": False,
    "claims_submission": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_health_priority_fit": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "requires_goktug_clearance_before_scouting": True,
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
    modules = payload.get("sidecar_modules", [])
    if payload.get("source_fact_count") != 6 or len(source_facts) != 6:
        errors.append("Expected 6 source facts")
    if payload.get("module_count") != 5 or len(modules) != 5:
        errors.append("Expected 5 sidecar modules")

    if errors:
        print("FAIL TÜBİTAK 1711 AI assurance sidecar validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜBİTAK 1711 AI assurance sidecar validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"facts={len(source_facts)}")
    print(f"modules={len(modules)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
