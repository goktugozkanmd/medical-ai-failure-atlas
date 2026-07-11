#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "docs" / "safetyguard_card_release_gate_smoke_20260708.json"
DEFAULT_CI_ARTIFACT = ROOT / "docs" / "safetyguard_card_release_gate_ci_artifact_20260708.json"
DEFAULT_OUT_MD = ROOT / "docs" / "SAFETYGUARD_CARD_RELEASE_NOTE_DRAFT_20260708.md"
DEFAULT_OUT_JSON = ROOT / "docs" / "safetyguard_card_release_note_draft_20260708.json"


def load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def build_release_note(manifest: dict[str, Any], ci_artifact: dict[str, Any]) -> dict[str, Any]:
    errors = release_blockers(manifest, ci_artifact)
    if errors:
        raise ValueError("; ".join(errors))
    prompt_count = int(manifest.get("prompt_count", 0))
    unsafe_count = int(manifest.get("unsafe_item_count", 0))
    source_gap_count = int(manifest.get("source_gap_item_count", 0))
    return {
        "artifact_id": "safetyguard_card_release_note_draft_20260708",
        "status": "local_release_note_draft",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_manifest": "docs/safetyguard_card_release_gate_smoke_20260708.json",
        "ci_artifact_manifest": "docs/safetyguard_card_release_gate_ci_artifact_20260708.json",
        "workflow_job": ci_artifact.get("job"),
        "artifact_name": ci_artifact.get("artifact_name"),
        "local_fake_server_used": manifest.get("local_fake_server_used") is True,
        "release_gate_passed": manifest.get("release_gate_passed") is True,
        "local_path_leak_scan_passed": manifest.get("local_path_leak_scan_passed") is True,
        "score_schema_version": manifest.get("score_schema_version"),
        "card_schema_version": manifest.get("card_schema_version"),
        "prompt_count": prompt_count,
        "score_item_count": int(manifest.get("score_item_count", 0)),
        "card_item_count": int(manifest.get("card_item_count", 0)),
        "unsafe_item_count": unsafe_count,
        "unsafe_rate": round(unsafe_count / prompt_count, 4) if prompt_count else 0,
        "source_gap_item_count": source_gap_count,
        "source_gap_rate": round(source_gap_count / prompt_count, 4) if prompt_count else 0,
        "contains_patient_data": False,
        "external_submission_allowed": False,
        "provider_api_call_allowed": False,
        "huggingface_publish_allowed": False,
        "agent_selected_physicians": False,
        "no_clinical_validation_claim": True,
        "no_model_ranking": True,
        "no_official_endorsement_claim": True,
        "blocked_actions": [
            "external publication",
            "Hugging Face publication",
            "provider API run",
            "model ranking claim",
            "clinical validation claim",
            "official endorsement claim",
        ],
    }


def release_blockers(manifest: dict[str, Any], ci_artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_manifest = {
        "status": "passed",
        "synthetic_only": True,
        "contains_patient_data": False,
        "external_submission_allowed": False,
        "local_fake_server_used": True,
        "release_gate_passed": True,
        "local_path_leak_scan_passed": True,
    }
    for key, expected in expected_manifest.items():
        if manifest.get(key) != expected:
            errors.append(f"manifest {key} must be {expected!r}")
    expected_ci = {
        "runs_only_when_dry_run": True,
        "external_submission_allowed": False,
        "provider_api_call_allowed": False,
        "huggingface_publish_allowed": False,
        "agent_selected_physicians": False,
    }
    for key, expected in expected_ci.items():
        if ci_artifact.get(key) != expected:
            errors.append(f"ci artifact {key} must be {expected!r}")
    if manifest.get("score_item_count") != manifest.get("prompt_count"):
        errors.append("manifest score_item_count must match prompt_count")
    if manifest.get("card_item_count") != manifest.get("prompt_count"):
        errors.append("manifest card_item_count must match prompt_count")
    flags = manifest.get("boundary_flags", {})
    if not isinstance(flags, dict) or flags.get("external_action_allowed") is not False:
        errors.append("manifest boundary external_action_allowed must be false")
    return errors


def render_markdown(note: dict[str, Any]) -> str:
    blocked = note.get("blocked_actions", [])
    lines = [
        "# SafetyGuard Card Release Note Draft",
        "",
        "Date: 2026 07 08",
        "",
        "Status: local draft only. Not published.",
        "",
        "## Source",
        "",
        f"Manifest: `{note['source_manifest']}`",
        "",
        f"CI artifact manifest: `{note['ci_artifact_manifest']}`",
        "",
        f"Workflow job: `{note['workflow_job']}`",
        "",
        f"Artifact name: `{note['artifact_name']}`",
        "",
        "## What This Shows",
        "",
        "The SafetyGuard card release gate can run in dry run CI mode, produce a real local score JSON through a local fake server, export transparency and HF evaluation card files, and keep external action blocked.",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "| --- | ---: |",
        f"| Prompt count | {note['prompt_count']} |",
        f"| Score item count | {note['score_item_count']} |",
        f"| Card item count | {note['card_item_count']} |",
        f"| Unsafe item count | {note['unsafe_item_count']} |",
        f"| Unsafe rate | {note['unsafe_rate']} |",
        f"| Source gap item count | {note['source_gap_item_count']} |",
        f"| Source gap rate | {note['source_gap_rate']} |",
        "",
        "## Release Gate State",
        "",
        "| Gate | Value |",
        "| --- | --- |",
        f"| Release gate passed | {str(note['release_gate_passed']).lower()} |",
        f"| Local path leak scan passed | {str(note['local_path_leak_scan_passed']).lower()} |",
        f"| Local fake server used | {str(note['local_fake_server_used']).lower()} |",
        f"| External submission allowed | {str(note['external_submission_allowed']).lower()} |",
        f"| Provider API call allowed | {str(note['provider_api_call_allowed']).lower()} |",
        f"| Hugging Face publish allowed | {str(note['huggingface_publish_allowed']).lower()} |",
        "",
        "## Still Blocked",
        "",
    ]
    for item in blocked:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "No external send, no public publication, no Hugging Face publish, no provider API run, no patient data, no physician selection, no clinical validation claim, no model ranking claim, and no official endorsement claim.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(note: dict[str, Any], *, out_md: Path, out_json: Path) -> None:
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_markdown(note), encoding="utf-8")
    out_json.write_text(json.dumps(note, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a local SafetyGuard release note draft from card gate artifacts.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--ci-artifact", type=Path, default=DEFAULT_CI_ARTIFACT)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    args = parser.parse_args()

    manifest = load_json_object(args.manifest)
    ci_artifact = load_json_object(args.ci_artifact)
    note = build_release_note(manifest, ci_artifact)
    write_outputs(note, out_md=args.out_md, out_json=args.out_json)
    print(f"Wrote release note draft Markdown: {args.out_md}")
    print(f"Wrote release note draft JSON: {args.out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
