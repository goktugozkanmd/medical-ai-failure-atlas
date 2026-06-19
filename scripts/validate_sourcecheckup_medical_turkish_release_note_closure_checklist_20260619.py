#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SOURCECHECKUP_MEDICAL_TURKISH_RELEASE_NOTE_CLOSURE_CHECKLIST_20260619.md"
DATA = ROOT / "docs" / "sourcecheckup_medical_turkish_release_note_closure_checklist_20260619.json"


REQUIRED_DOC_PHRASES = [
    "SourceCheckup Medical Turkish Release Note Closure Checklist",
    "public closure checklist for Turkish release note review",
    "The only inbound reply remains the Hacettepe health informatics acknowledgement",
    "Allowed closure states",
    "RNC001",
    "RNC002",
    "RNC003",
    "RNC004",
    "RNC005",
    "RNC006",
    "RNC007",
    "RNC008",
    "RGR001",
    "RGR008",
    "RGO001",
    "RGO008",
    "source support closure",
    "Turkish wording closure",
    "clinical boundary closure",
    "data boundary closure",
    "benchmark boundary closure",
    "institution and partner closure",
    "release note language closure",
    "action boundary closure",
    "closed with public wording allowed",
    "unresolved and named in release note",
    "blocked before release",
    "not applicable and recorded",
    "make sourcecheckup_medical_turkish_release_note_closure_checklist",
]

FORBIDDEN_PHRASES = [
    "this is a benchmark result",
    "leaderboard rank",
    "model standing confirmed",
    "score is certified",
    "source truth is certified",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data accessed",
    "regulated data accessed",
    "procurement evidence confirmed",
    "partner is confirmed",
    "institution is approved",
    "payment completed",
    "terms are accepted",
    "endorsement secured",
    "clinical clearance confirmed",
    "application is submitted",
    "tbys submitted",
    "prodis submitted",
    "real patient",
    "real Turkish clinical sentence included",
]

REQUIRED_FLAGS = {
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "contains_real_turkish_clinical_sentence": False,
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "contains_benchmark_examples": False,
    "contains_answer_keys": False,
    "contains_hidden_prompts": False,
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
    "claims_email_action": False,
    "claims_formal_application": False,
    "claims_tbys_action": False,
    "claims_prodis_action": False,
}

REQUIRED_THREADS = {
    "19edcafe5c2dfa60",
    "19eda863ce89f083",
    "19edaa3a3868fd0f",
    "19edac07e13052fa",
    "19edb2e645ca1f6d",
    "19edb491af3d687b",
    "19edb64c4ae9fec6",
    "19edb8289b165cc0",
    "19edb9dc297ad804",
}

CLOSURE_IDS = {f"RNC{index:03d}" for index in range(1, 9)}
SOURCE_ROW_IDS = {f"RGR{index:03d}" for index in range(1, 9)}
OUTCOME_IDS = {f"RGO{index:03d}" for index in range(1, 9)}
CLOSURE_STATES = {
    "closed with public wording allowed",
    "unresolved and named in release note",
    "blocked before release",
    "not applicable and recorded",
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
    if "prior Hacettepe health informatics acknowledgement" not in payload.get("gmail_reply_state", ""):
        errors.append("Expected prior Hacettepe acknowledgement state")
    if set(payload.get("active_thread_ids_checked", [])) != REQUIRED_THREADS:
        errors.append("Active thread ids checked do not match required set")
    if len(payload.get("targeted_gmail_searches_checked", [])) != 5:
        errors.append("Expected five targeted Gmail searches")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    if set(payload.get("closure_ids", [])) != CLOSURE_IDS:
        errors.append("Expected eight release note closure ids")
    if set(payload.get("linked_source_row_ids", [])) != SOURCE_ROW_IDS:
        errors.append("Expected eight source row ids")
    if set(payload.get("linked_outcome_ids", [])) != OUTCOME_IDS:
        errors.append("Expected eight outcome ids")
    if set(payload.get("closure_states", [])) != CLOSURE_STATES:
        errors.append("Closure states do not match required set")
    if payload.get("next_public_action") != "SourceCheckup Turkish maintainer handoff digest":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL SourceCheckup Medical Turkish release note closure checklist validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup Medical Turkish release note closure checklist validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"closures={len(CLOSURE_IDS)}")
    print(f"closure_states={len(CLOSURE_STATES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
