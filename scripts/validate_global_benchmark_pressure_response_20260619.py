#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "GLOBAL_BENCHMARK_PRESSURE_RESPONSE_20260619.md"
DATA = ROOT / "docs" / "global_benchmark_pressure_response_20260619.json"


REQUIRED_DOC_PHRASES = [
    "Global Benchmark Pressure Response",
    "public response to current global medical AI benchmark pressure",
    "No new route owner reply was found.",
    "BRIDGE",
    "87 tasks from 59 real world clinical data sources across 9 languages",
    "MedHELM",
    "121 clinical tasks",
    "HealthBench",
    "5000 realistic health conversations",
    "CHAI",
    "responsible development, deployment, and oversight of AI in healthcare",
    "EU AI Act",
    "risk assessment, high quality datasets, logging, documentation",
    "Failure Atlas real clinical text pressure",
    "SourceCheckup Medical source support pressure",
    "Turkish medical LLM coverage pressure",
    "Clinician review protocol pressure",
    "Health data quality and label audit pressure",
    "Governance and sandbox readiness pressure",
    "No ranking public reporting pressure",
    "Failure Atlas real clinical text pressure template",
    "make global_benchmark_pressure_response",
]

FORBIDDEN_PHRASES = [
    "bridge collaboration confirmed",
    "medhelm collaboration confirmed",
    "healthbench collaboration confirmed",
    "chai affiliation confirmed",
    "eu ai act compliant",
    "this is a benchmark result",
    "leaderboard rank",
    "this is model ranking",
    "score certified",
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
    "claims_bridge_collaboration": False,
    "claims_medhelm_collaboration": False,
    "claims_healthbench_collaboration": False,
    "claims_chai_affiliation": False,
    "claims_eu_ai_act_compliance": False,
    "claims_benchmark_result": False,
    "claims_leaderboard": False,
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
    "https://medhelm.org/",
    "https://openai.com/index/healthbench/",
    "https://www.chai.org/",
    "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai",
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
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    signals = payload.get("source_signals", [])
    urls = {signal.get("source_url") for signal in signals}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required global source set")
    if len(signals) != 5:
        errors.append("Expected five source signals")
    if len(payload.get("contribution_lanes", [])) != 7:
        errors.append("Expected seven contribution lanes")
    if len(payload.get("immediate_issue_queue", [])) != 7:
        errors.append("Expected seven immediate issue queue items")
    if payload.get("next_public_action") != "Failure Atlas real clinical text pressure template":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL global benchmark pressure response validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS global benchmark pressure response validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(signals)}")
    print(f"contribution_lanes={len(payload.get('contribution_lanes', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
