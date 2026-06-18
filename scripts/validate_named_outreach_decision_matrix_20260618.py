#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "NAMED_OUTREACH_DECISION_MATRIX_20260618.md"
DATA = ROOT / "docs" / "named_outreach_decision_matrix_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Named outreach decision matrix",
    "field readiness public preview",
    "TÜYZE institutional readiness route",
    "TEKNOFEST contestant safety route",
    "TÜBİTAK 1711 adjacent AI assurance route",
    "CHAI applied model card companion route",
    "MedHELM benchmark boundary companion route",
    "Decision needed",
    "Blocker",
    "No email is sent",
    "No submission is made",
    "make named_outreach_decision_matrix",
]

FORBIDDEN_PHRASES = [
    "email sent",
    "submission made",
    "application submitted",
    "partner confirmed",
    "official role confirmed",
    "endorsed by",
    "clinical deployment ready",
    "clinically validated",
    "patient data used",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "requires_goktug_clearance_before_outreach": True,
    "contains_patient_data": False,
    "claims_submission": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_endorsement": False,
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
    routes = payload.get("routes", [])
    if payload.get("route_count") != 5 or len(routes) != 5:
        errors.append("Expected 5 decision routes")
    required_ids = {f"NODM{index:03d}" for index in range(1, 6)}
    found_ids = {route.get("route_id") for route in routes}
    missing_ids = sorted(required_ids - found_ids)
    if missing_ids:
        errors.append(f"Missing route ids: {', '.join(missing_ids)}")

    if errors:
        print("FAIL named outreach decision matrix validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS named outreach decision matrix validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"routes={len(routes)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
