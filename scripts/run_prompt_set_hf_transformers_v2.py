#!/usr/bin/env python3
"""Run prompt TSV rows with Hugging Face Transformers.

This is an execution scaffold for local or hosted model weights. Dry run does
not import transformers or load a model.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import signal
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class GenerationTimeout(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    return sha256_bytes(path.read_bytes())


def atomic_write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def read_prompts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    required = {"scenario_id", "prompt_text"}
    missing = required - set(rows[0] if rows else {})
    if missing:
        raise SystemExit(f"Prompt TSV missing columns: {sorted(missing)}")
    seen: set[str] = set()
    for index, row in enumerate(rows):
        scenario_id = row["scenario_id"].strip()
        prompt_text = row["prompt_text"]
        if not scenario_id:
            raise SystemExit(f"Prompt row {index} has empty scenario_id")
        if scenario_id in seen:
            raise SystemExit(f"Duplicate scenario_id: {scenario_id}")
        if not prompt_text.strip():
            raise SystemExit(f"Prompt row {index} has empty prompt_text")
        seen.add(scenario_id)
    return rows


def default_sidecar_path(output_path: Path) -> Path:
    if output_path.suffix:
        return output_path.with_suffix(".run_metadata.json")
    return output_path.with_name(output_path.name + ".run_metadata.json")


def load_existing_rows(output_path: Path, expected_ids: list[str]) -> dict[str, dict[str, str]]:
    if not output_path.exists():
        return {}
    data = json.loads(output_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("Existing output JSON must be a list")
    expected_set = set(expected_ids)
    rows_by_id: dict[str, dict[str, str]] = {}
    for index, row in enumerate(data):
        if not isinstance(row, dict) or set(row) != {"scenario_id", "model_answer"}:
            raise SystemExit(f"Existing output row {index} is not validator compatible")
        scenario_id = row["scenario_id"]
        answer = row["model_answer"]
        if scenario_id not in expected_set:
            raise SystemExit(f"Existing output has unknown scenario_id: {scenario_id}")
        if scenario_id in rows_by_id:
            raise SystemExit(f"Existing output has duplicate scenario_id: {scenario_id}")
        if not isinstance(answer, str) or not answer.strip():
            raise SystemExit(f"Existing output row {index} has empty model_answer")
        rows_by_id[scenario_id] = {"scenario_id": scenario_id, "model_answer": answer}
    existing_order = [row["scenario_id"] for row in data]
    expected_prefix = [scenario_id for scenario_id in expected_ids if scenario_id in rows_by_id]
    if existing_order != expected_prefix:
        raise SystemExit("Existing output scenario order is not a prompt ordered prefix or subset")
    return rows_by_id


def ordered_rows(expected_ids: list[str], rows_by_id: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    return [rows_by_id[scenario_id] for scenario_id in expected_ids if scenario_id in rows_by_id]


def make_sidecar(
    *,
    args: argparse.Namespace,
    prompt_path: Path,
    output_path: Path,
    rows_by_id: dict[str, dict[str, str]],
    prompts: list[dict[str, str]],
    scenario_metadata: dict[str, dict[str, Any]],
    completion_status: str,
) -> dict[str, Any]:
    expected_ids = [row["scenario_id"] for row in prompts]
    completed_ids = [scenario_id for scenario_id in expected_ids if scenario_id in rows_by_id]
    per_scenario = []
    for prompt_row in prompts:
        scenario_id = prompt_row["scenario_id"]
        row = rows_by_id.get(scenario_id)
        metadata = dict(scenario_metadata.get(scenario_id, {}))
        metadata.update(
            {
                "scenario_id": scenario_id,
                "prompt_sha256": sha256_text(prompt_row["prompt_text"]),
                "status": metadata.get("status", "completed" if row else "pending"),
            }
        )
        if row:
            metadata["answer_sha256"] = sha256_text(row["model_answer"])
        per_scenario.append(metadata)
    return {
        "schema_version": "open_model_run_v2",
        "runner_name": "run_prompt_set_hf_transformers_v2",
        "created_or_updated_at_utc": utc_now(),
        "model_id": args.model,
        "provider_route": "huggingface_transformers_local",
        "generation_settings": {
            "max_new_tokens": args.max_new_tokens,
            "timeout_seconds": args.timeout_seconds,
            "max_attempts": args.max_attempts,
        },
        "prompt_tsv": str(prompt_path),
        "prompt_tsv_sha256": sha256_file(prompt_path),
        "raw_output_json": str(output_path),
        "raw_output_sha256": sha256_file(output_path),
        "row_counts": {
            "expected": len(expected_ids),
            "completed": len(completed_ids),
            "pending": len(expected_ids) - len(completed_ids),
        },
        "completion_status": completion_status,
        "scenario_order": expected_ids,
        "completed_scenario_ids": completed_ids,
        "per_scenario": per_scenario,
    }


def alarm_handler(signum: int, frame: object) -> None:
    raise GenerationTimeout("generation timed out")


def generate_one(tokenizer: Any, model: Any, prompt_text: str, max_new_tokens: int, timeout_seconds: int) -> str:
    old_handler = signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout_seconds)
    try:
        inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        return tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1] :], skip_special_tokens=True)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run prompt TSV rows with Hugging Face Transformers.")
    parser.add_argument("--prompts", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--sidecar", type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--max-new-tokens", type=int, default=768)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--max-attempts", type=int, default=1)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.resume and args.overwrite:
        raise SystemExit("--resume and --overwrite cannot be used together")
    if args.max_attempts < 1:
        raise SystemExit("--max-attempts must be at least 1")

    prompt_path = args.prompts.resolve()
    output_path = args.output.resolve()
    sidecar_path = (args.sidecar or default_sidecar_path(output_path)).resolve()
    prompts = read_prompts(prompt_path)
    expected_ids = [row["scenario_id"] for row in prompts]

    if output_path.exists() and not args.resume and not args.overwrite and not args.dry_run:
        raise SystemExit(f"Output exists. Use --resume or --overwrite: {output_path}")

    rows_by_id: dict[str, dict[str, str]] = {}
    if args.resume or args.dry_run:
        rows_by_id = load_existing_rows(output_path, expected_ids)
    elif args.overwrite and output_path.exists():
        output_path.unlink()

    print(f"Prompt rows: {len(prompts)}")
    print(f"Completed rows already present: {len(rows_by_id)}")
    print(f"Output: {output_path}")
    print(f"Sidecar: {sidecar_path}")

    if args.dry_run:
        print("DRY RUN: no model import, no model load, and no file write performed")
        return

    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise SystemExit("Install transformers and a suitable torch build before running this script") from exc

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, device_map="auto")

    scenario_metadata: dict[str, dict[str, Any]] = {}
    for prompt_row in prompts:
        scenario_id = prompt_row["scenario_id"]
        if scenario_id in rows_by_id:
            scenario_metadata[scenario_id] = {
                "status": "resumed",
                "attempts": 0,
            }
            continue
        started_at = utc_now()
        errors: list[str] = []
        answer = ""
        latency_ms = 0
        for attempt in range(1, args.max_attempts + 1):
            started = time.monotonic()
            try:
                answer = generate_one(
                    tokenizer=tokenizer,
                    model=model,
                    prompt_text=prompt_row["prompt_text"],
                    max_new_tokens=args.max_new_tokens,
                    timeout_seconds=args.timeout_seconds,
                )
                if not answer.strip():
                    raise RuntimeError("empty model answer")
                latency_ms = int((time.monotonic() - started) * 1000)
                break
            except GenerationTimeout as exc:
                errors.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
                if attempt >= args.max_attempts:
                    scenario_metadata[scenario_id] = {
                        "status": "failed",
                        "started_at_utc": started_at,
                        "ended_at_utc": utc_now(),
                        "attempts": attempt,
                        "errors": errors,
                    }
                    atomic_write_json(
                        sidecar_path,
                        make_sidecar(
                            args=args,
                            prompt_path=prompt_path,
                            output_path=output_path,
                            rows_by_id=rows_by_id,
                            prompts=prompts,
                            scenario_metadata=scenario_metadata,
                            completion_status="failed",
                        ),
                    )
                    raise
            except Exception as exc:  # noqa: BLE001
                errors.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
                scenario_metadata[scenario_id] = {
                    "status": "failed",
                    "started_at_utc": started_at,
                    "ended_at_utc": utc_now(),
                    "attempts": attempt,
                    "errors": errors,
                }
                atomic_write_json(
                    sidecar_path,
                    make_sidecar(
                        args=args,
                        prompt_path=prompt_path,
                        output_path=output_path,
                        rows_by_id=rows_by_id,
                        prompts=prompts,
                        scenario_metadata=scenario_metadata,
                        completion_status="failed",
                    ),
                )
                raise

        rows_by_id[scenario_id] = {"scenario_id": scenario_id, "model_answer": answer}
        atomic_write_json(output_path, ordered_rows(expected_ids, rows_by_id))
        scenario_metadata[scenario_id] = {
            "status": "completed",
            "started_at_utc": started_at,
            "ended_at_utc": utc_now(),
            "latency_ms": latency_ms,
            "attempts": len(errors) + 1,
            "errors_before_success": errors,
        }
        atomic_write_json(
            sidecar_path,
            make_sidecar(
                args=args,
                prompt_path=prompt_path,
                output_path=output_path,
                rows_by_id=rows_by_id,
                prompts=prompts,
                scenario_metadata=scenario_metadata,
                completion_status="partial" if len(rows_by_id) < len(expected_ids) else "completed",
            ),
        )

    print(f"Completed rows: {len(rows_by_id)}")
    print(f"Wrote: {output_path}")
    print(f"Wrote: {sidecar_path}")


if __name__ == "__main__":
    main()
