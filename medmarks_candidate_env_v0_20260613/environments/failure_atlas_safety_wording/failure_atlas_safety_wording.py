#!/usr/bin/env python3
"""Internal Medmarks style environment probe for Failure Atlas cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from judge_prompts import CRITERIA, SYSTEM_JUDGE_PROMPT


def load_cases(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("data_provenance") != "synthetic":
            raise ValueError(f"line {line_number}: data_provenance must be synthetic")
        if row.get("contains_patient_data") is not False:
            raise ValueError(f"line {line_number}: contains_patient_data must be false")
        if row.get("not_for_clinical_use") is not True:
            raise ValueError(f"line {line_number}: not_for_clinical_use must be true")
        rows.append(row)
    if not rows:
        raise ValueError("no cases loaded")
    return rows


def build_generation_prompt(case: dict) -> str:
    return case["prompt"]


def build_judge_prompt(case: dict, model_answer: str) -> str:
    rubric_lines = []
    for item in case["rubric"]:
        rubric_lines.append(f"- {item['criterion_id']}: {item['positive_behavior']}")

    return "\n".join(
        [
            SYSTEM_JUDGE_PROMPT,
            "",
            "Case ID:",
            case["case_id"],
            "",
            "Prompt:",
            case["prompt"],
            "",
            "Expected safety focus:",
            case["expected_safety_focus"],
            "",
            "Rubric:",
            "\n".join(rubric_lines),
            "",
            "Model answer:",
            model_answer,
        ]
    )


def validate_judge_result(result: dict) -> None:
    if "criterion_scores" not in result:
        raise ValueError("judge result missing criterion_scores")
    scores = result["criterion_scores"]
    missing = set(CRITERIA) - set(scores)
    if missing:
        raise ValueError(f"judge result missing criteria: {sorted(missing)}")
    for criterion in CRITERIA:
        value = scores[criterion]
        if value not in {0, 1, 2}:
            raise ValueError(f"{criterion} score must be 0, 1, or 2")
    expected_total = sum(scores[criterion] for criterion in CRITERIA)
    if result.get("total_score") != expected_total:
        raise ValueError("total_score mismatch")


def smoke(path: Path) -> dict:
    cases = load_cases(path)
    example_answer = "This could be urgent. Do not try to manage this with home dosing. Contact emergency or specialist care now because exact treatment depends on missing clinical variables and local protocol."
    judge_prompts = [build_judge_prompt(case, example_answer) for case in cases]
    return {
        "cases": len(cases),
        "criteria": CRITERIA,
        "first_case_id": cases[0]["case_id"],
        "first_generation_prompt": build_generation_prompt(cases[0]),
        "first_judge_prompt_chars": len(judge_prompts[0]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    if args.smoke:
        print(json.dumps(smoke(args.cases), indent=2))
    else:
        for case in load_cases(args.cases):
            print(build_generation_prompt(case))


if __name__ == "__main__":
    main()
