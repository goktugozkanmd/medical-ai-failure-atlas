#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODEL_NAME = "release-gate-demo-model"
DEFAULT_OUTPUT_DIR = ROOT / "build" / "safetyguard_card_release_gate_20260708"
DEFAULT_MANIFEST = ROOT / "docs" / "safetyguard_card_release_gate_smoke_20260708.json"
PROMPT_SET = ROOT / "safetyguard" / "data" / "medfailbench_prompts_v0_2.tsv"
RUBRIC = ROOT / "safetyguard" / "data" / "scoring_rubric_v0_3.json"
SAFE_FAKE_ANSWER = (
    "This may be urgent. Seek emergency care now and do not wait. "
    "Do not adjust medication dosing remotely. I cannot verify external sources here; "
    "use clinician or emergency evaluation."
)
LOCAL_PATH_PATTERNS = (
    "/".join(["", "Users", "goktugozkan"]),
    str(ROOT),
    "/private/tmp",
    "/var/folders",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a local SafetyGuard card release gate smoke.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--limit", type=int, default=2)
    args = parser.parse_args()

    output_dir = resolve_path(args.output_dir)
    manifest_path = resolve_path(args.manifest)
    if args.limit < 1:
        print("--limit must be greater than zero", file=sys.stderr)
        return 2

    result: dict[str, Any] = {
        "artifact_id": "safetyguard_card_release_gate_smoke_20260708",
        "status": "not_started",
        "synthetic_only": True,
        "contains_patient_data": False,
        "external_submission_allowed": False,
        "local_fake_server_used": True,
        "prompt_count": args.limit,
        "commands": [],
    }

    try:
        prepare_output_dir(output_dir)
        server = ThreadingHTTPServer(("127.0.0.1", 0), FakeChatHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        endpoint = f"http://127.0.0.1:{server.server_port}/v1/chat/completions"
        try:
            result["commands"].append(run_safetyguard_eval(output_dir=output_dir, endpoint=endpoint, limit=args.limit))
            result["commands"].append(run_card_export(output_dir=output_dir))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

        result.update(collect_artifact_state(output_dir))
        errors = validate_artifacts(output_dir, result)
        result["release_gate_passed"] = not errors
        result["local_path_leak_scan_passed"] = not scan_path_leaks(output_dir)
        if not result["local_path_leak_scan_passed"]:
            errors.extend(scan_path_leaks(output_dir))

        if errors:
            result["status"] = "failed"
            result["errors"] = errors
            write_manifest(manifest_path, result)
            print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
            return 1

        result["status"] = "passed"
        write_manifest(manifest_path, result)
        print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        result["status"] = "failed"
        result["errors"] = [str(exc)]
        write_manifest(manifest_path, result)
        print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
        return 1


class FakeChatHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        _ = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        body = json.dumps({"choices": [{"message": {"content": SAFE_FAKE_ANSWER}}]}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def run_safetyguard_eval(*, output_dir: Path, endpoint: str, limit: int) -> dict[str, Any]:
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = "local-fake-key"
    cmd = [
        sys.executable,
        "-m",
        "safetyguard",
        "eval",
        "--model",
        MODEL_NAME,
        "--endpoint",
        endpoint,
        "--prompt-set",
        path_arg(PROMPT_SET),
        "--rubric",
        path_arg(RUBRIC),
        "--limit",
        str(limit),
        "--rpm",
        "0",
        "--output",
        path_arg(output_dir),
    ]
    return run_command("safetyguard_eval", cmd, env=env, endpoint=endpoint, output_dir=output_dir)


def run_card_export(*, output_dir: Path) -> dict[str, Any]:
    cmd = [
        sys.executable,
        "scripts/export_safetyguard_transparency_card.py",
        "--score-file",
        path_arg(score_path(output_dir)),
        "--out-json",
        path_arg(transparency_json_path(output_dir)),
        "--out-md",
        path_arg(transparency_md_path(output_dir)),
        "--out-hf-card",
        path_arg(hf_card_path(output_dir)),
    ]
    return run_command("card_export", cmd, env=os.environ.copy(), endpoint="", output_dir=output_dir)


def run_command(
    name: str,
    cmd: list[str],
    *,
    env: dict[str, str],
    endpoint: str,
    output_dir: Path,
) -> dict[str, Any]:
    completed = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True, check=False)
    record = {
        "name": name,
        "cmd": redact_command(cmd, endpoint=endpoint, output_dir=output_dir),
        "returncode": completed.returncode,
        "stdout_tail": tail_lines(redact_text(completed.stdout, endpoint=endpoint, output_dir=output_dir)),
        "stderr_tail": tail_lines(redact_text(completed.stderr, endpoint=endpoint, output_dir=output_dir)),
    }
    if completed.returncode != 0:
        raise RuntimeError(f"{name} failed with return code {completed.returncode}: {record}")
    return record


def collect_artifact_state(output_dir: Path) -> dict[str, Any]:
    score_payload = read_json(score_path(output_dir))
    card_payload = read_json(transparency_json_path(output_dir))
    hf_text = hf_card_path(output_dir).read_text(encoding="utf-8")
    item_count = int(card_payload.get("item_count", 0))
    unsafe_count = int(card_payload.get("unsafe_item_count", 0))
    return {
        "score_file": display_path(score_path(output_dir), output_dir),
        "transparency_card_json": display_path(transparency_json_path(output_dir), output_dir),
        "transparency_card_markdown": display_path(transparency_md_path(output_dir), output_dir),
        "hf_evaluation_card_markdown": display_path(hf_card_path(output_dir), output_dir),
        "score_schema_version": score_payload.get("schema_version"),
        "card_schema_version": card_payload.get("schema_version"),
        "score_item_count": len(score_payload.get("items", [])),
        "card_item_count": item_count,
        "unsafe_item_count": unsafe_count,
        "unsafe_rate": round(unsafe_count / item_count, 4) if item_count else 0,
        "source_gap_item_count": int(card_payload.get("source_gap_item_count", 0)),
        "boundary_flags": card_payload.get("boundary_flags", {}),
        "hf_card_contains_not_published_state": "Not published to Hugging Face" in hf_text,
    }


def validate_artifacts(output_dir: Path, result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        score_path(output_dir),
        transparency_json_path(output_dir),
        transparency_md_path(output_dir),
        hf_card_path(output_dir),
    ]
    for path in required:
        if not path.exists():
            errors.append(f"Missing artifact: {display_path(path, output_dir)}")

    if result.get("score_schema_version") != "failure_atlas_scores_v0_1":
        errors.append("Score JSON schema mismatch")
    if result.get("card_schema_version") != "safetyguard_transparency_card_v0_1":
        errors.append("Transparency card schema mismatch")
    if result.get("score_item_count") != result.get("prompt_count"):
        errors.append("Score item count does not match prompt count")
    if result.get("card_item_count") != result.get("prompt_count"):
        errors.append("Card item count does not match prompt count")
    flags = result.get("boundary_flags", {})
    if not isinstance(flags, dict):
        errors.append("Boundary flags missing")
        return errors
    expected_flags = {
        "contains_patient_data": False,
        "not_clinical_advice": True,
        "not_clinical_validation": True,
        "not_model_ranking": True,
        "not_official_endorsement": True,
        "external_action_allowed": False,
    }
    for key, expected in expected_flags.items():
        if flags.get(key) is not expected:
            errors.append(f"Boundary flag {key} must be {expected!r}")
    if result.get("hf_card_contains_not_published_state") is not True:
        errors.append("HF card must state that it is not published")
    return errors


def scan_path_leaks(output_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in LOCAL_PATH_PATTERNS:
            if pattern and pattern in text:
                errors.append(f"Local path pattern found in {display_path(path, output_dir)}: {pattern}")
    return errors


def prepare_output_dir(output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        if not is_under(output_dir, ROOT / "build"):
            raise RuntimeError(f"Refusing to clean non-build output directory: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def score_path(output_dir: Path) -> Path:
    return output_dir / f"{MODEL_NAME}_scores.json"


def transparency_json_path(output_dir: Path) -> Path:
    return output_dir / "safetyguard_transparency_card_v0_1.json"


def transparency_md_path(output_dir: Path) -> Path:
    return output_dir / "SAFETYGUARD_TRANSPARENCY_CARD_V0_1.md"


def hf_card_path(output_dir: Path) -> Path:
    return output_dir / "HF_EVALUATION_CARD_MEDFAILBENCH_SAFETY_LAYER_V0_1.md"


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected JSON object: {path}")
    return payload


def path_arg(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def display_path(path: Path, output_dir: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        pass
    try:
        relative = resolved.relative_to(output_dir.resolve())
        if relative.as_posix() == ".":
            return "<output_dir>"
        return f"<output_dir>/{relative.as_posix()}"
    except ValueError:
        return "<outside_repo>"


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def redact_command(cmd: list[str], *, endpoint: str, output_dir: Path) -> list[str]:
    return [
        "python3" if part == sys.executable else redact_text(part, endpoint=endpoint, output_dir=output_dir)
        for part in cmd
    ]


def redact_text(text: str, *, endpoint: str, output_dir: Path) -> str:
    redacted = text.replace(str(ROOT), "<repo_root>")
    redacted = redacted.replace(str(output_dir), display_path(output_dir, output_dir))
    if endpoint:
        redacted = redacted.replace(endpoint, "<local_fake_openai_server>")
    return redacted


def tail_lines(text: str, limit: int = 12) -> list[str]:
    return text.splitlines()[-limit:]


def write_manifest(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
