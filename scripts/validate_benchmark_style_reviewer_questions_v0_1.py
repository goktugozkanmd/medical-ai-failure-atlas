#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md"
DATA = ROOT / "docs" / "benchmark_style_reviewer_questions_v0_1.json"

REQUIRED_DOC_PHRASES = [
    "Benchmark style reviewer questions v0.1",
    "SourceCheckup Medical",
    "Medical AI Failure Atlas",
    "HealthBench rubric discipline",
    "MedHELM mapping boundary",
    "No scoring.",
    "No model ranking.",
    "No benchmark compatibility claim.",
    "No benchmark equivalence claim.",
    "No clinical validation.",
    "No clinical deployment.",
    "No patient data.",
    "No endpoint call.",
    "No official endorsement.",
    "No source truth certification.",
    "source support, escalation, medication safety, missing context, policy wording, and warning sign visibility",
    "expand SourceCheckup and Failure Atlas contributor issue templates",
]

REQUIRED_IDS = [
    "BSRQ001",
    "BSRQ002",
    "BSRQ003",
    "BSRQ004",
    "BSRQ005",
    "BSRQ006",
    "BSRQ007",
    "BSRQ008",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "not_for_clinical_use": True,
    "no_model_calls": True,
    "no_endpoint_calls": True,
    "no_scoring": True,
    "no_ranking": True,
    "no_compatibility_claim": True,
}

FORBIDDEN_PHRASES = [
    "score report",
    "model ranking report",
    "benchmark compatible",
    "benchmark equivalent",
    "clinical validation claim",
    "deployment ready",
    "source truth certified",
    "patient data used",
    "endpoint result",
    "officially endorsed",
]


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"Missing doc: {DOC.relative_to(ROOT)}")
        text = ""
    else:
        text = DOC.read_text(encoding="utf-8")
    if not DATA.exists():
        errors.append(f"Missing data: {DATA.relative_to(ROOT)}")
        payload = {}
    else:
        payload = json.loads(DATA.read_text(encoding="utf-8"))

    lower_text = text.lower()
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Doc missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Doc contains forbidden phrase: {phrase}")
    if "-" in text:
        errors.append("Doc contains hyphen character")

    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    rows = payload.get("question_rows", [])
    if len(rows) != 8:
        errors.append("Expected 8 question rows")
    row_ids = {row.get("question_id") for row in rows}
    for row_id in REQUIRED_IDS:
        if row_id not in row_ids:
            errors.append(f"Missing question id: {row_id}")
    surfaces = {row.get("local_surface") for row in rows}
    if surfaces != {"SourceCheckup Medical", "Medical AI Failure Atlas"}:
        errors.append(f"Unexpected surfaces: {sorted(surfaces)}")
    if sum(1 for row in rows if row.get("local_surface") == "SourceCheckup Medical") != 4:
        errors.append("Expected 4 SourceCheckup rows")
    if sum(1 for row in rows if row.get("local_surface") == "Medical AI Failure Atlas") != 4:
        errors.append("Expected 4 Failure Atlas rows")
    for row in rows:
        for key in [
            "benchmark_lens",
            "reviewer_question",
            "blocked_claim",
            "minimum_review",
            "track_a_value",
            "track_b_value",
        ]:
            if not row.get(key):
                errors.append(f"{row.get('question_id')}: missing {key}")
        unsafe_text = " ".join(str(row.get(key, "")) for key in row)
        for phrase in ["score", "ranking", "compatible", "validated"]:
            if phrase in unsafe_text.lower() and phrase not in str(row.get("blocked_claim", "")).lower():
                errors.append(f"{row.get('question_id')}: unsafe benchmark wording in row")

    if errors:
        print("FAIL benchmark style reviewer questions validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS benchmark style reviewer questions validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"question_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
