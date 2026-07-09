#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / "docs" / "MEDFAILBENCH_SAFETY_ASSURANCE_CARD_V0_1.md"
CARD_JSON = ROOT / "docs" / "medfailbench_safety_assurance_card_v0_1.json"
SOURCE_NOTE = ROOT / "docs" / "MEDFAILBENCH_SAFETY_ASSURANCE_CARD_SOURCE_VERIFICATION_20260708.md"

REQUIRED_CARD_PHRASES = [
    "MedFailBench Safety Assurance Card v0.1",
    "Status: local build. Not externally released.",
    "Release gate level: L1 local build.",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not regulatory approval",
    "not official endorsement",
    "contains_patient_data: false",
    "identifiers_present: false",
    "synthetic_examples_only: true",
    "Current Evidence State",
    "Evidence Gaps",
    "Privacy And Data Boundary",
    "Source Lenses",
    "Risk Register",
    "Human Review State",
    "Release Gate",
    "Public Wording Allowed",
    "Public Wording Blocked",
    "External action status: blocked until fresh audit, source refresh, and owner approval.",
]

REQUIRED_SOURCE_PHRASES = [
    "Date checked: 2026 07 08",
    "NIST AI RMF",
    "https://www.nist.gov/itl/ai-risk-management-framework",
    "CHAI Applied Model Card",
    "https://www.chai.org/workgroup/applied-model",
    "FDA AI Device Lifecycle Draft Guidance",
    "not for implementation and contains non binding recommendations",
    "FDA PCCP Final Guidance",
    "WHO LMM Health Guidance",
    "ISBN 978-92-4-008475-9",
    "External use is blocked until",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "regulatory compliance",
    "FDA cleared",
    "FDA approved",
    "CHAI endorsed",
    "NIST compliant",
    "WHO endorsed",
    "official approval",
    "official acceptance",
    "institutional endorsement",
    "real patient data used",
    "model is safe",
    "best model",
    "MedHELM compatible",
    "HealthBench compatible",
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
    "no_regulatory_approval_claim": True,
    "no_official_endorsement_claim": True,
    "external_action_allowed": False,
}

REQUIRED_SECTIONS = {
    "intended_use",
    "non_use_boundary",
    "current_evidence_state",
    "evidence_gaps",
    "privacy_and_data_boundary",
    "source_lenses",
    "risk_register",
    "human_review_state",
    "release_gate",
    "public_wording_allowed",
    "public_wording_blocked",
    "audit_trail",
}

REQUIRED_SOURCE_IDS = {
    "nist_ai_rmf",
    "chai_applied_model_card",
    "fda_ai_device_lifecycle_draft",
    "fda_pccp_final_guidance",
    "who_lmm_health_guidance",
}


def main() -> int:
    errors: list[str] = []
    card_text = read_text(CARD, errors)
    source_text = read_text(SOURCE_NOTE, errors)
    json_payload = read_json(CARD_JSON, errors)

    lower_card = card_text.lower()
    joined_text = "\n".join([card_text, source_text]).lower()
    for phrase in REQUIRED_CARD_PHRASES:
        if phrase.lower() not in lower_card:
            errors.append(f"Missing card phrase: {phrase}")

    lower_source = source_text.lower()
    for phrase in REQUIRED_SOURCE_PHRASES:
        if phrase.lower() not in lower_source:
            errors.append(f"Missing source verification phrase: {phrase}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in joined_text:
            errors.append(f"Forbidden phrase present: {phrase}")

    if json_payload.get("card_id") != "medfailbench_safety_assurance_card_v0_1":
        errors.append("JSON card_id must be medfailbench_safety_assurance_card_v0_1")
    if json_payload.get("release_gate_level") != "L1":
        errors.append("JSON release_gate_level must be L1")

    for key, expected_value in REQUIRED_JSON_FLAGS.items():
        if json_payload.get(key) is not expected_value:
            errors.append(f"JSON {key} must be {expected_value!r}")

    current_evidence = json_payload.get("current_evidence", {})
    if not isinstance(current_evidence, dict):
        errors.append("JSON current_evidence must be an object")
    else:
        if current_evidence.get("failure_atlas_external_sample_rows") != 3:
            errors.append("JSON failure_atlas_external_sample_rows must be 3")
        if current_evidence.get("panel_case_count") != 15:
            errors.append("JSON panel_case_count must be 15")
        if current_evidence.get("panel_assignment_count") != 30:
            errors.append("JSON panel_assignment_count must be 30")
        if current_evidence.get("clinician_reviews_recorded") != 0:
            errors.append("JSON clinician_reviews_recorded must be 0 for this card")
        if current_evidence.get("raw_model_outputs_released") is not False:
            errors.append("JSON raw_model_outputs_released must be false")

    sections = set(json_payload.get("required_sections", []))
    missing_sections = REQUIRED_SECTIONS.difference(sections)
    if missing_sections:
        errors.append(f"JSON missing required sections: {sorted(missing_sections)}")

    anchors = json_payload.get("source_anchors", [])
    if not isinstance(anchors, list):
        errors.append("JSON source_anchors must be a list")
    else:
        anchor_ids = {item.get("source_id") for item in anchors if isinstance(item, dict)}
        missing_anchors = REQUIRED_SOURCE_IDS.difference(anchor_ids)
        if missing_anchors:
            errors.append(f"JSON missing source anchors: {sorted(missing_anchors)}")
        for item in anchors:
            if not isinstance(item, dict):
                errors.append("Every source anchor must be an object")
                continue
            if item.get("support_status") != "verified_from_official_page":
                errors.append(f"Source anchor {item.get('source_id')} must be verified_from_official_page")
            page = item.get("official_page", "")
            if not isinstance(page, str) or not page.startswith("https://"):
                errors.append(f"Source anchor {item.get('source_id')} must have an https official_page")

    gates = json_payload.get("release_gate_levels", [])
    if not isinstance(gates, list):
        errors.append("JSON release_gate_levels must be a list")
    else:
        gate_map = {item.get("level"): item for item in gates if isinstance(item, dict)}
        if gate_map.get("L1", {}).get("external_use") != "not_allowed_by_default":
            errors.append("JSON L1 external_use must be not_allowed_by_default")
        if gate_map.get("L5", {}).get("external_use") != "blocked_in_this_automation":
            errors.append("JSON L5 external_use must be blocked_in_this_automation")

    if errors:
        print("FAIL MedFailBench safety assurance card validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS MedFailBench safety assurance card validation")
    print(f"card={CARD.relative_to(ROOT)}")
    print(f"json={CARD_JSON.relative_to(ROOT)}")
    print(f"source_note={SOURCE_NOTE.relative_to(ROOT)}")
    return 0


def read_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def read_json(path: Path, errors: list[str]) -> dict[str, object]:
    if not path.exists():
        errors.append(f"Missing file: {path.relative_to(ROOT)}")
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON: {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"JSON root must be an object: {path.relative_to(ROOT)}")
        return {}
    return payload


if __name__ == "__main__":
    sys.exit(main())
