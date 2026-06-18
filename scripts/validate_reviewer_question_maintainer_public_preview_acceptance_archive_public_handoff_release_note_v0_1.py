#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_public_handoff_release_note_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ACCEPTANCE_ARCHIVE_PUBLIC_HANDOFF_RELEASE_NOTE_V0_1.md"

REQUIRED_RELEASE_NOTE_IDS = {"RQPHRN001", "RQPHRN002", "RQPHRN003", "RQPHRN004", "RQPHRN005", "RQPHRN006"}
REQUIRED_RELEASE_INDEX_IDS = {"RQPHRI001", "RQPHRI002", "RQPHRI003", "RQPHRI004", "RQPHRI005", "RQPHRI006"}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ACCEPTANCE_ARCHIVE_PUBLIC_HANDOFF_RELEASE_NOTE_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_acceptance_archive_public_handoff_release_note_v0_1.json",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ACCEPTANCE_ARCHIVE_PUBLIC_HANDOFF_RELEASE_INDEX_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_acceptance_archive_public_handoff_release_index_v0_1.json",
    "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
    "Makefile",
]
REQUIRED_PHRASES = [
    "Reviewer question maintainer public preview acceptance archive public handoff release note v0.1",
    "Acceptance archive public handoff release note rows: 6",
    "Acceptance archive public handoff release index rows represented: 6",
    "Acceptance archive public handoff digest rows represented: 6",
    "Acceptance archive public handoff note rows represented: 6",
    "Acceptance archive stewardship digest rows represented: 6",
    "Acceptance archive stewardship closeout rows represented: 6",
    "Acceptance archive steward index rows represented: 6",
    "Acceptance archive steward note rows represented: 6",
    "Acceptance archive handoff packet rows represented: 6",
    "Acceptance archive final index rows represented: 6",
    "Issue template route note rows represented: 6",
    "Contributor route note rows represented: 6",
    "Release card rows represented: 6",
    "Navigation rows represented: 6",
    "Rollup rows represented: 6",
    "Archive rows represented: 5",
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
    "Issue history rows represented: 18",
    "Previous public issue represented: 84",
    "current public preview route only",
    "ready_for_public_preview_acceptance_archive_public_handoff_release_note",
    "Boundary public handoff release note row",
    "Reviewer question public handoff release note row",
    "Blocked wording public handoff release note row",
    "Public surface public handoff release note row",
    "Validation public handoff release note row",
    "Next action public handoff release note row",
    "Release note action:",
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
    "make reviewer_question_maintainer_public_preview_acceptance_archive_public_handoff_release_note",
    "Add a reviewer question maintainer public preview acceptance archive public handoff closure note without scoring",
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
    expected_counts = {
        "acceptance_archive_public_handoff_release_note_row_count": 6,
        "acceptance_archive_public_handoff_release_index_rows_represented": 6,
        "acceptance_archive_public_handoff_digest_rows_represented": 6,
        "acceptance_archive_public_handoff_note_rows_represented": 6,
        "acceptance_archive_stewardship_digest_rows_represented": 6,
        "acceptance_archive_stewardship_closeout_rows_represented": 6,
        "acceptance_archive_steward_index_rows_represented": 6,
        "acceptance_archive_steward_note_rows_represented": 6,
        "acceptance_archive_handoff_packet_rows_represented": 6,
        "acceptance_archive_final_index_rows_represented": 6,
        "issue_template_route_note_rows_represented": 6,
        "contributor_route_note_rows_represented": 6,
        "release_card_rows_represented": 6,
        "navigation_rows_represented": 6,
        "rollup_rows_represented": 6,
        "archive_rows_represented": 5,
        "closure_rows_represented": 5,
        "handoff_rows_represented": 5,
        "decision_rows_represented": 5,
        "candidate_summary_rows_represented": 5,
        "audit_trail_rows_represented": 5,
        "evidence_rows_represented": 5,
        "readiness_rows_represented": 5,
        "closeout_rows_represented": 5,
        "contributor_digest_rows_represented": 5,
        "release_index_surface_rows_represented": 9,
        "issue_history_rows_represented": 18,
        "previous_public_issue_number": 84,
    }
    for key, value in expected_counts.items():
        if data.get(key) != value:
            errors.append(f"{key} must be {value}")
    if data.get("public_preview_acceptance_archive_public_handoff_release_note") != "ready_for_public_preview_acceptance_archive_public_handoff_release_note":
        errors.append("public_preview_acceptance_archive_public_handoff_release_note must be ready_for_public_preview_acceptance_archive_public_handoff_release_note")
    if data.get("maintainer_review_scope") != "current public preview route only":
        errors.append("maintainer_review_scope must be current public preview route only")
    if len(rows) != 6:
        errors.append(f"Expected 6 acceptance archive public handoff release note rows, found {len(rows)}")

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

    release_note_ids = {str(row.get("public_handoff_release_note_id")) for row in rows}
    if release_note_ids != REQUIRED_RELEASE_NOTE_IDS:
        errors.append("public handoff release note id set must match required ids")
    release_index_ids = {str(row.get("source_public_handoff_release_index_id")) for row in rows}
    if release_index_ids != REQUIRED_RELEASE_INDEX_IDS:
        errors.append("source public handoff release index id set must match required ids")
    if {str(row.get("public_handoff_release_note_state")) for row in rows} != {"ready_for_public_preview_acceptance_archive_public_handoff_release_note"}:
        errors.append("all public handoff release note states must be ready_for_public_preview_acceptance_archive_public_handoff_release_note")

    for row in rows:
        release_note_id = str(row.get("public_handoff_release_note_id", ""))
        for key in [
            "release_note_name",
            "source_public_handoff_release_index_id",
            "release_note_text",
            "release_note_action",
            "public_handoff_release_note_state",
            "public_handoff_release_note_boundary",
            "public_handoff_release_note_decision",
            "blocked_claims",
        ]:
            if key not in row:
                errors.append(f"{release_note_id}: missing {key}")

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
        errors.append("Generated outward facing acceptance archive public handoff release note must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question maintainer public preview acceptance archive public handoff release note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question maintainer public preview acceptance archive public handoff release note validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"acceptance_archive_public_handoff_release_note_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
