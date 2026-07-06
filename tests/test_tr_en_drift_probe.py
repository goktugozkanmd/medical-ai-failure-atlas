from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_tr_en_drift_glm_probe_artifacts_are_public_safe() -> None:
    summary = json.loads((ROOT / "docs" / "tr_en_drift_glm_probe_v0_1.json").read_text(encoding="utf-8"))
    sidecar = json.loads((ROOT / "model_runs" / "tr_en_drift_glm_5_2_probe_v0_1.run_metadata.json").read_text(encoding="utf-8"))
    raw_outputs = json.loads((ROOT / "model_runs" / "tr_en_drift_glm_5_2_probe_v0_1.json").read_text(encoding="utf-8"))

    assert summary["status"] == "small_probe_not_benchmark_claim"
    assert summary["synthetic_only"] is True
    assert summary["patient_data_used"] is False
    assert summary["clinical_validation_claim"] is False
    assert summary["pairs_evaluated"] == 5
    assert summary["outputs_evaluated"] == 10
    assert len(raw_outputs) == 10
    assert summary["summary"]["en_boundaries_met"] == 5
    assert summary["summary"]["tr_boundaries_met"] == 5

    assert sidecar["prompt_tsv"] == "data/tr_en_drift_glm_probe_v0_1.tsv"
    assert sidecar["raw_output_json"] == "model_runs/tr_en_drift_glm_5_2_probe_v0_1.json"
    assert "/Users/" not in json.dumps(sidecar)
    assert "/private/tmp" not in json.dumps(sidecar)


def test_tr_en_drift_glm_probe_markdown_keeps_boundary_language() -> None:
    markdown = (ROOT / "docs" / "TR_EN_DRIFT_GLM_PROBE_V0_1.md").read_text(encoding="utf-8")

    assert "not a benchmark claim" in markdown
    assert "No patient data used" in markdown
    assert "not clinical validation" in markdown
    assert "not a model ranking" in markdown
    assert "5 EN/TR pairs" in markdown
