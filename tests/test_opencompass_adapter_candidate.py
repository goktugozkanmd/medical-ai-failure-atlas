from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "adapters" / "opencompass" / "medfailbench_safety_layer_docs_v0_1.jsonl"
MANIFEST = ROOT / "adapters" / "opencompass" / "medfailbench_safety_layer_manifest_v0_1.json"


def test_opencompass_exporter_and_validator_pass() -> None:
    export = subprocess.run(
        [sys.executable, "scripts/export_opencompass_adapter_candidate_v0_1.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert export.returncode == 0, export.stdout + export.stderr
    assert "rows=44" in export.stdout

    validate = subprocess.run(
        [sys.executable, "scripts/validate_opencompass_adapter_candidate_v0_1.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "PASS OpenCompass adapter candidate validation" in validate.stdout


def test_opencompass_candidate_rows_preserve_boundary_metadata() -> None:
    rows = [
        json.loads(line)
        for line in DATASET.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert len(rows) == manifest["row_count"] == 44
    assert rows[0]["id"] == "TRFAI015"
    assert rows[-1]["id"] == "TRFAI058"
    assert {row["language"] for row in rows} == {"tr"}
    assert all(row["metadata"]["synthetic_only"] is True for row in rows)
    assert all(row["metadata"]["contains_patient_data"] is False for row in rows)
    assert all(row["metadata"]["no_clinical_validation_claim"] is True for row in rows)
    assert all(row["metadata"]["no_model_ranking_claim"] is True for row in rows)
