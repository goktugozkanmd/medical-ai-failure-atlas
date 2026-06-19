#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "HOSPITAL_AI_GOVERNANCE_INTAKE_WORKSHEET_20260619.md"
DATA = ROOT / "docs" / "hospital_ai_governance_intake_worksheet_20260619.json"

REQUIRED_DOC_PHRASES = [
    "Hospital AI Governance Intake Worksheet",
    "public intake worksheet for health AI governance readiness",
    "not CHAI affiliation",
    "not CHAI membership",
    "not CHAI partner status",
    "not CHAI endorsement",
    "not Joint Commission endorsement",
    "not certification",
    "not legal advice",
    "not regulatory evidence",
    "not clinical validation",
    "not clinical deployment",
    "not patient data clearance",
    "not procurement evidence",
    "not institutional adoption",
    "AI policy",
    "Organizational structures",
    "Organizational resources",
    "Responsible AI lifecycle management and use",
    "Risk and impact assessment",
    "Responsible data management and use",
    "Third party management",
    "Education, training, and feedback",
    "Public transparency and no ranking reporting",
    "Minimum pass condition",
    "Stop conditions",
    "make hospital_ai_governance_intake_worksheet",
]

REQUIRED_SOURCE_URLS = {
    "https://www.chai.org/",
    "https://www.chai.org/news/coalition-for-health-ai-chai-releases-comprehensive-governance-playbooks-to",
    "https://www.chai.org/workgroup/cross-cutting/ai-governance",
    "https://www.chai.org/workgroup/responsible-ai/responsible-ai-guide-raig-and-raig-executive-summary",
    "https://www.chai.org/blog/chai-releases-draft-responsible-health-ai-framework-for-public-comment",
}

REQUIRED_FALSE_FLAGS = [
    "contains_patient_data",
    "contains_private_operational_data",
    "claims_chai_affiliation",
    "claims_chai_membership",
    "claims_chai_partner",
    "claims_chai_endorsement",
    "claims_joint_commission_endorsement",
    "claims_certification",
    "claims_legal_advice",
    "claims_regulatory_evidence",
    "claims_clinical_validation",
    "claims_clinical_deployment",
    "claims_patient_data_clearance",
    "claims_procurement_evidence",
    "claims_institutional_adoption",
    "claims_model_ranking",
    "claims_score_certification",
    "claims_payment",
    "claims_terms_acceptance",
]

REQUIRED_LANES = {
    "AI policy",
    "Organizational structures",
    "Organizational resources",
    "Responsible AI lifecycle management and use",
    "Risk and impact assessment",
    "Responsible data management and use",
    "Third party management",
    "Education training and feedback",
    "Public transparency and no ranking reporting",
}

FORBIDDEN_PHRASES = [
    "chai affiliation confirmed",
    "chai membership confirmed",
    "chai partner confirmed",
    "endorsed by chai",
    "endorsed by joint commission",
    "certification complete",
    "legal advice provided",
    "regulatory evidence complete",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data cleared",
    "procurement evidence complete",
    "institutional adoption confirmed",
    "model ranking complete",
    "score certification complete",
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
        errors.append("Source URL set does not match required CHAI source set")

    lanes = payload.get("intake_lanes", [])
    if len(lanes) != 9:
        errors.append("Expected nine intake lanes")
    found_lanes = {row.get("lane") for row in lanes}
    missing = sorted(REQUIRED_LANES - found_lanes)
    if missing:
        errors.append(f"Missing lanes: {', '.join(missing)}")
    for row in lanes:
        for field in ["question", "records", "blocked_claim"]:
            if not row.get(field):
                errors.append(f"{row.get('lane')}: missing {field}")
        if len(row.get("records", [])) < 4:
            errors.append(f"{row.get('lane')}: expected at least four records")

    if errors:
        print("FAIL hospital AI governance intake worksheet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS hospital AI governance intake worksheet validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"intake_lanes={len(lanes)}")
    print(f"source_anchors={len(urls)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
