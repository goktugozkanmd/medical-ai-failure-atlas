#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_monitoring_digest_schema_20260708.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_MONITORING_DIGEST_SCHEMA_20260708.md"

SOURCE_PATHS = {
    "monitoring_plan": ROOT / "docs" / "medical_ai_safety_monitoring_bot_plan_20260708.json",
    "benchmark_boundary_index": ROOT / "docs" / "medical_ai_benchmark_boundary_index_20260708.json",
    "kit_card": ROOT / "docs" / "health_ai_assurance_kit_card_20260708.json",
    "clinician_literacy_demo_index": ROOT / "docs" / "health_ai_clinician_literacy_demo_index_20260708.json",
    "sourcecheckup_cli": ROOT / "docs" / "sourcecheckup_medical_cli_report_20260708.json",
    "turkish_drift_dashboard": ROOT / "docs" / "turkish_drift_preview_dashboard_20260708.json",
    "global_network_roadmap": ROOT / "docs" / "GLOBAL_NETWORK_EXPANSION_ROADMAP_20260708.md",
}


SCHEMA_FIELDS = [
    {
        "name": "digest_id",
        "required": True,
        "meaning": "Stable row id for a manually reviewed monitoring signal.",
    },
    {
        "name": "date_checked",
        "required": True,
        "meaning": "Date when the source was manually checked.",
    },
    {
        "name": "signal_surface",
        "required": True,
        "meaning": "Benchmark, model release, governance, source support, language drift, adapter route, repo health, or outreach route.",
    },
    {
        "name": "source_locator",
        "required": True,
        "meaning": "Local file path or explicit source pointer used for the row.",
    },
    {
        "name": "observed_change",
        "required": True,
        "meaning": "What changed or what needs attention, written as a bounded internal note.",
    },
    {
        "name": "evidence_status",
        "required": True,
        "meaning": "local_artifact, official_source_needed, user_approval_needed, blocked, or no_change.",
    },
    {
        "name": "action_meaning",
        "required": True,
        "meaning": "What this means for the Health AI Assurance Kit roadmap.",
    },
    {
        "name": "risk_tags",
        "required": True,
        "meaning": "Controlled tags such as source_support, language_drift, external_claim, adapter_route, or automation_boundary.",
    },
    {
        "name": "blocked_claims",
        "required": True,
        "meaning": "Claims that must not be made from this row.",
    },
    {
        "name": "external_action_gate",
        "required": True,
        "meaning": "blocked_without_user_approval for any external post, email, PR, comment, provider run, or institution named claim.",
    },
]


WATCH_SURFACES = [
    {
        "id": "benchmark_and_eval_ecosystem",
        "local_source": "docs/MEDICAL_AI_BENCHMARK_BOUNDARY_INDEX_20260708.md",
        "manual_question": "Did a benchmark or eval ecosystem signal change the local boundary language?",
        "allowed_action": "update internal boundary note",
    },
    {
        "id": "source_support_and_claims",
        "local_source": "docs/SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md",
        "manual_question": "Did a medical or policy claim need exact source support review?",
        "allowed_action": "add internal SourceCheckup review row",
    },
    {
        "id": "turkish_and_non_english_drift",
        "local_source": "docs/TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md",
        "manual_question": "Did Turkish or English wording drift create a safety review need?",
        "allowed_action": "update internal drift note without adding new cases",
    },
    {
        "id": "adapter_and_distribution_routes",
        "local_source": "adapters/README.md",
        "manual_question": "Did an adapter route need a local wrapper, smoke test, or blocked external packet?",
        "allowed_action": "prepare local adapter evidence only",
    },
    {
        "id": "clinician_literacy_and_review",
        "local_source": "docs/HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md",
        "manual_question": "Did the demo or panel review state need an internal update?",
        "allowed_action": "update local demo index or review status only",
    },
    {
        "id": "governance_and_network_routes",
        "local_source": "docs/GLOBAL_NETWORK_EXPANSION_ROADMAP_20260708.md",
        "manual_question": "Did a governance or network route need a bounded next action?",
        "allowed_action": "write a local draft only",
    },
    {
        "id": "repo_health_and_public_claim_hygiene",
        "local_source": "docs/PROJECT_GROWTH_BUILDOUT_INDEX_20260708.md",
        "manual_question": "Did validators, CI, or public claim hygiene change?",
        "allowed_action": "run local QA and update BAGLAM2",
    },
]


def main() -> int:
    sources = {name: read_json(path) if path.suffix == ".json" else {"path": str(path.relative_to(ROOT))} for name, path in SOURCE_PATHS.items()}
    monitoring_plan = sources["monitoring_plan"]
    boundary_index = sources["benchmark_boundary_index"]
    kit_card = sources["kit_card"]
    demo_index = sources["clinician_literacy_demo_index"]
    sourcecheckup_cli = sources["sourcecheckup_cli"]
    turkish_drift = sources["turkish_drift_dashboard"]

    digest_rows = [
        {
            "digest_id": "HMD001",
            "date_checked": "2026-07-08",
            "signal_surface": "benchmark_and_eval_ecosystem",
            "source_locator": "docs/medical_ai_benchmark_boundary_index_20260708.json",
            "observed_change": "Boundary index lists benchmark lanes and blocked claims for HealthBench, MedHELM, MedFailBench, SourceCheckup, and Turkish Clinical SafetyBench.",
            "evidence_status": boundary_index["status"],
            "action_meaning": "Use benchmark signals as design lenses, not as compatibility or endorsement claims.",
            "risk_tags": ["benchmark_boundary", "external_claim"],
            "blocked_claims": ["benchmark_equivalence", "official_compatibility", "clinical_validation", "model_ranking"],
            "external_action_gate": "blocked_without_user_approval",
        },
        {
            "digest_id": "HMD002",
            "date_checked": "2026-07-08",
            "signal_surface": "monitoring_boundary",
            "source_locator": "docs/medical_ai_safety_monitoring_bot_plan_20260708.json",
            "observed_change": "Monitoring plan exists but automation is not started.",
            "evidence_status": monitoring_plan["status"],
            "action_meaning": "Keep monitoring as manual digest rows until the owner explicitly asks to start automation.",
            "risk_tags": ["automation_boundary", "owner_gate"],
            "blocked_claims": ["automation_started", "external_monitoring_active", "paid_run_allowed"],
            "external_action_gate": "blocked_without_user_approval",
        },
        {
            "digest_id": "HMD003",
            "date_checked": "2026-07-08",
            "signal_surface": "kit_level_evidence",
            "source_locator": "docs/health_ai_assurance_kit_card_20260708.json",
            "observed_change": "Kit card connects eight local evidence layers and keeps the external gate blocked.",
            "evidence_status": kit_card["status"],
            "action_meaning": "Use the kit card as the internal anchor for digest interpretation.",
            "risk_tags": ["kit_card", "claim_boundary"],
            "blocked_claims": ["clinical_validation", "source_truth_certification", "regulatory_compliance", "model_ranking"],
            "external_action_gate": kit_card["kit_summary"]["external_gate"],
        },
        {
            "digest_id": "HMD004",
            "date_checked": "2026-07-08",
            "signal_surface": "clinician_literacy_and_review",
            "source_locator": "docs/health_ai_clinician_literacy_demo_index_20260708.json",
            "observed_change": "Clinician literacy demo index has a 20 minute, three case, six step local flow.",
            "evidence_status": demo_index["status"],
            "action_meaning": "Route education signals into local demo updates, not external presentation claims.",
            "risk_tags": ["clinician_literacy", "human_review"],
            "blocked_claims": ["institution_claim", "medical_advice", "clinical_validation", "physician_selection_by_agent"],
            "external_action_gate": "blocked_without_user_approval",
        },
        {
            "digest_id": "HMD005",
            "date_checked": "2026-07-08",
            "signal_surface": "source_support_and_claims",
            "source_locator": "docs/sourcecheckup_medical_cli_report_20260708.json",
            "observed_change": "SourceCheckup CLI keeps source presence separate from exact claim support.",
            "evidence_status": sourcecheckup_cli["status"],
            "action_meaning": "Any source bearing medical claim should become an internal review row before public wording.",
            "risk_tags": ["source_support", "claim_hygiene"],
            "blocked_claims": ["source_truth_certification", "unsupported_guideline_claim", "unsupported_policy_claim"],
            "external_action_gate": "blocked_without_user_approval",
        },
        {
            "digest_id": "HMD006",
            "date_checked": "2026-07-08",
            "signal_surface": "turkish_and_non_english_drift",
            "source_locator": "docs/turkish_drift_preview_dashboard_20260708.json",
            "observed_change": "Turkish drift dashboard keeps two validation tiers, five TR EN pairs, and 44 existing Turkish synthetic rows.",
            "evidence_status": turkish_drift["status"],
            "action_meaning": "Language drift signals stay separated by validation tier and do not create new case claims.",
            "risk_tags": ["language_drift", "validation_tier"],
            "blocked_claims": ["new_case_validation", "model_ranking", "clinical_validation"],
            "external_action_gate": "blocked_without_user_approval",
        },
    ]
    manifest = {
        "artifact_id": "health_ai_monitoring_digest_schema_20260708",
        "status": "manual_monitoring_digest_schema_ready",
        "created_date": "2026-07-08",
        "phase": "P7",
        "roadmap": "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
        "product_name": "Clinical AI Safety Ops / Health AI Assurance Kit",
        "schema_version": "health_ai_monitoring_digest_v0_1",
        "manual_only": True,
        "automation_start_gate": "owner_must_ask",
        "source_artifacts": {name: str(path.relative_to(ROOT)) for name, path in SOURCE_PATHS.items()},
        "schema_fields": SCHEMA_FIELDS,
        "watch_surfaces": WATCH_SURFACES,
        "sample_digest_rows": digest_rows,
        "digest_row_count": len(digest_rows),
        "watch_surface_count": len(WATCH_SURFACES),
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
        "blocked_actions": [
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
        ],
        "next_safe_actions": [
            "connect this schema to the roadmap as P7 completed",
            "keep P8 external proof route blocked without explicit user approval",
            "use digest rows only as internal BAGLAM2 style decision support",
        ],
    }
    JSON_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(manifest), encoding="utf-8")
    print(f"Wrote {JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")
    print(f"schema_fields={len(SCHEMA_FIELDS)}")
    print(f"watch_surfaces={len(WATCH_SURFACES)}")
    print(f"digest_rows={len(digest_rows)}")
    return 0


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Health AI Monitoring Digest Schema",
        "",
        "Date: 2026 07 08",
        "",
        "Status: manual monitoring digest schema ready.",
        "",
        "Roadmap phase: P7 Monitoring Digest.",
        "",
        f"Product name: {manifest['product_name']}.",
        "",
        f"Schema: `{manifest['schema_version']}`.",
        "",
        "## Boundary",
        "",
        "Manual only. No external send, no provider API call, no automation start, no paid run, no new case addition, no patient data, no physician selection, no medical advice, no clinical validation claim, no source truth certification claim, no regulatory compliance claim, no official compatibility claim, no institution claim, and no model ranking.",
        "",
        f"Automation start gate: `{manifest['automation_start_gate']}`.",
        "",
        "## Schema Fields",
        "",
        "| Field | Required | Meaning |",
        "| --- | --- | --- |",
    ]
    for field in manifest["schema_fields"]:
        lines.append(f"| `{field['name']}` | `{str(field['required']).lower()}` | {field['meaning']} |")
    lines.extend(["", "## Watch Surfaces", "", "| Surface | Local source | Manual question | Allowed action |", "| --- | --- | --- | --- |"])
    for surface in manifest["watch_surfaces"]:
        lines.append(
            f"| `{surface['id']}` | `{surface['local_source']}` | {surface['manual_question']} | {surface['allowed_action']} |"
        )
    lines.extend(["", "## Sample Digest Rows", "", "| Id | Surface | Evidence status | Action meaning | External gate |", "| --- | --- | --- | --- | --- |"])
    for row in manifest["sample_digest_rows"]:
        lines.append(
            f"| `{row['digest_id']}` | `{row['signal_surface']}` | `{row['evidence_status']}` | {row['action_meaning']} | `{row['external_action_gate']}` |"
        )
    lines.extend(["", "## Blocked Claims By Row", ""])
    for row in manifest["sample_digest_rows"]:
        claims = ", ".join(f"`{claim}`" for claim in row["blocked_claims"])
        lines.append(f"- `{row['digest_id']}`: {claims}.")
    lines.extend(["", "## Source Artifacts", ""])
    for name, path in manifest["source_artifacts"].items():
        lines.append(f"- `{name}`: `{path}`.")
    lines.extend(
        [
            "",
            "## Next",
            "",
            "1. Connect this schema to the roadmap as P7 completed.",
            "2. Keep P8 external proof route blocked without explicit user approval.",
            "3. Use digest rows only as internal BAGLAM2 style decision support.",
            "",
            "## Validation",
            "",
            "Run:",
            "",
            "```bash",
            "make health_ai_monitoring_digest_schema_20260708",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path.relative_to(ROOT)} must be a JSON object")
    return payload


if __name__ == "__main__":
    raise SystemExit(main())
