#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from failure_atlas.scorer import score_raw_output


TARGET_PROMPT_COUNT = 30
PROMPT_SET = ROOT / "data" / "prompt_set_v2_hard_30.tsv"
RUBRIC = ROOT / "data" / "scoring_rubric_v0_3.json"
OUTPUT_DIR = ROOT / "model_runs" / "model_run_normalization_20260708"
MANIFEST_PATH = ROOT / "docs" / "model_run_promotion_gate_20260708.json"
MD_PATH = ROOT / "docs" / "MODEL_RUN_PROMOTION_GATE_20260708.md"

MODELS = [
    {
        "model_name": "DeepSeek V4 Pro",
        "model_id": "deepseek_v4_pro_hard30_enriched",
        "source_raw": "model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_raw_outputs.json",
        "public_prompt_count": 5,
        "normalization_gap_closed_locally": 25,
    },
    {
        "model_name": "GLM-5.2",
        "model_id": "glm_5_2_hard30_enriched",
        "source_raw": "model_runs/weekly_eval_glm-5.2_20260704_130522.json",
        "public_prompt_count": 28,
        "normalization_gap_closed_locally": 2,
    },
]


def main() -> int:
    prompt_map = load_prompt_map(PROMPT_SET)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for model in MODELS:
        rows.append(process_model(model, prompt_map))

    manifest = {
        "artifact_id": "model_run_promotion_gate_20260708",
        "status": "local_score_table_promotion_gate",
        "created_date": "2026-07-08",
        "target_prompt_count": TARGET_PROMPT_COUNT,
        "external_action_allowed": False,
        "provider_api_call_allowed": False,
        "automation_started": False,
        "new_cases_added": False,
        "agent_selected_physicians": False,
        "contains_patient_data": False,
        "no_clinical_validation_claim": True,
        "no_model_ranking": True,
        "no_official_compatibility_claim": True,
        "source_prompt_set": "data/prompt_set_v2_hard_30.tsv",
        "rubric": "data/scoring_rubric_v0_3.json",
        "models": rows,
        "totals": {
            "models_ready_for_local_promotion_review": len(rows),
            "local_rows_scored": sum(row["scored_item_count"] for row in rows),
            "public_rows_closed_by_local_artifacts": sum(row["normalization_gap_closed_locally"] for row in rows),
            "provider_generation_rows_used": 0,
        },
        "blocked_actions": [
            "publish_public_table_without_user_approval",
            "start_provider_api_calls",
            "rank_models_from_this_gate",
            "claim_clinical_validation",
            "add_new_cases",
            "select_or_contact_physicians_by_agent",
        ],
        "next_safe_actions": [
            "review this local score table for schema and row consistency",
            "decide whether DeepSeek V4 Pro hard30 and GLM 5.2 rows should update the public leaderboard draft",
            "keep the remaining 149 provider generation rows blocked until explicit user approval",
        ],
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(manifest), encoding="utf-8")

    print(f"Wrote {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")
    print(f"local_rows_scored={manifest['totals']['local_rows_scored']}")
    print(f"public_rows_closed_by_local_artifacts={manifest['totals']['public_rows_closed_by_local_artifacts']}")
    return 0


def process_model(model: dict[str, Any], prompt_map: dict[str, str]) -> dict[str, Any]:
    source_raw = ROOT / str(model["source_raw"])
    raw_rows = json.loads(source_raw.read_text(encoding="utf-8"))
    if not isinstance(raw_rows, list):
        raise TypeError(f"{source_raw.relative_to(ROOT)} must be a legacy raw output list")
    if len(raw_rows) != TARGET_PROMPT_COUNT:
        raise ValueError(f"{source_raw.relative_to(ROOT)} must contain 30 rows, found {len(raw_rows)}")

    enriched_rows = []
    for row in raw_rows:
        if not isinstance(row, dict):
            raise TypeError("raw output row must be an object")
        scenario_id = str(row.get("scenario_id", "")).strip()
        if scenario_id not in prompt_map:
            raise ValueError(f"Missing prompt text for {scenario_id}")
        enriched = dict(row)
        enriched["prompt_text"] = prompt_map[scenario_id]
        enriched_rows.append(enriched)

    model_id = str(model["model_id"])
    enriched_path = OUTPUT_DIR / f"{model_id}_raw_outputs.json"
    score_path = OUTPUT_DIR / f"{model_id}_rule_scores.json"
    enriched_payload = {
        "model_name": model_id,
        "responses": enriched_rows,
    }
    enriched_path.write_text(json.dumps(enriched_payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    scores = score_raw_output(
        raw_path=enriched_path,
        rubric_path=RUBRIC,
        method="rule",
        output_path=score_path,
    )
    aggregates = scores.get("aggregates", {})
    item_count = int(aggregates.get("item_count", 0))
    if item_count != TARGET_PROMPT_COUNT:
        raise ValueError(f"{score_path.relative_to(ROOT)} scored {item_count} rows")

    return {
        "model_name": model["model_name"],
        "model_id": model_id,
        "source_raw": model["source_raw"],
        "enriched_raw": str(enriched_path.relative_to(ROOT)),
        "rule_scores": str(score_path.relative_to(ROOT)),
        "public_prompt_count_before_gate": model["public_prompt_count"],
        "target_prompt_count": TARGET_PROMPT_COUNT,
        "scored_item_count": item_count,
        "normalization_gap_closed_locally": model["normalization_gap_closed_locally"],
        "provider_generation_rows_used": 0,
        "mean_scores": aggregates.get("mean_scores", {}),
        "final_label_counts": aggregates.get("final_label_counts", {}),
        "safety_gate_counts": aggregates.get("safety_gate_counts", {}),
        "promotion_status": "ready_for_local_review_not_public",
    }


def load_prompt_map(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    prompt_map = {row["scenario_id"]: row["prompt_text"] for row in rows}
    if len(prompt_map) != TARGET_PROMPT_COUNT:
        raise ValueError(f"Expected 30 prompts in {path.relative_to(ROOT)}, found {len(prompt_map)}")
    return prompt_map


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Model Run Promotion Gate",
        "",
        "Date: 2026 07 08",
        "",
        "Status: local score table promotion gate.",
        "",
        "Purpose: close the local part of the 30 prompt normalization gap for DeepSeek V4 Pro and GLM 5.2 without provider calls.",
        "",
        "## Boundary",
        "",
        "No external action, no provider API call, no new case addition, no patient data, no physician selection, no clinical validation claim, no official compatibility claim, and no model ranking.",
        "",
        "## Local Rows",
        "",
        f"- Models ready for local promotion review: {manifest['totals']['models_ready_for_local_promotion_review']}.",
        f"- Local rows scored in this gate: {manifest['totals']['local_rows_scored']}.",
        f"- Public rows that this can close from existing local artifacts: {manifest['totals']['public_rows_closed_by_local_artifacts']}.",
        f"- Provider generation rows used: {manifest['totals']['provider_generation_rows_used']}.",
        "",
        "## Draft Score Table",
        "",
        "| Model | Public rows before | Scored local rows | Local gap closed | Promotion status | Score file |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in manifest["models"]:
        lines.append(
            "| {model_name} | {public_prompt_count_before_gate} | {scored_item_count} | "
            "{normalization_gap_closed_locally} | {promotion_status} | `{rule_scores}` |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Next",
            "",
            "1. Review schema and row consistency for the two local score files.",
            "2. Decide whether these rows should update a public leaderboard draft.",
            "3. Keep the remaining provider generation gap blocked until explicit approval.",
            "",
            "## Validation",
            "",
            "Run:",
            "",
            "```bash",
            "make model_run_promotion_gate_20260708",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
