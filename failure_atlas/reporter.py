from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from failure_atlas.data import PathLike
from failure_atlas.scorer import SCORE_DIMENSIONS


def load_score_file(path: PathLike) -> dict[str, Any]:
    target = Path(path)
    with target.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise ValueError(f"{target} must be a score JSON object with items")
    return data


def write_score_json(scores: dict[str, Any], output_path: PathLike) -> Path:
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(scores, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def write_markdown_report(scores: dict[str, Any], output_path: PathLike) -> Path:
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_markdown_report(scores), encoding="utf-8")
    return target


def build_markdown_report(scores: dict[str, Any]) -> str:
    model_name = str(scores.get("model_name", "unknown"))
    scored_at = str(scores.get("scored_at", datetime.now(timezone.utc).isoformat()))
    aggregates = scores.get("aggregates", {})
    mean_scores = aggregates.get("mean_scores", {})
    label_counts = aggregates.get("final_label_counts", {})
    gate_counts = aggregates.get("safety_gate_counts", {})
    items = scores.get("items", [])
    lines = [
        "# Failure Atlas benchmark report",
        "",
        f"Model: `{model_name}`",
        "",
        f"Date: `{scored_at}`",
        "",
        "Boundary: synthetic benchmark output only. Not clinical advice, validation, ranking, or certification.",
        "",
        "## Aggregate scores",
        "",
        "| Dimension | Mean score |",
        "| --- | ---: |",
    ]
    for dimension in SCORE_DIMENSIONS:
        lines.append(f"| {dimension} | {float(mean_scores.get(dimension, 0.0)):.3f} |")
    lines.extend(["", "## Label counts", "", "| Label | Rows |", "| --- | ---: |"])
    for label, count in sorted(label_counts.items()):
        lines.append(f"| {label} | {count} |")
    lines.extend(["", "## Safety gate breakdown", "", "| Gate | Rows |", "| --- | ---: |"])
    if gate_counts:
        for gate, count in sorted(gate_counts.items()):
            lines.append(f"| {gate} | {count} |")
    else:
        lines.append("| none | 0 |")
    lines.extend(["", "## Per category breakdown", ""])
    lines.extend(_category_lines(items))
    lines.extend(["", "## Failure analysis", ""])
    lines.extend(_failure_lines(items))
    return "\n".join(lines) + "\n"


def write_csv_summary(score_files: list[PathLike], output_path: PathLike) -> Path:
    rows = [summary_row(load_score_file(path)) for path in score_files]
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "model_name",
        "scored_at",
        "item_count",
        "mean_safety",
        "mean_accuracy",
        "mean_source_transparency",
        "mean_refusal_appropriateness",
        "mean_clinical_grounding",
        "unsafe",
        "needs_revision_before_clinical_use",
        "clinically_usable_with_caution",
        "clinically_useful",
    ]
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return target


def write_report_bundle(scores: dict[str, Any], output_dir: PathLike, stem: str | None = None) -> dict[str, Path]:
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    name = stem or _safe_name(str(scores.get("model_name", "model")))
    json_path = write_score_json(scores, target_dir / f"{name}_scores.json")
    markdown_path = write_markdown_report(scores, target_dir / f"{name}_report.md")
    csv_path = write_csv_summary([json_path], target_dir / f"{name}_summary.csv")
    return {"json": json_path, "markdown": markdown_path, "csv": csv_path}


def write_comparison_markdown(score_files: list[PathLike], output_path: PathLike) -> Path:
    rows = [summary_row(load_score_file(path)) for path in score_files]
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Failure Atlas model comparison",
        "",
        "Boundary: comparison is for synthetic benchmark review only and is not a model ranking or safety certification.",
        "",
        "| Model | Rows | Safety | Accuracy | Source transparency | Refusal | Clinical grounding | Unsafe | Needs revision |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {model_name} | {item_count} | {mean_safety} | {mean_accuracy} | {mean_source_transparency} | "
            "{mean_refusal_appropriateness} | {mean_clinical_grounding} | {unsafe} | {needs_revision_before_clinical_use} |".format(
                **row
            )
        )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def summary_row(scores: dict[str, Any]) -> dict[str, str]:
    aggregates = scores.get("aggregates", {})
    means = aggregates.get("mean_scores", {})
    labels = aggregates.get("final_label_counts", {})
    row = {
        "model_name": str(scores.get("model_name", "unknown")),
        "scored_at": str(scores.get("scored_at", "")),
        "item_count": str(aggregates.get("item_count", len(scores.get("items", [])))),
    }
    for dimension in SCORE_DIMENSIONS:
        row[f"mean_{dimension}"] = f"{float(means.get(dimension, 0.0)):.3f}"
    for label in (
        "unsafe",
        "needs_revision_before_clinical_use",
        "clinically_usable_with_caution",
        "clinically_useful",
    ):
        row[label] = str(labels.get(label, 0))
    return row


def _category_lines(items: list[dict[str, Any]]) -> list[str]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[_category_for(str(item.get("scenario_id", "")))].append(item)
    lines = ["| Category | Rows | Mean safety | Unsafe rows |", "| --- | ---: | ---: | ---: |"]
    for category, rows in sorted(grouped.items()):
        safety = sum(int(row["scores"]["safety"]) for row in rows) / len(rows)
        unsafe = sum(1 for row in rows if row.get("final_label") == "unsafe")
        lines.append(f"| {category} | {len(rows)} | {safety:.3f} | {unsafe} |")
    if not grouped:
        lines.append("| none | 0 | 0.000 | 0 |")
    return lines


def _failure_lines(items: list[dict[str, Any]]) -> list[str]:
    failures = [
        item
        for item in items
        if item.get("final_label") in {"unsafe", "needs_revision_before_clinical_use"}
    ]
    failures.sort(key=lambda item: (int(item["scores"]["safety"]), str(item.get("scenario_id", ""))))
    if not failures:
        return ["No unsafe or needs revision rows were identified by the selected scoring method."]
    lines: list[str] = []
    for item in failures[:20]:
        reasons = item.get("reasons", [])
        reason = reasons[0] if reasons else "No reason recorded."
        lines.append(
            f"- `{item.get('scenario_id', '')}`: {item.get('final_label', '')}; "
            f"safety {item['scores']['safety']}. {reason}"
        )
    return lines


def _category_for(scenario_id: str) -> str:
    if scenario_id.startswith("H"):
        return "hard"
    if scenario_id.startswith("S"):
        return "scale"
    if scenario_id.startswith("M"):
        return "v1"
    if scenario_id.startswith("TR"):
        return "turkish"
    return "other"


def _safe_name(value: str) -> str:
    return "".join(character if character.isalnum() or character in {"_", "-", "."} else "_" for character in value).strip("._") or "model"
