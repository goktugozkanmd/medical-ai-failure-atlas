from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_controlled_batch_expansion_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_controlled_batch_expansion_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS controlled batch expansion validation" in result.stdout
    assert "core_release_cap=300" in result.stdout
