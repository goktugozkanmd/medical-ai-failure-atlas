from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_medhelm_bilingual_adapter_example_is_live_and_safe_scoped() -> None:
    example_path = ROOT / "docs" / "medhelm_bilingual_safety_gate_example_v0_1.json"
    example = json.loads(example_path.read_text(encoding="utf-8"))

    assert example["schema_version"] == "medfailbench_medhelm_adapter_example_v0_1"
    assert example["status"] == "discussion_proposal_not_medhelm_endorsed"
    assert example["created_from_live_model_run"] is True
    assert example["synthetic_only"] is True
    assert example["patient_data_used"] is False
    assert example["clinical_use_allowed"] is False
    assert example["rule_gate_check"]["bilingual_consistency_passed"] is True
    assert example["rule_gate_check"]["note"] == "Rule-gate check only. This is not clinical validation and not a model ranking claim."

    for language in ("en", "tr"):
        gate_check = example["rule_gate_check"][language]
        assert gate_check["passed_count"] == gate_check["total_checks"] == 5
        assert gate_check["unsafe_discharge_reassurance_triggered"] is False


def test_medhelm_bilingual_adapter_hashes_match_raw_artifacts() -> None:
    example = json.loads((ROOT / "docs" / "medhelm_bilingual_safety_gate_example_v0_1.json").read_text(encoding="utf-8"))
    model_run = example["model_run"]

    raw_output = ROOT / model_run["raw_output_path"]
    sidecar = ROOT / model_run["run_metadata_path"]
    prompt_tsv = ROOT / "data" / "medhelm_bilingual_pair_v0_1.tsv"
    sidecar_json = json.loads(sidecar.read_text(encoding="utf-8"))

    assert raw_output.exists()
    assert sidecar.exists()
    assert prompt_tsv.exists()
    assert sha256_file(raw_output) == model_run["raw_output_sha256"]
    assert sha256_file(prompt_tsv) == model_run["prompt_tsv_sha256"]
    assert sidecar_json["completion_status"] == "completed"
    assert sidecar_json["row_counts"] == {"expected": 2, "completed": 2, "pending": 0}
