#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from safetyguard.studio import analyze_answer, load_examples, product_mode_manifest

REQUIRED_FILES = [
    "safetyguard/studio.py",
    "scripts/export_safetyguard_transparency_card.py",
    "adapters/README.md",
    "adapters/inspect_evals/register/medfailbench_safety_layer_v0_1.json",
    "adapters/lm_eval/medfailbench_safety_layer_v0_1.yaml",
    "adapters/huggingface/evaluation_card_medfailbench_safety_layer_v0_1.md",
    "docs/MEDFAILBENCH_ADAPTER_PACK_FOUNDATION_20260708.md",
    "docs/SOURCECHECKUP_MEDICAL_PRODUCT_PACKET_20260708.md",
    "docs/sourcecheckup_medical_product_packet_20260708.json",
    "docs/TURKISH_CLINICAL_SAFETYBENCH_PACKAGING_GATE_20260708.md",
    "docs/turkish_clinical_safetybench_packaging_gate_20260708.json",
    "docs/SAFETYGUARD_TRANSPARENCY_CARD_EXPORTER_20260708.md",
    "docs/SAFETYGUARD_EVALUATION_CARD_EXPORT_PATH_20260708.md",
    "docs/safetyguard_evaluation_card_export_path_20260708.json",
    "scripts/smoke_safetyguard_card_release_gate_20260708.py",
    "docs/SAFETYGUARD_CARD_RELEASE_GATE_SMOKE_20260708.md",
    "docs/safetyguard_card_release_gate_smoke_20260708.json",
    "docs/SAFETYGUARD_CARD_RELEASE_GATE_CI_ARTIFACT_20260708.md",
    "docs/safetyguard_card_release_gate_ci_artifact_20260708.json",
    "scripts/export_safetyguard_card_release_note_20260708.py",
    "docs/SAFETYGUARD_CARD_RELEASE_NOTE_DRAFT_20260708.md",
    "docs/safetyguard_card_release_note_draft_20260708.json",
    "docs/HEALTH_AI_SAFETY_OPS_POSITIONING_20260708.md",
    "docs/HEALTH_AI_SAFETY_OPS_DEMO_FLOW_20260708.md",
    "docs/HEALTH_AI_SAFETY_OPS_SOURCE_VERIFICATION_20260708.md",
    "docs/health_ai_safety_ops_positioning_20260708.json",
    "docs/BATCH_EXPANSION_PLAN_V0_3.md",
    "docs/controlled_batch_expansion_plan_20260708.json",
    "scripts/validate_controlled_batch_expansion_20260708.py",
    "docs/MODEL_RUN_NORMALIZATION_PLAN_20260708.md",
    "docs/model_run_normalization_plan_20260708.json",
    "scripts/export_model_run_normalization_plan_20260708.py",
    "scripts/validate_model_run_normalization_plan_20260708.py",
    "docs/MODEL_RUN_PROMOTION_GATE_20260708.md",
    "docs/model_run_promotion_gate_20260708.json",
    "scripts/export_model_run_promotion_gate_20260708.py",
    "scripts/validate_model_run_promotion_gate_20260708.py",
    "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
    "docs/health_ai_assurance_kit_roadmap_20260708.json",
    "scripts/export_health_ai_assurance_kit_roadmap_20260708.py",
    "scripts/validate_health_ai_assurance_kit_roadmap_20260708.py",
    "docs/LOCAL_LEADERBOARD_DRAFT_PREVIEW_20260708.md",
    "docs/local_leaderboard_draft_preview_20260708.json",
    "scripts/export_local_leaderboard_draft_preview_20260708.py",
    "scripts/validate_local_leaderboard_draft_preview_20260708.py",
    "docs/SAFETYGUARD_STUDIO_PRODUCT_MODE_20260708.md",
    "docs/safetyguard_studio_product_mode_20260708.json",
    "scripts/export_safetyguard_studio_product_mode_20260708.py",
    "scripts/validate_safetyguard_studio_product_mode_20260708.py",
    "docs/SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md",
    "docs/sourcecheckup_medical_cli_report_20260708.json",
    "sourcecheckup/build/sourcecheckup_medical_cli_report_20260708.json",
    "sourcecheckup/build/sourcecheckup_medical_cli_report_20260708.md",
    "scripts/export_sourcecheckup_medical_cli_report_20260708.py",
    "scripts/validate_sourcecheckup_medical_cli_report_20260708.py",
    "docs/TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md",
    "docs/turkish_drift_preview_dashboard_20260708.json",
    "scripts/export_turkish_drift_preview_dashboard_20260708.py",
    "scripts/validate_turkish_drift_preview_dashboard_20260708.py",
    "docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
    "docs/health_ai_assurance_kit_card_20260708.json",
    "scripts/export_health_ai_assurance_kit_card_20260708.py",
    "scripts/validate_health_ai_assurance_kit_card_20260708.py",
    "docs/HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md",
    "docs/health_ai_clinician_literacy_demo_index_20260708.json",
    "scripts/export_health_ai_clinician_literacy_demo_index_20260708.py",
    "scripts/validate_health_ai_clinician_literacy_demo_index_20260708.py",
    "docs/HEALTH_AI_MONITORING_DIGEST_SCHEMA_20260708.md",
    "docs/health_ai_monitoring_digest_schema_20260708.json",
    "scripts/export_health_ai_monitoring_digest_schema_20260708.py",
    "scripts/validate_health_ai_monitoring_digest_schema_20260708.py",
    "docs/HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md",
    "docs/health_ai_assurance_kit_start_here_20260708.json",
    "scripts/export_health_ai_assurance_kit_start_here_20260708.py",
    "scripts/validate_health_ai_assurance_kit_start_here_20260708.py",
    "docs/MEDICAL_AI_BENCHMARK_BOUNDARY_INDEX_20260708.md",
    "docs/medical_ai_benchmark_boundary_index_20260708.json",
    "docs/CLINICAL_AI_LITERACY_SIMULATOR_MODULE_20260708.md",
    "docs/clinical_ai_literacy_simulator_module_20260708.json",
    "docs/MEDICAL_AI_SAFETY_MONITORING_BOT_PLAN_20260708.md",
    "docs/medical_ai_safety_monitoring_bot_plan_20260708.json",
    "docs/PROJECT_GROWTH_BUILDOUT_INDEX_20260708.md",
    "docs/project_growth_buildout_index_20260708.json",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "regulatory compliance achieved",
    "accepted by medhelm",
    "accepted by inspect evals",
    "patient data used",
    "agent selected physicians",
]

REQUIRED_BOUNDARY_PHRASES = [
    "No external",
    "No patient data",
    "no clinical validation",
]


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.exists():
            errors.append(f"Missing required file: {relative}")
    buildout = read_json(ROOT / "docs" / "project_growth_buildout_index_20260708.json", errors)
    if buildout:
        expected_flags = {
            "external_action_allowed": False,
            "automation_started": False,
            "new_cases_added": False,
            "agent_selected_physicians": False,
            "contains_patient_data": False,
            "no_clinical_validation_claim": True,
            "no_model_ranking": True,
            "no_official_compatibility_claim": True,
        }
        for key, expected in expected_flags.items():
            if buildout.get(key) is not expected:
                errors.append(f"Buildout JSON {key} must be {expected!r}")
        if len(buildout.get("items", [])) < 8:
            errors.append("Buildout JSON must list at least eight item foundations")
        if "controlled_batch_expansion_plan" not in buildout.get("items", []):
            errors.append("Buildout JSON must include controlled_batch_expansion_plan")
        if "model_run_normalization_plan" not in buildout.get("items", []):
            errors.append("Buildout JSON must include model_run_normalization_plan")
        if "model_run_promotion_gate" not in buildout.get("items", []):
            errors.append("Buildout JSON must include model_run_promotion_gate")
        if "health_ai_assurance_kit_roadmap" not in buildout.get("items", []):
            errors.append("Buildout JSON must include health_ai_assurance_kit_roadmap")
        if "local_leaderboard_draft_preview" not in buildout.get("items", []):
            errors.append("Buildout JSON must include local_leaderboard_draft_preview")
        if "safetyguard_studio_product_mode" not in buildout.get("items", []):
            errors.append("Buildout JSON must include safetyguard_studio_product_mode")
        if "sourcecheckup_medical_cli_report" not in buildout.get("items", []):
            errors.append("Buildout JSON must include sourcecheckup_medical_cli_report")
        if "turkish_drift_preview_dashboard" not in buildout.get("items", []):
            errors.append("Buildout JSON must include turkish_drift_preview_dashboard")
        if "health_ai_assurance_kit_card" not in buildout.get("items", []):
            errors.append("Buildout JSON must include health_ai_assurance_kit_card")
        if "health_ai_clinician_literacy_demo_index" not in buildout.get("items", []):
            errors.append("Buildout JSON must include health_ai_clinician_literacy_demo_index")
        if "health_ai_monitoring_digest_schema" not in buildout.get("items", []):
            errors.append("Buildout JSON must include health_ai_monitoring_digest_schema")
        if "health_ai_assurance_kit_start_here" not in buildout.get("items", []):
            errors.append("Buildout JSON must include health_ai_assurance_kit_start_here")

    release_gate = read_json(ROOT / "docs" / "safetyguard_card_release_gate_smoke_20260708.json", errors)
    if release_gate:
        expected_release_gate = {
            "status": "passed",
            "synthetic_only": True,
            "contains_patient_data": False,
            "external_submission_allowed": False,
            "local_fake_server_used": True,
            "release_gate_passed": True,
            "local_path_leak_scan_passed": True,
            "score_schema_version": "failure_atlas_scores_v0_1",
            "card_schema_version": "safetyguard_transparency_card_v0_1",
        }
        for key, expected in expected_release_gate.items():
            if release_gate.get(key) != expected:
                errors.append(f"Release gate manifest {key} must be {expected!r}")
        if release_gate.get("score_item_count") != release_gate.get("prompt_count"):
            errors.append("Release gate score item count must match prompt count")
        if release_gate.get("card_item_count") != release_gate.get("prompt_count"):
            errors.append("Release gate card item count must match prompt count")
        flags = release_gate.get("boundary_flags", {})
        if not isinstance(flags, dict) or flags.get("external_action_allowed") is not False:
            errors.append("Release gate boundary flags must keep external_action_allowed false")

    ci_artifact = read_json(ROOT / "docs" / "safetyguard_card_release_gate_ci_artifact_20260708.json", errors)
    if ci_artifact:
        expected_ci_artifact = {
            "status": "workflow_dry_run_artifact_job_wired",
            "workflow": ".github/workflows/eval-pipeline.yml",
            "job": "safetyguard-card-release-gate",
            "runs_only_when_dry_run": True,
            "contains_patient_data": False,
            "external_submission_allowed": False,
            "provider_api_call_allowed": False,
            "huggingface_publish_allowed": False,
            "agent_selected_physicians": False,
            "no_clinical_validation_claim": True,
            "no_model_ranking": True,
            "no_official_endorsement_claim": True,
        }
        for key, expected in expected_ci_artifact.items():
            if ci_artifact.get(key) != expected:
                errors.append(f"CI artifact JSON {key} must be {expected!r}")
        workflow_text = (ROOT / ".github" / "workflows" / "eval-pipeline.yml").read_text(encoding="utf-8")
        required_workflow_phrases = [
            "safetyguard-card-release-gate:",
            "needs.resolve-models.outputs.dry_run == 'true'",
            "scripts/smoke_safetyguard_card_release_gate_20260708.py",
            "docs/safetyguard_card_release_gate_smoke_20260708.json",
            "build/safetyguard_card_release_gate_20260708/",
            "if-no-files-found: error",
        ]
        for phrase in required_workflow_phrases:
            if phrase not in workflow_text:
                errors.append(f"Eval pipeline workflow missing release gate phrase: {phrase}")

    release_note = read_json(ROOT / "docs" / "safetyguard_card_release_note_draft_20260708.json", errors)
    if release_note:
        expected_release_note = {
            "status": "local_release_note_draft",
            "source_manifest": "docs/safetyguard_card_release_gate_smoke_20260708.json",
            "ci_artifact_manifest": "docs/safetyguard_card_release_gate_ci_artifact_20260708.json",
            "workflow_job": "safetyguard-card-release-gate",
            "artifact_name": "safetyguard-card-release-gate",
            "local_fake_server_used": True,
            "release_gate_passed": True,
            "local_path_leak_scan_passed": True,
            "contains_patient_data": False,
            "external_submission_allowed": False,
            "provider_api_call_allowed": False,
            "huggingface_publish_allowed": False,
            "agent_selected_physicians": False,
            "no_clinical_validation_claim": True,
            "no_model_ranking": True,
            "no_official_endorsement_claim": True,
        }
        for key, expected in expected_release_note.items():
            if release_note.get(key) != expected:
                errors.append(f"Release note JSON {key} must be {expected!r}")
        if release_note.get("score_item_count") != release_note.get("prompt_count"):
            errors.append("Release note score item count must match prompt count")
        if release_note.get("card_item_count") != release_note.get("prompt_count"):
            errors.append("Release note card item count must match prompt count")

    safety_ops = read_json(ROOT / "docs" / "health_ai_safety_ops_positioning_20260708.json", errors)
    if safety_ops:
        expected_safety_ops = {
            "status": "local_positioning_draft",
            "external_action_allowed": False,
            "contains_patient_data": False,
            "new_cases_added": False,
            "agent_selected_physicians": False,
            "no_clinical_validation_claim": True,
            "no_model_ranking": True,
            "no_regulatory_compliance_claim": True,
            "no_official_compatibility_claim": True,
        }
        for key, expected in expected_safety_ops.items():
            if safety_ops.get(key) != expected:
                errors.append(f"Health AI Safety Ops JSON {key} must be {expected!r}")
        required_lanes = {
            "safety_gap_layer",
            "turkish_and_non_english_drift_layer",
            "post_deployment_monitoring_layer",
            "model_card_and_provenance_layer",
            "clinician_literacy_simulator",
        }
        if set(safety_ops.get("primary_lanes", [])) != required_lanes:
            errors.append("Health AI Safety Ops JSON primary_lanes mismatch")
        required_cases = {"MFB_PANEL_004", "MFB_PANEL_005", "MFB_PANEL_010"}
        if set(safety_ops.get("local_demo_cases", [])) != required_cases:
            errors.append("Health AI Safety Ops JSON local_demo_cases mismatch")

    batch_plan = read_json(ROOT / "docs" / "controlled_batch_expansion_plan_20260708.json", errors)
    if batch_plan:
        expected_batch_flags = {
            "external_action_allowed": False,
            "provider_api_call_allowed": False,
            "automation_started": False,
            "new_cases_added": False,
            "agent_selected_physicians": False,
            "contains_patient_data": False,
            "no_clinical_validation_claim": True,
            "no_model_ranking": True,
            "separate_validation_tiers": True,
        }
        for key, expected in expected_batch_flags.items():
            if batch_plan.get(key) is not expected:
                errors.append(f"Controlled batch expansion JSON {key} must be {expected!r}")
        if batch_plan.get("max_core_release_rows") != 300:
            errors.append("Controlled batch expansion max_core_release_rows must be 300")
        counts = batch_plan.get("current_counts", {})
        expected_counts = {
            "scenario_bank_core_rows": 150,
            "public_prompt_set_rows": 70,
            "safetyguard_prompt_surface_rows": 222,
            "leaderboard_prompt_surface_rows": 222,
            "turkish_medllm_rows": 44,
            "tr_en_drift_probe_rows": 10,
            "panel_pilot_rows": 15,
        }
        if counts != expected_counts:
            errors.append("Controlled batch expansion current_counts mismatch")

    normalization_plan = read_json(ROOT / "docs" / "model_run_normalization_plan_20260708.json", errors)
    if normalization_plan:
        expected_normalization_flags = {
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
        for key, expected in expected_normalization_flags.items():
            if normalization_plan.get(key) is not expected:
                errors.append(f"Model run normalization JSON {key} must be {expected!r}")
        if normalization_plan.get("target_prompt_count") != 30:
            errors.append("Model run normalization target_prompt_count must be 30")
        if normalization_plan.get("public_models_count") != 10:
            errors.append("Model run normalization public_models_count must be 10")
        if normalization_plan.get("totals") != {
            "public_normalization_gap_rows": 176,
            "provider_generation_gap_rows": 149,
            "local_score_or_promotion_gap_rows": 27,
        }:
            errors.append("Model run normalization totals mismatch")
        model_rows = normalization_plan.get("models", [])
        if not isinstance(model_rows, list) or len(model_rows) != 10:
            errors.append("Model run normalization must list 10 model rows")
        else:
            row_by_model = {str(row.get("model_name")): row for row in model_rows if isinstance(row, dict)}
            for model_name, public_count in {
                "DeepSeek V4 Pro": 5,
                "GLM-5.2": 28,
                "Qwen 3.7 Max": 30,
                "Qwen 3.6 Plus": 30,
            }.items():
                row = row_by_model.get(model_name, {})
                if row.get("public_prompt_count") != public_count:
                    errors.append(f"Model run normalization public count mismatch for {model_name}")
            if row_by_model.get("DeepSeek V4 Pro", {}).get("local_score_or_promotion_gap") != 25:
                errors.append("DeepSeek V4 Pro local score or promotion gap must be 25")
            if row_by_model.get("GLM-5.2", {}).get("local_score_or_promotion_gap") != 2:
                errors.append("GLM 5.2 local score or promotion gap must be 2")

    promotion_gate = read_json(ROOT / "docs" / "model_run_promotion_gate_20260708.json", errors)
    if promotion_gate:
        expected_promotion_flags = {
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
        for key, expected in expected_promotion_flags.items():
            if promotion_gate.get(key) is not expected:
                errors.append(f"Model run promotion gate JSON {key} must be {expected!r}")
        if promotion_gate.get("target_prompt_count") != 30:
            errors.append("Model run promotion gate target_prompt_count must be 30")
        if promotion_gate.get("totals") != {
            "models_ready_for_local_promotion_review": 2,
            "local_rows_scored": 60,
            "public_rows_closed_by_local_artifacts": 27,
            "provider_generation_rows_used": 0,
        }:
            errors.append("Model run promotion gate totals mismatch")
        rows = promotion_gate.get("models", [])
        if not isinstance(rows, list) or len(rows) != 2:
            errors.append("Model run promotion gate must list two model rows")
        else:
            row_by_model = {str(row.get("model_name")): row for row in rows if isinstance(row, dict)}
            if set(row_by_model) != {"DeepSeek V4 Pro", "GLM-5.2"}:
                errors.append("Model run promotion gate model set mismatch")
            if row_by_model.get("DeepSeek V4 Pro", {}).get("normalization_gap_closed_locally") != 25:
                errors.append("DeepSeek V4 Pro promotion gap must be 25")
            if row_by_model.get("GLM-5.2", {}).get("normalization_gap_closed_locally") != 2:
                errors.append("GLM 5.2 promotion gap must be 2")

    assurance_roadmap = read_json(ROOT / "docs" / "health_ai_assurance_kit_roadmap_20260708.json", errors)
    if assurance_roadmap:
        expected_roadmap_flags = {
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
        for key, expected in expected_roadmap_flags.items():
            if assurance_roadmap.get(key) is not expected:
                errors.append(f"Health AI Assurance Kit roadmap JSON {key} must be {expected!r}")
        if assurance_roadmap.get("project_name") != "Clinical AI Safety Ops / Health AI Assurance Kit":
            errors.append("Health AI Assurance Kit roadmap project_name mismatch")
        if assurance_roadmap.get("next_build_step") != "p8_followups_need_separate_review":
            errors.append("Health AI Assurance Kit roadmap next_build_step mismatch")
        lanes = assurance_roadmap.get("lanes", [])
        if not isinstance(lanes, list) or len(lanes) != 7:
            errors.append("Health AI Assurance Kit roadmap must list seven lanes")
        phases = assurance_roadmap.get("phases", [])
        if not isinstance(phases, list) or len(phases) != 10:
            errors.append("Health AI Assurance Kit roadmap must list ten phases")
        phase_status = {str(phase.get("phase")): str(phase.get("status")) for phase in phases if isinstance(phase, dict)}
        if phase_status.get("P5") != "completed":
            errors.append("Health AI Assurance Kit roadmap P5 must be completed")
        if phase_status.get("P6") != "completed":
            errors.append("Health AI Assurance Kit roadmap P6 must be completed")
        if phase_status.get("P7") != "completed":
            errors.append("Health AI Assurance Kit roadmap P7 must be completed")
        if phase_status.get("P7B") != "completed":
            errors.append("Health AI Assurance Kit roadmap P7B must be completed")
        if phase_status.get("P8") != "first_public_issue_opened":
            errors.append("Health AI Assurance Kit roadmap P8 must mark first_public_issue_opened")

    preview = read_json(ROOT / "docs" / "local_leaderboard_draft_preview_20260708.json", errors)
    if preview:
        expected_preview_flags = {
            "external_action_allowed": False,
            "provider_api_call_allowed": False,
            "automation_started": False,
            "public_leaderboard_modified": False,
            "new_cases_added": False,
            "agent_selected_physicians": False,
            "contains_patient_data": False,
            "no_clinical_validation_claim": True,
            "no_model_ranking": True,
            "no_official_compatibility_claim": True,
        }
        for key, expected in expected_preview_flags.items():
            if preview.get(key) is not expected:
                errors.append(f"Local leaderboard draft preview JSON {key} must be {expected!r}")
        scope = preview.get("draft_scope", {})
        if not isinstance(scope, dict):
            errors.append("Local leaderboard draft preview scope must be an object")
        else:
            if scope.get("models_in_preview") != 2:
                errors.append("Local leaderboard draft preview models_in_preview must be 2")
            if scope.get("public_rows_closed_by_local_artifacts") != 27:
                errors.append("Local leaderboard draft preview must close 27 rows")
            if scope.get("provider_generation_rows_used") != 0:
                errors.append("Local leaderboard draft preview provider rows must be 0")
            if scope.get("public_write_allowed") is not False:
                errors.append("Local leaderboard draft preview public_write_allowed must be false")
        rows = preview.get("draft_rows", [])
        if not isinstance(rows, list) or len(rows) != 2:
            errors.append("Local leaderboard draft preview must list two rows")

    studio_product = read_json(ROOT / "docs" / "safetyguard_studio_product_mode_20260708.json", errors)
    if studio_product:
        expected_studio_flags = {
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
        for key, expected in expected_studio_flags.items():
            if studio_product.get(key) is not expected:
                errors.append(f"SafetyGuard Studio product mode JSON {key} must be {expected!r}")
        if studio_product.get("phase") != "P2":
            errors.append("SafetyGuard Studio product mode phase must be P2")
        if studio_product.get("product_mode_schema") != "safetyguard_studio_product_mode_v0_1":
            errors.append("SafetyGuard Studio product mode schema mismatch")
        if set(studio_product.get("endpoints", [])) != {"/", "/api/examples", "/api/analyze", "/api/proof-pack"}:
            errors.append("SafetyGuard Studio product mode endpoints mismatch")
        if "proof_pack_panel" not in studio_product.get("features", []):
            errors.append("SafetyGuard Studio product mode must include proof_pack_panel feature")

    sourcecheckup_cli = read_json(ROOT / "docs" / "sourcecheckup_medical_cli_report_20260708.json", errors)
    if sourcecheckup_cli:
        expected_sourcecheckup_flags = {
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
        for key, expected in expected_sourcecheckup_flags.items():
            if sourcecheckup_cli.get(key) is not expected:
                errors.append(f"SourceCheckup Medical CLI report JSON {key} must be {expected!r}")
        if sourcecheckup_cli.get("phase") != "P3":
            errors.append("SourceCheckup Medical CLI report phase must be P3")
        if sourcecheckup_cli.get("report_schema") != "sourcecheckup_medical_report_v0_2":
            errors.append("SourceCheckup Medical CLI report schema mismatch")
        sample = sourcecheckup_cli.get("sample_result", {})
        if not isinstance(sample, dict) or sample.get("external_use_gate") != "blocked_pending_source_verification":
            errors.append("SourceCheckup Medical CLI report sample gate mismatch")
        if "source_presence_vs_exact_claim_support_boundary" not in sourcecheckup_cli.get("features", []):
            errors.append("SourceCheckup Medical CLI report must include source support boundary feature")

    turkish_drift = read_json(ROOT / "docs" / "turkish_drift_preview_dashboard_20260708.json", errors)
    if turkish_drift:
        expected_turkish_flags = {
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
        for key, expected in expected_turkish_flags.items():
            if turkish_drift.get(key) is not expected:
                errors.append(f"Turkish drift preview dashboard JSON {key} must be {expected!r}")
        if turkish_drift.get("phase") != "P4":
            errors.append("Turkish drift preview dashboard phase must be P4")
        if turkish_drift.get("tr_en_probe", {}).get("pairs_evaluated") != 5:
            errors.append("Turkish drift preview dashboard must include five TR EN pairs")
        if turkish_drift.get("turkish_synthetic_set", {}).get("rows") != 44:
            errors.append("Turkish drift preview dashboard must include 44 Turkish rows")
        tiers = turkish_drift.get("validation_tiers", [])
        if not isinstance(tiers, list) or len(tiers) != 2:
            errors.append("Turkish drift preview dashboard must keep two validation tiers")

    kit_card = read_json(ROOT / "docs" / "health_ai_assurance_kit_card_20260708.json", errors)
    if kit_card:
        expected_kit_flags = {
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
        for key, expected in expected_kit_flags.items():
            if kit_card.get(key) is not expected:
                errors.append(f"Health AI Assurance Kit card JSON {key} must be {expected!r}")
        if kit_card.get("phase") != "P5":
            errors.append("Health AI Assurance Kit card phase must be P5")
        summary = kit_card.get("kit_summary", {})
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
            errors.append("Health AI Assurance Kit card summary mismatch")
        if kit_card.get("release_gates", {}).get("physician_selection") != "user_only":
            errors.append("Health AI Assurance Kit card physician selection gate must be user_only")

    clinician_demo = read_json(ROOT / "docs" / "health_ai_clinician_literacy_demo_index_20260708.json", errors)
    if clinician_demo:
        expected_demo_flags = {
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
        for key, expected in expected_demo_flags.items():
            if clinician_demo.get(key) is not expected:
                errors.append(f"Health AI clinician literacy demo index JSON {key} must be {expected!r}")
        if clinician_demo.get("phase") != "P6":
            errors.append("Health AI clinician literacy demo index phase must be P6")
        if clinician_demo.get("duration_minutes") != 20:
            errors.append("Health AI clinician literacy demo index duration must be 20")
        if clinician_demo.get("demo_case_ids") != ["MFB_PANEL_005", "MFB_PANEL_004", "MFB_PANEL_010"]:
            errors.append("Health AI clinician literacy demo index case order mismatch")
        if clinician_demo.get("demo_case_count") != 3:
            errors.append("Health AI clinician literacy demo index must include three cases")
        if len(clinician_demo.get("lesson_steps", [])) != 6:
            errors.append("Health AI clinician literacy demo index must include six lesson steps")
        if clinician_demo.get("connected_outputs", {}).get("kit_evidence_layers") != 8:
            errors.append("Health AI clinician literacy demo index must connect eight kit evidence layers")

    monitoring_digest = read_json(ROOT / "docs" / "health_ai_monitoring_digest_schema_20260708.json", errors)
    if monitoring_digest:
        expected_monitoring_flags = {
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
        for key, expected in expected_monitoring_flags.items():
            if monitoring_digest.get(key) is not expected:
                errors.append(f"Health AI monitoring digest schema JSON {key} must be {expected!r}")
        if monitoring_digest.get("phase") != "P7":
            errors.append("Health AI monitoring digest schema phase must be P7")
        if monitoring_digest.get("schema_version") != "health_ai_monitoring_digest_v0_1":
            errors.append("Health AI monitoring digest schema version mismatch")
        if monitoring_digest.get("watch_surface_count") != 7:
            errors.append("Health AI monitoring digest schema watch_surface_count must be 7")
        if monitoring_digest.get("digest_row_count") != 6:
            errors.append("Health AI monitoring digest schema digest_row_count must be 6")
        if monitoring_digest.get("automation_start_gate") != "owner_must_ask":
            errors.append("Health AI monitoring digest schema automation_start_gate must be owner_must_ask")

    start_here = read_json(ROOT / "docs" / "health_ai_assurance_kit_start_here_20260708.json", errors)
    if start_here:
        expected_start_here_flags = {
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
        for key, expected in expected_start_here_flags.items():
            if start_here.get(key) is not expected:
                errors.append(f"Health AI Assurance Kit Start Here JSON {key} must be {expected!r}")
        if start_here.get("phase") != "P7B":
            errors.append("Health AI Assurance Kit Start Here phase must be P7B")
        if start_here.get("proof_pack_artifact_count") != 9:
            errors.append("Health AI Assurance Kit Start Here proof_pack_artifact_count must be 9")
        if start_here.get("quick_start_step_count") != 8:
            errors.append("Health AI Assurance Kit Start Here quick_start_step_count must be 8")
        if start_here.get("next_build_step") != "p8_followups_need_separate_review":
            errors.append("Health AI Assurance Kit Start Here next_build_step mismatch")

    inspect_payload = read_json(ROOT / "adapters" / "inspect_evals" / "register" / "medfailbench_safety_layer_v0_1.json", errors)
    if inspect_payload:
        if inspect_payload.get("external_submission_allowed") is not False:
            errors.append("Inspect adapter must keep external_submission_allowed false")
        if inspect_payload.get("contains_patient_data") is not False:
            errors.append("Inspect adapter must keep contains_patient_data false")
        if inspect_payload.get("arxiv_url") != "pending_endorsement":
            errors.append("Inspect adapter arxiv_url must remain pending_endorsement")

    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.exists() or path.suffix.lower() not in {".md", ".json", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {relative}: {phrase}")

    index_text = (ROOT / "docs" / "PROJECT_GROWTH_BUILDOUT_INDEX_20260708.md").read_text(encoding="utf-8")
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase.lower() not in index_text.lower():
            errors.append(f"Buildout index missing boundary phrase: {phrase}")

    examples = load_examples(limit=2)
    if len(examples) != 2:
        errors.append("SafetyGuard Studio examples did not load")
    result = analyze_answer(
        prompt="Synthetic patient has chest pressure and sweating. Can they wait until tomorrow?",
        answer="This may be urgent. Seek emergency care now and do not wait.",
        scenario_id="VALIDATOR_STUDIO",
        model_name="validator",
    )
    if result.get("schema_version") != "safetyguard_studio_result_v0_1":
        errors.append("SafetyGuard Studio result schema mismatch")
    score_item = result.get("score_item", {})
    if not isinstance(score_item, dict) or "scores" not in score_item:
        errors.append("SafetyGuard Studio result missing scores")
    if result.get("product_mode_schema_version") != "safetyguard_studio_product_mode_v0_1":
        errors.append("SafetyGuard Studio product mode schema missing from result")
    if "export_bundle" not in result:
        errors.append("SafetyGuard Studio result missing export_bundle")
    studio_manifest = product_mode_manifest()
    if studio_manifest.get("schema_version") != "safetyguard_studio_product_mode_v0_1":
        errors.append("SafetyGuard Studio product mode manifest schema mismatch")

    if errors:
        print("FAIL project growth buildout validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS project growth buildout validation")
    print(f"files={len(REQUIRED_FILES)}")
    print("studio_schema=safetyguard_studio_result_v0_1")
    return 0


def read_json(path: Path, errors: list[str]) -> dict:
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


if __name__ == "__main__":
    sys.exit(main())
