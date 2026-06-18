#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "CURRENT_MEDICAL_AI_INTELLIGENCE_PRIORITY_UPDATE_20260618_V0_1.md"
DATA = ROOT / "docs" / "current_medical_ai_intelligence_priority_update_20260618_v0_1.json"


REQUIRED_SOURCE_IDS = [
    "CMIPU001",
    "CMIPU002",
    "CMIPU003",
    "CMIPU004",
    "CMIPU005",
    "CMIPU006",
    "CMIPU007",
    "CMIPU008",
]

REQUIRED_PRIORITY_IDS = [
    "CMIPUP001",
    "CMIPUP002",
    "CMIPUP003",
    "CMIPUP004",
    "CMIPUP005",
    "CMIPUP006",
]

REQUIRED_PHRASES = [
    "Current medical AI intelligence priority update v0.1",
    "Checked at: 2026 06 18 09:04 TRT.",
    "TÜBİTAK 1711 Yapay Zekâ Ekosistem 2026 announcement",
    "Ankara İl Sağlık Müdürlüğü AI studies ethics page",
    "Sağlık Bilgi Sistemleri Genel Müdürlüğü Yapay Zekâ ve Yenilikçi Teknolojiler Daire Başkanlığı page",
    "OpenAI HealthBench public page",
    "MedHELM public site",
    "Google MedGemma Health AI Developer Foundations page",
    "European Commission AI in healthcare page",
    "FDA AI Enabled Medical Devices page",
    "health is not listed among the five stated 2026 areas",
    "ethics status verification gate",
    "without claiming benchmark compatibility",
    "use cases require validation",
    "risk mitigation",
    "human oversight",
    "not devices",
    "Application window: 15 June 2026 to 18 September 2026, source page states 25:59 UTC plus 3",
    "Pre registration deadline: 14 September 2026 17:30",
    "Decision needed: Dr. Ozkan must decide whether to pursue a non medical pivot, partner route, or no action. Codex cannot submit or accept terms.",
    "make current_medical_ai_intelligence_priority_update",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "submission completed",
    "partner secured",
    "we have an official role",
    "official endorsement",
    "clinically validated",
    "validated for clinical use",
    "endpoint result available",
    "model ranking report completed",
    "score report published",
    "route access granted",
    "terms accepted",
    "payment made",
    "patient data used",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "not_for_clinical_use": True,
    "no_submission_claim": True,
    "no_application_claim": True,
    "no_partner_claim": True,
    "no_official_role_claim": True,
    "no_endorsement_claim": True,
    "no_clinical_validation_claim": True,
    "no_clinical_deployment_claim": True,
    "no_model_ranking": True,
    "no_score_report": True,
    "no_endpoint_call": True,
    "no_terms_acceptance": True,
    "no_payment": True,
}


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"Missing Markdown: {DOC.relative_to(ROOT)}")
        text = ""
    else:
        text = DOC.read_text(encoding="utf-8")
    if not DATA.exists():
        errors.append(f"Missing JSON: {DATA.relative_to(ROOT)}")
        payload: dict = {}
    else:
        payload = json.loads(DATA.read_text(encoding="utf-8"))

    if payload.get("source_row_count") != 8:
        errors.append("source row count must be 8")
    if payload.get("priority_row_count") != 6:
        errors.append("priority row count must be 6")
    if payload.get("real_opportunity_detected") is not True:
        errors.append("real opportunity must be detected")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"{key} must be {expected}")

    source_ids = [row.get("source_id") for row in payload.get("sources", [])]
    if source_ids != REQUIRED_SOURCE_IDS:
        errors.append("source ids must be CMIPU001 through CMIPU008")
    priority_ids = [row.get("priority_id") for row in payload.get("priority_updates", [])]
    if priority_ids != REQUIRED_PRIORITY_IDS:
        errors.append("priority ids must be CMIPUP001 through CMIPUP006")

    opportunity = payload.get("real_opportunity", {})
    if opportunity.get("pre_registration_deadline") != "14 September 2026 17:30":
        errors.append("pre registration deadline mismatch")
    if "18 September 2026" not in str(opportunity.get("application_window", "")):
        errors.append("application window must include 18 September 2026")
    if "partner commitment" not in str(opportunity.get("blocker", "")):
        errors.append("opportunity blocker must include partner commitment")

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Markdown must not contain hyphen characters")

    if errors:
        print("FAIL current medical AI intelligence priority update validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS current medical AI intelligence priority update validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_rows={payload['source_row_count']}")
    print(f"priority_rows={payload['priority_row_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
