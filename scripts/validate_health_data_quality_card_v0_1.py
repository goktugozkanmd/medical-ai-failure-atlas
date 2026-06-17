#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / "docs" / "HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md"

SCENARIO_FILES = [
    ROOT / "data" / "scenario_bank_v1.tsv",
    ROOT / "data" / "scenario_bank_v2_hard_addendum.tsv",
    ROOT / "data" / "scenario_bank_v3_scale_seed.tsv",
]

PROMPT_FILES = [
    ROOT / "data" / "prompt_set_v1.tsv",
    ROOT / "data" / "prompt_set_v2_hard_30.tsv",
    ROOT / "data" / "prompt_set_v3_scale_30.tsv",
]

INTER_RATER_FILE = ROOT / "data" / "inter_rater_review_subset_v0_1.tsv"

REQUIRED_PHRASES = [
    "synthetic dataset release readiness checklist",
    "not proof of dataset quality",
    "not clinical advice",
    "not patient data",
    "not raw model output release",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "150 synthetic scenario rows",
    "70 prompt rows",
    "24 pilot inter rater rows",
    "12 source claim review queue rows",
    "single physician authored synthetic draft pending additional clinician review",
    "v0.1.0",
    "public_preview_allowed_synthetic_only",
    "sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl",
    "Label audit reviewer role table",
    "docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md",
    "make label_audit_role_table",
    "Label audit public contributor route",
    ".github/ISSUE_TEMPLATE/label_audit_review.yml",
    "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
    "make label_audit_public_issue",
    "Label audit example intake rows",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    "docs/label_audit/label_audit_example_intake_v0_1.json",
    "make label_audit_examples",
    "5 synthetic label audit examples",
    "Label audit example dashboard",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md",
    "docs/label_audit/label_audit_example_dashboard_v0_1.json",
    "make label_audit_dashboard",
    "Blocked public claim types represented: 5",
    "Label audit maintainer triage board",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md",
    "docs/label_audit/label_audit_maintainer_triage_board_v0_1.json",
    "make label_audit_triage",
    "Maintainer triage rows: 5",
    "Label audit public wording decision log",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/label_audit/label_audit_public_wording_decision_log_v0_1.json",
    "make label_audit_wording_log",
    "Public wording decision rows: 5",
    "Label audit release gate checklist",
    "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md",
    "docs/label_audit/label_audit_release_gate_checklist_v0_1.json",
    "make label_audit_release_gates",
    "Release gate rows: 5",
    "Synthetic provenance reviewer",
    "Label definition reviewer",
    "Pilot subset reviewer",
    "Public release boundary reviewer",
    "raw model outputs are not public",
    "No agreement statistic is reported here",
]

REQUIRED_FILES = [
    "data/scenario_bank_v1.tsv",
    "data/scenario_bank_v2_hard_addendum.tsv",
    "data/scenario_bank_v3_scale_seed.tsv",
    "data/prompt_set_v1.tsv",
    "data/prompt_set_v2_hard_30.tsv",
    "data/prompt_set_v3_scale_30.tsv",
    "data/inter_rater_review_subset_v0_1.tsv",
    "data/scoring_rubric_v0_1.json",
    "docs/LABEL_DEFINITION_LOCK_V0_1.md",
    "LABELING.md",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated benchmark",
    "safe for clinical use",
    "deployment ready",
    "model superiority",
    "official approval",
    "regulatory compliance",
    "sandbox access granted",
    "institutional endorsement",
    "real patient data used",
    "proves data quality",
]


def count_tsv_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    errors: list[str] = []
    if not CARD.exists():
        errors.append(f"Missing card: {CARD}")
        text = ""
    else:
        text = CARD.read_text(encoding="utf-8")

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")
    for relative_path in REQUIRED_FILES:
        if relative_path not in text:
            errors.append(f"Missing required file reference: {relative_path}")
        if not (ROOT / relative_path).exists():
            errors.append(f"Referenced file does not exist: {relative_path}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")

    scenario_rows = sum(count_tsv_rows(path) for path in SCENARIO_FILES)
    prompt_rows = sum(count_tsv_rows(path) for path in PROMPT_FILES)
    inter_rater_rows = count_tsv_rows(INTER_RATER_FILE)

    if scenario_rows != 150:
        errors.append(f"Expected 150 scenario rows, found {scenario_rows}")
    if prompt_rows != 70:
        errors.append(f"Expected 70 prompt rows, found {prompt_rows}")
    if inter_rater_rows != 24:
        errors.append(f"Expected 24 pilot inter rater rows, found {inter_rater_rows}")

    if errors:
        print("FAIL health data quality card validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS health data quality card validation")
    print(f"scenario_rows={scenario_rows}")
    print(f"prompt_rows={prompt_rows}")
    print(f"pilot_inter_rater_rows={inter_rater_rows}")
    print(f"file={CARD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
