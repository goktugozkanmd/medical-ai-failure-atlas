#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "safe_failure_card_objection.yml"
README = ROOT / "README.md"
SAFE_FAILURE_CARDS = ROOT / "docs" / "PUBLIC_SAFE_FAILURE_CARDS_20260619.md"

REQUIRED_CARD_IDS = [f"SFC{index:03d}" for index in range(1, 11)]

REQUIRED_TEMPLATE_PHRASES = [
    "Safe Failure Card objection",
    "Use synthetic or public information only.",
    "no patient data",
    "clinical validation claims",
    "clinical deployment claims",
    "benchmark ranking",
    "score certification",
    "source truth certification",
    "id: card_id",
    "id: lane",
    "id: risk",
    "id: missing_gate",
    "id: safer_wording",
    "id: boundaries",
    "This uses synthetic or public information only.",
    "This includes no patient data",
    "This does not provide clinical advice",
    "This does not claim benchmark ranking",
    "This does not claim partner status",
]

REQUIRED_DOC_PHRASES = [
    ".github/ISSUE_TEMPLATE/safe_failure_card_objection.yml",
    "Safe Failure Card issue template",
]

FORBIDDEN_TEMPLATE_PHRASES = [
    "clinically validated",
    "deployment ready",
    "endorsed by",
    "partner confirmed",
    "score certified",
    "source truth certified",
    "patient data used",
    "real patient",
    "official approval",
]

FORBIDDEN_INTERNAL_LABELS = [
    "de" + "AI",
    "human" + "ized",
    "AI " + "detector",
    "submit" + "_audit",
]


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def visible_yaml_text(text: str) -> str:
    visible_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("- "):
            stripped = stripped[2:]
        visible_lines.append(stripped)
    return "\n".join(visible_lines)


def main() -> int:
    errors: list[str] = []
    for path in [TEMPLATE, README, SAFE_FAILURE_CARDS]:
        if not path.exists():
            errors.append(f"Missing file: {path.relative_to(ROOT)}")

    template_text = TEMPLATE.read_text(encoding="utf-8") if TEMPLATE.exists() else ""
    readme_text = README.read_text(encoding="utf-8") if README.exists() else ""
    card_text = SAFE_FAILURE_CARDS.read_text(encoding="utf-8") if SAFE_FAILURE_CARDS.exists() else ""

    for phrase in REQUIRED_TEMPLATE_PHRASES:
        if phrase.lower() not in template_text.lower():
            errors.append(f"Template missing required phrase: {phrase}")

    for card_id in REQUIRED_CARD_IDS:
        if card_id not in template_text:
            errors.append(f"Template missing card id: {card_id}")

    combined_docs = f"{readme_text}\n{card_text}"
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in combined_docs.lower():
            errors.append(f"Docs missing issue template route phrase: {phrase}")

    lower_template = template_text.lower()
    for phrase in FORBIDDEN_TEMPLATE_PHRASES:
        if phrase in lower_template:
            errors.append(f"Template contains forbidden phrase: {phrase}")
    for phrase in FORBIDDEN_INTERNAL_LABELS:
        if phrase.lower() in lower_template:
            errors.append(f"Template contains internal process label: {phrase}")

    if "-" in text_without_urls(visible_yaml_text(template_text)):
        errors.append("Template contains non URL hyphen character")

    if errors:
        print("FAIL safe failure card issue template validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS safe failure card issue template validation")
    print(f"template={TEMPLATE.relative_to(ROOT)}")
    print(f"card_ids={len(REQUIRED_CARD_IDS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
