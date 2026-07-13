from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / "scripts" / "weekly_model_eval.py"))
generate_report = MODULE["generate_report"]
filter_complete_reports = MODULE["filter_complete_reports"]
is_model_error = MODULE["is_model_error"]
extract_model_content = MODULE["extract_model_content"]
extract_model_response = MODULE["extract_model_response"]
assess_finish_reason = MODULE["assess_finish_reason"]
classify_finish_reason = MODULE["classify_finish_reason"]
build_confound_condition = MODULE["build_confound_condition"]
build_response_metadata = MODULE["build_response_metadata"]
call_model_with_length_retry = MODULE["call_model_with_length_retry"]
build_run_provenance = MODULE["build_run_provenance"]
build_eval_run_config = MODULE["build_eval_run_config"]
build_exclusion_audit = MODULE["build_exclusion_audit"]
generate_dry_run_report = MODULE["generate_dry_run_report"]
write_json_atomic = MODULE["write_json_atomic"]
HARD_PROMPT_IDS = MODULE["HARD_PROMPT_IDS"]


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
        "comparability_status": "eligible",
        "prompts_attempted": 4,
        "prompts_evaluated": 4,
        "prompts_failed": 0,
    }

    published, excluded = filter_complete_reports([report])

    assert published == []
    assert excluded == [report]


def test_filter_complete_reports_requires_eligible_comparability_status() -> None:
    report = generate_report(
        "test-model",
        [
            {**_prompt_result("seek emergency care now"), "prompt_id": prompt_id}
            for prompt_id in HARD_PROMPT_IDS
        ],
    )
    report["comparability_status"] = "ineligible"

    published, excluded = filter_complete_reports([report])
    audit = build_exclusion_audit(excluded)

    assert published == []
    assert excluded == [report]
    assert audit["excluded_reports"][0]["exclusion_reasons"] == [
        "comparability_status=ineligible"
    ]


def test_exclusion_audit_records_why_reports_are_not_published() -> None:
    report = generate_report(
        "confounded-model",
        [
            {**_prompt_result("seek emergency care now"), "prompt_id": prompt_id}
            for prompt_id in ("H001", "H002", "H003", "H004")
        ],
        confound_conditions=[
            {
                "prompt_id": "H005",
                "confound_type": "output_length_truncation",
                "category": "confound",
                "detail": "finish_reason is length",
                "metadata": {"finish_reason": "length"},
            }
        ],
    )

    audit = build_exclusion_audit([report])

    assert audit["excluded_count"] == 1
    row = audit["excluded_reports"][0]
    assert row["model"] == "confounded-model"
    assert row["run_status"] == "complete_with_confounds"
    assert "run_status=complete_with_confounds" in row["exclusion_reasons"]
    assert "comparability_status=confounded" in row["exclusion_reasons"]
    assert "prompts_confound_excluded=1" in row["exclusion_reasons"]
    assert "prompts_evaluated=4/5" in row["exclusion_reasons"]


def test_extract_model_response_preserves_finish_reason_and_usage() -> None:
    payload = {
        "choices": [
            {
                "message": {"content": "clinical answer"},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 42,
            "completion_tokens": 7,
            "total_tokens": 49,
        },
    }

    parsed = extract_model_response(payload)

    assert parsed["content"] == "clinical answer"
    assert parsed["finish_reason"] == "stop"
    assert parsed["usage"] == {
        "prompt_tokens": 42,
        "completion_tokens": 7,
        "total_tokens": 49,
    }


def test_extract_model_response_defaults_usage_to_none_when_missing() -> None:
    payload = {"choices": [{"message": {"content": "answer"}, "finish_reason": "stop"}]}

    parsed = extract_model_response(payload)

    assert parsed["finish_reason"] == "stop"
    assert parsed["usage"] is None


def test_extract_model_response_defaults_finish_reason_to_none_when_missing() -> None:
    payload = {
        "choices": [{"message": {"content": "answer"}}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3},
    }

    parsed = extract_model_response(payload)

    assert parsed["finish_reason"] is None


def test_extract_model_content_still_wraps_response() -> None:
    payload = {
        "choices": [{"message": {"content": "answer"}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3},
    }

    assert extract_model_content(payload) == "answer"


def test_assess_finish_reason_accepts_stop() -> None:
    ok, reason = assess_finish_reason("stop")

    assert ok is True
    assert reason == ""


def test_assess_finish_reason_fails_closed_on_length() -> None:
    ok, reason = assess_finish_reason("length")

    assert ok is False
    assert "length" in reason
    assert "truncat" in reason


def test_assess_finish_reason_fails_closed_on_null() -> None:
    ok, reason = assess_finish_reason(None)

    assert ok is False
    assert "null" in reason


def test_assess_finish_reason_fails_closed_on_empty_string() -> None:
    ok, reason = assess_finish_reason("")

    assert ok is False
    assert "empty" in reason


def test_assess_finish_reason_fails_closed_on_unknown_value() -> None:
    ok, reason = assess_finish_reason("content_filter")

    assert ok is False
    assert "content_filter" in reason


def test_assess_finish_reason_is_case_insensitive() -> None:
    ok, _ = assess_finish_reason("STOP")

    assert ok is True


def test_assess_finish_reason_rejects_non_string_type() -> None:
    ok, reason = assess_finish_reason(123)

    assert ok is False
    assert "not a string" in reason


def test_build_response_metadata_normalizes_usage_fields() -> None:
    response = {
        "content": "answer",
        "finish_reason": "stop",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
        },
    }

    metadata = build_response_metadata(response)

    assert metadata == {
        "finish_reason": "stop",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
        },
        "request_max_tokens": None,
        "attempts": [],
    }


def test_build_response_metadata_defaults_usage_to_none_when_absent() -> None:
    response = {"content": "answer", "finish_reason": "stop"}

    metadata = build_response_metadata(response)

    assert metadata["finish_reason"] == "stop"
    assert metadata["usage"] == {
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
    }


def test_build_response_metadata_preserves_null_usage_fields() -> None:
    response = {"content": "answer", "finish_reason": "stop", "usage": {}}

    metadata = build_response_metadata(response)

    assert metadata["usage"] == {
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
    }


def test_build_response_metadata_on_error_response_records_defaults() -> None:
    response = {"error": "[API ERROR: timed out]"}

    metadata = build_response_metadata(response)

    assert metadata["finish_reason"] is None
    assert metadata["usage"] == {
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
    }


def test_generate_report_tracks_length_as_a_non_failure_confound() -> None:
    prompt_results = [
        {**_prompt_result("seek emergency care now"), "prompt_id": prompt_id}
        for prompt_id in ("H001", "H002", "H003", "H004")
    ]
    metadata = {
        "finish_reason": "length",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 1024,
            "total_tokens": 1034,
        },
    }
    category, detail = classify_finish_reason("length")
    confound = build_confound_condition("H005", category, detail, metadata)
    report = generate_report(
        "test-model",
        prompt_results,
        confound_conditions=[confound],
    )

    assert report["run_status"] == "complete_with_confounds"
    assert report["comparability_status"] == "confounded"
    assert report["scoring_coverage"] == 0.8
    assert report["prompts_attempted"] == 5
    assert report["prompts_evaluated"] == 4
    assert report["prompts_failed"] == 0
    assert report["prompts_confound_excluded"] == 1
    assert sum(report["label_distribution"].values()) == 4
    assert report["confound_conditions"] == [confound]
    assert confound["confound_type"] == "output_length_truncation"
    assert confound["metadata"]["usage"]["total_tokens"] == 1034

    published, excluded = filter_complete_reports([report])

    assert published == []
    assert excluded == [report]


def test_generate_report_retains_metadata_on_successful_results() -> None:
    successful = {
        **_prompt_result("seek emergency care now"),
        "metadata": {
            "finish_reason": "stop",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15,
            },
        },
    }
    report = generate_report("test-model", [successful])

    assert report["prompt_results"][0]["metadata"]["finish_reason"] == "stop"
    assert report["prompt_results"][0]["metadata"]["usage"]["total_tokens"] == 15


def test_call_model_with_length_retry_doubles_budget_and_returns_clean_stop() -> None:
    calls = []

    def fake_call_model(model_key, prompt, timeout, max_tokens):
        calls.append((model_key, prompt, timeout, max_tokens))
        if len(calls) == 1:
            return {
                "content": "truncated",
                "finish_reason": "length",
                "usage": {"completion_tokens": max_tokens},
                "request_max_tokens": max_tokens,
            }
        return {
            "content": "complete answer",
            "finish_reason": "stop",
            "usage": {"completion_tokens": 1200},
            "request_max_tokens": max_tokens,
        }

    original = call_model_with_length_retry.__globals__["call_model"]
    call_model_with_length_retry.__globals__["call_model"] = fake_call_model
    try:
        response = call_model_with_length_retry(
            "test-model", "prompt", timeout=12, initial_max_tokens=1000
        )
    finally:
        call_model_with_length_retry.__globals__["call_model"] = original

    assert [call[-1] for call in calls] == [1000, 2000]
    assert response["content"] == "complete answer"
    assert response["finish_reason"] == "stop"
    assert [attempt["finish_reason"] for attempt in response["attempts"]] == [
        "length",
        "stop",
    ]


def test_call_model_with_length_retry_keeps_exhausted_confound_provenance() -> None:
    def fake_call_model(model_key, prompt, timeout, max_tokens):
        return {
            "content": "still truncated",
            "finish_reason": "length",
            "usage": {"completion_tokens": max_tokens},
            "request_max_tokens": max_tokens,
        }

    original = call_model_with_length_retry.__globals__["call_model"]
    call_model_with_length_retry.__globals__["call_model"] = fake_call_model
    try:
        response = call_model_with_length_retry(
            "test-model", "prompt", initial_max_tokens=512, length_retries=2
        )
    finally:
        call_model_with_length_retry.__globals__["call_model"] = original

    assert response["finish_reason"] == "length"
    assert [attempt["request_max_tokens"] for attempt in response["attempts"]] == [
        512,
        1024,
        2048,
    ]


def test_call_model_with_length_retry_rejects_invalid_retry_configuration() -> None:
    for kwargs, message in [
        ({"initial_max_tokens": 0}, "initial_max_tokens must be positive"),
        ({"length_retries": -1}, "length_retries must not be negative"),
    ]:
        try:
            call_model_with_length_retry("test-model", "prompt", **kwargs)
        except ValueError as exc:
            assert str(exc) == message
        else:
            raise AssertionError("invalid retry configuration must be rejected")


def test_eval_run_config_validates_token_retry_and_timeout_values() -> None:
    assert build_eval_run_config(
        max_tokens=2048, length_retries=2, timeout_seconds=90
    ) == {
        "initial_max_tokens": 2048,
        "length_retries": 2,
        "timeout_seconds": 90,
    }

    for kwargs, message in [
        ({"max_tokens": 0}, "max_tokens must be positive"),
        ({"length_retries": -1}, "length_retries must not be negative"),
        ({"timeout_seconds": 0}, "timeout_seconds must be positive"),
    ]:
        try:
            build_eval_run_config(**kwargs)
        except ValueError as exc:
            assert str(exc) == message
        else:
            raise AssertionError("invalid eval config must be rejected")


def test_dry_run_validates_inputs_without_creating_scores() -> None:
    provenance = {"execution_mode": "dry_run"}

    report = generate_dry_run_report(
        "test-model", list(HARD_PROMPT_IDS), [], provenance
    )
    published, excluded = filter_complete_reports([report])

    assert report["run_status"] == "dry_run_validated"
    assert report["comparability_status"] == "ineligible"
    assert report["prompts_evaluated"] == 0
    assert report["scoring_coverage"] == 0.0
    assert sum(report["label_distribution"].values()) == 0
    assert report["prompt_results"] == []
    assert published == []
    assert excluded == [report]


def test_run_provenance_pins_inputs_and_runtime() -> None:
    run_config = build_eval_run_config(
        max_tokens=2048, length_retries=2, timeout_seconds=90
    )
    provenance = build_run_provenance("deepseek-v4-flash", "live", run_config)

    assert provenance["report_schema_version"] == "1.1.0"
    assert provenance["evaluator_version"] == "0.3.0"
    assert provenance["execution_mode"] == "live"
    assert provenance["model"]["model_id"] == "deepseek/deepseek-v4-flash"
    assert len(provenance["prompt_set"]["sha256"]) == 64
    assert len(provenance["evaluator"]["sha256"]) == 64
    assert provenance["prompt_set"]["path"] == "data/prompt_set_v2_hard_30.tsv"
    assert provenance["run_config"] == run_config


def test_write_json_atomic_replaces_destination_without_temp_artifacts(
    tmp_path,
) -> None:
    destination = tmp_path / "report.json"
    destination.write_text('{"old": true}', encoding="utf-8")

    write_json_atomic(destination, {"status": "complete", "count": 5})

    assert destination.read_text(encoding="utf-8") == (
        '{\n  "status": "complete",\n  "count": 5\n}\n'
    )
    assert list(tmp_path.iterdir()) == [destination]
