from __future__ import annotations

import shutil
from pathlib import Path

from scripts.validate_preprint_claim_guard import validate


ROOT = Path(__file__).resolve().parents[1]
CLAIM_GUARD_FILES = [
    "README.md",
    "preprint/main.tex",
    "preprint/references.bib",
    "preprint/ARXIV_UPLOAD.md",
    "preprint/README.md",
    "docs/ARXIV_SUBMIT_PREP_20260703.md",
]


def copy_claim_guard_files(tmp_path: Path) -> Path:
    for rel_path in CLAIM_GUARD_FILES:
        src = ROOT / rel_path
        dst = tmp_path / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    return tmp_path


def test_preprint_claim_guard_accepts_current_files() -> None:
    assert validate(ROOT) == []


def test_preprint_claim_guard_rejects_stale_100_case_release_claim(
    tmp_path: Path,
) -> None:
    root = copy_claim_guard_files(tmp_path)
    main_tex = root / "preprint/main.tex"
    text = main_tex.read_text(encoding="utf-8")
    main_tex.write_text(
        text.replace(
            "contains 44 clinician-reviewed synthetic cases",
            "contains 100-case clinician-reviewed synthetic cases",
        ),
        encoding="utf-8",
    )

    errors = validate(root)

    assert any("100-case" in error for error in errors)


def test_preprint_claim_guard_rejects_missing_boundary_sentence(tmp_path: Path) -> None:
    root = copy_claim_guard_files(tmp_path)
    main_tex = root / "preprint/main.tex"
    text = main_tex.read_text(encoding="utf-8")
    main_tex.write_text(
        text.replace(
            "No patient data, clinical validation claims, or model rankings\nare included.",
            "",
        ),
        encoding="utf-8",
    )

    errors = validate(root)

    assert any("missing required boundary sentence" in error for error in errors)


def test_preprint_claim_guard_rejects_policy_citation_reintroduction(
    tmp_path: Path,
) -> None:
    root = copy_claim_guard_files(tmp_path)
    references = root / "preprint/references.bib"
    references.write_text(
        references.read_text(encoding="utf-8")
        + "\n@misc{ministry2026aivision,\n  title={Policy page},\n  year={2026}\n}\n",
        encoding="utf-8",
    )

    errors = validate(root)

    assert any("ministry2026aivision" in error for error in errors)


def test_preprint_claim_guard_rejects_missing_bibliography_key(tmp_path: Path) -> None:
    root = copy_claim_guard_files(tmp_path)
    main_tex = root / "preprint/main.tex"
    main_tex.write_text(
        main_tex.read_text(encoding="utf-8")
        + "\nMissing citation \\cite{missing2026source}.\n",
        encoding="utf-8",
    )

    errors = validate(root)

    assert any("missing2026source" in error for error in errors)
