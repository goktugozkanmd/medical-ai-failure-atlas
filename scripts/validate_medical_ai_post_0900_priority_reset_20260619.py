#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_POST_0900_PRIORITY_RESET_20260619.md"
DATA = ROOT / "docs" / "medical_ai_post_0900_priority_reset_20260619.json"


REQUIRED_DOC_PHRASES = [
    "Medical AI Post 0900 Priority Reset",
    "public intelligence pass and priority reset after the first run past 09:00 Europe Istanbul",
    "No new route owner reply was found.",
    "TÜBİTAK 1711 2026",
    "15 June 2026 to 18 September 2026",
    "TÜSEB A4 UM",
    "30 June pre application cutoff",
    "TÜYZE health AI education and data route",
    "TEKNOFEST Sağlıkta Yapay Zeka",
    "29 June 2026 at 17:00",
    "Ministry health AI route signal",
    "EU AI Act sandbox and governance pressure",
    "CHAI governance signal",
    "MedHELM benchmark signal",
    "HealthBench signal",
    "BRIDGE signal",
    "Global Benchmark Pressure Response",
    "make medical_ai_post_0900_priority_reset",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "tbys submitted",
    "prodis submitted",
    "partner confirmed",
    "institution approved",
    "patient data used",
    "ethics approved",
    "clinical validation complete",
    "clinical deployment ready",
    "ranking certified",
    "score certified",
    "payment completed",
    "terms accepted",
    "endorsement secured",
]

REQUIRED_FLAGS = {
    "checked_after_0900_local": True,
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "claims_tubitak_application": False,
    "claims_tuseb_application": False,
    "claims_teknofest_submission": False,
    "claims_ministry_route": False,
    "claims_chai_affiliation": False,
    "claims_medhelm_collaboration": False,
    "claims_healthbench_collaboration": False,
    "claims_bridge_collaboration": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_ethics_approval": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_endorsement": False,
}

REQUIRED_SOURCE_URLS = {
    "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
    "https://www.tuseb.gov.tr/haberler/tuseb-2026-a4-um-uzman-mecburi-hizmet-grubuna-yonelik-proje-cagrisi-acildi-20260616",
    "https://tuyze.tuseb.gov.tr/",
    "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
    "https://sbsgm.saglik.gov.tr/TR-104172/yapay-zeka-ve-yenilikci-teknolojiler-daire-baskanligi.html",
    "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai",
    "https://www.chai.org/",
    "https://medhelm.org/",
    "https://openai.com/index/healthbench/",
    "https://www.nature.com/articles/s41551-026-01719-2",
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
        errors.append("Source URL set does not match required post 0900 source set")
    if len(signals) != 10:
        errors.append("Expected ten source signals")
    if len(payload.get("national_priority_order", [])) != 4:
        errors.append("Expected four national priority items")
    if len(payload.get("global_priority_order", [])) != 5:
        errors.append("Expected five global priority items")
    if payload.get("next_public_action") != "Global Benchmark Pressure Response":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL medical AI post 0900 priority reset validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS medical AI post 0900 priority reset validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(signals)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
