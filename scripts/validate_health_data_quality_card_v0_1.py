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
    "single physician authored synthetic draft pending additional clinician review",
    "v0.1.0",
    "public_preview_allowed_synthetic_only",
    "sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl",
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
