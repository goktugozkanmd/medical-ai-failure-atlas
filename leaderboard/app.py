#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import threading
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    import gradio as gr
except ImportError:  # Allows syntax and data helper checks without Gradio installed.
    gr = None

try:
    from leaderboard.policy import (
        FORBIDDEN_PUBLIC_CLAIM_PHRASES,
        MAX_HF_LINK_LENGTH,
        MAX_MODEL_NAME_LENGTH,
        MAX_NOTES_LENGTH,
        MAX_SUBMISSIONS,
        coerce_score,
        forbidden_public_claim_phrase,
        normalize_huggingface_model_url,
    )
except ImportError:  # Supports copying leaderboard/app.py and leaderboard/policy.py to a Space root.
    from policy import (  # type: ignore[no-redef]
        FORBIDDEN_PUBLIC_CLAIM_PHRASES,
        MAX_HF_LINK_LENGTH,
        MAX_MODEL_NAME_LENGTH,
        MAX_NOTES_LENGTH,
        MAX_SUBMISSIONS,
        coerce_score,
        forbidden_public_claim_phrase,
        normalize_huggingface_model_url,
    )


APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent if APP_DIR.name == "leaderboard" else APP_DIR
LEADERBOARD_DIR = ROOT / "leaderboard" if (ROOT / "leaderboard").exists() else APP_DIR
DEFAULT_RESULTS = LEADERBOARD_DIR / "synthetic_report_template_v0_1.tsv"
DEFAULT_SUBMISSIONS = LEADERBOARD_DIR / "submissions.json"
GITHUB_REPO_URL = os.getenv(
    "FAILURE_ATLAS_GITHUB_REPO_URL",
    "https://github.com/goktugozkanmd/medical-ai-failure-atlas",
).rstrip("/")
CONTRIBUTION_GUIDE_URL = os.getenv(
    "FAILURE_ATLAS_CONTRIBUTION_GUIDE_URL",
    f"{GITHUB_REPO_URL}/blob/main/CONTRIBUTING.md",
).rstrip("/")
STORE_LOCK = threading.Lock()

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

SUBMISSION_COLUMNS = [
    "model_name",
    "huggingface_link",
    "safety_score",
    "source_support_score",
    "clinical_boundary_score",
    "status",
    "submitted_at",
]

BOUNDARY_NOTE = (
    "This preview uses synthetic rows only. It is not clinical advice, not a "
    "clinical validation table, not a model ranking, and not a model safety claim."
)

SUBMISSION_BOUNDARY_NOTE = (
    "Submitted rows are contributor supplied and pending review. Scores shown here "
    "are not clinical validation, source truth certification, a model ranking, or a "
    "clinical use claim. Rows are ordered by latest submission time, not by score."
)


def configured_hf_timeout_seconds() -> float:
    try:
        return float(os.getenv("FAILURE_ATLAS_HF_TIMEOUT_SECONDS", "5"))
    except ValueError:
        return 5.0


HF_TIMEOUT_SECONDS = configured_hf_timeout_seconds()


def results_path() -> Path:
    configured = os.getenv("FAILURE_ATLAS_LEADERBOARD_TSV")
    if configured:
        candidate = Path(configured)
        return candidate if candidate.is_absolute() else ROOT / candidate
    return DEFAULT_RESULTS


def submissions_path() -> Path:
    configured = os.getenv("FAILURE_ATLAS_SUBMISSIONS_JSON")
    if configured:
        candidate = Path(configured)
        return candidate if candidate.is_absolute() else ROOT / candidate
    return DEFAULT_SUBMISSIONS


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


def current_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def empty_submission_store() -> dict[str, object]:
    return {"last_updated": current_utc_iso(), "submissions": []}


def load_submission_store(path: Path | None = None) -> dict[str, object]:
    target = path or submissions_path()
    if not target.exists():
        return empty_submission_store()

    with target.open(encoding="utf-8") as handle:
        data = json.load(handle)

    if isinstance(data, list):
        return {"last_updated": None, "submissions": data}
    if not isinstance(data, dict):
        raise ValueError(f"Submission store must contain a JSON object: {target}")

    submissions = data.get("submissions", [])
    if not isinstance(submissions, list):
        raise ValueError(f"Submission store submissions must be a list: {target}")

    return {
        "last_updated": data.get("last_updated"),
        "submissions": [row for row in submissions if isinstance(row, dict)],
    }


def save_submission_store(store: dict[str, object], path: Path | None = None) -> None:
    target = path or submissions_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(f"{target.suffix}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(store, handle, indent=2, sort_keys=True)
        handle.write("\n")
    temporary.replace(target)


def format_score(value: object) -> str:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return ""
    return f"{score:.2f}".rstrip("0").rstrip(".")


def submissions_to_table(submissions: list[dict[str, object]]) -> list[list[str]]:
    sorted_rows = sorted(
        submissions,
        key=lambda row: str(row.get("submitted_at", "")),
        reverse=True,
    )
    table: list[list[str]] = []
    for row in sorted_rows:
        scores = row.get("benchmark_scores", {})
        if not isinstance(scores, dict):
            scores = {}
        table.append(
            [
                str(row.get("model_name", "")),
                str(row.get("huggingface_link", "")),
                format_score(scores.get("safety_score")),
                format_score(scores.get("source_support_score")),
                format_score(scores.get("clinical_boundary_score")),
                str(row.get("status", "pending review")),
                str(row.get("submitted_at", "")),
            ]
        )
    return table


def recent_submission_rows(submissions: list[object]) -> list[dict[str, object]]:
    rows = [row for row in submissions if isinstance(row, dict)]
    return sorted(
        rows,
        key=lambda row: str(row.get("submitted_at", "")),
        reverse=True,
    )[:MAX_SUBMISSIONS]


def format_last_updated(value: object) -> str:
    if not value:
        return "No submissions yet"
    text = str(value)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return text
    return parsed.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def latest_submission_timestamp(submissions: list[object]) -> object:
    timestamps = [
        str(row.get("submitted_at", ""))
        for row in submissions
        if isinstance(row, dict) and row.get("submitted_at")
    ]
    return max(timestamps) if timestamps else None


def last_updated_markdown(store: dict[str, object] | None = None) -> str:
    store = store or load_submission_store()
    submissions = store.get("submissions", [])
    if not isinstance(submissions, list) or not submissions:
        return "**Last Updated:** No submissions yet"
    last_updated = store.get("last_updated") or latest_submission_timestamp(submissions)
    return f"**Last Updated:** {format_last_updated(last_updated)}"


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


def normalize_huggingface_link(link: str | None) -> str:
    return normalize_huggingface_model_url(link)


def reachable_url(url: str) -> tuple[bool, str]:
    last_error = "No response received."
    headers = {"User-Agent": "medical-ai-failure-atlas-leaderboard/1.0"}
    for method in ("HEAD", "GET"):
        request = Request(url, headers=headers, method=method)
        try:
            with urlopen(request, timeout=HF_TIMEOUT_SECONDS) as response:
                if 200 <= response.status < 400:
                    return True, f"{response.status}"
                last_error = f"HTTP {response.status}"
        except HTTPError as exc:
            if method == "HEAD" and exc.code in {403, 405}:
                last_error = f"HTTP {exc.code}"
                continue
            last_error = f"HTTP {exc.code}"
        except URLError as exc:
            reason = getattr(exc, "reason", exc)
            last_error = str(reason)
        except TimeoutError:
            last_error = "Timed out"
        except OSError as exc:
            last_error = str(exc)
    return False, last_error


def leaderboard_state(path: Path | None = None) -> tuple[list[list[str]], str]:
    try:
        store = load_submission_store(path)
    except (OSError, ValueError) as exc:
        return [], f"**Last Updated:** Submission store error: {exc}"
    submissions = store.get("submissions", [])
    if not isinstance(submissions, list):
        submissions = []
    return submissions_to_table(submissions), last_updated_markdown(store)


def submit_model(
    model_name: str,
    huggingface_link: str,
    safety_score: float,
    source_support_score: float,
    clinical_boundary_score: float,
    notes: str,
    *,
    reachability_checker=reachable_url,
    store_path: Path | None = None,
) -> tuple[str, list[list[str]], str]:
    try:
        clean_model_name = (model_name or "").strip()
        if not clean_model_name:
            raise ValueError("Model name is required.")
        if len(clean_model_name) > MAX_MODEL_NAME_LENGTH:
            raise ValueError(f"Model name must be {MAX_MODEL_NAME_LENGTH} characters or fewer.")
        forbidden_model_phrase = forbidden_public_claim_phrase(clean_model_name)
        if forbidden_model_phrase:
            raise ValueError(
                "Model name includes an unsupported public claim: "
                f"{forbidden_model_phrase!r}."
            )

        clean_link = normalize_huggingface_link(huggingface_link)
        clean_notes = (notes or "").strip()
        if len(clean_notes) > MAX_NOTES_LENGTH:
            raise ValueError(f"Benchmark notes must be {MAX_NOTES_LENGTH} characters or fewer.")
        forbidden_notes_phrase = forbidden_public_claim_phrase(clean_notes)
        if forbidden_notes_phrase:
            raise ValueError(
                "Benchmark notes include an unsupported public claim: "
                f"{forbidden_notes_phrase!r}."
            )
        clean_scores = {
            "safety_score": coerce_score(safety_score, "Safety score"),
            "source_support_score": coerce_score(source_support_score, "Source support score"),
            "clinical_boundary_score": coerce_score(
                clinical_boundary_score,
                "Clinical boundary score",
            ),
        }
        reachable, detail = reachability_checker(clean_link)
        if not reachable:
            raise ValueError(f"HuggingFace link was not reachable: {detail}")

        now = current_utc_iso()
        entry = {
            "id": uuid.uuid4().hex,
            "model_name": clean_model_name,
            "huggingface_link": clean_link,
            "benchmark_scores": clean_scores,
            "notes": clean_notes,
            "status": "pending review",
            "submitted_at": now,
            "huggingface_reachable": True,
            "huggingface_status": detail,
        }

        with STORE_LOCK:
            store = load_submission_store(store_path)
            submissions = store.get("submissions", [])
            if not isinstance(submissions, list):
                submissions = []

            updated = False
            for index, existing in enumerate(submissions):
                if not isinstance(existing, dict):
                    continue
                if existing.get("huggingface_link") == clean_link:
                    entry["id"] = str(existing.get("id", entry["id"]))
                    entry["first_submitted_at"] = str(
                        existing.get("first_submitted_at", existing.get("submitted_at", now))
                    )
                    submissions[index] = entry
                    updated = True
                    break

            if not updated:
                entry["first_submitted_at"] = now
                submissions.append(entry)

            submissions = recent_submission_rows(submissions)
            store = {"last_updated": now, "submissions": submissions}
            save_submission_store(store, store_path)

        message = "Submission updated and saved." if updated else "Submission saved."
        return message, submissions_to_table(submissions), last_updated_markdown(store)
    except (OSError, ValueError) as exc:
        table, updated_text = leaderboard_state(store_path)
        return f"Submission not saved. {exc}", table, updated_text


def build_demo():
    if gr is None:
        raise RuntimeError("Install Gradio with: python3 -m pip install -r leaderboard/requirements.txt")

    rows = load_rows()
    submission_table_rows, last_updated = leaderboard_state()
    with gr.Blocks(title="Medical AI Failure Atlas Leaderboard") as demo:
        gr.Markdown("# Medical AI Failure Atlas Leaderboard")
        gr.Markdown(BOUNDARY_NOTE)

        with gr.Tab("Submitted Runs"):
            gr.Markdown(SUBMISSION_BOUNDARY_NOTE)
            last_updated_display = gr.Markdown(last_updated)
            submission_table = gr.Dataframe(
                headers=SUBMISSION_COLUMNS,
                value=submission_table_rows,
                datatype=["str"] * len(SUBMISSION_COLUMNS),
                interactive=False,
                wrap=True,
            )

            with gr.Group():
                gr.Markdown("## Submit a Model")
                with gr.Row():
                    model_name = gr.Textbox(label="Model name", placeholder="org or model name")
                    huggingface_link = gr.Textbox(
                        label="HuggingFace model repo link",
                        placeholder="https://huggingface.co/org/model",
                    )
                with gr.Row():
                    safety_score = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=0,
                        step=0.01,
                        label="Safety score",
                    )
                    source_support_score = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=0,
                        step=0.01,
                        label="Source support score",
                    )
                    clinical_boundary_score = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=0,
                        step=0.01,
                        label="Clinical boundary score",
                    )
                notes = gr.Textbox(
                    label="Benchmark notes",
                    placeholder="Synthetic benchmark context, scorer version, or review caveat",
                    lines=3,
                )
                submit_button = gr.Button("Submit model", variant="primary")
                submission_message = gr.Markdown()
                submit_button.click(
                    submit_model,
                    inputs=[
                        model_name,
                        huggingface_link,
                        safety_score,
                        source_support_score,
                        clinical_boundary_score,
                        notes,
                    ],
                    outputs=[submission_message, submission_table, last_updated_display],
                )

        with gr.Tab("Synthetic Preview"):
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

        gr.Markdown(
            f"[GitHub repo]({GITHUB_REPO_URL}) | "
            f"[Contribution guide]({CONTRIBUTION_GUIDE_URL})"
        )

    return demo


demo = build_demo() if gr is not None else None


if __name__ == "__main__":
    if demo is None:
        raise SystemExit("Install Gradio with: python3 -m pip install -r leaderboard/requirements.txt")
    demo.launch()
