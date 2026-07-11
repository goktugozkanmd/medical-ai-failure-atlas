from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_turkish_drift_preview_dashboard_exporter_and_validator_pass() -> None:
    export = subprocess.run(
        [sys.executable, "scripts/export_turkish_drift_preview_dashboard_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert export.returncode == 0, export.stdout + export.stderr
    assert "pairs=5" in export.stdout
    assert "turkish_rows=44" in export.stdout

    validate = subprocess.run(
        [sys.executable, "scripts/validate_turkish_drift_preview_dashboard_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "PASS Turkish drift preview dashboard validation" in validate.stdout
