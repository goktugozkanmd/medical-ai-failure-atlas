#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "public_review_operating_system_20260625.json"
MARKDOWN = ROOT / "docs" / "PUBLIC_REVIEW_OPERATING_SYSTEM_20260625.md"


def numbered(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def render(data: dict) -> str:
    lines: list[str] = [
        "# Public Review Operating System",
        "",
        f"Date: {data['date']}",
        "",
        f"Status: {data['status']}.",
        "",
        "## Purpose",
        "",
        data["purpose"],
        "",
        "## Live inputs",
        "",
        *numbered(data["live_inputs"]),
        "",
        "## Review lanes",
        "",
    ]

    for index, lane in enumerate(data["review_lanes"], 1):
        lines.extend(
            [
                f"### {index}. {lane['name']}",
                "",
                f"Route: {lane['route']}.",
                "",
                f"Action: {lane['action']}",
                "",
                f"Stop rule: {lane['stop_rule']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Queue states",
            "",
            *numbered(data["queue_states"]),
            "",
            "## Daily loop",
            "",
            *numbered(data["daily_loop"]),
            "",
            "## Blocked claims",
            "",
            *numbered(data["blocked_claims"]),
            "",
            "## Validator commands",
            "",
            *numbered([f"`{command}`" for command in data["validator_commands"]]),
            "",
            "## Current use",
            "",
            data["current_use"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    rendered = render(data)

    if args.check:
        if not MARKDOWN.exists():
            print(f"FAIL missing generated file: {MARKDOWN.relative_to(ROOT)}")
            return 1
        current = MARKDOWN.read_text(encoding="utf-8")
        if current != rendered:
            print(f"FAIL generated file is stale: {MARKDOWN.relative_to(ROOT)}")
            return 1
        print(f"PASS generated file is current: {MARKDOWN.relative_to(ROOT)}")
        return 0

    MARKDOWN.write_text(rendered, encoding="utf-8")
    print(f"Wrote {MARKDOWN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
