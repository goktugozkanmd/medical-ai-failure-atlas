#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "health_ai_clinician_literacy_demo_index_20260708.json"
MD_PATH = ROOT / "docs" / "HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md"

PANEL_CASES_TSV = ROOT / "data" / "panel_pilot" / "clinician_panel_pilot_cases_v0_1.tsv"
DEMO_CASE_IDS = ["MFB_PANEL_005", "MFB_PANEL_004", "MFB_PANEL_010"]

SOURCE_PATHS = {
    "kit_card": ROOT / "docs" / "health_ai_assurance_kit_card_20260708.json",
    "simulator_module": ROOT / "docs" / "clinical_ai_literacy_simulator_module_20260708.json",
    "demo_flow": ROOT / "docs" / "HEALTH_AI_SAFETY_OPS_DEMO_FLOW_20260708.md",
    "panel_cases": PANEL_CASES_TSV,
    "panel_packet": ROOT / "docs" / "clinician_panel_reviewer_packet_20260708.json",
    "medhelm_three_case_packet": ROOT / "docs" / "medhelm_three_case_upstream_packet_v0_1.json",
    "safetyguard_studio": ROOT / "docs" / "safetyguard_studio_product_mode_20260708.json",
    "sourcecheckup_cli": ROOT / "docs" / "sourcecheckup_medical_cli_report_20260708.json",
}


def main() -> int:
    kit_card = read_json(SOURCE_PATHS["kit_card"])
    simulator = read_json(SOURCE_PATHS["simulator_module"])
    panel_packet = read_json(SOURCE_PATHS["panel_packet"])
    medhelm_packet = read_json(SOURCE_PATHS["medhelm_three_case_packet"])
    studio = read_json(SOURCE_PATHS["safetyguard_studio"])
    sourcecheckup = read_json(SOURCE_PATHS["sourcecheckup_cli"])
    panel_cases = read_panel_cases(PANEL_CASES_TSV)
    cases_by_id = {row["panel_case_id"]: row for row in panel_cases}
    demo_cases = [summarize_case(cases_by_id[case_id]) for case_id in DEMO_CASE_IDS]

    manifest = {
        "artifact_id": "health_ai_clinician_literacy_demo_index_20260708",
        "status": "local_clinician_literacy_demo_index_ready",
        "created_date": "2026-07-08",
        "phase": "P6",
        "roadmap": "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
        "product_name": "Clinical AI Safety Ops / Health AI Assurance Kit",
        "index_schema": "health_ai_clinician_literacy_demo_index_v0_1",
        "source_artifacts": {name: str(path.relative_to(ROOT)) for name, path in SOURCE_PATHS.items()},
        "duration_minutes": simulator["duration_minutes"],
        "demo_case_ids": DEMO_CASE_IDS,
        "demo_case_count": len(demo_cases),
        "demo_cases": demo_cases,
        "lesson_steps": [
            {
                "id": "frame_problem",
                "minutes": "0-2",
                "source": "docs/HEALTH_AI_SAFETY_OPS_DEMO_FLOW_20260708.md",
                "objective": "Frame synthetic cases, safety review, and claim boundaries.",
                "show": ["synthetic only boundary", "not a model ranking", "not clinical validation"],
            },
            {
                "id": "case_urgent_escalation",
                "minutes": "2-6",
                "case_id": "MFB_PANEL_005",
                "objective": "Recognize bleeding risk and avoid catch up dosing language.",
                "show": ["synthetic case summary", "expected safety focus", "danger signal question"],
            },
            {
                "id": "case_missing_variable",
                "minutes": "6-10",
                "case_id": "MFB_PANEL_004",
                "objective": "Recognize unsafe remote dosing under missing ketone and DKA context.",
                "show": ["synthetic case summary", "missing variable prompt", "expected safety focus"],
            },
            {
                "id": "case_safe_uncertainty",
                "minutes": "10-14",
                "case_id": "MFB_PANEL_010",
                "objective": "Preserve symptom based escalation instead of hiding behind a number.",
                "show": ["synthetic case summary", "uncertainty boundary", "expected safety focus"],
            },
            {
                "id": "assurance_output",
                "minutes": "14-18",
                "source": "docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
                "objective": "Connect flags to the kit level evidence card.",
                "show": ["SafetyGuard flags", "SourceCheckup gate", "transparency card fields", "claim boundary flags"],
            },
            {
                "id": "close_with_small_ask",
                "minutes": "18-20",
                "source": "docs/HEALTH_AI_SAFETY_OPS_DEMO_FLOW_20260708.md",
                "objective": "Ask only for feedback on education value and failure categories.",
                "show": ["no institution endorsement ask", "no patient data ask", "no public name use ask"],
            },
        ],
        "connected_outputs": {
            "kit_card_schema": kit_card["card_schema"],
            "kit_evidence_layers": kit_card["kit_summary"]["evidence_layer_count"],
            "studio_features": len(studio["features"]),
            "sourcecheckup_report_schema": sourcecheckup["report_schema"],
            "panel_assignment_count": panel_packet["assignment_count"],
            "medhelm_case_count": medhelm_packet["case_count"],
        },
        "screen_sequence": [
            "synthetic_case_text",
            "unsafe_or_incomplete_answer_pattern",
            "missing_danger_signal_prompt",
            "safer_answer_pattern",
            "safetyguard_flag_view",
            "sourcecheckup_claim_support_gate",
            "kit_level_assurance_card",
            "claim_boundary_close",
        ],
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
        "blocked_actions": [
            "send_external_email_or_post_without_user_approval",
            "run_external_presentation_without_user_approval",
            "start_provider_api_calls_without_user_approval",
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
            "connect this index to the roadmap as P6 completed",
            "build the manual monitoring digest schema next",
            "keep any external demo or follow up note blocked until explicit user approval and audit",
        ],
    }
    JSON_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(manifest), encoding="utf-8")
    print(f"Wrote {JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")
    print(f"duration_minutes={manifest['duration_minutes']}")
    print(f"demo_cases={manifest['demo_case_count']}")
    print(f"lesson_steps={len(manifest['lesson_steps'])}")
    return 0


def summarize_case(row: dict[str, str]) -> dict[str, Any]:
    return {
        "case_id": row["panel_case_id"],
        "source_scenario_id": row["source_scenario_id"],
        "language": row["language"],
        "theme": row["theme"],
        "domain": row["domain"],
        "setting": row["setting"],
        "synthetic_patient_summary": row["synthetic_patient_summary"],
        "task_for_model": row["task_for_model"],
        "expected_safety_focus": row["expected_safety_focus"],
        "review_question": row["review_question"],
        "patient_data_status": row["patient_data_status"],
        "rating_status": row["rating_status"],
    }


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Health AI Clinician Literacy Demo Index",
        "",
        "Date: 2026 07 08",
        "",
        "Status: local clinician literacy demo index ready.",
        "",
        "Roadmap phase: P6 Clinician Literacy Demo.",
        "",
        f"Product name: {manifest['product_name']}.",
        "",
        f"Schema: `{manifest['index_schema']}`.",
        "",
        "## Boundary",
        "",
        "No external send, no provider API call, no automation start, no new case addition, no patient data, no physician selection, no medical advice, no clinical validation claim, no source truth certification claim, no regulatory compliance claim, no official compatibility claim, no institution claim, and no model ranking.",
        "",
        "## Demo Summary",
        "",
        f"- Duration: {manifest['duration_minutes']} minutes.",
        f"- Demo cases: {manifest['demo_case_count']}.",
        f"- Lesson steps: {len(manifest['lesson_steps'])}.",
        f"- Connected kit evidence layers: {manifest['connected_outputs']['kit_evidence_layers']}.",
        f"- Panel assignments prepared: {manifest['connected_outputs']['panel_assignment_count']}.",
        "",
        "## Twenty Minute Flow",
        "",
        "| Time | Step | Case | Objective |",
        "| --- | --- | --- | --- |",
    ]
    for step in manifest["lesson_steps"]:
        case = step.get("case_id", "")
        lines.append(f"| {step['minutes']} | `{step['id']}` | `{case}` | {step['objective']} |")
    lines.extend(["", "## Demo Cases", ""])
    for case in manifest["demo_cases"]:
        lines.extend(
            [
                f"### {case['case_id']}",
                "",
                f"- Domain: {case['domain']}.",
                f"- Theme: {case['theme']}.",
                f"- Setting: {case['setting']}.",
                f"- Synthetic summary: {case['synthetic_patient_summary']}.",
                f"- Expected safety focus: {case['expected_safety_focus']}.",
                f"- Patient data status: {case['patient_data_status']}.",
                f"- Rating status: {case['rating_status']}.",
                "",
            ]
        )
    lines.extend(
        [
            "## Screen Sequence",
            "",
        ]
    )
    for item in manifest["screen_sequence"]:
        lines.append(f"- `{item}`.")
    lines.extend(
        [
            "",
            "## Connected Outputs",
            "",
            "| Output | Value |",
            "| --- | --- |",
        ]
    )
    for key, value in manifest["connected_outputs"].items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(["", "## Source Artifacts", ""])
    for name, path in manifest["source_artifacts"].items():
        lines.append(f"- `{name}`: `{path}`.")
    lines.extend(
        [
            "",
            "## Next",
            "",
            "1. Connect this index to the roadmap as P6 completed.",
            "2. Build the manual monitoring digest schema next.",
            "3. Keep any external demo or follow up note blocked until explicit user approval and audit.",
            "",
            "## Validation",
            "",
            "Run:",
            "",
            "```bash",
            "make health_ai_clinician_literacy_demo_index_20260708",
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


def read_panel_cases(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


if __name__ == "__main__":
    raise SystemExit(main())
