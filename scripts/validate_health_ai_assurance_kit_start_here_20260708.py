#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_assurance_kit_start_here_20260708.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md"

EXPECTED_QUICK_START_IDS = [
    "read_start_here",
    "read_roadmap",
    "read_kit_card",
    "try_studio_locally",
    "run_sourcecheckup_locally",
    "review_language_drift",
    "review_demo_index",
    "stop_at_external_gate",
]

EXPECTED_PROOF_IDS = [
    "roadmap",
    "kit_card",
    "safetyguard_studio",
    "sourcecheckup_cli",
    "turkish_drift_dashboard",
    "clinician_literacy_demo",
    "monitoring_digest_schema",
    "local_leaderboard_preview",
    "adapter_framework_smoke",
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
    "automation started",
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
            "paid_run_allowed": False,
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
                errors.append(f"Start Here {key} must be {expected!r}")
        if manifest.get("status") != "local_start_here_proof_pack_ready":
            errors.append("Start Here status mismatch")
        if manifest.get("phase") != "P7B":
            errors.append("Start Here phase must be P7B")
        if manifest.get("product_name") != "Clinical AI Safety Ops / Health AI Assurance Kit":
            errors.append("Start Here product name mismatch")
        if manifest.get("next_build_step") != "p8_followups_need_separate_review":
            errors.append("Start Here next build step mismatch")

        source_artifacts = manifest.get("source_artifacts", {})
        if not isinstance(source_artifacts, dict) or len(source_artifacts) != 11:
            errors.append("Start Here must list eleven source artifacts")
            source_artifacts = {}
        for label, relative in source_artifacts.items():
            if not (ROOT / str(relative)).exists():
                errors.append(f"Start Here source artifact missing for {label}: {relative}")

        quick_start = manifest.get("quick_start_order", [])
        quick_ids = [str(step.get("id")) for step in quick_start if isinstance(step, dict)]
        if quick_ids != EXPECTED_QUICK_START_IDS:
            errors.append(f"Start Here quick start order mismatch: {quick_ids!r}")
        if manifest.get("quick_start_step_count") != len(EXPECTED_QUICK_START_IDS):
            errors.append("Start Here quick_start_step_count mismatch")

        proof_pack = manifest.get("proof_pack_artifacts", [])
        proof_ids = [str(item.get("id")) for item in proof_pack if isinstance(item, dict)]
        if proof_ids != EXPECTED_PROOF_IDS:
            errors.append(f"Start Here proof pack order mismatch: {proof_ids!r}")
        if manifest.get("proof_pack_artifact_count") != len(EXPECTED_PROOF_IDS):
            errors.append("Start Here proof_pack_artifact_count mismatch")
        for item in proof_pack if isinstance(proof_pack, list) else []:
            source = item.get("source")
            if not source or not (ROOT / str(source)).exists():
                errors.append(f"Start Here proof source missing: {item.get('id')}")
            if not item.get("what_it_shows") or not item.get("does_not_show"):
                errors.append(f"Start Here proof item incomplete: {item.get('id')}")

        counts = manifest.get("summary_counts", {})
        expected_counts = {
            "evidence_layers": 8,
            "local_rows_scored": 60,
            "tr_en_pairs": 5,
            "turkish_rows": 44,
            "human_review_assignments_prepared": 30,
            "monitoring_watch_surfaces": 7,
            "monitoring_sample_rows": 6,
        }
        if counts != expected_counts:
            errors.append("Start Here summary counts mismatch")

        release_gates = manifest.get("release_gate_summary", {})
        expected_gates = {
            "internal_start_here": "ready",
            "external_proof_route": "first_public_issue_opened",
            "provider_api_run": "separate_review_required",
            "new_case_addition": "separate_review_required",
            "physician_selection": "user_only",
            "automation_start": "owner_must_ask",
        }
        if release_gates != expected_gates:
            errors.append("Start Here release gates mismatch")
        if manifest.get("external_proof_issue") != "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231":
            errors.append("Start Here external proof issue mismatch")

        completed = manifest.get("completed_roadmap_phases", [])
        if not isinstance(completed, list) or "P7" not in completed or manifest.get("completed_roadmap_phase_count", 0) < 8:
            errors.append("Start Here must show P0 through P7 completed")

        blocked = set(manifest.get("blocked_actions", []))
        for required in {
            "send_external_email_or_post_without_user_approval",
            "run_external_presentation_without_user_approval",
            "start_provider_api_calls_without_user_approval",
            "start_automation_without_user_approval",
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
                errors.append(f"Start Here blocked_actions missing {required}")

    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in [
            "Health AI Assurance Kit Start Here",
            "P7B internal hardening",
            "No external send",
            "no provider API call",
            "no automation start",
            "no paid run",
            "no new case addition",
            "no patient data",
            "no physician selection",
            "no medical advice",
            "no clinical validation claim",
            "no source truth certification claim",
            "no model ranking",
            "Proof Pack Artifacts",
            "make health_ai_assurance_kit_start_here_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"Start Here markdown missing required phrase: {phrase}")

    for path in [JSON_PATH, MD_PATH]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL Health AI Assurance Kit Start Here validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Health AI Assurance Kit Start Here validation")
    print("proof_pack_artifacts=9")
    print("quick_start_steps=8")
    print("next_build_step=p8_followups_need_separate_review")
    return 0


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
