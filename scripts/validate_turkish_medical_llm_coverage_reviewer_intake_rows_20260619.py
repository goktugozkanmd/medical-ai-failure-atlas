#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKISH_MEDICAL_LLM_COVERAGE_REVIEWER_INTAKE_ROWS_20260619.md"
DATA = ROOT / "docs" / "turkish_medical_llm_coverage_reviewer_intake_rows_20260619.json"


REQUIRED_DOC_PHRASES = [
    "Turkish Medical LLM Coverage Reviewer Intake Rows",
    "public reviewer intake rows for Turkish medical LLM coverage review",
    "No new route owner reply was found.",
    "BRIDGE",
    "87 tasks from 59 real world clinical data sources across 9 languages",
    "HealthBench",
    "5000 realistic health conversations",
    "TurkBench",
    "8151 data samples across 21 subtasks",
    "Turkish MMLU article",
    "Turkish morphology and syntax create evaluation challenges",
    "TMI001",
    "TMI002",
    "TMI003",
    "TMI004",
    "TMI005",
    "TMI006",
    "TMI007",
    "TMI008",
    "TMI009",
    "TMI010",
    "Link these rows to issues `#132`, `#133`, `#134`, and `#135`",
    "make turkish_medical_llm_coverage_reviewer_intake_rows",
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

REQUIRED_SOURCE_URLS = {
    "https://www.nature.com/articles/s41551-026-01719-2",
    "https://openai.com/tr-TR/index/healthbench/",
    "https://arxiv.org/html/2601.07020v1",
    "https://arxiv.org/html/2508.13044v1",
}

REQUIRED_OUTPUT_FIELDS = {
    "Language state",
    "Medical scope",
    "Clinical context",
    "Source support state",
    "Terminology risk",
    "Clinician review question",
    "Data boundary",
    "Ranking boundary",
    "Public route fit",
    "Release decision",
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
    if payload.get("linked_issues") != [132, 133, 134, 135]:
        errors.append("Expected links to issues 132, 133, 134, and 135")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    signals = payload.get("source_signals", [])
    urls = {signal.get("source_url") for signal in signals}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required source set")
    if len(signals) != 4:
        errors.append("Expected four source signals")
    intake_rows = set(payload.get("intake_rows", []))
    if intake_rows != {f"TMI{index:03d}" for index in range(1, 11)}:
        errors.append("Expected ten intake rows")
    output_fields = set(payload.get("output_fields", []))
    if output_fields != REQUIRED_OUTPUT_FIELDS:
        errors.append("Output fields do not match required field set")
    if len(payload.get("reviewer_roles", [])) < 6:
        errors.append("Expected at least six reviewer roles")
    if payload.get("next_public_action") != "Turkish medical LLM reviewer intake issue template":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL Turkish medical LLM coverage reviewer intake rows validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Turkish medical LLM coverage reviewer intake rows validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(signals)}")
    print(f"intake_rows={len(intake_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
