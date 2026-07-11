#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "EU_AI_ACT_HEALTH_AI_SANDBOX_READINESS_CROSSWALK_20260619.md"
DATA = ROOT / "docs" / "eu_ai_act_health_ai_sandbox_readiness_crosswalk_20260619.json"

REQUIRED_DOC_PHRASES = [
    "EU AI Act Health AI Sandbox Readiness Crosswalk",
    "public readiness crosswalk for medical AI safety infrastructure",
    "not legal advice",
    "not an EU sandbox application",
    "not a regulatory submission",
    "not a conformity assessment",
    "not a CE marking claim",
    "not a medical device claim",
    "AI literacy obligations entered into application on 2 February 2025",
    "general purpose AI models became applicable on 2 August 2025",
    "generally applicable on 2 August 2026",
    "systems used in certain high risk areas will apply from 2 December 2027",
    "systems integrated into products will apply from 2 August 2028",
    "risk management, data quality, documentation and traceability, transparency, human oversight, accuracy, robustness",
    "medical treatment assessment as an example of a high risk use case",
    "AI regulatory sandboxes provide a controlled environment",
    "Intended use",
    "AI literacy",
    "Risk management",
    "Data quality",
    "Documentation",
    "Transparency",
    "Human oversight",
    "Robustness",
    "Data and operational boundary",
    "Monitoring",
    "Incident handling",
    "Sandbox route",
    "make eu_ai_act_health_ai_sandbox_readiness_crosswalk",
]

REQUIRED_SOURCE_URLS = {
    "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai",
    "https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act",
    "https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-57",
}

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "claims_legal_advice": False,
    "claims_eu_sandbox_application": False,
    "claims_regulatory_submission": False,
    "claims_conformity_assessment": False,
    "claims_ce_marking": False,
    "claims_medical_device_status": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
}

FORBIDDEN_PHRASES = [
    "legal advice provided",
    "sandbox application submitted",
    "sandbox access granted",
    "regulatory submission complete",
    "conformity assessment complete",
    "ce marked",
    "medical device cleared",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used",
    "partner confirmed",
    "official role confirmed",
    "endorsed by",
    "payment completed",
    "terms accepted",
    "model ranking report",
    "score certification complete",
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
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    urls = {item.get("source_url") for item in payload.get("source_anchors", [])}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required EU AI Act source set")
    rows = payload.get("crosswalk_rows", [])
    if len(rows) != 12:
        errors.append("Expected twelve crosswalk rows")
    required_domains = {
        "Intended use",
        "AI literacy",
        "Risk management",
        "Data quality",
        "Documentation",
        "Transparency",
        "Human oversight",
        "Robustness",
        "Data and operational boundary",
        "Monitoring",
        "Incident handling",
        "Sandbox route",
    }
    found_domains = {row.get("domain") for row in rows}
    missing = sorted(required_domains - found_domains)
    if missing:
        errors.append(f"Missing domains: {', '.join(missing)}")
    for row in rows:
        for field in ["public_artifact_question", "evidence_to_prepare", "blocked_claim"]:
            if not row.get(field):
                errors.append(f"{row.get('domain')}: missing {field}")

    if errors:
        print("FAIL EU AI Act health AI sandbox readiness crosswalk validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS EU AI Act health AI sandbox readiness crosswalk validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"crosswalk_rows={len(rows)}")
    print(f"source_anchors={len(urls)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
