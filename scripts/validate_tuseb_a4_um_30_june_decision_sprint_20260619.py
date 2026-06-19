#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUSEB_A4_UM_30_JUNE_DECISION_SPRINT_20260619.md"
DATA = ROOT / "docs" / "tuseb_a4_um_30_june_decision_sprint_20260619.json"


REQUIRED_DOC_PHRASES = [
    "TÜSEB A4 UM 30 June Decision Sprint",
    "not an application",
    "not a TÜSEB application",
    "not a TBYS submission",
    "Live source signals checked on 2026 06 19",
    "SPRINT001: TÜSEB A4 UM official notice",
    "16 June 2026",
    "SPRINT002: TÜSEB A group call document",
    "15 June to 30 June",
    "10 July",
    "13 July to 14 August",
    "16 September",
    "SPRINT003: TÜBİTAK 1711 contrast",
    "smart education technologies",
    "letter of intent",
    "Sprint decision table",
    "Personal A4 UM eligibility",
    "Route owner",
    "TBYS action",
    "Patient data boundary",
    "The only useful pre application question",
    "Minimum concept if route fit is positive",
    "Stop rules",
    "Current state is route and eligibility closure, not proposal writing.",
    "make tuseb_a4_um_30_june_decision_sprint",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "tbys submitted",
    "partner confirmed",
    "institution approved",
    "budget approved",
    "payment completed",
    "terms accepted",
    "patient data used",
    "ethics approved",
    "clinical validation complete",
    "clinical deployment ready",
    "ranking certified",
    "endorsement secured",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "claims_tuseb_application": False,
    "claims_tbys_submission": False,
    "claims_tuyze_proposal": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_budget_approval": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_ethics_approval": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_endorsement": False,
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
    if len(payload.get("source_signals", [])) != 3:
        errors.append("Expected 3 source signals")
    if len(payload.get("decision_rows", [])) != 10:
        errors.append("Expected 10 decision rows")
    if len(payload.get("minimum_concept_scope", [])) != 6:
        errors.append("Expected 6 minimum concept scope rows")
    if payload.get("current_decision") != "route and eligibility closure, not proposal writing":
        errors.append("Unexpected current decision")

    if errors:
        print("FAIL TÜSEB A4 UM 30 June decision sprint validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜSEB A4 UM 30 June decision sprint validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(payload.get('source_signals', []))}")
    print(f"decision_rows={len(payload.get('decision_rows', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
