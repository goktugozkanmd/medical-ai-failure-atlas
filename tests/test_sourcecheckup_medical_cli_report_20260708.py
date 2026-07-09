from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_sourcecheckup_medical_cli_report_exporter_and_validator_pass() -> None:
    export = subprocess.run(
        [sys.executable, "scripts/export_sourcecheckup_medical_cli_report_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert export.returncode == 0, export.stdout + export.stderr
    assert "gate=blocked_pending_source_verification" in export.stdout

    validate = subprocess.run(
        [sys.executable, "scripts/validate_sourcecheckup_medical_cli_report_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "PASS SourceCheckup Medical CLI report validation" in validate.stdout
