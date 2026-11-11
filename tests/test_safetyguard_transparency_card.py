from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.export_safetyguard_transparency_card import EXAMPLE_SCORE_FILE, build_card, build_hf_evaluation_fields, render_hf_evaluation_card, render_markdown


ROOT = Path(__file__).resolve().parents[1]


def sample_scores() -> dict:
    return {
        "schema_version": "failure_atlas_scores_v0_1",
        "model_name": "demo-model",
        "method": "rule",
        "items": [
            {
                "scenario_id": "A",
                "scores": {"safety": 1, "source_transparency": 2},
                "safety_gates": {"missed_urgent_escalation": 4},
                "final_label": "unsafe",
                "reasons": ["Missed urgent escalation."],
            },
            {
                "scenario_id": "B",
                "scores": {"safety": 5, "source_transparency": 5},
                "safety_gates": {},
                "final_label": "clinically_useful",
                "reasons": ["Urgent escalation present."],
            },
        ],
    }


def test_transparency_card_builder_counts_worst_cases(tmp_path: Path) -> None:
    score_file = tmp_path / "scores.json"
    card = build_card(sample_scores(), score_file=score_file)

    assert card["schema_version"] == "safetyguard_transparency_card_v0_1"
    assert card["model_name"] == "demo-model"
    assert card["item_count"] == 2
    assert card["unsafe_item_count"] == 1
    assert card["source_gap_item_count"] == 1
    assert card["boundary_flags"]["external_action_allowed"] is False
    assert card["safety_gate_counts"]["missed_urgent_escalation"] == 1
    assert "clinical validation" in render_markdown(card)
    hf_fields = build_hf_evaluation_fields(card)
    assert hf_fields["unsafe_rate"] == 0.5
    assert hf_fields["source_gap_rate"] == 0.5
    assert "Hugging Face" in render_hf_evaluation_card(card)


def test_transparency_card_cli_writes_outputs(tmp_path: Path) -> None:
    score_file = tmp_path / "scores.json"
    out_json = tmp_path / "card.json"
    out_md = tmp_path / "card.md"
    out_hf_card = tmp_path / "hf_card.md"
    score_file.write_text(json.dumps(sample_scores()) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/export_safetyguard_transparency_card.py",
            "--score-file",
            str(score_file),
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--out-hf-card",
            str(out_hf_card),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert out_json.exists()
    assert out_md.exists()
    assert out_hf_card.exists()
    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload["unsafe_item_count"] == 1
    assert "Unsafe rate" in out_hf_card.read_text(encoding="utf-8")


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/export_safetyguard_transparency_card.py", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_transparency_card_cli_reports_missing_score_file_without_traceback(tmp_path: Path) -> None:
    result = _run_cli("--score-file", str(tmp_path / "missing_scores.json"))

    assert result.returncode == 2
    assert "score file not found" in result.stderr
    assert EXAMPLE_SCORE_FILE in result.stderr
    assert "Traceback" not in result.stderr


def test_transparency_card_cli_reports_wrong_shape_without_traceback(tmp_path: Path) -> None:
    score_file = tmp_path / "scores.json"
    score_file.write_text(json.dumps({"model_name": "demo-model"}) + "\n", encoding="utf-8")

    result = _run_cli("--score-file", str(score_file))

    assert result.returncode == 2
    assert "is not a Failure Atlas score JSON" in result.stderr
    assert "Traceback" not in result.stderr


def test_readme_transparency_card_command_runs_on_bundled_score_file(tmp_path: Path) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"export_safetyguard_transparency_card.py --score-file {EXAMPLE_SCORE_FILE}" in readme
    assert (ROOT / EXAMPLE_SCORE_FILE).is_file()

    out_json = tmp_path / "card.json"
    result = _run_cli(
        "--score-file", EXAMPLE_SCORE_FILE, "--out-json", str(out_json), "--out-md", str(tmp_path / "card.md")
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(out_json.read_text(encoding="utf-8"))["item_count"] > 0
