#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PUBLIC_ENTRY_FILES = [
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml",
]

EXPECTED_OWNER_FRAGMENT = "goktugozkanmd/medical-ai-failure-atlas"
STALE_OWNER_FRAGMENT = "v0id-lab/medical-ai-failure-atlas"


def main() -> int:
    errors: list[str] = []

    for path in PUBLIC_ENTRY_FILES:
        relative_path = path.relative_to(ROOT)
        if not path.exists():
            errors.append(f"Missing public entry file: {relative_path}")
            continue

        text = path.read_text(encoding="utf-8")
        if STALE_OWNER_FRAGMENT in text:
            errors.append(f"Stale GitHub owner link in {relative_path}")
        if EXPECTED_OWNER_FRAGMENT not in text:
            errors.append(f"Missing current GitHub owner link in {relative_path}")

    if errors:
        print("FAIL public repo owner link validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS public repo owner link validation")
    print(f"checked_files={len(PUBLIC_ENTRY_FILES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
