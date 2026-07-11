#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_assurance_kit_card_20260708.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md"

EXPECTED_LAYER_IDS = [
    "safety_evidence_spine",
    "safetyguard_studio_surface",
    "source_support_layer",
    "turkish_drift_layer",
    "transparency_card_layer",
    "human_review_status_layer",
    "clinician_literacy_layer",
    "monitoring_boundary_layer",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "source truth certified",
    "regulatory compliance achieved",
    "officially compatible",
    "patient data used",
    "agent selected physicians",
    "best model",
    "model winner",
]


def main() -> int:
    errors: list[str] = []
    for path in [JSON_PATH, MD_PATH]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    manifest = read_json(JSON_PATH, errors)
    if manifest:
        expected_flags = {
            "external_action_allowed": False,
            "provider_api_call_allowed": False,
            "automation_started": False,
            "new_cases_added": False,
            "agent_selected_physicians": False,
            "contains_patient_data": False,
            "no_clinical_validation_claim": True,
            "no_source_truth_certification_claim": True,
            "no_model_ranking": True,
            "no_regulatory_compliance_claim": True,
            "no_official_compatibility_claim": True,
        }
        for key, expected in expected_flags.items():
            if manifest.get(key) is not expected:
                errors.append(f"Kit card {key} must be {expected!r}")
        if manifest.get("status") != "local_kit_level_assurance_card_ready":
            errors.append("Kit card status mismatch")
        if manifest.get("phase") != "P5":
            errors.append("Kit card phase must be P5")
        if manifest.get("product_name") != "Clinical AI Safety Ops / Health AI Assurance Kit":
            errors.append("Kit card product_name mismatch")
        if manifest.get("card_schema") != "health_ai_assurance_kit_card_v0_1":
            errors.append("Kit card schema mismatch")

        source_artifacts = manifest.get("source_artifacts", {})
        if not isinstance(source_artifacts, dict) or len(source_artifacts) != 9:
            errors.append("Kit card must list nine source artifacts")
            source_artifacts = {}
        for label, relative in source_artifacts.items():
            if not (ROOT / str(relative)).exists():
                errors.append(f"Kit card source artifact missing for {label}: {relative}")

        layers = manifest.get("evidence_layers", [])
        layer_ids = [str(layer.get("id")) for layer in layers if isinstance(layer, dict)]
        if layer_ids != EXPECTED_LAYER_IDS:
            errors.append(f"Kit card layer order mismatch: {layer_ids!r}")
        for layer in layers if isinstance(layers, list) else []:
            if not layer.get("source") or not (ROOT / str(layer.get("source"))).exists():
                errors.append(f"Kit card layer source missing: {layer.get('id')}")
            if not isinstance(layer.get("signals"), dict) or not layer["signals"]:
                errors.append(f"Kit card layer signals missing: {layer.get('id')}")
            boundary = str(layer.get("public_claim_boundary", "")).lower()
            if not boundary:
                errors.append(f"Kit card layer boundary missing: {layer.get('id')}")
            if "ranking" in boundary and "not" not in boundary:
                errors.append(f"Kit card layer boundary has ranking risk: {layer.get('id')}")

        summary = manifest.get("kit_summary", {})
        expected_summary = {
            "evidence_layer_count": 8,
            "local_rows_scored": 60,
            "tr_en_pairs": 5,
            "turkish_rows": 44,
            "sourcecheckup_needed_rows": 6,
            "human_review_assignments_prepared": 30,
            "external_gate": "blocked_without_user_approval",
        }
        if summary != expected_summary:
            errors.append("Kit card summary mismatch")

        gates = manifest.get("release_gates", {})
        expected_gates = {
            "internal_product_card": "ready",
            "external_release": "blocked_without_user_approval",
            "provider_api_run": "blocked_without_user_approval",
            "new_case_addition": "blocked_without_user_approval",
            "physician_selection": "user_only",
            "clinical_validation_claim": "not_claimed",
            "source_truth_certification": "not_claimed",
            "regulatory_compliance_claim": "not_claimed",
            "official_compatibility_claim": "not_claimed",
            "model_ranking": "not_claimed",
        }
        if gates != expected_gates:
            errors.append("Kit card release gates mismatch")

        validate_source_flags(source_artifacts, errors)

        blocked = set(manifest.get("blocked_actions", []))
        for required in {
            "send_external_email_or_post_without_user_approval",
            "start_provider_api_calls_without_user_approval",
            "add_new_cases_without_user_approval",
            "claim_clinical_validation",
            "claim_source_truth_certification",
            "claim_regulatory_compliance",
            "claim_official_endorsement_or_compatibility",
            "rank_models_as_winners",
            "select_or_contact_physicians_by_agent",
        }:
            if required not in blocked:
                errors.append(f"Kit card blocked_actions missing {required}")

    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in [
            "Health AI Assurance Kit Card",
            "P5 Kit Level Assurance Card",
            "No external send",
            "no provider API call",
            "no new case addition",
            "no patient data",
            "no physician selection",
            "no clinical validation claim",
            "no source truth certification claim",
            "no model ranking",
            "Evidence Layers",
            "Release Gates",
            "make health_ai_assurance_kit_card_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"Kit card markdown missing required phrase: {phrase}")

    for path in [JSON_PATH, MD_PATH]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL Health AI Assurance Kit card validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Health AI Assurance Kit card validation")
    print("evidence_layers=8")
    print("turkish_rows=44")
    print("external_gate=blocked_without_user_approval")
    return 0


def validate_source_flags(source_artifacts: dict[str, Any], errors: list[str]) -> None:
    source_flags = {
        "safetyguard_studio": {"external_action_allowed": False, "contains_patient_data": False},
        "sourcecheckup_cli": {"external_action_allowed": False, "contains_patient_data": False},
        "turkish_drift": {"external_action_allowed": False, "contains_patient_data": False},
        "clinician_panel_packet": {"external_send_allowed": False, "contains_patient_data": False},
        "clinician_literacy": {"external_action_allowed": False, "contains_patient_data": False},
        "monitoring_plan": {"external_action_allowed": False, "automation_started": False},
        "promotion_gate": {"external_action_allowed": False, "provider_api_call_allowed": False},
    }
    for label, expected in source_flags.items():
        relative = source_artifacts.get(label)
        if not relative:
            errors.append(f"Kit card missing source label: {label}")
            continue
        payload = read_json(ROOT / str(relative), errors)
        for key, value in expected.items():
            if payload.get(key) is not value:
                errors.append(f"Kit card source {label} {key} must be {value!r}")


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
        errors.append(f"Missing JSON file: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"JSON must be an object: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
        return {}
    return payload


if __name__ == "__main__":
    sys.exit(main())
