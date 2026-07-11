from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_safetyguard_card_release_gate_smoke_passes(tmp_path: Path) -> None:
    output_dir = ROOT / "build" / "pytest_safetyguard_card_release_gate"
    manifest = tmp_path / "manifest.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/smoke_safetyguard_card_release_gate_20260708.py",
            "--output-dir",
            str(output_dir),
            "--manifest",
            str(manifest),
            "--limit",
            "2",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["release_gate_passed"] is True
    assert payload["local_path_leak_scan_passed"] is True
    assert payload["external_submission_allowed"] is False
    assert payload["score_schema_version"] == "failure_atlas_scores_v0_1"
    assert payload["score_item_count"] == 2
    assert payload["card_item_count"] == 2
    assert (output_dir / "release-gate-demo-model_scores.json").exists()
    assert (output_dir / "HF_EVALUATION_CARD_MEDFAILBENCH_SAFETY_LAYER_V0_1.md").exists()
