#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCENARIO_BANK_FILES = [
    "data/scenario_bank_v1.tsv",
    "data/scenario_bank_v2_hard_addendum.tsv",
    "data/scenario_bank_v3_scale_seed.tsv",
]

PROMPT_SET_FILES = [
    "data/prompt_set_v1.tsv",
    "data/prompt_set_v2_hard_30.tsv",
    "data/prompt_set_v3_scale_30.tsv",
]

REQUIRED_FILES = [
    "docs/BATCH_EXPANSION_PLAN_V0_3.md",
    "docs/controlled_batch_expansion_plan_20260708.json",
]

FORBIDDEN_TEXT = [
    "300-500",
    "300–500",
    "500 Rows",
    "500-scenario",
    "15-20 Model",
    "all active working rows are the same validation tier",
    "clinical validation is complete",
    "patient data used",
]


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).exists():
            errors.append(f"Missing required file: {relative}")

    manifest = read_json(ROOT / "docs" / "controlled_batch_expansion_plan_20260708.json", errors)
    plan_text = (ROOT / "docs" / "BATCH_EXPANSION_PLAN_V0_3.md").read_text(encoding="utf-8")

    scenario_bank_rows = sum(count_tsv_rows(ROOT / relative) for relative in SCENARIO_BANK_FILES)
    prompt_set_rows = sum(count_tsv_rows(ROOT / relative) for relative in PROMPT_SET_FILES)
    safetyguard_rows = count_tsv_rows(ROOT / "safetyguard" / "data" / "medfailbench_prompts_v0_2.tsv")
    leaderboard_rows, leaderboard_categories = count_jsonl_categories(
        ROOT / "leaderboard" / "medfailbench_prompts_v0_2.jsonl"
    )
    turkish_rows = count_jsonl_rows(ROOT / "data" / "tr_medllm_synthetic_eval_set_v0_3.jsonl")
    drift_rows = count_tsv_rows(ROOT / "data" / "tr_en_drift_glm_probe_v0_1.tsv")
    panel_rows = count_tsv_rows(ROOT / "data" / "panel_pilot" / "clinician_panel_pilot_cases_v0_1.tsv")

    expected_counts = {
        "scenario_bank_core_rows": scenario_bank_rows,
        "public_prompt_set_rows": prompt_set_rows,
        "safetyguard_prompt_surface_rows": safetyguard_rows,
        "leaderboard_prompt_surface_rows": leaderboard_rows,
        "turkish_medllm_rows": turkish_rows,
        "tr_en_drift_probe_rows": drift_rows,
        "panel_pilot_rows": panel_rows,
    }

    if manifest:
        expected_flags = {
            "external_action_allowed": False,
            "provider_api_call_allowed": False,
            "automation_started": False,
            "new_cases_added": False,
            "agent_selected_physicians": False,
            "contains_patient_data": False,
            "no_clinical_validation_claim": True,
            "no_model_ranking": True,
            "separate_validation_tiers": True,
        }
        for key, expected in expected_flags.items():
            if manifest.get(key) is not expected:
                errors.append(f"Manifest {key} must be {expected!r}")
        if manifest.get("max_core_release_rows") != 300:
            errors.append("Manifest max_core_release_rows must be 300")
        if manifest.get("current_counts") != expected_counts:
            errors.append(
                "Manifest current_counts mismatch: "
                f"expected {expected_counts!r}, found {manifest.get('current_counts')!r}"
            )
        expected_categories = {
            "turkish_safety": 36,
            "bilingual_drift": 100,
            "case_intake": 86,
        }
        if leaderboard_categories != expected_categories:
            errors.append(f"Live leaderboard categories mismatch: {leaderboard_categories!r}")
        if manifest.get("leaderboard_prompt_categories") != expected_categories:
            errors.append("Manifest leaderboard prompt categories mismatch")
        phases = manifest.get("phases", [])
        if len(phases) != 3:
            errors.append("Manifest must contain three phases")
        for phase in phases:
            target = phase.get("target_core_rows")
            if not isinstance(target, int):
                errors.append(f"Phase target_core_rows must be int: {phase!r}")
            elif target > manifest.get("max_core_release_rows", 0):
                errors.append(f"Phase target exceeds core cap: {phase!r}")
        blocked = set(manifest.get("blocked_actions", []))
        for required in {
            "merge_validation_tiers",
            "claim_300_rows_exist_now",
            "claim_external_panel_complete",
            "add_patient_data",
            "start_paid_provider_runs_without_g_approval",
            "publish_release_without_fresh_audit",
        }:
            if required not in blocked:
                errors.append(f"Manifest blocked_actions missing {required}")

    for phrase in FORBIDDEN_TEXT:
        if phrase.lower() in plan_text.lower():
            errors.append(f"Plan contains forbidden stale wording: {phrase}")
    for required_phrase in [
        "hard cap of 300 public core scenario bank rows",
        "not one validation tier",
        "No patient data",
        "New cases were added in this planning step",
        "make controlled_batch_expansion_20260708",
    ]:
        if required_phrase.lower() not in plan_text.lower():
            errors.append(f"Plan missing required guardrail phrase: {required_phrase}")

    if scenario_bank_rows != 150:
        errors.append(f"Expected 150 core scenario rows, found {scenario_bank_rows}")
    if prompt_set_rows != 70:
        errors.append(f"Expected 70 public prompt set rows, found {prompt_set_rows}")
    if safetyguard_rows != 222 or leaderboard_rows != 222:
        errors.append(f"Expected 222 SafetyGuard and leaderboard rows, found {safetyguard_rows}/{leaderboard_rows}")
    if scenario_bank_rows > 300:
        errors.append("Core scenario bank already exceeds the 300 row cap")

    if errors:
        print("FAIL controlled batch expansion validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS controlled batch expansion validation")
    print(f"core_scenario_rows={scenario_bank_rows}")
    print(f"public_prompt_set_rows={prompt_set_rows}")
    print(f"safetyguard_prompt_rows={safetyguard_rows}")
    print("core_release_cap=300")
    return 0


def read_json(path: Path, errors: list[str]) -> dict:
    if not path.exists():
        errors.append(f"Missing JSON file: {path.relative_to(ROOT)}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}


def count_tsv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return max(0, sum(1 for _ in csv.reader(handle, delimiter="\t")) - 1)


def count_jsonl_rows(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def count_jsonl_categories(path: Path) -> tuple[int, dict[str, int]]:
    counts: dict[str, int] = {}
    rows = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows += 1
        payload = json.loads(line)
        category = str(payload.get("category", ""))
        counts[category] = counts.get(category, 0) + 1
    return rows, counts


if __name__ == "__main__":
    raise SystemExit(main())
