#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "docs" / "reviewer_question_release_gate_checklist_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_release_gate_outcome_dashboard_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md"


def build_rows(checklist: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(checklist["rows"], start=1):
        rows.append(
            {
                "outcome_id": f"RQRGO{index:03d}",
                "release_gate_id": item["release_gate_id"],
                "gate_name": item["gate_name"],
                "intake_id": item["intake_id"],
                "benchmark_reviewer_question_id": item["benchmark_reviewer_question_id"],
                "current_state": item["current_state"],
                "release_decision": item["release_decision"],
                "required_public_wording": item["required_public_wording"],
                "blocked_wording": item["blocked_wording"],
                "evidence_surface": item["evidence_surface"],
                "track_a_value": item["track_a_value"],
                "track_b_value": item["track_b_value"],
                "next_action": "keep public preview wording",
            }
        )
    return rows


def render_markdown(data: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Reviewer question release gate outcome dashboard v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This dashboard summarizes pass and block outcomes across reviewer question release gate rows.",
        "",
        "It is not clinical advice, not patient data, not raw model output, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Outcome rows: {data['outcome_row_count']}",
        "",
        f"Pass state rows: {data['pass_state_count']}",
        "",
        f"Block state rows: {data['block_state_count']}",
        "",
        f"Release decision values represented: {data['release_decision_count']}",
        "",
        "Release decision: `allowed_for_public_preview`",
        "",
        "## Outcome rows",
        "",
    ]

    for row in data["rows"]:
        lines.extend(
            [
                f"### {row['outcome_id']}",
                "",
                f"Release gate id: `{row['release_gate_id']}`",
                "",
                f"Gate name: {row['gate_name']}",
                "",
                f"Intake id: `{row['intake_id']}`",
                "",
                f"Reviewer question id: `{row['benchmark_reviewer_question_id']}`",
                "",
                f"Current state: `{row['current_state']}`",
                "",
                f"Release decision: `{row['release_decision']}`",
                "",
                f"Required public wording: {row['required_public_wording']}",
                "",
                f"Blocked wording: {row['blocked_wording']}",
                "",
                f"Evidence surface: {row['evidence_surface']}",
                "",
                f"Track A value: {row['track_a_value']}",
                "",
                f"Track B value: {row['track_b_value']}",
                "",
                f"Next action: {row['next_action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Public files",
            "",
            "1. Outcome dashboard JSON: `docs/reviewer_question_release_gate_outcome_dashboard_v0_1.json`",
            "2. Release gate checklist: `docs/REVIEWER_QUESTION_RELEASE_GATE_CHECKLIST_V0_1.md`",
            "3. Public wording decision log: `docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md`",
            "4. Maintainer triage board: `docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md`",
            "5. Intake examples: `docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md`",
            "",
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make reviewer_question_gate_outcomes",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question public release packet without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    checklist = json.loads(CHECKLIST.read_text(encoding="utf-8"))
    rows = build_rows(checklist)
    state_counts = Counter(row["current_state"] for row in rows)
    decision_counts = Counter(row["release_decision"] for row in rows)
    data: dict[str, Any] = {
        "artifact": "reviewer_question_release_gate_outcome_dashboard_v0_1",
        "date": "2026 06 17",
        "status": "generated public preview",
        "source_artifact": "reviewer_question_release_gate_checklist_v0_1",
        "outcome_row_count": len(rows),
        "pass_state_count": state_counts.get("pass", 0),
        "block_state_count": state_counts.get("block", 0),
        "release_decision_count": len(decision_counts),
        "contains_patient_data": False,
        "synthetic_examples_only": True,
        "not_for_clinical_use": True,
        "no_raw_model_output_release": True,
        "no_endpoint_result": True,
        "no_score_report": True,
        "no_model_ranking": True,
        "no_benchmark_compatibility_claim": True,
        "no_benchmark_equivalence_claim": True,
        "no_clinical_deployment_claim": True,
        "no_clinical_validation_claim": True,
        "no_official_endorsement_claim": True,
        "rows": rows,
    }
    JSON_OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MD_OUTPUT.write_text(render_markdown(data), encoding="utf-8")
    print(f"wrote {MD_OUTPUT.relative_to(ROOT)}")
    print(f"wrote {JSON_OUTPUT.relative_to(ROOT)}")
    print(f"outcome_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
