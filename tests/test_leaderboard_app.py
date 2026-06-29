from __future__ import annotations

import json
from pathlib import Path

from leaderboard.app import (
    MAX_HF_LINK_LENGTH,
    MAX_MODEL_NAME_LENGTH,
    MAX_NOTES_LENGTH,
    coerce_score,
    load_submission_store,
    normalize_huggingface_link,
    submit_model,
    submissions_to_table,
)


def reachable(url: str) -> tuple[bool, str]:
    assert url == "https://huggingface.co/org/model"
    return True, "200"


def unreachable(url: str) -> tuple[bool, str]:
    assert url == "https://huggingface.co/org/model"
    return False, "HTTP 404"


def test_normalize_huggingface_link_requires_https_model_path() -> None:
    assert normalize_huggingface_link("huggingface.co/model-name/") == "https://huggingface.co/model-name"
    assert normalize_huggingface_link("huggingface.co/org/model/") == "https://huggingface.co/org/model"
    assert (
        normalize_huggingface_link("https://www.huggingface.co/org/model?revision=main")
        == "https://huggingface.co/org/model"
    )


def test_normalize_huggingface_link_rejects_non_model_repo_paths() -> None:
    for link in (
        "https://huggingface.co/spaces/org/demo",
        "https://huggingface.co/datasets/org/data",
    ):
        try:
            normalize_huggingface_link(link)
        except ValueError as exc:
            assert "model repo" in str(exc)
        else:
            raise AssertionError(f"Expected non-model path to fail: {link}")

    try:
        normalize_huggingface_link("https://huggingface.co/org/model/blob/main/config.json")
    except ValueError as exc:
        assert "https://huggingface.co/org/model" in str(exc)
    else:
        raise AssertionError("Expected nested HuggingFace file path to fail")


def test_coerce_score_limits_public_submission_scores() -> None:
    assert coerce_score("89.126", "Safety score") == 89.13

    try:
        coerce_score(101, "Safety score")
    except ValueError as exc:
        assert "between 0 and 100" in str(exc)
    else:
        raise AssertionError("Expected out of range score to fail")


def test_submission_text_limits_block_oversized_public_rows(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"

    message, table, updated = submit_model(
        "M" * (MAX_MODEL_NAME_LENGTH + 1),
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "",
        reachability_checker=reachable,
        store_path=store_path,
    )
    assert message == f"Submission not saved. Model name must be {MAX_MODEL_NAME_LENGTH} characters or fewer."
    assert table == []
    assert "No submissions yet" in updated

    try:
        normalize_huggingface_link("https://huggingface.co/" + "m" * MAX_HF_LINK_LENGTH)
    except ValueError as exc:
        assert f"{MAX_HF_LINK_LENGTH} characters or fewer" in str(exc)
    else:
        raise AssertionError("Expected oversized HuggingFace link to fail")

    message, table, updated = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "N" * (MAX_NOTES_LENGTH + 1),
        reachability_checker=reachable,
        store_path=store_path,
    )
    assert message == f"Submission not saved. Benchmark notes must be {MAX_NOTES_LENGTH} characters or fewer."
    assert table == []
    assert "No submissions yet" in updated


def test_submit_model_saves_new_row_and_replaces_duplicate(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"

    message, table, updated = submit_model(
        "  Test Model  ",
        "huggingface.co/org/model/",
        80,
        70.5,
        60,
        "synthetic run",
        reachability_checker=reachable,
        store_path=store_path,
    )
    assert message == "Submission saved."
    assert table[0][:5] == ["Test Model", "https://huggingface.co/org/model", "80", "70.5", "60"]
    assert "Last Updated" in updated

    second_message, second_table, _ = submit_model(
        "Test Model v2",
        "https://huggingface.co/org/model",
        81,
        71,
        61,
        "rerun",
        reachability_checker=reachable,
        store_path=store_path,
    )
    assert second_message == "Submission updated and saved."
    assert second_table[0][:5] == ["Test Model v2", "https://huggingface.co/org/model", "81", "71", "61"]

    store = load_submission_store(store_path)
    submissions = store["submissions"]
    assert isinstance(submissions, list)
    assert len(submissions) == 1
    assert submissions[0]["first_submitted_at"]


def test_submit_model_does_not_save_unreachable_link(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"

    message, table, updated = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "",
        reachability_checker=unreachable,
        store_path=store_path,
    )

    assert message == "Submission not saved. HuggingFace link was not reachable: HTTP 404"
    assert table == []
    assert "No submissions yet" in updated
    assert not store_path.exists()


def test_submissions_table_sorts_by_recent_submission_not_score() -> None:
    table = submissions_to_table(
        [
            {
                "model_name": "older higher score",
                "huggingface_link": "https://huggingface.co/org/lower",
                "benchmark_scores": {"safety_score": 90},
                "submitted_at": "2026-06-27T10:00:00Z",
            },
            {
                "model_name": "newer lower score",
                "huggingface_link": "https://huggingface.co/org/higher",
                "benchmark_scores": {"safety_score": 10},
                "submitted_at": "2026-06-27T11:00:00Z",
            },
        ]
    )

    assert [row[0] for row in table] == ["newer lower score", "older higher score"]


def test_submit_model_handles_submission_store_errors(tmp_path: Path) -> None:
    message, table, updated = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "",
        reachability_checker=reachable,
        store_path=tmp_path,
    )

    assert message.startswith("Submission not saved.")
    assert table == []
    assert "Submission store error" in updated


def test_load_submission_store_accepts_legacy_list(tmp_path: Path) -> None:
    store_path = tmp_path / "legacy.json"
    store_path.write_text(json.dumps([{"model_name": "legacy"}]), encoding="utf-8")

    store = load_submission_store(store_path)

    assert store["last_updated"] is None
    assert store["submissions"] == [{"model_name": "legacy"}]
