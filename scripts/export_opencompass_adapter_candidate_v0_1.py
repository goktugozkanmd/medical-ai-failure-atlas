#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SOURCE_DATASET = ROOT / "data" / "tr_medllm_synthetic_eval_set_v0_3.jsonl"
EXPORT_DATASET = (
    ROOT
    / "adapters"
    / "opencompass"
    / "medfailbench_safety_layer_docs_v0_1.jsonl"
)
MANIFEST_PATH = (
    ROOT
    / "adapters"
    / "opencompass"
    / "medfailbench_safety_layer_manifest_v0_1.json"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _metadata(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_dataset": "data/tr_medllm_synthetic_eval_set_v0_3.jsonl",
        "source_case_id": row["case_id"],
        "language": row.get("language", "tr"),
        "clinical_domain": row.get("clinical_domain", "unknown"),
        "taxonomy_domain_id": row.get("taxonomy_domain_id"),
        "setting": row.get("setting"),
        "taxonomy_setting_id": row.get("taxonomy_setting_id"),
        "failure_pattern": row.get("failure_pattern"),
        "taxonomy_pattern_ids": row.get("taxonomy_pattern_ids", []),
        "risk_axis": row.get("risk_axis"),
        "safety_gate": row.get("safety_gate"),
        "severity_1_to_5": row.get("severity_1_to_5"),
        "release_gate": row.get("release_gate"),
        "review_status": row.get("review_status"),
        "synthetic_only": True,
        "contains_patient_data": False,
        "not_for_clinical_use": True,
        "no_clinical_validation_claim": True,
        "no_model_ranking_claim": True,
        "no_official_compatibility_or_endorsement_claim": True,
    }


def opencompass_record(row: dict[str, Any]) -> dict[str, Any]:
    prompt = row.get("turkish_prompt_seed") or row.get("prompt")
    target = row.get("safe_answer_expectation")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError(f"{row.get('case_id', 'unknown')}: missing prompt")
    if not isinstance(target, str) or not target.strip():
        raise ValueError(f"{row.get('case_id', 'unknown')}: missing safe answer expectation")

    return {
        "id": row["case_id"],
        "question": prompt,
        "target": target,
        "language": row.get("language", "tr"),
        "clinical_domain": row.get("clinical_domain", "unknown"),
        "risk_axis": row.get("risk_axis", "unknown"),
        "safety_gate": row.get("safety_gate"),
        "severity_1_to_5": row.get("severity_1_to_5"),
        "metadata": _metadata(row),
    }


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")
            count += 1
    return count


def build_manifest(row_count: int) -> dict[str, Any]:
    return {
        "schema_version": "medfailbench_opencompass_adapter_candidate_v0_1",
        "status": "local_candidate_not_submitted",
        "source_dataset": "data/tr_medllm_synthetic_eval_set_v0_3.jsonl",
        "source_sha256": _sha256(SOURCE_DATASET),
        "export_dataset": "adapters/opencompass/medfailbench_safety_layer_docs_v0_1.jsonl",
        "export_sha256": _sha256(EXPORT_DATASET),
        "row_count": row_count,
        "language": "tr",
        "synthetic_only": True,
        "contains_patient_data": False,
        "external_submission_allowed": False,
        "no_clinical_validation_claim": True,
        "no_model_ranking_claim": True,
        "no_official_compatibility_or_endorsement_claim": True,
        "opencompass_issue": "https://github.com/open-compass/opencompass/issues/2516",
        "opencompass_docs_checked": [
            "docs/en/advanced_guides/new_dataset.md",
            "docs/en/user_guides/datasets.md",
            "docs/en/notes/contribution_guide.md",
        ],
        "candidate_upstream_files": [
            "opencompass/datasets/medfailbench.py",
            "opencompass/configs/datasets/MedFailBench/medfailbench_gen.py",
            "opencompass/utils/datasets_info.py",
            "dataset-index.yml",
        ],
    }


def export() -> dict[str, Any]:
    from failure_atlas.data import load_eval_set

    cases = load_eval_set(SOURCE_DATASET)
    records = [opencompass_record(case.raw) for case in cases]
    count = write_jsonl(EXPORT_DATASET, records)
    if count != 44:
        raise ValueError(f"Expected 44 OpenCompass candidate rows, wrote {count}")
    manifest = build_manifest(row_count=count)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export a bounded OpenCompass candidate dataset from MedFailBench."
    )
    parser.parse_args()
    manifest = export()
    print("PASS OpenCompass adapter candidate export")
    print(f"rows={manifest['row_count']}")
    print(f"dataset={manifest['export_dataset']}")
    print(f"manifest={MANIFEST_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
