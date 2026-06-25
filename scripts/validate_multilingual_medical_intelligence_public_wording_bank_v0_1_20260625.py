#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_public_wording_bank_v0_1_20260625.jsonl"
)
DEFAULT_PAIRED_FIXTURE = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_paired_state_examples_v0_1_20260625.jsonl"
)
EXPECTED_ROW_COUNT = 8
EXPECTED_VERSION = "v0_1_20260625"
EXPECTED_LAYER = "Multilingual Medical Intelligence"
EXPECTED_NODE = "mia_mmi_002"
EXPECTED_LANGUAGE_PAIR = "Turkish English"

REQUIRED_FIELDS = {
    "row_id",
    "fixture_version",
    "atlas_layer",
    "atlas_node_id",
    "source_state_pair_id",
    "language_pair",
    "clinical_domain",
    "scenario_stub",
    "public_wording_en",
    "public_wording_tr_ascii",
    "plain_clinical_language_checks",
    "missing_data_to_preserve",
    "source_support_to_preserve",
    "unsafe_rewrite_to_avoid",
    "review_gate",
    "release_boundary",
}

REQUIRED_REVIEW_GATE_FLAGS = {
    "requires_human_review_before_public_claim": True,
    "source_support_required_before_pathway_claim": True,
    "blocks_if_missing_data_removed": True,
    "blocks_if_diagnosis_or_treatment_instruction_added": True,
}

REQUIRED_RELEASE_FLAGS = {
    "synthetic_only": True,
    "patient_data_used": False,
    "clinical_use_allowed": False,
    "clinical_deployment_claim_made": False,
    "clinical_validation_claim_made": False,
    "model_superiority_claim_made": False,
    "external_urls_present": False,
    "partner_or_institution_claim_made": False,
}

PUBLIC_WORDING_FIELDS = ("public_wording_en", "public_wording_tr_ascii")

EXTERNAL_URL_RE = re.compile(r"\b(?:https?://|www\.)", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_CANDIDATE_RE = re.compile(r"\+?\d[\d .()/\-]{8,}\d")

PRIVATE_IDENTIFIER_FIELD_NAMES = {
    "address",
    "date_of_birth",
    "dob",
    "birthdate",
    "email",
    "email_address",
    "full_name",
    "home_address",
    "insurance_number",
    "ip_address",
    "medical_record_number",
    "mrn",
    "national_id",
    "passport",
    "patient_id",
    "patient_name",
    "phone",
    "phone_number",
    "record_number",
    "social_security_number",
    "ssn",
    "street_address",
    "tc_kimlik",
    "tckn",
    "telephone",
}

PRIVATE_IDENTIFIER_VALUE_PATTERNS = {
    "date of birth": re.compile(r"\b(?:date of birth|birthdate|dob)\s*[:#]", re.IGNORECASE),
    "medical record number": re.compile(
        r"\b(?:mrn|medical record number|record number)\s*[:#]",
        re.IGNORECASE,
    ),
    "home address": re.compile(
        r"\b(?:home address|street address|apartment number)\s*[:#]",
        re.IGNORECASE,
    ),
    "passport": re.compile(r"\bpassport\s*(?:number)?\s*[:#]", re.IGNORECASE),
    "social security number": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "turkish national id": re.compile(
        r"\b(?:tckn|tc kimlik|t\.c\. kimlik)\s*(?:no|number)?\s*[:#]?\s*\d",
        re.IGNORECASE,
    ),
    "long numeric identifier": re.compile(r"\b\d{11,}\b"),
}

FORBIDDEN_CLAIM_PATTERNS = {
    "clinical validation complete": "clinical validation completion claim",
    "clinical validation passed": "clinical validation claim",
    "clinically validated": "clinical validation claim",
    "validated for clinical use": "clinical validation claim",
    "clinical deployment ready": "clinical deployment readiness claim",
    "ready for clinical deployment": "clinical deployment readiness claim",
    "deployed for clinical use": "clinical deployment claim",
    "safe for clinical use": "clinical safety claim",
    "diagnosis provided": "diagnosis claim",
    "treatment recommendation provided": "treatment instruction claim",
    "model superiority proven": "model superiority claim",
    "superior model": "model superiority claim",
    "best model": "model ranking claim",
    "outperforms all models": "model superiority claim",
    "partner confirmed": "partner claim",
    "partnership confirmed": "partner claim",
    "official partner": "partner claim",
    "institutional support confirmed": "institutional support claim",
    "payment completed": "payment claim",
    "payment confirmed": "payment claim",
    "terms accepted": "terms claim",
    "terms agreed": "terms claim",
}

PATIENT_FACING_INSTRUCTION_RE = re.compile(
    r"\b("
    r"you should|you must|you need to|start taking|stop taking|change your dose|"
    r"take this medicine|wait at home|go to the hospital|go to emergency|"
    r"evde bekle|ilaci al|ilaci birak|dozu degistir|hastaneye git"
    r")\b",
    re.IGNORECASE,
)


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return ROOT / path


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"{repo_relative(path)} line {line_number}: invalid JSON: {error}"
            ) from error
        if not isinstance(row, dict):
            raise ValueError(f"{repo_relative(path)} line {line_number}: row must be an object")
        rows.append(row)
    return rows


def normalized_key(key: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(key).strip().lower()).strip("_")


def iter_string_values(value: Any, path: str = "") -> list[tuple[str, str]]:
    if isinstance(value, str):
        return [(path, value)]
    if isinstance(value, dict):
        pairs: list[tuple[str, str]] = []
        for key, item in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            pairs.extend(iter_string_values(item, child_path))
        return pairs
    if isinstance(value, list):
        pairs = []
        for index, item in enumerate(value, 1):
            pairs.extend(iter_string_values(item, f"{path}[{index}]"))
        return pairs
    return []


def iter_keys(value: Any, path: str = "") -> list[tuple[str, str]]:
    if isinstance(value, dict):
        pairs: list[tuple[str, str]] = []
        for key, item in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            pairs.append((child_path, str(key)))
            pairs.extend(iter_keys(item, child_path))
        return pairs
    if isinstance(value, list):
        pairs = []
        for index, item in enumerate(value, 1):
            pairs.extend(iter_keys(item, f"{path}[{index}]"))
        return pairs
    return []


def has_phone_like_value(text: str) -> bool:
    for candidate in PHONE_CANDIDATE_RE.findall(text):
        digits = re.sub(r"\D", "", candidate)
        if len(digits) >= 10:
            return True
    return False


def validate_private_identifier_absence(row: dict[str, Any], label: str, errors: list[str]) -> None:
    for key_path, key in iter_keys(row):
        if normalized_key(key) in PRIVATE_IDENTIFIER_FIELD_NAMES:
            errors.append(f"{label}: private identifier field is not allowed: {key_path}")

    for value_path, text in iter_string_values(row):
        if EMAIL_RE.search(text):
            errors.append(f"{label}: email like value is not allowed at {value_path}")
        if has_phone_like_value(text):
            errors.append(f"{label}: phone like value is not allowed at {value_path}")
        for name, pattern in PRIVATE_IDENTIFIER_VALUE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label}: private identifier pattern '{name}' at {value_path}")


def validate_no_forbidden_claims(row: dict[str, Any], label: str, errors: list[str]) -> None:
    for value_path, text in iter_string_values(row):
        if EXTERNAL_URL_RE.search(text):
            errors.append(f"{label}: external URL is not allowed at {value_path}")
        lower = text.lower()
        for phrase, description in FORBIDDEN_CLAIM_PATTERNS.items():
            if phrase in lower:
                errors.append(f"{label}: forbidden {description} at {value_path}: {phrase}")


def validate_list_field(
    row: dict[str, Any],
    field: str,
    label: str,
    errors: list[str],
    minimum: int = 1,
) -> None:
    value = row.get(field)
    if not isinstance(value, list) or len(value) < minimum:
        errors.append(f"{label}: {field} must be a list with at least {minimum} item")
        return
    for index, item in enumerate(value, 1):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{label}: {field}[{index}] must be a non empty string")


def validate_public_wording_text(row: dict[str, Any], label: str, errors: list[str]) -> None:
    for field in PUBLIC_WORDING_FIELDS:
        text = row.get(field)
        if not isinstance(text, str) or not text.strip():
            errors.append(f"{label}: {field} must be a non empty string")
            continue
        if len(text.split()) < 12:
            errors.append(f"{label}: {field} is too short for a public wording fixture")
        if PATIENT_FACING_INSTRUCTION_RE.search(text):
            errors.append(f"{label}: {field} includes patient facing instruction wording")

    turkish_text = row.get("public_wording_tr_ascii", "")
    if isinstance(turkish_text, str) and not turkish_text.isascii():
        errors.append(f"{label}: public_wording_tr_ascii must be ASCII")


def validate_boundary_objects(row: dict[str, Any], label: str, errors: list[str]) -> None:
    gate = row.get("review_gate")
    if not isinstance(gate, dict):
        errors.append(f"{label}: review_gate must be an object")
    else:
        if gate.get("status") != "ready_for_local_fixture_use":
            errors.append(f"{label}: review_gate.status must be ready_for_local_fixture_use")
        for key, expected in REQUIRED_REVIEW_GATE_FLAGS.items():
            if gate.get(key) is not expected:
                errors.append(f"{label}: review_gate.{key} must be {expected}")

    boundary = row.get("release_boundary")
    if not isinstance(boundary, dict):
        errors.append(f"{label}: release_boundary must be an object")
        return

    for key, expected in REQUIRED_RELEASE_FLAGS.items():
        if boundary.get(key) is not expected:
            errors.append(f"{label}: release_boundary.{key} must be {expected}")

    allowed_use = boundary.get("allowed_use")
    not_allowed_use = boundary.get("not_allowed_use")
    if not isinstance(allowed_use, str) or "fixture" not in allowed_use.lower():
        errors.append(f"{label}: release_boundary.allowed_use must name fixture use")
    if not isinstance(not_allowed_use, str):
        errors.append(f"{label}: release_boundary.not_allowed_use must be a string")
    elif "patient care" not in not_allowed_use.lower():
        errors.append(f"{label}: release_boundary.not_allowed_use must block patient care")


def load_pair_ids(path: Path) -> set[str]:
    rows = load_jsonl(path)
    pair_ids: set[str] = set()
    for index, row in enumerate(rows, 1):
        pair_id = row.get("pair_id")
        if not isinstance(pair_id, str) or not pair_id.strip():
            raise ValueError(f"{repo_relative(path)} row {index}: missing pair_id")
        pair_ids.add(pair_id)
    return pair_ids


def validate_rows(rows: list[dict[str, Any]], pair_ids: set[str]) -> list[str]:
    errors: list[str] = []

    if len(rows) != EXPECTED_ROW_COUNT:
        errors.append(f"Expected {EXPECTED_ROW_COUNT} public wording rows, found {len(rows)}")

    seen: set[str] = set()
    used_pairs: set[str] = set()

    for index, row in enumerate(rows, 1):
        row_id = row.get("row_id")
        label = row_id if isinstance(row_id, str) and row_id else f"row {index}"

        missing_fields = sorted(REQUIRED_FIELDS - set(row))
        if missing_fields:
            errors.append(f"{label}: missing fields: {', '.join(missing_fields)}")
            continue

        if not isinstance(row_id, str) or not re.fullmatch(r"MMI_PUBLIC_WORDING_\d{3}", row_id):
            errors.append(f"{label}: row_id must match MMI_PUBLIC_WORDING_NNN")
        elif row_id in seen:
            errors.append(f"{label}: duplicate row_id")
        else:
            seen.add(row_id)

        if row.get("fixture_version") != EXPECTED_VERSION:
            errors.append(f"{label}: fixture_version must be {EXPECTED_VERSION}")
        if row.get("atlas_layer") != EXPECTED_LAYER:
            errors.append(f"{label}: atlas_layer must be {EXPECTED_LAYER}")
        if row.get("atlas_node_id") != EXPECTED_NODE:
            errors.append(f"{label}: atlas_node_id must be {EXPECTED_NODE}")
        if row.get("language_pair") != EXPECTED_LANGUAGE_PAIR:
            errors.append(f"{label}: language_pair must be {EXPECTED_LANGUAGE_PAIR}")

        source_pair = row.get("source_state_pair_id")
        if not isinstance(source_pair, str) or source_pair not in pair_ids:
            errors.append(f"{label}: source_state_pair_id must match an existing paired state row")
        else:
            used_pairs.add(source_pair)

        for field in ("clinical_domain", "scenario_stub", "unsafe_rewrite_to_avoid"):
            value = row.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}: {field} must be a non empty string")

        validate_public_wording_text(row, label, errors)
        validate_list_field(row, "plain_clinical_language_checks", label, errors, minimum=3)
        validate_list_field(row, "missing_data_to_preserve", label, errors, minimum=4)
        validate_list_field(row, "source_support_to_preserve", label, errors, minimum=1)
        validate_boundary_objects(row, label, errors)
        validate_private_identifier_absence(row, label, errors)
        validate_no_forbidden_claims(row, label, errors)

    if len(used_pairs) < 6:
        errors.append("Expected the public wording bank to cover all six paired state examples")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", nargs="?", default=str(DEFAULT_FIXTURE))
    parser.add_argument("--paired-fixture", default=str(DEFAULT_PAIRED_FIXTURE))
    args = parser.parse_args()

    fixture = resolve_path(Path(args.fixture))
    paired_fixture = resolve_path(Path(args.paired_fixture))

    errors: list[str] = []
    if not fixture.exists():
        errors.append(f"Missing fixture: {repo_relative(fixture)}")
    if not paired_fixture.exists():
        errors.append(f"Missing paired fixture: {repo_relative(paired_fixture)}")
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    try:
        rows = load_jsonl(fixture)
        pair_ids = load_pair_ids(paired_fixture)
    except ValueError as error:
        print(f"FAIL {error}")
        return 1

    errors = validate_rows(rows, pair_ids)
    if errors:
        print("FAIL Multilingual Medical Intelligence public wording bank validation")
        for error in errors:
            print(f"- {error}")
        return 1

    domains = sorted({str(row["clinical_domain"]) for row in rows})
    used_pairs = sorted({str(row["source_state_pair_id"]) for row in rows})
    print("PASS Multilingual Medical Intelligence public wording bank validation")
    print(f"fixture={repo_relative(fixture)}")
    print(f"rows={len(rows)}")
    print(f"source_state_pairs={len(used_pairs)}")
    print(f"domains={len(domains)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
