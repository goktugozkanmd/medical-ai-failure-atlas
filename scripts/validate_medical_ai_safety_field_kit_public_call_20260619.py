#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_CALL_20260619.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_public_call_20260619.json"
ISSUE_BODY = ROOT / "outputs" / "medical_ai_safety_field_kit_public_call_issue_body_20260619.md"
RELEASE_NOTES = ROOT / "outputs" / "medical_ai_safety_field_kit_public_call_release_notes_20260619.md"
PUBLIC_POST_SEED = ROOT / "outputs" / "medical_ai_safety_field_kit_public_call_public_post_seed_20260619.md"


REQUIRED_DOC_PHRASES = [
    "Medical AI Safety Field Kit Public Call",
    "public flagship call for clinical and technical reviewers",
    "This is the public front door for the Medical AI Safety Field Kit",
    "Medical AI projects should not ask for trust",
    "This call asks the field to attack those weak points in public",
    "TR MedLLM SafetyBench",
    "Medical AI Failure Atlas Global",
    "Turkish Clinical AI Assurance Lab",
    "SourceCheckup Medical",
    "Clinician AI Literacy Academy Turkiye",
    "Health Data Quality and Label Audit Commons",
    "Reviewer roles we want now",
    "How to contribute in public",
    "Live BAGLAM2, portfolio trackers, active Gmail outreach threads, and targeted Gmail searches were checked",
    "make medical_ai_safety_field_kit_public_call",
]

REQUIRED_ISSUE_PHRASES = [
    "Medical AI Safety Field Kit Public Call",
    "The ask is direct",
    "Useful comments",
    "Role:",
    "Lane:",
    "Concern:",
    "Suggested fix:",
    "Boundary: this is not clinical validation",
    "make medical_ai_safety_field_kit_public_call",
]

REQUIRED_RELEASE_PHRASES = [
    "Medical AI Safety Field Kit Public Call",
    "flagship public call",
    "six platform lanes",
    "twenty minutes",
    "Boundary: no patient data",
]

FORBIDDEN_PHRASES = [
    "patient data used",
    "real patient",
    "provides diagnosis advice",
    "provides treatment advice",
    "gives diagnosis advice",
    "gives treatment advice",
    "clinically validated",
    "clinical deployment ready",
    "benchmark ranking confirmed",
    "score certified",
    "source truth certified",
    "partner confirmed",
    "institution approved",
    "endorsed by",
    "formal application submitted",
    "payment completed",
    "terms accepted",
    "official guidance",
    "compliance certified",
]

FORBIDDEN_INTERNAL_LABELS = [
    "de" + "AI",
    "human" + "ized",
    "AI " + "detector",
    "submit" + "_audit",
]

REQUIRED_FLAGS = {
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "contains_patient_data": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_diagnosis_or_treatment_advice": False,
    "claims_benchmark_ranking": False,
    "claims_score_certification": False,
    "claims_source_truth_certification": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_endorsement": False,
    "claims_formal_application": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
}

REQUIRED_THREADS = {
    "19edcafe5c2dfa60",
    "19eda863ce89f083",
    "19edaa3a3868fd0f",
    "19edac07e13052fa",
    "19edb2e645ca1f6d",
    "19edb491af3d687b",
    "19edb64c4ae9fec6",
    "19edb8289b165cc0",
    "19edb9dc297ad804",
}

REQUIRED_PLATFORM_IDS = {f"FK{index:03d}" for index in range(1, 7)}
REQUIRED_ROLE_IDS = {f"R{index:03d}" for index in range(1, 7)}


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def add_text_checks(errors: list[str], label: str, text: str) -> None:
    lower_text = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains forbidden phrase: {phrase}")
    for phrase in FORBIDDEN_INTERNAL_LABELS:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains internal process label: {phrase}")
    if "-" in text_without_urls(text):
        errors.append(f"{label} contains non URL hyphen character")


def main() -> int:
    errors: list[str] = []
    for path in [DOC, DATA, ISSUE_BODY, RELEASE_NOTES, PUBLIC_POST_SEED]:
        if not path.exists():
            errors.append(f"Missing artifact: {path.relative_to(ROOT)}")

    doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    issue_text = ISSUE_BODY.read_text(encoding="utf-8") if ISSUE_BODY.exists() else ""
    release_text = RELEASE_NOTES.read_text(encoding="utf-8") if RELEASE_NOTES.exists() else ""
    post_text = PUBLIC_POST_SEED.read_text(encoding="utf-8") if PUBLIC_POST_SEED.exists() else ""

    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in doc_text.lower():
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in REQUIRED_ISSUE_PHRASES:
        if phrase.lower() not in issue_text.lower():
            errors.append(f"Issue body missing required phrase: {phrase}")
    for phrase in REQUIRED_RELEASE_PHRASES:
        if phrase.lower() not in release_text.lower():
            errors.append(f"Release notes missing required phrase: {phrase}")

    add_text_checks(errors, "Doc", doc_text)
    add_text_checks(errors, "Issue body", issue_text)
    add_text_checks(errors, "Release notes", release_text)
    add_text_checks(errors, "Public post seed", post_text)

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    if payload.get("platform_count") != 6 or set(payload.get("platform_ids", [])) != REQUIRED_PLATFORM_IDS:
        errors.append("Expected six platform ids")
    if payload.get("review_role_count") != 6 or set(payload.get("review_role_ids", [])) != REQUIRED_ROLE_IDS:
        errors.append("Expected six review role ids")
    if payload.get("boundary_count") != 12:
        errors.append("Expected twelve boundaries")

    gmail_check = payload.get("gmail_check", {})
    if set(gmail_check.get("active_thread_ids_checked", [])) != REQUIRED_THREADS:
        errors.append("Active thread ids checked do not match required set")
    if len(gmail_check.get("targeted_searches_checked", [])) != 5:
        errors.append("Expected five targeted Gmail searches")
    if "No new substantive route owner reply" not in gmail_check.get("reply_state", ""):
        errors.append("Gmail reply state must state no new substantive route owner reply")

    if errors:
        print("FAIL Medical AI Safety Field Kit public call validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Medical AI Safety Field Kit public call validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"issue_body={ISSUE_BODY.relative_to(ROOT)}")
    print(f"release_notes={RELEASE_NOTES.relative_to(ROOT)}")
    print(f"public_post_seed={PUBLIC_POST_SEED.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
