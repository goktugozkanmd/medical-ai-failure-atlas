#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "HOSPITAL_AI_LITERACY_COLLABORATION_PACKET_20260619.md"
DATA = ROOT / "docs" / "hospital_ai_literacy_collaboration_packet_20260619.json"

REQUIRED_DOC_PHRASES = [
    "Hospital AI Literacy Collaboration Packet",
    "public one page route owner packet",
    "not a hospital partnership",
    "not an official course",
    "not accredited training",
    "not a clinical protocol",
    "not clinical validation",
    "not clinical deployment",
    "not patient data use",
    "not ethics approval",
    "not procurement evidence",
    "not model ranking",
    "not score certification",
    "not an application",
    "not a proposal",
    "not payment",
    "not terms acceptance",
    "Türkiye Clinical AI Assurance Lab Readiness Matrix",
    "Türkiye Clinician AI Safety Mini Curriculum",
    "Hospital AI Governance Intake Worksheet",
    "TÜSEB A4 UM notice",
    "TÜSEB A group call document",
    "TÜBİTAK 1711 2026 call notice",
    "Medical faculty education",
    "Hospital quality",
    "Health informatics",
    "Medical ethics",
    "Simulation education",
    "Health data governance",
    "Research coordination",
    "Not fit",
    "Thirty minute review route",
    "Minimum useful outcome",
    "Stop conditions",
    "TÜSEB A4 UM is time sensitive",
    "TÜBİTAK 1711 is larger and longer",
    "make hospital_ai_literacy_collaboration_packet",
]

REQUIRED_SOURCE_URLS = {
    "docs/TURKIYE_CLINICAL_AI_ASSURANCE_LAB_READINESS_MATRIX_20260619.md",
    "docs/TURKIYE_CLINICIAN_AI_SAFETY_MINI_CURRICULUM_20260618.md",
    "docs/HOSPITAL_AI_GOVERNANCE_INTAKE_WORKSHEET_20260619.md",
    "https://www.tuseb.gov.tr/haberler/tuseb-2026-a4-um-uzman-mecburi-hizmet-grubuna-yonelik-proje-cagrisi-acildi-20260616",
    "https://files.tuseb.gov.tr/tuseb/files/dokumanlar/tuseb-2026projecagrilari-agrubu.pdf",
    "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
}

REQUIRED_FALSE_FLAGS = [
    "contains_patient_data",
    "contains_private_operational_data",
    "claims_hospital_partner",
    "claims_official_course",
    "claims_accredited_training",
    "claims_clinical_protocol",
    "claims_clinical_validation",
    "claims_clinical_deployment",
    "claims_ethics_approval",
    "claims_procurement_evidence",
    "claims_model_ranking",
    "claims_score_certification",
    "claims_application",
    "claims_proposal",
    "claims_payment",
    "claims_terms_acceptance",
    "claims_official_role",
]

FORBIDDEN_PHRASES = [
    "hospital partner confirmed",
    "official course approved",
    "accredited training approved",
    "clinical protocol approved",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used",
    "ethics approval granted",
    "procurement evidence complete",
    "model ranking complete",
    "score certification complete",
    "application submitted",
    "proposal submitted",
    "payment completed",
    "terms accepted",
    "official role granted",
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
    if len(payload.get("possible_review_owners", [])) != 8:
        errors.append("Expected eight possible review owners")
    if len(payload.get("review_steps", [])) != 4:
        errors.append("Expected four review steps")
    if len(payload.get("review_objects", [])) != 4:
        errors.append("Expected four review objects")
    if len(payload.get("minimum_useful_outcomes", [])) != 5:
        errors.append("Expected five minimum useful outcomes")
    if len(payload.get("stop_conditions", [])) != 13:
        errors.append("Expected thirteen stop conditions")
    if payload.get("next_outward_action") != "if route owner reply appears map this packet to the reply and choose the smallest truthful follow up":
        errors.append("Unexpected next outward action")

    if errors:
        print("FAIL hospital AI literacy collaboration packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS hospital AI literacy collaboration packet validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_anchors={len(urls)}")
    print(f"review_owners={len(payload.get('possible_review_owners', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
