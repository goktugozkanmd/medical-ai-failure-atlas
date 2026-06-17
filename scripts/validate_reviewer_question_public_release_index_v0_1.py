#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_public_release_index_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_PUBLIC_RELEASE_INDEX_V0_1.md"

REQUIRED_SURFACE_IDS = {
    "RQRPI001",
    "RQRPI002",
    "RQRPI003",
    "RQRPI004",
    "RQRPI005",
    "RQRPI006",
    "RQRPI007",
    "RQRPI008",
    "RQRPI009",
}
REQUIRED_ISSUES = set(range(45, 56))
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_INDEX_V0_1.md",
    "docs/reviewer_question_public_release_index_v0_1.json",
    "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/CONTRIBUTOR_ISSUE_TEMPLATE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
    "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
    "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/REVIEWER_QUESTION_RELEASE_GATE_CHECKLIST_V0_1.md",
    "docs/REVIEWER_QUESTION_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
    "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_PACKET_V0_1.md",
    "docs/REVIEWER_QUESTION_PUBLIC_CHANGELOG_V0_1.md",
]
REQUIRED_PHRASES = [
    "Reviewer question public release index v0.1",
    "Index surface rows: 9",
    "Issue history rows: 11",
    "Release packet rows represented: 7",
    "Changelog rows represented: 8",
    "ready_for_public_preview",
    "Benchmark style reviewer questions",
    "Contributor issue template reviewer questions",
    "Reviewer question intake examples",
    "Reviewer question intake triage board",
    "Reviewer question public wording decision log",
    "Reviewer question release gate checklist",
    "Reviewer question release gate outcome dashboard",
    "Reviewer question public release packet",
    "Reviewer question public changelog",
    "included_in_public_release_index",
    "Roadmap: benchmark style reviewer questions",
    "Roadmap: reviewer question issue template fields",
    "Roadmap: reviewer question intake examples",
    "Roadmap: reviewer question intake triage board",
    "Roadmap: reviewer question wording decision log",
    "Roadmap: reviewer question release gate checklist",
    "Roadmap: reviewer question gate outcome dashboard",
    "Roadmap: reviewer question public release packet",
    "Roadmap: reviewer question public changelog",
    "Roadmap: reviewer question public release index",
    "Roadmap: reviewer question public contributor digest",
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
    "make reviewer_question_release_index",
    "Add a reviewer question maintainer release readiness digest without scoring",
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
        data: dict[str, Any] = {"surfaces": [], "issue_history": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    surfaces = data.get("surfaces", [])
    issues = data.get("issue_history", [])
    if not isinstance(surfaces, list):
        errors.append("surfaces must be a list")
        surfaces = []
    if not isinstance(issues, list):
        errors.append("issue_history must be a list")
        issues = []
    if data.get("index_surface_count") != 9:
        errors.append("index_surface_count must be 9")
    if data.get("issue_history_count") != 11:
        errors.append("issue_history_count must be 11")
    if data.get("release_packet_rows_represented") != 7:
        errors.append("release_packet_rows_represented must be 7")
    if data.get("changelog_rows_represented") != 8:
        errors.append("changelog_rows_represented must be 8")
    if data.get("index_decision") != "ready_for_public_preview":
        errors.append("index_decision must be ready_for_public_preview")
    if len(surfaces) != 9:
        errors.append(f"Expected 9 index surfaces, found {len(surfaces)}")
    if len(issues) != 11:
        errors.append(f"Expected 11 issue history rows, found {len(issues)}")

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

    surface_ids = {str(row.get("surface_id")) for row in surfaces}
    issue_numbers = {int(row.get("issue_number", -1)) for row in issues}
    if surface_ids != REQUIRED_SURFACE_IDS:
        errors.append("surface id set must match required ids")
    if issue_numbers != REQUIRED_ISSUES:
        errors.append("issue numbers must be 45 through 55")
    if {str(row.get("index_status")) for row in surfaces} != {"included_in_public_release_index"}:
        errors.append("all index statuses must be included_in_public_release_index")
    if {str(row.get("issue_state")) for row in issues} != {"closed"}:
        errors.append("all issue history states must be closed")

    for row in surfaces:
        surface_id = str(row.get("surface_id", ""))
        for key in ["surface_name", "public_file", "role", "index_status", "next_action"]:
            if key not in row:
                errors.append(f"{surface_id}: missing {key}")
    for row in issues:
        issue_number = str(row.get("issue_number", ""))
        for key in ["issue_title", "issue_state", "public_label", "public_value"]:
            if key not in row:
                errors.append(f"issue {issue_number}: missing {key}")

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
        errors.append("Generated outward facing release index must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question public release index validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question public release index validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"index_surface_rows={len(surfaces)}")
    print(f"issue_history_rows={len(issues)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
