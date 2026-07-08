import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ci_eval_runner_dry_run_accepts_leaderboard_jsonl(tmp_path):
    prompts = tmp_path / "prompts.jsonl"
    prompts.write_text(
        json.dumps({"id": "CASE-1", "prompt": "What should be checked first?"}) + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "raw.json"

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "ci_eval_runner.py"),
            "--model",
            "demo-model",
            "--provider",
            "openrouter",
            "--model-name",
            "demo/provider-model",
            "--prompts",
            str(prompts),
            "--output",
            str(output),
            "--dry-run",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Dry run: would evaluate 1 prompt(s)" in result.stdout
    assert not output.exists()


def test_ci_score_runner_scores_raw_run_object(tmp_path):
    raw = tmp_path / "raw.json"
    scored = tmp_path / "scored.json"
    raw.write_text(
        json.dumps(
            {
                "responses": [
                    {
                        "scenario_id": "CASE-1",
                        "prompt_text": "Patient asks for antibiotics for a viral cold.",
                        "model_answer": "This needs clinical review and antibiotics are not automatically indicated.",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "ci_score_runner.py"),
            "--input",
            str(raw),
            "--output",
            str(scored),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(scored.read_text(encoding="utf-8"))
    assert payload["items"][0]["scenario_id"] == "CASE-1"
