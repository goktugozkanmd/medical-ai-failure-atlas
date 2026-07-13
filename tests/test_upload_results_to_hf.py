import json
from pathlib import Path

import pytest

import scripts.upload_results_to_hf as upload_results_to_hf


def test_discovery_skips_weekly_eval_without_run_metadata(
    tmp_path: Path,
    monkeypatch,
) -> None:
    prompt_path = _write_prompt_tsv(tmp_path, count=30)
    _write_raw_outputs(tmp_path / "weekly_eval_legacy_20260704_120000.json", count=5)
    monkeypatch.setattr(upload_results_to_hf, "DATA_DIR", tmp_path)
    monkeypatch.setattr(upload_results_to_hf, "HARD30_PROMPTS_FILE", prompt_path)

    runs, skipped = upload_results_to_hf.discover_model_runs_with_skips()

    assert runs == []
    assert skipped == [
        "weekly_eval_legacy_20260704_120000.json: missing run metadata sidecar"
    ]


def test_discovery_accepts_complete_weekly_eval_with_valid_sidecar(
    tmp_path: Path,
    monkeypatch,
) -> None:
    prompt_path = _write_prompt_tsv(tmp_path, count=30)
    raw_path = _write_raw_outputs(
        tmp_path / "weekly_eval_test-model_20260704_120000.json",
        count=30,
    )
    _write_sidecar(raw_path, prompt_path, count=30)
    monkeypatch.setattr(upload_results_to_hf, "DATA_DIR", tmp_path)
    monkeypatch.setattr(upload_results_to_hf, "HARD30_PROMPTS_FILE", prompt_path)

    runs, skipped = upload_results_to_hf.discover_model_runs_with_skips()

    assert skipped == []
    assert [run["result_file"] for run in runs] == [raw_path]


def test_discovery_blocks_weekly_eval_with_partial_sidecar(
    tmp_path: Path,
    monkeypatch,
) -> None:
    prompt_path = _write_prompt_tsv(tmp_path, count=30)
    raw_path = _write_raw_outputs(
        tmp_path / "weekly_eval_partial_20260704_120000.json",
        count=30,
    )
    _write_sidecar(raw_path, prompt_path, count=30, completion_status="partial")
    monkeypatch.setattr(upload_results_to_hf, "DATA_DIR", tmp_path)
    monkeypatch.setattr(upload_results_to_hf, "HARD30_PROMPTS_FILE", prompt_path)

    runs, skipped = upload_results_to_hf.discover_model_runs_with_skips()

    assert runs == []
    assert skipped == [
        "weekly_eval_partial_20260704_120000.json: completion_status=partial"
    ]


def test_discovery_blocks_weekly_eval_with_sidecar_hash_mismatch(
    tmp_path: Path,
    monkeypatch,
) -> None:
    prompt_path = _write_prompt_tsv(tmp_path, count=30)
    raw_path = _write_raw_outputs(
        tmp_path / "weekly_eval_bad_hash_20260704_120000.json",
        count=30,
    )
    _write_sidecar(raw_path, prompt_path, count=30, raw_output_sha256="bad")
    monkeypatch.setattr(upload_results_to_hf, "DATA_DIR", tmp_path)
    monkeypatch.setattr(upload_results_to_hf, "HARD30_PROMPTS_FILE", prompt_path)

    runs, skipped = upload_results_to_hf.discover_model_runs_with_skips()

    assert runs == []
    assert skipped == [
        "weekly_eval_bad_hash_20260704_120000.json: raw_output_sha256 mismatch"
    ]


def test_discovery_blocks_weekly_eval_with_non_object_row(
    tmp_path: Path,
    monkeypatch,
) -> None:
    prompt_path = _write_prompt_tsv(tmp_path, count=30)
    raw_path = _write_raw_outputs(
        tmp_path / "weekly_eval_non_object_20260704_120000.json",
        count=30,
        row_overrides={0: "not an object"},
    )
    _write_sidecar(raw_path, prompt_path, count=30)
    monkeypatch.setattr(upload_results_to_hf, "DATA_DIR", tmp_path)
    monkeypatch.setattr(upload_results_to_hf, "HARD30_PROMPTS_FILE", prompt_path)

    runs, skipped = upload_results_to_hf.discover_model_runs_with_skips()

    assert runs == []
    assert skipped == [
        "weekly_eval_non_object_20260704_120000.json: row 0 is not an object"
    ]


def test_discovery_blocks_weekly_eval_with_unexpected_row_keys(
    tmp_path: Path,
    monkeypatch,
) -> None:
    prompt_path = _write_prompt_tsv(tmp_path, count=30)
    raw_path = _write_raw_outputs(
        tmp_path / "weekly_eval_bad_keys_20260704_120000.json",
        count=30,
        row_overrides={
            0: {
                "scenario_id": "H001",
                "model_answer": "Answer H001",
                "extra": "leaks into raw output",
            }
        },
    )
    _write_sidecar(raw_path, prompt_path, count=30)
    monkeypatch.setattr(upload_results_to_hf, "DATA_DIR", tmp_path)
    monkeypatch.setattr(upload_results_to_hf, "HARD30_PROMPTS_FILE", prompt_path)

    runs, skipped = upload_results_to_hf.discover_model_runs_with_skips()

    assert runs == []
    assert skipped == [
        "weekly_eval_bad_keys_20260704_120000.json: row 0 has unexpected keys"
    ]


def test_discovery_blocks_weekly_eval_with_empty_model_answer(
    tmp_path: Path,
    monkeypatch,
) -> None:
    prompt_path = _write_prompt_tsv(tmp_path, count=30)
    raw_path = _write_raw_outputs(
        tmp_path / "weekly_eval_empty_answer_20260704_120000.json",
        count=30,
        row_overrides={0: {"scenario_id": "H001", "model_answer": "  "}},
    )
    _write_sidecar(raw_path, prompt_path, count=30)
    monkeypatch.setattr(upload_results_to_hf, "DATA_DIR", tmp_path)
    monkeypatch.setattr(upload_results_to_hf, "HARD30_PROMPTS_FILE", prompt_path)

    runs, skipped = upload_results_to_hf.discover_model_runs_with_skips()

    assert runs == []
    assert skipped == [
        "weekly_eval_empty_answer_20260704_120000.json: row 0 has empty model_answer"
    ]


def test_publish_gate_exits_when_skipped_items_exist(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        upload_results_to_hf.enforce_no_skips_before_publish(
            ["weekly_eval_partial.json: completion_status=partial"],
            allow_skips=False,
        )

    assert exc.value.code == 1
    output = capsys.readouterr().out
    assert "refused to publish" in output
    assert "weekly_eval_partial.json: completion_status=partial" in output


def test_publish_gate_allows_reviewed_skipped_items() -> None:
    upload_results_to_hf.enforce_no_skips_before_publish(
        ["weekly_eval_partial.json: completion_status=partial"],
        allow_skips=True,
    )


def test_publish_gate_allows_exact_reviewed_skip_manifest(tmp_path: Path) -> None:
    manifest = tmp_path / "reviewed_skips.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "hf_publish_reviewed_skips_v1",
                "skipped": [
                    {
                        "file": "weekly_eval_partial.json",
                        "reason": "completion_status=partial",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    upload_results_to_hf.enforce_no_skips_before_publish(
        ["weekly_eval_partial.json: completion_status=partial"],
        allow_skips=False,
        reviewed_skip_manifest=manifest,
    )


def test_publish_gate_rejects_unexpected_reviewed_skip_manifest(
    tmp_path: Path,
    capsys,
) -> None:
    manifest = tmp_path / "reviewed_skips.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "hf_publish_reviewed_skips_v1",
                "skipped": [
                    {
                        "file": "weekly_eval_partial.json",
                        "reason": "completion_status=partial",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(SystemExit) as exc:
        upload_results_to_hf.enforce_no_skips_before_publish(
            [
                "weekly_eval_partial.json: completion_status=partial",
                "weekly_eval_new.json: missing run metadata sidecar",
            ],
            allow_skips=False,
            reviewed_skip_manifest=manifest,
        )

    assert exc.value.code == 1
    output = capsys.readouterr().out
    assert "reviewed skip manifest does not match" in output
    assert "unexpected: weekly_eval_new.json: missing run metadata sidecar" in output


def test_strict_dry_run_exits_when_skipped_items_exist(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        upload_results_to_hf, "load_prompts_index", lambda: {"H001": {}}
    )
    monkeypatch.setattr(
        upload_results_to_hf,
        "collect_rows",
        lambda: (
            [
                {
                    "id": "run-H001",
                    "model_name": "test-model",
                    "model_response": "safe answer",
                }
            ],
            ["weekly_eval_partial.json: completion_status=partial"],
            [
                {
                    "name": "test-model",
                    "result_file": upload_results_to_hf.REPO_ROOT
                    / "model_runs"
                    / "weekly_eval_partial.json",
                    "rows": 1,
                    "skipped": 1,
                }
            ],
        ),
    )

    with pytest.raises(SystemExit) as exc:
        upload_results_to_hf.dry_run(strict=True)

    assert exc.value.code == 1
    output = capsys.readouterr().out
    assert "Total valid rows: 1" in output
    assert "refused to publish" in output


def test_strict_dry_run_allows_exact_reviewed_manifest(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    manifest = tmp_path / "reviewed_skips.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "hf_publish_reviewed_skips_v1",
                "skipped": [
                    {
                        "file": "weekly_eval_partial.json",
                        "reason": "completion_status=partial",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        upload_results_to_hf, "load_prompts_index", lambda: {"H001": {}}
    )
    monkeypatch.setattr(
        upload_results_to_hf,
        "collect_rows",
        lambda: (
            [
                {
                    "id": "run-H001",
                    "model_name": "test-model",
                    "model_response": "safe answer",
                }
            ],
            ["weekly_eval_partial.json: completion_status=partial"],
            [
                {
                    "name": "test-model",
                    "result_file": upload_results_to_hf.REPO_ROOT
                    / "model_runs"
                    / "weekly_eval_partial.json",
                    "rows": 1,
                    "skipped": 1,
                }
            ],
        ),
    )

    upload_results_to_hf.dry_run(strict=True, reviewed_skip_manifest=manifest)

    output = capsys.readouterr().out
    assert "Total valid rows: 1" in output
    assert "Run with HF_TOKEN set to actually publish." in output


def _scenario_ids(count: int) -> list[str]:
    return [f"H{index:03d}" for index in range(1, count + 1)]


def _write_prompt_tsv(tmp_path: Path, count: int) -> Path:
    path = tmp_path / "prompt_set_v2_hard_30.tsv"
    rows = ["scenario_id\tprompt_text\toutput_capture_instruction"]
    rows.extend(
        f"{scenario_id}\tPrompt {scenario_id}\tCapture"
        for scenario_id in _scenario_ids(count)
    )
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def _write_raw_outputs(
    path: Path,
    count: int,
    *,
    row_overrides: dict[int, object] | None = None,
) -> Path:
    rows = [
        {"scenario_id": scenario_id, "model_answer": f"Answer {scenario_id}"}
        for scenario_id in _scenario_ids(count)
    ]
    for index, row in (row_overrides or {}).items():
        rows[index] = row
    path.write_text(json.dumps(rows), encoding="utf-8")
    return path


def _write_sidecar(
    raw_path: Path,
    prompt_path: Path,
    count: int,
    *,
    completion_status: str = "completed",
    raw_output_sha256: str | None = None,
) -> Path:
    scenario_ids = _scenario_ids(count)
    rows = json.loads(raw_path.read_text(encoding="utf-8"))
    sidecar = {
        "schema_version": "open_model_run_v2",
        "completion_status": completion_status,
        "prompt_tsv_sha256": upload_results_to_hf.sha256_file(prompt_path),
        "raw_output_sha256": raw_output_sha256
        or upload_results_to_hf.sha256_file(raw_path),
        "row_counts": {
            "expected": count,
            "completed": count,
            "pending": 0,
        },
        "scenario_order": scenario_ids,
        "completed_scenario_ids": scenario_ids,
        "per_scenario": [
            {
                "scenario_id": row.get("scenario_id", scenario_ids[index])
                if isinstance(row, dict)
                else scenario_ids[index],
                "status": "completed",
                "answer_sha256": upload_results_to_hf.sha256_text(
                    str(row.get("model_answer", "")) if isinstance(row, dict) else ""
                ),
            }
            for index, row in enumerate(rows)
        ],
    }
    sidecar_path = raw_path.with_suffix(".run_metadata.json")
    sidecar_path.write_text(json.dumps(sidecar), encoding="utf-8")
    return sidecar_path
