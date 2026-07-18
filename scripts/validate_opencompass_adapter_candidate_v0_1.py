#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "adapters" / "opencompass" / "medfailbench_safety_layer_docs_v0_1.jsonl"
MANIFEST_PATH = ROOT / "adapters" / "opencompass" / "medfailbench_safety_layer_manifest_v0_1.json"
README_PATH = ROOT / "adapters" / "opencompass" / "README.md"
EXPECTED_SCHEMA = "medfailbench_opencompass_adapter_candidate_v0_1"
FORBIDDEN_TEXT = (
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "model ranking",
    "officially compatible",
    "opencompass accepted",
    "regulatory approval",
    "patient data used",
)


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing JSON file: {path.relative_to(ROOT)}")
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return {}
    return payload


def read_jsonl(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    if not path.is_file():
        errors.append(f"missing JSONL file: {path.relative_to(ROOT)}")
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: invalid JSON: {exc}")
                continue
            if not isinstance(row, dict):
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: row must be an object")
                continue
            rows.append(row)
    return rows


def validate_manifest(manifest: dict[str, Any], errors: list[str]) -> None:
    expected_flags = {
        "schema_version": EXPECTED_SCHEMA,
        "status": "local_candidate_not_submitted",
        "synthetic_only": True,
        "contains_patient_data": False,
        "external_submission_allowed": False,
        "no_clinical_validation_claim": True,
        "no_model_ranking_claim": True,
        "no_official_compatibility_or_endorsement_claim": True,
        "row_count": 44,
        "language": "tr",
    }
    for key, expected in expected_flags.items():
        if manifest.get(key) != expected:
            errors.append(f"manifest {key} must be {expected!r}")
    for key in ("source_sha256", "export_sha256"):
        value = manifest.get(key)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            errors.append(f"manifest {key} must be a lowercase sha256")
    docs = manifest.get("opencompass_docs_checked")
    if not isinstance(docs, list) or len(docs) < 3:
        errors.append("manifest must record OpenCompass docs checked")


def validate_rows(rows: list[dict[str, Any]], errors: list[str]) -> None:
    if len(rows) != 44:
        errors.append(f"OpenCompass candidate dataset must contain 44 rows, found {len(rows)}")
    seen_ids: set[str] = set()
    for index, row in enumerate(rows, start=1):
        row_id = row.get("id")
        if not isinstance(row_id, str) or not row_id.startswith("TRFAI"):
            errors.append(f"row {index} id must be a TRFAI string")
        elif row_id in seen_ids:
            errors.append(f"duplicate row id: {row_id}")
        else:
            seen_ids.add(row_id)
        for field in ("question", "target", "language", "clinical_domain", "risk_axis", "metadata"):
            if field not in row:
                errors.append(f"row {index} missing field: {field}")
        if row.get("language") != "tr":
            errors.append(f"row {index} language must be tr")
        metadata = row.get("metadata")
        if not isinstance(metadata, dict):
            errors.append(f"row {index} metadata must be an object")
            continue
        expected_metadata = {
            "synthetic_only": True,
            "contains_patient_data": False,
            "not_for_clinical_use": True,
            "no_clinical_validation_claim": True,
            "no_model_ranking_claim": True,
            "no_official_compatibility_or_endorsement_claim": True,
            "release_gate": "approved",
        }
        for key, expected in expected_metadata.items():
            if metadata.get(key) != expected:
                errors.append(f"row {index} metadata.{key} must be {expected!r}")
        if not isinstance(row.get("target"), str) or len(row["target"].strip()) < 40:
            errors.append(f"row {index} target must contain a substantial safe answer expectation")


def validate_text_boundaries(errors: list[str]) -> None:
    for path in (README_PATH, MANIFEST_PATH):
        if not path.is_file():
            errors.append(f"missing text boundary file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_TEXT:
            if phrase in text:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden phrase: {phrase}")


def main() -> int:
    errors: list[str] = []
    manifest = read_json(MANIFEST_PATH, errors)
    rows = read_jsonl(DATASET_PATH, errors)
    if manifest:
        validate_manifest(manifest, errors)
    validate_rows(rows, errors)
    validate_text_boundaries(errors)
    if errors:
        print("FAIL OpenCompass adapter candidate validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS OpenCompass adapter candidate validation")
    print(f"rows={len(rows)}")
    print("status=local_candidate_not_submitted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
