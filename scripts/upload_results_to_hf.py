#!/usr/bin/env python3
"""
MedFailBench → HuggingFace Dataset Publishing Pipeline

Converts full model run outputs/scores to HF Dataset format and uploads.

Usage:
    python3 scripts/upload_results_to_hf.py --dry-run
    HF_TOKEN=hf_xxx python3 scripts/upload_results_to_hf.py

Output:
    Dataset at https://huggingface.co/datasets/goktugozkanmd/medfailbench-v02-results
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "model_runs"
PROMPTS_FILE = REPO_ROOT / "leaderboard" / "medfailbench_prompts_v0_2.jsonl"
HARD30_PROMPTS_FILE = REPO_ROOT / "data" / "prompt_set_v2_hard_30.tsv"
PREVIEW_PROMPTS_FILE = (
    REPO_ROOT
    / "model_runs"
    / "medfailbench_weekly_preview_20260702"
    / "prompt_set_v2_hard_5_preview.tsv"
)
SCENARIO_BANK_FILE = REPO_ROOT / "data" / "scenario_bank_v2_hard_addendum.tsv"
RESULTS_DATASET = "goktugozkanmd/medfailbench-v02-results"

ROW_FIELDS = {
    "id": str,
    "model_name": str,
    "prompt": str,
    "safe_answer_hint": str,
    "model_response": str,
    "language": str,
    "domain": str,
    "safety_focus": str,
    "risk_axis": str,
    "category": str,
    "safety_score": (int, float, type(None)),
    "accuracy_score": (int, float, type(None)),
    "source_score": (int, float, type(None)),
    "refusal_score": (int, float, type(None)),
    "clinical_grounding_score": (int, float, type(None)),
    "final_label": (str, type(None)),
    "run_timestamp": str,
    "run_config": str,
    "source_file": str,
}

SKIP_NAME_PARTS = ("summary", ".run_metadata", "metadata")


def discover_model_runs() -> list[dict[str, Any]]:
    runs, _skipped = discover_model_runs_with_skips()
    return runs


def discover_model_runs_with_skips() -> tuple[list[dict[str, Any]], list[str]]:
    runs: list[dict[str, Any]] = []
    skipped: list[str] = []
    if not DATA_DIR.exists():
        return runs, skipped

    candidates: list[Path] = []
    candidates.extend(DATA_DIR.glob("weekly_eval_*.json"))
    candidates.extend(DATA_DIR.glob("*/*raw_outputs.json"))
    candidates.extend(DATA_DIR.glob("*/*rule_scores.json"))
    candidates.extend(DATA_DIR.glob("*/*scores.json"))
    candidates.extend(DATA_DIR.glob("*/*report.json"))

    seen: set[Path] = set()
    for path in sorted(candidates):
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        if should_skip_file(path):
            continue
        if block_reason := weekly_eval_publish_block_reason(path):
            skipped.append(f"{path.name}: {block_reason}")
            continue
        runs.append(
            {
                "name": infer_run_name(path),
                "model_name": infer_model_name(path),
                "result_file": path,
                "source": "file",
            }
        )
    return sorted(runs, key=lambda x: (x["name"], str(x["result_file"]))), skipped


def should_skip_file(path: Path) -> bool:
    lower = path.name.lower()
    if any(part in lower for part in SKIP_NAME_PARTS):
        return True
    if lower.endswith("_raw_outputs.json"):
        scored_sibling = path.with_name(
            path.name.replace("_raw_outputs.json", "_rule_scores.json")
        )
        if scored_sibling.exists():
            return True
    return False


def weekly_eval_publish_block_reason(path: Path) -> str | None:
    if not path.name.startswith("weekly_eval_"):
        return None

    sidecar_path = path.with_suffix(".run_metadata.json")
    if not sidecar_path.exists():
        return "missing run metadata sidecar"
    if not HARD30_PROMPTS_FILE.exists():
        return f"missing prompt file {HARD30_PROMPTS_FILE.relative_to(REPO_ROOT)}"

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"invalid JSON: {exc.msg}"

    if not isinstance(data, list):
        return "weekly eval output must be a raw list"
    if not isinstance(sidecar, dict):
        return "run metadata sidecar must be an object"

    expected_ids = read_hard30_prompt_ids()
    if len(data) != len(expected_ids):
        return f"row count {len(data)} != expected {len(expected_ids)}"
    found_ids = [
        row.get("scenario_id") if isinstance(row, dict) else None for row in data
    ]
    if found_ids != expected_ids:
        return "scenario order mismatch"

    if sidecar.get("schema_version") != "open_model_run_v2":
        return f"schema_version={sidecar.get('schema_version')}"
    if sidecar.get("completion_status") != "completed":
        return f"completion_status={sidecar.get('completion_status')}"
    if sidecar.get("prompt_tsv_sha256") != sha256_file(HARD30_PROMPTS_FILE):
        return "prompt_tsv_sha256 mismatch"
    if sidecar.get("raw_output_sha256") != sha256_file(path):
        return "raw_output_sha256 mismatch"
    if sidecar.get("scenario_order") != expected_ids:
        return "sidecar scenario_order mismatch"
    if sidecar.get("completed_scenario_ids") != expected_ids:
        return "sidecar completed_scenario_ids mismatch"

    row_counts = sidecar.get("row_counts")
    if not isinstance(row_counts, dict):
        return "sidecar row_counts missing"
    if row_counts.get("expected") != len(expected_ids):
        return f"row_counts.expected={row_counts.get('expected')}"
    if row_counts.get("completed") != len(expected_ids):
        return f"row_counts.completed={row_counts.get('completed')}"

    per_scenario = sidecar.get("per_scenario")
    if not isinstance(per_scenario, list) or len(per_scenario) != len(expected_ids):
        return "sidecar per_scenario length mismatch"
    answer_hash_by_id = {
        row["scenario_id"]: sha256_text(str(row.get("model_answer", "")))
        for row in data
        if isinstance(row, dict)
    }
    for index, item in enumerate(per_scenario):
        if not isinstance(item, dict):
            return f"sidecar per_scenario {index} is not an object"
        scenario_id = expected_ids[index]
        if item.get("scenario_id") != scenario_id:
            return f"sidecar per_scenario order mismatch at {index}"
        if item.get("status") not in {"completed", "resumed"}:
            return f"sidecar status={item.get('status')} for {scenario_id}"
        if item.get("answer_sha256") != answer_hash_by_id.get(scenario_id):
            return f"sidecar answer_sha256 mismatch for {scenario_id}"

    return None


def read_hard30_prompt_ids() -> list[str]:
    with HARD30_PROMPTS_FILE.open(newline="", encoding="utf-8") as handle:
        return [row["scenario_id"] for row in csv.DictReader(handle, delimiter="\t")]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def infer_run_name(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"^weekly_eval_", "", stem)
    stem = re.sub(r"_\d{8}_\d{6}$", "", stem)
    stem = re.sub(r"_hard30_raw_outputs$", "", stem)
    stem = re.sub(r"_raw_outputs$", "", stem)
    stem = re.sub(r"_rule_scores$", "", stem)
    stem = re.sub(r"_scores$", "", stem)
    return slug(stem)


def infer_model_name(path: Path) -> str:
    name = infer_run_name(path)
    return (
        name.replace("_", "/", 1)
        if name.startswith(("qwen_", "deepseek_", "meta_"))
        else name.replace("_", "-")
    )


def slug(value: str) -> str:
    value = value.strip().replace("/", "_")
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("._-")
    return value or "run"


def load_prompts_index() -> dict[str, dict[str, Any]]:
    prompts: dict[str, dict[str, Any]] = {}

    if PROMPTS_FILE.exists():
        with open(PROMPTS_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                prompt_id = (
                    rec.get("id") or rec.get("scenario_id") or rec.get("prompt_id")
                )
                if prompt_id:
                    prompts[str(prompt_id)] = rec
    else:
        print(f"  Warning: {PROMPTS_FILE} not found")

    for path in (HARD30_PROMPTS_FILE, PREVIEW_PROMPTS_FILE):
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                prompt_id = row.get("scenario_id") or row.get("id")
                if not prompt_id:
                    continue
                prompts.setdefault(
                    prompt_id,
                    {
                        "id": prompt_id,
                        "prompt": row.get("prompt_text", ""),
                        "language": "en",
                        "domain": "",
                        "safety_focus": "",
                        "risk_axis": "",
                        "safe_answer_hint": row.get("output_capture_instruction", ""),
                        "category": "hard30",
                    },
                )

    if SCENARIO_BANK_FILE.exists():
        with SCENARIO_BANK_FILE.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                prompt_id = row.get("scenario_id")
                if not prompt_id or prompt_id not in prompts:
                    continue
                prompts[prompt_id].update(
                    {
                        "domain": row.get(
                            "domain", prompts[prompt_id].get("domain", "")
                        ),
                        "safety_focus": row.get(
                            "expected_safety_focus",
                            prompts[prompt_id].get("safety_focus", ""),
                        ),
                        "risk_axis": row.get(
                            "theme", prompts[prompt_id].get("risk_axis", "")
                        ),
                    }
                )

    return prompts


def build_rows_from_run(
    run_info: dict[str, Any], prompts_index: dict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[str]]:
    path = Path(run_info["result_file"])
    data = json.loads(path.read_text(encoding="utf-8"))
    items, metadata = extract_items(data)
    rows: list[dict[str, Any]] = []
    skipped: list[str] = []

    model_name = (
        metadata.get("model_name") or metadata.get("model") or run_info["model_name"]
    )
    run_timestamp = str(metadata.get("scored_at") or metadata.get("timestamp") or "")

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            skipped.append(f"{path.name}#{index}: item is not an object")
            continue

        prompt_id = first_str(item, "id", "scenario_id", "prompt_id")
        prompt_info = prompts_index.get(prompt_id, {})
        scores_raw = item.get("scores")
        scores: dict[str, Any] = scores_raw if isinstance(scores_raw, dict) else {}
        response = first_str(item, "model_answer", "response", "completion")
        prompt = prompt_info.get("prompt") or first_str(item, "prompt_text", "prompt")

        row = {
            "id": prompt_id,
            "model_name": str(
                item.get("model_name") or item.get("model") or model_name
            ),
            "prompt": str(prompt or ""),
            "safe_answer_hint": str(
                prompt_info.get("safe_answer_hint")
                or item.get("safe_answer_hint")
                or ""
            ),
            "model_response": str(response or ""),
            "language": str(prompt_info.get("language") or item.get("language") or ""),
            "domain": str(prompt_info.get("domain") or item.get("domain") or ""),
            "safety_focus": str(
                prompt_info.get("safety_focus") or item.get("safety_focus") or ""
            ),
            "risk_axis": str(
                prompt_info.get("risk_axis") or item.get("risk_axis") or ""
            ),
            "category": str(prompt_info.get("category") or item.get("category") or ""),
            "safety_score": first_score(item, scores, "safety_score", "safety"),
            "accuracy_score": first_score(item, scores, "accuracy_score", "accuracy"),
            "source_score": first_score(
                item, scores, "source_score", "source_transparency", "source_support"
            ),
            "refusal_score": first_score(
                item, scores, "refusal_score", "refusal_appropriateness", "refusal"
            ),
            "clinical_grounding_score": first_score(
                item, scores, "clinical_grounding_score", "clinical_grounding"
            ),
            "final_label": item.get("final_label") or item.get("label"),
            "run_timestamp": str(
                item.get("run_timestamp") or item.get("timestamp") or run_timestamp
            ),
            "run_config": run_info["name"],
            "source_file": str(path.relative_to(REPO_ROOT)),
        }

        error = validate_row(row)
        if error:
            skipped.append(f"{path.name}#{index}: {error}")
            continue
        rows.append(row)

    return rows, skipped


def extract_items(data: Any) -> tuple[list[Any], dict[str, Any]]:
    if isinstance(data, list):
        return data, {}
    if not isinstance(data, dict):
        return [], {}
    if isinstance(data.get("items"), list):
        return data["items"], data
    if isinstance(data.get("results"), list):
        return data["results"], data
    return [], data


def first_str(item: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def first_score(
    item: dict[str, Any], scores: dict[str, Any], *keys: str
) -> int | float | None:
    for key in keys:
        value = item.get(key)
        if isinstance(value, (int, float)):
            return value
        value = scores.get(key)
        if isinstance(value, (int, float)):
            return value
    return None


def validate_row(row: dict[str, Any]) -> str | None:
    for key, expected in ROW_FIELDS.items():
        value = row.get(key)
        if not isinstance(value, expected):
            return f"{key} has invalid type {type(value).__name__}"
    if not row["id"]:
        return "empty id"
    if not row["prompt"]:
        return "empty prompt"
    if not row["model_response"]:
        return "empty model_response"
    return None


def collect_rows() -> tuple[list[dict[str, Any]], list[str], list[dict[str, Any]]]:
    prompts = load_prompts_index()
    runs, discovery_skips = discover_model_runs_with_skips()
    all_rows: list[dict[str, Any]] = []
    all_skipped: list[str] = list(discovery_skips)
    run_summaries: list[dict[str, Any]] = []

    for run in runs:
        rows, skipped = build_rows_from_run(run, prompts)
        all_rows.extend(rows)
        all_skipped.extend(skipped)
        run_summaries.append({**run, "rows": len(rows), "skipped": len(skipped)})

    return all_rows, all_skipped, run_summaries


def dry_run() -> None:
    prompts = load_prompts_index()
    print(f"Prompt index: {len(prompts)} entries")
    rows, skipped, runs = collect_rows()
    print(f"\nDiscovered {len(runs)} publishable run files:\n")
    for run in runs:
        path = Path(run["result_file"])
        print(
            f"  {run['name']}: {run['rows']} rows, {run['skipped']} skipped — {path.relative_to(REPO_ROOT)}"
        )
    print(f"\nTotal valid rows: {len(rows)}")
    print(f"Skipped rows: {len(skipped)}")
    for item in skipped[:20]:
        print(f"  skipped: {item}")
    if len(skipped) > 20:
        print(f"  ... {len(skipped) - 20} more skipped")
    print(f"Target dataset: {RESULTS_DATASET}")
    if rows:
        first = rows[0]
        print(
            f"First row: {first['id']} | {first['model_name']} | {len(first['model_response'])} chars"
        )
    print("Run with HF_TOKEN set to actually publish.")


def upload() -> None:
    try:
        from datasets import Dataset
    except ImportError:
        print(
            "Error: Install datasets and huggingface-hub: python3 -m pip install datasets huggingface-hub"
        )
        sys.exit(1)

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("Error: HF_TOKEN environment variable not set")
        sys.exit(1)

    rows, skipped, _runs = collect_rows()
    if not rows:
        print("No valid data to upload")
        sys.exit(1)

    print(f"Valid rows: {len(rows)}")
    print(f"Skipped rows: {len(skipped)}")
    dataset = Dataset.from_list(rows)
    print(f"\nPushing to {RESULTS_DATASET}...")
    dataset.push_to_hub(RESULTS_DATASET, token=token, private=False)
    print(f"Done! https://huggingface.co/datasets/{RESULTS_DATASET}")


if __name__ == "__main__":
    if "--dry-run" in sys.argv or not os.environ.get("HF_TOKEN"):
        dry_run()
    else:
        upload()
