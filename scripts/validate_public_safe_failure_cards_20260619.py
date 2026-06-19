#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "PUBLIC_SAFE_FAILURE_CARDS_20260619.md"
DATA = ROOT / "docs" / "public_safe_failure_cards_20260619.json"
LAUNCH_SEED = ROOT / "docs" / "PUBLIC_SAFE_FAILURE_CARDS_LAUNCH_SEED_20260619.md"

REQUIRED_DOC_PHRASES = [
    "Public Safe Failure Cards",
    "public synthetic card pack for reviewer attack",
    "make weak safety language easy to attack before it becomes trusted public wording",
    "no patient data",
    "no clinical advice",
    "no clinical validation",
    "no clinical deployment",
    "no benchmark ranking",
    "no score certification",
    "no source truth certification",
    "Benchmark score becomes safety proof",
    "Source link becomes source support",
    "Turkish wording sounds fluent but shifts risk",
    "Demo success becomes hospital readiness",
    "Synthetic card becomes real case evidence",
    "Policy wording becomes clinical instruction",
    "Public dataset means data fitness",
    "Human review role is missing",
    "Vendor language becomes medical assurance",
    "Sandbox route becomes deployment readiness",
    "make public_safe_failure_cards",
]

REQUIRED_LAUNCH_PHRASES = [
    "Public Safe Failure Cards launch seed",
    "pick one card and attack the unsafe wording",
    "Role:",
    "Lane:",
    "Card id:",
    "Risk:",
    "Missing gate:",
    "Safer wording:",
]

FORBIDDEN_PHRASES = [
    "patient data used",
    "real patient",
    "clinical advice provided",
    "clinically validated",
    "clinical deployment ready",
    "benchmark ranking confirmed",
    "score certified",
    "source truth certified",
    "partner confirmed",
    "institution approved",
    "endorsed by",
    "formal application submitted",
    "payment completed",
    "terms accepted",
    "official guidance",
    "compliance certified",
]

FORBIDDEN_INTERNAL_LABELS = [
    "de" + "AI",
    "human" + "ized",
    "AI " + "detector",
    "submit" + "_audit",
]

REQUIRED_FLAGS = {
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "contains_patient_data": False,
    "claims_clinical_advice": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_benchmark_ranking": False,
    "claims_score_certification": False,
    "claims_source_truth_certification": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_endorsement": False,
    "claims_formal_application": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
}

REQUIRED_THREADS = {
    "19eda863ce89f083",
    "19edaa3a3868fd0f",
    "19edac07e13052fa",
    "19edcafe5c2dfa60",
    "19edb2e645ca1f6d",
    "19edb491af3d687b",
    "19edb64c4ae9fec6",
    "19edb8289b165cc0",
    "19edb9dc297ad804",
    "19ee10ad385519d5",
    "19ee125893972e6d",
    "19edb48f891326e3",
}

REQUIRED_CARD_IDS = {f"SFC{index:03d}" for index in range(1, 11)}
REQUIRED_PATTERNS = {
    "Benchmark score becomes safety proof",
    "Source link becomes source support",
    "Turkish wording sounds fluent but shifts risk",
    "Demo success becomes hospital readiness",
    "Synthetic card becomes real case evidence",
    "Policy wording becomes clinical instruction",
    "Public dataset means data fitness",
    "Human review role is missing",
    "Vendor language becomes medical assurance",
    "Sandbox route becomes deployment readiness",
}


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def add_text_checks(errors: list[str], label: str, text: str) -> None:
    lower_text = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains forbidden phrase: {phrase}")
    for phrase in FORBIDDEN_INTERNAL_LABELS:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains internal process label: {phrase}")
    if "-" in text_without_urls(text):
        errors.append(f"{label} contains non URL hyphen character")


def main() -> int:
    errors: list[str] = []
    for path in [DOC, DATA, LAUNCH_SEED]:
        if not path.exists():
            errors.append(f"Missing artifact: {path.relative_to(ROOT)}")

    doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    launch_text = LAUNCH_SEED.read_text(encoding="utf-8") if LAUNCH_SEED.exists() else ""
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in doc_text.lower():
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in REQUIRED_LAUNCH_PHRASES:
        if phrase.lower() not in launch_text.lower():
            errors.append(f"Launch seed missing required phrase: {phrase}")
    add_text_checks(errors, "Doc", doc_text)
    add_text_checks(errors, "Launch seed", launch_text)

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    if payload.get("card_count") != 10:
        errors.append("Expected ten cards")
    if set(payload.get("active_thread_ids_checked", [])) != REQUIRED_THREADS:
        errors.append("Active thread ids checked do not match required set")
    if payload.get("targeted_search_count") != 4:
        errors.append("Expected four targeted Gmail search groups")
    if "No new substantive medical AI reply required action" not in payload.get("gmail_reply_state", ""):
        errors.append("Gmail reply state missing no action required language")

    cards = payload.get("cards", [])
    if {card.get("card_id") for card in cards} != REQUIRED_CARD_IDS:
        errors.append("Card ids do not match expected set")
    if {card.get("unsafe_pattern") for card in cards} != REQUIRED_PATTERNS:
        errors.append("Unsafe pattern set does not match expected set")
    for card in cards:
        for field in ["platform_lane", "unsafe_pattern", "reviewer_check", "stop_condition"]:
            if not card.get(field):
                errors.append(f"{card.get('card_id')}: missing {field}")

    if errors:
        print("FAIL public safe failure cards validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS public safe failure cards validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"launch_seed={LAUNCH_SEED.relative_to(ROOT)}")
    print(f"cards={len(cards)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
