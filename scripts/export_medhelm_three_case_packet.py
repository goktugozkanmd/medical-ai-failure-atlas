#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from failure_atlas.panel_review import DEFAULT_PANEL_CASES_PATH, PanelCase, load_panel_cases

OUT_JSON = ROOT / "docs" / "medhelm_three_case_upstream_packet_v0_1.json"
OUT_MD = ROOT / "docs" / "MEDHELM_THREE_CASE_UPSTREAM_PACKET_V0_1.md"
SELECTED_CASE_IDS = ("MFB_PANEL_004", "MFB_PANEL_005", "MFB_PANEL_010")
GATE_BY_CASE_ID = {
    "MFB_PANEL_004": "unsafe_remote_dosing",
    "MFB_PANEL_005": "unsafe_remote_dosing",
    "MFB_PANEL_010": "missed_urgent_escalation",
}


def main() -> int:
    cases = load_panel_cases(DEFAULT_PANEL_CASES_PATH)
    selected = select_cases(cases)
    packet = build_packet(selected)
    OUT_JSON.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(build_markdown(packet), encoding="utf-8")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    return 0


def select_cases(cases: list[PanelCase]) -> list[PanelCase]:
    case_map = {case.panel_case_id: case for case in cases}
    missing = [case_id for case_id in SELECTED_CASE_IDS if case_id not in case_map]
    if missing:
        raise SystemExit(f"Missing panel case IDs: {missing}")
    return [case_map[case_id] for case_id in SELECTED_CASE_IDS]


def build_packet(cases: list[PanelCase]) -> dict[str, object]:
    return {
        "schema_version": "medfailbench_medhelm_three_case_packet_v0_1",
        "status": "draft_not_posted_not_medhelm_endorsed",
        "purpose": "Small MedHELM oriented discussion packet for synthetic clinician safety gate cases.",
        "source_data": str(DEFAULT_PANEL_CASES_PATH.relative_to(ROOT)),
        "case_count": len(cases),
        "boundaries": {
            "synthetic_only": True,
            "patient_data_used": False,
            "clinical_use_allowed": False,
            "claims_blocked": [
                "clinical validation",
                "model ranking",
                "deployment readiness",
                "official endorsement",
                "benchmark compatibility",
            ],
        },
        "cases": [adapt_case(case) for case in cases],
    }


def adapt_case(case: PanelCase) -> dict[str, object]:
    task_family = "patient_communication" if case.setting.lower() == "patient message" else "clinical_decision_support"
    return {
        "scenario_name": f"medfailbench_panel_{case.panel_case_id.lower()}",
        "source_case_id": case.panel_case_id,
        "source_scenario_id": case.source_scenario_id,
        "medhelm_task_family_lens": task_family,
        "clinical_domain": case.domain,
        "setting": case.setting,
        "synthetic_patient_summary": case.synthetic_patient_summary,
        "task_for_model": case.task_for_model,
        "expected_safety_focus": case.expected_safety_focus,
        "candidate_safety_gate": GATE_BY_CASE_ID[case.panel_case_id],
        "review_question": case.review_question,
        "synthetic_only": True,
        "patient_data_used": False,
        "clinical_use_allowed": False,
    }


def build_markdown(packet: dict[str, object]) -> str:
    cases = packet["cases"]
    assert isinstance(cases, list)
    lines = [
        "# MedHELM Three Case Upstream Packet v0.1",
        "",
        "Status: draft only. Not posted. Not endorsed by MedHELM.",
        "",
        "Purpose: provide a compact synthetic discussion packet for clinician safety gate review.",
        "",
        "Boundary:",
        "",
        "1. Synthetic cases only.",
        "2. No patient data.",
        "3. Not clinical validation.",
        "4. Not a model ranking.",
        "5. Not a deployment readiness claim.",
        "6. Not an official endorsement claim.",
        "7. Not a benchmark compatibility claim.",
        "",
        "Cases:",
        "",
    ]
    for index, case in enumerate(cases, start=1):
        assert isinstance(case, dict)
        lines.extend(
            [
                f"{index}. `{case['source_case_id']}`",
                f"   Domain: {case['clinical_domain']}",
                f"   Task family lens: {case['medhelm_task_family_lens']}",
                f"   Summary: {case['synthetic_patient_summary']}",
                f"   Task: {case['task_for_model']}",
                f"   Safety focus: {case['expected_safety_focus']}",
                f"   Candidate safety gate: `{case['candidate_safety_gate']}`",
                "",
            ]
        )
    lines.extend(
        [
            "Use:",
            "",
            "Ask maintainers whether this should be a discussion, an issue, a small scenario example, or a separate local adapter artifact.",
            "",
            "Do not post this text externally before a fresh audit and owner approval.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
