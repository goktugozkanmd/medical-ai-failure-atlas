#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TARGET_PROMPT_COUNT = 30
MANIFEST_PATH = ROOT / "docs" / "model_run_promotion_gate_20260708.json"
MD_PATH = ROOT / "docs" / "MODEL_RUN_PROMOTION_GATE_20260708.md"
PROMPT_SET = ROOT / "data" / "prompt_set_v2_hard_30.tsv"

EXPECTED_MODELS = {
    "DeepSeek V4 Pro": {
        "public_prompt_count_before_gate": 5,
        "normalization_gap_closed_locally": 25,
        "source_raw": "model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_raw_outputs.json",
    },
    "GLM-5.2": {
        "public_prompt_count_before_gate": 28,
        "normalization_gap_closed_locally": 2,
        "source_raw": "model_runs/weekly_eval_glm-5.2_20260704_130522.json",
    },
}

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "regulatory compliance achieved",
    "patient data used",
    "agent selected physicians",
    "best model",
    "model winner",
    "superior model",
]


def main() -> int:
    errors: list[str] = []
    for path in [MANIFEST_PATH, MD_PATH, PROMPT_SET]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    manifest = read_json(MANIFEST_PATH, errors)
    prompt_ids = load_prompt_ids(errors)

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
        if manifest.get("totals") != {
            "models_ready_for_local_promotion_review": 2,
            "local_rows_scored": 60,
            "public_rows_closed_by_local_artifacts": 27,
            "provider_generation_rows_used": 0,
        }:
            errors.append(f"Promotion gate totals mismatch: {manifest.get('totals')!r}")

        rows = manifest.get("models", [])
        if not isinstance(rows, list) or len(rows) != 2:
            errors.append("Promotion gate must list exactly two model rows")
            rows = []
        row_by_model = {str(row.get("model_name")): row for row in rows if isinstance(row, dict)}
        if set(row_by_model) != set(EXPECTED_MODELS):
            errors.append(f"Promotion gate model set mismatch: {sorted(row_by_model)}")
        for model_name, expected in EXPECTED_MODELS.items():
            validate_model_row(row_by_model.get(model_name, {}), model_name, expected, prompt_ids, errors)

        blocked = set(manifest.get("blocked_actions", []))
        for required in {
            "publish_public_table_without_user_approval",
            "start_provider_api_calls",
            "rank_models_from_this_gate",
            "claim_clinical_validation",
            "add_new_cases",
            "select_or_contact_physicians_by_agent",
        }:
            if required not in blocked:
                errors.append(f"Promotion gate blocked_actions missing {required}")

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
            "make model_run_promotion_gate_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"Promotion markdown missing boundary phrase: {phrase}")

    for path in [MANIFEST_PATH, MD_PATH]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL model run promotion gate validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS model run promotion gate validation")
    print("models_ready_for_local_promotion_review=2")
    print("local_rows_scored=60")
    print("public_rows_closed_by_local_artifacts=27")
    print("provider_generation_rows_used=0")
    return 0


def validate_model_row(
    row: dict[str, Any],
    model_name: str,
    expected: dict[str, Any],
    prompt_ids: list[str],
    errors: list[str],
) -> None:
    if not row:
        errors.append(f"Missing promotion gate row for {model_name}")
        return
    for key, expected_value in expected.items():
        if row.get(key) != expected_value:
            errors.append(f"{model_name} {key} mismatch: {row.get(key)!r} != {expected_value!r}")
    if row.get("target_prompt_count") != TARGET_PROMPT_COUNT:
        errors.append(f"{model_name} target_prompt_count must be 30")
    if row.get("scored_item_count") != TARGET_PROMPT_COUNT:
        errors.append(f"{model_name} scored_item_count must be 30")
    if row.get("provider_generation_rows_used") != 0:
        errors.append(f"{model_name} provider_generation_rows_used must be 0")
    if row.get("promotion_status") != "ready_for_local_review_not_public":
        errors.append(f"{model_name} promotion_status mismatch")

    source_raw = ROOT / str(row.get("source_raw", ""))
    enriched_raw = ROOT / str(row.get("enriched_raw", ""))
    score_path = ROOT / str(row.get("rule_scores", ""))
    for path in [source_raw, enriched_raw, score_path]:
        if not path.exists():
            errors.append(f"{model_name} missing path: {path}")
            return

    source_rows = read_json_or_list(source_raw, errors)
    if not isinstance(source_rows, list) or len(source_rows) != TARGET_PROMPT_COUNT:
        errors.append(f"{model_name} source raw must have 30 rows")

    enriched_payload = read_json(enriched_raw, errors)
    responses = enriched_payload.get("responses", [])
    if not isinstance(responses, list) or len(responses) != TARGET_PROMPT_COUNT:
        errors.append(f"{model_name} enriched raw must have 30 responses")
    else:
        response_ids = [str(row.get("scenario_id")) for row in responses if isinstance(row, dict)]
        if response_ids != prompt_ids:
            errors.append(f"{model_name} enriched scenario order mismatch")
        if any(not str(row.get("prompt_text", "")).strip() for row in responses if isinstance(row, dict)):
            errors.append(f"{model_name} enriched responses must include prompt_text")

    score_payload = read_json(score_path, errors)
    if score_payload.get("schema_version") != "failure_atlas_scores_v0_1":
        errors.append(f"{model_name} score schema mismatch")
    items = score_payload.get("items", [])
    if not isinstance(items, list) or len(items) != TARGET_PROMPT_COUNT:
        errors.append(f"{model_name} score items must have 30 rows")
    else:
        item_ids = [str(item.get("scenario_id")) for item in items if isinstance(item, dict)]
        if item_ids != prompt_ids:
            errors.append(f"{model_name} score scenario order mismatch")
        if any(not str(item.get("prompt_text", "")).strip() for item in items if isinstance(item, dict)):
            errors.append(f"{model_name} score items must include prompt_text")
    aggregates = score_payload.get("aggregates", {})
    if not isinstance(aggregates, dict) or aggregates.get("item_count") != TARGET_PROMPT_COUNT:
        errors.append(f"{model_name} aggregate item_count must be 30")


def load_prompt_ids(errors: list[str]) -> list[str]:
    if not PROMPT_SET.exists():
        return []
    with PROMPT_SET.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    prompt_ids = [row.get("scenario_id", "") for row in rows]
    if len(prompt_ids) != TARGET_PROMPT_COUNT:
        errors.append("Prompt set must contain 30 rows")
    return prompt_ids


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
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


if __name__ == "__main__":
    sys.exit(main())
