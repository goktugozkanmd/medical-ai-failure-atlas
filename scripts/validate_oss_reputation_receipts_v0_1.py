#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = Path("docs/release/OSS_REPUTATION_RECEIPTS_V0_1.json")

SCHEMA_VERSION = "oss_reputation_receipts_v0_1"
STATUS = "live_review_snapshot_not_acceptance"
REQUIRED_BOUNDARY_FLAGS = {
    "no_upstream_acceptance_without_merge": True,
    "no_official_endorsement_claim": True,
    "no_clinical_validation_claim": True,
    "no_model_ranking_claim": True,
    "pending_review_is_not_acceptance": True,
}
ALLOWED_SCOPES = {"main_project", "upstream", "external"}
ALLOWED_TYPES = {"pull_request", "issue", "discussion"}
ALLOWED_STATES = {"open", "closed", "merged"}
ALLOWED_ACCEPTANCE_STATES = {
    "pending_review",
    "closed_no_merge",
    "internal_merged",
    "merged_upstream",
    "issue_open_pending",
    "issue_closed_no_action",
}
GITHUB_URL_RE = re.compile(
    r"^https://github\.com/"
    r"(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)/"
    r"(?P<kind>pull|issues|discussions)/(?P<number>[0-9]+)$"
)
URL_KIND_TO_CONTRIBUTION_TYPE = {
    "pull": "pull_request",
    "issues": "issue",
    "discussions": "discussion",
}


def validate(root: Path = ROOT, manifest_path: Path = DEFAULT_MANIFEST) -> list[str]:
    manifest_file = root / manifest_path
    manifest, errors = _load_json(manifest_file)
    if manifest is None:
        return errors

    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{manifest_path}: schema_version must be {SCHEMA_VERSION!r}")
    if manifest.get("status") != STATUS:
        errors.append(f"{manifest_path}: status must be {STATUS!r}")
    _validate_timestamp(manifest.get("reviewed_at"), f"{manifest_path}:reviewed_at", errors)

    boundary_flags = manifest.get("boundary_flags")
    if not isinstance(boundary_flags, dict):
        errors.append(f"{manifest_path}: boundary_flags must be an object")
    else:
        for key, expected in REQUIRED_BOUNDARY_FLAGS.items():
            if boundary_flags.get(key) is not expected:
                errors.append(f"{manifest_path}: boundary_flags.{key} must be {expected!r}")

    receipts = manifest.get("receipts")
    if not isinstance(receipts, list) or not receipts:
        errors.append(f"{manifest_path}: receipts must be a non-empty list")
        return errors

    seen_urls: set[str] = set()
    seen_repo_numbers: set[tuple[str, int, str]] = set()
    for index, receipt in enumerate(receipts):
        prefix = f"{manifest_path}:receipts[{index}]"
        if not isinstance(receipt, dict):
            errors.append(f"{prefix}: receipt must be an object")
            continue
        _validate_receipt(prefix, receipt, seen_urls, seen_repo_numbers, errors)

    return errors


def _load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"{path}: missing manifest"]
    except json.JSONDecodeError as exc:
        return None, [f"{path}: invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return None, [f"{path}: manifest root must be an object"]
    return payload, []


def _validate_receipt(
    prefix: str,
    receipt: dict[str, Any],
    seen_urls: set[str],
    seen_repo_numbers: set[tuple[str, int, str]],
    errors: list[str],
) -> None:
    repository = receipt.get("repository")
    if not isinstance(repository, str) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository
    ):
        errors.append(f"{prefix}: repository must be owner/name")
        repository = ""

    number = receipt.get("number")
    if not isinstance(number, int) or number <= 0:
        errors.append(f"{prefix}: number must be a positive integer")
        number = -1

    url = receipt.get("url")
    url_match = GITHUB_URL_RE.fullmatch(url) if isinstance(url, str) else None
    if not url_match:
        errors.append(f"{prefix}: url must be a GitHub pull, issue, or discussion URL")
        url = ""
    elif url in seen_urls:
        errors.append(f"{prefix}: duplicate url {url}")
    else:
        seen_urls.add(url)

    scope = _require_enum(prefix, receipt, "scope", ALLOWED_SCOPES, errors)
    contribution_type = _require_enum(
        prefix, receipt, "contribution_type", ALLOWED_TYPES, errors
    )
    state = _require_enum(prefix, receipt, "state", ALLOWED_STATES, errors)
    acceptance_state = _require_enum(
        prefix, receipt, "acceptance_state", ALLOWED_ACCEPTANCE_STATES, errors
    )
    accepted_upstream = receipt.get("accepted_upstream")
    if not isinstance(accepted_upstream, bool):
        errors.append(f"{prefix}: accepted_upstream must be a boolean")

    if repository and number > 0 and contribution_type:
        identity = (repository, number, contribution_type)
        if identity in seen_repo_numbers:
            errors.append(f"{prefix}: duplicate repository/number/type {identity}")
        else:
            seen_repo_numbers.add(identity)

    if url_match:
        url_repository = f"{url_match.group('owner')}/{url_match.group('repo')}"
        url_number = int(url_match.group("number"))
        url_contribution_type = URL_KIND_TO_CONTRIBUTION_TYPE[url_match.group("kind")]
        if repository and repository != url_repository:
            errors.append(f"{prefix}: url repository must match repository")
        if number > 0 and number != url_number:
            errors.append(f"{prefix}: url number must match number")
        if contribution_type and contribution_type != url_contribution_type:
            errors.append(f"{prefix}: url type must match contribution_type")

    _validate_timestamp(
        receipt.get("last_verified_at"), f"{prefix}:last_verified_at", errors
    )
    _validate_evidence(prefix, receipt.get("evidence"), errors)
    _validate_claim_boundary(
        prefix=prefix,
        scope=scope,
        contribution_type=contribution_type,
        state=state,
        acceptance_state=acceptance_state,
        accepted_upstream=accepted_upstream,
        errors=errors,
    )


def _require_enum(
    prefix: str,
    receipt: dict[str, Any],
    field: str,
    allowed: set[str],
    errors: list[str],
) -> str | None:
    value = receipt.get(field)
    if value not in allowed:
        errors.append(f"{prefix}: {field} must be one of {sorted(allowed)}")
        return None
    return value


def _validate_timestamp(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        errors.append(f"{label} must be an ISO-8601 UTC timestamp ending in Z")
        return
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} must be a valid ISO-8601 UTC timestamp")
        return
    if parsed.tzinfo != UTC:
        errors.append(f"{label} must use UTC")


def _validate_evidence(prefix: str, evidence: Any, errors: list[str]) -> None:
    if not isinstance(evidence, dict):
        errors.append(f"{prefix}: evidence must be an object")
        return
    for field in ("command", "result"):
        value = evidence.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{prefix}: evidence.{field} must be a non-empty string")


def _validate_claim_boundary(
    *,
    prefix: str,
    scope: str | None,
    contribution_type: str | None,
    state: str | None,
    acceptance_state: str | None,
    accepted_upstream: Any,
    errors: list[str],
) -> None:
    if contribution_type == "pull_request" and state == "open":
        if acceptance_state != "pending_review":
            errors.append(f"{prefix}: open pull requests must be pending_review")
        if accepted_upstream is not False:
            errors.append(f"{prefix}: open pull requests must not claim upstream acceptance")

    if contribution_type == "pull_request" and state == "closed":
        if acceptance_state != "closed_no_merge":
            errors.append(f"{prefix}: closed pull requests must be closed_no_merge")
        if accepted_upstream is not False:
            errors.append(f"{prefix}: closed pull requests must not claim upstream acceptance")

    if contribution_type == "pull_request" and state == "merged":
        if scope == "main_project":
            if acceptance_state != "internal_merged":
                errors.append(f"{prefix}: main_project merges must be internal_merged")
            if accepted_upstream is not False:
                errors.append(f"{prefix}: main_project merge is not upstream acceptance")
        elif scope in {"upstream", "external"}:
            if acceptance_state != "merged_upstream":
                errors.append(f"{prefix}: upstream/external merges must be merged_upstream")
            if accepted_upstream is not True:
                errors.append(f"{prefix}: merged upstream/external PR must mark accepted_upstream")

    if contribution_type in {"issue", "discussion"}:
        if state == "merged":
            errors.append(f"{prefix}: issues and discussions cannot use merged state")
        if state == "open":
            if acceptance_state != "issue_open_pending":
                errors.append(f"{prefix}: open issues/discussions must be issue_open_pending")
            if accepted_upstream is not False:
                errors.append(f"{prefix}: open issues/discussions must not claim acceptance")
        if state == "closed":
            if acceptance_state != "issue_closed_no_action":
                errors.append(
                    f"{prefix}: closed issues/discussions must be issue_closed_no_action"
                )
            if accepted_upstream is not False:
                errors.append(f"{prefix}: closed issues/discussions must not claim acceptance")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate OSS reputation receipt claim boundaries."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    errors = validate(args.root, args.manifest)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1

    print("PASS OSS reputation receipts manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
