#!/usr/bin/env python3
"""
MedFailBench → HuggingFace Dataset Publishing Pipeline

Converts model run results to HF Dataset format and uploads.

Usage:
    # Preview (dry-run)
    python3 scripts/upload_results_to_hf.py --dry-run

    # Upload (requires HF token with write access)
    HF_TOKEN=hf_xxx python3 scripts/upload_results_to_hf.py

    # Upload specific run
    HF_TOKEN=hf_xxx python3 scripts/upload_results_to_hf.py \
        --run model_runs/qwen_37max_hard30_20260707

Output:
    Dataset at https://huggingface.co/datasets/goktugozkanmd/medfailbench-v02-results
    Each model run as a separate config (e.g., qwen_37max_hard30)

Dependencies:
    pip install datasets huggingface-hub

Notes:
    - G approval required before first upload
    - README will be auto-generated on first push
    - Configs are split by model name for easy filtering
"""

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "model_runs"
PROMPTS_FILE = REPO_ROOT / "leaderboard" / "medfailbench_prompts_v0_2.jsonl"
RESULTS_DATASET = "goktugozkanmd/medfailbench-v02-results"

# Schema for HF Dataset rows
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
}


def discover_model_runs():
    """Discover all model run directories and flat JSON result files."""
    runs = []

    # Discover directories (e.g., medfailbench_weekly_preview_20260702)
    for d in sorted(DATA_DIR.iterdir()):
        if not d.is_dir():
            continue
        result_files = list(d.glob("*results*.json")) + list(d.glob("*scores*.json")) + list(d.glob("*report*.json"))
        if result_files:
            runs.append({
                "name": d.name,
                "path": d,
                "result_files": result_files,
                "source": "directory",
            })

    # Discover flat JSON files (e.g., weekly_eval_qwen-3.7-max_20260704_150000.json)
    for f in sorted(DATA_DIR.glob("weekly_eval_*.json")):
        if f.name.endswith("run_metadata.json") or f.name.endswith("summary.json"):
            continue
        # Skip files inside subdirectories (already covered above)
        if f.parent != DATA_DIR:
            continue
        stem = f.stem.replace("weekly_eval_", "").replace("_2026", "").rsplit("_", 1)[0]
        runs.append({
            "name": stem or f.stem,
            "path": f.parent,
            "result_files": [f],
            "source": "flat_file",
        })

    # Discover batch_expansion files
    for d in sorted(DATA_DIR.iterdir()):
        if not d.is_dir() or "batch" not in d.name:
            continue
        result_files = list(d.glob("*raw_outputs*.json"))
        if result_files:
            runs.append({
                "name": d.name,
                "path": d,
                "result_files": result_files,
                "source": "batch_expansion",
            })

    return sorted(runs, key=lambda x: x["name"])


def load_prompts_index():
    """Build prompt lookup dict from JSONL."""
    prompts = {}
    if not PROMPTS_FILE.exists():
        print(f"  Warning: {PROMPTS_FILE} not found, using empty index")
        return prompts
    with open(PROMPTS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                rec = json.loads(line)
                prompts[rec["id"]] = rec
    return prompts


def build_rows_from_run(run_info, prompts_index):
    """Convert a model run directory into a list of HF Dataset rows."""
    rows = []
    model_name = run_info["name"].split("_hard30")[0].split("_run")[0]

    for rf in run_info["result_files"]:
        with open(rf) as f:
            data = json.load(f)

        # Handle both list and dict containers
        items = data if isinstance(data, list) else data.get("results", data.get("items", [data]))

        for item in items:
            prompt_id = item.get("id") or item.get("scenario_id") or item.get("prompt_id", "")
            prompt_info = prompts_index.get(prompt_id, {})

            row = {
                "id": prompt_id,
                "model_name": model_name,
                "prompt": prompt_info.get("prompt", item.get("prompt_text", "")),
                "safe_answer_hint": prompt_info.get("safe_answer_hint", item.get("safe_answer_hint", "")),
                "model_response": item.get("model_answer") or item.get("response") or item.get("completion", ""),
                "language": prompt_info.get("language", item.get("language", "en")),
                "domain": prompt_info.get("domain", item.get("domain", "")),
                "safety_focus": prompt_info.get("safety_focus", item.get("safety_focus", "")),
                "risk_axis": prompt_info.get("risk_axis", item.get("risk_axis", "")),
                "category": prompt_info.get("category", item.get("category", "")),
                "safety_score": item.get("safety_score") or item.get("safety", None),
                "accuracy_score": item.get("accuracy_score") or item.get("accuracy", None),
                "source_score": item.get("source_score") or item.get("source_transparency", None),
                "refusal_score": item.get("refusal_score") or item.get("refusal_appropriateness", None),
                "clinical_grounding_score": item.get("clinical_grounding_score") or item.get("clinical_grounding", None),
                "final_label": item.get("final_label", item.get("label", None)),
                "run_timestamp": item.get("run_timestamp", item.get("timestamp", "")),
                "run_config": run_info["name"],
            }
            rows.append(row)

    return rows


def dry_run():
    """Preview what would be uploaded without actually uploading."""
    prompts = load_prompts_index()
    print(f"Prompt index: {len(prompts)} entries")

    runs = discover_model_runs()
    print(f"\nDiscovered {len(runs)} model run directories:\n")

    for run in runs:
        rows = build_rows_from_run(run, prompts)
        print(f"  {run['name']}: {len(rows)} rows")
        result_shown = False
        for rf in run["result_files"]:
            size = rf.stat().st_size
            print(f"    {rf.name} ({size:,} bytes)")
            result_shown = True
        if rows:
            print(f"    Sample keys: {list(rows[0].keys())[:6]}...")
            print(f"    First row: {rows[0]['id']} | {rows[0]['domain']} | score={rows[0].get('safety_score')}")
        print()

    total = sum(len(build_rows_from_run(r, prompts)) for r in runs)
    print(f"\nTotal: {total} rows across {len(runs)} model configs")
    print(f"Target dataset: {RESULTS_DATASET}")
    print("Run with HF_TOKEN set to actually publish.")


def upload():
    """Upload all model runs to HF Datasets."""
    try:
        from datasets import Dataset, DatasetDict, concatenate_datasets, Features, Value, ClassLabel
        import huggingface_hub
    except ImportError:
        print("Error: Install datasets and huggingface-hub: pip install datasets huggingface-hub")
        sys.exit(1)

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("Error: HF_TOKEN environment variable not set")
        sys.exit(1)

    prompts = load_prompts_index()
    runs = discover_model_runs()

    configs = {}
    for run in runs:
        rows = build_rows_from_run(run, prompts)
        if rows:
            config_name = run["name"].replace("_hard30", "").replace("_run", "").replace("_", "-")
            ds = Dataset.from_list(rows)
            configs[config_name] = ds
            print(f"  {config_name}: {len(ds)} rows")

    if not configs:
        print("No data to upload")
        sys.exit(1)

    # Build DatasetDict
    dd = DatasetDict(configs)

    # Push to hub
    print(f"\nPushing to {RESULTS_DATASET}...")
    dd.push_to_hub(RESULTS_DATASET, token=token, private=False)
    print(f"Done! https://huggingface.co/datasets/{RESULTS_DATASET}")


if __name__ == "__main__":
    if "--dry-run" in sys.argv or not os.environ.get("HF_TOKEN"):
        dry_run()
    else:
        upload()
