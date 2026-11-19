"""Guard the README Current Snapshot table against drift from the raw source files.

The snapshot table is the first thing a visitor reads. It combines:
- average safety from ``leaderboard/submissions.json``
- prompt count, minimum safety and unsafe-tier count from
  ``model_runs/worst_case_safety_report_v0_1.json``

This test keeps the README table in lock-step with those raw files.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SUBMISSIONS = ROOT / "leaderboard" / "submissions.json"
WORST_CASE = ROOT / "model_runs" / "worst_case_safety_report_v0_1.json"

ROW_RE = re.compile(
    r"^\|\s*(?P<model>.+?)\s*\|\s*(?P<prompts>\d+)\s*\|\s*"
    r"(?P<avg_safety>\d+(?:\.\d+)?)\s*\|\s*(?P<min_safety>\d/5)\s*\|\s*"
    r"(?P<unsafe_tier>\d+/\d+)\s*\|$"
)


def _snapshot_section() -> str:
    markdown = README.read_text(encoding="utf-8")
    match = re.search(r"^## Current Snapshot\s*$", markdown, re.MULTILINE)
    assert match, "README must contain a '## Current Snapshot' heading"
    rest = markdown[match.end():]
    next_heading = re.search(r"^## ", rest, re.MULTILINE)
    return rest[: next_heading.start() if next_heading else len(rest)]


def _snapshot_rows() -> list[re.Match[str]]:
    rows = []
    for line in _snapshot_section().splitlines():
        match = ROW_RE.match(line)
        if match:
            rows.append(match)
    return rows


def _slug(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9.\-]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def _scores_by_model() -> dict[str, float]:
    payload = json.loads(SUBMISSIONS.read_text(encoding="utf-8"))
    return {
        row["model_name"]: float(row["benchmark_scores"]["safety_score"])
        for row in payload["submissions"]
    }


def _worst_case_by_slug() -> dict[str, dict[str, object]]:
    payload = json.loads(WORST_CASE.read_text(encoding="utf-8"))
    return {str(row["model"]): row for row in payload["models"]}


def test_snapshot_table_matches_leaderboard_and_worst_case_report() -> None:
    rows = _snapshot_rows()
    scores = _scores_by_model()
    worst_case = _worst_case_by_slug()

    assert len(rows) == len(scores), (
        "README snapshot rows must match the public leaderboard store "
        f"({len(rows)} rows vs {len(scores)} submissions)"
    )

    for row in rows:
        model = row.group("model")
        assert model in scores, f"README row model missing from submissions.json: {model}"
        expected_avg = scores[model]
        assert float(row.group("avg_safety")) == expected_avg, (
            f"README avg safety for {model} does not match submissions.json "
            f"({row.group('avg_safety')} vs {expected_avg})"
        )

        slug = _slug(model)
        assert slug in worst_case, f"README row model missing from worst-case report: {model}"
        report = worst_case[slug]
        prompts = int(row.group("prompts"))
        assert prompts == int(report["n"]), (
            f"README prompt count for {model} does not match worst-case report "
            f"({prompts} vs {report['n']})"
        )
        min_safety, _ = row.group("min_safety").split("/")
        assert int(min_safety) == int(report["worst_safety"]), (
            f"README min safety for {model} does not match worst-case report "
            f"({min_safety} vs {report['worst_safety']})"
        )
        unsafe_count, unsafe_total = row.group("unsafe_tier").split("/")
        assert int(unsafe_total) == prompts, (
            f"README unsafe-tier denominator for {model} must equal the prompt count"
        )
        assert int(unsafe_count) == int(report["unsafe_count"]), (
            f"README unsafe-tier count for {model} does not match worst-case report "
            f"({unsafe_count} vs {report['unsafe_count']})"
        )


def test_snapshot_lead_sentence_matches_report_min_safety_counts() -> None:
    rows = _snapshot_rows()
    worst_case = _worst_case_by_slug()

    lowest_tier_models = sum(
        1
        for row in rows
        if int(row.group("min_safety").split("/")[0]) == 1
        and _slug(row.group("model")) in worst_case
    )

    section = _snapshot_section()
    match = re.search(
        r"In the current rule-based snapshot, (\d+) of (\d+) evaluated models",
        section,
    )
    assert match, "README snapshot lead sentence must state 'N of M evaluated models'"
    stated_lowest, stated_total = int(match.group(1)), int(match.group(2))

    assert stated_total == len(rows), (
        f"README lead sentence total ({stated_total}) must match table rows ({len(rows)})"
    )
    assert stated_lowest == lowest_tier_models, (
        f"README lead sentence lowest-tier count ({stated_lowest}) does not match "
        f"the worst-case report ({lowest_tier_models})"
    )
