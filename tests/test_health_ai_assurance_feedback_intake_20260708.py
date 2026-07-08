from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_health_ai_assurance_feedback_intake_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_health_ai_assurance_feedback_intake_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS health AI assurance feedback intake validation" in result.stdout
    assert "routes=4" in result.stdout
    assert "small_tasks=5" in result.stdout
