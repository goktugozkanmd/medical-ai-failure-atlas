#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDHELM_HEALTHBENCH_BRIDGE_COMPATIBILITY_NOTE_20260619.md"
DATA = ROOT / "docs" / "medhelm_healthbench_bridge_compatibility_note_20260619.json"

REQUIRED_DOC_PHRASES = [
    "MedHELM HealthBench BRIDGE Compatibility Note",
    "public compatibility note for benchmark aware medical AI safety work",
    "not an official MedHELM, OpenAI HealthBench, or BRIDGE statement",
    "not a benchmark result",
    "not a score report",
    "not a model comparison",
    "not a validation study",
    "not a medical device claim",
    "not a regulatory claim",
    "not a clinical recommendation",
    "not a route access claim",
    "121 clinical tasks",
    "22 subcategories",
    "31 datasets",
    "5 categories",
    "5000 realistic health conversations",
    "48562 unique rubric criteria",
    "avoid copying examples",
    "87 real world clinical text tasks",
    "9 languages",
    "more than one million samples",
    "regulated access clinical datasets cannot be directly published",
    "Failure mode complement",
    "Source support",
    "Clinician review",
    "No ranking public reporting",
    "Multilingual and Turkish readiness",
    "Specialty and care stage coverage",
    "Data quality and label audit",
    "Leakage and example protection",
    "Release boundary",
    "make medhelm_healthbench_bridge_compatibility_note",
]

REQUIRED_SOURCE_URLS = {
    "https://medhelm.org/",
    "https://openai.com/index/healthbench/",
    "https://github.com/YLab-Open/BRIDGE",
}

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "contains_healthbench_examples": False,
    "claims_official_compatibility": False,
    "claims_benchmark_submission": False,
    "claims_leaderboard_submission": False,
    "claims_model_ranking": False,
    "claims_benchmark_score": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_regulatory_evidence": False,
    "claims_medical_device_status": False,
}

FORBIDDEN_PHRASES = [
    "official compatibility confirmed",
    "benchmark submission complete",
    "leaderboard submission complete",
    "ranked models",
    "model ranking report",
    "score certification complete",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used",
    "partner confirmed",
    "official role confirmed",
    "endorsed by",
    "payment completed",
    "terms accepted",
    "regulatory evidence complete",
    "medical device cleared",
]

REQUIRED_LANES = {
    "Failure mode complement",
    "Source support",
    "Clinician review",
    "No ranking public reporting",
    "Multilingual and Turkish readiness",
    "Specialty and care stage coverage",
    "Data quality and label audit",
    "Leakage and example protection",
    "Release boundary",
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
    if payload.get("checked_after_reading_baglam2") is not True:
        errors.append("Expected BAGLAM2 read flag")
    if payload.get("checked_after_reading_trackers") is not True:
        errors.append("Expected tracker read flag")
    if payload.get("checked_gmail_before_build") is not True:
        errors.append("Expected Gmail checked flag")
    if payload.get("gmail_reply_state") != "no new route owner reply":
        errors.append("Expected no new route owner reply state")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    urls = {item.get("source_url") for item in payload.get("source_anchors", [])}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required benchmark source set")
    lanes = payload.get("compatibility_lanes", [])
    if len(lanes) != 9:
        errors.append("Expected nine compatibility lanes")
    found_lanes = {row.get("lane") for row in lanes}
    missing = sorted(REQUIRED_LANES - found_lanes)
    if missing:
        errors.append(f"Missing lanes: {', '.join(missing)}")
    for row in lanes:
        for field in ["public_artifact_question", "evidence_to_prepare", "blocked_claim"]:
            if not row.get(field):
                errors.append(f"{row.get('lane')}: missing {field}")

    if errors:
        print("FAIL MedHELM HealthBench BRIDGE compatibility note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS MedHELM HealthBench BRIDGE compatibility note validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"compatibility_lanes={len(lanes)}")
    print(f"source_anchors={len(urls)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
