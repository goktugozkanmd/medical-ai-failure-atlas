#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEADERBOARD = ROOT / "leaderboard" / "submissions.json"
PROMOTION_GATE = ROOT / "docs" / "model_run_promotion_gate_20260708.json"
JSON_PATH = ROOT / "docs" / "local_leaderboard_draft_preview_20260708.json"
MD_PATH = ROOT / "docs" / "LOCAL_LEADERBOARD_DRAFT_PREVIEW_20260708.md"


def main() -> int:
    leaderboard_payload = read_json(LEADERBOARD)
    promotion_gate = read_json(PROMOTION_GATE)
    submissions = leaderboard_payload.get("submissions", [])
    if not isinstance(submissions, list):
        raise TypeError("leaderboard submissions must be a list")

    current_by_name = {str(row.get("model_name")): row for row in submissions if isinstance(row, dict)}
    draft_rows = []
    for promoted in promotion_gate.get("models", []):
        if not isinstance(promoted, dict):
            continue
        model_name = str(promoted["model_name"])
        current = current_by_name.get(model_name)
        if not isinstance(current, dict):
            raise ValueError(f"Promotion gate model not found in leaderboard: {model_name}")
        score_path = ROOT / str(promoted["rule_scores"])
        score_payload = read_json(score_path)
        draft_rows.append(build_draft_row(current, promoted, score_payload))

    manifest = {
        "artifact_id": "local_leaderboard_draft_preview_20260708",
        "status": "local_draft_preview_not_public_update",
        "created_date": "2026-07-08",
        "source_leaderboard": "leaderboard/submissions.json",
        "source_leaderboard_sha256": sha256(LEADERBOARD),
        "source_promotion_gate": "docs/model_run_promotion_gate_20260708.json",
        "external_action_allowed": False,
        "provider_api_call_allowed": False,
        "automation_started": False,
        "public_leaderboard_modified": False,
        "new_cases_added": False,
        "agent_selected_physicians": False,
        "contains_patient_data": False,
        "no_clinical_validation_claim": True,
        "no_model_ranking": True,
        "no_official_compatibility_claim": True,
        "draft_scope": {
            "purpose": "show how existing local 30 row artifacts could close part of the public leaderboard prompt count gap",
            "models_in_preview": len(draft_rows),
            "public_rows_closed_by_local_artifacts": sum(row["local_rows_closing_public_gap"] for row in draft_rows),
            "provider_generation_rows_used": 0,
            "public_write_allowed": False,
        },
        "draft_rows": draft_rows,
        "blocked_actions": [
            "write_leaderboard_submissions_json",
            "publish_preview_without_user_approval",
            "rank_models_from_preview",
            "claim_clinical_validation",
            "start_provider_api_calls",
            "add_new_cases",
        ],
        "next_safe_actions": [
            "review preview row wording and score derivation",
            "if approved later, create a separate public leaderboard update patch",
            "keep remaining provider generation gap blocked until explicit approval",
        ],
    }
    JSON_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(manifest), encoding="utf-8")
    print(f"Wrote {JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")
    print(f"models_in_preview={len(draft_rows)}")
    print(f"public_rows_closed_by_local_artifacts={manifest['draft_scope']['public_rows_closed_by_local_artifacts']}")
    print("public_leaderboard_modified=false")
    return 0


def build_draft_row(current: dict[str, Any], promoted: dict[str, Any], score_payload: dict[str, Any]) -> dict[str, Any]:
    aggregates = score_payload.get("aggregates", {})
    mean_scores = aggregates.get("mean_scores", {})
    if not isinstance(mean_scores, dict):
        raise TypeError("score aggregates mean_scores must be an object")
    draft_scores = {
        "safety_score": to_percent(mean_scores.get("safety")),
        "source_support_score": to_percent(mean_scores.get("source_transparency")),
        "clinical_boundary_score": to_percent(
            mean(
                [
                    mean_scores.get("refusal_appropriateness"),
                    mean_scores.get("clinical_grounding"),
                ]
            )
        ),
    }
    return {
        "model_name": promoted["model_name"],
        "current_submission_id": current.get("id"),
        "current_public_prompt_count": promoted["public_prompt_count_before_gate"],
        "draft_prompt_count": promoted["target_prompt_count"],
        "local_rows_closing_public_gap": promoted["normalization_gap_closed_locally"],
        "provider_generation_rows_used": 0,
        "current_public_scores": current.get("benchmark_scores", {}),
        "draft_scores_from_local_rule_scores": draft_scores,
        "score_file": promoted["rule_scores"],
        "source_raw": promoted["source_raw"],
        "final_label_counts": promoted.get("final_label_counts", {}),
        "safety_gate_counts": promoted.get("safety_gate_counts", {}),
        "draft_status": "local_preview_only_not_written_to_public_leaderboard",
    }


def to_percent(value: Any) -> float:
    if not isinstance(value, (int, float)):
        raise TypeError(f"score value must be numeric, got {value!r}")
    return round(float(value) * 20.0, 1)


def mean(values: list[Any]) -> float:
    numeric = [float(value) for value in values if isinstance(value, (int, float))]
    if len(numeric) != len(values):
        raise TypeError(f"mean values must be numeric: {values!r}")
    return sum(numeric) / len(numeric)


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Local Leaderboard Draft Preview",
        "",
        "Date: 2026 07 08",
        "",
        "Status: local draft preview only. The public leaderboard file was not changed.",
        "",
        "## Boundary",
        "",
        "No external send, no provider API call, no public leaderboard write, no new case addition, no patient data, no physician selection, no clinical validation claim, no official compatibility claim, and no model ranking.",
        "",
        "## Scope",
        "",
        f"- Models in preview: {manifest['draft_scope']['models_in_preview']}.",
        f"- Public rows closed by existing local artifacts: {manifest['draft_scope']['public_rows_closed_by_local_artifacts']}.",
        f"- Provider generation rows used: {manifest['draft_scope']['provider_generation_rows_used']}.",
        f"- Source leaderboard SHA256: `{manifest['source_leaderboard_sha256']}`.",
        "",
        "## Draft Rows",
        "",
        "| Model | Current public rows | Draft rows | Local rows closing gap | Draft safety | Draft source support | Draft clinical boundary | Status |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in manifest["draft_rows"]:
        scores = row["draft_scores_from_local_rule_scores"]
        lines.append(
            "| {model_name} | {current_public_prompt_count} | {draft_prompt_count} | "
            "{local_rows_closing_public_gap} | {safety_score:.1f} | {source_support_score:.1f} | "
            "{clinical_boundary_score:.1f} | {draft_status} |".format(
                model_name=row["model_name"],
                current_public_prompt_count=row["current_public_prompt_count"],
                draft_prompt_count=row["draft_prompt_count"],
                local_rows_closing_public_gap=row["local_rows_closing_public_gap"],
                safety_score=scores["safety_score"],
                source_support_score=scores["source_support_score"],
                clinical_boundary_score=scores["clinical_boundary_score"],
                draft_status=row["draft_status"],
            )
        )
    lines.extend(
        [
            "",
            "## Next",
            "",
            "1. Review score derivation and row wording.",
            "2. If the user later approves, create a separate public leaderboard update patch.",
            "3. Keep remaining provider generation rows blocked until explicit approval.",
            "",
            "## Validation",
            "",
            "Run:",
            "",
            "```bash",
            "make local_leaderboard_draft_preview_20260708",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path.relative_to(ROOT)} must be a JSON object")
    return payload


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
