#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_OUTSIDE_REVIEWER_MICRO_BRIEF_20260620.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_outside_reviewer_micro_brief_public_action_audit_20260620.md"
SUPPORT = ROOT / "outputs" / "medical_ai_safety_field_kit_outside_reviewer_micro_brief_manual_source_support_20260620.md"

REQUIRED_FILES = [DOC, AUDIT, SUPPORT]

REQUIRED_DOC_PHRASES = [
    "Medical AI Safety Field Kit Outside Reviewer Micro Brief",
    "Leave one small objection on issue 154.",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/154",
    "One useful sentence is enough",
    "not maintaining this repository",
    "not posting through a project account",
    "controlled seed can test comment routing, but it is not outside review and is not external validation",
    "Use synthetic or public examples only.",
    "Done means issue 154 has one true outside comment",
]

FORBIDDEN = [
    "patient data used",
    "real patient evidence confirmed",
    "clinically validated",
    "clinical deployment ready",
    "safe for clinical use",
    "diagnosis advice provided",
    "treatment advice provided",
    "benchmark ranking confirmed",
    "score certified",
    "source truth certified",
    "partner confirmed",
    "institution approved",
    "endorsed by",
    "formal application submitted",
    "payment completed",
    "terms accepted",
    "TBYS submitted",
    "PRODIS submitted",
    "official guidance",
    "compliance certified",
    "outside style public objection",
    "independent validation",
    "external validation achieved",
]


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def check_text(label: str, text: str, errors: list[str]) -> None:
    lower_text = text.lower()
    for phrase in FORBIDDEN:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append(f"{label} contains non URL hyphen character")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing file: {path.relative_to(ROOT)}")

    doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    audit_text = AUDIT.read_text(encoding="utf-8") if AUDIT.exists() else ""
    support_text = SUPPORT.read_text(encoding="utf-8") if SUPPORT.exists() else ""

    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in doc_text.lower():
            errors.append(f"Doc missing required phrase: {phrase}")

    if "Allowed action: public GitHub commit after validation." not in audit_text:
        errors.append("Audit missing allowed action boundary")
    if "navigation claims only" not in support_text:
        errors.append("Source support missing navigation claim boundary")
    if "Issue 154 state and comment count." not in support_text:
        errors.append("Source support missing issue readback check")

    check_text("Doc", doc_text, errors)
    check_text("Audit", audit_text, errors)
    check_text("Source support", support_text, errors)

    if errors:
        print("FAIL Outside Reviewer Micro Brief validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Outside Reviewer Micro Brief validation")
    print(f"doc={DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
