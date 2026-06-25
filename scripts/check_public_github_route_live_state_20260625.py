#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs" / "public_github_route_watchlist_20260625.json"

EXPECTED_COUNTS = {
    "ai_alliance_issue_50": {"comments": 2},
    "lighteval_pr_1272": {"comments": 0, "reviews": 0},
    "inspect_ai_pr_4343": {"comments": 0, "reviews": 0},
    "failure_atlas_issue_154": {"comments": 0},
}


def normalize(value: object) -> str:
    return str(value or "").strip().lower().replace("_", " ")


def run_json(command: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        return json.loads(completed.stdout)
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        raise RuntimeError(f"GitHub CLI command failed: {' '.join(command)}: {detail}")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"GitHub CLI returned invalid JSON: {' '.join(command)}") from exc


def count_items(value: object) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict) and "nodes" in value and isinstance(value["nodes"], list):
        return len(value["nodes"])
    return 0


def issue_state(repo: str, number: int) -> dict[str, object]:
    payload = run_json(
        [
            "gh",
            "issue",
            "view",
            str(number),
            "--repo",
            repo,
            "--json",
            "state,comments,updatedAt",
        ]
    )
    return {
        "live_state": normalize(payload.get("state")),
        "comments": count_items(payload.get("comments")),
        "updated_at": payload.get("updatedAt", ""),
    }


def pull_request_state(repo: str, number: int) -> dict[str, object]:
    payload = run_json(
        [
            "gh",
            "pr",
            "view",
            str(number),
            "--repo",
            repo,
            "--json",
            "state,reviewDecision,mergeStateStatus,comments,reviews,updatedAt",
        ]
    )
    return {
        "live_state": normalize(payload.get("state")),
        "review_state": normalize(payload.get("reviewDecision")),
        "merge_state": normalize(payload.get("mergeStateStatus")),
        "comments": count_items(payload.get("comments")),
        "reviews": count_items(payload.get("reviews")),
        "updated_at": payload.get("updatedAt", ""),
    }


def main() -> int:
    errors: list[str] = []
    if shutil.which("gh") is None:
        print("FAIL public GitHub route live state check")
        print("- GitHub CLI not found")
        return 1
    if not DATA.exists():
        print("FAIL public GitHub route live state check")
        print(f"- Missing data file: {DATA.relative_to(ROOT)}")
        return 1

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    routes = {route.get("id"): route for route in payload.get("routes", [])}
    try:
        live = {
            "ai_alliance_issue_50": issue_state(
                "The-AI-Alliance/trust-safety-evals", 50
            ),
            "lighteval_pr_1272": pull_request_state("huggingface/lighteval", 1272),
            "inspect_ai_pr_4343": pull_request_state(
                "UKGovernmentBEIS/inspect_ai", 4343
            ),
            "failure_atlas_issue_154": issue_state(
                "goktugozkanmd/medical-ai-failure-atlas", 154
            ),
        }
    except RuntimeError as exc:
        print("FAIL public GitHub route live state check")
        print(f"- {exc}")
        return 1

    for route_id, observed in live.items():
        route = routes.get(route_id)
        if route is None:
            errors.append(f"Missing route in watchlist JSON: {route_id}")
            continue
        for key in ["live_state", "review_state", "merge_state"]:
            expected = route.get(key)
            if expected is None or key not in observed:
                continue
            if normalize(expected) != normalize(observed[key]):
                errors.append(
                    f"{route_id} {key} expected {expected}, observed {observed[key]}"
                )
        for key, expected_count in EXPECTED_COUNTS.get(route_id, {}).items():
            observed_count = int(observed.get(key, 0))
            if observed_count != expected_count:
                errors.append(
                    f"{route_id} {key} expected {expected_count}, observed {observed_count}"
                )

    if errors:
        print("FAIL public GitHub route live state check")
        for error in errors:
            print(f"- {error}")
        print("A new public route signal may need triage before posting or replying.")
        return 1

    print("PASS public GitHub route live state check")
    for route_id, observed in live.items():
        parts = [
            route_id,
            f"state={observed['live_state']}",
            f"comments={observed.get('comments', 0)}",
        ]
        if "review_state" in observed:
            parts.append(f"review={observed['review_state']}")
        if "merge_state" in observed:
            parts.append(f"merge={observed['merge_state']}")
        if "reviews" in observed:
            parts.append(f"reviews={observed['reviews']}")
        print(" ".join(parts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
