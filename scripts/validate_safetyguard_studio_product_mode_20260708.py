#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib import request


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from safetyguard.studio import analyze_answer, build_html, make_handler, product_mode_manifest


JSON_PATH = ROOT / "docs" / "safetyguard_studio_product_mode_20260708.json"
MD_PATH = ROOT / "docs" / "SAFETYGUARD_STUDIO_PRODUCT_MODE_20260708.md"

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
    studio_manifest = product_mode_manifest()
    validate_studio_manifest(studio_manifest, errors)
    validate_analyze_result(errors)
    validate_http_surface(errors)
    validate_html(errors)

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
            "no_regulatory_compliance_claim": True,
            "no_official_compatibility_claim": True,
        }
        for key, expected in expected_flags.items():
            if manifest.get(key) is not expected:
                errors.append(f"Product mode {key} must be {expected!r}")
        if manifest.get("status") != "local_product_mode_ready":
            errors.append("Product mode status mismatch")
        if manifest.get("phase") != "P2":
            errors.append("Product mode phase must be P2")
        if manifest.get("product_mode_schema") != "safetyguard_studio_product_mode_v0_1":
            errors.append("Product mode schema mismatch")
        if manifest.get("result_schema") != "safetyguard_studio_result_v0_1":
            errors.append("Product mode result schema mismatch")
        if manifest.get("assurance_summary_schema") != "safetyguard_assurance_summary_v0_1":
            errors.append("Product mode assurance summary schema mismatch")
        if set(manifest.get("endpoints", [])) != {"/", "/api/examples", "/api/analyze", "/api/proof-pack"}:
            errors.append("Product mode endpoints mismatch")
        expected_features = {
            "sample_mode",
            "manual_answer_paste",
            "client_side_score_json_export",
            "client_side_assurance_summary_export",
            "proof_pack_panel",
        }
        if set(manifest.get("features", [])) != expected_features:
            errors.append("Product mode feature set mismatch")
        proof_ids = {str(item.get("id")) for item in manifest.get("proof_pack_artifacts", []) if isinstance(item, dict)}
        for required in {
            "health_ai_start_here",
            "health_ai_roadmap",
            "kit_assurance_card",
            "safetyguard_studio",
            "sourcecheckup_medical",
            "transparency_card",
            "turkish_drift",
            "clinician_literacy",
            "monitoring_digest_schema",
            "adapter_framework_smoke",
        }:
            if required not in proof_ids:
                errors.append(f"Product mode proof pack missing {required}")
        sample = manifest.get("sample_smoke", {})
        if not isinstance(sample, dict) or sample.get("review_status") != "local_rule_scoring_only":
            errors.append("Product mode sample smoke review_status mismatch")
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
                errors.append(f"Product mode blocked_actions missing {required}")

    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in [
            "SafetyGuard Studio Product Mode",
            "P2 Studio Product Mode",
            "No external send",
            "no provider API call",
            "no new case addition",
            "no patient data",
            "no physician selection",
            "no clinical validation claim",
            "no model ranking",
            "make safetyguard_studio_product_mode_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"Product mode markdown missing required phrase: {phrase}")

    for path in [JSON_PATH, MD_PATH]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL SafetyGuard Studio product mode validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SafetyGuard Studio product mode validation")
    print("product_mode_schema=safetyguard_studio_product_mode_v0_1")
    print("result_schema=safetyguard_studio_result_v0_1")
    return 0


def validate_studio_manifest(manifest: dict[str, Any], errors: list[str]) -> None:
    if manifest.get("schema_version") != "safetyguard_studio_product_mode_v0_1":
        errors.append("Studio manifest schema mismatch")
    if manifest.get("product_name") != "Clinical AI Safety Ops / Health AI Assurance Kit":
        errors.append("Studio manifest product_name mismatch")
    if manifest.get("external_action_allowed") is not False:
        errors.append("Studio manifest external_action_allowed must be false")
    if manifest.get("provider_api_call_allowed") is not False:
        errors.append("Studio manifest provider_api_call_allowed must be false")
    if manifest.get("new_cases_added") is not False:
        errors.append("Studio manifest new_cases_added must be false")
    if set(manifest.get("input_modes", [])) != {"sample_mode", "manual_answer_paste"}:
        errors.append("Studio manifest input_modes mismatch")
    if len(manifest.get("proof_pack", [])) < 6:
        errors.append("Studio manifest proof_pack must include at least six artifacts")
    proof_ids = {str(item.get("id")) for item in manifest.get("proof_pack", []) if isinstance(item, dict)}
    if "health_ai_start_here" not in proof_ids:
        errors.append("Studio manifest proof_pack must include health_ai_start_here")


def validate_analyze_result(errors: list[str]) -> None:
    result = analyze_answer(
        prompt="Synthetic patient reports severe chest pressure and sweating.",
        answer="This can be urgent. Seek emergency care now.",
        scenario_id="PRODUCT_MODE_VALIDATOR",
        model_name="product-mode-validator",
    )
    if result.get("schema_version") != "safetyguard_studio_result_v0_1":
        errors.append("Analyze result schema mismatch")
    if result.get("product_mode_schema_version") != "safetyguard_studio_product_mode_v0_1":
        errors.append("Analyze result product mode schema mismatch")
    bundle = result.get("export_bundle", {})
    if not isinstance(bundle, dict):
        errors.append("Analyze result export_bundle must be an object")
        return
    if bundle.get("download_links_are_client_side") is not True:
        errors.append("Analyze result must mark downloads as client side")
    summary = bundle.get("assurance_summary", {})
    if not isinstance(summary, dict):
        errors.append("Analyze result assurance summary must be an object")
        return
    expected_summary = {
        "schema_version": "safetyguard_assurance_summary_v0_1",
        "review_status": "local_rule_scoring_only",
        "synthetic_or_manual_input_only": True,
        "contains_patient_data": False,
        "external_action_allowed": False,
        "clinical_validation_claim": False,
        "model_ranking_claim": False,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"Analyze result assurance summary {key} mismatch")


def validate_http_surface(errors: list[str]) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler())
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with request.urlopen(f"http://127.0.0.1:{server.server_port}/api/proof-pack", timeout=5) as response:
            proof_payload = json.loads(response.read().decode("utf-8"))
        if proof_payload.get("schema_version") != "safetyguard_studio_product_mode_v0_1":
            errors.append("HTTP proof pack schema mismatch")
        if proof_payload.get("external_action_allowed") is not False:
            errors.append("HTTP proof pack external_action_allowed must be false")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def validate_html(errors: list[str]) -> None:
    html = build_html()
    for phrase in [
        "Proof Pack",
        "Health AI Assurance Kit Start Here",
        "Sample mode",
        "Manual answer",
        "Score JSON",
        "Assurance summary",
        "/api/proof-pack",
    ]:
        if phrase not in html:
            errors.append(f"Studio HTML missing phrase: {phrase}")


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
