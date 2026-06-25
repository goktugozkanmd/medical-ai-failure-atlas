#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

SECTION_TITLE = "2026 06 25 public route and report hygiene surfaces"

REQUIRED_LINKS = {
    "docs/HEALTH_AI_ASSURANCE_OPPORTUNITY_RADAR_20260625.md",
    "docs/TEKNOFEST_HEALTH_AI_REPORT_CLAIM_HYGIENE_CHECKLIST_20260625.md",
    "docs/AI_ALLIANCE_MEDHELM_FOLLOW_UP_PREP_20260625.md",
    "docs/PUBLIC_GITHUB_ROUTE_WATCHLIST_20260625.md",
}

REQUIRED_PHRASES = [
    "Current public navigation for the latest medical AI assurance work",
    "without application, partner, device, clinical validation, or compliance claims",
    "ten gate checklist for safer project report language",
    "keeps acknowledgement separate from endorsement",
    "The AI Alliance issue 50",
    "lighteval pull request 1272",
    "inspect ai pull request 4343",
    "public navigation and claim hygiene materials only",
    "not submissions, applications, merge decisions",
]

FORBIDDEN_SECTION_PHRASES = [
    "application submitted",
    "partner confirmed",
    "official role granted",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used",
    "benchmark compatible",
    "score certified",
    "fda authorized",
    "eu compliant",
    "chai certified",
    "medhelm partner",
    "healthbench partner",
    "bridge partner",
    "teknofest finalist",
    "terms accepted",
    "payment completed",
    "accepted contribution",
    "merged contribution",
    "endorsement confirmed",
]


def extract_section(text: str, title: str) -> str:
    pattern = rf"^## {re.escape(title)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    return match.group(0) if match else ""


def main() -> int:
    errors: list[str] = []
    if not README.exists():
        errors.append("Missing README.md")
        section = ""
    else:
        text = README.read_text(encoding="utf-8")
        section = extract_section(text, SECTION_TITLE)

    if not section:
        errors.append(f"README missing section: {SECTION_TITLE}")

    lower_section = section.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_section:
            errors.append(f"Section missing required phrase: {phrase}")

    for link in REQUIRED_LINKS:
        if link not in section:
            errors.append(f"Section missing required link: {link}")
        if not (ROOT / link).exists():
            errors.append(f"Linked file missing: {link}")

    for phrase in FORBIDDEN_SECTION_PHRASES:
        if phrase in lower_section:
            errors.append(f"Section contains forbidden phrase: {phrase}")

    if errors:
        print("FAIL README current surface links validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS README current surface links validation")
    print(f"section={SECTION_TITLE}")
    print(f"links={len(REQUIRED_LINKS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
