#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_assurance_product_packet_20260709.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_PRODUCT_PACKET_20260709.md"
README_PATH = ROOT / "README.md"
MAKEFILE_PATH = ROOT / "Makefile"

EXPECTED_SOURCE_IDS = [
    "readme",
    "roadmap",
    "start_here",
    "kit_card",
    "safety_ops_positioning",
    "growth_buildout_index",
    "feedback_intake_md",
    "feedback_intake_json",
    "feedback_triage_board_md",
    "feedback_triage_board_json",
    "feedback_triage_examples_md",
    "feedback_triage_examples_json",
]

EXPECTED_PHASES = [
    "P0",
    "P1",
    "P2",
    "P3",
    "P4",
    "P5",
    "P6",
    "P7",
    "P7B",
    "P8",
    "P9",
    "P10",
    "P11",
]

EXPECTED_FLAGS = {
    "external_action_allowed": False,
    "provider_api_call_allowed": False,
    "automation_started": False,
    "paid_run_allowed": False,
    "new_cases_added": False,
    "agent_selected_physicians": False,
    "contains_patient_data": False,
    "contains_private_clinical_text": False,
    "contains_raw_clinical_notes": False,
    "contains_private_model_output": False,
    "no_medical_advice": True,
    "no_clinical_validation_claim": True,
    "no_model_ranking": True,
    "no_source_truth_certification_claim": True,
    "no_regulatory_compliance_claim": True,
    "no_official_compatibility_claim": True,
    "no_institution_support_claim": True,
    "no_partnership_claim": True,
    "no_payment_claim": True,
    "no_terms_acceptance_claim": True,
}

REQUIRED_MD_PHRASES = [
    "Health AI Assurance Product Packet",
    "Roadmap phase: P12 product packet.",
    "P0 Through P11 Spine",
    "Feedback Loop",
    "P9 routes",
    "P10 triage states",
    "P11 example records",
    "No external send",
    "no provider API call",
    "no automation start",
    "no new case addition",
    "no patient data",
    "no private clinical text",
    "no raw clinical notes",
    "no private model output",
    "no physician selection",
    "no medical advice",
    "no clinical validation claim",
    "no model ranking",
    "no source truth certification claim",
    "no regulatory compliance claim",
    "no official compatibility claim",
    "no institution support claim",
    "make health_ai_assurance_product_packet_20260709",
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
    "payment completed",
    "terms accepted",
    "partner confirmed",
    "institution endorsed",
]


def main() -> int:
    errors: list[str] = []
    for path in [JSON_PATH, MD_PATH, README_PATH, MAKEFILE_PATH]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    manifest = read_json(JSON_PATH, errors)
    if manifest:
        validate_manifest(manifest, errors)

    if MD_PATH.exists():
        md_text = MD_PATH.read_text(encoding="utf-8")
        md_lower = md_text.lower()
        for phrase in REQUIRED_MD_PHRASES:
            if phrase.lower() not in md_lower:
                errors.append(f"Product packet markdown missing required phrase: {phrase}")
        check_forbidden_phrases(MD_PATH, md_lower, errors)

    if JSON_PATH.exists():
        check_forbidden_phrases(JSON_PATH, JSON_PATH.read_text(encoding="utf-8").lower(), errors)

    if README_PATH.exists():
        readme_text = README_PATH.read_text(encoding="utf-8")
        if "docs/HEALTH_AI_ASSURANCE_PRODUCT_PACKET_20260709.md" not in readme_text:
            errors.append("README must link Health AI Assurance Product Packet")

    if MAKEFILE_PATH.exists():
        makefile_text = MAKEFILE_PATH.read_text(encoding="utf-8")
        if "health_ai_assurance_product_packet_20260709" not in makefile_text:
            errors.append("Makefile must expose health_ai_assurance_product_packet_20260709 target")
        if "scripts/export_health_ai_assurance_product_packet_20260709.py" not in makefile_text:
            errors.append("Makefile must run P12 product packet exporter")
        if "scripts/validate_health_ai_assurance_product_packet_20260709.py" not in makefile_text:
            errors.append("Makefile must run P12 product packet validator")

    if errors:
        print("FAIL health AI assurance product packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS health AI assurance product packet validation")
    print("phase=P12")
    print("source_artifacts=12")
    print("feedback_loop_phases=3")
    print("external_action_allowed=false")
    return 0


def validate_manifest(manifest: dict[str, Any], errors: list[str]) -> None:
    if manifest.get("artifact_id") != "health_ai_assurance_product_packet_20260709":
        errors.append("Product packet artifact_id mismatch")
    if manifest.get("status") != "internal_product_packet_ready":
        errors.append("Product packet status must be internal_product_packet_ready")
    if manifest.get("phase") != "P12":
        errors.append("Product packet phase must be P12")
    if manifest.get("product_name") != "Clinical AI Safety Ops / Health AI Assurance Kit":
        errors.append("Product packet product_name mismatch")
    if manifest.get("public_anchor") != "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231":
        errors.append("Product packet public anchor must be issue 231")
    if manifest.get("next_build_step") != "p12_product_packet_ready_for_review":
        errors.append("Product packet next_build_step mismatch")

    for key, expected in EXPECTED_FLAGS.items():
        if manifest.get(key) is not expected:
            errors.append(f"Product packet {key} must be {expected!r}")

    source_artifacts = manifest.get("source_artifacts", [])
    if not isinstance(source_artifacts, list) or len(source_artifacts) != len(EXPECTED_SOURCE_IDS):
        errors.append("Product packet must list 12 source artifacts")
        source_artifacts = []
    if manifest.get("source_artifact_count") != len(EXPECTED_SOURCE_IDS):
        errors.append("Product packet source_artifact_count must be 12")
    source_ids = [str(item.get("id")) for item in source_artifacts if isinstance(item, dict)]
    if source_ids != EXPECTED_SOURCE_IDS:
        errors.append(f"Product packet source artifact order mismatch: {source_ids!r}")
    for item in source_artifacts:
        if not isinstance(item, dict):
            continue
        relative = item.get("path")
        if not relative:
            errors.append(f"Product packet source artifact path missing for {item.get('id')}")
            continue
        if str(relative).startswith("http"):
            continue
        if not (ROOT / str(relative)).exists():
            errors.append(f"Product packet source artifact missing: {relative}")
        if not item.get("phase") or not item.get("role"):
            errors.append(f"Product packet source artifact metadata incomplete: {item.get('id')}")

    phase_spine = manifest.get("phase_spine", [])
    phase_ids = [str(item.get("phase")) for item in phase_spine if isinstance(item, dict)]
    if phase_ids != EXPECTED_PHASES:
        errors.append(f"Product packet phase spine mismatch: {phase_ids!r}")
    if manifest.get("phase_spine_count") != len(EXPECTED_PHASES):
        errors.append("Product packet phase_spine_count mismatch")

    feedback_loop = manifest.get("feedback_loop", {})
    if not isinstance(feedback_loop, dict):
        errors.append("Product packet feedback_loop must be an object")
        feedback_loop = {}
    if feedback_loop.get("phases") != ["P9", "P10", "P11"]:
        errors.append("Product packet feedback loop phases must be P9, P10, P11")
    expected_feedback_counts = {
        "route_count": 4,
        "small_task_count": 5,
        "triage_state_count": 6,
        "board_row_count": 6,
        "decision_type_count": 6,
        "example_record_count": 6,
    }
    for key, expected in expected_feedback_counts.items():
        if feedback_loop.get(key) != expected:
            errors.append(f"Product packet feedback_loop {key} must be {expected}")
    if feedback_loop.get("public_anchor") != "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231":
        errors.append("Product packet feedback loop public anchor mismatch")

    steps = manifest.get("review_packet_steps", [])
    if not isinstance(steps, list) or len(steps) != 8:
        errors.append("Product packet must contain 8 review packet steps")
    if manifest.get("review_packet_step_count") != 8:
        errors.append("Product packet review_packet_step_count must be 8")

    release_gates = manifest.get("release_gates", {})
    expected_gates = {
        "internal_product_packet": "ready",
        "external_followup": "separate_owner_review_required",
        "provider_api_run": "blocked_without_owner_approval",
        "new_case_addition": "blocked_without_owner_approval",
        "physician_selection": "user_only",
        "automation_start": "owner_must_ask",
    }
    if release_gates != expected_gates:
        errors.append("Product packet release gates mismatch")


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
        errors.append(f"Missing JSON file: {path.relative_to(ROOT)}")
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


def check_forbidden_phrases(path: Path, lowered: str, errors: list[str]) -> None:
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lowered:
            errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")


if __name__ == "__main__":
    sys.exit(main())
