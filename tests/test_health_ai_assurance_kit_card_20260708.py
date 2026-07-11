from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_health_ai_assurance_kit_card_exporter_and_validator_pass() -> None:
    export = subprocess.run(
        [sys.executable, "scripts/export_health_ai_assurance_kit_card_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert export.returncode == 0, export.stdout + export.stderr
    assert "evidence_layers=8" in export.stdout
    assert "external_gate=blocked_without_user_approval" in export.stdout

    validate = subprocess.run(
        [sys.executable, "scripts/validate_health_ai_assurance_kit_card_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "PASS Health AI Assurance Kit card validation" in validate.stdout
