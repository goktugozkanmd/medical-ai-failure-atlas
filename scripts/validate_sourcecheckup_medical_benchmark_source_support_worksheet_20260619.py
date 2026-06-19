#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SOURCECHECKUP_MEDICAL_BENCHMARK_SOURCE_SUPPORT_WORKSHEET_20260619.md"
DATA = ROOT / "docs" / "sourcecheckup_medical_benchmark_source_support_worksheet_20260619.json"


REQUIRED_DOC_PHRASES = [
    "SourceCheckup Medical Benchmark Source Support Worksheet",
    "public worksheet for benchmark adjacent source support review",
    "No new route owner reply was found.",
    "BRIDGE",
    "87 tasks from 59 real world clinical data sources across 9 languages",
    "MedHELM",
    "121 clinical tasks",
    "HealthBench",
    "5000 realistic health conversations",
    "Worksheet fields",
    "claim id",
    "claim sentence",
    "source surface",
    "support state",
    "uncertainty state",
    "reviewer role",
    "evidence needed",
    "allowed public wording",
    "blocked public claim",
    "escalation route",
    "stop condition",
    "SCSW001",
    "SCSW002",
    "SCSW003",
    "SCSW004",
    "SCSW005",
    "SCSW006",
    "Link benchmark adjacent SourceCheckup work back to issues #132 and #133",
    "make sourcecheckup_medical_benchmark_source_support_worksheet",
]

FORBIDDEN_PHRASES = [
    "bridge collaboration confirmed",
    "medhelm collaboration confirmed",
    "healthbench collaboration confirmed",
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
    "claims_healthbench_collaboration": False,
    "claims_benchmark_result": False,
    "claims_leaderboard_ranking": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_source_truth_certification": False,
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
    "https://medhelm.org/",
    "https://openai.com/index/healthbench/",
}

REQUIRED_WORKSHEET_FIELDS = {
    "claim id",
    "claim sentence",
    "source surface",
    "support state",
    "uncertainty state",
    "reviewer role",
    "evidence needed",
    "allowed public wording",
    "blocked public claim",
    "escalation route",
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
    if payload.get("linked_issues") != [132, 133]:
        errors.append("Expected links to issues 132 and 133")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    signals = payload.get("source_signals", [])
    urls = {signal.get("source_url") for signal in signals}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required source set")
    if len(signals) != 3:
        errors.append("Expected three source signals")
    fields = set(payload.get("worksheet_fields", []))
    if fields != REQUIRED_WORKSHEET_FIELDS:
        errors.append("Worksheet fields do not match required field set")
    example_rows = set(payload.get("example_rows", []))
    if example_rows != {f"SCSW{index:03d}" for index in range(1, 7)}:
        errors.append("Expected six example rows")
    if len(payload.get("public_use_rules", [])) < 6:
        errors.append("Expected at least six public use rules")
    if payload.get("next_public_action") != "Turkish medical LLM coverage pressure addendum":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL SourceCheckup Medical benchmark source support worksheet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup Medical benchmark source support worksheet validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(signals)}")
    print(f"worksheet_fields={len(fields)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
