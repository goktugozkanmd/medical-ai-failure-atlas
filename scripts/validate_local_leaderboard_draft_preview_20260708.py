#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "local_leaderboard_draft_preview_20260708.json"
MD_PATH = ROOT / "docs" / "LOCAL_LEADERBOARD_DRAFT_PREVIEW_20260708.md"
LEADERBOARD = ROOT / "leaderboard" / "submissions.json"

EXPECTED_MODELS = {
    "DeepSeek V4 Pro": {"current_public_prompt_count": 5, "draft_prompt_count": 30, "local_rows_closing_public_gap": 25},
    "GLM-5.2": {"current_public_prompt_count": 28, "draft_prompt_count": 30, "local_rows_closing_public_gap": 2},
}

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "regulatory compliance achieved",
    "officially compatible",
    "patient data used",
    "agent selected physicians",
    "best model",
    "model winner",
]


def main() -> int:
    errors: list[str] = []
    for path in [JSON_PATH, MD_PATH, LEADERBOARD]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    manifest = read_json(JSON_PATH, errors)
    leaderboard = read_json(LEADERBOARD, errors)
    if manifest:
        expected_flags = {
            "external_action_allowed": False,
            "provider_api_call_allowed": False,
            "automation_started": False,
            "public_leaderboard_modified": False,
            "new_cases_added": False,
            "agent_selected_physicians": False,
            "contains_patient_data": False,
            "no_clinical_validation_claim": True,
            "no_model_ranking": True,
            "no_official_compatibility_claim": True,
        }
        for key, expected in expected_flags.items():
            if manifest.get(key) is not expected:
                errors.append(f"Preview {key} must be {expected!r}")
        if manifest.get("source_leaderboard_sha256") != sha256(LEADERBOARD):
            errors.append("Preview source_leaderboard_sha256 mismatch")
        scope = manifest.get("draft_scope", {})
        if scope != {
            "purpose": "show how existing local 30 row artifacts could close part of the public leaderboard prompt count gap",
            "models_in_preview": 2,
            "public_rows_closed_by_local_artifacts": 27,
            "provider_generation_rows_used": 0,
            "public_write_allowed": False,
        }:
            errors.append(f"Preview draft_scope mismatch: {scope!r}")

        rows = manifest.get("draft_rows", [])
        if not isinstance(rows, list) or len(rows) != 2:
            errors.append("Preview must contain exactly two draft rows")
            rows = []
        by_model = {str(row.get("model_name")): row for row in rows if isinstance(row, dict)}
        if set(by_model) != set(EXPECTED_MODELS):
            errors.append(f"Preview model set mismatch: {sorted(by_model)}")
        for model_name, expected in EXPECTED_MODELS.items():
            validate_row(by_model.get(model_name, {}), model_name, expected, errors)

        blocked = set(manifest.get("blocked_actions", []))
        for required in {
            "write_leaderboard_submissions_json",
            "publish_preview_without_user_approval",
            "rank_models_from_preview",
            "claim_clinical_validation",
            "start_provider_api_calls",
            "add_new_cases",
        }:
            if required not in blocked:
                errors.append(f"Preview blocked_actions missing {required}")

    if leaderboard:
        submissions = leaderboard.get("submissions", [])
        if not isinstance(submissions, list) or len(submissions) != 10:
            errors.append("Public leaderboard must remain at 10 submissions")
        for row in submissions if isinstance(submissions, list) else []:
            if row.get("model_name") == "DeepSeek V4 Pro" and "5-prompt subset" not in str(row.get("notes", "")):
                errors.append("Public DeepSeek V4 Pro row should remain unchanged at 5-prompt subset")
            if row.get("model_name") == "GLM-5.2" and "28-prompt set" not in str(row.get("notes", "")):
                errors.append("Public GLM-5.2 row should remain unchanged at 28-prompt set")

    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in [
            "Local Leaderboard Draft Preview",
            "public leaderboard file was not changed",
            "No external send",
            "no provider API call",
            "no public leaderboard write",
            "no new case addition",
            "no patient data",
            "no clinical validation claim",
            "no model ranking",
            "make local_leaderboard_draft_preview_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"Preview markdown missing required phrase: {phrase}")

    for path in [JSON_PATH, MD_PATH]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL local leaderboard draft preview validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS local leaderboard draft preview validation")
    print("models_in_preview=2")
    print("public_rows_closed_by_local_artifacts=27")
    print("public_leaderboard_modified=false")
    return 0


def validate_row(row: dict[str, Any], model_name: str, expected: dict[str, int], errors: list[str]) -> None:
    if not row:
        errors.append(f"Missing preview row for {model_name}")
        return
    for key, value in expected.items():
        if row.get(key) != value:
            errors.append(f"{model_name} {key} mismatch: {row.get(key)!r} != {value!r}")
    if row.get("provider_generation_rows_used") != 0:
        errors.append(f"{model_name} provider_generation_rows_used must be 0")
    if row.get("draft_status") != "local_preview_only_not_written_to_public_leaderboard":
        errors.append(f"{model_name} draft_status mismatch")
    score_file = ROOT / str(row.get("score_file", ""))
    if not score_file.exists():
        errors.append(f"{model_name} score_file missing: {row.get('score_file')}")
    score_payload = read_json(score_file, errors)
    if score_payload and score_payload.get("aggregates", {}).get("item_count") != 30:
        errors.append(f"{model_name} score_file must have 30 scored items")
    scores = row.get("draft_scores_from_local_rule_scores", {})
    if not isinstance(scores, dict):
        errors.append(f"{model_name} draft_scores_from_local_rule_scores must be an object")
        return
    for key in ["safety_score", "source_support_score", "clinical_boundary_score"]:
        value = scores.get(key)
        if not isinstance(value, (int, float)) or value < 0 or value > 100:
            errors.append(f"{model_name} {key} must be a 0 to 100 numeric score")


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"JSON must be an object: {path.relative_to(ROOT)}")
        return {}
    return payload


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    sys.exit(main())
