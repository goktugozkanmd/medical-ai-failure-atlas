#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "public_review_operating_system_20260625.json"
MARKDOWN = ROOT / "docs" / "PUBLIC_REVIEW_OPERATING_SYSTEM_20260625.md"
BUILDER = ROOT / "scripts" / "build_public_review_operating_system_20260625.py"

REQUIRED_PHRASES = [
    "Public Review Operating System",
    "Turn public attention into one concrete review action",
    "Issue 154",
    "LinkedIn visibility",
    "Route owner response",
    "Maintainer route",
    "Run public GitHub route preflight",
    "Produce one concrete artifact",
    "make public_review_operating_system",
]

FORBIDDEN_PHRASES = [
    "endorsement confirmed",
    "partner confirmed",
    "institutional support confirmed",
    "clinical validation complete",
    "clinical deployment ready",
    "model superiority proven",
    "score certified",
    "patient data used",
    "regulatory approval secured",
    "terms accepted",
    "payment completed",
    "accepted contribution",
    "merged contribution",
]


def main() -> int:
    errors: list[str] = []

    if not JSON_PATH.exists():
        errors.append(f"Missing json: {JSON_PATH.relative_to(ROOT)}")
        data = {}
    else:
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    if not MARKDOWN.exists():
        errors.append(f"Missing markdown: {MARKDOWN.relative_to(ROOT)}")
        text = ""
    else:
        text = MARKDOWN.read_text(encoding="utf-8")

    check = subprocess.run(
        [sys.executable, str(BUILDER), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if check.returncode != 0:
        errors.append(check.stdout.strip())

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase in markdown: {phrase}")

    if "-" in text:
        errors.append("Markdown contains a hyphen character")

    expected_lengths = {
        "live_inputs": 6,
        "review_lanes": 5,
        "queue_states": 6,
        "daily_loop": 8,
        "blocked_claims": 12,
        "validator_commands": 3,
    }
    for key, expected in expected_lengths.items():
        if len(data.get(key, [])) != expected:
            errors.append(f"JSON {key} must contain {expected} rows")

    if errors:
        print("FAIL public review operating system validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS public review operating system validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"json={JSON_PATH.relative_to(ROOT)}")
    print(f"review_lanes={len(data['review_lanes'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
