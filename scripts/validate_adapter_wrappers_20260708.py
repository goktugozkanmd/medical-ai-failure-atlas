#!/usr/bin/env python3
from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

REQUIRED_FILES = [
    "adapters/__init__.py",
    "adapters/inspect_evals/__init__.py",
    "adapters/inspect_evals/README.md",
    "adapters/inspect_evals/medfailbench_safety_layer_v0_1.py",
    "adapters/inspect_evals/medfailbench_safety_layer_dataset_v0_1.jsonl",
    "adapters/inspect_evals/register/medfailbench_safety_layer_v0_1.json",
    "adapters/lm_eval/__init__.py",
    "adapters/lm_eval/README.md",
    "adapters/lm_eval/medfailbench_safety_layer_docs_v0_1.jsonl",
    "adapters/lm_eval/medfailbench_safety_layer_metrics.py",
    "adapters/lm_eval/medfailbench_safety_layer_v0_1.yaml",
    "docs/MEDFAILBENCH_LOCAL_ADAPTER_WRAPPERS_20260708.md",
    "docs/MEDFAILBENCH_ADAPTER_FRAMEWORK_SMOKE_20260708.md",
    "docs/medfailbench_adapter_framework_smoke_20260708.json",
    "docs/medfailbench_local_adapter_wrappers_20260708.json",
    "scripts/smoke_adapter_frameworks_20260708.py",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "regulatory compliance achieved",
    "accepted by inspect evals",
    "accepted by lm evaluation harness",
    "patient data used",
]


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).exists():
            errors.append(f"Missing required file: {relative}")

    inspect_rows = read_jsonl(ROOT / "adapters" / "inspect_evals" / "medfailbench_safety_layer_dataset_v0_1.jsonl", errors)
    lm_rows = read_jsonl(ROOT / "adapters" / "lm_eval" / "medfailbench_safety_layer_docs_v0_1.jsonl", errors)
    validate_rows("Inspect", inspect_rows, ("id", "input", "target", "metadata"), errors)
    validate_rows("LM Eval", lm_rows, ("id", "question", "target", "metadata"), errors)

    manifest = read_json(ROOT / "docs" / "medfailbench_local_adapter_wrappers_20260708.json", errors)
    if manifest:
        expected_flags = {
            "synthetic_only": True,
            "contains_patient_data": False,
            "external_submission_allowed": False,
            "no_clinical_validation_claim": True,
            "no_model_ranking": True,
            "no_registry_acceptance_claim": True,
        }
        for key, expected in expected_flags.items():
            if manifest.get(key) is not expected:
                errors.append(f"Manifest {key} must be {expected!r}")
        if manifest.get("inspect_rows") != 20 or manifest.get("lm_eval_rows") != 20:
            errors.append("Manifest row counts must be 20 and 20")

    register = read_json(
        ROOT / "adapters" / "inspect_evals" / "register" / "medfailbench_safety_layer_v0_1.json",
        errors,
    )
    if register:
        if register.get("external_submission_allowed") is not False:
            errors.append("Inspect register external_submission_allowed must be false")
        if register.get("contains_patient_data") is not False:
            errors.append("Inspect register contains_patient_data must be false")
        if "medfailbench_safety_layer_v0_1.py" not in str(register.get("implementation_entrypoint", "")):
            errors.append("Inspect register must point to the local task wrapper")

    smoke = read_json(ROOT / "docs" / "medfailbench_adapter_framework_smoke_20260708.json", errors)
    if smoke:
        expected_smoke_flags = {
            "synthetic_only": True,
            "contains_patient_data": False,
            "external_submission_allowed": False,
            "inspect_task_build_passed": True,
            "lm_eval_validate_passed": True,
            "lm_eval_dummy_run_passed": True,
        }
        for key, expected in expected_smoke_flags.items():
            if smoke.get(key) is not expected:
                errors.append(f"Framework smoke {key} must be {expected!r}")
        if smoke.get("inspect_sample_count") != 20:
            errors.append("Framework smoke inspect_sample_count must be 20")
        if smoke.get("lm_eval_sample_len") != 1:
            errors.append("Framework smoke lm_eval_sample_len must be 1")

    validate_inspect_task(errors)
    validate_lm_eval_yaml(errors)
    validate_metrics(errors)
    validate_text_boundaries(errors)

    if errors:
        print("FAIL adapter wrapper validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS adapter wrapper validation")
    print(f"inspect_rows={len(inspect_rows)}")
    print(f"lm_eval_rows={len(lm_rows)}")
    print("metric_schema=medfailbench_composite")
    return 0


def read_json(path: Path, errors: list[str]) -> dict:
    if not path.exists():
        errors.append(f"Missing JSON file: {path.relative_to(ROOT)}")
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


def read_jsonl(path: Path, errors: list[str]) -> list[dict]:
    if not path.exists():
        errors.append(f"Missing JSONL file: {path.relative_to(ROOT)}")
        return []
    rows: list[dict] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                payload = json.loads(line)
                if not isinstance(payload, dict):
                    errors.append(f"{path.relative_to(ROOT)} line {line_number} must be an object")
                    continue
                rows.append(payload)
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSONL {path.relative_to(ROOT)}: {exc}")
    return rows


def validate_rows(label: str, rows: list[dict], required_fields: tuple[str, ...], errors: list[str]) -> None:
    if len(rows) != 20:
        errors.append(f"{label} dataset must contain 20 rows")
    for index, row in enumerate(rows, start=1):
        for field in required_fields:
            if field not in row:
                errors.append(f"{label} row {index} missing field: {field}")
        metadata = row.get("metadata", {})
        if not isinstance(metadata, dict):
            errors.append(f"{label} row {index} metadata must be an object")
            continue
        if metadata.get("synthetic_only") is not True:
            errors.append(f"{label} row {index} synthetic_only must be true")
        if metadata.get("contains_patient_data") is not False:
            errors.append(f"{label} row {index} contains_patient_data must be false")


def validate_inspect_task(errors: list[str]) -> None:
    path = ROOT / "adapters" / "inspect_evals" / "medfailbench_safety_layer_v0_1.py"
    if not path.exists():
        return
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        errors.append(f"Inspect task has syntax error: {exc}")
        return
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    for required in {"load_records", "build_samples", "medfailbench_safety_scorer", "medfailbench_safety_layer", "local_record_count"}:
        if required not in names:
            errors.append(f"Inspect task missing function: {required}")
    text = path.read_text(encoding="utf-8")
    for snippet in ("Task(", "generate()", "medfailbench_safety_scorer()", "synthetic_only", "process_results"):
        if snippet not in text:
            errors.append(f"Inspect task missing snippet: {snippet}")


def validate_lm_eval_yaml(errors: list[str]) -> None:
    path = ROOT / "adapters" / "lm_eval" / "medfailbench_safety_layer_v0_1.yaml"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    required_snippets = [
        "dataset_path: json",
        "medfailbench_safety_layer_docs_v0_1.jsonl",
        "process_results: !function medfailbench_safety_layer_metrics.process_results",
        "medfailbench_composite",
        "external_submission_allowed: false",
    ]
    for snippet in required_snippets:
        if snippet not in text:
            errors.append(f"LM Eval YAML missing snippet: {snippet}")


def validate_metrics(errors: list[str]) -> None:
    path = ROOT / "adapters" / "lm_eval" / "medfailbench_safety_layer_metrics.py"
    if not path.exists():
        return
    spec = importlib.util.spec_from_file_location("medfailbench_metrics", path)
    if spec is None or spec.loader is None:
        errors.append("Could not load metrics module spec")
        return
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.process_results(
        {"risk_axis": "medication_safety"},
        ["Do not change the dose remotely. Seek urgent clinician review now."],
    )
    expected = {
        "medfailbench_safety_presence",
        "medfailbench_source_boundary",
        "medfailbench_no_remote_dosing",
        "medfailbench_composite",
    }
    if set(result) != expected:
        errors.append("Metrics result keys do not match expected schema")
    if result.get("medfailbench_composite") != 1.0:
        errors.append("Metrics safe smoke answer should score composite 1.0")


def validate_text_boundaries(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.exists() or path.suffix.lower() not in {".md", ".json", ".yaml", ".py"}:
            continue
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        if "/users/goktugozkan" in lowered:
            errors.append(f"Local user path present in {relative}")
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {relative}: {phrase}")


if __name__ == "__main__":
    sys.exit(main())
