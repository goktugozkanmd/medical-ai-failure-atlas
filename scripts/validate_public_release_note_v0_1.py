#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "PUBLIC_RELEASE_NOTE_V0_1_20260616.md"

REQUIRED_PHRASES = [
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "19 synthetic intake rows",
    "14 Turkish synthetic risk rows",
    "10 risk axes",
    "10 of 10 Failure Atlas taxonomy pattern IDs represented",
    "6 public review states",
    "Clinician review protocol v0.1",
    "19 clinician review queue rows",
    "4 source review rows",
    "Source claim review queue v0.1",
    "8 source claim review queue rows",
    "Health data quality and label audit card v0.1",
    "150 synthetic scenario rows",
    "70 prompt rows",
    "24 pilot inter rater rows",
    "MedHELM and Medmarks boundary notes v0.1",
    "Medical language model assurance card template v0.1",
    "Assurance card template for intended use, risk, source support, human review, and release gate boundaries",
]

FORBIDDEN_PHRASES = [
    "validated for clinical use",
    "safe for clinical use",
    "approved by",
    "official acceptance",
    "regulatory approval",
    "model is safe",
    "best model",
    "patient data used",
]


def main() -> int:
    errors: list[str] = []
    if not NOTE.exists():
        errors.append(f"Missing release note: {NOTE}")
        text = ""
    else:
        text = NOTE.read_text(encoding="utf-8")
    lower_text = text.lower()

    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")

    if "```bash" not in text:
        errors.append("Release note should include runnable command block")

    if errors:
        print("FAIL public release note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS public release note validation")
    print(f"file={NOTE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
