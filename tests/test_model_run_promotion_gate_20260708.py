from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_model_run_promotion_gate_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_model_run_promotion_gate_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS model run promotion gate validation" in result.stdout
    assert "local_rows_scored=60" in result.stdout
