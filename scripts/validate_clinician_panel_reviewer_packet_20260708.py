#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from failure_atlas.panel_review import load_panel_cases, load_rating_template, reviewer_codes

PACKET = ROOT / "docs" / "CLINICIAN_PANEL_REVIEWER_PACKET_20260708.md"
MESSAGE = ROOT / "docs" / "CLINICIAN_PANEL_REVIEWER_MESSAGE_20260708.md"
JSON_PATH = ROOT / "docs" / "clinician_panel_reviewer_packet_20260708.json"
AUDIT_NOTE = ROOT / "docs" / "CLINICIAN_PANEL_REVIEWER_AUDIT_NOTE_20260708.md"
CASES = ROOT / "data" / "panel_pilot" / "clinician_panel_pilot_cases_v0_1.tsv"
ASSIGNMENTS = ROOT / "data" / "panel_pilot" / "clinician_panel_rating_sheet_v0_1.tsv"

REQUIRED_PACKET_PHRASES = [
    "controlled local reviewer handoff",
    "Not an external publication",
    "The cases are synthetic",
    "The task is not clinical advice",
    "The review does not create clinical validation",
    "The review does not rank models",
    "The review does not test a live model endpoint",
    "Reviewer names are not public by default",
    "R01: 15 cases",
    "R02: 15 cases",
    "30 total review assignments",
    "Do not write public text that says the panel is complete",
]

REQUIRED_MESSAGE_PHRASES = [
    "Status: message draft. Not sent.",
    "gerçek hasta verisi değildir",
    "tanı veya tedavi önerisi istemiyorum",
    "reviewer code",
    "klinik validasyon, model sıralaması veya kurum onayı olarak sunulmayacak",
    "local review ekranını",
]

REQUIRED_AUDIT_PHRASES = [
    "Status: internal audit note. Not for reviewer package.",
    "Result: overall ok.",
    "External send status: blocked until G gives target and channel approval.",
    "Not cleared for sending yet.",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "model is safe",
    "best model",
    "deployment ready",
    "FDA approved",
    "FDA cleared",
    "officially endorsed",
    "official approval",
    "real patient data used",
    "panel validation complete",
    "panel review complete",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "synthetic_examples_only": True,
    "not_for_clinical_use": True,
    "no_clinical_validation_claim": True,
    "no_model_safety_claim": True,
    "no_model_ranking": True,
    "no_clinical_deployment_claim": True,
    "no_regulatory_approval_claim": True,
    "no_official_endorsement_claim": True,
    "external_send_allowed": False,
    "requires_owner_approval_before_send": True,
}


def main() -> int:
    errors: list[str] = []
    packet_text = read_text(PACKET, errors)
    message_text = read_text(MESSAGE, errors)
    audit_text = read_text(AUDIT_NOTE, errors)
    payload = read_json(JSON_PATH, errors)

    for phrase in REQUIRED_PACKET_PHRASES:
        if phrase.lower() not in packet_text.lower():
            errors.append(f"Missing packet phrase: {phrase}")
    for phrase in REQUIRED_MESSAGE_PHRASES:
        if phrase.lower() not in message_text.lower():
            errors.append(f"Missing message phrase: {phrase}")
    for phrase in REQUIRED_AUDIT_PHRASES:
        if phrase.lower() not in audit_text.lower():
            errors.append(f"Missing audit phrase: {phrase}")

    joined = "\n".join([packet_text, message_text, audit_text]).lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in joined:
            errors.append(f"Forbidden phrase present: {phrase}")

    if re.search(r"https?://", message_text):
        errors.append("Reviewer message must not contain a URL")
    absolute_user_path = "/" + "Users" + "/" + "goktugozkan"
    if absolute_user_path in joined:
        errors.append("Packet files must not expose an absolute local user path")

    cases = load_panel_cases(CASES)
    assignments = load_rating_template(ASSIGNMENTS)
    if len(cases) != 15:
        errors.append(f"Expected 15 panel cases, found {len(cases)}")
    if len(assignments) != 30:
        errors.append(f"Expected 30 review assignments, found {len(assignments)}")
    if reviewer_codes(assignments) != ["R01", "R02"]:
        errors.append(f"Expected reviewer codes R01/R02, found {reviewer_codes(assignments)}")

    if payload.get("packet_id") != "clinician_panel_reviewer_packet_20260708":
        errors.append("JSON packet_id must be clinician_panel_reviewer_packet_20260708")
    if payload.get("case_count") != len(cases):
        errors.append("JSON case_count must match panel cases")
    if payload.get("assignment_count") != len(assignments):
        errors.append("JSON assignment_count must match review assignments")
    if payload.get("reviewer_codes") != ["R01", "R02"]:
        errors.append("JSON reviewer_codes must be R01/R02")

    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON {key} must be {expected!r}")

    if errors:
        print("FAIL clinician panel reviewer packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS clinician panel reviewer packet validation")
    print(f"packet={PACKET.relative_to(ROOT)}")
    print(f"message={MESSAGE.relative_to(ROOT)}")
    print(f"audit={AUDIT_NOTE.relative_to(ROOT)}")
    return 0


def read_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def read_json(path: Path, errors: list[str]) -> dict[str, object]:
    if not path.exists():
        errors.append(f"Missing JSON: {path.relative_to(ROOT)}")
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON: {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"JSON root must be an object: {path.relative_to(ROOT)}")
        return {}
    return payload


if __name__ == "__main__":
    sys.exit(main())
