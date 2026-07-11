from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_health_ai_assurance_kit_start_here_exporter_and_validator_pass() -> None:
    export = subprocess.run(
        [sys.executable, "scripts/export_health_ai_assurance_kit_start_here_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert export.returncode == 0, export.stdout + export.stderr
    assert "proof_pack_artifacts=9" in export.stdout
    assert "quick_start_steps=8" in export.stdout

    validate = subprocess.run(
        [sys.executable, "scripts/validate_health_ai_assurance_kit_start_here_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "PASS Health AI Assurance Kit Start Here validation" in validate.stdout
    assert "next_build_step=p8_followups_need_separate_review" in validate.stdout
