#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / "docs" / "ASSURANCE_CARD_TEMPLATE_V0_1.md"
CARD_JSON = ROOT / "docs" / "assurance_card_template_v0_1.json"

REQUIRED_PHRASES = [
    "medical language model assurance card template",
    "pre release assurance card",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not regulatory approval",
    "not official endorsement",
    "patient_data_present must be false for this public example",
    "identifiers_present must be false for this public example",
    "Synthetic examples only",
    "Any real patient data route is blocked in this automation",
    "Model card",
    "Risk card",
    "Data card",
    "Source support card",
    "Human review card",
    "Audit trail",
    "SourceCheckup Medical",
    "Health data quality and label audit card",
    "MedHELM and Medmarks boundary notes",
    "Clinician review protocol",
    "L5 clinical deployment is blocked in this automation",
    "release_gate_level L1",
    "make assurance_card_template",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "regulatory compliance",
    "official approval",
    "official acceptance",
    "sandbox access granted",
    "institutional endorsement",
    "real patient data used",
    "model is safe",
    "best model",
]

REQUIRED_JSON_FLAGS = {
    "contains_patient_data": False,
    "identifiers_present": False,
    "synthetic_examples_only": True,
    "not_for_clinical_use": True,
    "no_clinical_deployment_claim": True,
    "no_clinical_validation_claim": True,
    "no_model_safety_claim": True,
    "no_model_ranking": True,
    "no_official_endorsement_claim": True,
}

REQUIRED_SECTIONS = {
    "card_identity",
    "model_card",
    "patient_data_and_privacy_boundary",
    "risk_card",
    "data_card",
    "source_support_card",
    "human_review_card",
    "audit_trail",
    "release_gate_levels",
    "public_action_checklist",
}


def main() -> int:
    errors: list[str] = []
    if not CARD.exists():
        errors.append(f"Missing card: {CARD.relative_to(ROOT)}")
        text = ""
    else:
        text = CARD.read_text(encoding="utf-8")

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")

    if not CARD_JSON.exists():
        errors.append(f"Missing JSON companion: {CARD_JSON.relative_to(ROOT)}")
        card_json: dict[str, object] = {}
    else:
        try:
            card_json = json.loads(CARD_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON companion: {exc}")
            card_json = {}

    if card_json.get("card_id") != "assurance_card_template_v0_1":
        errors.append("JSON card_id must be assurance_card_template_v0_1")
    if card_json.get("release_gate_level") != "L1":
        errors.append("JSON release_gate_level must be L1")

    for key, expected_value in REQUIRED_JSON_FLAGS.items():
        if card_json.get(key) is not expected_value:
            errors.append(f"JSON {key} must be {expected_value!r}")

    sections = set(card_json.get("required_sections", []))
    missing_sections = REQUIRED_SECTIONS.difference(sections)
    if missing_sections:
        errors.append(f"JSON missing required sections: {sorted(missing_sections)}")

    gate_levels = card_json.get("release_gate_levels", [])
    if not isinstance(gate_levels, list):
        errors.append("JSON release_gate_levels must be a list")
    else:
        level_map = {item.get("level"): item for item in gate_levels if isinstance(item, dict)}
        for level in ["L0", "L1", "L2", "L3", "L4", "L5"]:
            if level not in level_map:
                errors.append(f"JSON missing release gate level {level}")
        if level_map.get("L5", {}).get("external_use") != "blocked_in_this_automation":
            errors.append("JSON L5 external_use must be blocked_in_this_automation")

    if errors:
        print("FAIL assurance card template validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS assurance card template validation")
    print(f"card={CARD.relative_to(ROOT)}")
    print(f"json={CARD_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
