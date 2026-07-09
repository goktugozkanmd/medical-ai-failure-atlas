#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_assurance_kit_card_20260708.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md"

SOURCE_PATHS = {
    "roadmap": ROOT / "docs" / "health_ai_assurance_kit_roadmap_20260708.json",
    "safetyguard_studio": ROOT / "docs" / "safetyguard_studio_product_mode_20260708.json",
    "sourcecheckup_cli": ROOT / "docs" / "sourcecheckup_medical_cli_report_20260708.json",
    "turkish_drift": ROOT / "docs" / "turkish_drift_preview_dashboard_20260708.json",
    "transparency_export": ROOT / "docs" / "safetyguard_evaluation_card_export_path_20260708.json",
    "clinician_panel_packet": ROOT / "docs" / "clinician_panel_reviewer_packet_20260708.json",
    "clinician_literacy": ROOT / "docs" / "clinical_ai_literacy_simulator_module_20260708.json",
    "monitoring_plan": ROOT / "docs" / "medical_ai_safety_monitoring_bot_plan_20260708.json",
    "promotion_gate": ROOT / "docs" / "model_run_promotion_gate_20260708.json",
}


def main() -> int:
    sources = {name: read_json(path) for name, path in SOURCE_PATHS.items()}
    studio = sources["safetyguard_studio"]
    sourcecheckup = sources["sourcecheckup_cli"]
    drift = sources["turkish_drift"]
    transparency = sources["transparency_export"]
    panel = sources["clinician_panel_packet"]
    literacy = sources["clinician_literacy"]
    monitoring = sources["monitoring_plan"]
    promotion = sources["promotion_gate"]

    manifest = {
        "artifact_id": "health_ai_assurance_kit_card_20260708",
        "status": "local_kit_level_assurance_card_ready",
        "created_date": "2026-07-08",
        "phase": "P5",
        "roadmap": "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
        "product_name": "Clinical AI Safety Ops / Health AI Assurance Kit",
        "card_schema": "health_ai_assurance_kit_card_v0_1",
        "source_artifacts": {name: str(path.relative_to(ROOT)) for name, path in SOURCE_PATHS.items()},
        "evidence_layers": [
            {
                "id": "safety_evidence_spine",
                "label": "Safety evidence spine",
                "status": "local_promoted_score_review_ready",
                "source": "docs/model_run_promotion_gate_20260708.json",
                "signals": {
                    "models_ready_for_local_promotion_review": promotion["totals"]["models_ready_for_local_promotion_review"],
                    "local_rows_scored": promotion["totals"]["local_rows_scored"],
                    "provider_generation_rows_used": promotion["totals"]["provider_generation_rows_used"],
                },
                "public_claim_boundary": "local score review only, not model ranking",
            },
            {
                "id": "safetyguard_studio_surface",
                "label": "SafetyGuard Studio surface",
                "status": studio["status"],
                "source": "docs/safetyguard_studio_product_mode_20260708.json",
                "signals": {
                    "features": len(studio["features"]),
                    "endpoints": len(studio["endpoints"]),
                    "sample_review_status": studio["sample_smoke"]["review_status"],
                },
                "public_claim_boundary": "local synthetic/manual review surface only",
            },
            {
                "id": "source_support_layer",
                "label": "SourceCheckup Medical source support",
                "status": sourcecheckup["status"],
                "source": "docs/sourcecheckup_medical_cli_report_20260708.json",
                "signals": {
                    "report_schema": sourcecheckup["report_schema"],
                    "sample_external_use_gate": sourcecheckup["sample_result"]["external_use_gate"],
                    "verification_queue_count": sourcecheckup["sample_result"]["verification_queue_count"],
                },
                "public_claim_boundary": "source presence is separated from exact claim support",
            },
            {
                "id": "turkish_drift_layer",
                "label": "Turkish and English drift preview",
                "status": drift["status"],
                "source": "docs/turkish_drift_preview_dashboard_20260708.json",
                "signals": {
                    "validation_tiers": len(drift["validation_tiers"]),
                    "tr_en_pairs": drift["tr_en_probe"]["pairs_evaluated"],
                    "probe_outputs": drift["tr_en_probe"]["outputs_evaluated"],
                    "turkish_rows": drift["turkish_synthetic_set"]["rows"],
                    "sourcecheckup_needed_rows": drift["turkish_synthetic_set"]["sourcecheckup_needed_rows"],
                    "high_severity_rows": drift["turkish_synthetic_set"]["high_severity_rows"],
                },
                "public_claim_boundary": "small probe and existing Turkish synthetic rows stay separate",
            },
            {
                "id": "transparency_card_layer",
                "label": "Transparency card export path",
                "status": transparency["status"],
                "source": "docs/safetyguard_evaluation_card_export_path_20260708.json",
                "signals": {
                    "outputs": transparency["outputs"],
                    "local_smoke_status": transparency["local_smoke"]["status"],
                    "external_submission_allowed": transparency["external_submission_allowed"],
                },
                "public_claim_boundary": "export path only, no registry acceptance claim",
            },
            {
                "id": "human_review_status_layer",
                "label": "Human review status",
                "status": panel["status"],
                "source": "docs/clinician_panel_reviewer_packet_20260708.json",
                "signals": {
                    "case_count": panel["case_count"],
                    "assignment_count": panel["assignment_count"],
                    "external_send_allowed": panel["external_send_allowed"],
                    "reviewer_selection_owner": "user",
                },
                "public_claim_boundary": "review packet prepared, external reviewer selection remains with the user",
            },
            {
                "id": "clinician_literacy_layer",
                "label": "Clinician literacy demo layer",
                "status": literacy["status"],
                "source": "docs/clinical_ai_literacy_simulator_module_20260708.json",
                "signals": {
                    "duration_minutes": literacy["duration_minutes"],
                    "steps": len(literacy["steps"]),
                    "external_action_allowed": literacy["external_action_allowed"],
                },
                "public_claim_boundary": "local education module only, not medical advice",
            },
            {
                "id": "monitoring_boundary_layer",
                "label": "Monitoring boundary",
                "status": monitoring["status"],
                "source": "docs/medical_ai_safety_monitoring_bot_plan_20260708.json",
                "signals": {
                    "automation_started": monitoring["automation_started"],
                    "external_action_allowed": monitoring["external_action_allowed"],
                    "start_gate": monitoring["start_gate"],
                },
                "public_claim_boundary": "plan only, automation not started",
            },
        ],
        "release_gates": {
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
        },
        "kit_summary": {
            "evidence_layer_count": 8,
            "local_rows_scored": promotion["totals"]["local_rows_scored"],
            "tr_en_pairs": drift["tr_en_probe"]["pairs_evaluated"],
            "turkish_rows": drift["turkish_synthetic_set"]["rows"],
            "sourcecheckup_needed_rows": drift["turkish_synthetic_set"]["sourcecheckup_needed_rows"],
            "human_review_assignments_prepared": panel["assignment_count"],
            "external_gate": "blocked_without_user_approval",
        },
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
        "blocked_actions": [
            "send_external_email_or_post_without_user_approval",
            "start_provider_api_calls_without_user_approval",
            "add_new_cases_without_user_approval",
            "claim_clinical_validation",
            "claim_source_truth_certification",
            "claim_regulatory_compliance",
            "claim_official_endorsement_or_compatibility",
            "rank_models_as_winners",
            "select_or_contact_physicians_by_agent",
        ],
        "next_safe_actions": [
            "use this card as the kit level internal index",
            "connect the clinician literacy demo into the next roadmap phase",
            "keep external release blocked until explicit user approval and audit",
        ],
    }
    JSON_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(manifest), encoding="utf-8")
    print(f"Wrote {JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")
    print(f"evidence_layers={manifest['kit_summary']['evidence_layer_count']}")
    print(f"turkish_rows={manifest['kit_summary']['turkish_rows']}")
    print(f"external_gate={manifest['kit_summary']['external_gate']}")
    return 0


def render_markdown(manifest: dict[str, Any]) -> str:
    summary = manifest["kit_summary"]
    lines = [
        "# Health AI Assurance Kit Card",
        "",
        "Date: 2026 07 08",
        "",
        "Status: local kit level assurance card ready.",
        "",
        "Roadmap phase: P5 Kit Level Assurance Card.",
        "",
        f"Product name: {manifest['product_name']}.",
        "",
        f"Schema: `{manifest['card_schema']}`.",
        "",
        "## Boundary",
        "",
        "No external send, no provider API call, no automation start, no new case addition, no patient data, no physician selection, no clinical validation claim, no source truth certification claim, no regulatory compliance claim, no official compatibility claim, and no model ranking.",
        "",
        "## Kit Summary",
        "",
        f"- Evidence layers: {summary['evidence_layer_count']}.",
        f"- Local scored rows: {summary['local_rows_scored']}.",
        f"- TR EN pairs: {summary['tr_en_pairs']}.",
        f"- Turkish synthetic rows: {summary['turkish_rows']}.",
        f"- SourceCheckup needed rows: {summary['sourcecheckup_needed_rows']}.",
        f"- Human review assignments prepared: {summary['human_review_assignments_prepared']}.",
        f"- External gate: `{summary['external_gate']}`.",
        "",
        "## Evidence Layers",
        "",
        "| Layer | Status | Source | Main signals | Boundary |",
        "| --- | --- | --- | --- | --- |",
    ]
    for layer in manifest["evidence_layers"]:
        signals = "; ".join(f"{key}={format_signal(value)}" for key, value in layer["signals"].items())
        lines.append(
            f"| {layer['label']} | `{layer['status']}` | `{layer['source']}` | {signals} | {layer['public_claim_boundary']} |"
        )
    lines.extend(
        [
            "",
            "## Release Gates",
            "",
            "| Gate | State |",
            "| --- | --- |",
        ]
    )
    for gate, state in manifest["release_gates"].items():
        lines.append(f"| `{gate}` | `{state}` |")
    lines.extend(
        [
            "",
            "## Source Artifacts",
            "",
        ]
    )
    for name, path in manifest["source_artifacts"].items():
        lines.append(f"- `{name}`: `{path}`.")
    lines.extend(
        [
            "",
            "## Next",
            "",
            "1. Use this as the kit level internal index.",
            "2. Connect the clinician literacy demo into the next roadmap phase.",
            "3. Keep external release blocked until explicit user approval and audit.",
            "",
            "## Validation",
            "",
            "Run:",
            "",
            "```bash",
            "make health_ai_assurance_kit_card_20260708",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def format_signal(value: Any) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(str(item) for item in value) + "]"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path.relative_to(ROOT)} must be a JSON object")
    return payload


if __name__ == "__main__":
    raise SystemExit(main())
