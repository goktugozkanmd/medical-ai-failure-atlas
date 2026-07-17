from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

from scripts.validate_clinician_panel_readiness_manifest_v0_1 import (
    DEFAULT_MANIFEST,
    validate,
)


ROOT = Path(__file__).resolve().parents[1]


def copy_manifest_tree(tmp_path: Path) -> Path:
    manifest = read_manifest(ROOT)
    manifest_dst = tmp_path / DEFAULT_MANIFEST
    manifest_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / DEFAULT_MANIFEST, manifest_dst)

    for artifact in manifest["artifacts"]:
        src = ROOT / artifact["path"]
        dst = tmp_path / artifact["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)

    return tmp_path


def read_manifest(root: Path) -> dict:
    return json.loads((root / DEFAULT_MANIFEST).read_text(encoding="utf-8"))


def rewrite_manifest(root: Path, manifest: dict) -> None:
    (root / DEFAULT_MANIFEST).write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def rewrite_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def test_clinician_panel_readiness_manifest_accepts_current_files() -> None:
    assert validate(ROOT) == []


def test_clinician_panel_readiness_manifest_rejects_completion_claim(
    tmp_path: Path,
) -> None:
    root = copy_manifest_tree(tmp_path)
    manifest = read_manifest(root)
    manifest["panel_claim_state"] = "complete"
    rewrite_manifest(root, manifest)

    errors = validate(root)

    assert any("panel_claim_state must stay 'not_complete'" in error for error in errors)


def test_clinician_panel_readiness_manifest_rejects_missing_artifact(
    tmp_path: Path,
) -> None:
    root = copy_manifest_tree(tmp_path)
    (root / "docs/CLINICIAN_REVIEW_PROTOCOL_V0_1.md").unlink()

    errors = validate(root)

    assert any(
        "missing artifact docs/CLINICIAN_REVIEW_PROTOCOL_V0_1.md" in error
        for error in errors
    )


def test_clinician_panel_readiness_manifest_rejects_assignment_gap(
    tmp_path: Path,
) -> None:
    root = copy_manifest_tree(tmp_path)
    assignment_path = root / "data/panel_pilot/clinician_panel_rating_sheet_v0_1.tsv"
    with assignment_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    rows = [
        row
        for row in rows
        if not (
            row["panel_case_id"] == "MFB_PANEL_001"
            and row["reviewer_code"] == "R02"
        )
    ]
    rewrite_tsv(assignment_path, rows, fieldnames)

    errors = validate(root)

    assert any("MFB_PANEL_001 must be assigned to R01, R02" in error for error in errors)


def test_clinician_panel_readiness_manifest_rejects_patient_data_flag(
    tmp_path: Path,
) -> None:
    root = copy_manifest_tree(tmp_path)
    case_path = root / "data/panel_pilot/clinician_panel_pilot_cases_v0_1.tsv"
    with case_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    rows[0]["patient_data_status"] = "synthetic with possible patient data"
    rewrite_tsv(case_path, rows, fieldnames)

    errors = validate(root)

    assert any("patient_data_status must be synthetic only" in error for error in errors)
