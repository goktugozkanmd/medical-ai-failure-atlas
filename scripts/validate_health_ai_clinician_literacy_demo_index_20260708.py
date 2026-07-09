#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_clinician_literacy_demo_index_20260708.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md"
PANEL_CASES_TSV = ROOT / "data" / "panel_pilot" / "clinician_panel_pilot_cases_v0_1.tsv"

EXPECTED_CASE_IDS = ["MFB_PANEL_005", "MFB_PANEL_004", "MFB_PANEL_010"]
EXPECTED_STEPS = [
    "frame_problem",
    "case_urgent_escalation",
    "case_missing_variable",
    "case_safe_uncertainty",
    "assurance_output",
    "close_with_small_ask",
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
    for path in [JSON_PATH, MD_PATH, PANEL_CASES_TSV]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    manifest = read_json(JSON_PATH, errors)
    panel_rows = read_panel_cases(PANEL_CASES_TSV, errors)
    rows_by_id = {row.get("panel_case_id"): row for row in panel_rows}
    if manifest:
        expected_flags = {
            "external_action_allowed": False,
            "provider_api_call_allowed": False,
            "automation_started": False,
            "new_cases_added": False,
            "agent_selected_physicians": False,
            "contains_patient_data": False,
            "no_medical_advice": True,
            "no_clinical_validation_claim": True,
            "no_source_truth_certification_claim": True,
            "no_model_ranking": True,
            "no_regulatory_compliance_claim": True,
            "no_official_compatibility_claim": True,
            "no_institution_claim": True,
        }
        for key, expected in expected_flags.items():
            if manifest.get(key) is not expected:
                errors.append(f"Clinician literacy demo index {key} must be {expected!r}")
        if manifest.get("status") != "local_clinician_literacy_demo_index_ready":
            errors.append("Clinician literacy demo index status mismatch")
        if manifest.get("phase") != "P6":
            errors.append("Clinician literacy demo index phase must be P6")
        if manifest.get("index_schema") != "health_ai_clinician_literacy_demo_index_v0_1":
            errors.append("Clinician literacy demo index schema mismatch")
        if manifest.get("duration_minutes") != 20:
            errors.append("Clinician literacy demo index duration must be 20 minutes")
        if manifest.get("demo_case_ids") != EXPECTED_CASE_IDS:
            errors.append("Clinician literacy demo index case order mismatch")
        if manifest.get("demo_case_count") != 3:
            errors.append("Clinician literacy demo index must include three demo cases")

        source_artifacts = manifest.get("source_artifacts", {})
        if not isinstance(source_artifacts, dict) or len(source_artifacts) != 8:
            errors.append("Clinician literacy demo index must list eight source artifacts")
            source_artifacts = {}
        for label, relative in source_artifacts.items():
            if not (ROOT / str(relative)).exists():
                errors.append(f"Clinician literacy source artifact missing for {label}: {relative}")

        cases = manifest.get("demo_cases", [])
        case_ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
        if case_ids != EXPECTED_CASE_IDS:
            errors.append(f"Clinician literacy demo cases mismatch: {case_ids!r}")
        for case in cases if isinstance(cases, list) else []:
            source = rows_by_id.get(case.get("case_id"), {})
            if not source:
                errors.append(f"Clinician literacy demo case missing from panel TSV: {case.get('case_id')}")
                continue
            for key in ["synthetic_patient_summary", "expected_safety_focus", "patient_data_status", "rating_status"]:
                if case.get(key) != source.get(key):
                    errors.append(f"Clinician literacy demo case {case.get('case_id')} {key} mismatch")
            if case.get("patient_data_status") != "synthetic only; no patient data":
                errors.append(f"Clinician literacy demo case patient data boundary mismatch: {case.get('case_id')}")

        steps = manifest.get("lesson_steps", [])
        step_ids = [step.get("id") for step in steps if isinstance(step, dict)]
        if step_ids != EXPECTED_STEPS:
            errors.append(f"Clinician literacy lesson steps mismatch: {step_ids!r}")
        if len(steps) != 6:
            errors.append("Clinician literacy demo index must include six lesson steps")
        case_steps = [step.get("case_id") for step in steps if isinstance(step, dict) and step.get("case_id")]
        if case_steps != EXPECTED_CASE_IDS:
            errors.append("Clinician literacy case step order must match demo case order")

        connected = manifest.get("connected_outputs", {})
        expected_connected = {
            "kit_card_schema": "health_ai_assurance_kit_card_v0_1",
            "kit_evidence_layers": 8,
            "studio_features": 5,
            "sourcecheckup_report_schema": "sourcecheckup_medical_report_v0_2",
            "panel_assignment_count": 30,
            "medhelm_case_count": 3,
        }
        if connected != expected_connected:
            errors.append("Clinician literacy connected outputs mismatch")

        blocked = set(manifest.get("blocked_actions", []))
        for required in {
            "send_external_email_or_post_without_user_approval",
            "run_external_presentation_without_user_approval",
            "start_provider_api_calls_without_user_approval",
            "add_new_cases_without_user_approval",
            "claim_clinical_validation",
            "claim_source_truth_certification",
            "claim_regulatory_compliance",
            "claim_official_endorsement_or_compatibility",
            "rank_models_as_winners",
            "select_or_contact_physicians_by_agent",
            "ask_for_patient_data",
            "use_institution_name_publicly_without_written_permission",
        }:
            if required not in blocked:
                errors.append(f"Clinician literacy blocked_actions missing {required}")

    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in [
            "Health AI Clinician Literacy Demo Index",
            "P6 Clinician Literacy Demo",
            "No external send",
            "no provider API call",
            "no new case addition",
            "no patient data",
            "no physician selection",
            "no medical advice",
            "no clinical validation claim",
            "no institution claim",
            "no model ranking",
            "Twenty Minute Flow",
            "make health_ai_clinician_literacy_demo_index_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"Clinician literacy markdown missing required phrase: {phrase}")

    for path in [JSON_PATH, MD_PATH]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL Health AI clinician literacy demo index validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Health AI clinician literacy demo index validation")
    print("duration_minutes=20")
    print("demo_cases=3")
    print("lesson_steps=6")
    return 0


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"JSON must be an object: {path.relative_to(ROOT)}")
        return {}
    return payload


def read_panel_cases(path: Path, errors: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter="\t"))
    except csv.Error as exc:
        errors.append(f"Invalid TSV {path.relative_to(ROOT)}: {exc}")
        return []


if __name__ == "__main__":
    sys.exit(main())
