from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_model_run_normalization_plan_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_model_run_normalization_plan_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS model run normalization plan validation" in result.stdout
    assert "public_normalization_gap_rows=176" in result.stdout
