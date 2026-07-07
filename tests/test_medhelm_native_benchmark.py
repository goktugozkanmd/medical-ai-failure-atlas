from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "medhelm-benchmark"
LABELS = {
    "missed_urgent_escalation",
    "unsafe_remote_dosing",
    "unsafe_discharge_reassurance",
    "evidence_fabrication_or_overclaim",
    "unsafe_protocol_execution_detail",
    "source_support_gap",
}


def test_medhelm_candidate_files_exist_and_parse() -> None:
    prompt = BENCH / "prompts" / "medfailbench_safety_gate_prompt.txt"
    dataset = BENCH / "datasets" / "medfailbench_safety_gate.csv"
    config = BENCH / "config" / "medfailbench_safety_gate.yaml"
    run_conf = BENCH / "run_medfailbench_safety_gate.conf"
    for path in (prompt, dataset, config, run_conf):
        assert path.exists(), path
        assert path.read_text(encoding="utf-8").strip()
    parsed = yaml.safe_load(config.read_text(encoding="utf-8"))
    assert parsed["name"] == "MEDFAILBENCH-SAFETY-GATE"
    assert parsed["prompt_file"] == "../prompts/medfailbench_safety_gate_prompt.txt"
    assert parsed["dataset_file"] == "../datasets/medfailbench_safety_gate.csv"
    assert parsed["metrics"][0]["name"] == "exact_match"
    assert "medhelm_configurable_benchmark" in run_conf.read_text(encoding="utf-8")


def test_medhelm_candidate_dataset_schema_and_boundaries() -> None:
    dataset = BENCH / "datasets" / "medfailbench_safety_gate.csv"
    with dataset.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 150
    required = {
        "scenario_id",
        "clinical_domain",
        "setting",
        "patient_summary",
        "task_for_model",
        "correct_answer",
        "incorrect_answers",
        "synthetic_only",
        "patient_data_used",
        "not_for_clinical_use",
    }
    assert required <= set(rows[0])
    assert len({row["scenario_id"] for row in rows}) == 150
    for row in rows:
        assert row["correct_answer"] in LABELS
        incorrect = json.loads(row["incorrect_answers"])
        assert set(incorrect) == LABELS - {row["correct_answer"]}
        assert row["synthetic_only"] == "true"
        assert row["patient_data_used"] == "false"
        assert row["not_for_clinical_use"] == "true"


def test_medhelm_candidate_no_overclaim_phrase() -> None:
    forbidden = "MedHELM compatible"
    for path in BENCH.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".txt", ".csv", ".yaml", ".yml", ".md", ".conf"}:
            assert forbidden not in path.read_text(encoding="utf-8")
