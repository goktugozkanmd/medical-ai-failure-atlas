#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BENCHMARK_LANGUAGE_REVIEWER_HANDOFF_CARD_20260619.md"
DATA = ROOT / "docs" / "benchmark_language_reviewer_handoff_card_20260619.json"

REQUIRED_DOC_PHRASES = [
    "Benchmark Language Reviewer Handoff Card",
    "public reviewer handoff card for benchmark based safety wording",
    "No Ranking Benchmark Misuse Warning",
    "not a benchmark result",
    "not model comparison",
    "not ranking",
    "not leaderboard",
    "not score certification",
    "not procurement evidence",
    "not clinical validation",
    "not clinical deployment",
    "not patient data",
    "not official compatibility",
    "Identify the proposed public sentence",
    "Name the benchmark surface",
    "Convert score language into task language",
    "Check the blocked claim list",
    "Request the evidence packet",
    "Protect examples and hidden test content",
    "Add the no ranking wording",
    "Allowed public wording",
    "Blocked public wording",
    "Minimum pass condition",
    "make benchmark_language_reviewer_handoff_card",
]

REQUIRED_SOURCE_URLS = {
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/124",
    "https://medhelm.org/",
    "https://openai.com/index/healthbench/",
    "https://github.com/YLab-Open/BRIDGE",
    "https://www.chai.org/workgroup/cross-cutting/ai-governance",
}

REQUIRED_FALSE_FLAGS = [
    "contains_patient_data",
    "contains_private_operational_data",
    "contains_healthbench_examples",
    "claims_benchmark_result",
    "claims_model_comparison",
    "claims_model_ranking",
    "claims_leaderboard_status",
    "claims_score_certification",
    "claims_procurement_evidence",
    "claims_clinical_validation",
    "claims_clinical_deployment",
    "claims_partner",
    "claims_official_role",
    "claims_endorsement",
    "claims_payment",
    "claims_terms_acceptance",
]

REQUIRED_STEPS = {
    "Identify the proposed public sentence",
    "Name the benchmark surface",
    "Convert score language into task language",
    "Check the blocked claim list",
    "Request the evidence packet",
    "Protect examples and hidden test content",
    "Add the no ranking wording",
}

FORBIDDEN_PHRASES = [
    "safety proof confirmed",
    "procurement readiness confirmed",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data cleared",
    "official compatibility confirmed",
    "leaderboard submission complete",
    "score certification complete",
    "partner confirmed",
    "official role confirmed",
    "endorsed by",
    "payment completed",
    "terms accepted",
]


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
    for key in REQUIRED_FALSE_FLAGS:
        if payload.get(key) is not False:
            errors.append(f"JSON flag {key} expected False")

    urls = {item.get("source_url") for item in payload.get("source_anchors", [])}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required source set")

    steps = payload.get("handoff_steps", [])
    if len(steps) != 7:
        errors.append("Expected seven handoff steps")
    found_steps = {row.get("step") for row in steps}
    missing = sorted(REQUIRED_STEPS - found_steps)
    if missing:
        errors.append(f"Missing handoff steps: {', '.join(missing)}")
    for row in steps:
        for field in ["reviewer_question", "required_record", "blocked_state"]:
            if not row.get(field):
                errors.append(f"{row.get('step')}: missing {field}")
        if len(row.get("required_record", [])) < 4:
            errors.append(f"{row.get('step')}: expected at least four required records")

    if errors:
        print("FAIL benchmark language reviewer handoff card validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS benchmark language reviewer handoff card validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"handoff_steps={len(steps)}")
    print(f"source_anchors={len(urls)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
