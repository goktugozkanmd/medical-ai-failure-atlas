#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_monitoring_digest_schema_20260708.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_MONITORING_DIGEST_SCHEMA_20260708.md"

EXPECTED_FIELDS = [
    "digest_id",
    "date_checked",
    "signal_surface",
    "source_locator",
    "observed_change",
    "evidence_status",
    "action_meaning",
    "risk_tags",
    "blocked_claims",
    "external_action_gate",
]

EXPECTED_SURFACES = {
    "benchmark_and_eval_ecosystem",
    "source_support_and_claims",
    "turkish_and_non_english_drift",
    "adapter_and_distribution_routes",
    "clinician_literacy_and_review",
    "governance_and_network_routes",
    "repo_health_and_public_claim_hygiene",
}

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
            "manual_only": True,
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
                errors.append(f"Monitoring digest schema {key} must be {expected!r}")
        if manifest.get("status") != "manual_monitoring_digest_schema_ready":
            errors.append("Monitoring digest schema status mismatch")
        if manifest.get("phase") != "P7":
            errors.append("Monitoring digest schema phase must be P7")
        if manifest.get("schema_version") != "health_ai_monitoring_digest_v0_1":
            errors.append("Monitoring digest schema version mismatch")
        if manifest.get("automation_start_gate") != "owner_must_ask":
            errors.append("Monitoring digest automation_start_gate must be owner_must_ask")

        source_artifacts = manifest.get("source_artifacts", {})
        if not isinstance(source_artifacts, dict) or len(source_artifacts) != 7:
            errors.append("Monitoring digest schema must list seven source artifacts")
            source_artifacts = {}
        for label, relative in source_artifacts.items():
            if not (ROOT / str(relative)).exists():
                errors.append(f"Monitoring digest source artifact missing for {label}: {relative}")

        fields = manifest.get("schema_fields", [])
        field_names = [field.get("name") for field in fields if isinstance(field, dict)]
        if field_names != EXPECTED_FIELDS:
            errors.append(f"Monitoring digest field order mismatch: {field_names!r}")
        if any(field.get("required") is not True for field in fields if isinstance(field, dict)):
            errors.append("Monitoring digest all schema fields must be required")

        surfaces = manifest.get("watch_surfaces", [])
        surface_ids = {str(surface.get("id")) for surface in surfaces if isinstance(surface, dict)}
        if surface_ids != EXPECTED_SURFACES:
            errors.append(f"Monitoring digest watch surfaces mismatch: {sorted(surface_ids)}")
        if manifest.get("watch_surface_count") != 7:
            errors.append("Monitoring digest watch_surface_count must be 7")

        rows = manifest.get("sample_digest_rows", [])
        if not isinstance(rows, list) or len(rows) != 6:
            errors.append("Monitoring digest must include six sample digest rows")
            rows = []
        if manifest.get("digest_row_count") != len(rows):
            errors.append("Monitoring digest digest_row_count mismatch")
        for index, row in enumerate(rows, start=1):
            if row.get("digest_id") != f"HMD{index:03d}":
                errors.append(f"Monitoring digest row id mismatch at {index}")
            for field in EXPECTED_FIELDS:
                if field not in row:
                    errors.append(f"Monitoring digest row {row.get('digest_id')} missing field {field}")
            if row.get("external_action_gate") != "blocked_without_user_approval":
                errors.append(f"Monitoring digest row {row.get('digest_id')} external gate must stay blocked")
            if not isinstance(row.get("risk_tags"), list) or not row["risk_tags"]:
                errors.append(f"Monitoring digest row {row.get('digest_id')} must include risk tags")
            if not isinstance(row.get("blocked_claims"), list) or not row["blocked_claims"]:
                errors.append(f"Monitoring digest row {row.get('digest_id')} must include blocked claims")

        validate_source_flags(source_artifacts, errors)

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
                errors.append(f"Monitoring digest blocked_actions missing {required}")

    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in [
            "Health AI Monitoring Digest Schema",
            "P7 Monitoring Digest",
            "Manual only",
            "No external send",
            "no provider API call",
            "no automation start",
            "no paid run",
            "no new case addition",
            "no patient data",
            "no physician selection",
            "no clinical validation claim",
            "no model ranking",
            "make health_ai_monitoring_digest_schema_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"Monitoring digest markdown missing required phrase: {phrase}")

    for path in [JSON_PATH, MD_PATH]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL Health AI monitoring digest schema validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Health AI monitoring digest schema validation")
    print("schema_fields=10")
    print("watch_surfaces=7")
    print("digest_rows=6")
    return 0


def validate_source_flags(source_artifacts: dict[str, Any], errors: list[str]) -> None:
    json_expectations = {
        "monitoring_plan": {"automation_started": False, "external_action_allowed": False, "paid_run_allowed": False},
        "benchmark_boundary_index": {"external_action_allowed": False},
        "kit_card": {"external_action_allowed": False, "automation_started": False},
        "clinician_literacy_demo_index": {"external_action_allowed": False, "automation_started": False},
        "sourcecheckup_cli": {"external_action_allowed": False, "contains_patient_data": False},
        "turkish_drift_dashboard": {"external_action_allowed": False, "new_cases_added": False},
    }
    for label, expectations in json_expectations.items():
        relative = source_artifacts.get(label)
        if not relative:
            errors.append(f"Monitoring digest missing source label: {label}")
            continue
        payload = read_json(ROOT / str(relative), errors)
        for key, expected in expectations.items():
            if payload.get(key) is not expected:
                errors.append(f"Monitoring digest source {label} {key} must be {expected!r}")


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
