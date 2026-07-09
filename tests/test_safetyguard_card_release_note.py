from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.export_safetyguard_card_release_note_20260708 import build_release_note, release_blockers, render_markdown


ROOT = Path(__file__).resolve().parents[1]


def sample_manifest() -> dict:
    return {
        "status": "passed",
        "synthetic_only": True,
        "contains_patient_data": False,
        "external_submission_allowed": False,
        "local_fake_server_used": True,
        "release_gate_passed": True,
        "local_path_leak_scan_passed": True,
        "prompt_count": 2,
        "score_item_count": 2,
        "card_item_count": 2,
        "unsafe_item_count": 0,
        "source_gap_item_count": 0,
        "score_schema_version": "failure_atlas_scores_v0_1",
        "card_schema_version": "safetyguard_transparency_card_v0_1",
        "boundary_flags": {"external_action_allowed": False},
    }


def sample_ci_artifact() -> dict:
    return {
        "job": "safetyguard-card-release-gate",
        "artifact_name": "safetyguard-card-release-gate",
        "runs_only_when_dry_run": True,
        "external_submission_allowed": False,
        "provider_api_call_allowed": False,
        "huggingface_publish_allowed": False,
        "agent_selected_physicians": False,
    }


def test_release_note_builder_keeps_external_actions_blocked() -> None:
    note = build_release_note(sample_manifest(), sample_ci_artifact())

    assert note["status"] == "local_release_note_draft"
    assert note["release_gate_passed"] is True
    assert note["external_submission_allowed"] is False
    assert note["provider_api_call_allowed"] is False
    assert note["huggingface_publish_allowed"] is False
    assert note["prompt_count"] == 2
    assert note["unsafe_rate"] == 0
    text = render_markdown(note)
    assert "local draft only" in text
    assert "No external send" in text


def test_release_note_builder_blocks_external_action_state() -> None:
    manifest = sample_manifest()
    manifest["external_submission_allowed"] = True

    errors = release_blockers(manifest, sample_ci_artifact())

    assert errors
    assert any("external_submission_allowed" in error for error in errors)


def test_release_note_cli_writes_outputs(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    ci_artifact = tmp_path / "ci.json"
    out_md = tmp_path / "note.md"
    out_json = tmp_path / "note.json"
    manifest.write_text(json.dumps(sample_manifest()) + "\n", encoding="utf-8")
    ci_artifact.write_text(json.dumps(sample_ci_artifact()) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/export_safetyguard_card_release_note_20260708.py",
            "--manifest",
            str(manifest),
            "--ci-artifact",
            str(ci_artifact),
            "--out-md",
            str(out_md),
            "--out-json",
            str(out_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert out_md.exists()
    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload["artifact_id"] == "safetyguard_card_release_note_draft_20260708"
