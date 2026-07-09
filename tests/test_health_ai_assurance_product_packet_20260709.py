from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_health_ai_assurance_product_packet_exporter_and_validator_pass() -> None:
    export = subprocess.run(
        [sys.executable, "scripts/export_health_ai_assurance_product_packet_20260709.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert export.returncode == 0, export.stdout + export.stderr
    assert "phase=P12" in export.stdout
    assert "source_artifacts=12" in export.stdout
    assert "feedback_loop_phases=3" in export.stdout

    validate = subprocess.run(
        [sys.executable, "scripts/validate_health_ai_assurance_product_packet_20260709.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "PASS health AI assurance product packet validation" in validate.stdout
    assert "phase=P12" in validate.stdout
    assert "feedback_loop_phases=3" in validate.stdout
    assert "external_action_allowed=false" in validate.stdout
