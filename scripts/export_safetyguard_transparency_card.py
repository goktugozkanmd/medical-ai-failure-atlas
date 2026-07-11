#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_scores(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise ValueError(f"{path} must be a Failure Atlas score JSON object with items")
    return payload


def build_card(scores: dict[str, Any], *, score_file: Path) -> dict[str, Any]:
    items = [item for item in scores.get("items", []) if isinstance(item, dict)]
    unsafe_items = [
        item
        for item in items
        if item.get("final_label") == "unsafe"
        or _score_value(item, "safety") <= 2
    ]
    source_gap_items = [
        item
        for item in items
        if _score_value(item, "source_transparency") <= 2
    ]
    gate_counts: dict[str, int] = {}
    for item in items:
        gates = item.get("safety_gates", {})
        if isinstance(gates, dict):
            for gate in gates:
                gate_counts[str(gate)] = gate_counts.get(str(gate), 0) + 1
    return {
        "schema_version": "safetyguard_transparency_card_v0_1",
        "card_id": f"safetyguard_transparency_card_{_safe_name(str(scores.get('model_name', 'model')))}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_score_file": str(score_file),
        "model_name": str(scores.get("model_name", "unknown")),
        "scoring_method": str(scores.get("method", "unknown")),
        "item_count": len(items),
        "unsafe_item_count": len(unsafe_items),
        "source_gap_item_count": len(source_gap_items),
        "safety_gate_counts": gate_counts,
        "boundary_flags": {
            "synthetic_or_manual_review_only": True,
            "contains_patient_data": False,
            "not_clinical_advice": True,
            "not_clinical_validation": True,
            "not_model_ranking": True,
            "not_regulatory_compliance": True,
            "not_official_endorsement": True,
            "external_action_allowed": False,
        },
        "review_state": {
            "human_review_recorded": False,
            "external_use_blocked_until_fresh_audit": True,
            "source_support_refresh_required_for_external_claims": True,
        },
        "worst_case_items": [
            {
                "scenario_id": str(item.get("scenario_id", "")),
                "final_label": str(item.get("final_label", "")),
                "safety": _score_value(item, "safety"),
                "source_transparency": _score_value(item, "source_transparency"),
                "first_reason": _first_reason(item),
            }
            for item in sorted(items, key=lambda row: (_score_value(row, "safety"), str(row.get("scenario_id", ""))))[:10]
        ],
    }


def render_markdown(card: dict[str, Any]) -> str:
    flags = card["boundary_flags"]
    lines = [
        "# SafetyGuard Transparency Card v0.1",
        "",
        f"Model: `{card['model_name']}`",
        "",
        f"Generated: `{card['generated_at']}`",
        "",
        "Boundary: synthetic or manually pasted review only. Not clinical advice, clinical validation, model ranking, regulatory compliance, certification, or official endorsement.",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "| --- | ---: |",
        f"| Items | {card['item_count']} |",
        f"| Unsafe items | {card['unsafe_item_count']} |",
        f"| Source gap items | {card['source_gap_item_count']} |",
        "",
        "## Boundary Flags",
        "",
        "| Flag | Value |",
        "| --- | --- |",
    ]
    for key, value in flags.items():
        lines.append(f"| {key} | {str(value).lower()} |")
    lines.extend(["", "## Safety Gates", "", "| Gate | Rows |", "| --- | ---: |"])
    gate_counts = card.get("safety_gate_counts", {})
    if gate_counts:
        for gate, count in sorted(gate_counts.items()):
            lines.append(f"| {gate} | {count} |")
    else:
        lines.append("| none | 0 |")
    lines.extend(
        [
            "",
            "## Worst Case Items",
            "",
            "| Scenario | Label | Safety | Source | First reason |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for item in card.get("worst_case_items", []):
        lines.append(
            "| {scenario_id} | {final_label} | {safety} | {source_transparency} | {first_reason} |".format(
                **{key: _md_cell(str(value)) for key, value in item.items()}
            )
        )
    lines.extend(
        [
            "",
            "## External Gate",
            "",
            "External use is blocked until the target text, target venue, source support, audit state, and owner approval are all refreshed.",
            "",
        ]
    )
    return "\n".join(lines)


def build_hf_evaluation_fields(card: dict[str, Any]) -> dict[str, Any]:
    item_count = int(card.get("item_count", 0))
    unsafe_count = int(card.get("unsafe_item_count", 0))
    source_gap_count = int(card.get("source_gap_item_count", 0))
    return {
        "schema_version": "safetyguard_hf_evaluation_card_fields_v0_1",
        "model_name": card.get("model_name", "unknown"),
        "prompt_set_path": "safetyguard/data/medfailbench_prompts_v0_2.jsonl",
        "scoring_method": card.get("scoring_method", "unknown"),
        "item_count": item_count,
        "unsafe_item_count": unsafe_count,
        "unsafe_rate": round(unsafe_count / item_count, 4) if item_count else 0,
        "source_gap_item_count": source_gap_count,
        "source_gap_rate": round(source_gap_count / item_count, 4) if item_count else 0,
        "human_review_state": "not recorded in this card",
        "external_audit_state": "blocked until fresh audit and owner approval",
        "worst_case_items": card.get("worst_case_items", []),
        "boundary_flags": card.get("boundary_flags", {}),
    }


def render_hf_evaluation_card(card: dict[str, Any]) -> str:
    fields = build_hf_evaluation_fields(card)
    lines = [
        "# MedFailBench Safety Layer Evaluation Card v0.1",
        "",
        "Status: local generated card. Not published to Hugging Face.",
        "",
        f"Model: `{fields['model_name']}`",
        "",
        f"Prompt set: `{fields['prompt_set_path']}`",
        "",
        f"Scoring method: `{fields['scoring_method']}`",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "| --- | ---: |",
        f"| Items | {fields['item_count']} |",
        f"| Unsafe items | {fields['unsafe_item_count']} |",
        f"| Unsafe rate | {fields['unsafe_rate']} |",
        f"| Source gap items | {fields['source_gap_item_count']} |",
        f"| Source gap rate | {fields['source_gap_rate']} |",
        "",
        "## Review State",
        "",
        f"Human review: {fields['human_review_state']}.",
        "",
        f"External audit: {fields['external_audit_state']}.",
        "",
        "## Boundary",
        "",
        "Synthetic prompts only. Not clinical advice, clinical validation, model ranking, regulatory compliance, certification, or official endorsement.",
        "",
        "## Worst Case Items",
        "",
        "| Scenario | Label | Safety | Source | First reason |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for item in fields.get("worst_case_items", []):
        lines.append(
            "| {scenario_id} | {final_label} | {safety} | {source_transparency} | {first_reason} |".format(
                **{key: _md_cell(str(value)) for key, value in item.items()}
            )
        )
    if not fields.get("worst_case_items"):
        lines.append("| none | none | 0 | 0 | none |")
    lines.append("")
    return "\n".join(lines)


def write_card(card: dict[str, Any], *, out_json: Path, out_md: Path, out_hf_card: Path | None = None) -> None:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_md.write_text(render_markdown(card), encoding="utf-8")
    if out_hf_card is not None:
        out_hf_card.parent.mkdir(parents=True, exist_ok=True)
        out_hf_card.write_text(render_hf_evaluation_card(card), encoding="utf-8")


def _score_value(item: dict[str, Any], key: str) -> int:
    scores = item.get("scores", {})
    if isinstance(scores, dict):
        try:
            return int(scores.get(key, 0))
        except (TypeError, ValueError):
            return 0
    return 0


def _first_reason(item: dict[str, Any]) -> str:
    reasons = item.get("reasons", [])
    if isinstance(reasons, list) and reasons:
        return str(reasons[0])
    return ""


def _safe_name(value: str) -> str:
    safe = "".join(character if character.isalnum() or character in {"_", "-", "."} else "_" for character in value)
    return safe.strip("._") or "model"


def _md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a SafetyGuard transparency card from a score JSON.")
    parser.add_argument("--score-file", required=True, help="Failure Atlas score JSON file")
    parser.add_argument("--out-json", default=str(ROOT / "outputs" / "safetyguard_transparency_card_v0_1.json"))
    parser.add_argument("--out-md", default=str(ROOT / "outputs" / "SAFETYGUARD_TRANSPARENCY_CARD_V0_1.md"))
    parser.add_argument("--out-hf-card", help="Optional Hugging Face evaluation card Markdown output")
    args = parser.parse_args()

    score_file = Path(args.score_file)
    scores = load_scores(score_file)
    card = build_card(scores, score_file=score_file)
    write_card(
        card,
        out_json=Path(args.out_json),
        out_md=Path(args.out_md),
        out_hf_card=Path(args.out_hf_card) if args.out_hf_card else None,
    )
    print(f"Wrote transparency card JSON: {Path(args.out_json)}")
    print(f"Wrote transparency card Markdown: {Path(args.out_md)}")
    if args.out_hf_card:
        print(f"Wrote HF evaluation card Markdown: {Path(args.out_hf_card)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
