#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_intake_examples_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md"
OUT_JSON = ROOT / "docs" / "reviewer_question_intake_triage_board_v0_1.json"


ROLE_BY_BLOCKED_CLAIM = {
    "source truth certification": ("RQTR001", "Source evidence reviewer"),
    "official policy proof": ("RQTR002", "Policy wording reviewer"),
    "false reassurance safety proof": ("RQTR003", "Escalation boundary reviewer"),
    "clinical advice": ("RQTR004", "Medication safety reviewer"),
}

ACTION_BY_INTAKE = {
    "RQINT001": "route to source support queue",
    "RQINT002": "route to policy wording review",
    "RQINT003": "route to escalation boundary review",
    "RQINT004": "route to medication safety review",
}

DECISION_BY_INTAKE = {
    "RQINT001": "say locator is not evidence",
    "RQINT002": "say policy source is required",
    "RQINT003": "say escalation remains visible",
    "RQINT004": "say individualized medication advice is blocked",
}

SURFACE_BY_TEMPLATE = {
    "sourcecheckup_review": "SourceCheckup public contributor issue",
    "synthetic_failure_case": "Failure Atlas case intake checklist",
}


def build_rows(examples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for example in examples:
        blocked_claim = str(example["blocked_claim_type"])
        role_id, role_name = ROLE_BY_BLOCKED_CLAIM[blocked_claim]
        intake_id = str(example["intake_id"])
        rows.append(
            {
                "intake_id": intake_id,
                "template": example["template"],
                "benchmark_reviewer_question_id": example["benchmark_reviewer_question_id"],
                "owner_role_id": role_id,
                "owner_role_name": role_name,
                "review_state": "synthetic_preview_only",
                "blocked_public_claim_type": blocked_claim,
                "maintainer_action": ACTION_BY_INTAKE[intake_id],
                "triage_status": "ready_for_maintainer_review",
                "public_wording_decision": DECISION_BY_INTAKE[intake_id],
                "next_public_surface": SURFACE_BY_TEMPLATE[str(example["template"])],
                "track_a_value": example["track_a_value"],
                "track_b_value": example["track_b_value"],
            }
        )
    return rows


def render_markdown(payload: dict[str, Any]) -> str:
    rows = payload["rows"]
    role_counts = Counter(f"{row['owner_role_id']} {row['owner_role_name']}" for row in rows)
    status_counts = Counter(row["triage_status"] for row in rows)

    lines = [
        "# Reviewer question intake triage board v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This board turns synthetic reviewer question intake examples into maintainer actions, owner roles, triage status values, and next public wording decisions.",
        "",
        "It is not clinical advice, not patient data, not raw model output, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Maintainer triage rows: {payload['triage_row_count']}",
        "",
        f"Owner roles represented: {payload['owner_role_count']}",
        "",
        f"Maintainer actions represented: {payload['maintainer_action_count']}",
        "",
        f"Public wording decisions represented: {payload['public_wording_decision_count']}",
        "",
        f"Triage status values represented: {payload['triage_status_count']}",
        "",
        "## Owner role summary",
        "",
    ]
    for role, count in sorted(role_counts.items()):
        lines.append(f"1. `{role}`: {count}")
        lines.append("")

    lines.extend(["## Triage status summary", ""])
    for status, count in sorted(status_counts.items()):
        lines.append(f"1. `{status}`: {count}")
        lines.append("")

    lines.extend(["## Triage rows", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['intake_id']}: {row['template']}",
                "",
                f"Reviewer question id: `{row['benchmark_reviewer_question_id']}`",
                "",
                f"Owner role: `{row['owner_role_id']}` {row['owner_role_name']}",
                "",
                f"Review state: `{row['review_state']}`",
                "",
                f"Blocked public claim type: {row['blocked_public_claim_type']}",
                "",
                f"Maintainer action: {row['maintainer_action']}",
                "",
                f"Triage status: `{row['triage_status']}`",
                "",
                f"Public wording decision: {row['public_wording_decision']}",
                "",
                f"Next public surface: {row['next_public_surface']}",
                "",
                f"Track A value: {row['track_a_value']}",
                "",
                f"Track B value: {row['track_b_value']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Public files",
            "",
            "1. Triage board JSON: `docs/reviewer_question_intake_triage_board_v0_1.json`",
            "2. Intake examples: `docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md`",
            "3. Intake examples JSON: `docs/reviewer_question_intake_examples_v0_1.json`",
            "4. SourceCheckup contributor guide: `docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md`",
            "5. Failure Atlas checklist: `failure_atlas/public/CASE_INTAKE_CHECKLIST_V0_1.md`",
            "",
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make reviewer_question_intake_triage",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a public wording decision log for reviewer question intake triage without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = build_rows(source["examples"])
    payload = {
        "artifact": "reviewer_question_intake_triage_board_v0_1",
        "date": "2026 06 17",
        "status": "generated public preview",
        "source_artifact": "reviewer_question_intake_examples_v0_1",
        "triage_row_count": len(rows),
        "owner_role_count": len({row["owner_role_id"] for row in rows}),
        "maintainer_action_count": len({row["maintainer_action"] for row in rows}),
        "public_wording_decision_count": len({row["public_wording_decision"] for row in rows}),
        "triage_status_count": len({row["triage_status"] for row in rows}),
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
    MARKDOWN.write_text(render_markdown(payload), encoding="utf-8")
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MARKDOWN.relative_to(ROOT)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
