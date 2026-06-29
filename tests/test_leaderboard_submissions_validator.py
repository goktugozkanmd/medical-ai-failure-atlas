from __future__ import annotations

from scripts.validate_leaderboard_submissions_v0_1 import MAX_SUBMISSIONS, validate_store


def valid_row(index: int) -> dict[str, object]:
    timestamp = f"2026-06-27T00:{index % 60:02d}:00Z"
    return {
        "id": f"{index:032x}",
        "model_name": f"Model {index}",
        "huggingface_link": f"https://huggingface.co/org/model-{index}",
        "benchmark_scores": {
            "safety_score": 80,
            "source_support_score": 70,
            "clinical_boundary_score": 60,
        },
        "notes": "",
        "status": "pending review",
        "submitted_at": timestamp,
        "first_submitted_at": timestamp,
        "huggingface_reachable": True,
        "huggingface_status": "200",
    }


def test_validate_store_rejects_unbounded_submission_store() -> None:
    store = {
        "last_updated": "2026-06-27T02:00:00Z",
        "submissions": [valid_row(index) for index in range(MAX_SUBMISSIONS + 1)],
    }

    errors = validate_store(store)

    assert f"submissions must contain {MAX_SUBMISSIONS} rows or fewer" in errors


def test_validate_store_requires_latest_first_submission_order() -> None:
    newer = valid_row(2)
    newer["submitted_at"] = "2026-06-27T02:00:00Z"
    older = valid_row(1)
    older["submitted_at"] = "2026-06-27T01:00:00Z"

    valid_store = {
        "last_updated": "2026-06-27T02:00:00Z",
        "submissions": [newer, older],
    }
    assert validate_store(valid_store) == []

    unsorted_store = {
        "last_updated": "2026-06-27T02:00:00Z",
        "submissions": [older, newer],
    }
    assert "submissions[2].submitted_at: submissions must be ordered latest first" in validate_store(
        unsorted_store
    )


def test_validate_store_requires_generated_hex_submission_id() -> None:
    row = valid_row(1)
    row["id"] = "row-1"
    store = {
        "last_updated": "2026-06-27T02:00:00Z",
        "submissions": [row],
    }

    errors = validate_store(store)

    assert "submissions[1].id: must be a 32 character lowercase hex id" in errors


def test_validate_store_rejects_last_updated_before_latest_submission() -> None:
    row = valid_row(1)
    row["submitted_at"] = "2026-06-27T02:00:00Z"
    store = {
        "last_updated": "2026-06-27T01:59:59Z",
        "submissions": [row],
    }

    errors = validate_store(store)

    assert "last_updated: cannot be earlier than the latest submission" in errors


def test_validate_store_requires_normalized_huggingface_model_url() -> None:
    row = valid_row(1)
    row["huggingface_link"] = "https://www.huggingface.co/org/model-1?revision=main"
    store = {
        "last_updated": "2026-06-27T02:00:00Z",
        "submissions": [row],
    }

    errors = validate_store(store)

    assert (
        "submissions[1].huggingface_link: must be stored as "
        "https://huggingface.co/org/model-1"
    ) in errors


def test_validate_store_rejects_top_level_huggingface_pages() -> None:
    row = valid_row(1)
    row["huggingface_link"] = "https://huggingface.co/models"
    store = {
        "last_updated": "2026-06-27T02:00:00Z",
        "submissions": [row],
    }

    errors = validate_store(store)

    assert "submissions[1].huggingface_link: must be a normalized HuggingFace model URL" in errors


def test_validate_store_rejects_score_out_of_range() -> None:
    row = valid_row(1)
    row["benchmark_scores"]["safety_score"] = 101
    store = {
        "last_updated": "2026-06-27T02:00:00Z",
        "submissions": [row],
    }

    errors = validate_store(store)

    assert (
        "submissions[1].benchmark_scores.safety_score: score must be between 0 and 100"
        in errors
    )


def test_validate_store_rejects_private_data_patterns() -> None:
    row = valid_row(1)
    row["notes"] = "Contact reviewer@example.com for context"
    store = {
        "last_updated": "2026-06-27T02:00:00Z",
        "submissions": [row],
    }

    errors = validate_store(store)

    assert "submissions[1].notes: private data pattern 'email address'" in errors

    row = valid_row(2)
    row["model_name"] = "+90 555 555 5555"
    store = {
        "last_updated": "2026-06-27T02:00:00Z",
        "submissions": [row],
    }

    errors = validate_store(store)

    assert "submissions[1].model_name: private data pattern 'phone or long numeric identifier'" in errors
