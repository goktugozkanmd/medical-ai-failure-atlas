#!/usr/bin/env python3
import json
import sys
from pathlib import Path


REQUIRED_KEYS = {
    "case_id",
    "source_scenario_id",
    "task_family",
    "medhelm_category_guess",
    "medmarks_subset_guess",
    "clinical_domain",
    "data_provenance",
    "contains_patient_data",
    "not_for_clinical_use",
    "external_status",
    "prompt",
    "expected_safety_focus",
    "failure_mechanism_tags",
    "clinician_review_question",
    "rubric",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_external_sample_jsonl.py path/to/file.jsonl")

    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"file not found: {path}")

    seen_case_ids = set()
    rows = 0

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue

        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"line {line_number} is not valid JSON: {exc}")

        missing = REQUIRED_KEYS - set(row)
        if missing:
            fail(f"line {line_number} missing keys: {sorted(missing)}")

        case_id = row["case_id"]
        if case_id in seen_case_ids:
            fail(f"duplicate case_id: {case_id}")
        seen_case_ids.add(case_id)

        if row["data_provenance"] != "synthetic":
            fail(f"{case_id}: data_provenance must be synthetic")
        if row["contains_patient_data"] is not False:
            fail(f"{case_id}: contains_patient_data must be false")
        if row["not_for_clinical_use"] is not True:
            fail(f"{case_id}: not_for_clinical_use must be true")
        if row["external_status"] != "internal_draft":
            fail(f"{case_id}: external_status must be internal_draft")
        if not isinstance(row["failure_mechanism_tags"], list) or not row["failure_mechanism_tags"]:
            fail(f"{case_id}: failure_mechanism_tags must be a non empty list")
        if not isinstance(row["rubric"], list) or len(row["rubric"]) < 3:
            fail(f"{case_id}: rubric must contain at least three criteria")

        for criterion in row["rubric"]:
            if not isinstance(criterion, dict):
                fail(f"{case_id}: rubric criteria must be objects")
            if "criterion_id" not in criterion or "positive_behavior" not in criterion:
                fail(f"{case_id}: rubric criterion missing criterion_id or positive_behavior")

        rows += 1

    if rows == 0:
        fail("no rows found")

    print("PASS")
    print(f"Rows: {rows}")


if __name__ == "__main__":
    main()
