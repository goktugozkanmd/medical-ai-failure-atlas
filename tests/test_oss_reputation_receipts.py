from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.validate_oss_reputation_receipts_v0_1 import DEFAULT_MANIFEST, validate


ROOT = Path(__file__).resolve().parents[1]


def copy_manifest(tmp_path: Path) -> Path:
    manifest_dst = tmp_path / DEFAULT_MANIFEST
    manifest_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / DEFAULT_MANIFEST, manifest_dst)
    return tmp_path


def read_manifest(root: Path) -> dict:
    return json.loads((root / DEFAULT_MANIFEST).read_text(encoding="utf-8"))


def rewrite_manifest(root: Path, manifest: dict) -> None:
    (root / DEFAULT_MANIFEST).write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def test_oss_reputation_receipts_accept_current_manifest() -> None:
    assert validate(ROOT) == []


def test_oss_reputation_receipts_reject_open_acceptance_claim(tmp_path: Path) -> None:
    root = copy_manifest(tmp_path)
    manifest = read_manifest(root)
    manifest["receipts"][1]["accepted_upstream"] = True
    rewrite_manifest(root, manifest)

    errors = validate(root)

    assert any("open pull requests must not claim upstream acceptance" in error for error in errors)


def test_oss_reputation_receipts_reject_closed_pending_review(tmp_path: Path) -> None:
    root = copy_manifest(tmp_path)
    manifest = read_manifest(root)
    manifest["receipts"][5]["acceptance_state"] = "pending_review"
    rewrite_manifest(root, manifest)

    errors = validate(root)

    assert any("closed pull requests must be closed_no_merge" in error for error in errors)


def test_oss_reputation_receipts_reject_duplicate_url(tmp_path: Path) -> None:
    root = copy_manifest(tmp_path)
    manifest = read_manifest(root)
    manifest["receipts"].append(dict(manifest["receipts"][0]))
    rewrite_manifest(root, manifest)

    errors = validate(root)

    assert any("duplicate url" in error for error in errors)


def test_oss_reputation_receipts_require_boundary_flags(tmp_path: Path) -> None:
    root = copy_manifest(tmp_path)
    manifest = read_manifest(root)
    manifest["boundary_flags"]["pending_review_is_not_acceptance"] = False
    rewrite_manifest(root, manifest)

    errors = validate(root)

    assert any("boundary_flags.pending_review_is_not_acceptance must be True" in error for error in errors)


def test_oss_reputation_receipts_reject_non_github_url(tmp_path: Path) -> None:
    root = copy_manifest(tmp_path)
    manifest = read_manifest(root)
    manifest["receipts"][0]["url"] = "https://example.com/not-a-receipt"
    rewrite_manifest(root, manifest)

    errors = validate(root)

    assert any("url must be a GitHub pull, issue, or discussion URL" in error for error in errors)
