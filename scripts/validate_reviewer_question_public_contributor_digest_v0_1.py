#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_public_contributor_digest_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_PUBLIC_CONTRIBUTOR_DIGEST_V0_1.md"

REQUIRED_STEP_IDS = {"RQCD001", "RQCD002", "RQCD003", "RQCD004", "RQCD005"}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_PUBLIC_CONTRIBUTOR_DIGEST_V0_1.md",
    "docs/reviewer_question_public_contributor_digest_v0_1.json",
    "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_INDEX_V0_1.md",
    "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
    "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "Makefile",
]
REQUIRED_PHRASES = [
    "Reviewer question public contributor digest v0.1",
    "Digest step rows: 5",
    "Release index surface rows represented: 9",
    "Issue history rows represented: 10",
    "ready_for_public_preview",
    "Read the reviewer question release index",
    "Choose the matching reviewer question surface",
    "Match an intake example",
    "Check wording boundaries",
    "Run the release index check",
    "included_in_public_contributor_digest",
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
    "make reviewer_question_contributor_digest",
    "Add a reviewer question maintainer handoff note without scoring",
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
    if data.get("digest_step_count") != 5:
        errors.append("digest_step_count must be 5")
    if data.get("release_index_surface_rows_represented") != 9:
        errors.append("release_index_surface_rows_represented must be 9")
    if data.get("issue_history_rows_represented") != 10:
        errors.append("issue_history_rows_represented must be 10")
    if data.get("digest_decision") != "ready_for_public_preview":
        errors.append("digest_decision must be ready_for_public_preview")
    if len(rows) != 5:
        errors.append(f"Expected 5 digest rows, found {len(rows)}")

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

    step_ids = {str(row.get("step_id")) for row in rows}
    if step_ids != REQUIRED_STEP_IDS:
        errors.append("step id set must match required ids")
    if {str(row.get("digest_status")) for row in rows} != {"included_in_public_contributor_digest"}:
        errors.append("all digest statuses must be included_in_public_contributor_digest")

    for row in rows:
        step_id = str(row.get("step_id", ""))
        for key in ["step_name", "public_file", "contributor_action", "digest_status", "boundary"]:
            if key not in row:
                errors.append(f"{step_id}: missing {key}")

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
        errors.append("Generated outward facing contributor digest must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question public contributor digest validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question public contributor digest validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"digest_step_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
