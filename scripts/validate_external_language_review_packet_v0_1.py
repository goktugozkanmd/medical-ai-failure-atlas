#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_CASES = ROOT / "data" / "failure_atlas_external_sample_v0_1.jsonl"

REQUIRED_KEYS = {
    "review_id",
    "source_case_id",
    "review_language",
    "review_kind",
    "reviewer_public_handle",
    "reviewer_role",
    "translation_text",
    "risk_preservation_note",
    "failure_mechanism_tags_preserved",
    "wording_risk_note",
    "safer_rewrite",
    "contains_patient_data",
    "clinical_use_allowed",
    "model_ranking_claim",
    "clinical_validation_claim",
}

ALLOWED_REVIEW_KINDS = {"close_translation_then_safer_rewrite"}
LANGUAGE_CODE = re.compile(r"^[a-z]{2}([_-][A-Za-z]{2})?$")
REVIEW_ID = re.compile(r"^[A-Z0-9_]+_LANG_REVIEW_[0-9]{3}$")

FORBIDDEN_CLAIM_PHRASES = {
    "clinically validated",
    "clinical validation",
    "deployment ready",
    "safe for clinical use",
    "model ranking",
    "best model",
    "real patient data",
    "patient data used",
    "official endorsement",
}

TEXT_PACKET_FIELDS = (
    "translation_text",
    "risk_preservation_note",
    "wording_risk_note",
    "safer_rewrite",
)

PLACEHOLDER_PHRASES = {
    "short note about preserved risk.",
    "short note about unsafe wording risk.",
    "target language close translation.",
    "target language safer rewrite.",
}
PLACEHOLDER_TOKEN = re.compile(r"\b(todo|tbd|placeholder|fill me|replace this)\b", re.IGNORECASE)


def normalize_text(value: str) -> str:
    return " ".join(value.casefold().split())


def load_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    rows: list[tuple[int, dict[str, Any]]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"line {line_number}: row must be a JSON object")
        rows.append((line_number, row))
    return rows


def load_source_cases(path: Path) -> dict[str, dict[str, Any]]:
    cases: dict[str, dict[str, Any]] = {}
    for line_number, row in load_jsonl(path):
        case_id = row.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"source line {line_number}: missing case_id")
        cases[case_id] = row
    return cases


def validate_file(review_path: Path, source_cases_path: Path = DEFAULT_SOURCE_CASES) -> list[str]:
    errors: list[str] = []
    if not review_path.exists():
        return [f"file not found: {review_path}"]
    if not source_cases_path.exists():
        return [f"source case file not found: {source_cases_path}"]

    try:
        source_cases = load_source_cases(source_cases_path)
        rows = load_jsonl(review_path)
    except ValueError as exc:
        return [str(exc)]

    if not rows:
        return ["no review rows found"]

    seen_review_ids: set[str] = set()
    for line_number, row in rows:
        errors.extend(validate_row(row, line_number, source_cases, seen_review_ids))
    return errors


def validate_row(
    row: dict[str, Any],
    line_number: int,
    source_cases: dict[str, dict[str, Any]],
    seen_review_ids: set[str],
) -> list[str]:
    prefix = f"line {line_number}"
    errors: list[str] = []

    missing = REQUIRED_KEYS - set(row)
    if missing:
        errors.append(f"{prefix}: missing keys: {sorted(missing)}")
        return errors

    review_id = row["review_id"]
    valid_review_id = isinstance(review_id, str) and bool(REVIEW_ID.match(review_id))
    if not valid_review_id:
        errors.append(f"{prefix}.review_id: expected pattern CASE_LANG_REVIEW_001")
    elif review_id in seen_review_ids:
        errors.append(f"{prefix}.review_id: duplicate {review_id}")
    else:
        seen_review_ids.add(review_id)

    source_case_id = row["source_case_id"]
    source_case = source_cases.get(source_case_id) if isinstance(source_case_id, str) else None
    if source_case is None:
        errors.append(f"{prefix}.source_case_id: unknown source case {source_case_id!r}")
    elif valid_review_id and not review_id.startswith(f"{source_case_id}_LANG_REVIEW_"):
        errors.append(f"{prefix}.review_id: must start with source_case_id plus _LANG_REVIEW_")

    review_language = row["review_language"]
    if not isinstance(review_language, str) or not LANGUAGE_CODE.match(review_language):
        errors.append(f"{prefix}.review_language: expected language code like zh or zh_CN")

    if row["review_kind"] not in ALLOWED_REVIEW_KINDS:
        errors.append(f"{prefix}.review_kind: must be one of {sorted(ALLOWED_REVIEW_KINDS)}")

    for key in (
        "reviewer_public_handle",
        "reviewer_role",
        "translation_text",
        "risk_preservation_note",
        "wording_risk_note",
        "safer_rewrite",
    ):
        value = row[key]
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{prefix}.{key}: must be a non empty string")

    for key in TEXT_PACKET_FIELDS:
        value = row[key]
        if not isinstance(value, str) or not value.strip():
            continue
        normalized_value = normalize_text(value)
        if normalized_value in PLACEHOLDER_PHRASES or PLACEHOLDER_TOKEN.search(value):
            errors.append(f"{prefix}.{key}: replace template placeholder text before submission")

    translation_text = row["translation_text"]
    safer_rewrite = row["safer_rewrite"]
    if (
        isinstance(translation_text, str)
        and isinstance(safer_rewrite, str)
        and translation_text.strip()
        and safer_rewrite.strip()
        and normalize_text(translation_text) == normalize_text(safer_rewrite)
    ):
        errors.append(f"{prefix}.safer_rewrite: must differ from translation_text")

    preserved_tags = row["failure_mechanism_tags_preserved"]
    if not isinstance(preserved_tags, list) or not preserved_tags:
        errors.append(f"{prefix}.failure_mechanism_tags_preserved: must be a non empty list")
    elif source_case is not None:
        non_string_tags = [tag for tag in preserved_tags if not isinstance(tag, str) or not tag.strip()]
        if non_string_tags:
            errors.append(
                f"{prefix}.failure_mechanism_tags_preserved: all tags must be non empty strings"
            )
        else:
            duplicated_tags = sorted({tag for tag in preserved_tags if preserved_tags.count(tag) > 1})
            if duplicated_tags:
                errors.append(
                    f"{prefix}.failure_mechanism_tags_preserved: duplicate tags: {duplicated_tags}"
                )
            source_tags = set(source_case.get("failure_mechanism_tags", []))
            unknown_tags = sorted(tag for tag in preserved_tags if tag not in source_tags)
            if unknown_tags:
                errors.append(
                    f"{prefix}.failure_mechanism_tags_preserved: tags not in source case: {unknown_tags}"
                )

    boolean_requirements = {
        "contains_patient_data": False,
        "clinical_use_allowed": False,
        "model_ranking_claim": False,
        "clinical_validation_claim": False,
    }
    for key, expected in boolean_requirements.items():
        if row[key] is not expected:
            errors.append(f"{prefix}.{key}: must be {str(expected).lower()}")

    lower_text = json.dumps(row, ensure_ascii=False).lower()
    for phrase in sorted(FORBIDDEN_CLAIM_PHRASES):
        if phrase in lower_text:
            errors.append(f"{prefix}: forbidden claim phrase present: {phrase}")

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate external language review packets for synthetic Failure Atlas cases."
    )
    parser.add_argument("review_jsonl", type=Path)
    parser.add_argument("--source-cases", type=Path, default=DEFAULT_SOURCE_CASES)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = validate_file(args.review_jsonl, args.source_cases)
    if errors:
        print("FAIL external language review packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS external language review packet validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
