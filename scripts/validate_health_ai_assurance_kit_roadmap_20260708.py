#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_assurance_kit_roadmap_20260708.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md"

EXPECTED_LANES = {
    "safety_gap_layer",
    "adapter_distribution_layer",
    "sourcecheckup_medical_layer",
    "turkish_drift_layer",
    "transparency_card_layer",
    "clinician_literacy_layer",
    "monitoring_layer",
}

EXPECTED_PHASES = ["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P7B", "P8"]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
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
            "no_model_ranking": True,
            "no_official_compatibility_claim": True,
        }
        for key, expected in expected_flags.items():
            if manifest.get(key) is not expected:
                errors.append(f"Roadmap {key} must be {expected!r}")
        if manifest.get("project_name") != "Clinical AI Safety Ops / Health AI Assurance Kit":
            errors.append("Roadmap project_name mismatch")
        if manifest.get("next_build_step") != "p8_followups_need_separate_review":
            errors.append("Roadmap next_build_step must be p8_followups_need_separate_review")

        lanes = manifest.get("lanes", [])
        if not isinstance(lanes, list) or len(lanes) != 7:
            errors.append("Roadmap must list seven product lanes")
            lanes = []
        lane_ids = {str(lane.get("id")) for lane in lanes if isinstance(lane, dict)}
        if lane_ids != EXPECTED_LANES:
            errors.append(f"Roadmap lane ids mismatch: {sorted(lane_ids)}")
        for lane in lanes:
            if not isinstance(lane, dict):
                continue
            artifacts = lane.get("current_artifacts", [])
            if not isinstance(artifacts, list) or not artifacts:
                errors.append(f"Lane {lane.get('id')} must include current_artifacts")
                continue
            for relative in artifacts:
                if not (ROOT / str(relative)).exists():
                    errors.append(f"Lane {lane.get('id')} artifact missing: {relative}")

        phases = manifest.get("phases", [])
        phase_ids = [str(phase.get("phase")) for phase in phases if isinstance(phase, dict)]
        if phase_ids != EXPECTED_PHASES:
            errors.append(f"Roadmap phase order mismatch: {phase_ids!r}")
        statuses = {str(phase.get("status")) for phase in phases if isinstance(phase, dict)}
        if "first_public_issue_opened" not in statuses:
            errors.append("Roadmap must include first public proof issue phase")
        completed = [phase for phase in phases if isinstance(phase, dict) and phase.get("status") == "completed"]
        if len(completed) < 9:
            errors.append("Roadmap must mark P0 through P7B completed")
        phase_status = {str(phase.get("phase")): str(phase.get("status")) for phase in phases if isinstance(phase, dict)}
        if phase_status.get("P5") != "completed":
            errors.append("Roadmap must mark P5 completed")
        if phase_status.get("P6") != "completed":
            errors.append("Roadmap must mark P6 completed")
        if phase_status.get("P7") != "completed":
            errors.append("Roadmap must mark P7 completed")
        if phase_status.get("P7B") != "completed":
            errors.append("Roadmap must mark P7B completed")
        if phase_status.get("P8") != "first_public_issue_opened":
            errors.append("Roadmap must mark P8 first_public_issue_opened")
        route = manifest.get("external_proof_route", {})
        if not isinstance(route, dict) or route.get("issue") != "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231":
            errors.append("Roadmap external proof route issue mismatch")
        if isinstance(route, dict):
            for internal_key in ("body_source", "audit_note", "send_log"):
                if internal_key in route:
                    errors.append(f"Roadmap external proof route exposes internal field {internal_key}")
            if route.get("followup_gate") != "separate_review_required":
                errors.append("Roadmap external proof route must require separate review for followups")

        blocked = set(manifest.get("blocked_actions", []))
        for required in {
            "send_external_email_or_post_without_user_approval",
            "start_provider_api_calls_without_user_approval",
            "add_new_cases_without_user_approval",
            "claim_clinical_validation",
            "claim_regulatory_compliance",
            "claim_official_endorsement_or_compatibility",
            "rank_models_as_winners",
            "select_or_contact_physicians_by_agent",
        }:
            if required not in blocked:
                errors.append(f"Roadmap blocked_actions missing {required}")

    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in [
            "Health AI Assurance Kit Roadmap",
            "Clinical AI Safety Ops / Health AI Assurance Kit",
            "No external send",
            "no provider API call",
            "no new case addition",
            "no patient data",
            "no physician selection",
            "no clinical validation claim",
            "no model ranking",
            "make health_ai_assurance_kit_roadmap_20260708",
            "HEALTH_AI_ASSURANCE_KIT_CARD_20260708",
            "HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708",
            "HEALTH_AI_MONITORING_DIGEST_SCHEMA_20260708",
            "HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"Roadmap markdown missing required phrase: {phrase}")

    for path in [JSON_PATH, MD_PATH]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL health AI assurance kit roadmap validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS health AI assurance kit roadmap validation")
    print("lanes=7")
    print("phases=10")
    print("next_build_step=p8_followups_need_separate_review")
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


if __name__ == "__main__":
    sys.exit(main())
