from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_safetyguard_eval_dry_run_with_limit_makes_no_api_call(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "safetyguard",
            "eval",
            "--model",
            "demo-model",
            "--dry-run",
            "--limit",
            "3",
            "--output",
            str(tmp_path / "out"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Dry run: would evaluate 3 prompt(s)" in result.stdout
    assert "No API calls were made." in result.stdout
    assert not (tmp_path / "out").exists()


def test_safetyguard_compare_reads_failure_atlas_score_json(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs"
    run_dir.mkdir()
    score_file = run_dir / "demo_scores.json"
    score_file.write_text(
        json.dumps(
            {
                "schema_version": "failure_atlas_scores_v0_1",
                "model_name": "demo-model",
                "items": [
                    {
                        "scenario_id": "A",
                        "scores": {"safety": 1, "source_transparency": 2, "clinical_grounding": 3},
                        "final_label": "unsafe",
                    },
                    {
                        "scenario_id": "B",
                        "scores": {"safety": 4, "source_transparency": 5, "clinical_grounding": 4},
                        "final_label": "clinically_usable_with_caution",
                    },
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "safetyguard", "compare", "--runs", str(run_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "demo-model" in result.stdout
    assert "2.5" in result.stdout
    assert "1/2 (50.0%)" in result.stdout


def test_safetyguard_eval_full_pipeline_with_local_openai_compatible_server(tmp_path: Path) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), FakeChatHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    endpoint = f"http://127.0.0.1:{server.server_port}/v1/chat/completions"
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = "test-key"
    out_dir = tmp_path / "safetyguard"

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "safetyguard",
                "eval",
                "--model",
                "demo-model",
                "--endpoint",
                endpoint,
                "--limit",
                "2",
                "--rpm",
                "0",
                "--output",
                str(out_dir),
            ],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

    assert result.returncode == 0, result.stderr
    score_path = out_dir / "demo-model_scores.json"
    assert score_path.exists()
    assert (out_dir / "reports" / "demo-model_report.md").exists()
    assert (out_dir / "reports" / "demo-model_summary.csv").exists()
    scores = json.loads(score_path.read_text(encoding="utf-8"))
    assert scores["model_name"] == "demo-model"
    assert len(scores["items"]) == 2


class FakeChatHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        _ = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        body = json.dumps(
            {
                "choices": [
                    {
                        "message": {
                            "content": "This may be urgent. Seek emergency care now and consult a clinician. Do not adjust medication dosing remotely."
                        }
                    }
                ]
            }
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return
