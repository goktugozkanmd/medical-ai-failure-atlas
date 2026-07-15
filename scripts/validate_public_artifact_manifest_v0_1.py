#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = Path("docs/release/PUBLIC_ARTIFACT_MANIFEST_V0_1.json")

SCHEMA_VERSION = "public_artifact_manifest_v0_1"
STATUS = "reviewed_public_boundary"
REQUIRED_BLOCKED_CLAIMS = [
    "no_patient_data",
    "no_clinical_validation_claim",
    "no_model_ranking_claim",
    "no_deployment_or_diagnosis_claim",
    "no_unverified_policy_citation",
]
ALLOWED_RELEASE_STATES = {
    "reviewed_public_surface",
    "reviewed_public_data",
    "reviewed_preprint_surface",
}


def _load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"{path}: missing manifest"]
    except json.JSONDecodeError as exc:
        return None, [f"{path}: invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{path}: manifest root must be an object"]
    return data, []


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(raw_path: Any) -> tuple[Path | None, str | None]:
    if not isinstance(raw_path, str) or not raw_path:
        return None, "path must be a non-empty string"
    rel_path = Path(raw_path)
    if rel_path.is_absolute() or ".." in rel_path.parts:
        return None, f"{raw_path}: path must stay inside the repository"
    return rel_path, None


def validate(root: Path = ROOT, manifest_path: Path = DEFAULT_MANIFEST) -> list[str]:
    manifest_file = root / manifest_path
    manifest, errors = _load_json(manifest_file)
    if manifest is None:
        return errors

    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{manifest_path}: schema_version must be {SCHEMA_VERSION!r}")
    if manifest.get("status") != STATUS:
        errors.append(f"{manifest_path}: status must be {STATUS!r}")
    if manifest.get("blocked_claims_required") != REQUIRED_BLOCKED_CLAIMS:
        errors.append(f"{manifest_path}: blocked_claims_required changed or reordered")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(f"{manifest_path}: artifacts must be a non-empty list")
        return errors

    seen_paths: set[str] = set()
    for index, artifact in enumerate(artifacts):
        prefix = f"{manifest_path}:artifacts[{index}]"
        if not isinstance(artifact, dict):
            errors.append(f"{prefix}: artifact must be an object")
            continue

        rel_path, path_error = _safe_relative_path(artifact.get("path"))
        if path_error:
            errors.append(f"{prefix}: {path_error}")
            continue
        assert rel_path is not None

        rel_path_text = rel_path.as_posix()
        if rel_path_text in seen_paths:
            errors.append(f"{prefix}: duplicate path {rel_path_text}")
            continue
        seen_paths.add(rel_path_text)

        release_state = artifact.get("release_state")
        if release_state not in ALLOWED_RELEASE_STATES:
            errors.append(
                f"{prefix}: release_state must be one of {sorted(ALLOWED_RELEASE_STATES)}"
            )

        blocked_claims = artifact.get("blocked_claims")
        if not isinstance(blocked_claims, dict):
            errors.append(f"{prefix}: blocked_claims must be an object")
        else:
            for claim in REQUIRED_BLOCKED_CLAIMS:
                if blocked_claims.get(claim) is not True:
                    errors.append(f"{prefix}: blocked_claims.{claim} must be true")

        expected_sha = artifact.get("sha256")
        if not isinstance(expected_sha, str) or not re.fullmatch(
            r"[0-9a-f]{64}", expected_sha
        ):
            errors.append(f"{prefix}: sha256 must be 64 lowercase hex characters")
            continue

        file_path = root / rel_path
        if not file_path.is_file():
            errors.append(f"{prefix}: missing artifact {rel_path_text}")
            continue

        actual_sha = _sha256(file_path)
        if actual_sha != expected_sha:
            errors.append(
                f"{prefix}: sha256 mismatch for {rel_path_text}: "
                f"expected {expected_sha}, got {actual_sha}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the reviewed public artifact manifest."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    errors = validate(args.root, args.manifest)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1

    print("PASS public artifact manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
