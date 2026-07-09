#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_assurance_product_packet_20260709.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_PRODUCT_PACKET_20260709.md"

SOURCE_ARTIFACTS = [
    {
        "id": "readme",
        "phase": "public_entry",
        "path": "README.md",
        "role": "Top level repository navigation.",
    },
    {
        "id": "roadmap",
        "phase": "P0_P8",
        "path": "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
        "role": "Canonical Health AI Assurance Kit roadmap and lane map.",
    },
    {
        "id": "start_here",
        "phase": "P7B",
        "path": "docs/HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md",
        "role": "Local proof pack entry point.",
    },
    {
        "id": "kit_card",
        "phase": "P5",
        "path": "docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
        "role": "Kit level evidence card and blocked gate summary.",
    },
    {
        "id": "safety_ops_positioning",
        "phase": "product_positioning",
        "path": "docs/HEALTH_AI_SAFETY_OPS_POSITIONING_20260708.md",
        "role": "Product positioning for Clinical AI Safety Ops.",
    },
    {
        "id": "growth_buildout_index",
        "phase": "growth_spine",
        "path": "docs/PROJECT_GROWTH_BUILDOUT_INDEX_20260708.md",
        "role": "Buildout index for project growth artifacts.",
    },
    {
        "id": "feedback_intake_md",
        "phase": "P9",
        "path": "docs/HEALTH_AI_ASSURANCE_FEEDBACK_INTAKE_20260708.md",
        "role": "Public feedback intake routes.",
    },
    {
        "id": "feedback_intake_json",
        "phase": "P9",
        "path": "docs/health_ai_assurance_feedback_intake_20260708.json",
        "role": "Machine readable feedback intake manifest.",
    },
    {
        "id": "feedback_triage_board_md",
        "phase": "P10",
        "path": "docs/HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_BOARD_20260708.md",
        "role": "Maintainer triage board for public feedback.",
    },
    {
        "id": "feedback_triage_board_json",
        "phase": "P10",
        "path": "docs/health_ai_assurance_feedback_triage_board_20260708.json",
        "role": "Machine readable feedback triage board.",
    },
    {
        "id": "feedback_triage_examples_md",
        "phase": "P11",
        "path": "docs/HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_EXAMPLES_20260709.md",
        "role": "Synthetic maintainer decision examples.",
    },
    {
        "id": "feedback_triage_examples_json",
        "phase": "P11",
        "path": "docs/health_ai_assurance_feedback_triage_examples_20260709.json",
        "role": "Machine readable triage example records.",
    },
]

PHASE_SPINE = [
    {
        "phase": "P0",
        "name": "Product Spine",
        "state": "completed",
        "artifact": "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
    },
    {
        "phase": "P1",
        "name": "Safety Evidence Spine",
        "state": "completed",
        "artifact": "docs/LOCAL_LEADERBOARD_DRAFT_PREVIEW_20260708.md",
    },
    {
        "phase": "P2",
        "name": "Studio Product Mode",
        "state": "completed",
        "artifact": "docs/SAFETYGUARD_STUDIO_PRODUCT_MODE_20260708.md",
    },
    {
        "phase": "P3",
        "name": "SourceCheckup Medical CLI",
        "state": "completed",
        "artifact": "docs/SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md",
    },
    {
        "phase": "P4",
        "name": "Turkish Drift Preview",
        "state": "completed",
        "artifact": "docs/TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md",
    },
    {
        "phase": "P5",
        "name": "Kit Level Assurance Card",
        "state": "completed",
        "artifact": "docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
    },
    {
        "phase": "P6",
        "name": "Clinician Literacy Demo",
        "state": "completed",
        "artifact": "docs/HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md",
    },
    {
        "phase": "P7",
        "name": "Monitoring Digest",
        "state": "completed",
        "artifact": "docs/HEALTH_AI_MONITORING_DIGEST_SCHEMA_20260708.md",
    },
    {
        "phase": "P7B",
        "name": "Start Here Proof Pack",
        "state": "completed",
        "artifact": "docs/HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md",
    },
    {
        "phase": "P8",
        "name": "External Proof Route",
        "state": "first_public_issue_opened",
        "artifact": "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231",
    },
    {
        "phase": "P9",
        "name": "Feedback Intake",
        "state": "completed",
        "artifact": "docs/HEALTH_AI_ASSURANCE_FEEDBACK_INTAKE_20260708.md",
    },
    {
        "phase": "P10",
        "name": "Feedback Triage Board",
        "state": "completed",
        "artifact": "docs/HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_BOARD_20260708.md",
    },
    {
        "phase": "P11",
        "name": "Feedback Triage Examples",
        "state": "completed",
        "artifact": "docs/HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_EXAMPLES_20260709.md",
    },
]


def main() -> int:
    intake = read_json(ROOT / "docs" / "health_ai_assurance_feedback_intake_20260708.json")
    triage = read_json(ROOT / "docs" / "health_ai_assurance_feedback_triage_board_20260708.json")
    examples = read_json(ROOT / "docs" / "health_ai_assurance_feedback_triage_examples_20260709.json")

    manifest = {
        "artifact_id": "health_ai_assurance_product_packet_20260709",
        "status": "internal_product_packet_ready",
        "created_date": "2026-07-09",
        "phase": "P12",
        "product_name": "Clinical AI Safety Ops / Health AI Assurance Kit",
        "purpose": "Package P0 through P11 into one reviewable product packet before any further external follow up.",
        "public_anchor": "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231",
        "source_artifacts": SOURCE_ARTIFACTS,
        "source_artifact_count": len(SOURCE_ARTIFACTS),
        "phase_spine": PHASE_SPINE,
        "phase_spine_count": len(PHASE_SPINE),
        "feedback_loop": {
            "phases": ["P9", "P10", "P11"],
            "route_count": intake.get("route_count"),
            "small_task_count": intake.get("small_task_count"),
            "triage_state_count": triage.get("triage_state_count"),
            "board_row_count": triage.get("board_row_count"),
            "decision_type_count": examples.get("decision_type_count"),
            "example_record_count": examples.get("example_record_count"),
            "public_anchor": examples.get("public_anchor"),
        },
        "review_packet_steps": [
            "Start with README navigation.",
            "Open the Health AI Assurance Kit Start Here proof pack.",
            "Use the roadmap to see the P0 through P11 build spine.",
            "Use the kit card to keep evidence layers and blocked gates together.",
            "Use P9 feedback intake to choose one public feedback route.",
            "Use P10 triage board to classify the feedback state.",
            "Use P11 examples to draft narrow maintainer decisions.",
            "Stop before any external follow up that needs separate owner review.",
        ],
        "review_packet_step_count": 8,
        "release_gates": {
            "internal_product_packet": "ready",
            "external_followup": "separate_owner_review_required",
            "provider_api_run": "blocked_without_owner_approval",
            "new_case_addition": "blocked_without_owner_approval",
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
        "next_build_step": "p12_product_packet_ready_for_review",
        "next_safe_action": "Review this product packet, rerun CI, and only then decide whether to merge or open any further public follow up.",
    }

    JSON_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(manifest), encoding="utf-8")
    print(f"Wrote {JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")
    print("phase=P12")
    print(f"source_artifacts={manifest['source_artifact_count']}")
    print(f"feedback_loop_phases={len(manifest['feedback_loop']['phases'])}")
    return 0


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Health AI Assurance Product Packet",
        "",
        "Date: 2026 07 09",
        "",
        "Status: internal product packet ready.",
        "",
        "Roadmap phase: P12 product packet.",
        "",
        f"Product name: {manifest['product_name']}.",
        "",
        "## Purpose",
        "",
        "This packet turns P0 through P11 into one reviewable product entry. It is the handoff layer between the internal proof pack, the public feedback route, and future owner reviewed follow up.",
        "",
        "## Boundary",
        "",
        "No external send, no public follow up, no provider API call, no automation start, no paid run, no new case addition, no patient data, no private clinical text, no raw clinical notes, no private model output, no physician selection, no medical advice, no clinical validation claim, no model ranking, no source truth certification claim, no regulatory compliance claim, no official compatibility claim, no institution support claim, no partnership claim, no payment claim, and no terms acceptance claim.",
        "",
        "## One Screen Summary",
        "",
        f"- Phase: `{manifest['phase']}`.",
        f"- Source artifacts: {manifest['source_artifact_count']}.",
        f"- Phase spine entries: {manifest['phase_spine_count']}.",
        f"- Feedback loop phases: {len(manifest['feedback_loop']['phases'])}.",
        f"- Feedback routes: {manifest['feedback_loop']['route_count']}.",
        f"- Triage states: {manifest['feedback_loop']['triage_state_count']}.",
        f"- Triage examples: {manifest['feedback_loop']['example_record_count']}.",
        f"- Public anchor: {manifest['public_anchor']}.",
        f"- Next build step: `{manifest['next_build_step']}`.",
        "",
        "## P0 Through P11 Spine",
        "",
        "| Phase | Name | State | Artifact |",
        "| --- | --- | --- | --- |",
    ]
    for item in manifest["phase_spine"]:
        artifact = item["artifact"]
        if artifact.startswith("http"):
            artifact_cell = artifact
        else:
            artifact_cell = f"`{artifact}`"
        lines.append(f"| {item['phase']} | {item['name']} | `{item['state']}` | {artifact_cell} |")

    lines.extend(
        [
            "",
            "## Source Artifacts",
            "",
            "| Id | Phase | Path | Role |",
            "| --- | --- | --- | --- |",
        ]
    )
    for artifact in manifest["source_artifacts"]:
        lines.append(
            f"| `{artifact['id']}` | `{artifact['phase']}` | `{artifact['path']}` | {artifact['role']} |"
        )

    lines.extend(
        [
            "",
            "## Feedback Loop",
            "",
            "| Layer | Count |",
            "| --- | --- |",
            f"| P9 routes | {manifest['feedback_loop']['route_count']} |",
            f"| P9 small reviewer tasks | {manifest['feedback_loop']['small_task_count']} |",
            f"| P10 triage states | {manifest['feedback_loop']['triage_state_count']} |",
            f"| P10 board rows | {manifest['feedback_loop']['board_row_count']} |",
            f"| P11 decision types | {manifest['feedback_loop']['decision_type_count']} |",
            f"| P11 example records | {manifest['feedback_loop']['example_record_count']} |",
            "",
            "## Review Packet Steps",
            "",
        ]
    )
    for index, step in enumerate(manifest["review_packet_steps"], start=1):
        lines.append(f"{index}. {step}")

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
            "## Next Safe Action",
            "",
            manifest["next_safe_action"],
            "",
            "## Rebuild",
            "",
            "```bash",
            "make health_ai_assurance_product_packet_20260709",
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
