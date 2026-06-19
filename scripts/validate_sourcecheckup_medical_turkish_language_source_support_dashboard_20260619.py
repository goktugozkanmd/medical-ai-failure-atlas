#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SOURCECHECKUP_MEDICAL_TURKISH_LANGUAGE_SOURCE_SUPPORT_DASHBOARD_20260619.md"
DATA = ROOT / "docs" / "sourcecheckup_medical_turkish_language_source_support_dashboard_20260619.json"


REQUIRED_DOC_PHRASES = [
    "SourceCheckup Medical Turkish Language Source Support Dashboard",
    "public dashboard for Turkish language source support review",
    "No new route owner reply was found.",
    "prior Hacettepe acknowledgement remains the only reply",
    "Dashboard rows",
    "TLSS001",
    "TLSS002",
    "TLSS003",
    "TLSS004",
    "TLSS005",
    "TLSS006",
    "TLSS007",
    "TLSS008",
    "source support state",
    "Turkish wording risk",
    "data boundary",
    "reviewer route",
    "blocked public claim",
    "stop condition",
    "make sourcecheckup_medical_turkish_language_source_support_dashboard",
]

FORBIDDEN_PHRASES = [
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
    "clinical clearance confirmed",
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

REQUIRED_FIELDS = {
    "row id",
    "Turkish sentence under review",
    "English gloss",
    "source surface",
    "source support state",
    "Turkish wording risk",
    "clinical scope",
    "data boundary",
    "reviewer route",
    "evidence needed",
    "allowed public wording",
    "blocked public claim",
    "stop condition",
    "release state",
}

REQUIRED_ROUTES = {
    "source reviewer",
    "language reviewer",
    "clinician reviewer",
    "data steward",
    "governance reviewer",
    "benchmark reviewer",
    "maintainer release decision",
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
    if payload.get("gmail_reply_state") != "checked, no new route owner reply":
        errors.append("Expected checked no new route owner reply state")
    if payload.get("prior_acknowledgement_state") != "Hacettepe health informatics acknowledgement only":
        errors.append("Expected Hacettepe acknowledgement only state")
    if set(payload.get("active_thread_ids_checked", [])) != REQUIRED_THREADS:
        errors.append("Active thread ids checked do not match required set")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    row_ids = set(payload.get("dashboard_row_ids", []))
    if row_ids != {f"TLSS{index:03d}" for index in range(1, 9)}:
        errors.append("Expected eight dashboard row ids")
    if set(payload.get("required_fields", [])) != REQUIRED_FIELDS:
        errors.append("Required fields do not match required field set")
    if set(payload.get("reviewer_routes", [])) != REQUIRED_ROUTES:
        errors.append("Reviewer routes do not match required route set")
    if payload.get("next_public_action") != "SourceCheckup Turkish release gate row pack":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL SourceCheckup Medical Turkish language source support dashboard validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup Medical Turkish language source support dashboard validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"dashboard_rows={len(row_ids)}")
    print(f"reviewer_routes={len(REQUIRED_ROUTES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
