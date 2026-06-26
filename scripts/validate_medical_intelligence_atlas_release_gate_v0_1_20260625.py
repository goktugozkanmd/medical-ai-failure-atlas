#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_CANDIDATES = [
    ROOT / "data" / "medical_intelligence_atlas_release_gate_v0_1_20260625.json",
    ROOT / "data" / "medical_intelligence_atlas_release_gate_fixture_v0_1_20260625.json",
    ROOT / "docs" / "medical_intelligence_atlas_release_gate_v0_1_20260625.json",
    ROOT / "docs" / "medical_intelligence_atlas_release_gate_fixture_v0_1_20260625.json",
]
ATLAS_CONFIG = ROOT / "data" / "medical_intelligence_atlas_v0_1_20260625.json"

EXPECTED_LAYERS = {
    "Clinical State Language",
    "Clinical Trajectory Engine",
    "Medical Reasoning Verifier",
    "Agentic Medicine Sandbox",
    "Multilingual Medical Intelligence",
    "Medical Intelligence Atlas",
}
ALLOWED_READINESS_STATUSES = {"ready", "blocked", "needs source check"}
EXPECTED_RISK_GATE = "public release cannot outrun validators"
EXPECTED_ATLAS_NODE_COUNT = 88

ROW_KEYS = ("release_gate_rows", "gate_rows", "readiness_rows", "layers", "rows")
NEXT_ACTION_KEYS = ("expected_next_action", "exact_next_action")
READINESS_KEYS = ("readiness_status", "readiness_state", "status")
ARTIFACT_PATH_KEYS = ("artifact_path", "artifact_paths", "local_artifacts", "artifact")
EXTERNAL_URL_RE = re.compile(r"\b(?:https?://|www\.)", re.IGNORECASE)
EXPECTED_SOURCE_CHECK_RULE = "Source flags stay open unless repo local source review evidence exists."
EXPECTED_STATUS_CODES = {"ready", "blocked", "needs_source_check"}

FORBIDDEN_CLAIM_PATTERNS = {
    "clinical validation complete": "clinical validation completion claim",
    "clinically validated": "clinical validation claim",
    "validated for clinical use": "clinical validation claim",
    "clinical deployment ready": "clinical deployment readiness claim",
    "ready for clinical deployment": "clinical deployment readiness claim",
    "deployed for clinical use": "clinical deployment claim",
    "safe for clinical use": "clinical safety claim",
    "diagnosis provided": "diagnosis claim",
    "treatment recommendation provided": "treatment instruction claim",
    "model superiority proven": "model superiority claim",
    "best model": "model ranking claim",
    "official endorsement": "endorsement claim",
    "partner confirmed": "partner confirmation claim",
    "institutional support confirmed": "institutional support claim",
    "payment completed": "payment completion claim",
    "terms accepted": "terms acceptance claim",
    "patient data used true": "patient data use claim",
    "patient data used: true": "patient data use claim",
}

CLAIM_SCAN_SKIP_PARTS = {
    "blocked_claims",
    "blocked_wording",
    "forbidden_claims",
    "forbidden_phrases",
    "global_boundaries",
}


def repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_fixture(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    try:
        if path.suffix == ".jsonl":
            rows = []
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                item = json.loads(line)
                if not isinstance(item, dict):
                    errors.append(f"{repo_relative(path)} line {line_number}: row must be an object")
                    continue
                rows.append(item)
            return {}, rows, errors

        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return {}, [], [f"{repo_relative(path)}: invalid JSON: {error}"]

    if isinstance(payload, list):
        rows = [item for item in payload if isinstance(item, dict)]
        if len(rows) != len(payload):
            errors.append("Fixture list entries must all be objects")
        return {}, rows, errors

    if not isinstance(payload, dict):
        return {}, [], ["Fixture root must be an object, a list of row objects, or JSONL row objects"]

    rows = []
    for key in ROW_KEYS:
        if key in payload:
            candidate = payload[key]
            if isinstance(candidate, list):
                rows = [item for item in candidate if isinstance(item, dict)]
                if len(rows) != len(candidate):
                    errors.append(f"{key} entries must all be objects")
            else:
                errors.append(f"{key} must be a list")
            break
    if not rows and not any(key in payload for key in ROW_KEYS):
        errors.append(f"Fixture must include one row list key: {', '.join(ROW_KEYS)}")

    return payload, rows, errors


def select_fixture(explicit_fixture: str | None) -> tuple[Path | None, list[str]]:
    if explicit_fixture:
        path = Path(explicit_fixture)
        if not path.is_absolute():
            path = ROOT / path
        if not path.exists():
            return path, [f"Missing release gate fixture: {repo_relative(path)}"]
        return path, []

    matches = [path for path in FIXTURE_CANDIDATES if path.exists()]
    if not matches:
        expected = ", ".join(repo_relative(path) for path in FIXTURE_CANDIDATES)
        return None, [f"Missing release gate fixture. Expected one of: {expected}"]
    if len(matches) > 1:
        found = ", ".join(repo_relative(path) for path in matches)
        return matches[0], [f"Multiple release gate fixtures found; pass --fixture explicitly: {found}"]
    return matches[0], []


def extract_expected_next_action(payload: dict[str, Any], cli_value: str | None, errors: list[str]) -> str | None:
    if cli_value:
        return cli_value

    values = []
    for key in NEXT_ACTION_KEYS:
        value = payload.get(key)
        if value is not None:
            if isinstance(value, str) and value.strip():
                values.append(value)
            else:
                errors.append(f"{key} must be a non-empty string")

    if not values:
        return None
    if len(set(values)) != 1:
        errors.append("Expected next action fields disagree")
        return None
    return values[0]


def row_label(index: int, row: dict[str, Any]) -> str:
    for key in ("id", "gate_id", "release_gate_id", "layer"):
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    return f"row {index}"


def first_present(row: dict[str, Any], keys: tuple[str, ...]) -> tuple[str | None, Any]:
    for key in keys:
        if key in row:
            return key, row[key]
    return None, None


def artifact_paths(row: dict[str, Any]) -> list[str]:
    key, value = first_present(row, ARTIFACT_PATH_KEYS)
    if key is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    return []


def validate_artifact_path(value: str, label: str, errors: list[str]) -> None:
    if EXTERNAL_URL_RE.search(value):
        errors.append(f"{label}: artifact path must be a repo path, not an external URL: {value}")
        return

    candidate = Path(value)
    resolved = candidate.resolve() if candidate.is_absolute() else (ROOT / candidate).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        errors.append(f"{label}: artifact path points outside the repo: {value}")
        return

    if not resolved.exists():
        errors.append(f"{label}: artifact path does not exist: {value}")


def iter_strings(value: Any, path: str = "") -> list[tuple[str, str]]:
    if isinstance(value, str):
        return [(path, value)]
    if isinstance(value, dict):
        pairs: list[tuple[str, str]] = []
        for key, item in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            pairs.extend(iter_strings(item, child_path))
        return pairs
    if isinstance(value, list):
        pairs = []
        for index, item in enumerate(value):
            pairs.extend(iter_strings(item, f"{path}[{index}]"))
        return pairs
    return []


def should_scan_for_claims(path: str) -> bool:
    parts = set(re.split(r"[.\[\]]+", path))
    return not bool(parts & CLAIM_SCAN_SKIP_PARTS)


def validate_forbidden_claim_absence(payload: dict[str, Any], rows: list[dict[str, Any]], errors: list[str]) -> None:
    scan_root: Any = payload if payload else rows
    for path, text in iter_strings(scan_root):
        if EXTERNAL_URL_RE.search(text):
            errors.append(f"{path}: external URL is not allowed")

        if not should_scan_for_claims(path):
            continue
        lower = text.lower()
        for phrase, description in FORBIDDEN_CLAIM_PATTERNS.items():
            if phrase in lower:
                errors.append(f"{path}: forbidden {description}: {phrase}")


def validate_status_vocabulary(payload: dict[str, Any], rows: list[dict[str, Any]], errors: list[str]) -> None:
    vocabulary = payload.get("status_vocabulary")
    if vocabulary is not None:
        if not isinstance(vocabulary, list):
            errors.append("status_vocabulary must be a list")
        else:
            statuses = {str(item.get("status")) for item in vocabulary if isinstance(item, dict)}
            status_codes = {str(item.get("status_code")) for item in vocabulary if isinstance(item, dict)}
            if statuses != ALLOWED_READINESS_STATUSES:
                errors.append("status_vocabulary statuses must exactly match atlas release states")
            if status_codes != EXPECTED_STATUS_CODES:
                errors.append("status_vocabulary status_code values must exactly match expected machine values")

    summary = payload.get("release_gate_summary")
    if isinstance(summary, dict):
        if summary.get("layer_count") != len(EXPECTED_LAYERS):
            errors.append(f"release_gate_summary.layer_count must be {len(EXPECTED_LAYERS)}")
        status_counts = summary.get("status_counts")
        if isinstance(status_counts, dict):
            if set(status_counts) != ALLOWED_READINESS_STATUSES:
                errors.append("release_gate_summary.status_counts must include exactly the allowed readiness statuses")
            counted = sum(value for value in status_counts.values() if isinstance(value, int))
            if counted != len(rows):
                errors.append("release_gate_summary.status_counts must sum to the row count")
        else:
            errors.append("release_gate_summary.status_counts must be an object")
        if summary.get("source_check_rule") != EXPECTED_SOURCE_CHECK_RULE:
            errors.append(f"release_gate_summary.source_check_rule must exactly equal: {EXPECTED_SOURCE_CHECK_RULE}")
        if summary.get("expected_atlas_node_count") != EXPECTED_ATLAS_NODE_COUNT:
            errors.append(f"release_gate_summary.expected_atlas_node_count must be {EXPECTED_ATLAS_NODE_COUNT}")

    atlas_layer_source = payload.get("atlas_layer_source")
    if isinstance(atlas_layer_source, dict):
        if atlas_layer_source.get("expected_node_count") != EXPECTED_ATLAS_NODE_COUNT:
            errors.append(f"atlas_layer_source.expected_node_count must be {EXPECTED_ATLAS_NODE_COUNT}")


def validate_source_policy(payload: dict[str, Any], errors: list[str]) -> None:
    policy = payload.get("source_policy")
    if policy is None:
        return
    if not isinstance(policy, dict):
        errors.append("source_policy must be an object")
        return

    expected_flags = {
        "external_urls_allowed": False,
        "patient_data_allowed": False,
        "care_use_claims_allowed": False,
        "model_ranking_claims_allowed": False,
        "synthetic_boundary_required": True,
    }
    for key, expected in expected_flags.items():
        if policy.get(key) is not expected:
            errors.append(f"source_policy.{key} must be {expected}")


def validate_boundary_gate(row: dict[str, Any], label: str, errors: list[str]) -> None:
    boundary = row.get("synthetic_boundary")
    if not isinstance(boundary, dict):
        errors.append(f"{label}: missing risk_gate or synthetic_boundary gate")
        return

    expected_flags = {
        "synthetic_only": True,
        "patient_data_used": False,
        "clinical_use_allowed": False,
    }
    for key, expected in expected_flags.items():
        if boundary.get(key) is not expected:
            errors.append(f"{label}: synthetic_boundary.{key} must be {expected}")


def validate_gate_inputs(row: dict[str, Any], label: str, errors: list[str]) -> None:
    gate_inputs = row.get("gate_inputs")
    if not isinstance(gate_inputs, dict):
        return
    if "atlas_nodes" in gate_inputs and gate_inputs.get("atlas_nodes") != EXPECTED_ATLAS_NODE_COUNT:
        errors.append(f"{label}: gate_inputs.atlas_nodes must be {EXPECTED_ATLAS_NODE_COUNT}")


def atlas_node_ids_by_layer(errors: list[str]) -> dict[str, list[str]]:
    if not ATLAS_CONFIG.exists():
        errors.append(f"Missing atlas config: {repo_relative(ATLAS_CONFIG)}")
        return {}
    try:
        payload = json.loads(ATLAS_CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        errors.append(f"{repo_relative(ATLAS_CONFIG)}: invalid JSON: {error}")
        return {}

    nodes = payload.get("nodes")
    if not isinstance(nodes, list):
        errors.append("Atlas config nodes must be a list")
        return {}
    if len(nodes) != EXPECTED_ATLAS_NODE_COUNT:
        errors.append(f"Atlas config node count must be {EXPECTED_ATLAS_NODE_COUNT}")

    by_layer: dict[str, list[str]] = {}
    for node in nodes:
        if not isinstance(node, dict):
            continue
        layer = node.get("layer")
        node_id = node.get("id")
        if isinstance(layer, str) and isinstance(node_id, str):
            by_layer.setdefault(layer, []).append(node_id)
    return by_layer


def validate_atlas_node_id_continuity(rows: list[dict[str, Any]], errors: list[str]) -> None:
    expected_by_layer = atlas_node_ids_by_layer(errors)
    if not expected_by_layer:
        return

    for row in rows:
        layer = row.get("layer")
        if layer not in expected_by_layer:
            continue
        expected_ids = expected_by_layer[layer]
        row_ids = row.get("atlas_node_ids")
        if row_ids is not None and row_ids != expected_ids:
            errors.append(f"{layer}: atlas_node_ids must match Medical Intelligence Atlas node ids")

        gate_inputs = row.get("gate_inputs")
        if isinstance(gate_inputs, dict) and "atlas_node_ids" in gate_inputs:
            if gate_inputs.get("atlas_node_ids") != expected_ids:
                errors.append(f"{layer}: gate_inputs.atlas_node_ids must match Medical Intelligence Atlas node ids")


def validate_next_action(
    row: dict[str, Any],
    label: str,
    readiness_value: Any,
    expected_next_action: str | None,
    errors: list[str],
) -> None:
    next_action = row.get("next_action")
    if expected_next_action is not None:
        if next_action != expected_next_action:
            errors.append(f"{label}: next_action must exactly equal: {expected_next_action}")
        return

    if next_action is not None:
        if not isinstance(next_action, str) or not next_action.strip():
            errors.append(f"{label}: next_action must be a non-empty string")
        return

    if readiness_value == "blocked":
        blockers = row.get("blockers")
        if not isinstance(blockers, list) or not blockers:
            errors.append(f"{label}: blocked rows must include exact blockers when next_action is absent")
    elif readiness_value == "needs source check":
        source_check_items = row.get("source_check_items")
        if not isinstance(source_check_items, list) or not source_check_items:
            errors.append(f"{label}: needs source check rows must include exact source_check_items when next_action is absent")


def validate_rows(rows: list[dict[str, Any]], expected_next_action: str | None, errors: list[str]) -> None:
    if not rows:
        errors.append("Release gate fixture contains no rows")
        return

    layers: set[str] = set()
    for index, row in enumerate(rows, 1):
        label = row_label(index, row)

        layer = row.get("layer")
        if not isinstance(layer, str) or not layer.strip():
            errors.append(f"{label}: layer must be a non-empty string")
        else:
            layers.add(layer)

        paths = artifact_paths(row)
        if not paths:
            errors.append(f"{label}: missing artifact_path or artifact_paths")
        for value in paths:
            validate_artifact_path(value, label, errors)

        readiness_key, readiness_value = first_present(row, READINESS_KEYS)
        if readiness_key is None:
            errors.append(f"{label}: missing readiness_status")
        elif readiness_value not in ALLOWED_READINESS_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_READINESS_STATUSES))
            errors.append(f"{label}: {readiness_key} must be one of: {allowed}")

        validate_next_action(row, label, readiness_value, expected_next_action, errors)

        risk_gate = row.get("risk_gate")
        if risk_gate is None:
            validate_boundary_gate(row, label, errors)
        elif risk_gate != EXPECTED_RISK_GATE:
            errors.append(f"{label}: risk_gate must exactly equal: {EXPECTED_RISK_GATE}")
        validate_gate_inputs(row, label, errors)

    missing_layers = sorted(EXPECTED_LAYERS - layers)
    extra_layers = sorted(layers - EXPECTED_LAYERS)
    if missing_layers:
        errors.append(f"Missing layer coverage: {', '.join(missing_layers)}")
    if extra_layers:
        errors.append(f"Unexpected layer coverage: {', '.join(extra_layers)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", help="Path to a Medical Intelligence Atlas release gate fixture")
    parser.add_argument(
        "--expected-next-action",
        help="Exact next_action value to require in every release gate row",
    )
    args = parser.parse_args()

    errors: list[str] = []
    fixture, fixture_errors = select_fixture(args.fixture)
    errors.extend(fixture_errors)

    payload: dict[str, Any] = {}
    rows: list[dict[str, Any]] = []
    if fixture and fixture.exists() and not fixture_errors:
        payload, rows, load_errors = load_fixture(fixture)
        errors.extend(load_errors)

        expected_next_action = extract_expected_next_action(payload, args.expected_next_action, errors)
        if payload.get("expected_risk_gate") not in (None, EXPECTED_RISK_GATE):
            errors.append(f"expected_risk_gate must exactly equal: {EXPECTED_RISK_GATE}")
        validate_status_vocabulary(payload, rows, errors)
        validate_source_policy(payload, errors)
        validate_rows(rows, expected_next_action, errors)
        validate_atlas_node_id_continuity(rows, errors)
        validate_forbidden_claim_absence(payload, rows, errors)

    if errors:
        print("FAIL Medical Intelligence Atlas release gate validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Medical Intelligence Atlas release gate validation")
    print(f"fixture={repo_relative(fixture)}")
    print(f"rows={len(rows)}")
    print(f"layers={len(EXPECTED_LAYERS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
