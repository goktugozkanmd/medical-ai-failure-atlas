#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, urlunparse


ROOT = Path(__file__).resolve().parents[1]
SUBMISSIONS = ROOT / "leaderboard" / "submissions.json"

MAX_MODEL_NAME_LENGTH = 120
MAX_HF_LINK_LENGTH = 240
MAX_NOTES_LENGTH = 1000
MAX_SUBMISSIONS = 100

REQUIRED_SCORE_KEYS = [
    "safety_score",
    "source_support_score",
    "clinical_boundary_score",
]

ALLOWED_STATUS = {"pending review"}

FORBIDDEN_TEXT = [
    "clinical advice",
    "clinical validation",
    "clinically validated",
    "safe for clinical use",
    "approved for clinical use",
    "regulatory approved",
    "best model",
    "model ranking",
    "source truth certification",
    "patient data",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_timestamp(value: object, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        fail(errors, f"{label}: missing timestamp")
        return None

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail(errors, f"{label}: timestamp must be ISO 8601")
        return None

    if parsed.tzinfo is None:
        fail(errors, f"{label}: timestamp must include timezone")
    return parsed


def normalized_huggingface_model_url(value: str) -> str | None:
    if len(value) > MAX_HF_LINK_LENGTH:
        return None

    parsed = urlparse(value)
    host = parsed.netloc.lower()
    if parsed.scheme != "https" or host not in {"huggingface.co", "www.huggingface.co"}:
        return None
    if parsed.params or parsed.query or parsed.fragment:
        return None

    path_segments = [segment for segment in parsed.path.split("/") if segment]
    if not path_segments:
        return None
    if path_segments[0].lower() in {"datasets", "spaces"}:
        return None
    if len(path_segments) > 2:
        return None

    return urlunparse(("https", "huggingface.co", "/" + "/".join(path_segments), "", "", ""))


def contains_forbidden_text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    lower = value.lower()
    for phrase in FORBIDDEN_TEXT:
        if phrase in lower:
            return phrase
    return None


def validate_score(value: object, label: str, errors: list[str]) -> None:
    if isinstance(value, bool):
        fail(errors, f"{label}: score must be numeric")
        return
    try:
        score = float(value)
    except (TypeError, ValueError):
        fail(errors, f"{label}: score must be numeric")
        return
    if not 0 <= score <= 100:
        fail(errors, f"{label}: score must be between 0 and 100")


def validate_store(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Submission store must contain a JSON object"]

    submissions = data.get("submissions")
    if not isinstance(submissions, list):
        fail(errors, "submissions must be a list")
        submissions = []
    elif len(submissions) > MAX_SUBMISSIONS:
        fail(errors, f"submissions must contain {MAX_SUBMISSIONS} rows or fewer")

    last_updated = data.get("last_updated")
    if submissions or last_updated:
        parse_timestamp(last_updated, "last_updated", errors)

    seen_ids: set[str] = set()
    seen_links: set[str] = set()
    previous_submitted_at: datetime | None = None
    latest_submitted_at: datetime | None = None

    for index, row in enumerate(submissions, start=1):
        label = f"submissions[{index}]"
        if not isinstance(row, dict):
            fail(errors, f"{label}: row must be an object")
            continue

        row_id = row.get("id")
        if not isinstance(row_id, str) or not row_id.strip():
            fail(errors, f"{label}.id: missing id")
        elif row_id in seen_ids:
            fail(errors, f"{label}.id: duplicate id {row_id}")
        else:
            seen_ids.add(row_id)

        model_name = row.get("model_name")
        if not isinstance(model_name, str) or not model_name.strip():
            fail(errors, f"{label}.model_name: missing model name")
        elif len(model_name) > MAX_MODEL_NAME_LENGTH:
            fail(errors, f"{label}.model_name: exceeds {MAX_MODEL_NAME_LENGTH} characters")

        link = row.get("huggingface_link")
        if not isinstance(link, str) or not link.strip():
            fail(errors, f"{label}.huggingface_link: missing link")
        else:
            normalized = normalized_huggingface_model_url(link)
            if normalized is None:
                fail(errors, f"{label}.huggingface_link: must be a normalized HuggingFace model URL")
            elif normalized != link:
                fail(errors, f"{label}.huggingface_link: must be stored as {normalized}")
            elif link in seen_links:
                fail(errors, f"{label}.huggingface_link: duplicate link {link}")
            else:
                seen_links.add(link)

        status = row.get("status")
        if status not in ALLOWED_STATUS:
            fail(errors, f"{label}.status: must be pending review")

        scores = row.get("benchmark_scores")
        if not isinstance(scores, dict):
            fail(errors, f"{label}.benchmark_scores: must be an object")
        else:
            for score_key in REQUIRED_SCORE_KEYS:
                validate_score(scores.get(score_key), f"{label}.benchmark_scores.{score_key}", errors)

        notes = row.get("notes", "")
        if notes is not None and not isinstance(notes, str):
            fail(errors, f"{label}.notes: must be a string")
        elif isinstance(notes, str) and len(notes) > MAX_NOTES_LENGTH:
            fail(errors, f"{label}.notes: exceeds {MAX_NOTES_LENGTH} characters")

        submitted_at = parse_timestamp(row.get("submitted_at"), f"{label}.submitted_at", errors)
        if submitted_at:
            if previous_submitted_at and submitted_at > previous_submitted_at:
                fail(errors, f"{label}.submitted_at: submissions must be ordered latest first")
            previous_submitted_at = submitted_at
            if latest_submitted_at is None or submitted_at > latest_submitted_at:
                latest_submitted_at = submitted_at

        first_submitted_at = row.get("first_submitted_at")
        if first_submitted_at:
            first_parsed = parse_timestamp(first_submitted_at, f"{label}.first_submitted_at", errors)
            if first_parsed and submitted_at and first_parsed > submitted_at:
                fail(errors, f"{label}.first_submitted_at: cannot be later than submitted_at")

        if row.get("huggingface_reachable") is not True:
            fail(errors, f"{label}.huggingface_reachable: must be true")

        hf_status = row.get("huggingface_status")
        if not isinstance(hf_status, str) or not hf_status.strip():
            fail(errors, f"{label}.huggingface_status: missing reachability status")

        for field in ("model_name", "notes", "status"):
            phrase = contains_forbidden_text(row.get(field))
            if phrase:
                fail(errors, f"{label}.{field}: forbidden phrase {phrase!r}")

    if last_updated and latest_submitted_at:
        parsed_last_updated = parse_timestamp(last_updated, "last_updated", errors)
        if parsed_last_updated and parsed_last_updated < latest_submitted_at:
            fail(errors, "last_updated: cannot be earlier than the latest submission")

    return errors


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    target = Path(argv[0]) if argv else SUBMISSIONS
    if not target.is_absolute():
        target = ROOT / target

    if not target.exists():
        print("FAIL leaderboard submissions validation")
        print(f"- Missing submissions store: {target}")
        return 1

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print("FAIL leaderboard submissions validation")
        print(f"- Invalid JSON: {exc}")
        return 1

    errors = validate_store(data)
    if errors:
        print("FAIL leaderboard submissions validation")
        for error in errors:
            print(f"- {error}")
        return 1

    submissions = data.get("submissions", []) if isinstance(data, dict) else []
    print("PASS leaderboard submissions validation")
    print(f"rows={len(submissions)}")
    print(f"store={target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
