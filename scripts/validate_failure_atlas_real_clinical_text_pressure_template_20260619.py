#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "FAILURE_ATLAS_REAL_CLINICAL_TEXT_PRESSURE_TEMPLATE_20260619.md"
DATA = ROOT / "docs" / "failure_atlas_real_clinical_text_pressure_template_20260619.json"


REQUIRED_DOC_PHRASES = [
    "Failure Atlas Real Clinical Text Pressure Template",
    "public template for benchmark pressure around real clinical text",
    "No new route owner reply was found.",
    "BRIDGE",
    "87 tasks from 59 real world clinical data sources across 9 languages",
    "BRIDGE leaderboard surface",
    "No ranking, score, model standing, submission, compatibility, or benchmark result claim is made.",
    "MedHELM",
    "121 clinical tasks",
    "Template fields",
    "task type",
    "source type",
    "specialty",
    "document type",
    "care stage",
    "language and local context",
    "data boundary",
    "failure mechanism",
    "reviewer question",
    "evidence needed",
    "public wording allowed",
    "blocked public claim",
    "stop condition",
    "Example row skeleton",
    "Link benchmark adjacent notes back to issue #132",
    "make failure_atlas_real_clinical_text_pressure_template",
]

FORBIDDEN_PHRASES = [
    "bridge collaboration confirmed",
    "medhelm collaboration confirmed",
    "this is a benchmark result",
    "leaderboard rank",
    "model standing confirmed",
    "this is model ranking",
    "score certified",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data accessed",
    "regulated data accessed",
    "source truth certified",
    "this is procurement evidence",
    "partner confirmed",
    "institution approved",
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
    "claims_bridge_collaboration": False,
    "claims_medhelm_collaboration": False,
    "claims_benchmark_result": False,
    "claims_leaderboard_ranking": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_regulated_data_access": False,
    "claims_patient_data_clearance": False,
    "claims_procurement_evidence": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_endorsement": False,
}

REQUIRED_SOURCE_URLS = {
    "https://www.nature.com/articles/s41551-026-01719-2",
    "https://huggingface.co/spaces/YLab-Open/BRIDGE-Medical-Leaderboard",
    "https://medhelm.org/",
}

REQUIRED_TEMPLATE_FIELDS = {
    "row id",
    "task type",
    "source type",
    "specialty",
    "document type",
    "care stage",
    "language and local context",
    "data boundary",
    "failure mechanism",
    "reviewer question",
    "evidence needed",
    "public wording allowed",
    "blocked public claim",
    "stop condition",
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
    if payload.get("linked_issue") != 132:
        errors.append("Expected link to issue 132")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    signals = payload.get("source_signals", [])
    urls = {signal.get("source_url") for signal in signals}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required source set")
    if len(signals) != 3:
        errors.append("Expected three source signals")
    fields = set(payload.get("template_fields", []))
    if fields != REQUIRED_TEMPLATE_FIELDS:
        errors.append("Template fields do not match required field set")
    if len(payload.get("public_use_rules", [])) < 5:
        errors.append("Expected at least five public use rules")
    if payload.get("next_public_action") != "SourceCheckup Medical benchmark source support worksheet":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL Failure Atlas real clinical text pressure template validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Failure Atlas real clinical text pressure template validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(signals)}")
    print(f"template_fields={len(fields)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
