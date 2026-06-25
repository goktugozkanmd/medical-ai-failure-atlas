#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "docs" / "PUBLIC_VISIBILITY_CLAIM_GATE_20260625.md"
JSON_PATH = ROOT / "docs" / "public_visibility_claim_gate_20260625.json"

REQUIRED_PHRASES = [
    "Public Visibility Claim Gate",
    "Run `make public_github_route_preflight` before naming live GitHub route state",
    "A public comment was received",
    "A maintainer replied",
    "A validator passed",
    "Keep public visibility separate from route pressure",
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
    "merged contribution",
    "accepted contribution",
]


def main() -> int:
    errors: list[str] = []

    if not MARKDOWN.exists():
        errors.append(f"Missing markdown: {MARKDOWN.relative_to(ROOT)}")
        text = ""
    else:
        text = MARKDOWN.read_text(encoding="utf-8")

    if not JSON_PATH.exists():
        errors.append(f"Missing json: {JSON_PATH.relative_to(ROOT)}")
        data = {}
    else:
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase in markdown: {phrase}")

    if "-" in text:
        errors.append("Markdown contains a hyphen character")

    if data.get("required_command_before_route_state") != "make public_github_route_preflight":
        errors.append("JSON missing required preflight command")

    if len(data.get("gate_rows", [])) != 6:
        errors.append("JSON gate_rows must contain 6 rows")

    if len(data.get("blocked_claims", [])) != 10:
        errors.append("JSON blocked_claims must contain 10 rows")

    if len(data.get("allowed_wording", [])) != 6:
        errors.append("JSON allowed_wording must contain 6 rows")

    if errors:
        print("FAIL public visibility claim gate validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS public visibility claim gate validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"json={JSON_PATH.relative_to(ROOT)}")
    print(f"gate_rows={len(data['gate_rows'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
