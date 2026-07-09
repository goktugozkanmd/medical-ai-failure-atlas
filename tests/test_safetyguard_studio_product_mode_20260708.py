from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_safetyguard_studio_product_mode_exporter_and_validator_pass() -> None:
    export = subprocess.run(
        [sys.executable, "scripts/export_safetyguard_studio_product_mode_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert export.returncode == 0, export.stdout + export.stderr
    assert "product_mode_schema=safetyguard_studio_product_mode_v0_1" in export.stdout

    validate = subprocess.run(
        [sys.executable, "scripts/validate_safetyguard_studio_product_mode_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "PASS SafetyGuard Studio product mode validation" in validate.stdout
