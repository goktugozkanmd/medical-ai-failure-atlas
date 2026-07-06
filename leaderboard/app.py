#!/usr/bin/env python3
from __future__ import annotations

import csv
import html as html_lib
import json
import os
import re
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
        ALLOWED_STATUS,
        ALLOWED_SUBMISSION_KEYS,
        FORBIDDEN_PUBLIC_CLAIM_PHRASES,
        HF_REACHABILITY_STATUS_PATTERN,
        MAX_HF_LINK_LENGTH,
        MAX_MODEL_NAME_LENGTH,
        MAX_NOTES_LENGTH,
        MAX_SUBMISSIONS,
        REQUIRED_SCORE_KEYS,
        coerce_score,
        forbidden_private_data_pattern,
        forbidden_public_claim_phrase,
        is_valid_submission_id,
        normalize_huggingface_model_url,
        unsafe_public_text_pattern,
    )
except ImportError:  # Supports copying leaderboard/app.py and leaderboard/policy.py to a Space root.
    from policy import (  # type: ignore[no-redef]
        ALLOWED_STATUS,
        ALLOWED_SUBMISSION_KEYS,
        FORBIDDEN_PUBLIC_CLAIM_PHRASES,
        HF_REACHABILITY_STATUS_PATTERN,
        MAX_HF_LINK_LENGTH,
        MAX_MODEL_NAME_LENGTH,
        MAX_NOTES_LENGTH,
        MAX_SUBMISSIONS,
        REQUIRED_SCORE_KEYS,
        coerce_score,
        forbidden_private_data_pattern,
        forbidden_public_claim_phrase,
        is_valid_submission_id,
        normalize_huggingface_model_url,
        unsafe_public_text_pattern,
    )


APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent if APP_DIR.name == "leaderboard" else APP_DIR
LEADERBOARD_DIR = ROOT / "leaderboard" if (ROOT / "leaderboard").exists() else APP_DIR
DEFAULT_RESULTS = LEADERBOARD_DIR / "synthetic_report_template_v0_1.tsv"
DEFAULT_SUBMISSIONS = LEADERBOARD_DIR / "submissions.json"
DEFAULT_WORST_CASE_REPORT = ROOT / "model_runs" / "worst_case_safety_report_v0_1.json"
DEFAULT_CASES = ROOT / "data" / "tr_medllm_synthetic_eval_set_v0_3.jsonl"
DEFAULT_FAILURE_CARDS_DIR = ROOT / "docs" / "model_failure_cards"
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

WORST_CASE_COLUMNS = [
    "model",
    "prompts",
    "min_safety",
    "unsafe_tier_count",
    "unsafe_rate",
]

BOUNDARY_NOTE = (
    "This preview uses synthetic rows only. It is not clinical advice, not a "
    "clinical validation table, not a model ranking, and not a model safety claim."
)

SUBMISSION_BOUNDARY_NOTE = (
    "Submitted rows are contributor supplied and pending review. Scores shown here "
    "are not clinical validation, source truth certification, a model ranking, or a "
    "clinical use claim. Rows are ordered by latest submission time, not by score. "
    "The JSON store is local to the running app unless persistent Space storage is enabled."
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


def worst_case_report_path() -> Path:
    configured = os.getenv("FAILURE_ATLAS_WORST_CASE_JSON")
    if configured:
        candidate = Path(configured)
        return candidate if candidate.is_absolute() else ROOT / candidate
    return DEFAULT_WORST_CASE_REPORT


def cases_path() -> Path:
    configured = os.getenv("FAILURE_ATLAS_CASES_JSONL")
    if configured:
        candidate = Path(configured)
        return candidate if candidate.is_absolute() else ROOT / candidate
    return DEFAULT_CASES


def failure_cards_dir() -> Path:
    configured = os.getenv("FAILURE_ATLAS_FAILURE_CARDS_DIR")
    if configured:
        candidate = Path(configured)
        return candidate if candidate.is_absolute() else ROOT / candidate
    return DEFAULT_FAILURE_CARDS_DIR


def load_case_rows(path: Path | None = None) -> list[dict[str, object]]:
    target = path or cases_path()
    if not target.exists():
        return []
    rows: list[dict[str, object]] = []
    with target.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if isinstance(row, dict):
                rows.append(row)
    return rows


def load_worst_case_report(path: Path | None = None) -> list[dict[str, object]]:
    target = path or worst_case_report_path()
    if not target.exists():
        return []
    with target.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    models = payload.get("models", []) if isinstance(payload, dict) else []
    return [row for row in models if isinstance(row, dict)]


def model_slug(value: object) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9.\-]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def public_leaderboard_model_slugs(submissions: list[dict[str, object]]) -> set[str]:
    return {model_slug(row.get("model_name")) for row in submissions if row.get("model_name")}


def as_float(value: object, default: float = 0.0) -> float:
    if not isinstance(value, (int, float, str)):
        return default
    try:
        return float(value)
    except ValueError:
        return default


def as_int(value: object, default: int = 0) -> int:
    if not isinstance(value, (int, float, str)):
        return default
    try:
        return int(value)
    except ValueError:
        return default


def worst_case_display_rows(
    report_rows: list[dict[str, object]] | None = None,
    submissions: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    report_rows = report_rows if report_rows is not None else load_worst_case_report()
    if submissions is None:
        store = load_submission_store()
        raw_submissions = store.get("submissions", [])
        submissions = displayable_submission_rows(raw_submissions if isinstance(raw_submissions, list) else [])
    public_slugs = public_leaderboard_model_slugs(submissions)
    rows = [row for row in report_rows if model_slug(row.get("model")) in public_slugs]
    return sorted(
        rows,
        key=lambda row: (-as_float(row.get("unsafe_rate")), str(row.get("model", ""))),
    )


def worst_case_to_table(rows: list[dict[str, object]]) -> list[list[str]]:
    table: list[list[str]] = []
    for row in rows:
        n = as_int(row.get("n"))
        unsafe_count = as_int(row.get("unsafe_count"))
        unsafe_rate = as_float(row.get("unsafe_rate"))
        worst_safety = row.get("worst_safety", "")
        table.append(
            [
                str(row.get("model", "")),
                str(n),
                f"{worst_safety}/5" if worst_safety != "" else "",
                f"{unsafe_count}/{n}" if n else str(unsafe_count),
                f"{unsafe_rate:.1f}%",
            ]
        )
    return table


def worst_case_summary_markdown(rows: list[dict[str, object]]) -> str:
    if not rows:
        return (
            "## Worst-case safety\n\n"
            "Worst-case report is not available in this runtime. "
            "This section uses synthetic, rule-based results only when the JSON report is present."
        )
    total = len(rows)
    unsafe_models = sum(1 for row in rows if as_int(row.get("unsafe_count")) > 0)
    highest = max(rows, key=lambda row: as_float(row.get("unsafe_rate")))
    return "\n".join(
        [
            "## Worst-case safety",
            "",
            "Average scores can hide unsafe-tier answers. This view shows each model's minimum safety score and the share of prompts scoring 1-2/5.",
            "",
            f"Current public leaderboard match: **{total} models**. Models with at least one unsafe-tier answer: **{unsafe_models}/{total}**.",
            "",
            f"Highest unsafe-tier rate in this snapshot: **{highest.get('model', '')}**: **{as_float(highest.get('unsafe_rate')):.1f}%** on **{as_int(highest.get('n'))}** prompts.",
            "",
            "Rule-based scoring; synthetic cases only; external clinician validation pending. This is a triage view, not a model ranking or deployment claim.",
        ]
    )


def extract_markdown_section(markdown: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^## ", markdown[start:], re.MULTILINE)
    end = start + next_match.start() if next_match else len(markdown)
    return markdown[start:end].strip()


def load_model_failure_cards(path: Path | None = None) -> list[dict[str, str]]:
    target = path or failure_cards_dir()
    if not target.exists():
        return []
    cards: list[dict[str, str]] = []
    for file_path in sorted(target.glob("[0-9][0-9][0-9]_*.md")):
        markdown = file_path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
        scenario_match = re.search(r"\*\*Scenario:\*\*\s*(.+)", markdown)
        risk_match = re.search(r"\*\*Risk Level:\*\*\s*(.+)", markdown)
        score_match = re.search(r"\*\*Safety Score:\*\*\s*(.+)", markdown)
        dangerous = extract_markdown_section(markdown, "Neden Tehlikeli?")
        safer = extract_markdown_section(markdown, "Daha Güvenli Cevap")
        if not dangerous or not safer:
            continue
        cards.append(
            {
                "title": title_match.group(1).strip() if title_match else file_path.stem,
                "scenario": scenario_match.group(1).strip() if scenario_match else "",
                "risk_level": risk_match.group(1).strip() if risk_match else "",
                "safety_score": score_match.group(1).strip() if score_match else "",
                "why_dangerous": dangerous,
                "safer_answer": safer,
                "path": str(file_path.relative_to(ROOT)),
            }
        )
    return cards


def model_failure_cards_markdown(cards: list[dict[str, str]] | None = None) -> str:
    selected = cards if cards is not None else load_model_failure_cards()
    if not selected:
        return "## Model Failure Cards\n\nNo model failure cards are available in this runtime."
    sections = [
        "## Model Failure Cards",
        "",
        "Each card shows the unsafe model answer pattern, then the two public-demo blocks: **Neden Tehlikeli?** and **Daha Güvenli Cevap**.",
    ]
    for card in selected:
        sections.extend(
            [
                "",
                f"### {card['title']}",
                "",
                f"**Scenario:** {card['scenario']}",
                f"**Risk level:** {card['risk_level']}",
                f"**Safety score:** {card['safety_score']}",
                f"**Source:** `{card['path']}`",
                "",
                "#### Neden Tehlikeli?",
                "",
                card["why_dangerous"],
                "",
                "#### Daha Güvenli Cevap",
                "",
                card["safer_answer"],
            ]
        )
    return "\n".join(sections)


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
        if not all(isinstance(row, dict) for row in data):
            raise ValueError(f"Submission store rows must be objects: {target}")
        return {"last_updated": None, "submissions": data}
    if not isinstance(data, dict):
        raise ValueError(f"Submission store must contain a JSON object: {target}")

    submissions = data.get("submissions", [])
    if not isinstance(submissions, list):
        raise ValueError(f"Submission store submissions must be a list: {target}")
    if not all(isinstance(row, dict) for row in submissions):
        raise ValueError(f"Submission store rows must be objects: {target}")

    return {
        "last_updated": data.get("last_updated"),
        "submissions": submissions,
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


def parse_submission_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def is_displayable_submission_row(row: object) -> bool:
    if not isinstance(row, dict):
        return False
    if set(row) - ALLOWED_SUBMISSION_KEYS:
        return False

    row_id = row.get("id")
    if not is_valid_submission_id(row_id):
        return False

    model_name = row.get("model_name")
    if not isinstance(model_name, str) or not model_name.strip():
        return False
    if len(model_name) > MAX_MODEL_NAME_LENGTH:
        return False
    if (
        forbidden_public_claim_phrase(model_name)
        or forbidden_private_data_pattern(model_name)
        or unsafe_public_text_pattern(model_name)
    ):
        return False

    link = row.get("huggingface_link")
    if not isinstance(link, str) or not link.strip():
        return False
    try:
        normalized_link = normalize_huggingface_link(link)
    except ValueError:
        return False
    if normalized_link != link:
        return False

    scores = row.get("benchmark_scores")
    if not isinstance(scores, dict):
        return False
    if set(scores) - set(REQUIRED_SCORE_KEYS):
        return False
    for score_key in REQUIRED_SCORE_KEYS:
        try:
            coerce_score(scores.get(score_key), score_key)
        except ValueError:
            return False

    notes = row.get("notes", "")
    if notes is not None and not isinstance(notes, str):
        return False
    if isinstance(notes, str):
        if len(notes) > MAX_NOTES_LENGTH:
            return False
        if (
            forbidden_public_claim_phrase(notes)
            or forbidden_private_data_pattern(notes)
            or unsafe_public_text_pattern(notes)
        ):
            return False

    if row.get("status") not in ALLOWED_STATUS:
        return False

    submitted_at = parse_submission_timestamp(row.get("submitted_at"))
    if submitted_at is None:
        return False

    first_submitted_at = row.get("first_submitted_at")
    if first_submitted_at:
        parsed_first_submitted_at = parse_submission_timestamp(first_submitted_at)
        if parsed_first_submitted_at is None or parsed_first_submitted_at > submitted_at:
            return False

    if row.get("huggingface_reachable") is not True:
        return False

    hf_status = row.get("huggingface_status")
    if not isinstance(hf_status, str) or not HF_REACHABILITY_STATUS_PATTERN.fullmatch(hf_status):
        return False

    return True


def displayable_submission_rows(submissions: list[object]) -> list[dict[str, object]]:
    return recent_submission_rows([row for row in submissions if is_displayable_submission_row(row)])


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


def normalized_legacy_timestamp(value: object, latest_allowed: str) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        latest = datetime.fromisoformat(latest_allowed.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or latest.tzinfo is None or parsed > latest:
        return None
    return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def severity_distribution(case_rows: list[dict[str, object]]) -> list[tuple[str, int]]:
    counts = Counter(str(row.get("severity_1_to_5", "missing")) for row in case_rows)
    return sorted(counts.items(), key=lambda item: (item[0] == "missing", item[0]))


def severity_distribution_html(case_rows: list[dict[str, object]]) -> str:
    distribution = severity_distribution(case_rows)
    if not distribution:
        return "<p><strong>Clinical severity distribution:</strong> case JSONL not available in this runtime.</p>"
    total = sum(count for _, count in distribution)
    max_count = max(count for _, count in distribution)
    colors = {
        "1": "#d1fae5",
        "2": "#a7f3d0",
        "3": "#fde68a",
        "4": "#fb923c",
        "5": "#ef4444",
        "missing": "#9ca3af",
    }
    bars = []
    for severity, count in distribution:
        width = round((count / max_count) * 100, 2) if max_count else 0
        percent = (count / total) * 100 if total else 0
        escaped_severity = html_lib.escape(severity)
        color = colors.get(severity, "#60a5fa")
        bars.append(
            "".join(
                [
                    '<div style="display:grid; grid-template-columns: 6rem 1fr 7rem; gap:0.75rem; align-items:center; margin:0.35rem 0;">',
                    f'<div>Severity {escaped_severity}</div>',
                    '<div style="background:#111827; border:1px solid #374151; border-radius:999px; overflow:hidden; height:1rem;">',
                    f'<div style="width:{width}%; background:{color}; height:1rem;"></div>',
                    "</div>",
                    f'<div>{count} cases ({percent:.1f}%)</div>',
                    "</div>",
                ]
            )
        )
    return "".join(
        [
            '<section style="border:1px solid #374151; border-radius:0.75rem; padding:1rem; margin:1rem 0;">',
            "<h3>Clinical severity distribution</h3>",
            f"<p>Synthetic clinician-authored case subset: <strong>{total}</strong> rows. Higher severity means greater harm if the model misses the safety boundary.</p>",
            *bars,
            '<p style="font-size:0.9rem; opacity:0.8;">This chart describes the synthetic benchmark mix only. It is not a model ranking or clinical validation claim.</p>',
            "</section>",
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
    display_rows = displayable_submission_rows(submissions)
    display_store = dict(store)
    display_store["submissions"] = display_rows
    if not display_rows:
        display_store["last_updated"] = None
    return submissions_to_table(display_rows), last_updated_markdown(display_store)


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
        forbidden_model_private_pattern = forbidden_private_data_pattern(clean_model_name)
        if forbidden_model_private_pattern:
            raise ValueError(
                "Model name includes private data pattern: "
                f"{forbidden_model_private_pattern}."
            )
        unsafe_model_text_pattern = unsafe_public_text_pattern(clean_model_name)
        if unsafe_model_text_pattern:
            raise ValueError(
                "Model name includes unsafe public text pattern: "
                f"{unsafe_model_text_pattern}."
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
        forbidden_notes_private_pattern = forbidden_private_data_pattern(clean_notes)
        if forbidden_notes_private_pattern:
            raise ValueError(
                "Benchmark notes include private data pattern: "
                f"{forbidden_notes_private_pattern}."
            )
        unsafe_notes_text_pattern = unsafe_public_text_pattern(clean_notes)
        if unsafe_notes_text_pattern:
            raise ValueError(
                "Benchmark notes include unsafe public text pattern: "
                f"{unsafe_notes_text_pattern}."
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
                    existing_id = existing.get("id")
                    if is_valid_submission_id(existing_id):
                        entry["id"] = str(existing_id)
                    legacy_first_submitted_at = normalized_legacy_timestamp(
                        existing.get("first_submitted_at") or existing.get("submitted_at"),
                        now,
                    )
                    entry["first_submitted_at"] = legacy_first_submitted_at or now
                    submissions[index] = entry
                    updated = True
                    break

            if not updated:
                entry["first_submitted_at"] = now
                submissions.append(entry)

            submissions = displayable_submission_rows(submissions)
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
    case_rows = load_case_rows()
    submission_table_rows, last_updated = leaderboard_state()
    worst_case_rows = worst_case_display_rows()
    failure_cards = load_model_failure_cards()
    with gr.Blocks(title="Medical AI Failure Atlas Leaderboard") as demo:
        gr.Markdown("# Medical AI Failure Atlas Leaderboard")
        gr.Markdown(BOUNDARY_NOTE)
        gr.Markdown(worst_case_summary_markdown(worst_case_rows))

        with gr.Tab("Submitted Runs"):
            gr.Markdown(SUBMISSION_BOUNDARY_NOTE)
            gr.Markdown(
                "## Submit your model or collaborate\n\n"
                "Use the form below for a Hugging Face model repository you want reviewed against the synthetic preview gates. "
                "For collaboration, open a GitHub issue with one synthetic case, one safety gate objection, or one wording fix. "
                "Do not submit patient data, private clinical text, clinical validation claims, ranking claims, or endorsement claims."
            )
            last_updated_display = gr.Markdown(last_updated)
            submission_table = gr.Dataframe(
                headers=SUBMISSION_COLUMNS,
                value=submission_table_rows,
                datatype=["str"] * len(SUBMISSION_COLUMNS),
                interactive=False,
                wrap=True,
            )

            with gr.Group():
                gr.Markdown("## Model submission form")
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

        with gr.Tab("Worst-case Safety"):
            gr.Markdown(worst_case_summary_markdown(worst_case_rows))
            gr.Dataframe(
                headers=WORST_CASE_COLUMNS,
                value=worst_case_to_table(worst_case_rows),
                datatype=["str"] * len(WORST_CASE_COLUMNS),
                interactive=False,
                wrap=True,
            )
            gr.Markdown(
                "Data source: `model_runs/worst_case_safety_report_v0_1.json`. "
                "The source file can include historical rows; this Space filters the view to current public leaderboard submissions."
            )

        with gr.Tab("Failure Cards"):
            gr.Markdown(model_failure_cards_markdown(failure_cards))

        with gr.Tab("Synthetic Preview"):
            gr.HTML(severity_distribution_html(case_rows))
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
