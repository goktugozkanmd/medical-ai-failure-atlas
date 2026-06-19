#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ROUTE_OWNER_ACKNOWLEDGEMENT_FOLLOW_UP_DECISION_MEMO_20260619.md"
DATA = ROOT / "docs" / "route_owner_acknowledgement_follow_up_decision_memo_20260619.json"

REQUIRED_DOC_PHRASES = [
    "Route Owner Acknowledgement Follow Up Decision Memo",
    "public decision memo",
    "without turning it into endorsement",
    "Purpose: convert a polite acknowledgement into a disciplined follow up gate",
    "not a hospital partnership",
    "not a university partnership",
    "not institutional approval",
    "not an endorsement",
    "not an official role",
    "not a course approval",
    "not clinical validation",
    "not clinical deployment",
    "not patient data use",
    "One academic route owner acknowledgement exists.",
    "No substantive route guidance has arrived.",
    "No separate reply outside the original thread was found.",
    "Other active route owner threads remain silent.",
    "No new follow up e mail was sent in this run.",
    "State 1. Recent acknowledgement window",
    "State 2. One concise follow up after a real trigger",
    "State 3. Stop and do not follow up",
    "State 4. Substantive reply received",
    "Hospital AI Literacy Collaboration Packet",
    "Türkiye Clinical AI Assurance Lab Readiness Matrix",
    "Türkiye Health AI Safety Handoff Index",
    "No Ranking Benchmark Misuse Warning",
    "Today's state is State 1. Recent acknowledgement window.",
    "not to send another message",
    "No repeated outreach without a real trigger.",
    "make route_owner_acknowledgement_follow_up_decision_memo",
]

FORBIDDEN_PHRASES = [
    "partner confirmed",
    "endorsement confirmed",
    "approval confirmed",
    "official role granted",
    "course approved",
    "patient data used",
    "clinical deployment ready",
    "clinical validation complete",
    "score certification complete",
    "application submitted",
    "proposal submitted",
    "payment completed",
    "terms accepted",
    "silence means rejection",
    "silence means support",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "claims_hospital_partner": False,
    "claims_university_partner": False,
    "claims_institutional_approval": False,
    "claims_endorsement": False,
    "claims_official_role": False,
    "claims_course_approval": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_ethics_approval": False,
    "claims_procurement_evidence": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_formal_application": False,
    "claims_proposal": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "allows_repeated_outreach_without_real_trigger": False,
}

EXPECTED_STATES = {
    "recent_acknowledgement_window",
    "one_concise_follow_up_after_real_trigger",
    "stop_and_do_not_follow_up",
    "substantive_reply_received",
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
    if payload.get("current_state") != "recent_acknowledgement_window":
        errors.append("Expected current_state recent_acknowledgement_window")
    if payload.get("checked_after_reading_baglam2") is not True:
        errors.append("Expected BAGLAM2 read flag")
    if payload.get("checked_after_reading_trackers") is not True:
        errors.append("Expected tracker read flag")
    if payload.get("checked_gmail_before_build") is not True:
        errors.append("Expected Gmail checked flag")
    if payload.get("gmail_reply_state") != "one acknowledgement remains no new substantive route reply":
        errors.append("Expected acknowledgement waiting Gmail state")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    states = payload.get("decision_states", [])
    if len(states) != 4:
        errors.append("Expected four decision states")
    state_names = {state.get("name") for state in states}
    if state_names != EXPECTED_STATES:
        errors.append("Decision state names do not match expected state set")
    for state in states:
        if not state.get("trigger"):
            errors.append(f"Decision state {state.get('name')} missing trigger")
        if not state.get("allowed_actions"):
            errors.append(f"Decision state {state.get('name')} missing allowed actions")
        if not state.get("blocked_actions"):
            errors.append(f"Decision state {state.get('name')} missing blocked actions")

    entry_points = payload.get("public_entry_points", [])
    if len(entry_points) != 4:
        errors.append("Expected four public entry points")
    for entry in entry_points:
        if not (ROOT / entry).exists():
            errors.append(f"Public entry point missing from tree: {entry}")

    if errors:
        print("FAIL route owner acknowledgement follow up decision memo validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS route owner acknowledgement follow up decision memo validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"decision_states={len(states)}")
    print(f"public_entry_points={len(entry_points)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
