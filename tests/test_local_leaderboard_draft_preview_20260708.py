from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_local_leaderboard_draft_preview_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_local_leaderboard_draft_preview_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS local leaderboard draft preview validation" in result.stdout
    assert "public_leaderboard_modified=false" in result.stdout
