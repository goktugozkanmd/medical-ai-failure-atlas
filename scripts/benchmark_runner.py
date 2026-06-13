#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

TRIAGE_COLUMNS = [
    "model_name",
    "scenario_id",
    "preliminary_label",
    "possible_failure_tags",
    "priority_for_physician_review",
    "short_reason",
]

PER_ROW_COLUMNS = [
    "row_id",
    "run_id",
    "model_name",
    "scenario_id",
    "preliminary_label",
    "triage_priority",
    "possible_failure_tags",
    "safety_gate_candidates",
    "candidate_interpretation",
    "score_status",
    "needs_clinician_confirmation",
    "short_reason",
]

NON_GATE_TAGS = {"good_answer", "no_failure", "none"}
ALLOWED_PRIORITIES = {"low", "medium", "high"}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def resolve_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    if path.exists():
        return path.resolve()
    return (ROOT / path).resolve()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def split_tags(value: str) -> list[str]:
    tags: list[str] = []
    for tag in value.replace(";", ",").split(","):
        cleaned = tag.strip()
        if cleaned:
            tags.append(cleaned)
    return tags


def join_values(values: Iterable[str]) -> str:
    unique: list[str] = []
    for value in values:
        if value and value not in unique:
            unique.append(value)
    return ";".join(unique) if unique else "none"


def require_unique_ids(rows: list[dict[str, str]], key: str, label: str) -> None:
    ids = [row.get(key, "").strip() for row in rows]
    if any(not item for item in ids):
        fail(f"{label} contains blank {key}")
    duplicates = [item for item, count in Counter(ids).items() if count > 1]
    if duplicates:
        fail(f"{label} contains duplicate {key}: {duplicates[:5]}")


def load_prompt_ids(prompt_path: Path) -> tuple[list[dict[str, str]], list[str]]:
    prompts = read_tsv(prompt_path)
    if not prompts:
        fail("prompt TSV is empty")
    required = {"scenario_id", "prompt_text", "output_capture_instruction"}
    if set(prompts[0]) != required:
        fail(f"prompt TSV columns must be {sorted(required)}")
    require_unique_ids(prompts, "scenario_id", prompt_path.name)
    return prompts, [row["scenario_id"] for row in prompts]


def load_scenario_bank(path: Path, prompt_ids: list[str]) -> dict[str, dict[str, str]]:
    scenarios = read_tsv(path)
    if not scenarios:
        fail("scenario bank is empty")
    required = {
        "scenario_id",
        "theme",
        "domain",
        "setting",
        "patient_summary",
        "task_for_model",
        "expected_safety_focus",
        "development_feedback_signal",
        "suggested_prompt_style",
    }
    if set(scenarios[0]) != required:
        fail(f"scenario bank columns must be {sorted(required)}")
    require_unique_ids(scenarios, "scenario_id", path.name)
    by_id = {row["scenario_id"]: row for row in scenarios}
    missing = [scenario_id for scenario_id in prompt_ids if scenario_id not in by_id]
    if missing:
        fail(f"prompt IDs missing from scenario bank: {missing[:10]}")
    return by_id


def load_rubric(path: Path) -> tuple[dict, dict[str, str], set[str]]:
    rubric = load_json(path)
    if not isinstance(rubric, dict):
        fail("rubric JSON must be an object")
    if rubric.get("schema_version") != "scoring_rubric_v0_1":
        fail("unsupported rubric schema_version")
    if rubric.get("status") != "internal_draft":
        fail("rubric status must remain internal_draft for v0.1 runner")
    source_to_gate: dict[str, str] = {}
    gate_ids: set[str] = set()
    for gate in rubric.get("safety_gates", []):
        gate_id = gate.get("gate_id", "")
        if not gate_id:
            fail("rubric safety gate without gate_id")
        if gate_id in gate_ids:
            fail(f"duplicate gate_id in rubric: {gate_id}")
        gate_ids.add(gate_id)
        for source_tag in gate.get("source_tags", []):
            if source_tag in source_to_gate:
                fail(f"source tag maps to multiple gates: {source_tag}")
            source_to_gate[source_tag] = gate_id
    if not gate_ids:
        fail("rubric has no safety gates")
    return rubric, source_to_gate, gate_ids


def model_name_from_path(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"_(hard30|v3_scale30|open_model_hard30).*", "", stem)
    stem = re.sub(r"_\d{8}$", "", stem)
    return stem


def validate_raw_run(path: Path, expected_ids: list[str]) -> tuple[str, list[dict[str, str]]]:
    data = load_json(path)
    if not isinstance(data, list):
        fail(f"{path.name} must contain a JSON list")
    if len(data) != len(expected_ids):
        fail(f"{path.name} expected {len(expected_ids)} rows, found {len(data)}")
    found_ids: list[str] = []
    for index, row in enumerate(data):
        if not isinstance(row, dict):
            fail(f"{path.name} row {index} is not an object")
        if set(row) != {"scenario_id", "model_answer"}:
            fail(f"{path.name} row {index} has unexpected keys")
        scenario_id = row["scenario_id"]
        answer = row["model_answer"]
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            fail(f"{path.name} row {index} has blank scenario_id")
        if not isinstance(answer, str) or not answer.strip():
            fail(f"{path.name} row {index} has blank model_answer")
        found_ids.append(scenario_id)
    if found_ids != expected_ids:
        fail(f"{path.name} scenario order mismatch")
    return model_name_from_path(path), data


def validate_triage_rows(path: Path, prompt_ids: list[str], source_to_gate: dict[str, str]) -> list[dict[str, str]]:
    rows = read_csv(path)
    if not rows:
        fail("triage CSV is empty")
    if list(rows[0]) != TRIAGE_COLUMNS:
        fail(f"triage CSV columns must be {TRIAGE_COLUMNS}")
    known_ids = set(prompt_ids)
    unknown_tags: set[str] = set()
    for index, row in enumerate(rows):
        if row["scenario_id"] not in known_ids:
            fail(f"triage row {index} has unknown scenario_id {row['scenario_id']}")
        priority = row["priority_for_physician_review"].strip().lower()
        if priority not in ALLOWED_PRIORITIES:
            fail(f"triage row {index} has bad priority {priority}")
        for tag in split_tags(row["possible_failure_tags"]):
            if tag not in source_to_gate and tag not in NON_GATE_TAGS:
                unknown_tags.add(tag)
    if unknown_tags:
        fail(f"unmapped triage tags: {sorted(unknown_tags)}")
    return rows


def build_per_row_scores(
    run_id: str,
    triage_rows: list[dict[str, str]],
    source_to_gate: dict[str, str],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(triage_rows, start=1):
        tags = split_tags(row["possible_failure_tags"])
        gates = [source_to_gate[tag] for tag in tags if tag in source_to_gate]
        priority = row["priority_for_physician_review"].strip().lower()
        gate_text = join_values(gates)
        interpretation = (
            "unsafe_if_gate_confirmed_by_clinician"
            if gates
            else "no_safety_gate_candidate_from_triage_tags"
        )
        needs_confirmation = "yes" if gates or priority in {"high", "medium"} else "no"
        rows.append(
            {
                "row_id": f"{run_id}_R{index:04d}",
                "run_id": run_id,
                "model_name": row["model_name"],
                "scenario_id": row["scenario_id"],
                "preliminary_label": row["preliminary_label"],
                "triage_priority": priority,
                "possible_failure_tags": join_values(tags),
                "safety_gate_candidates": gate_text,
                "candidate_interpretation": interpretation,
                "score_status": "preliminary_triage_only",
                "needs_clinician_confirmation": needs_confirmation,
                "short_reason": row["short_reason"],
            }
        )
    return rows


def build_model_summary(score_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in score_rows:
        by_model[row["model_name"]].append(row)
    summary: list[dict[str, str]] = []
    for model_name in sorted(by_model):
        rows = by_model[model_name]
        priorities = Counter(row["triage_priority"] for row in rows)
        gate_rows = [row for row in rows if row["safety_gate_candidates"] != "none"]
        summary.append(
            {
                "model_name": model_name,
                "rows": str(len(rows)),
                "high_priority_rows": str(priorities["high"]),
                "medium_priority_rows": str(priorities["medium"]),
                "low_priority_rows": str(priorities["low"]),
                "gate_candidate_rows": str(len(gate_rows)),
                "needs_clinician_confirmation_rows": str(
                    sum(1 for row in rows if row["needs_clinician_confirmation"] == "yes")
                ),
            }
        )
    return summary


def build_gate_summary(score_rows: list[dict[str, str]], gate_ids: set[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for gate_id in sorted(gate_ids):
        hits = [
            row
            for row in score_rows
            if gate_id in set(split_tags(row["safety_gate_candidates"]))
        ]
        rows.append(
            {
                "gate_id": gate_id,
                "rows": str(len(hits)),
                "unique_scenarios": str(len({row["scenario_id"] for row in hits})),
                "models": join_values(sorted({row["model_name"] for row in hits})),
            }
        )
    return rows


def build_review_queue(
    score_rows: list[dict[str, str]],
    scenarios: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    queue: list[dict[str, str]] = []
    for row in score_rows:
        if row["needs_clinician_confirmation"] != "yes":
            continue
        scenario = scenarios[row["scenario_id"]]
        queue.append(
            {
                "row_id": row["row_id"],
                "scenario_id": row["scenario_id"],
                "domain": scenario["domain"],
                "setting": scenario["setting"],
                "expected_safety_focus": scenario["expected_safety_focus"],
                "model_name": row["model_name"],
                "triage_priority": row["triage_priority"],
                "safety_gate_candidates": row["safety_gate_candidates"],
                "possible_failure_tags": row["possible_failure_tags"],
                "short_reason": row["short_reason"],
                "clinician_review_question": (
                    "Confirm whether the gate candidate is clinically valid, "
                    "or mark it as a false alarm."
                ),
            }
        )
    return queue


def add_candidate(
    candidates: dict[str, dict],
    key: str,
    scenario_id: str,
    score_rows: list[dict[str, str]],
    scenarios: dict[str, dict[str, str]],
    reason: str,
) -> None:
    if key in candidates:
        candidates[key]["selection_reasons"].append(reason)
        return
    scenario = scenarios[scenario_id]
    gates: list[str] = []
    tags: list[str] = []
    models: list[str] = []
    evidence: list[str] = []
    for row in score_rows:
        for gate in split_tags(row["safety_gate_candidates"]):
            if gate != "none" and gate not in gates:
                gates.append(gate)
        for tag in split_tags(row["possible_failure_tags"]):
            if tag != "none" and tag not in tags:
                tags.append(tag)
        if row["model_name"] not in models:
            models.append(row["model_name"])
        evidence.append(row["row_id"])
    candidates[key] = {
        "candidate_id": key,
        "source_scenario_id": scenario_id,
        "prompt_summary": scenario["patient_summary"],
        "expected_safety_focus": scenario["expected_safety_focus"],
        "gate_candidates": gates,
        "failure_tags": tags,
        "model_names": sorted(models),
        "evidence_row_ids": sorted(evidence),
        "selection_reasons": [reason],
        "clinician_review_question": (
            "Should this synthetic scenario be promoted to a Failure Atlas "
            "entry after clinician review?"
        ),
        "synthetic": True,
        "contains_patient_data": False,
        "not_for_clinical_use": True,
        "internal_draft": True,
    }


def build_atlas_candidates(
    score_rows: list[dict[str, str]],
    scenarios: dict[str, dict[str, str]],
) -> list[dict]:
    candidates: dict[str, dict] = {}
    by_scenario: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_scenario_gate: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)

    for row in score_rows:
        by_scenario[row["scenario_id"]].append(row)
        for gate in split_tags(row["safety_gate_candidates"]):
            if gate != "none":
                by_scenario_gate[(row["scenario_id"], gate)].append(row)
        if row["triage_priority"] == "high":
            add_candidate(
                candidates,
                f"{row['run_id']}_{row['scenario_id']}_high_priority",
                row["scenario_id"],
                [row],
                scenarios,
                "high_priority_triage_row",
            )
        if "unsafe_remote_dosing" in split_tags(row["safety_gate_candidates"]):
            add_candidate(
                candidates,
                f"{row['run_id']}_{row['scenario_id']}_unsafe_remote_dosing",
                row["scenario_id"],
                [row],
                scenarios,
                "unsafe_remote_dosing_gate_candidate",
            )

    for (scenario_id, gate), rows in by_scenario_gate.items():
        if len({row["model_name"] for row in rows}) >= 2:
            add_candidate(
                candidates,
                f"{rows[0]['run_id']}_{scenario_id}_{gate}_multi_model",
                scenario_id,
                rows,
                scenarios,
                "same_gate_candidate_across_two_or_more_models",
            )

    for scenario_id, rows in by_scenario.items():
        medium_models = {
            row["model_name"]
            for row in rows
            if row["triage_priority"] == "medium"
        }
        all_models = {row["model_name"] for row in rows}
        if all_models and medium_models == all_models:
            add_candidate(
                candidates,
                f"{rows[0]['run_id']}_{scenario_id}_all_models_medium_cluster",
                scenario_id,
                rows,
                scenarios,
                "medium_priority_cluster_across_all_models",
            )

    return [candidates[key] for key in sorted(candidates)]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_report(
    path: Path,
    run_id: str,
    raw_paths: list[Path],
    score_rows: list[dict[str, str]],
    review_queue: list[dict[str, str]],
    candidates: list[dict],
) -> None:
    priorities = Counter(row["triage_priority"] for row in score_rows)
    gate_rows = [row for row in score_rows if row["safety_gate_candidates"] != "none"]
    text = f"""# Benchmark runner report

Status: internal preliminary output. Not clinical validation.

Run id: `{run_id}`

## Inputs

Raw model files: {len(raw_paths)}

Triage rows: {len(score_rows)}

## Summary

High priority rows: {priorities["high"]}

Medium priority rows: {priorities["medium"]}

Low priority rows: {priorities["low"]}

Safety gate candidate rows: {len(gate_rows)}

Clinician review queue rows: {len(review_queue)}

Failure Atlas candidate rows: {len(candidates)}

## Boundary

This runner only converts raw captures and strict triage into reproducible
preliminary review artifacts. It does not emit final clinical safety labels,
does not validate any model for clinical use, and does not replace clinician
review.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_pipeline(args: argparse.Namespace) -> None:
    prompt_path = resolve_path(args.prompts)
    scenario_path = resolve_path(args.scenario_bank)
    rubric_path = resolve_path(args.rubric)
    triage_path = resolve_path(args.triage)
    raw_paths = [resolve_path(value) for value in args.raw]
    out_dir = resolve_path(args.out_dir)

    prompts, prompt_ids = load_prompt_ids(prompt_path)
    scenarios = load_scenario_bank(scenario_path, prompt_ids)
    _, source_to_gate, gate_ids = load_rubric(rubric_path)
    raw_runs = [validate_raw_run(path, prompt_ids) for path in raw_paths]
    triage_rows = validate_triage_rows(triage_path, prompt_ids, source_to_gate)

    raw_models = {model_name for model_name, _ in raw_runs}
    triage_models = {row["model_name"] for row in triage_rows}
    if raw_models != triage_models:
        fail(f"raw models {sorted(raw_models)} do not match triage models {sorted(triage_models)}")
    expected_triage_rows = len(prompt_ids) * len(raw_models)
    if len(triage_rows) != expected_triage_rows:
        fail(f"expected {expected_triage_rows} triage rows, found {len(triage_rows)}")

    score_rows = build_per_row_scores(args.run_id, triage_rows, source_to_gate)
    model_summary = build_model_summary(score_rows)
    gate_summary = build_gate_summary(score_rows, gate_ids)
    review_queue = build_review_queue(score_rows, scenarios)
    candidates = build_atlas_candidates(score_rows, scenarios)

    write_csv(out_dir / "per_row_scores.csv", score_rows, PER_ROW_COLUMNS)
    write_csv(
        out_dir / "model_summary.csv",
        model_summary,
        [
            "model_name",
            "rows",
            "high_priority_rows",
            "medium_priority_rows",
            "low_priority_rows",
            "gate_candidate_rows",
            "needs_clinician_confirmation_rows",
        ],
    )
    write_csv(out_dir / "gate_summary.csv", gate_summary, ["gate_id", "rows", "unique_scenarios", "models"])
    write_tsv(
        out_dir / "clinician_review_queue.tsv",
        review_queue,
        [
            "row_id",
            "scenario_id",
            "domain",
            "setting",
            "expected_safety_focus",
            "model_name",
            "triage_priority",
            "safety_gate_candidates",
            "possible_failure_tags",
            "short_reason",
            "clinician_review_question",
        ],
    )
    write_jsonl(out_dir / "failure_atlas_candidates.jsonl", candidates)
    write_report(out_dir / "RUN_REPORT.md", args.run_id, raw_paths, score_rows, review_queue, candidates)

    print("PASS")
    print(f"Run id: {args.run_id}")
    print(f"Rows: {len(score_rows)}")
    print(f"Review queue rows: {len(review_queue)}")
    print(f"Failure Atlas candidates: {len(candidates)}")
    print(f"Output: {out_dir}")


def validate_inputs(args: argparse.Namespace) -> None:
    args.out_dir = args.out_dir or "/tmp/medical_ai_failure_atlas_benchmark_runner_validate_only"
    run_pipeline(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run internal Failure Atlas benchmark review pipeline.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--run-id", required=True)
        subparser.add_argument("--prompts", required=True)
        subparser.add_argument("--scenario-bank", required=True)
        subparser.add_argument("--rubric", required=True)
        subparser.add_argument("--raw", action="append", required=True)
        subparser.add_argument("--triage", required=True)
        subparser.add_argument("--out-dir", required=True)

    run_parser = subparsers.add_parser("run")
    add_common(run_parser)
    run_parser.set_defaults(func=run_pipeline)

    validate_parser = subparsers.add_parser("validate-inputs")
    add_common(validate_parser)
    validate_parser.set_defaults(func=validate_inputs)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
