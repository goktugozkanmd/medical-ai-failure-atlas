from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.validate_public_artifact_manifest_v0_1 import DEFAULT_MANIFEST, validate


ROOT = Path(__file__).resolve().parents[1]


def copy_manifest_tree(tmp_path: Path) -> Path:
    manifest_src = ROOT / DEFAULT_MANIFEST
    manifest = json.loads(manifest_src.read_text(encoding="utf-8"))

    manifest_dst = tmp_path / DEFAULT_MANIFEST
    manifest_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(manifest_src, manifest_dst)

    for artifact in manifest["artifacts"]:
        src = ROOT / artifact["path"]
        dst = tmp_path / artifact["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)

    return tmp_path


def rewrite_manifest(root: Path, manifest: dict) -> None:
    (root / DEFAULT_MANIFEST).write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def read_manifest(root: Path) -> dict:
    return json.loads((root / DEFAULT_MANIFEST).read_text(encoding="utf-8"))


def test_public_artifact_manifest_accepts_current_files() -> None:
    assert validate(ROOT) == []


def test_public_artifact_manifest_rejects_stale_hash(tmp_path: Path) -> None:
    root = copy_manifest_tree(tmp_path)
    readme = root / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\nreview drift\n",
        encoding="utf-8",
    )

    errors = validate(root)

    assert any("sha256 mismatch" in error for error in errors)


def test_public_artifact_manifest_requires_blocked_claims(tmp_path: Path) -> None:
    root = copy_manifest_tree(tmp_path)
    manifest = read_manifest(root)
    manifest["artifacts"][0]["blocked_claims"]["no_model_ranking_claim"] = False
    rewrite_manifest(root, manifest)

    errors = validate(root)

    assert any("blocked_claims.no_model_ranking_claim must be true" in error for error in errors)


def test_public_artifact_manifest_rejects_missing_artifact(tmp_path: Path) -> None:
    root = copy_manifest_tree(tmp_path)
    (root / "preprint/main.tex").unlink()

    errors = validate(root)

    assert any("missing artifact preprint/main.tex" in error for error in errors)


def test_public_artifact_manifest_rejects_duplicate_paths(tmp_path: Path) -> None:
    root = copy_manifest_tree(tmp_path)
    manifest = read_manifest(root)
    manifest["artifacts"].append(dict(manifest["artifacts"][0]))
    rewrite_manifest(root, manifest)

    errors = validate(root)

    assert any("duplicate path README.md" in error for error in errors)
