from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_medhelm_three_case_packet_exports_expected_cases() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/export_medhelm_three_case_packet.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    packet_path = ROOT / "docs" / "medhelm_three_case_upstream_packet_v0_1.json"
    markdown_path = ROOT / "docs" / "MEDHELM_THREE_CASE_UPSTREAM_PACKET_V0_1.md"
    assert packet_path.exists()
    assert markdown_path.exists()

    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    assert packet["schema_version"] == "medfailbench_medhelm_three_case_packet_v0_1"
    assert packet["status"] == "draft_not_posted_not_medhelm_endorsed"
    assert packet["case_count"] == 3
    assert packet["boundaries"]["synthetic_only"] is True
    assert packet["boundaries"]["patient_data_used"] is False
    assert packet["boundaries"]["clinical_use_allowed"] is False

    case_ids = [case["source_case_id"] for case in packet["cases"]]
    assert case_ids == ["MFB_PANEL_004", "MFB_PANEL_005", "MFB_PANEL_010"]
    assert {case["candidate_safety_gate"] for case in packet["cases"]} == {
        "unsafe_remote_dosing",
        "missed_urgent_escalation",
    }


def test_medhelm_three_case_packet_blocks_overclaim_phrases() -> None:
    for path in (
        ROOT / "docs" / "medhelm_three_case_upstream_packet_v0_1.json",
        ROOT / "docs" / "MEDHELM_THREE_CASE_UPSTREAM_PACKET_V0_1.md",
    ):
        text = path.read_text(encoding="utf-8")
        assert "MedHELM compatible" not in text
        assert "clinically validated" not in text.lower()
