from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_clinician_panel_reviewer_packet_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_clinician_panel_reviewer_packet_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS clinician panel reviewer packet validation" in result.stdout


def test_clinician_panel_reviewer_packet_boundaries_are_locked() -> None:
    payload = json.loads((ROOT / "docs" / "clinician_panel_reviewer_packet_20260708.json").read_text(encoding="utf-8"))

    assert payload["case_count"] == 15
    assert payload["assignment_count"] == 30
    assert payload["contains_patient_data"] is False
    assert payload["synthetic_examples_only"] is True
    assert payload["no_clinical_validation_claim"] is True
    assert payload["no_model_ranking"] is True
    assert payload["external_send_allowed"] is False
    assert payload["requires_owner_approval_before_send"] is True


def test_clinician_panel_reviewer_message_has_no_external_link() -> None:
    message = (ROOT / "docs" / "CLINICIAN_PANEL_REVIEWER_MESSAGE_20260708.md").read_text(encoding="utf-8")

    assert "http://" not in message
    assert "https://" not in message
    assert "gerçek hasta verisi değildir" in message
    assert "tanı veya tedavi önerisi istemiyorum" in message
