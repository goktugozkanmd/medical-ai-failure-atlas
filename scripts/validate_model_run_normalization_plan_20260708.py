#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TARGET_PROMPT_COUNT = 30
MANIFEST_PATH = ROOT / "docs" / "model_run_normalization_plan_20260708.json"
MD_PATH = ROOT / "docs" / "MODEL_RUN_NORMALIZATION_PLAN_20260708.md"
SUBMISSIONS_PATH = ROOT / "leaderboard" / "submissions.json"
WORST_CASE_PATH = ROOT / "model_runs" / "worst_case_safety_report_v0_1.json"

PUBLIC_PROMPT_RE = re.compile(r"(\d+)\s*[- ]prompt", re.IGNORECASE)

EXPECTED_PUBLIC_COUNTS = {
    "Llama 3.1-8B-Instruct": 5,
    "Qwen 2.5-7B-Instruct": 5,
    "Kimi K2.6": 6,
    "Qwen 3.7 Max": 30,
    "Qwen 3.6 Plus": 30,
    "DeepSeek V3.2": 5,
    "Kimi K2.7 Code": 5,
    "GLM-5.2": 28,
    "DeepSeek V4 Pro": 5,
    "DeepSeek V4 Flash": 5,
}

EXPECTED_STATES = {
    "Llama 3.1-8B-Instruct": "provider_generation_needed_later",
    "Qwen 2.5-7B-Instruct": "provider_generation_needed_later",
    "Kimi K2.6": "provider_generation_needed_later",
    "Qwen 3.7 Max": "public_already_30",
    "Qwen 3.6 Plus": "public_already_30",
    "DeepSeek V3.2": "provider_generation_needed_later",
    "Kimi K2.7 Code": "provider_generation_needed_later",
    "GLM-5.2": "local_30_available_public_table_lagging",
    "DeepSeek V4 Pro": "local_30_available_public_table_lagging",
    "DeepSeek V4 Flash": "provider_generation_needed_later",
}

EXPECTED_LOCAL_COMPLETED = {
    "Llama 3.1-8B-Instruct": 5,
    "Qwen 2.5-7B-Instruct": 5,
    "Kimi K2.6": 6,
    "Qwen 3.7 Max": 30,
    "Qwen 3.6 Plus": 30,
    "DeepSeek V3.2": 5,
    "Kimi K2.7 Code": 5,
    "GLM-5.2": 30,
    "DeepSeek V4 Pro": 30,
    "DeepSeek V4 Flash": 5,
}

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "regulatory compliance achieved",
    "accepted by medhelm",
    "accepted by inspect evals",
    "patient data used",
    "agent selected physicians",
    "best model",
    "model winner",
]


def main() -> int:
    errors: list[str] = []
    for path in [MANIFEST_PATH, MD_PATH, SUBMISSIONS_PATH, WORST_CASE_PATH]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    manifest = read_json(MANIFEST_PATH, errors)
    submissions = read_json(SUBMISSIONS_PATH, errors)
    worst_case_counts = load_worst_case_counts(errors)

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
            "no_official_compatibility_claim": True,
        }
        for key, expected in expected_flags.items():
            if manifest.get(key) is not expected:
                errors.append(f"Manifest {key} must be {expected!r}")
        if manifest.get("target_prompt_count") != TARGET_PROMPT_COUNT:
            errors.append("Manifest target_prompt_count must be 30")
        if manifest.get("public_models_count") != 10:
            errors.append("Manifest public_models_count must be 10")

        models = manifest.get("models", [])
        if not isinstance(models, list):
            errors.append("Manifest models must be a list")
            models = []
        rows_by_model = {str(row.get("model_name")): row for row in models if isinstance(row, dict)}
        if set(rows_by_model) != set(EXPECTED_PUBLIC_COUNTS):
            errors.append(f"Manifest model set mismatch: {sorted(rows_by_model)}")

        totals = manifest.get("totals", {})
        if totals != {
            "public_normalization_gap_rows": 176,
            "provider_generation_gap_rows": 149,
            "local_score_or_promotion_gap_rows": 27,
        }:
            errors.append(f"Manifest totals mismatch: {totals!r}")

        for model_name, public_count in EXPECTED_PUBLIC_COUNTS.items():
            row = rows_by_model.get(model_name, {})
            validate_model_row(row, model_name, public_count, worst_case_counts, errors)

        blocked = set(manifest.get("blocked_actions", []))
        for required in {
            "start_provider_api_calls_without_user_approval",
            "add_new_cases_for_this_step",
            "rank_models_from_partial_rows",
            "claim_clinical_validation",
            "publish_or_submit_without_fresh_audit",
            "select_or_contact_physicians_by_agent",
        }:
            if required not in blocked:
                errors.append(f"Manifest blocked_actions missing {required}")

    if submissions:
        submission_rows = submissions.get("submissions", [])
        if not isinstance(submission_rows, list) or len(submission_rows) != 10:
            errors.append("Leaderboard submissions must contain 10 public rows")
        else:
            for submission in submission_rows:
                model_name = str(submission.get("model_name", ""))
                live_count = extract_live_public_count(submission, worst_case_counts, errors)
                expected = EXPECTED_PUBLIC_COUNTS.get(model_name)
                if expected is None:
                    errors.append(f"Unexpected public model in leaderboard: {model_name}")
                elif live_count != expected:
                    errors.append(f"Live public count mismatch for {model_name}: {live_count} != {expected}")

    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in [
            "No external action",
            "no provider API call",
            "no new case addition",
            "no patient data",
            "no physician selection",
            "no clinical validation claim",
            "no model ranking",
            "make model_run_normalization_plan_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"Plan markdown missing boundary phrase: {phrase}")
        for model_name in EXPECTED_PUBLIC_COUNTS:
            if model_name not in text:
                errors.append(f"Plan markdown missing model: {model_name}")

    for path in [MANIFEST_PATH, MD_PATH]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL model run normalization plan validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS model run normalization plan validation")
    print("public_models=10")
    print("target_prompt_count=30")
    print("public_normalization_gap_rows=176")
    print("provider_generation_gap_rows=149")
    print("local_score_or_promotion_gap_rows=27")
    return 0


def validate_model_row(
    row: dict[str, Any],
    model_name: str,
    public_count: int,
    worst_case_counts: dict[str, int],
    errors: list[str],
) -> None:
    if not row:
        errors.append(f"Missing manifest row for {model_name}")
        return
    if row.get("target_prompt_count") != TARGET_PROMPT_COUNT:
        errors.append(f"{model_name} target_prompt_count must be 30")
    if row.get("public_prompt_count") != public_count:
        errors.append(f"{model_name} public_prompt_count mismatch")
    expected_public_gap = max(0, TARGET_PROMPT_COUNT - public_count)
    if row.get("public_additional_needed") != expected_public_gap:
        errors.append(f"{model_name} public_additional_needed mismatch")
    if row.get("local_completed_prompt_count") != EXPECTED_LOCAL_COMPLETED[model_name]:
        errors.append(f"{model_name} local_completed_prompt_count mismatch")
    expected_local_gap = max(0, TARGET_PROMPT_COUNT - EXPECTED_LOCAL_COMPLETED[model_name])
    if row.get("local_missing_prompt_count") != expected_local_gap:
        errors.append(f"{model_name} local_missing_prompt_count mismatch")
    expected_local_score_gap = max(0, expected_public_gap - expected_local_gap)
    if row.get("local_score_or_promotion_gap") != expected_local_score_gap:
        errors.append(f"{model_name} local_score_or_promotion_gap mismatch")
    if row.get("state") != EXPECTED_STATES[model_name]:
        errors.append(f"{model_name} state mismatch: {row.get('state')!r}")

    expected_worst_case = worst_case_counts.get(slugify_model(model_name))
    if row.get("worst_case_report_prompt_count") != expected_worst_case:
        errors.append(f"{model_name} worst_case_report_prompt_count mismatch")

    artifacts = row.get("local_artifacts", [])
    if not isinstance(artifacts, list):
        errors.append(f"{model_name} local_artifacts must be a list")
        return
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            errors.append(f"{model_name} local_artifact must be an object")
            continue
        path = ROOT / str(artifact.get("path", ""))
        if artifact.get("exists") is not True:
            errors.append(f"{model_name} artifact must exist: {artifact.get('path')}")
        elif not path.exists():
            errors.append(f"{model_name} artifact path missing: {artifact.get('path')}")
        else:
            live_count = count_payload_rows(read_json_or_list(path, errors))
            if artifact.get("row_count") != live_count:
                errors.append(f"{model_name} artifact row_count mismatch for {artifact.get('path')}")


def extract_live_public_count(
    submission: dict[str, Any],
    worst_case_counts: dict[str, int],
    errors: list[str],
) -> int | None:
    notes = str(submission.get("notes", ""))
    match = PUBLIC_PROMPT_RE.search(notes)
    if match:
        return int(match.group(1))
    model_name = str(submission.get("model_name", ""))
    fallback = worst_case_counts.get(slugify_model(model_name))
    if fallback is None:
        errors.append(f"Could not derive live public prompt count for {model_name}")
    return fallback


def load_worst_case_counts(errors: list[str]) -> dict[str, int]:
    payload = read_json(WORST_CASE_PATH, errors)
    counts: dict[str, int] = {}
    for row in payload.get("models", []):
        if isinstance(row, dict) and isinstance(row.get("model"), str) and isinstance(row.get("n"), int):
            counts[slugify_model(str(row["model"]))] = int(row["n"])
    return counts


def count_payload_rows(payload: Any) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        row_counts = payload.get("row_counts")
        if isinstance(row_counts, dict) and isinstance(row_counts.get("completed"), int):
            return int(row_counts["completed"])
        if isinstance(payload.get("prompts_evaluated"), int):
            return int(payload["prompts_evaluated"])
        for key in ("items", "prompt_results", "outputs", "results", "scores", "responses", "raw_outputs"):
            value = payload.get(key)
            if isinstance(value, list):
                return len(value)
    return 0


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
        errors.append(f"Missing JSON file: {path.relative_to(ROOT)}")
        return {}
    payload = read_json_or_list(path, errors)
    if not isinstance(payload, dict):
        errors.append(f"JSON must be an object: {path.relative_to(ROOT)}")
        return {}
    return payload


def read_json_or_list(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}


def slugify_model(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


if __name__ == "__main__":
    sys.exit(main())
