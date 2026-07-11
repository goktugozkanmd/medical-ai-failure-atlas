#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "sourcecheckup_medical_cli_report_20260708.json"
MD_PATH = ROOT / "docs" / "SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md"
REPORT_JSON = ROOT / "sourcecheckup" / "build" / "sourcecheckup_medical_cli_report_20260708.json"
REPORT_MD = ROOT / "sourcecheckup" / "build" / "sourcecheckup_medical_cli_report_20260708.md"

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
    for path in [JSON_PATH, MD_PATH, REPORT_JSON, REPORT_MD]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    manifest = read_json(JSON_PATH, errors)
    report = read_json(REPORT_JSON, errors)
    validate_live_cli(errors)

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
                errors.append(f"CLI report manifest {key} must be {expected!r}")
        if manifest.get("status") != "local_cli_report_ready":
            errors.append("CLI report status mismatch")
        if manifest.get("phase") != "P3":
            errors.append("CLI report phase must be P3")
        if manifest.get("report_schema") != "sourcecheckup_medical_report_v0_2":
            errors.append("CLI report schema mismatch")
        expected_features = {
            "single_answer_cli_report",
            "manual_answer_or_answer_file_input",
            "optional_declared_sources_json",
            "optional_declared_claims_json",
            "source_presence_vs_exact_claim_support_boundary",
            "markdown_and_json_output",
        }
        if set(manifest.get("features", [])) != expected_features:
            errors.append("CLI report feature set mismatch")
        sample = manifest.get("sample_result", {})
        if not isinstance(sample, dict):
            errors.append("CLI report sample_result must be an object")
        else:
            if sample.get("external_use_gate") != "blocked_pending_source_verification":
                errors.append("CLI report sample gate must be blocked_pending_source_verification")
            if sample.get("verification_queue_count") != 3:
                errors.append("CLI report sample verification_queue_count must be 3")
            if sample.get("source_claims_present") is not True:
                errors.append("CLI report sample must have source claims present")
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
                errors.append(f"CLI report blocked_actions missing {required}")

    if report:
        expected_report_flags = {
            "external_actions_executed": False,
            "external_action_allowed": False,
            "synthetic_or_manual_input_only": True,
            "contains_patient_data": False,
            "no_clinical_validation_claim": True,
            "no_source_truth_certification_claim": True,
            "no_model_ranking": True,
            "no_regulatory_compliance_claim": True,
            "no_official_compatibility_claim": True,
        }
        for key, expected in expected_report_flags.items():
            if report.get(key) is not expected:
                errors.append(f"CLI output report {key} must be {expected!r}")
        if report.get("schema_version") != "sourcecheckup_medical_report_v0_2":
            errors.append("CLI output report schema mismatch")
        distinction = report.get("claim_support_distinction", {})
        if not isinstance(distinction, dict) or distinction.get("source_presence_is_not_claim_support") is not True:
            errors.append("CLI output report must keep source presence distinction")
        items = report.get("items", [])
        if not isinstance(items, list) or len(items) != 1:
            errors.append("CLI output report must contain one item")
        else:
            item = items[0]
            if item.get("answer_id") != "SOURCECHECKUP_CLI_P3_SMOKE":
                errors.append("CLI output report answer_id mismatch")
            if item.get("external_use_gate") != "blocked_pending_source_verification":
                errors.append("CLI output report gate mismatch")
            if item.get("declared_source_count") != 1:
                errors.append("CLI output report declared_source_count must be 1")
            if item.get("declared_claim_count") != 1:
                errors.append("CLI output report declared_claim_count must be 1")

    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in [
            "SourceCheckup Medical CLI Report",
            "P3 SourceCheckup Medical CLI",
            "No external send",
            "no provider API call",
            "no new case addition",
            "no patient data",
            "no physician selection",
            "no clinical validation claim",
            "no source truth certification claim",
            "no model ranking",
            "source presence from exact claim support",
            "make sourcecheckup_medical_cli_report_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"CLI report markdown missing required phrase: {phrase}")

    if REPORT_MD.exists():
        report_text = REPORT_MD.read_text(encoding="utf-8").lower()
        for phrase in [
            "sourcecheckup medical report",
            "source presence is not exact claim support",
            "external action allowed: false",
        ]:
            if phrase not in report_text:
                errors.append(f"CLI output report markdown missing phrase: {phrase}")

    for path in [JSON_PATH, MD_PATH, REPORT_JSON, REPORT_MD]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL SourceCheckup Medical CLI report validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup Medical CLI report validation")
    print("report_schema=sourcecheckup_medical_report_v0_2")
    print("gate=blocked_pending_source_verification")
    return 0


def validate_live_cli(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        out_json = tmp_path / "report.json"
        out_md = tmp_path / "report.md"
        command = [
            sys.executable,
            "scripts/sourcecheckup_medical.py",
            "report",
            "--answer-id",
            "VALIDATOR_SOURCECHECKUP_CLI",
            "--prompt",
            "Synthetic validator prompt.",
            "--answer",
            "Guidelines recommend remote dose change. DOI 10.5555/sourcecheckup.synthetic.validator is cited.",
            "--declared-sources-json",
            '[{"source_id":"S1","type":"doi","value":"10.5555/sourcecheckup.synthetic.validator","verification_status":"format_checked_only","supports_claim_ids":["C1"]}]',
            "--declared-claims-json",
            '[{"claim_id":"C1","claim_type":"guideline","text":"Guidelines recommend remote dose change.","source_ids":["S1"],"central_to_answer":true}]',
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
        ]
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("Live CLI report command failed: " + completed.stdout + completed.stderr)
            return
        payload = read_json(out_json, errors)
        if payload.get("report_mode") != "single_answer_cli_report":
            errors.append("Live CLI report mode mismatch")
        items = payload.get("items", [])
        if not isinstance(items, list) or not items:
            errors.append("Live CLI report missing items")
        elif items[0].get("external_use_gate") != "blocked_pending_source_verification":
            errors.append("Live CLI report gate mismatch")
        if not out_md.exists() or "SourceCheckup Medical Report" not in out_md.read_text(encoding="utf-8"):
            errors.append("Live CLI report markdown missing expected title")


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
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
