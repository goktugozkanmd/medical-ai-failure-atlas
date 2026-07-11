#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

TASK_NAME = "medfailbench_safety_layer_v0_1"
LM_EVAL_INCLUDE_PATH = "adapters/lm_eval"


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test MedFailBench adapters with real framework imports.")
    parser.add_argument("--skip-missing", action="store_true", help="Return success if optional framework deps are missing")
    parser.add_argument("--write-result", type=Path, help="Optional JSON result path")
    args = parser.parse_args()

    result: dict[str, Any] = {
        "artifact_id": "medfailbench_adapter_framework_smoke_20260708",
        "status": "not_started",
        "synthetic_only": True,
        "contains_patient_data": False,
        "external_submission_allowed": False,
        "commands": [],
    }
    missing = missing_dependencies()
    if missing:
        result.update(
            {
                "status": "skipped_missing_dependency",
                "missing_dependencies": missing,
                "inspect_task_build_passed": False,
                "lm_eval_validate_passed": False,
                "lm_eval_dummy_run_passed": False,
            }
        )
        write_result(args.write_result, result)
        print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
        return 0 if args.skip_missing else 1

    try:
        result.update(framework_versions())
        result.update(run_inspect_smoke())
        result.update(run_lm_eval_smoke())
        result["status"] = "passed"
    except Exception as exc:
        result["status"] = "failed"
        result["error"] = str(exc)
        write_result(args.write_result, result)
        print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
        return 1

    write_result(args.write_result, result)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
    return 0


def missing_dependencies() -> list[str]:
    missing: list[str] = []
    for module in ("inspect_ai", "lm_eval", "datasets", "yaml"):
        try:
            __import__(module)
        except ModuleNotFoundError:
            missing.append(module)
    if lm_eval_bin() is None:
        missing.append("lm_eval_cli")
    return missing


def framework_versions() -> dict[str, str]:
    import datasets
    import inspect_ai
    import lm_eval

    return {
        "python": sys.version.split()[0],
        "inspect_ai_version": getattr(inspect_ai, "__version__", "unknown"),
        "lm_eval_version": getattr(lm_eval, "__version__", "unknown"),
        "datasets_version": getattr(datasets, "__version__", "unknown"),
    }


def run_inspect_smoke() -> dict[str, Any]:
    from adapters.inspect_evals.medfailbench_safety_layer_v0_1 import (
        build_samples,
        medfailbench_safety_layer,
        medfailbench_safety_scorer,
    )
    from inspect_ai.model import ModelOutput
    from inspect_ai.scorer import Target
    from inspect_ai.solver import TaskState

    samples = build_samples()
    task = medfailbench_safety_layer()
    state = TaskState(
        model="mockllm/model",
        sample_id=samples[0].id,
        epoch=0,
        input=samples[0].input,
        messages=[],
        target=Target(samples[0].target),
        output=ModelOutput.from_content(
            model="mockllm/model",
            content="This may be urgent. Seek emergency care now and do not wait.",
        ),
        metadata=samples[0].metadata,
    )
    score = asyncio.run(medfailbench_safety_scorer()(state, Target(samples[0].target)))
    return {
        "inspect_task_build_passed": True,
        "inspect_sample_count": len(samples),
        "inspect_task_type": type(task).__name__,
        "inspect_scorer_count": len(task.scorer),
        "inspect_scorer_smoke_value": score.value,
        "inspect_scorer_metadata_keys": sorted(score.metadata or {}),
    }


def run_lm_eval_smoke() -> dict[str, Any]:
    output_dir = Path(tempfile.mkdtemp(prefix="medfailbench_lm_eval_smoke_"))
    validate_cmd = [
        str(lm_eval_bin()),
        "validate",
        "--tasks",
        TASK_NAME,
        "--include_path",
        LM_EVAL_INCLUDE_PATH,
    ]
    run_cmd = [
        str(lm_eval_bin()),
        "run",
        "--model",
        "dummy",
        "--tasks",
        TASK_NAME,
        "--include_path",
        LM_EVAL_INCLUDE_PATH,
        "--limit",
        "1",
        "--output_path",
        str(output_dir),
        "--log_samples",
    ]
    validate_result = run_command(validate_cmd)
    run_result = run_command(run_cmd)
    result_file = next(output_dir.rglob("results_*.json"), None)
    sample_file = next(output_dir.rglob("samples_*.jsonl"), None)
    result_payload = json.loads(result_file.read_text(encoding="utf-8")) if result_file else {}
    task_result = result_payload.get("results", {}).get(TASK_NAME, {})
    return {
        "lm_eval_validate_passed": True,
        "lm_eval_dummy_run_passed": True,
        "lm_eval_output_dir": "<temporary_lm_eval_output_dir>",
        "lm_eval_result_file_found": result_file is not None,
        "lm_eval_sample_file_found": sample_file is not None,
        "lm_eval_sample_len": task_result.get("sample_len"),
        "lm_eval_composite": task_result.get("medfailbench_composite,none"),
        "commands": [
            {"cmd": redact_command(validate_cmd, output_dir), "stdout_tail": tail_lines(run_resultless_stdout(validate_result.stdout))},
            {"cmd": redact_command(run_cmd, output_dir), "stdout_tail": tail_lines(run_resultless_stdout(run_result.stdout))},
        ],
    }


def run_command(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def tail_lines(text: str, limit: int = 12) -> list[str]:
    return text.splitlines()[-limit:]


def redact_command(cmd: list[str], output_dir: Path) -> list[str]:
    redacted: list[str] = []
    for part in cmd:
        if part == str(lm_eval_bin()):
            redacted.append("lm_eval")
        elif part == str(output_dir):
            redacted.append("<temporary_lm_eval_output_dir>")
        else:
            redacted.append(part)
    return redacted


def run_resultless_stdout(stdout: str) -> str:
    return stdout.replace(str(ROOT), "<repo_root>")


def lm_eval_bin() -> Path | None:
    sibling = Path(sys.executable).with_name("lm_eval")
    if sibling.exists():
        return sibling
    found = shutil.which("lm_eval")
    return Path(found) if found else None


def write_result(path: Path | None, result: dict[str, Any]) -> None:
    if path is None:
        return
    output = path if path.is_absolute() else ROOT / path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
