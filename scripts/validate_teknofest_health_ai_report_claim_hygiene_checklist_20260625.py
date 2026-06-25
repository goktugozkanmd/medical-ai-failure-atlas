#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TEKNOFEST_HEALTH_AI_REPORT_CLAIM_HYGIENE_CHECKLIST_20260625.md"
DATA = ROOT / "docs" / "teknofest_health_ai_report_claim_hygiene_checklist_20260625.json"

REQUIRED_DOC_PHRASES = [
    "TEKNOFEST Health AI report claim hygiene checklist",
    "project detail report deadline on 2026 06 29 at 17:00",
    "Gate 1. Scope lock",
    "Gate 2. Dataset meaning",
    "Gate 3. EKG classification language",
    "Gate 4. Variant prediction language",
    "Gate 5. Performance reporting",
    "Gate 6. Error analysis",
    "Gate 7. Human oversight",
    "Gate 8. User information",
    "Gate 9. Regulatory and device boundary",
    "Gate 10. Safer sentence patterns",
    "The model remains a competition prototype",
    "Any future clinical use would need separate data review",
    "No clinical validation claim appears",
    "validate_teknofest_health_ai_report_claim_hygiene_checklist_20260625.py",
]

FORBIDDEN_PHRASES = [
    "teknofest submitted",
    "official guide",
    "team member confirmed",
    "diagnoses patients",
    "ready for clinical use",
    "clinical validation complete",
    "clinical deployment ready",
    "patient benefit proven",
    "fda authorized",
    "ai act compliant",
    "device approved",
    "score certified",
    "clinician replacement",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_clinical_text": False,
    "claims_teknofest_submission": False,
    "claims_team_membership": False,
    "claims_official_guide": False,
    "claims_official_role": False,
    "claims_partner": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_medical_advice": False,
    "claims_diagnosis": False,
    "claims_treatment": False,
    "claims_patient_benefit": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_regulatory_approval": False,
    "claims_fda_authorization": False,
    "claims_ai_act_compliance": False,
    "claims_device_status": False,
    "claims_endorsement": False,
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
    if payload.get("source_url") != "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/":
        errors.append("Source URL mismatch")
    if len(payload.get("source_claims_checked", [])) != 4:
        errors.append("Expected four checked source claims")
    if len(payload.get("gates", [])) != 10:
        errors.append("Expected ten gates")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    if payload.get("safe_next_use") != "generic public checklist or internal report review aid":
        errors.append("Safe next use mismatch")

    if errors:
        print("FAIL TEKNOFEST health AI report claim hygiene checklist validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TEKNOFEST health AI report claim hygiene checklist validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"gates={len(payload.get('gates', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
