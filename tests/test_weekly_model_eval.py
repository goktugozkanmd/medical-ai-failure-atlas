from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / "scripts" / "weekly_model_eval.py"))
generate_report = MODULE["generate_report"]


def _prompt_result(output: str, label: str = "safe") -> dict:
    return {
        "prompt_id": "H001",
        "output": output,
        "output_preview": output[:20],
        "scores": {"final_label": label},
    }


def test_generate_report_scores_safety_gates_from_full_output() -> None:
    report = generate_report(
        "test-model",
        [
            _prompt_result("Context " * 40 + "seek emergency care now"),
            _prompt_result("Monitor symptoms at home"),
        ],
    )

    assert report["safety_gate_counts"]["missed_urgent_escalation"] == 1


def test_generate_report_does_not_persist_full_output() -> None:
    report = generate_report("test-model", [_prompt_result("seek emergency care now")])

    assert report["prompt_results"][0]["output_preview"] == "seek emergency care "
    assert "output" not in report["prompt_results"][0]
