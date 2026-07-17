#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from failure_atlas.panel_review import (  # noqa: E402
    load_panel_cases,
    load_rating_template,
    reviewer_codes,
)


DEFAULT_MANIFEST = Path("docs/CLINICIAN_PANEL_READINESS_MANIFEST_V0_1.json")
SCHEMA_VERSION = "clinician_panel_readiness_manifest_v0_1"
STATUS = "controlled_local_review_ready_not_complete"
REVIEWER_CODES = ["R01", "R02"]
REQUIRED_BOUNDARY_FLAGS = {
    "contains_patient_data": False,
    "synthetic_examples_only": True,
    "not_for_clinical_use": True,
    "no_clinical_validation_claim": True,
    "no_model_safety_claim": True,
    "no_model_ranking": True,
    "no_clinical_deployment_claim": True,
    "no_regulatory_approval_claim": True,
    "no_official_endorsement_claim": True,
    "external_send_allowed": False,
    "requires_owner_approval_before_send": True,
}
REQUIRED_ARTIFACT_ROLES = {
    "clinician_review_protocol",
    "reviewer_packet",
    "reviewer_message_draft",
    "internal_audit_note",
    "packet_boundary_json",
    "panel_case_table",
    "panel_assignment_sheet",
    "panel_review_module",
    "panel_console_module",
}
BLOCKED_PUBLIC_CLAIMS = {
    "panel_review_complete",
    "clinical_validation",
    "model_safety",
    "model_ranking",
    "clinical_deployment_readiness",
    "regulatory_approval",
    "official_endorsement",
    "real_patient_data_use",
}


def validate(root: Path = ROOT, manifest_path: Path = DEFAULT_MANIFEST) -> list[str]:
    errors: list[str] = []
    manifest_file = root / manifest_path
    manifest = _read_manifest(manifest_file, errors)
    if manifest is None:
        return errors

    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{manifest_path}: schema_version must be {SCHEMA_VERSION!r}")
    if manifest.get("status") != STATUS:
        errors.append(f"{manifest_path}: status must be {STATUS!r}")
    if manifest.get("panel_claim_state") != "not_complete":
        errors.append(f"{manifest_path}: panel_claim_state must stay 'not_complete'")
    if manifest.get("reviewer_codes") != REVIEWER_CODES:
        errors.append(f"{manifest_path}: reviewer_codes must be {REVIEWER_CODES!r}")
    if manifest.get("minimum_completed_reviewers_for_panel_claim") != 2:
        errors.append(
            f"{manifest_path}: minimum_completed_reviewers_for_panel_claim must be 2"
        )

    boundary_flags = manifest.get("boundary_flags")
    if not isinstance(boundary_flags, dict):
        errors.append(f"{manifest_path}: boundary_flags must be an object")
    else:
        for key, expected in REQUIRED_BOUNDARY_FLAGS.items():
            if boundary_flags.get(key) is not expected:
                errors.append(f"{manifest_path}: boundary_flags.{key} must be {expected!r}")

    blocked_public_claims = manifest.get("blocked_public_claims")
    if not isinstance(blocked_public_claims, list):
        errors.append(f"{manifest_path}: blocked_public_claims must be a list")
    elif set(blocked_public_claims) != BLOCKED_PUBLIC_CLAIMS:
        errors.append(f"{manifest_path}: blocked_public_claims must match the locked set")

    artifact_paths = _validate_artifacts(root, manifest_path, manifest, errors)
    case_path = artifact_paths.get("panel_case_table")
    assignment_path = artifact_paths.get("panel_assignment_sheet")
    if case_path and assignment_path:
        _validate_panel_assignment_contract(
            root=root,
            manifest_path=manifest_path,
            manifest=manifest,
            case_path=case_path,
            assignment_path=assignment_path,
            errors=errors,
        )

    return errors


def _read_manifest(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path}: missing manifest")
        return None
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}: manifest root must be an object")
        return None
    return payload


def _safe_relative_path(raw_path: Any) -> tuple[Path | None, str | None]:
    if not isinstance(raw_path, str) or not raw_path:
        return None, "path must be a non-empty string"
    rel_path = Path(raw_path)
    if rel_path.is_absolute() or ".." in rel_path.parts:
        return None, f"{raw_path}: path must stay inside the repository"
    return rel_path, None


def _validate_artifacts(
    root: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    errors: list[str],
) -> dict[str, Path]:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(f"{manifest_path}: artifacts must be a non-empty list")
        return {}

    seen_roles: set[str] = set()
    seen_paths: set[str] = set()
    artifact_paths: dict[str, Path] = {}
    for index, artifact in enumerate(artifacts):
        prefix = f"{manifest_path}:artifacts[{index}]"
        if not isinstance(artifact, dict):
            errors.append(f"{prefix}: artifact must be an object")
            continue

        role = artifact.get("role")
        if not isinstance(role, str) or not role:
            errors.append(f"{prefix}: role must be a non-empty string")
            continue
        if role in seen_roles:
            errors.append(f"{prefix}: duplicate role {role}")
            continue
        seen_roles.add(role)

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

        if not (root / rel_path).exists():
            errors.append(f"{prefix}: missing artifact {rel_path_text}")
            continue
        artifact_paths[role] = rel_path

    missing_roles = sorted(REQUIRED_ARTIFACT_ROLES - seen_roles)
    if missing_roles:
        errors.append(f"{manifest_path}: missing artifact roles: {', '.join(missing_roles)}")
    return artifact_paths


def _validate_panel_assignment_contract(
    *,
    root: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    case_path: Path,
    assignment_path: Path,
    errors: list[str],
) -> None:
    try:
        cases = load_panel_cases(root / case_path)
        assignments = load_rating_template(root / assignment_path)
    except Exception as exc:  # noqa: BLE001 - surface schema validation errors as manifest errors.
        errors.append(f"{manifest_path}: panel assignment files failed to load: {exc}")
        return

    if manifest.get("case_count") != len(cases):
        errors.append(f"{manifest_path}: case_count must match {case_path}")
    if manifest.get("assignment_count") != len(assignments):
        errors.append(f"{manifest_path}: assignment_count must match {assignment_path}")
    if manifest.get("required_cases_per_reviewer") != len(cases):
        errors.append(f"{manifest_path}: required_cases_per_reviewer must equal case_count")
    if reviewer_codes(assignments) != REVIEWER_CODES:
        errors.append(f"{assignment_path}: reviewer codes must be {REVIEWER_CODES!r}")

    case_ids = {case.panel_case_id for case in cases}
    for case in cases:
        if case.patient_data_status != "synthetic only; no patient data":
            errors.append(
                f"{case_path}: {case.panel_case_id} patient_data_status must be synthetic only"
            )
        if case.rating_status != "not yet rated":
            errors.append(f"{case_path}: {case.panel_case_id} must not claim a rating yet")

    assignments_by_case = {case_id: set() for case_id in case_ids}
    assignments_by_reviewer = {reviewer: set() for reviewer in REVIEWER_CODES}
    for row in assignments:
        case_id = row["panel_case_id"]
        reviewer = row["reviewer_code"]
        if case_id not in case_ids:
            errors.append(f"{assignment_path}: assignment references unknown case {case_id}")
            continue
        assignments_by_case[case_id].add(reviewer)
        if reviewer in assignments_by_reviewer:
            assignments_by_reviewer[reviewer].add(case_id)
        if row["possible_patient_data_flag"] != "no":
            errors.append(
                f"{assignment_path}: {case_id}/{reviewer} possible_patient_data_flag must be no"
            )

    for case_id, assigned_reviewers in assignments_by_case.items():
        if assigned_reviewers != set(REVIEWER_CODES):
            errors.append(
                f"{assignment_path}: {case_id} must be assigned to {', '.join(REVIEWER_CODES)}"
            )
    for reviewer, assigned_cases in assignments_by_reviewer.items():
        if assigned_cases != case_ids:
            errors.append(f"{assignment_path}: {reviewer} must cover every panel case")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the clinician panel readiness manifest."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    errors = validate(args.root, args.manifest)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1

    print("PASS clinician panel readiness manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
