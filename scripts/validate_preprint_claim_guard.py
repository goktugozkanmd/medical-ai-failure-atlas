#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CLAIM_FILES = [
    Path("README.md"),
    Path("preprint/main.tex"),
    Path("preprint/ARXIV_UPLOAD.md"),
    Path("preprint/README.md"),
    Path("docs/ARXIV_SUBMIT_PREP_20260703.md"),
]

FORBIDDEN_PATTERNS = [
    (
        re.compile(
            r"\b(current|public|v0\.2\.1|release)\b[^.\n]{0,120}\b100[- ]case",
            re.IGNORECASE,
        ),
        "current release must not claim a 100-case set",
    ),
    (
        re.compile(
            r"\b(contains|includes|reports)\b[^.\n]{0,80}\b100\b[^.\n]{0,40}\bcases\b",
            re.IGNORECASE,
        ),
        "current release must not claim 100 cases",
    ),
    (
        re.compile(
            r"\b(ministry2026aivision|Ministry of Industry and Technology|AI vision consultation)\b"
        ),
        "unverified 2026 policy citation must not be reintroduced",
    ),
]

REQUIRED_MAIN_TEX_SNIPPETS = [
    "contains 44 clinician-reviewed synthetic cases",
    "No patient data, clinical validation claims, or model rankings are included.",
    "this report makes no comparative model-performance claim",
]


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    text_by_path: dict[Path, str] = {}

    for rel_path in CLAIM_FILES:
        path = root / rel_path
        if not path.exists():
            errors.append(f"{rel_path}: missing required claim-guard file")
            continue
        text_by_path[rel_path] = path.read_text(encoding="utf-8")

    for rel_path, text in text_by_path.items():
        for pattern, message in FORBIDDEN_PATTERNS:
            if (
                rel_path == Path("docs/ARXIV_SUBMIT_PREP_20260703.md")
                and "policy citation" in message
            ):
                continue
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{rel_path}:{line}: {message}: {match.group(0)!r}")

    main_tex = text_by_path.get(Path("preprint/main.tex"), "")
    normalized_main_tex = " ".join(main_tex.split())
    for snippet in REQUIRED_MAIN_TEX_SNIPPETS:
        if snippet not in normalized_main_tex:
            errors.append(
                f"preprint/main.tex: missing required boundary sentence: {snippet!r}"
            )

    references = (root / "preprint/references.bib").read_text(encoding="utf-8")
    if "ministry2026aivision" in references:
        errors.append(
            "preprint/references.bib: unverified ministry2026aivision entry must stay removed"
        )

    bib_keys = set(re.findall(r"@\w+\{([^,\s]+)", references))
    cite_keys = {
        key.strip()
        for cite_body in re.findall(r"\\cite\{([^}]+)\}", main_tex)
        for key in cite_body.split(",")
        if key.strip()
    }
    missing = sorted(cite_keys - bib_keys)
    if missing:
        errors.append(
            f"preprint/main.tex: citation keys missing from references.bib: {', '.join(missing)}"
        )

    unused = sorted(bib_keys - cite_keys)
    if unused:
        errors.append(
            f"preprint/references.bib: uncited bibliography entries: {', '.join(unused)}"
        )

    if len(bib_keys) != 9:
        errors.append(
            f"preprint/references.bib: expected 9 verified references, found {len(bib_keys)}"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate preprint public claim boundaries."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1

    print("PASS preprint claim guard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
