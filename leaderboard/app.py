#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
from collections import Counter
from pathlib import Path

try:
    import gradio as gr
except ImportError:  # Allows syntax and data helper checks without Gradio installed.
    gr = None


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT / "leaderboard" / "synthetic_report_template_v0_1.tsv"

DISPLAY_COLUMNS = [
    "run_id",
    "model_label",
    "scenario_set",
    "sourcecheckup_gate",
    "failure_atlas_pattern",
    "clinician_review_state",
    "release_gate",
    "public_summary",
]

BOUNDARY_NOTE = (
    "This preview uses synthetic rows only. It is not clinical advice, not a "
    "clinical validation table, not a model ranking, and not a model safety claim."
)


def results_path() -> Path:
    configured = os.getenv("FAILURE_ATLAS_LEADERBOARD_TSV")
    if configured:
        candidate = Path(configured)
        return candidate if candidate.is_absolute() else ROOT / candidate
    return DEFAULT_RESULTS


def load_rows(path: Path | None = None) -> list[dict[str, str]]:
    target = path or results_path()
    with target.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def unique_values(rows: list[dict[str, str]], column: str) -> list[str]:
    values = sorted({row.get(column, "").strip() for row in rows if row.get(column, "").strip()})
    return ["All", *values]


def filter_rows(
    rows: list[dict[str, str]],
    sourcecheckup_gate: str,
    clinician_review_state: str,
    release_gate: str,
    query: str,
) -> list[dict[str, str]]:
    query = query.strip().lower()
    filtered: list[dict[str, str]] = []
    for row in rows:
        if sourcecheckup_gate != "All" and row.get("sourcecheckup_gate") != sourcecheckup_gate:
            continue
        if clinician_review_state != "All" and row.get("clinician_review_state") != clinician_review_state:
            continue
        if release_gate != "All" and row.get("release_gate") != release_gate:
            continue
        searchable = " ".join(row.get(column, "") for column in DISPLAY_COLUMNS).lower()
        if query and query not in searchable:
            continue
        filtered.append(row)
    return filtered


def rows_to_table(rows: list[dict[str, str]]) -> list[list[str]]:
    return [[row.get(column, "") for column in DISPLAY_COLUMNS] for row in rows]


def summary_markdown(rows: list[dict[str, str]]) -> str:
    source_counts = Counter(row.get("sourcecheckup_gate", "missing") for row in rows)
    review_counts = Counter(row.get("clinician_review_state", "missing") for row in rows)
    release_counts = Counter(row.get("release_gate", "missing") for row in rows)
    return "\n".join(
        [
            f"Rows shown: **{len(rows)}**",
            "",
            f"SourceCheckup gates: `{dict(source_counts)}`",
            "",
            f"Clinician review states: `{dict(review_counts)}`",
            "",
            f"Release gates: `{dict(release_counts)}`",
        ]
    )


def update_table(
    sourcecheckup_gate: str,
    clinician_review_state: str,
    release_gate: str,
    query: str,
) -> tuple[list[list[str]], str]:
    rows = filter_rows(load_rows(), sourcecheckup_gate, clinician_review_state, release_gate, query)
    return rows_to_table(rows), summary_markdown(rows)


def build_demo():
    if gr is None:
        raise RuntimeError("Install Gradio with: python3 -m pip install -r leaderboard/requirements.txt")

    rows = load_rows()
    with gr.Blocks(title="Medical AI Failure Atlas Leaderboard") as demo:
        gr.Markdown("# Medical AI Failure Atlas Leaderboard")
        gr.Markdown(BOUNDARY_NOTE)
        with gr.Row():
            sourcecheckup_gate = gr.Dropdown(
                choices=unique_values(rows, "sourcecheckup_gate"),
                value="All",
                label="SourceCheckup gate",
            )
            clinician_review_state = gr.Dropdown(
                choices=unique_values(rows, "clinician_review_state"),
                value="All",
                label="Clinician review state",
            )
            release_gate = gr.Dropdown(
                choices=unique_values(rows, "release_gate"),
                value="All",
                label="Release gate",
            )
        query = gr.Textbox(label="Search", placeholder="Model label, scenario set, or failure pattern")
        table = gr.Dataframe(
            headers=DISPLAY_COLUMNS,
            value=rows_to_table(rows),
            datatype=["str"] * len(DISPLAY_COLUMNS),
            interactive=False,
            wrap=True,
        )
        summary = gr.Markdown(summary_markdown(rows))

        inputs = [sourcecheckup_gate, clinician_review_state, release_gate, query]
        for control in inputs:
            control.change(update_table, inputs=inputs, outputs=[table, summary])

    return demo


demo = build_demo() if gr is not None else None


if __name__ == "__main__":
    if demo is None:
        raise SystemExit("Install Gradio with: python3 -m pip install -r leaderboard/requirements.txt")
    demo.launch()
