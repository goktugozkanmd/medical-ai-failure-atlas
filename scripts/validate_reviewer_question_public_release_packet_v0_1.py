#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_public_release_packet_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_PUBLIC_RELEASE_PACKET_V0_1.md"

REQUIRED_SURFACE_IDS = {
    "RQRLP001",
    "RQRLP002",
    "RQRLP003",
    "RQRLP004",
    "RQRLP005",
    "RQRLP006",
    "RQRLP007",
}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_PACKET_V0_1.md",
    "docs/reviewer_question_public_release_packet_v0_1.json",
    "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/CONTRIBUTOR_ISSUE_TEMPLATE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
    "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
    "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/REVIEWER_QUESTION_RELEASE_GATE_CHECKLIST_V0_1.md",
    "docs/REVIEWER_QUESTION_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
]
REQUIRED_PHRASES = [
    "Reviewer question public release packet v0.1",
    "Packet surface rows: 7",
    "Outcome rows represented: 4",
    "Pass state rows represented: 4",
    "Block state rows represented: 0",
    "ready_for_public_preview",
    "Benchmark style reviewer questions",
    "Contributor issue template reviewer questions",
    "Reviewer question intake examples",
    "Reviewer question intake triage board",
    "Reviewer question public wording decision log",
    "Reviewer question release gate checklist",
    "Reviewer question release gate outcome dashboard",
    "included_in_public_preview",
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
    "make reviewer_question_release_packet",
    "Add a reviewer question maintainer release candidate summary without scoring",
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
    if data.get("packet_surface_count") != 7:
        errors.append("packet_surface_count must be 7")
    if data.get("outcome_row_count") != 4:
        errors.append("outcome_row_count must be 4")
    if data.get("pass_state_count") != 4:
        errors.append("pass_state_count must be 4")
    if data.get("block_state_count") != 0:
        errors.append("block_state_count must be 0")
    if data.get("packet_decision") != "ready_for_public_preview":
        errors.append("packet_decision must be ready_for_public_preview")
    if len(rows) != 7:
        errors.append(f"Expected 7 packet rows, found {len(rows)}")

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

    surface_ids = {str(row.get("surface_id")) for row in rows}
    statuses = {str(row.get("packet_status")) for row in rows}
    if surface_ids != REQUIRED_SURFACE_IDS:
        errors.append("surface id set must match required ids")
    if statuses != {"included_in_public_preview"}:
        errors.append("all packet statuses must be included_in_public_preview")

    for row in rows:
        surface_id = str(row.get("surface_id", ""))
        for key in ["surface_name", "public_file", "role", "packet_status", "next_action"]:
            if key not in row:
                errors.append(f"{surface_id}: missing {key}")

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
        errors.append("Generated outward facing release packet must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question public release packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question public release packet validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"packet_surface_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
