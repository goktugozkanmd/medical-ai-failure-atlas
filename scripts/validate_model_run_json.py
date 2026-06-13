#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def resolve_input_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    if path.exists():
        return path.resolve()
    return (ROOT / path).resolve()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_expected_ids(prompt_path: Path) -> list[str]:
    with prompt_path.open(newline="", encoding="utf-8") as handle:
        return [row["scenario_id"] for row in csv.DictReader(handle, delimiter="\t")]


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_raw(prompt_path: Path, output_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    expected_ids = read_expected_ids(prompt_path)
    data = load_json(output_path)
    if not isinstance(data, list):
        raise SystemExit("FAIL: output JSON must be a list")
    if len(data) != len(expected_ids):
        raise SystemExit(f"FAIL: expected {len(expected_ids)} rows, found {len(data)}")

    found_ids = []
    for index, row in enumerate(data):
        if not isinstance(row, dict):
            raise SystemExit(f"FAIL: row {index} is not an object")
        if set(row) != {"scenario_id", "model_answer"}:
            raise SystemExit(f"FAIL: row {index} has unexpected keys")
        if not isinstance(row["model_answer"], str) or not row["model_answer"].strip():
            raise SystemExit(f"FAIL: row {index} has empty model_answer")
        found_ids.append(row["scenario_id"])

    if found_ids != expected_ids:
        raise SystemExit("FAIL: scenario order mismatch")

    return expected_ids, data


def validate_sidecar(prompt_path: Path, output_path: Path, sidecar_path: Path, expected_ids: list[str], data: list[dict[str, str]]) -> None:
    sidecar = load_json(sidecar_path)
    if not isinstance(sidecar, dict):
        raise SystemExit("FAIL: sidecar JSON must be an object")
    if sidecar.get("schema_version") != "open_model_run_v2":
        raise SystemExit("FAIL: sidecar schema_version must be open_model_run_v2")
    if sidecar.get("raw_output_sha256") != sha256_file(output_path):
        raise SystemExit("FAIL: sidecar raw_output_sha256 mismatch")
    if sidecar.get("prompt_tsv_sha256") != sha256_file(prompt_path):
        raise SystemExit("FAIL: sidecar prompt_tsv_sha256 mismatch")
    if sidecar.get("scenario_order") != expected_ids:
        raise SystemExit("FAIL: sidecar scenario_order mismatch")

    row_counts = sidecar.get("row_counts")
    if not isinstance(row_counts, dict):
        raise SystemExit("FAIL: sidecar row_counts missing")
    if row_counts.get("expected") != len(expected_ids):
        raise SystemExit("FAIL: sidecar expected row count mismatch")
    if row_counts.get("completed") != len(data):
        raise SystemExit("FAIL: sidecar completed row count mismatch")
    if sidecar.get("completed_scenario_ids") != expected_ids:
        raise SystemExit("FAIL: sidecar completed_scenario_ids mismatch")

    per_scenario = sidecar.get("per_scenario")
    if not isinstance(per_scenario, list) or len(per_scenario) != len(expected_ids):
        raise SystemExit("FAIL: sidecar per_scenario length mismatch")
    answer_hash_by_id = {row["scenario_id"]: sha256_text(row["model_answer"]) for row in data}
    for index, item in enumerate(per_scenario):
        if not isinstance(item, dict):
            raise SystemExit(f"FAIL: sidecar per_scenario {index} is not an object")
        scenario_id = expected_ids[index]
        if item.get("scenario_id") != scenario_id:
            raise SystemExit(f"FAIL: sidecar per_scenario order mismatch at {index}")
        if item.get("answer_sha256") != answer_hash_by_id[scenario_id]:
            raise SystemExit(f"FAIL: sidecar answer_sha256 mismatch for {scenario_id}")
        if item.get("status") not in {"completed", "resumed"}:
            raise SystemExit(f"FAIL: sidecar status is not completed for {scenario_id}")


def main() -> None:
    if len(sys.argv) not in {3, 5}:
        raise SystemExit("Usage: validate_model_run_json.py PROMPT_TSV RAW_OUTPUT_JSON [--sidecar RUN_METADATA_JSON]")
    if len(sys.argv) == 5 and sys.argv[3] != "--sidecar":
        raise SystemExit("Usage: validate_model_run_json.py PROMPT_TSV RAW_OUTPUT_JSON [--sidecar RUN_METADATA_JSON]")

    prompt_path = resolve_input_path(sys.argv[1])
    output_path = resolve_input_path(sys.argv[2])
    expected_ids, data = validate_raw(prompt_path, output_path)
    if len(sys.argv) == 5:
        sidecar_path = resolve_input_path(sys.argv[4])
        validate_sidecar(prompt_path, output_path, sidecar_path, expected_ids, data)

    print("PASS")
    print(f"Rows: {len(data)}")
    print(f"First: {expected_ids[0]}")
    print(f"Last: {expected_ids[-1]}")
    if len(sys.argv) == 5:
        print("Sidecar: PASS")


if __name__ == "__main__":
    main()
