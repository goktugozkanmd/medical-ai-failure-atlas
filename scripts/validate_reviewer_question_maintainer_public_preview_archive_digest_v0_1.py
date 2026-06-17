#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_archive_digest_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ARCHIVE_DIGEST_V0_1.md"

REQUIRED_ARCHIVE_IDS = {"RQPA001", "RQPA002", "RQPA003", "RQPA004", "RQPA005"}
REQUIRED_CLOSURE_IDS = {"RQPC001", "RQPC002", "RQPC003", "RQPC004", "RQPC005"}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ARCHIVE_DIGEST_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_archive_digest_v0_1.json",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_CLOSURE_CHECKLIST_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_closure_checklist_v0_1.json",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_HANDOFF_SUMMARY_V0_1.md",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_DECISION_LOG_V0_1.md",
    "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
    "Makefile",
]
REQUIRED_PHRASES = [
    "Reviewer question maintainer public preview archive digest v0.1",
    "Archive rows: 5",
    "Closure rows represented: 5",
    "Handoff rows represented: 5",
    "Decision rows represented: 5",
    "Candidate summary rows represented: 5",
    "Audit trail rows represented: 5",
    "Evidence rows represented: 5",
    "Readiness rows represented: 5",
    "Closeout rows represented: 5",
    "Contributor digest rows represented: 5",
    "Release index surface rows represented: 9",
    "Issue history rows represented: 11",
    "Previous public issue represented: 64",
    "current public preview route only",
    "archived_for_public_preview_trace",
    "Synthetic boundary archive",
    "Reviewer question lane archive",
    "Public wording archive",
    "Release surface archive",
    "Validation archive",
    "benchmark scoring",
    "benchmark compatibility",
    "benchmark equivalence",
    "endpoint result",
    "patient data",
    "clinical validation",
    "clinical deployment",
    "model ranking",
    "official endorsement",
    "route access",
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
    "not route access",
    "not an official endorsement",
    "make reviewer_question_maintainer_public_preview_archive_digest",
    "Add a reviewer question maintainer public preview index rollup without scoring",
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
    if data.get("archive_row_count") != 5:
        errors.append("archive_row_count must be 5")
    if data.get("closure_rows_represented") != 5:
        errors.append("closure_rows_represented must be 5")
    if data.get("handoff_rows_represented") != 5:
        errors.append("handoff_rows_represented must be 5")
    if data.get("decision_rows_represented") != 5:
        errors.append("decision_rows_represented must be 5")
    if data.get("candidate_summary_rows_represented") != 5:
        errors.append("candidate_summary_rows_represented must be 5")
    if data.get("audit_trail_rows_represented") != 5:
        errors.append("audit_trail_rows_represented must be 5")
    if data.get("evidence_rows_represented") != 5:
        errors.append("evidence_rows_represented must be 5")
    if data.get("readiness_rows_represented") != 5:
        errors.append("readiness_rows_represented must be 5")
    if data.get("closeout_rows_represented") != 5:
        errors.append("closeout_rows_represented must be 5")
    if data.get("contributor_digest_rows_represented") != 5:
        errors.append("contributor_digest_rows_represented must be 5")
    if data.get("release_index_surface_rows_represented") != 9:
        errors.append("release_index_surface_rows_represented must be 9")
    if data.get("issue_history_rows_represented") != 11:
        errors.append("issue_history_rows_represented must be 11")
    if data.get("previous_public_issue_number") != 64:
        errors.append("previous_public_issue_number must be 64")
    if data.get("public_preview_archive") != "archived_for_public_preview_trace":
        errors.append("public_preview_archive must be archived_for_public_preview_trace")
    if data.get("maintainer_review_scope") != "current public preview route only":
        errors.append("maintainer_review_scope must be current public preview route only")
    if len(rows) != 5:
        errors.append(f"Expected 5 archive rows, found {len(rows)}")

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
        "no_route_access_claim",
    ]:
        expected = False if field == "contains_patient_data" else True
        if data.get(field) is not expected:
            errors.append(f"{field} must be {expected}")

    archive_ids = {str(row.get("archive_id")) for row in rows}
    if archive_ids != REQUIRED_ARCHIVE_IDS:
        errors.append("archive id set must match required ids")
    closure_ids = {str(row.get("source_closure_id")) for row in rows}
    if closure_ids != REQUIRED_CLOSURE_IDS:
        errors.append("source closure id set must match required ids")
    if {str(row.get("archive_state")) for row in rows} != {"archived_for_public_preview_trace"}:
        errors.append("all archive states must be archived_for_public_preview_trace")

    for row in rows:
        archive_id = str(row.get("archive_id", ""))
        for key in ["archive_name", "source_closure_id", "archive_note", "archive_state", "archive_boundary", "archive_decision", "blocked_claims"]:
            if key not in row:
                errors.append(f"{archive_id}: missing {key}")

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
        errors.append("Generated outward facing maintainer public preview archive digest must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question maintainer public preview archive digest validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question maintainer public preview archive digest validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"archive_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
