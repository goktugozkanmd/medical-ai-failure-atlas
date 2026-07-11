#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_assurance_kit_roadmap_20260708.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md"


LANES = [
    {
        "id": "safety_gap_layer",
        "name": "Safety Gap Layer",
        "purpose": "Inspect worst answers, missed escalation, unsafe reassurance, missing clinical variables, and source support gaps.",
        "current_artifacts": [
            "safetyguard/studio.py",
            "docs/SAFETYGUARD_STUDIO_PRODUCT_MODE_20260708.md",
            "docs/MODEL_RUN_NORMALIZATION_PLAN_20260708.md",
            "docs/MODEL_RUN_PROMOTION_GATE_20260708.md",
            "docs/LOCAL_LEADERBOARD_DRAFT_PREVIEW_20260708.md",
            "docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
        ],
        "next_build": "clinician_literacy_demo_index",
    },
    {
        "id": "adapter_distribution_layer",
        "name": "Adapter Distribution Layer",
        "purpose": "Make the safety layer runnable where evaluators already work.",
        "current_artifacts": [
            "adapters/README.md",
            "docs/MEDFAILBENCH_LOCAL_ADAPTER_WRAPPERS_20260708.md",
            "docs/MEDFAILBENCH_ADAPTER_FRAMEWORK_SMOKE_20260708.md",
        ],
        "next_build": "upstream_ready_packet_without_external_submit",
    },
    {
        "id": "sourcecheckup_medical_layer",
        "name": "SourceCheckup Medical Layer",
        "purpose": "Separate source presence from exact medical claim support.",
        "current_artifacts": [
            "docs/SOURCECHECKUP_MEDICAL_PRODUCT_PACKET_20260708.md",
            "docs/SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md",
            "docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
            "docs/sourcecheckup/SOURCECHECKUP_REPO_RUN_GUIDE_V0_1.md",
            "sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl",
        ],
        "next_build": "included_in_kit_level_card",
    },
    {
        "id": "turkish_drift_layer",
        "name": "Turkish and Non English Drift Layer",
        "purpose": "Track Turkish clinical wording risk, meaning loss, escalation drift, and source support drift.",
        "current_artifacts": [
            "docs/TURKISH_CLINICAL_SAFETYBENCH_PACKAGING_GATE_20260708.md",
            "docs/TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md",
            "docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
            "data/tr_en_drift_glm_probe_v0_1.tsv",
            "data/tr_medllm_synthetic_eval_set_v0_3.jsonl",
        ],
        "next_build": "included_in_kit_level_card",
    },
    {
        "id": "transparency_card_layer",
        "name": "Transparency and Assurance Card Layer",
        "purpose": "Convert evaluation runs into readable evidence cards with limits, prompt set, model version, and review status.",
        "current_artifacts": [
            "scripts/export_safetyguard_transparency_card.py",
            "docs/SAFETYGUARD_EVALUATION_CARD_EXPORT_PATH_20260708.md",
            "docs/SAFETYGUARD_CARD_RELEASE_NOTE_DRAFT_20260708.md",
            "docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
            "docs/HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md",
        ],
        "next_build": "start_here_proof_pack_completed",
    },
    {
        "id": "clinician_literacy_layer",
        "name": "Clinician Literacy Simulator",
        "purpose": "Turn synthetic failure cases into a short training and demo workflow.",
        "current_artifacts": [
            "docs/CLINICAL_AI_LITERACY_SIMULATOR_MODULE_20260708.md",
            "docs/HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md",
            "docs/HEALTH_AI_SAFETY_OPS_DEMO_FLOW_20260708.md",
            "failure_atlas/panel_console.py",
        ],
        "next_build": "monitoring_digest_schema",
    },
    {
        "id": "monitoring_layer",
        "name": "Medical AI Safety Monitoring Layer",
        "purpose": "Track benchmark, governance, model release, and issue route changes for internal decision support.",
        "current_artifacts": [
            "docs/MEDICAL_AI_SAFETY_MONITORING_BOT_PLAN_20260708.md",
            "docs/HEALTH_AI_MONITORING_DIGEST_SCHEMA_20260708.md",
            "docs/MEDICAL_AI_BENCHMARK_BOUNDARY_INDEX_20260708.md",
            "docs/GLOBAL_NETWORK_EXPANSION_ROADMAP_20260708.md",
        ],
        "next_build": "p8_external_proof_route_issue_opened",
    },
]


PHASES = [
    {
        "phase": "P0",
        "name": "Product Spine",
        "status": "completed",
        "build": "Create a canonical roadmap, lane manifest, and local validation target for the full Health AI Assurance Kit.",
    },
    {
        "phase": "P1",
        "name": "Safety Evidence Spine",
        "status": "completed",
        "build": "Create local leaderboard draft preview from promoted 30 prompt score files without changing the public leaderboard.",
    },
    {
        "phase": "P2",
        "name": "Studio Product Mode",
        "status": "completed",
        "build": "Turn SafetyGuard Studio from local scorer into a guided product surface with sample mode, answer paste, and export links.",
    },
    {
        "phase": "P3",
        "name": "SourceCheckup Medical CLI",
        "status": "completed",
        "build": "Produce a runnable medical claim support report from synthetic answers and optional source locators.",
    },
    {
        "phase": "P4",
        "name": "Turkish Drift Preview",
        "status": "completed",
        "build": "Create a small Turkish and English drift dashboard with explicit validation tier labeling.",
    },
    {
        "phase": "P5",
        "name": "Kit Level Assurance Card",
        "status": "completed",
        "build": "Generate one kit level assurance card that links safety gaps, source support, transparency, Turkish drift, and human review status.",
    },
    {
        "phase": "P6",
        "name": "Clinician Literacy Demo",
        "status": "completed",
        "build": "Package the 20 minute synthetic demo into a reusable local lesson index.",
    },
    {
        "phase": "P7",
        "name": "Monitoring Digest",
        "status": "completed",
        "build": "Create a manual digest schema before any automation loop is allowed.",
    },
    {
        "phase": "P7B",
        "name": "Start Here Proof Pack",
        "status": "completed",
        "build": "Create one local entry point that maps the roadmap, kit card, product surfaces, language drift, source support, demo, monitoring, and blocked gates.",
    },
    {
        "phase": "P8",
        "name": "External Proof Route",
        "status": "first_public_issue_opened",
        "build": "Open the first public proof route issue after explicit user approval, with further external actions kept behind separate review.",
    },
]


def main() -> int:
    manifest = {
        "artifact_id": "health_ai_assurance_kit_roadmap_20260708",
        "status": "canonical_big_project_roadmap",
        "created_date": "2026-07-08",
        "project_name": "Clinical AI Safety Ops / Health AI Assurance Kit",
        "one_sentence": (
            "A clinician built safety ops layer that helps inspect worst answers, missed escalation, "
            "missing clinical variables, source support, Turkish and English drift, transparency, "
            "and public claim hygiene before teams make claims about a medical AI system."
        ),
        "external_action_allowed": False,
        "provider_api_call_allowed": False,
        "automation_started": False,
        "new_cases_added": False,
        "agent_selected_physicians": False,
        "contains_patient_data": False,
        "no_clinical_validation_claim": True,
        "no_model_ranking": True,
        "no_official_compatibility_claim": True,
        "strategic_decision": "Do not build another broad medical benchmark; build the safety, assurance, source support, and transparency layer around existing evaluation ecosystems.",
        "lanes": LANES,
        "phases": PHASES,
        "current_build_focus": "p8_external_proof_route_issue_opened",
        "next_build_step": "p8_followups_need_separate_review",
        "external_proof_route": {
            "status": "first_public_issue_opened",
            "issue": "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231",
            "followup_gate": "separate_review_required",
        },
        "proof_pack_definition": [
            "SafetyGuard Studio local scoring",
            "SourceCheckup Medical claim support review",
            "Transparency card generated from a run",
            "Turkish and English drift review",
            "Clinician literacy demo material",
            "Monitoring digest route",
            "Start Here proof pack index",
        ],
        "blocked_actions": [
            "send_external_email_or_post_without_user_approval",
            "start_provider_api_calls_without_user_approval",
            "add_new_cases_without_user_approval",
            "claim_clinical_validation",
            "claim_regulatory_compliance",
            "claim_official_endorsement_or_compatibility",
            "rank_models_as_winners",
            "select_or_contact_physicians_by_agent",
        ],
    }
    JSON_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(manifest), encoding="utf-8")
    print(f"Wrote {JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")
    print(f"lanes={len(LANES)}")
    print(f"phases={len(PHASES)}")
    print(f"next_build_step={manifest['next_build_step']}")
    return 0


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Health AI Assurance Kit Roadmap",
        "",
        "Date: 2026 07 08",
        "",
        "Status: canonical big project roadmap.",
        "",
        f"Project name: {manifest['project_name']}.",
        "",
        "## Direction",
        "",
        manifest["one_sentence"],
        "",
        "Strategic decision: do not build another broad medical benchmark. Build the safety, assurance, source support, Turkish drift, transparency, clinician literacy, and monitoring layer around existing evaluation ecosystems.",
        "",
        "## Boundary",
        "",
        "No external send, no provider API call, no automation start, no new case addition, no patient data, no physician selection, no clinical validation claim, no regulatory compliance claim, no official compatibility claim, and no model ranking.",
        "",
        "## Product Lanes",
        "",
        "| Lane | Purpose | Current artifacts | Next build |",
        "| --- | --- | --- | --- |",
    ]
    for lane in manifest["lanes"]:
        artifacts = ", ".join(f"`{path}`" for path in lane["current_artifacts"])
        lines.append(f"| {lane['name']} | {lane['purpose']} | {artifacts} | `{lane['next_build']}` |")
    lines.extend(
        [
            "",
            "## Build Phases",
            "",
            "| Phase | Name | Status | Build |",
            "| --- | --- | --- | --- |",
        ]
    )
    for phase in manifest["phases"]:
        lines.append(f"| {phase['phase']} | {phase['name']} | `{phase['status']}` | {phase['build']} |")
    lines.extend(
        [
            "",
            "## Current Build Focus",
            "",
            f"Current focus: `{manifest['current_build_focus']}`.",
            "",
            f"Next build step: `{manifest['next_build_step']}`.",
            "",
            "## Proof Pack",
            "",
        ]
    )
    for item in manifest["proof_pack_definition"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Validation",
            "",
            "Run:",
            "",
            "```bash",
            "make health_ai_assurance_kit_roadmap_20260708",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
