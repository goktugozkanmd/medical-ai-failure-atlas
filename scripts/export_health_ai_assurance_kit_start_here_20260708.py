#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_assurance_kit_start_here_20260708.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md"

SOURCE_PATHS = {
    "roadmap_json": ROOT / "docs" / "health_ai_assurance_kit_roadmap_20260708.json",
    "roadmap_md": ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
    "kit_card_json": ROOT / "docs" / "health_ai_assurance_kit_card_20260708.json",
    "kit_card_md": ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
    "safetyguard_studio": ROOT / "docs" / "safetyguard_studio_product_mode_20260708.json",
    "sourcecheckup_cli": ROOT / "docs" / "sourcecheckup_medical_cli_report_20260708.json",
    "turkish_drift": ROOT / "docs" / "turkish_drift_preview_dashboard_20260708.json",
    "clinician_literacy": ROOT / "docs" / "health_ai_clinician_literacy_demo_index_20260708.json",
    "monitoring_digest": ROOT / "docs" / "health_ai_monitoring_digest_schema_20260708.json",
    "local_leaderboard_preview": ROOT / "docs" / "local_leaderboard_draft_preview_20260708.json",
    "adapter_framework_smoke": ROOT / "docs" / "medfailbench_adapter_framework_smoke_20260708.json",
}


def main() -> int:
    sources = {name: read_json(path) for name, path in SOURCE_PATHS.items() if path.suffix == ".json"}
    roadmap = sources["roadmap_json"]
    kit_card = sources["kit_card_json"]
    studio = sources["safetyguard_studio"]
    sourcecheckup = sources["sourcecheckup_cli"]
    turkish_drift = sources["turkish_drift"]
    clinician = sources["clinician_literacy"]
    monitoring = sources["monitoring_digest"]
    preview = sources["local_leaderboard_preview"]
    adapter_smoke = sources["adapter_framework_smoke"]

    proof_pack = [
        proof_item(
            "roadmap",
            "Roadmap",
            "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
            "Shows the full Clinical AI Safety Ops build direction and completed phases.",
            "Does not allow external release or institution named claims.",
        ),
        proof_item(
            "kit_card",
            "Kit level assurance card",
            "docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
            "Connects eight local evidence layers into one internal card.",
            "Does not claim clinical validation, source truth certification, model ranking, or regulatory compliance.",
        ),
        proof_item(
            "safetyguard_studio",
            "SafetyGuard Studio product mode",
            "docs/SAFETYGUARD_STUDIO_PRODUCT_MODE_20260708.md",
            f"Local product surface with {len(studio.get('features', []))} features and {len(studio.get('endpoints', []))} endpoints.",
            "Does not call provider APIs or make deployment claims.",
        ),
        proof_item(
            "sourcecheckup_cli",
            "SourceCheckup Medical CLI report",
            "docs/SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md",
            f"Runnable source support report with schema {sourcecheckup.get('report_schema')}.",
            "Does not certify exact claim support without separate review.",
        ),
        proof_item(
            "turkish_drift_dashboard",
            "Turkish drift preview dashboard",
            "docs/TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md",
            f"Tracks {turkish_drift.get('tr_en_probe', {}).get('pairs_evaluated')} TR EN pairs and {turkish_drift.get('turkish_synthetic_set', {}).get('rows')} existing Turkish synthetic rows.",
            "Does not merge validation tiers or create new case claims.",
        ),
        proof_item(
            "clinician_literacy_demo",
            "Clinician literacy demo index",
            "docs/HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md",
            f"Local {clinician.get('duration_minutes')} minute demo with {clinician.get('demo_case_count')} synthetic cases.",
            "Does not select physicians, give medical advice, or claim institution support.",
        ),
        proof_item(
            "monitoring_digest_schema",
            "Monitoring digest schema",
            "docs/HEALTH_AI_MONITORING_DIGEST_SCHEMA_20260708.md",
            f"Manual monitoring schema with {monitoring.get('watch_surface_count')} watch surfaces and {monitoring.get('digest_row_count')} sample rows.",
            "Does not start automation or paid runs.",
        ),
        proof_item(
            "local_leaderboard_preview",
            "Local leaderboard draft preview",
            "docs/LOCAL_LEADERBOARD_DRAFT_PREVIEW_20260708.md",
            f"Local preview closes {preview.get('draft_scope', {}).get('public_rows_closed_by_local_artifacts')} public rows from existing artifacts.",
            "Does not modify the public leaderboard or rank models as winners.",
        ),
        proof_item(
            "adapter_framework_smoke",
            "Adapter framework smoke",
            "docs/MEDFAILBENCH_ADAPTER_FRAMEWORK_SMOKE_20260708.md",
            f"Local adapter smoke status: {adapter_smoke.get('status')}.",
            "Does not claim registry acceptance or upstream compatibility.",
        ),
    ]

    quick_start = [
        {
            "id": "read_start_here",
            "order": 1,
            "action": "Open this Start Here file first.",
            "why": "It maps every local proof artifact and repeats the blocked gates.",
        },
        {
            "id": "read_roadmap",
            "order": 2,
            "action": "Read the Health AI Assurance Kit roadmap.",
            "why": "It shows the lane structure, the opened P8 issue, and the follow up review gates.",
        },
        {
            "id": "read_kit_card",
            "order": 3,
            "action": "Read the kit level assurance card.",
            "why": "It is the single evidence layer summary.",
        },
        {
            "id": "try_studio_locally",
            "order": 4,
            "action": "Use SafetyGuard Studio only as a local synthetic or manual answer surface.",
            "why": "It gives a practical product view without provider calls.",
        },
        {
            "id": "run_sourcecheckup_locally",
            "order": 5,
            "action": "Use SourceCheckup Medical for internal source support review.",
            "why": "It keeps source presence separate from exact claim support.",
        },
        {
            "id": "review_language_drift",
            "order": 6,
            "action": "Check the Turkish drift dashboard before language claims.",
            "why": "It preserves validation tier separation.",
        },
        {
            "id": "review_demo_index",
            "order": 7,
            "action": "Use the clinician literacy demo index for local education flow only.",
            "why": "It keeps medical advice and institution claims blocked.",
        },
        {
            "id": "stop_at_external_gate",
            "order": 8,
            "action": "Use issue 231 as the first public proof route and stop before any further external action.",
            "why": "Any follow up email, post, PR, provider run, clinical panel work, or institution named route still needs separate review.",
        },
    ]

    completed_phases = [
        phase.get("phase")
        for phase in roadmap.get("phases", [])
        if isinstance(phase, dict) and phase.get("status") == "completed"
    ]
    kit_summary = kit_card.get("kit_summary", {})

    manifest = {
        "artifact_id": "health_ai_assurance_kit_start_here_20260708",
        "status": "local_start_here_proof_pack_ready",
        "created_date": "2026-07-08",
        "phase": "P7B",
        "roadmap": "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
        "product_name": "Clinical AI Safety Ops / Health AI Assurance Kit",
        "purpose": "Give a single local entry point for the P0 through P7 Health AI Assurance Kit artifacts before any external proof route.",
        "source_artifacts": {name: str(path.relative_to(ROOT)) for name, path in SOURCE_PATHS.items()},
        "quick_start_order": quick_start,
        "quick_start_step_count": len(quick_start),
        "proof_pack_artifacts": proof_pack,
        "proof_pack_artifact_count": len(proof_pack),
        "completed_roadmap_phases": completed_phases,
        "completed_roadmap_phase_count": len(completed_phases),
        "summary_counts": {
            "evidence_layers": kit_summary.get("evidence_layer_count"),
            "local_rows_scored": kit_summary.get("local_rows_scored"),
            "tr_en_pairs": kit_summary.get("tr_en_pairs"),
            "turkish_rows": kit_summary.get("turkish_rows"),
            "human_review_assignments_prepared": kit_summary.get("human_review_assignments_prepared"),
            "monitoring_watch_surfaces": monitoring.get("watch_surface_count"),
            "monitoring_sample_rows": monitoring.get("digest_row_count"),
        },
        "release_gate_summary": {
            "internal_start_here": "ready",
            "external_proof_route": "first_public_issue_opened",
            "provider_api_run": "separate_review_required",
            "new_case_addition": "separate_review_required",
            "physician_selection": "user_only",
            "automation_start": "owner_must_ask",
        },
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
        "external_proof_issue": "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231",
        "next_build_step": "p8_followups_need_separate_review",
        "next_safe_internal_action": "Prepare separate reviewed routes for any follow up PR, provider run, panel work, or institution named action.",
    }

    JSON_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(manifest), encoding="utf-8")
    print(f"Wrote {JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")
    print(f"proof_pack_artifacts={manifest['proof_pack_artifact_count']}")
    print(f"quick_start_steps={manifest['quick_start_step_count']}")
    print(f"next_build_step={manifest['next_build_step']}")
    return 0


def proof_item(
    item_id: str,
    label: str,
    source: str,
    what_it_shows: str,
    does_not_show: str,
) -> dict[str, str]:
    return {
        "id": item_id,
        "label": label,
        "source": source,
        "what_it_shows": what_it_shows,
        "does_not_show": does_not_show,
    }


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Health AI Assurance Kit Start Here",
        "",
        "Date: 2026 07 08",
        "",
        "Status: local start here proof pack ready.",
        "",
        "Roadmap phase: P7B internal hardening.",
        "",
        f"Product name: {manifest['product_name']}.",
        "",
        "## What This Is",
        "",
        "This is the local entry point for the Clinical AI Safety Ops / Health AI Assurance Kit. It points to the roadmap, kit card, product surfaces, language drift review, source support review, clinician literacy demo, monitoring digest, and adapter smoke artifacts.",
        "",
        "## Boundary",
        "",
        "No external send, no public submission, no provider API call, no automation start, no paid run, no new case addition, no patient data, no physician selection, no medical advice, no clinical validation claim, no source truth certification claim, no regulatory compliance claim, no official compatibility claim, no institution claim, and no model ranking.",
        "",
        "## One Screen Summary",
        "",
        f"- Completed roadmap phases: {manifest['completed_roadmap_phase_count']}.",
        f"- Evidence layers: {manifest['summary_counts']['evidence_layers']}.",
        f"- Local scored rows: {manifest['summary_counts']['local_rows_scored']}.",
        f"- TR EN pairs: {manifest['summary_counts']['tr_en_pairs']}.",
        f"- Turkish synthetic rows: {manifest['summary_counts']['turkish_rows']}.",
        f"- Human review assignments prepared: {manifest['summary_counts']['human_review_assignments_prepared']}.",
        f"- Monitoring watch surfaces: {manifest['summary_counts']['monitoring_watch_surfaces']}.",
        f"- Monitoring sample rows: {manifest['summary_counts']['monitoring_sample_rows']}.",
        f"- Next build step: `{manifest['next_build_step']}`.",
        "",
        "## Quick Start Order",
        "",
        "| Order | Step | Why |",
        "| --- | --- | --- |",
    ]
    for step in manifest["quick_start_order"]:
        lines.append(f"| {step['order']} | {step['action']} | {step['why']} |")
    lines.extend(
        [
            "",
            "## Proof Pack Artifacts",
            "",
            "| Artifact | Source | What it shows | What it does not show |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in manifest["proof_pack_artifacts"]:
        lines.append(
            f"| {item['label']} | `{item['source']}` | {item['what_it_shows']} | {item['does_not_show']} |"
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
    for gate, state in manifest["release_gate_summary"].items():
        lines.append(f"| `{gate}` | `{state}` |")
    lines.extend(
        [
            "",
            "## Source Artifacts",
            "",
            "| Label | Path |",
            "| --- | --- |",
        ]
    )
    for label, path in manifest["source_artifacts"].items():
        lines.append(f"| `{label}` | `{path}` |")
    lines.extend(
        [
            "",
            "## Rebuild",
            "",
            "```bash",
            "make health_ai_assurance_kit_start_here_20260708",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {}
    return payload


if __name__ == "__main__":
    raise SystemExit(main())
