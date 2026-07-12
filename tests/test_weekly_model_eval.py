from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / "scripts" / "weekly_model_eval.py"))
generate_report = MODULE["generate_report"]
filter_complete_reports = MODULE["filter_complete_reports"]
is_model_error = MODULE["is_model_error"]
extract_model_content = MODULE["extract_model_content"]


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


def test_model_errors_are_recognized() -> None:
    assert is_model_error("[ERROR: OPENROUTER_API_KEY not set]")
    assert is_model_error("[API ERROR: timed out]")
    assert not is_model_error("A valid model response")
    assert is_model_error(None)


def test_extract_model_content_accepts_non_empty_text() -> None:
    payload = {"choices": [{"message": {"content": "  clinical answer  "}}]}

    assert extract_model_content(payload) == "  clinical answer  "


def test_extract_model_content_rejects_null_content() -> None:
    payload = {"choices": [{"message": {"content": None}}]}

    try:
        extract_model_content(payload)
    except ValueError as exc:
        assert str(exc) == "response message has no text content"
    else:
        raise AssertionError("null content must be rejected")


def test_extract_model_content_rejects_missing_choices() -> None:
    try:
        extract_model_content({"choices": []})
    except ValueError as exc:
        assert str(exc) == "response has no choices"
    else:
        raise AssertionError("missing choices must be rejected")


def test_generate_report_marks_api_failures_incomplete_without_scoring_them() -> None:
    report = generate_report(
        "test-model",
        [_prompt_result("seek emergency care now")],
        [{"prompt_id": "H002", "error": "[API ERROR: timed out]"}],
    )

    assert report["run_status"] == "incomplete"
    assert report["prompts_attempted"] == 2
    assert report["prompts_evaluated"] == 1
    assert report["prompts_failed"] == 1
    assert sum(report["label_distribution"].values()) == 1
    assert report["prompt_errors"] == [
        {"prompt_id": "H002", "error": "[API ERROR: timed out]"}
    ]


def test_filter_complete_reports_excludes_incomplete_run() -> None:
    complete_results = [
        {**_prompt_result("seek emergency care now"), "prompt_id": prompt_id}
        for prompt_id in ("H001", "H002", "H003", "H004", "H005")
    ]
    complete = generate_report("complete-model", complete_results)
    incomplete = generate_report(
        "incomplete-model",
        complete_results[:4],
        [{"prompt_id": "H005", "error": "[API ERROR: timed out]"}],
    )
    short_run = generate_report("short-model", complete_results[:4])

    published, excluded = filter_complete_reports([complete, incomplete, short_run])

    assert [report["model"] for report in published] == ["complete-model"]
    assert short_run["run_status"] == "incomplete"
    assert [report["model"] for report in excluded] == [
        "incomplete-model",
        "short-model",
    ]


def test_filter_complete_reports_fails_closed_on_missing_status() -> None:
    report = {
        "model": "legacy-model",
        "prompts_attempted": 5,
        "prompts_evaluated": 5,
        "prompts_failed": 0,
    }

    published, excluded = filter_complete_reports([report])

    assert published == []
    assert excluded == [report]


def test_filter_complete_reports_rejects_inconsistent_complete_marker() -> None:
    report = {
        "model": "partial-model",
        "run_status": "complete",
        "prompts_attempted": 4,
        "prompts_evaluated": 4,
        "prompts_failed": 0,
    }

    published, excluded = filter_complete_reports([report])

    assert published == []
    assert excluded == [report]
