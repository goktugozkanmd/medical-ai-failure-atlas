from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from failure_atlas.data import load_eval_set
from scripts.validate_opencompass_adapter_candidate_v0_1 import (
    validate_manifest,
    validate_source_alignment,
)


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
    assert "status=upstream_candidate_pr_open_pending_review" in validate.stdout


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


def test_opencompass_manifest_records_pending_upstream_pr_without_acceptance_claim() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["status"] == "upstream_candidate_pr_open_pending_review"
    assert manifest["opencompass_issue"] == "https://github.com/open-compass/opencompass/issues/2516"
    assert manifest["opencompass_pr"] == "https://github.com/open-compass/opencompass/pull/2560"
    assert manifest["upstream_review_state"] == "pending_maintainer_review"
    assert manifest["accepted_upstream"] is False
    assert manifest["no_official_compatibility_or_endorsement_claim"] is True


def test_opencompass_validator_rejects_upstream_acceptance_claim() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["accepted_upstream"] = True
    manifest["upstream_review_state"] = "accepted"

    errors: list[str] = []
    validate_manifest(manifest, errors)

    assert "manifest accepted_upstream must be False" in errors
    assert "manifest upstream_review_state must be 'pending_maintainer_review'" in errors


def test_opencompass_validator_rejects_source_hash_drift() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["source_sha256"] = "0" * 64

    errors: list[str] = []
    validate_manifest(manifest, errors)

    assert any(
        error.startswith(
            "manifest source_sha256 does not match "
            "data/tr_medllm_synthetic_eval_set_v0_3.jsonl"
        )
        for error in errors
    )


def test_opencompass_validator_rejects_export_hash_drift() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["export_sha256"] = "0" * 64

    errors: list[str] = []
    validate_manifest(manifest, errors)

    assert any(
        error.startswith(
            "manifest export_sha256 does not match "
            "adapters/opencompass/medfailbench_safety_layer_docs_v0_1.jsonl"
        )
        for error in errors
    )


def test_opencompass_validator_rejects_source_alignment_drift() -> None:
    rows = [
        json.loads(line)
        for line in DATASET.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    rows[0]["target"] = "This no longer matches the source safe answer expectation."
    rows[0]["metadata"]["review_status"] = "pending clinician review"

    errors: list[str] = []
    source_cases = load_eval_set(ROOT / "data" / "tr_medllm_synthetic_eval_set_v0_3.jsonl")
    validate_source_alignment(rows, source_cases, errors)

    assert "row 1 TRFAI015 target does not match source dataset" in errors
    assert "row 1 TRFAI015 metadata.review_status does not match source dataset" in errors
