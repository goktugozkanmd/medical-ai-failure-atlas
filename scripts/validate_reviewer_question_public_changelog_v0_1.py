#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_public_changelog_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_PUBLIC_CHANGELOG_V0_1.md"

REQUIRED_CHANGE_IDS = {
    "RQRC001",
    "RQRC002",
    "RQRC003",
    "RQRC004",
    "RQRC005",
    "RQRC006",
    "RQRC007",
    "RQRC008",
}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_PUBLIC_CHANGELOG_V0_1.md",
    "docs/reviewer_question_public_changelog_v0_1.json",
    "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/CONTRIBUTOR_ISSUE_TEMPLATE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
    "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
    "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/REVIEWER_QUESTION_RELEASE_GATE_CHECKLIST_V0_1.md",
    "docs/REVIEWER_QUESTION_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
    "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_PACKET_V0_1.md",
]
REQUIRED_PHRASES = [
    "Reviewer question public changelog v0.1",
    "Change rows: 8",
    "Release packet rows represented: 7",
    "Latest change id: `RQRC008`",
    "ready_for_public_preview",
    "Benchmark style reviewer questions",
    "Contributor issue template reviewer questions",
    "Reviewer question intake examples",
    "Reviewer question intake triage board",
    "Reviewer question public wording decision log",
    "Reviewer question release gate checklist",
    "Reviewer question release gate outcome dashboard",
    "Reviewer question public release packet",
    "public_preview_added",
    "synthetic only and not for clinical use",
    "not clinical advice",
    "not patient data",
    "not raw model output release",
    "not clinical deployment",
    "not clinical validation",
    "not a benchmark compatibility claim",
    "not a benchmark equivalence claim",
    "not a score report",
    "not a model ranking",
    "not an endpoint result",
    "not an official endorsement",
    "make reviewer_question_changelog",
    "Add a reviewer question maintainer audit trail packet without scoring",
]
FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "official approval",
    "official acceptance",
    "sandbox access granted",
    "patient data used",
    "model is safe",
    "best model",
    "benchmark compatible",
    "score improved",
]


def main() -> int:
    errors: list[str] = []
    if not SOURCE.exists():
        errors.append(f"Missing source JSON: {SOURCE.relative_to(ROOT)}")
        data: dict[str, Any] = {"rows": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    rows = data.get("rows", [])
    if not isinstance(rows, list):
        errors.append("rows must be a list")
        rows = []
    if data.get("change_row_count") != 8:
        errors.append("change_row_count must be 8")
    if data.get("release_packet_rows_represented") != 7:
        errors.append("release_packet_rows_represented must be 7")
    if data.get("latest_change_id") != "RQRC008":
        errors.append("latest_change_id must be RQRC008")
    if data.get("changelog_decision") != "ready_for_public_preview":
        errors.append("changelog_decision must be ready_for_public_preview")
    if len(rows) != 8:
        errors.append(f"Expected 8 change rows, found {len(rows)}")

    for field in [
        "contains_patient_data",
        "synthetic_examples_only",
        "not_for_clinical_use",
        "no_raw_model_output_release",
        "no_endpoint_result",
        "no_score_report",
        "no_model_ranking",
        "no_benchmark_compatibility_claim",
        "no_benchmark_equivalence_claim",
        "no_clinical_deployment_claim",
        "no_clinical_validation_claim",
        "no_official_endorsement_claim",
    ]:
        expected = False if field == "contains_patient_data" else True
        if data.get(field) is not expected:
            errors.append(f"{field} must be {expected}")

    change_ids = {str(row.get("change_id")) for row in rows}
    statuses = {str(row.get("change_status")) for row in rows}
    if change_ids != REQUIRED_CHANGE_IDS:
        errors.append("change id set must match required ids")
    if statuses != {"public_preview_added"}:
        errors.append("all change statuses must be public_preview_added")

    for row in rows:
        change_id = str(row.get("change_id", ""))
        for key in ["date", "surface_name", "public_file", "public_value", "change_status", "boundary", "next_action"]:
            if key not in row:
                errors.append(f"{change_id}: missing {key}")

    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).exists():
            errors.append(f"Referenced file does not exist: {relative_path}")

    if not MARKDOWN.exists():
        errors.append(f"Missing generated Markdown: {MARKDOWN.relative_to(ROOT)}")
        text = ""
    else:
        text = MARKDOWN.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Generated Markdown missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing changelog must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question public changelog validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question public changelog validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"change_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
