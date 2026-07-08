from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_health_ai_assurance_feedback_triage_board_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_health_ai_assurance_feedback_triage_board_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS health AI assurance feedback triage board validation" in result.stdout
    assert "routes=4" in result.stdout
    assert "states=6" in result.stdout
    assert "rows=6" in result.stdout
