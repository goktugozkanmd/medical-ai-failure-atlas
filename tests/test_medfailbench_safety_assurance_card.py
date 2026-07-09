from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_medfailbench_safety_assurance_card_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_medfailbench_safety_assurance_card_v0_1.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS MedFailBench safety assurance card validation" in result.stdout


def test_medfailbench_safety_assurance_card_keeps_boundary_flags() -> None:
    payload = json.loads((ROOT / "docs" / "medfailbench_safety_assurance_card_v0_1.json").read_text(encoding="utf-8"))

    assert payload["release_gate_level"] == "L1"
    assert payload["contains_patient_data"] is False
    assert payload["identifiers_present"] is False
    assert payload["synthetic_examples_only"] is True
    assert payload["no_clinical_validation_claim"] is True
    assert payload["no_model_safety_claim"] is True
    assert payload["no_model_ranking"] is True
    assert payload["external_action_allowed"] is False
    assert payload["current_evidence"]["panel_case_count"] == 15
    assert payload["current_evidence"]["panel_assignment_count"] == 30


def test_medfailbench_safety_assurance_card_has_official_source_anchors() -> None:
    payload = json.loads((ROOT / "docs" / "medfailbench_safety_assurance_card_v0_1.json").read_text(encoding="utf-8"))
    anchors = {anchor["source_id"]: anchor for anchor in payload["source_anchors"]}

    assert set(anchors) == {
        "nist_ai_rmf",
        "chai_applied_model_card",
        "fda_ai_device_lifecycle_draft",
        "fda_pccp_final_guidance",
        "who_lmm_health_guidance",
    }
    for anchor in anchors.values():
        assert anchor["official_page"].startswith("https://")
        assert anchor["support_status"] == "verified_from_official_page"
