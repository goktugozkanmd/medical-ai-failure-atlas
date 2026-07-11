from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_health_ai_monitoring_digest_schema_exporter_and_validator_pass() -> None:
    export = subprocess.run(
        [sys.executable, "scripts/export_health_ai_monitoring_digest_schema_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert export.returncode == 0, export.stdout + export.stderr
    assert "schema_fields=10" in export.stdout
    assert "digest_rows=6" in export.stdout

    validate = subprocess.run(
        [sys.executable, "scripts/validate_health_ai_monitoring_digest_schema_20260708.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "PASS Health AI monitoring digest schema validation" in validate.stdout
