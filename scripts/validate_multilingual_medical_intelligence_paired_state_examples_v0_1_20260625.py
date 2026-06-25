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
    / "multilingual_medical_intelligence_paired_state_examples_v0_1_20260625.jsonl"
)

REQUIRED_TOP_LEVEL_FIELDS = {
    "pair_id",
    "turkish_state",
    "english_state",
    "cross_language_checks",
    "source_check",
    "release_boundary",
}

CSL_STRING_FIELDS = {
    "state_id",
    "trajectory_id",
    "timepoint",
    "patient_voice",
    "risk_state",
    "action_boundary",
    "language_context",
}

CSL_ARRAY_FIELDS = {
    "problem_list",
    "timeline",
    "missing_data",
    "hypotheses",
    "evidence_for",
    "evidence_against",
    "follow_up_triggers",
    "source_support_needed",
}

CSL_REQUIRED_FIELDS = CSL_STRING_FIELDS | CSL_ARRAY_FIELDS | {
    "synthetic_only",
    "patient_data_used",
    "clinical_use_allowed",
}

REQUIRED_STATE_FLAGS = {
    "synthetic_only": True,
    "patient_data_used": False,
    "clinical_use_allowed": False,
}

REQUIRED_CROSS_LANGUAGE_CHECKS = {
    "no_added_certainty",
    "missing_data_preserved",
    "action_boundary_preserved",
    "source_support_preserved",
    "not_literal_translation_only",
}

EXPECTED_SOURCE_CHECK_STATUS = "ready"
EXPECTED_SOURCE_CHECK_SCOPE = "repo local synthetic pair check"
EXPECTED_ROW_COUNT = 6

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
    "model superiority proven": "model superiority claim",
    "superior model": "model superiority claim",
    "best model": "model superiority claim",
    "outperforms all models": "model superiority claim",
    "partner confirmed": "partner claim",
    "partnership confirmed": "partner claim",
    "official partner": "partner claim",
    "institutional partner confirmed": "partner claim",
    "collaboration confirmed": "partner claim",
    "payment completed": "payment claim",
    "payment confirmed": "payment claim",
    "invoice paid": "payment claim",
    "paid invoice": "payment claim",
    "terms accepted": "terms claim",
    "terms agreed": "terms claim",
    "accepted terms": "terms claim",
    "accepted the terms": "terms claim",
    "terms of service accepted": "terms claim",
}

CLAIM_SCAN_SKIP_PARTS = {
    "blocked_claims",
    "blocked_wording",
    "forbidden_claims",
    "forbidden_phrases",
    "not_allowed_claims",
}

CLAIM_NEGATION_MARKERS = (
    "no ",
    "not ",
    "without ",
    "never ",
    "must not ",
    "cannot ",
    "do not ",
    "does not ",
    "blocked ",
)


def path_label(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def resolve_fixture(path: Path) -> Path:
    if path.is_absolute():
        return path
    return ROOT / path


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path_label(path)} line {line_number}: invalid JSON: {error}") from error
        if not isinstance(item, dict):
            raise ValueError(f"{path_label(path)} line {line_number}: expected JSON object")
        rows.append(item)
    return rows


def row_label(row: dict[str, Any], index: int) -> str:
    pair_id = row.get("pair_id")
    if isinstance(pair_id, str) and pair_id.strip():
        return pair_id.strip()
    return f"row {index}"


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


def path_parts(path: str) -> set[str]:
    return {part for part in re.split(r"[.\[\]]+", path) if part}


def should_scan_for_claims(path: str) -> bool:
    return not bool(path_parts(path) & CLAIM_SCAN_SKIP_PARTS)


def is_negated_claim(text: str, start_index: int) -> bool:
    window = text[max(0, start_index - 40):start_index]
    return any(marker in window for marker in CLAIM_NEGATION_MARKERS)


def has_phone_like_value(text: str) -> bool:
    for candidate in PHONE_CANDIDATE_RE.findall(text):
        digits = re.sub(r"\D", "", candidate)
        if len(digits) >= 10:
            return True
    return False


def validate_text_boundaries(row: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []

    for path, key in iter_keys(row):
        key_name = normalized_key(key)
        if key_name == "external_url":
            errors.append(f"{label}.{path}: external_url field is not allowed")
        if key_name in PRIVATE_IDENTIFIER_FIELD_NAMES:
            errors.append(f"{label}.{path}: private identifier field is not allowed")

    for path, text in iter_string_values(row):
        if EXTERNAL_URL_RE.search(text):
            errors.append(f"{label}.{path}: external URL is not allowed")
        if EMAIL_RE.search(text):
            errors.append(f"{label}.{path}: email address is not allowed")
        if has_phone_like_value(text):
            errors.append(f"{label}.{path}: phone-like private identifier is not allowed")

        for identifier_name, pattern in PRIVATE_IDENTIFIER_VALUE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label}.{path}: private identifier value is not allowed: {identifier_name}")

        if not should_scan_for_claims(path):
            continue
        lower_text = text.lower()
        for phrase, description in FORBIDDEN_CLAIM_PATTERNS.items():
            start = lower_text.find(phrase)
            if start != -1 and not is_negated_claim(lower_text, start):
                errors.append(f"{label}.{path}: forbidden {description}: {phrase}")

    return errors


def validate_state(state: Any, label: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(state, dict):
        return [f"{label}: must be an object"]

    missing_fields = sorted(CSL_REQUIRED_FIELDS - set(state))
    if missing_fields:
        errors.append(f"{label}: missing Clinical State Language fields: {', '.join(missing_fields)}")

    for field in sorted(CSL_STRING_FIELDS):
        if field not in state:
            continue
        value = state[field]
        if not isinstance(value, str):
            errors.append(f"{label}.{field}: expected string")
        elif not value.strip():
            errors.append(f"{label}.{field}: cannot be empty")

    for field in sorted(CSL_ARRAY_FIELDS):
        if field not in state:
            continue
        value = state[field]
        if not isinstance(value, list):
            errors.append(f"{label}.{field}: expected array")
            continue
        for item_index, item in enumerate(value, 1):
            if not isinstance(item, str):
                errors.append(f"{label}.{field}[{item_index}]: expected string")
            elif not item.strip():
                errors.append(f"{label}.{field}[{item_index}]: cannot be empty")

    for field, expected in REQUIRED_STATE_FLAGS.items():
        if state.get(field) is not expected:
            errors.append(f"{label}.{field}: must be {str(expected).lower()}")

    missing_data = state.get("missing_data")
    if isinstance(missing_data, list) and not missing_data:
        errors.append(f"{label}.missing_data: must name at least one missing item")

    source_support_needed = state.get("source_support_needed")
    if isinstance(source_support_needed, list) and len(source_support_needed) < 2:
        errors.append(f"{label}.source_support_needed: must include at least two items")

    return errors


def validate_cross_language_checks(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return [f"{label}.cross_language_checks: must be an object"]

    missing_checks = sorted(REQUIRED_CROSS_LANGUAGE_CHECKS - set(value))
    if missing_checks:
        errors.append(
            f"{label}.cross_language_checks: missing checks: {', '.join(missing_checks)}"
        )

    for check in sorted(REQUIRED_CROSS_LANGUAGE_CHECKS):
        if value.get(check) is not True:
            errors.append(f"{label}.cross_language_checks.{check}: must be true")

    return errors


def validate_source_check(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return [f"{label}.source_check: must be an object"]

    if value.get("status") != EXPECTED_SOURCE_CHECK_STATUS:
        errors.append(f"{label}.source_check.status: must be {EXPECTED_SOURCE_CHECK_STATUS!r}")
    if value.get("scope") != EXPECTED_SOURCE_CHECK_SCOPE:
        errors.append(f"{label}.source_check.scope: must be {EXPECTED_SOURCE_CHECK_SCOPE!r}")
    if "external_url" in value:
        errors.append(f"{label}.source_check.external_url: field is not allowed")

    return errors


def validate_release_boundary(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return [f"{label}.release_boundary: must be an object"]

    for field, expected in REQUIRED_STATE_FLAGS.items():
        if value.get(field) is not expected:
            errors.append(f"{label}.release_boundary.{field}: must be {str(expected).lower()}")

    return errors


def validate_row(row: dict[str, Any], index: int, seen_pair_ids: set[str]) -> list[str]:
    errors: list[str] = []
    label = row_label(row, index)

    missing_fields = sorted(REQUIRED_TOP_LEVEL_FIELDS - set(row))
    if missing_fields:
        errors.append(f"{label}: missing top-level fields: {', '.join(missing_fields)}")

    pair_id = row.get("pair_id")
    if not isinstance(pair_id, str) or not pair_id.strip():
        errors.append(f"{label}.pair_id: must be a non empty string")
    else:
        compact_pair_id = pair_id.strip()
        if compact_pair_id in seen_pair_ids:
            errors.append(f"{label}.pair_id: duplicate pair_id")
        seen_pair_ids.add(compact_pair_id)

    errors.extend(validate_state(row.get("turkish_state"), f"{label}.turkish_state"))
    errors.extend(validate_state(row.get("english_state"), f"{label}.english_state"))
    errors.extend(validate_cross_language_checks(row.get("cross_language_checks"), label))
    errors.extend(validate_source_check(row.get("source_check"), label))
    errors.extend(validate_release_boundary(row.get("release_boundary"), label))
    errors.extend(validate_text_boundaries(row, label))

    return errors


def validate_rows(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if len(rows) != EXPECTED_ROW_COUNT:
        errors.append(f"expected exactly {EXPECTED_ROW_COUNT} rows, found {len(rows)}")

    seen_pair_ids: set[str] = set()
    for index, row in enumerate(rows, 1):
        errors.extend(validate_row(row, index, seen_pair_ids))

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Multilingual Medical Intelligence paired state examples v0.1."
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="JSONL fixture with Turkish and English paired Clinical State Language rows.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fixture = resolve_fixture(args.fixture)

    if not fixture.exists():
        print(f"FAIL missing fixture file: {path_label(fixture)}")
        return 1

    try:
        rows = load_jsonl(fixture)
    except Exception as error:  # noqa: BLE001
        print(f"FAIL multilingual medical intelligence paired state fixture validation")
        print(f"- {error}")
        return 1

    errors = validate_rows(rows)
    if errors:
        print("FAIL multilingual medical intelligence paired state fixture validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS multilingual medical intelligence paired state fixture validation")
    print(f"fixture={path_label(fixture)}")
    print(f"rows={len(rows)}")
    print(f"pairs={len({row['pair_id'].strip() for row in rows})}")
    print(f"states={len(rows) * 2}")
    print(f"cross_language_checks={len(REQUIRED_CROSS_LANGUAGE_CHECKS)}")
    print(f"source_check_status={EXPECTED_SOURCE_CHECK_STATUS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
