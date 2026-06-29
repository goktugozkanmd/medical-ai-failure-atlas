from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import leaderboard.app as leaderboard_app
from leaderboard.app import (
    MAX_HF_LINK_LENGTH,
    MAX_MODEL_NAME_LENGTH,
    MAX_NOTES_LENGTH,
    MAX_SUBMISSIONS,
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


def submission_row(
    *,
    model_name: str = "Test Model",
    huggingface_link: str = "https://huggingface.co/org/model",
    submitted_at: str = "2026-06-27T10:00:00Z",
    row_id: str = "0" * 32,
    notes: str = "",
) -> dict[str, object]:
    return {
        "id": row_id,
        "model_name": model_name,
        "huggingface_link": huggingface_link,
        "benchmark_scores": {
            "safety_score": 80,
            "source_support_score": 70,
            "clinical_boundary_score": 60,
        },
        "notes": notes,
        "status": "pending review",
        "submitted_at": submitted_at,
        "first_submitted_at": submitted_at,
        "huggingface_reachable": True,
        "huggingface_status": "200",
    }


def test_normalize_huggingface_link_requires_https_model_path() -> None:
    assert normalize_huggingface_link("huggingface.co/model-name/") == "https://huggingface.co/model-name"
    assert normalize_huggingface_link("huggingface.co/org/model/") == "https://huggingface.co/org/model"
    assert (
        normalize_huggingface_link("https://huggingface.co/org-name/model_name.v1")
        == "https://huggingface.co/org-name/model_name.v1"
    )
    assert (
        normalize_huggingface_link("https://huggingface.co/org/model.git")
        == "https://huggingface.co/org/model"
    )
    assert (
        normalize_huggingface_link("https://www.huggingface.co/org/model?revision=main")
        == "https://huggingface.co/org/model"
    )


def test_normalize_huggingface_link_rejects_non_model_repo_paths() -> None:
    for link in (
        "https://huggingface.co/models",
        "https://huggingface.co/new",
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


def test_normalize_huggingface_link_rejects_invalid_repo_segments() -> None:
    for link in (
        "https://huggingface.co/org/..",
        "https://huggingface.co/org/-model",
        "https://huggingface.co/org/model.",
        "https://huggingface.co/org/model--candidate",
        "https://huggingface.co/org/model%2Ffile",
    ):
        try:
            normalize_huggingface_link(link)
        except ValueError as exc:
            assert "valid model repo path" in str(exc)
        else:
            raise AssertionError(f"Expected invalid HuggingFace repo segment to fail: {link}")


def test_normalize_huggingface_link_rejects_private_token_patterns() -> None:
    fake_github_token = "gh" + "o_" + "a" * 20
    fake_openai_token = "sk" + "-proj-" + "a" * 20
    for link in (
        f"https://huggingface.co/org/{fake_github_token}",
        f"https://huggingface.co/org/{fake_openai_token}",
        "https://huggingface.co/org/model?access_token=" + "a" * 16,
    ):
        try:
            normalize_huggingface_link(link)
        except ValueError as exc:
            assert "private data pattern: credential-like token" in str(exc)
        else:
            raise AssertionError(f"Expected private token pattern to fail: {link}")


def test_coerce_score_limits_public_submission_scores() -> None:
    assert coerce_score("89.126", "Safety score") == 89.13

    try:
        coerce_score(True, "Safety score")
    except ValueError as exc:
        assert "must be a number" in str(exc)
    else:
        raise AssertionError("Expected boolean score to fail")

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

    too_long_after_scheme = "huggingface.co/" + "m" * (MAX_HF_LINK_LENGTH - len("huggingface.co/"))
    try:
        normalize_huggingface_link(too_long_after_scheme)
    except ValueError as exc:
        assert f"{MAX_HF_LINK_LENGTH} characters or fewer" in str(exc)
    else:
        raise AssertionError("Expected normalized oversized HuggingFace link to fail")

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


def test_submit_model_blocks_unsupported_public_claims(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"

    message, table, updated = submit_model(
        "best model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "",
        reachability_checker=reachable,
        store_path=store_path,
    )
    assert message == "Submission not saved. Model name includes an unsupported public claim: 'best model'."
    assert table == []
    assert "No submissions yet" in updated

    message, table, updated = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "clinically validated by our team",
        reachability_checker=reachable,
        store_path=store_path,
    )
    assert (
        message
        == "Submission not saved. Benchmark notes include an unsupported public claim: 'clinically validated'."
    )
    assert table == []
    assert "No submissions yet" in updated
    assert not store_path.exists()


def test_submit_model_blocks_private_data_patterns(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"

    message, table, updated = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "Contact reviewer@example.com for details",
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert message == "Submission not saved. Benchmark notes include private data pattern: email address."
    assert table == []
    assert "No submissions yet" in updated
    assert not store_path.exists()

    message, table, updated = submit_model(
        "+90 555 555 5555",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "",
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert message == "Submission not saved. Model name includes private data pattern: phone or long numeric identifier."
    assert table == []
    assert "No submissions yet" in updated
    assert not store_path.exists()

    credential_like_note = "access_" + "token=" + "REDACTED" + "123456"
    message, table, updated = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        credential_like_note,
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert message == "Submission not saved. Benchmark notes include private data pattern: credential-like token."
    assert table == []
    assert "No submissions yet" in updated
    assert not store_path.exists()

    fake_token_path = "gh" + "o_" + "a" * 20
    message, table, updated = submit_model(
        "Test Model",
        f"https://huggingface.co/org/{fake_token_path}",
        80,
        70,
        60,
        "",
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert (
        message
        == "Submission not saved. HuggingFace link includes private data pattern: credential-like token."
    )
    assert table == []
    assert "No submissions yet" in updated
    assert not store_path.exists()

    bearer_note = "Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456"
    message, table, updated = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        bearer_note,
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert message == "Submission not saved. Benchmark notes include private data pattern: credential-like token."
    assert table == []
    assert "No submissions yet" in updated
    assert not store_path.exists()

    jwt_note = "token eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzdWJtaXNzaW9uIn0.signaturepayload123"
    message, table, updated = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        jwt_note,
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert message == "Submission not saved. Benchmark notes include private data pattern: credential-like token."
    assert table == []
    assert "No submissions yet" in updated
    assert not store_path.exists()


def test_submit_model_blocks_unsafe_public_text_patterns(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"

    message, table, updated = submit_model(
        "Test <script>",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "",
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert (
        message
        == "Submission not saved. Model name includes unsafe public text pattern: "
        "HTML or Markdown delimiter."
    )
    assert table == []
    assert "No submissions yet" in updated
    assert not store_path.exists()

    message, table, updated = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "line one\nline two",
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert (
        message
        == "Submission not saved. Benchmark notes include unsafe public text pattern: "
        "control character."
    )
    assert table == []
    assert "No submissions yet" in updated
    assert not store_path.exists()


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


def test_submit_model_regenerates_malformed_legacy_duplicate_id(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"
    store_path.write_text(
        json.dumps(
            {
                "last_updated": "2026-06-27T10:00:00Z",
                "submissions": [
                    {
                        "id": "legacy-row",
                        "model_name": "Legacy Model",
                        "huggingface_link": "https://huggingface.co/org/model",
                        "benchmark_scores": {
                            "safety_score": 70,
                            "source_support_score": 60,
                            "clinical_boundary_score": 50,
                        },
                        "notes": "",
                        "status": "pending review",
                        "submitted_at": "2026-06-27T10:00:00Z",
                        "first_submitted_at": "2026-06-27T09:00:00Z",
                        "huggingface_reachable": True,
                        "huggingface_status": "200",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    message, _, _ = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "",
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert message == "Submission updated and saved."
    store = load_submission_store(store_path)
    submissions = store["submissions"]
    assert isinstance(submissions, list)
    assert len(submissions) == 1
    assert submissions[0]["id"] != "legacy-row"
    assert len(str(submissions[0]["id"])) == 32
    int(str(submissions[0]["id"]), 16)
    assert submissions[0]["first_submitted_at"] == "2026-06-27T09:00:00Z"


def test_submit_model_repairs_malformed_legacy_first_submitted_timestamp(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"
    store_path.write_text(
        json.dumps(
            {
                "last_updated": "2026-06-27T10:00:00Z",
                "submissions": [
                    {
                        "id": "0" * 32,
                        "model_name": "Legacy Model",
                        "huggingface_link": "https://huggingface.co/org/model",
                        "benchmark_scores": {
                            "safety_score": 70,
                            "source_support_score": 60,
                            "clinical_boundary_score": 50,
                        },
                        "notes": "",
                        "status": "pending review",
                        "submitted_at": "2026-06-27T10:00:00Z",
                        "first_submitted_at": "not-a-timestamp",
                        "huggingface_reachable": True,
                        "huggingface_status": "200",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    message, _, _ = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "",
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert message == "Submission updated and saved."
    store = load_submission_store(store_path)
    submissions = store["submissions"]
    assert isinstance(submissions, list)
    repaired = submissions[0]["first_submitted_at"]
    submitted = submissions[0]["submitted_at"]
    assert repaired != "not-a-timestamp"
    assert datetime.fromisoformat(str(repaired).replace("Z", "+00:00")) <= datetime.fromisoformat(
        str(submitted).replace("Z", "+00:00")
    )


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


def test_submit_model_caps_submission_store_to_recent_rows(tmp_path: Path, monkeypatch) -> None:
    store_path = tmp_path / "submissions.json"
    base = datetime(2026, 6, 27, tzinfo=timezone.utc)
    counter = {"value": 0}

    def fake_now() -> str:
        value = counter["value"]
        counter["value"] += 1
        return (base + timedelta(minutes=value)).isoformat().replace("+00:00", "Z")

    def reachable_any(url: str) -> tuple[bool, str]:
        assert url.startswith("https://huggingface.co/org/model-")
        return True, "200"

    monkeypatch.setattr(leaderboard_app, "current_utc_iso", fake_now)

    table: list[list[str]] = []
    for index in range(MAX_SUBMISSIONS + 5):
        message, table, _ = submit_model(
            f"Test Model {index}",
            f"https://huggingface.co/org/model-{index}",
            80,
            70,
            60,
            "",
            reachability_checker=reachable_any,
            store_path=store_path,
        )
        assert message == "Submission saved."

    store = load_submission_store(store_path)
    submissions = store["submissions"]
    assert isinstance(submissions, list)
    assert len(submissions) == MAX_SUBMISSIONS
    assert len(table) == MAX_SUBMISSIONS
    links = {str(row["huggingface_link"]) for row in submissions}
    assert "https://huggingface.co/org/model-0" not in links
    assert f"https://huggingface.co/org/model-{MAX_SUBMISSIONS + 4}" in links


def test_load_submission_store_accepts_legacy_list(tmp_path: Path) -> None:
    store_path = tmp_path / "legacy.json"
    store_path.write_text(json.dumps([{"model_name": "legacy"}]), encoding="utf-8")

    store = load_submission_store(store_path)

    assert store["last_updated"] is None
    assert store["submissions"] == [{"model_name": "legacy"}]


def test_load_submission_store_rejects_non_object_rows(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"
    store_path.write_text(
        json.dumps(
            {
                "last_updated": "2026-06-27T10:00:00Z",
                "submissions": [{"model_name": "valid"}, "malformed"],
            }
        ),
        encoding="utf-8",
    )

    try:
        load_submission_store(store_path)
    except ValueError as exc:
        assert "Submission store rows must be objects" in str(exc)
    else:
        raise AssertionError("Expected malformed submission rows to fail")


def test_load_submission_store_rejects_non_object_legacy_list_rows(tmp_path: Path) -> None:
    store_path = tmp_path / "legacy.json"
    store_path.write_text(json.dumps([{"model_name": "legacy"}, None]), encoding="utf-8")

    try:
        load_submission_store(store_path)
    except ValueError as exc:
        assert "Submission store rows must be objects" in str(exc)
    else:
        raise AssertionError("Expected malformed legacy rows to fail")


def test_submit_model_does_not_overwrite_malformed_submission_store(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"
    original_store = {
        "last_updated": "2026-06-27T10:00:00Z",
        "submissions": [{"model_name": "valid"}, "malformed"],
    }
    store_path.write_text(json.dumps(original_store), encoding="utf-8")

    message, table, updated = submit_model(
        "Test Model",
        "https://huggingface.co/org/model",
        80,
        70,
        60,
        "",
        reachability_checker=reachable,
        store_path=store_path,
    )

    assert message.startswith("Submission not saved. Submission store rows must be objects")
    assert table == []
    assert "Submission store error" in updated
    assert json.loads(store_path.read_text(encoding="utf-8")) == original_store


def test_last_updated_markdown_falls_back_to_latest_submission_timestamp() -> None:
    store = {
        "last_updated": None,
        "submissions": [
            {"submitted_at": "2026-06-27T10:00:00Z"},
            {"submitted_at": "2026-06-27T11:00:00Z"},
        ],
    }

    assert leaderboard_app.last_updated_markdown(store) == "**Last Updated:** 2026-06-27 11:00:00 UTC"


def test_leaderboard_state_hides_existing_rows_that_fail_public_display_rules(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"
    invalid_claim = submission_row(
        model_name="best model",
        huggingface_link="https://huggingface.co/org/unsafe-claim",
        row_id="1" * 32,
    )
    invalid_private_note = submission_row(
        model_name="Unsafe Note",
        huggingface_link="https://huggingface.co/org/private-note",
        row_id="2" * 32,
        notes="Contact reviewer@example.com for details",
    )
    invalid_unexpected_field = submission_row(
        model_name="Unexpected Field",
        huggingface_link="https://huggingface.co/org/unexpected-field",
        row_id="3" * 32,
    )
    invalid_unexpected_field["raw_model_output"] = "synthetic answer draft"
    invalid_unexpected_score = submission_row(
        model_name="Unexpected Score Field",
        huggingface_link="https://huggingface.co/org/unexpected-score-field",
        row_id="5" * 32,
    )
    scores = invalid_unexpected_score["benchmark_scores"]
    assert isinstance(scores, dict)
    scores["overall_score"] = 99
    invalid_private_link = submission_row(
        model_name="Private Link",
        huggingface_link="https://huggingface.co/org/" + ("gh" + "o_" + "a" * 20),
        row_id="6" * 32,
    )
    visible = submission_row(
        model_name="Visible Model",
        huggingface_link="https://huggingface.co/org/visible-model",
        submitted_at="2026-06-27T11:00:00Z",
        row_id="4" * 32,
    )
    store_path.write_text(
        json.dumps(
            {
                "last_updated": "2026-06-27T11:00:00Z",
                "submissions": [
                    invalid_claim,
                    invalid_private_note,
                    invalid_unexpected_field,
                    invalid_unexpected_score,
                    invalid_private_link,
                    visible,
                ],
            }
        ),
        encoding="utf-8",
    )

    table, updated = leaderboard_app.leaderboard_state(store_path)

    assert [row[0] for row in table] == ["Visible Model"]
    assert table[0][1] == "https://huggingface.co/org/visible-model"
    assert updated == "**Last Updated:** 2026-06-27 11:00:00 UTC"


def test_submit_model_drops_existing_rows_that_fail_public_display_rules(tmp_path: Path) -> None:
    store_path = tmp_path / "submissions.json"
    unsafe_row = submission_row(
        model_name="Clinical validation row",
        huggingface_link="https://huggingface.co/org/unsafe-row",
        row_id="1" * 32,
    )
    safe_row = submission_row(
        model_name="Existing Safe Row",
        huggingface_link="https://huggingface.co/org/existing-safe-row",
        submitted_at="2026-06-27T09:00:00Z",
        row_id="2" * 32,
    )
    store_path.write_text(
        json.dumps(
            {
                "last_updated": "2026-06-27T10:00:00Z",
                "submissions": [unsafe_row, safe_row],
            }
        ),
        encoding="utf-8",
    )

    def reachable_any(url: str) -> tuple[bool, str]:
        assert url == "https://huggingface.co/org/new-safe-row"
        return True, "200"

    message, table, _ = submit_model(
        "New Safe Row",
        "https://huggingface.co/org/new-safe-row",
        82,
        72,
        62,
        "",
        reachability_checker=reachable_any,
        store_path=store_path,
    )

    assert message == "Submission saved."
    assert [row[0] for row in table] == ["New Safe Row", "Existing Safe Row"]
    store = load_submission_store(store_path)
    submissions = store["submissions"]
    assert isinstance(submissions, list)
    assert [row["model_name"] for row in submissions] == ["New Safe Row", "Existing Safe Row"]
