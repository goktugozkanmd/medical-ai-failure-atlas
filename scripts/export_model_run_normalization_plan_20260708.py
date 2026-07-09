#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TARGET_PROMPT_COUNT = 30
OUTPUT_JSON = ROOT / "docs" / "model_run_normalization_plan_20260708.json"
OUTPUT_MD = ROOT / "docs" / "MODEL_RUN_NORMALIZATION_PLAN_20260708.md"

PUBLIC_PROMPT_RE = re.compile(r"(\d+)\s*[- ]prompt", re.IGNORECASE)

MODEL_ARTIFACTS: dict[str, list[dict[str, str]]] = {
    "Llama 3.1-8B-Instruct": [
        {"kind": "weekly_score_summary", "path": "model_runs/weekly_eval_llama-3.1-8b-instruct_20260705_171309.json"},
    ],
    "Qwen 2.5-7B-Instruct": [
        {"kind": "weekly_score_summary", "path": "model_runs/weekly_eval_qwen-2.5-7b-instruct_20260704_204124.json"},
    ],
    "Kimi K2.6": [
        {"kind": "partial_raw_outputs", "path": "model_runs/weekly_eval_kimi-k2.6_20260704_160510.json"},
        {"kind": "partial_run_metadata", "path": "model_runs/weekly_eval_kimi-k2.6_20260704_160510.run_metadata.json"},
    ],
    "Qwen 3.7 Max": [
        {"kind": "weekly_raw_outputs", "path": "model_runs/weekly_eval_qwen-3.7-max_20260704_150000.json"},
        {"kind": "weekly_run_metadata", "path": "model_runs/weekly_eval_qwen-3.7-max_20260704_150000.run_metadata.json"},
        {"kind": "hard30_raw_outputs", "path": "model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_raw_outputs.json"},
        {"kind": "hard30_rule_scores", "path": "model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_rule_scores.json"},
    ],
    "Qwen 3.6 Plus": [
        {"kind": "weekly_raw_outputs", "path": "model_runs/weekly_eval_qwen-3.6-plus_20260704_140751.json"},
        {"kind": "weekly_run_metadata", "path": "model_runs/weekly_eval_qwen-3.6-plus_20260704_140751.run_metadata.json"},
    ],
    "DeepSeek V3.2": [
        {"kind": "weekly_raw_outputs", "path": "model_runs/weekly_eval_deepseek-v3.2_20260704_130631.json"},
        {"kind": "weekly_run_metadata", "path": "model_runs/weekly_eval_deepseek-v3.2_20260704_130631.run_metadata.json"},
    ],
    "Kimi K2.7 Code": [
        {"kind": "weekly_raw_outputs", "path": "model_runs/weekly_eval_kimi-k2.7-code_20260704_130620.json"},
        {"kind": "weekly_run_metadata", "path": "model_runs/weekly_eval_kimi-k2.7-code_20260704_130620.run_metadata.json"},
    ],
    "GLM-5.2": [
        {"kind": "weekly_raw_outputs", "path": "model_runs/weekly_eval_glm-5.2_20260704_130522.json"},
        {"kind": "weekly_run_metadata", "path": "model_runs/weekly_eval_glm-5.2_20260704_130522.run_metadata.json"},
    ],
    "DeepSeek V4 Pro": [
        {"kind": "weekly_score_summary", "path": "model_runs/weekly_eval_deepseek-v4-pro_20260704_120507.json"},
        {"kind": "hard30_raw_outputs", "path": "model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_raw_outputs.json"},
        {"kind": "hard30_run_metadata", "path": "model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_raw_outputs.run_metadata.json"},
        {"kind": "hard30_rule_scores", "path": "model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_rule_scores.json"},
    ],
    "DeepSeek V4 Flash": [
        {"kind": "weekly_score_summary", "path": "model_runs/weekly_eval_deepseek-v4-flash_20260704_120225.json"},
    ],
}


def main() -> int:
    submissions_payload = read_json(ROOT / "leaderboard" / "submissions.json")
    submissions = submissions_payload.get("submissions", [])
    if not isinstance(submissions, list):
        raise TypeError("leaderboard/submissions.json submissions must be a list")

    worst_case = load_worst_case_counts()
    models = [build_model_row(submission, worst_case) for submission in submissions]
    totals = {
        "public_normalization_gap_rows": sum(row["public_additional_needed"] for row in models),
        "provider_generation_gap_rows": sum(row["local_missing_prompt_count"] for row in models),
        "local_score_or_promotion_gap_rows": sum(row["local_score_or_promotion_gap"] for row in models),
    }

    manifest = {
        "artifact_id": "model_run_normalization_plan_20260708",
        "status": "local_manifest_and_score_table_plan",
        "created_date": "2026-07-08",
        "target_prompt_count": TARGET_PROMPT_COUNT,
        "public_models_count": len(models),
        "external_action_allowed": False,
        "provider_api_call_allowed": False,
        "automation_started": False,
        "new_cases_added": False,
        "agent_selected_physicians": False,
        "contains_patient_data": False,
        "no_clinical_validation_claim": True,
        "no_model_ranking": True,
        "no_official_compatibility_claim": True,
        "source_files": [
            "leaderboard/submissions.json",
            "model_runs/worst_case_safety_report_v0_1.json",
            "model_runs/",
        ],
        "score_table_scope": {
            "purpose": "normalize existing public model runs toward the shared 30 prompt hard set",
            "ranking_allowed": False,
            "public_claim_allowed": False,
            "provider_call_allowed": False,
            "new_prompt_or_case_creation_allowed": False,
        },
        "totals": totals,
        "models": models,
        "blocked_actions": [
            "start_provider_api_calls_without_user_approval",
            "add_new_cases_for_this_step",
            "rank_models_from_partial_rows",
            "claim_clinical_validation",
            "publish_or_submit_without_fresh_audit",
            "select_or_contact_physicians_by_agent",
        ],
        "next_safe_actions": [
            "promote or rescore existing DeepSeek V4 Pro hard30 local artifacts into a draft score table",
            "close the GLM 5.2 public table gap from existing local 30 row output before any provider call",
            "keep short set models parked until the user approves any provider generation budget",
        ],
    }

    OUTPUT_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(manifest), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_MD.relative_to(ROOT)}")
    print(f"public_models={len(models)}")
    print(f"public_normalization_gap_rows={totals['public_normalization_gap_rows']}")
    return 0


def build_model_row(submission: dict[str, Any], worst_case: dict[str, int]) -> dict[str, Any]:
    model_name = str(submission.get("model_name", "")).strip()
    if not model_name:
        raise ValueError("submission missing model_name")
    worst_case_count = worst_case.get(slugify_model(model_name))
    public_count = extract_public_prompt_count(str(submission.get("notes", "")), worst_case_count)
    artifacts = collect_artifacts(model_name)
    local_completed = max([public_count, *[artifact["row_count"] for artifact in artifacts]], default=public_count)
    local_completed = min(local_completed, TARGET_PROMPT_COUNT)
    public_gap = max(0, TARGET_PROMPT_COUNT - public_count)
    local_gap = max(0, TARGET_PROMPT_COUNT - local_completed)
    local_score_or_promotion_gap = max(0, public_gap - local_gap)
    state = classify_state(public_count, local_completed, local_score_or_promotion_gap)

    return {
        "model_name": model_name,
        "submission_id": submission.get("id"),
        "target_prompt_count": TARGET_PROMPT_COUNT,
        "public_prompt_count": public_count,
        "public_additional_needed": public_gap,
        "local_completed_prompt_count": local_completed,
        "local_missing_prompt_count": local_gap,
        "local_score_or_promotion_gap": local_score_or_promotion_gap,
        "worst_case_report_prompt_count": worst_case_count,
        "current_public_score_fields": submission.get("benchmark_scores", {}),
        "public_note": submission.get("notes", ""),
        "local_artifacts": artifacts,
        "state": state,
        "safe_next_action": safe_next_action(state, public_gap, local_gap, local_score_or_promotion_gap),
    }


def collect_artifacts(model_name: str) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for spec in MODEL_ARTIFACTS.get(model_name, []):
        path = ROOT / spec["path"]
        exists = path.exists()
        payload = read_json_or_list(path) if exists else None
        artifacts.append(
            {
                "kind": spec["kind"],
                "path": spec["path"],
                "exists": exists,
                "row_count": count_payload_rows(payload),
                "completion_status": completion_status(payload),
            }
        )
    return artifacts


def extract_public_prompt_count(notes: str, fallback_count: int | None) -> int:
    match = PUBLIC_PROMPT_RE.search(notes)
    if match:
        return int(match.group(1))
    if isinstance(fallback_count, int):
        return fallback_count
    raise ValueError(f"Could not find public prompt count in notes or worst case report: {notes!r}")


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


def completion_status(payload: Any) -> str:
    if isinstance(payload, dict):
        status = payload.get("completion_status")
        if isinstance(status, str):
            return status
        row_counts = payload.get("row_counts")
        if isinstance(row_counts, dict):
            completed = row_counts.get("completed")
            expected = row_counts.get("expected")
            if isinstance(completed, int) and isinstance(expected, int):
                return "completed" if completed == expected else "partial"
    rows = count_payload_rows(payload)
    if rows >= TARGET_PROMPT_COUNT:
        return "completed"
    if rows > 0:
        return "partial"
    return "missing"


def classify_state(public_count: int, local_completed: int, local_score_or_promotion_gap: int) -> str:
    if public_count >= TARGET_PROMPT_COUNT:
        return "public_already_30"
    if local_completed >= TARGET_PROMPT_COUNT and local_score_or_promotion_gap > 0:
        return "local_30_available_public_table_lagging"
    return "provider_generation_needed_later"


def safe_next_action(state: str, public_gap: int, local_gap: int, local_score_gap: int) -> str:
    if state == "public_already_30":
        return "No generation needed; keep as normalization anchor."
    if local_score_gap:
        return f"Use existing local rows to close {local_score_gap} public table rows; no provider call."
    return f"Park {local_gap} missing rows until the user approves provider generation."


def load_worst_case_counts() -> dict[str, int]:
    path = ROOT / "model_runs" / "worst_case_safety_report_v0_1.json"
    payload = read_json(path)
    counts: dict[str, int] = {}
    for row in payload.get("models", []):
        if isinstance(row, dict) and "model" in row and isinstance(row.get("n"), int):
            counts[slugify_model(str(row["model"]))] = int(row["n"])
    return counts


def slugify_model(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def read_json(path: Path) -> dict[str, Any]:
    payload = read_json_or_list(path)
    if not isinstance(payload, dict):
        raise TypeError(f"{path.relative_to(ROOT)} must be a JSON object")
    return payload


def read_json_or_list(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Model Run Normalization Plan",
        "",
        "Date: 2026 07 08",
        "",
        "Status: local manifest and score table plan.",
        "",
        "Purpose: move the current public model run surface toward one shared 30 prompt hard set without adding cases or starting provider calls.",
        "",
        "## Boundary",
        "",
        "No external action, no provider API call, no new case addition, no patient data, no physician selection, no clinical validation claim, no official compatibility claim, and no model ranking.",
        "",
        "## Current Gap",
        "",
        f"- Public models tracked: {manifest['public_models_count']}.",
        f"- Target prompt count per public model: {manifest['target_prompt_count']}.",
        f"- Public normalization gap: {manifest['totals']['public_normalization_gap_rows']} rows.",
        f"- Rows that require future provider generation if approved: {manifest['totals']['provider_generation_gap_rows']}.",
        f"- Rows already available locally but not yet fully reflected in the public score table: {manifest['totals']['local_score_or_promotion_gap_rows']}.",
        "",
        "## Score Table Draft",
        "",
        "| Model | Public rows | Local rows found | Public gap | Provider generation gap | Local score or promotion gap | State |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in manifest["models"]:
        lines.append(
            "| {model_name} | {public_prompt_count} | {local_completed_prompt_count} | "
            "{public_additional_needed} | {local_missing_prompt_count} | "
            "{local_score_or_promotion_gap} | {state} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Immediate Work Order",
            "",
            "1. Promote or rescore the existing DeepSeek V4 Pro hard30 local artifacts into the draft score table.",
            "2. Close the GLM 5.2 table gap from the existing local 30 row output before any provider call.",
            "3. Park models with missing local rows until the user explicitly approves provider generation.",
            "",
            "## Validation",
            "",
            "Run:",
            "",
            "```bash",
            "make model_run_normalization_plan_20260708",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
