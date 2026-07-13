import json
from pathlib import Path

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


def _write_raw_outputs(path: Path, count: int) -> Path:
    rows = [
        {"scenario_id": scenario_id, "model_answer": f"Answer {scenario_id}"}
        for scenario_id in _scenario_ids(count)
    ]
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
                "scenario_id": row["scenario_id"],
                "status": "completed",
                "answer_sha256": upload_results_to_hf.sha256_text(row["model_answer"]),
            }
            for row in rows
        ],
    }
    sidecar_path = raw_path.with_suffix(".run_metadata.json")
    sidecar_path.write_text(json.dumps(sidecar), encoding="utf-8")
    return sidecar_path
