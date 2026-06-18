#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TEKNOFEST_HEALTH_AI_SAFETY_ADDENDUM_20260618.md"
DATA = ROOT / "docs" / "teknofest_health_ai_safety_addendum_20260618.json"


REQUIRED_DOC_PHRASES = [
    "TEKNOFEST Health AI Safety Addendum",
    "field readiness public preview",
    "not an official TEKNOFEST document",
    "29 June 2026 at 17:00",
    "predicting whether genetic variants are pathogenic or benign",
    "Health claim boundary",
    "Label uncertainty",
    "Data leakage",
    "Population and context limits",
    "Source support",
    "Human review handoff",
    "Failure examples",
    "No official TEKNOFEST endorsement claim.",
    "No submission claim.",
    "No clinical deployment claim.",
    "No clinical validation claim.",
    "No patient data included.",
    "make teknofest_health_ai_safety_addendum",
]

FORBIDDEN_PHRASES = [
    "official teknofest endorsement granted",
    "teknofest endorsed",
    "partner confirmed",
    "submitted to",
    "clinical deployment ready",
    "clinically validated",
    "patient data used",
    "score certification complete",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "claims_official_endorsement": False,
    "claims_submission": False,
    "claims_partner": False,
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
    checks = payload.get("checks", [])
    if len(source_signals) != 3:
        errors.append("Expected 3 source signals")
    if payload.get("check_count") != 7 or len(checks) != 7:
        errors.append("Expected 7 addendum checks")
    required_ids = {f"THASC{index:03d}" for index in range(1, 8)}
    found_ids = {check.get("check_id") for check in checks}
    missing_ids = sorted(required_ids - found_ids)
    if missing_ids:
        errors.append(f"Missing check ids: {', '.join(missing_ids)}")

    if errors:
        print("FAIL TEKNOFEST health AI safety addendum validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TEKNOFEST health AI safety addendum validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"checks={len(checks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
