from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_health_ai_assurance_kit_roadmap_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_health_ai_assurance_kit_roadmap_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS health AI assurance kit roadmap validation" in result.stdout
    assert "next_build_step=p8_followups_need_separate_review" in result.stdout
