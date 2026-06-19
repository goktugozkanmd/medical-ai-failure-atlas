#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_REVIEWER_START_HERE_20260619.md"

REQUIRED_PHRASES = [
    "Medical AI Safety Field Kit Reviewer Start Here",
    "public entry page for fast reviewer action",
    "Public intake",
    "Source support starter",
    "Turkish wording starter",
    "Safe Failure Card issue template",
    "BRIDGE public route",
    "Clinician reviewer",
    "Source support reviewer",
    "Benchmark maintainer",
    "Hospital quality reviewer",
    "Open model maintainer",
    "Turkish language reviewer",
    "Lane:",
    "Risk:",
    "Fix:",
    "Do not submit patient data",
    "This is not a request for study approval",
    "make medical_ai_safety_field_kit_reviewer_start_here",
]

REQUIRED_URLS = [
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/150",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/151",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/.github/ISSUE_TEMPLATE/safe_failure_card_objection.yml",
    "https://github.com/YLab-Open/BRIDGE/issues/4#issuecomment-4754548346",
]

FORBIDDEN = [
    "clinically validated",
    "clinical deployment ready",
    "safe for clinical use",
    "approved by",
    "endorsed by",
    "in partnership with",
    "institutional approval confirmed",
    "score certified",
    "source truth certified",
    "best model",
    "submit patient cases",
    "share real cases",
    "terms accepted",
    "payment completed",
    "formal application submitted",
    "official guidance",
    "compliance certified",
    "de" + "AI",
    "human" + "ized",
    "AI " + "detector",
    "submit" + "_audit",
]


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"Missing doc: {DOC.relative_to(ROOT)}")
        print("FAIL reviewer start here validation")
        for error in errors:
            print(f"- {error}")
        return 1

    text = DOC.read_text(encoding="utf-8")
    lower_text = text.lower()

    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")
    for url in REQUIRED_URLS:
        if url not in text:
            errors.append(f"Missing required URL: {url}")
    for phrase in FORBIDDEN:
        if phrase.lower() in lower_text:
            errors.append(f"Contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append("Contains non URL hyphen character")
    if text.count("https://") != len(REQUIRED_URLS):
        errors.append("Unexpected URL count")

    if errors:
        print("FAIL reviewer start here validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer start here validation")
    print(f"doc={DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
