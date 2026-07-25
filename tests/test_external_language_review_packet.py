from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_external_language_review_packet_v0_1 import validate_file


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CASES = ROOT / "data" / "failure_atlas_external_sample_v0_1.jsonl"


def write_review(tmp_path: Path, row: dict[str, object]) -> Path:
    path = tmp_path / "review.jsonl"
    path.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def valid_row() -> dict[str, object]:
    return {
        "review_id": "FA_SAMPLE_001_LANG_REVIEW_001",
        "source_case_id": "FA_SAMPLE_001",
        "review_language": "zh",
        "review_kind": "close_translation_then_safer_rewrite",
        "reviewer_public_handle": "YuxingLu613",
        "reviewer_role": "biomedical language reviewer",
        "translation_text": "Close translation text for the synthetic prompt.",
        "risk_preservation_note": "Preserves unsafe remote dosing and urgent escalation risk.",
        "failure_mechanism_tags_preserved": [
            "unsafe_remote_dosing",
            "urgent_escalation",
        ],
        "wording_risk_note": "The wording must not turn missing ketones into a dose request.",
        "safer_rewrite": "Safer rewrite keeps urgent clinician contact visible and avoids dosing.",
        "contains_patient_data": False,
        "clinical_use_allowed": False,
        "model_ranking_claim": False,
        "clinical_validation_claim": False,
    }


def test_valid_language_review_packet_passes(tmp_path: Path) -> None:
    path = write_review(tmp_path, valid_row())

    assert validate_file(path, SOURCE_CASES) == []


def test_unknown_source_case_is_rejected(tmp_path: Path) -> None:
    row = valid_row()
    row["source_case_id"] = "FA_SAMPLE_999"
    path = write_review(tmp_path, row)

    errors = validate_file(path, SOURCE_CASES)

    assert "line 1.source_case_id: unknown source case 'FA_SAMPLE_999'" in errors


def test_review_id_must_match_source_case_prefix(tmp_path: Path) -> None:
    row = valid_row()
    row["review_id"] = "FA_SAMPLE_002_LANG_REVIEW_001"
    path = write_review(tmp_path, row)

    errors = validate_file(path, SOURCE_CASES)

    assert "line 1.review_id: must start with source_case_id plus _LANG_REVIEW_" in errors


def test_duplicate_review_ids_are_rejected(tmp_path: Path) -> None:
    first = valid_row()
    second = valid_row()
    second["reviewer_public_handle"] = "second-reviewer"
    path = tmp_path / "review.jsonl"
    path.write_text(
        "\n".join(
            [
                json.dumps(first, ensure_ascii=False),
                json.dumps(second, ensure_ascii=False),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    errors = validate_file(path, SOURCE_CASES)

    assert "line 2.review_id: duplicate FA_SAMPLE_001_LANG_REVIEW_001" in errors


def test_placeholder_reviewer_handle_is_rejected(tmp_path: Path) -> None:
    row = valid_row()
    row["reviewer_public_handle"] = "example-reviewer"
    path = write_review(tmp_path, row)

    errors = validate_file(path, SOURCE_CASES)

    assert (
        "line 1.reviewer_public_handle: replace template handle with a public reviewer handle"
        in errors
    )


def test_preserved_tags_must_come_from_source_case(tmp_path: Path) -> None:
    row = valid_row()
    row["failure_mechanism_tags_preserved"] = ["made_up_tag"]
    path = write_review(tmp_path, row)

    errors = validate_file(path, SOURCE_CASES)

    assert (
        "line 1.failure_mechanism_tags_preserved: tags not in source case: ['made_up_tag']"
        in errors
    )


def test_preserved_tags_must_be_non_empty_strings(tmp_path: Path) -> None:
    row = valid_row()
    row["failure_mechanism_tags_preserved"] = ["unsafe_remote_dosing", ""]
    path = write_review(tmp_path, row)

    errors = validate_file(path, SOURCE_CASES)

    assert (
        "line 1.failure_mechanism_tags_preserved: all tags must be non empty strings"
        in errors
    )


def test_preserved_tags_must_not_be_duplicated(tmp_path: Path) -> None:
    row = valid_row()
    row["failure_mechanism_tags_preserved"] = [
        "unsafe_remote_dosing",
        "unsafe_remote_dosing",
    ]
    path = write_review(tmp_path, row)

    errors = validate_file(path, SOURCE_CASES)

    assert (
        "line 1.failure_mechanism_tags_preserved: duplicate tags: ['unsafe_remote_dosing']"
        in errors
    )


def test_clinical_claims_are_rejected(tmp_path: Path) -> None:
    row = valid_row()
    row["clinical_validation_claim"] = True
    row["wording_risk_note"] = "This is clinical validation."
    path = write_review(tmp_path, row)

    errors = validate_file(path, SOURCE_CASES)

    assert "line 1.clinical_validation_claim: must be false" in errors
    assert "line 1: forbidden claim phrase present: clinical validation" in errors


def test_template_placeholder_text_is_rejected(tmp_path: Path) -> None:
    row = valid_row()
    row["translation_text"] = "Target language close translation."
    path = write_review(tmp_path, row)

    errors = validate_file(path, SOURCE_CASES)

    assert "line 1.translation_text: replace template placeholder text before submission" in errors


def test_safer_rewrite_must_differ_from_translation(tmp_path: Path) -> None:
    row = valid_row()
    row["translation_text"] = "请不要根据这个信息现在调整胰岛素剂量。"
    row["safer_rewrite"] = "  请不要根据这个信息现在调整胰岛素剂量。 "
    path = write_review(tmp_path, row)

    errors = validate_file(path, SOURCE_CASES)

    assert "line 1.safer_rewrite: must differ from translation_text" in errors


def test_blank_safer_rewrite_is_rejected(tmp_path: Path) -> None:
    row = valid_row()
    row["safer_rewrite"] = " "
    path = write_review(tmp_path, row)

    errors = validate_file(path, SOURCE_CASES)

    assert "line 1.safer_rewrite: must be a non empty string" in errors
