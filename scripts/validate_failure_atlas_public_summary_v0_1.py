#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = ROOT / "failure_atlas" / "public"
INDEX = PUBLIC_DIR / "INDEX.md"
METHODOLOGY = PUBLIC_DIR / "METHODOLOGY.md"

REQUIRED_INDEX_PHRASES = [
    "Status: public safe draft.",
    "Not for clinical use.",
    "raw output withheld view",
    "FA_PUBLIC_001",
    "FA_PUBLIC_002",
    "FA_PUBLIC_003",
    "Raw output withheld",
    "Clinical validation claims",
]

REQUIRED_METHOD_PHRASES = [
    "Status: public safe draft.",
    "Not for clinical use.",
    "Raw output withheld policy",
    "Claim limits",
    "Release boundary",
]


def joined(*parts: str) -> str:
    return "".join(parts)


BLOCKED_PATTERNS = [
    joined("This is preeclampsia", " with severe features"),
    joined("Take 0.1", " units"),
    joined("hold", " warfarin"),
    joined("4b27b4ef70851453d9b41c29aaada256", "ec7e0e9bee4c799a8e734eadddcc9da4"),
    joined("c9d3b4587fb9804cdecfa70d44944ac26", "bcd735adf664ab2b1a6bf1999b96aa5"),
    joined("f7d6df9dd8fdc58620845c3c613fa796", "d89d1372dfee5f8386fabb1be6099b53"),
    joined("5ea671a98a5a109c875cc73348c170fd", "ccf2ed807a489413384454f8d92703df"),
    joined("v3_scale30_20260613", "_R0066"),
    joined("hard30_20260613", "_R0067"),
    joined("hard30_20260613", "_R0073"),
    joined("clinically", " validated"),
    joined("safe for", " clinical use"),
    joined("best", " model"),
]

BLOCKED_PATH_PARTS = [
    joined("failure_atlas", "/cases"),
    joined("outputs", "/raw.txt"),
    joined("inputs", "/prompt.txt"),
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require_file(path: Path) -> str:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    index = require_file(INDEX)
    methodology = require_file(METHODOLOGY)
    combined = index + "\n" + methodology

    for phrase in REQUIRED_INDEX_PHRASES:
        if phrase not in index:
            fail(f"INDEX.md missing required phrase: {phrase}")

    for phrase in REQUIRED_METHOD_PHRASES:
        if phrase not in methodology:
            fail(f"METHODOLOGY.md missing required phrase: {phrase}")

    for pattern in BLOCKED_PATTERNS:
        if pattern.lower() in combined.lower():
            fail(f"blocked public summary pattern present: {pattern}")

    normalized = combined.replace("\\", "/")
    for path_part in BLOCKED_PATH_PARTS:
        if path_part in normalized:
            fail(f"internal path reference present: {path_part}")

    if combined.count("Raw output withheld") < 3:
        fail("expected at least three raw output withheld markers")

    if "Patient data" not in index:
        fail("INDEX.md must explicitly exclude patient data")

    print("PASS failure atlas public summary v0.1")


if __name__ == "__main__":
    main()
