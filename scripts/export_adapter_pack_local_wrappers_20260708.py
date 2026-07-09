#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DATASET = ROOT / "safetyguard" / "data" / "medfailbench_prompts_v0_2.jsonl"
INSPECT_DATASET = ROOT / "adapters" / "inspect_evals" / "medfailbench_safety_layer_dataset_v0_1.jsonl"
LM_EVAL_DATASET = ROOT / "adapters" / "lm_eval" / "medfailbench_safety_layer_docs_v0_1.jsonl"
MANIFEST_PATH = ROOT / "docs" / "medfailbench_local_adapter_wrappers_20260708.json"


def load_source_rows(limit: int) -> list[dict]:
    rows: list[dict] = []
    with SOURCE_DATASET.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError("Source JSONL row must be an object")
            rows.append(row)
            if len(rows) >= limit:
                break
    return rows


def common_metadata(row: dict) -> dict:
    return {
        "source_id": row["id"],
        "language": row.get("language", "unknown"),
        "domain": row.get("domain", "unknown"),
        "safety_focus": row.get("safety_focus", "unknown"),
        "risk_axis": row.get("risk_axis", "unknown"),
        "category": row.get("category", "unknown"),
        "synthetic_only": True,
        "contains_patient_data": False,
        "not_for_clinical_use": True,
        "source_dataset": "safetyguard/data/medfailbench_prompts_v0_2.jsonl",
    }


def inspect_record(row: dict) -> dict:
    return {
        "id": row["id"],
        "input": row["prompt"],
        "target": row["safe_answer_hint"],
        "metadata": common_metadata(row),
    }


def lm_eval_record(row: dict) -> dict:
    metadata = common_metadata(row)
    return {
        "id": row["id"],
        "question": row["prompt"],
        "target": row["safe_answer_hint"],
        "language": metadata["language"],
        "domain": metadata["domain"],
        "risk_axis": metadata["risk_axis"],
        "metadata": metadata,
    }


def write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")
            count += 1
    return count


def build_manifest(limit: int, inspect_count: int, lm_eval_count: int) -> dict:
    return {
        "artifact_id": "medfailbench_local_adapter_wrappers_20260708",
        "status": "local_wrapper_package",
        "source_dataset": "safetyguard/data/medfailbench_prompts_v0_2.jsonl",
        "source_limit": limit,
        "inspect_dataset": "adapters/inspect_evals/medfailbench_safety_layer_dataset_v0_1.jsonl",
        "inspect_rows": inspect_count,
        "lm_eval_dataset": "adapters/lm_eval/medfailbench_safety_layer_docs_v0_1.jsonl",
        "lm_eval_rows": lm_eval_count,
        "synthetic_only": True,
        "contains_patient_data": False,
        "external_submission_allowed": False,
        "no_clinical_validation_claim": True,
        "no_model_ranking": True,
        "no_registry_acceptance_claim": True,
    }


def write_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def export(limit: int) -> dict:
    rows = load_source_rows(limit=limit)
    if len(rows) != limit:
        raise ValueError(f"Expected {limit} source rows, found {len(rows)}")
    inspect_count = write_jsonl(INSPECT_DATASET, (inspect_record(row) for row in rows))
    lm_eval_count = write_jsonl(LM_EVAL_DATASET, (lm_eval_record(row) for row in rows))
    manifest = build_manifest(limit=limit, inspect_count=inspect_count, lm_eval_count=lm_eval_count)
    write_manifest(MANIFEST_PATH, manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Export local MedFailBench adapter wrapper datasets.")
    parser.add_argument("--limit", type=int, default=20, help="Number of source rows to export")
    args = parser.parse_args()
    manifest = export(limit=args.limit)
    print("PASS local adapter wrapper export")
    print(f"inspect_rows={manifest['inspect_rows']}")
    print(f"lm_eval_rows={manifest['lm_eval_rows']}")
    print(f"manifest={MANIFEST_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
