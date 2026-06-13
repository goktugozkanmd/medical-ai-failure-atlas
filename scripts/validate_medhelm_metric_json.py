#!/usr/bin/env python3
import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = {
    "metric_id",
    "status",
    "not_for_clinical_use",
    "contains_patient_data",
    "data_provenance",
    "intended_route",
    "purpose",
    "source_case_ids",
    "source_scenario_ids",
    "score_scale",
    "criteria",
    "judge_prompt_draft",
    "failure_tags",
    "release_boundary",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_medhelm_metric_json.py path/to/metric.json")

    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_TOP_LEVEL - set(data)
    if missing:
        fail(f"missing keys: {sorted(missing)}")

    if data["status"] != "internal_draft":
        fail("status must be internal_draft")
    if data["not_for_clinical_use"] is not True:
        fail("not_for_clinical_use must be true")
    if data["contains_patient_data"] is not False:
        fail("contains_patient_data must be false")
    if data["data_provenance"] != "synthetic":
        fail("data_provenance must be synthetic")
    if set(data["score_scale"].keys()) != {"0", "1", "2"}:
        fail("score_scale must define 0, 1, and 2")
    if not isinstance(data["criteria"], list) or len(data["criteria"]) < 5:
        fail("criteria must contain at least five items")
    for criterion in data["criteria"]:
        if "criterion_id" not in criterion or "score_focus" not in criterion:
            fail("each criterion needs criterion_id and score_focus")

    print("PASS")
    print(f"Metric: {data['metric_id']}")
    print(f"Criteria: {len(data['criteria'])}")


if __name__ == "__main__":
    main()
