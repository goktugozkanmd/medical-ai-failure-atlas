#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "GOKTUG_FIELD_ACTION_REVIEW_PACKET_20260618.md"
DATA = ROOT / "docs" / "goktug_field_action_review_packet_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Goktug Field Action Review Packet",
    "Dr. Goktug review packet public preview",
    "TEKNOFEST public share draft",
    "TÜYZE readiness outreach draft",
    "TÜBİTAK 1711 consortium scouting brief",
    "29 June 2026 at 17:00",
    "Direct health fit is weak",
    "No email is sent",
    "No public post is made",
    "No submission is made",
    "No application is submitted",
    "No partner commitment is made",
    "No official role is claimed",
    "No patient data is used",
    "No clinical deployment is claimed",
    "No clinical validation is claimed",
    "make goktug_field_action_review_packet",
]

FORBIDDEN_PHRASES = [
    "email sent",
    "public post made",
    "submission made",
    "application submitted",
    "partner confirmed",
    "official role confirmed",
    "endorsed by",
    "patient data used for",
    "clinical deployment ready",
    "clinically validated",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "requires_goktug_clearance_before_send": True,
    "contains_patient_data": False,
    "claims_submission": False,
    "claims_application": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_tubitak_health_priority_fit": False,
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
    options = payload.get("options", [])
    if payload.get("source_fact_count") != 7 or len(source_facts) != 7:
        errors.append("Expected 7 source facts")
    if payload.get("option_count") != 3 or len(options) != 3:
        errors.append("Expected 3 field action options")
    required_ids = {f"GFARO{index:03d}" for index in range(1, 4)}
    found_ids = {option.get("option_id") for option in options}
    missing_ids = sorted(required_ids - found_ids)
    if missing_ids:
        errors.append(f"Missing option ids: {', '.join(missing_ids)}")

    if errors:
        print("FAIL Goktug field action review packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Goktug field action review packet validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_facts={len(source_facts)}")
    print(f"options={len(options)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
