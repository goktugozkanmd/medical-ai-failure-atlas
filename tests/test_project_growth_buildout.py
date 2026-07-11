from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_project_growth_buildout_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_project_growth_buildout_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS project growth buildout validation" in result.stdout
