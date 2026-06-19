#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKISH_MEDICAL_LLM_ISSUE_TRIAGE_EXAMPLES_20260619.md"
DATA = ROOT / "docs" / "turkish_medical_llm_issue_triage_examples_20260619.json"


REQUIRED_DOC_PHRASES = [
    "Turkish Medical LLM Issue Triage Examples",
    "public triage examples for Turkish medical LLM issue routing",
    "No new route owner reply was found.",
    "Issue `#132`: Global Benchmark Pressure Response",
    "Issue `#133`: Failure Atlas Real Clinical Text Pressure Template",
    "Issue `#134`: SourceCheckup Medical Benchmark Source Support Worksheet",
    "Issue `#135`: Turkish Medical LLM Coverage Pressure Addendum",
    "Issue `#136`: Turkish Medical LLM Coverage Reviewer Intake Rows",
    "Issue `#137`: Turkish Medical LLM Reviewer Issue Template",
    "Example id: TMT001.",
    "Example id: TMT002.",
    "Example id: TMT003.",
    "Example id: TMT004.",
    "Example id: TMT005.",
    "Example id: TMT006.",
    "Turkish language only claim needs medical coverage review",
    "Translated patient education snippet needs language and clinician review",
    "Medication safety statement needs source support before public release",
    "Turkish abbreviation ambiguity needs language and clinician routing",
    "Benchmark adjacent claim needs no ranking boundary review",
    "Public route fit question needs governance boundary review",
    "make turkish_medical_llm_issue_triage_examples",
]

FORBIDDEN_PHRASES = [
    "turkish medical benchmark complete",
    "this is a benchmark result",
    "leaderboard rank",
    "model standing confirmed",
    "this is model ranking",
    "score certified",
    "source truth certified",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data accessed",
    "regulated data accessed",
    "partner confirmed",
    "institution approved",
    "formal application submitted",
    "payment completed",
    "terms accepted",
    "endorsement secured",
]

REQUIRED_FLAGS = {
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "checked_current_web_radar_after_0900_trt": True,
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "contains_benchmark_examples": False,
    "contains_answer_keys": False,
    "contains_hidden_prompts": False,
    "claims_turkish_medical_benchmark": False,
    "claims_benchmark_result": False,
    "claims_leaderboard_ranking": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_source_truth_certification": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_regulated_data_access": False,
    "claims_patient_data_clearance": False,
    "claims_institutional_approval": False,
    "claims_partner": False,
    "claims_formal_application": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_endorsement": False,
}

REQUIRED_FIELDS = {
    "Issue intent",
    "Linked context",
    "Turkish language state",
    "Medical scope",
    "Clinical context",
    "Source support",
    "Turkish terminology risk",
    "Clinician review question",
    "Data boundary",
    "Ranking boundary",
    "Public route fit",
    "Release decision",
    "Stop rule",
}

REQUIRED_ROUTES = {
    "language review",
    "clinician review",
    "source review",
    "data steward review",
    "governance review",
    "maintainer release decision",
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
    if payload.get("gmail_reply_state") != "no new route owner reply":
        errors.append("Expected no new route owner reply state")
    if payload.get("linked_issues") != [132, 133, 134, 135, 136, 137]:
        errors.append("Expected links to issues 132 through 137")
    if payload.get("example_ids") != ["TMT001", "TMT002", "TMT003", "TMT004", "TMT005", "TMT006"]:
        errors.append("Expected six ordered example ids")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    fields = set(payload.get("required_fields", []))
    if fields != REQUIRED_FIELDS:
        errors.append("Required fields do not match required field set")
    routes = set(payload.get("reviewer_routes", []))
    if routes != REQUIRED_ROUTES:
        errors.append("Reviewer routes do not match required route set")
    if payload.get("next_public_action") != "SourceCheckup Medical Turkish source support examples":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL Turkish medical LLM issue triage examples validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Turkish medical LLM issue triage examples validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"linked_issues={len(payload.get('linked_issues', []))}")
    print(f"examples={len(payload.get('example_ids', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
