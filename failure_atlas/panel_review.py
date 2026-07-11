from __future__ import annotations

import csv
import json
import os
import tempfile
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from failure_atlas.data import SchemaValidationError, load_tsv_rows


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PANEL_CASES_PATH = ROOT / "data" / "panel_pilot" / "clinician_panel_pilot_cases_v0_1.tsv"
DEFAULT_RATING_TEMPLATE_PATH = ROOT / "data" / "panel_pilot" / "clinician_panel_rating_sheet_v0_1.tsv"
DEFAULT_REVIEW_STORE_PATH = ROOT / ".local" / "clinician_review_console" / "reviews.json"

PANEL_CASE_COLUMNS = (
    "panel_case_id",
    "source_scenario_id",
    "language",
    "theme",
    "domain",
    "setting",
    "synthetic_patient_summary",
    "task_for_model",
    "expected_safety_focus",
    "review_question",
    "patient_data_status",
    "rating_status",
)

RATING_TEMPLATE_COLUMNS = (
    "panel_case_id",
    "reviewer_code",
    "language",
    "clinical_domain",
    "severity_1_to_5",
    "likely_harm_if_copied",
    "missing_safety_gate",
    "failure_tags",
    "confidence",
    "free_text_note",
    "should_this_case_stay_in_benchmark",
    "possible_patient_data_flag",
)

REVIEW_COLUMNS = RATING_TEMPLATE_COLUMNS + ("updated_at_utc",)
YES_NO_UNCLEAR = {"yes", "no", "unclear"}
STAY_CHOICES = {"yes", "no", "revise"}
PATIENT_DATA_CHOICES = {"no", "possible", "yes"}


@dataclass(frozen=True)
class PanelCase:
    panel_case_id: str
    source_scenario_id: str
    language: str
    theme: str
    domain: str
    setting: str
    synthetic_patient_summary: str
    task_for_model: str
    expected_safety_focus: str
    review_question: str
    patient_data_status: str
    rating_status: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "PanelCase":
        return cls(**{column: row[column] for column in PANEL_CASE_COLUMNS})

    def to_dict(self) -> dict[str, str]:
        return {column: getattr(self, column) for column in PANEL_CASE_COLUMNS}


def load_panel_cases(path: str | Path = DEFAULT_PANEL_CASES_PATH) -> list[PanelCase]:
    rows = load_tsv_rows(path, PANEL_CASE_COLUMNS)
    _require_unique(rows, "panel_case_id", Path(path))
    cases = [PanelCase.from_row(row) for row in rows]
    for case in cases:
        if "synthetic" not in case.patient_data_status.lower():
            raise SchemaValidationError(f"{path} contains a non-synthetic patient data status for {case.panel_case_id}")
    return cases


def load_rating_template(path: str | Path = DEFAULT_RATING_TEMPLATE_PATH) -> list[dict[str, str]]:
    rows = load_tsv_rows(path, RATING_TEMPLATE_COLUMNS)
    seen: set[tuple[str, str]] = set()
    for row in rows:
        key = (row["panel_case_id"], row["reviewer_code"])
        if key in seen:
            raise SchemaValidationError(f"{path} duplicates review assignment {key[0]} / {key[1]}")
        seen.add(key)
    return rows


def reviewer_codes(template_rows: list[dict[str, str]]) -> list[str]:
    return sorted({row["reviewer_code"] for row in template_rows if row["reviewer_code"]})


def load_reviews(path: str | Path = DEFAULT_REVIEW_STORE_PATH) -> list[dict[str, Any]]:
    target = Path(path)
    if not target.exists():
        return []
    with target.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        records = data.get("records", [])
    else:
        raise SchemaValidationError(f"{target} must contain a JSON object or list")
    if not isinstance(records, list):
        raise SchemaValidationError(f"{target} records must be a list")
    return [dict(record) for record in records]


def save_reviews(records: list[dict[str, Any]], path: str | Path = DEFAULT_REVIEW_STORE_PATH) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "clinician_review_console_v0_1",
        "updated_at_utc": utc_now(),
        "records": sorted(records, key=lambda row: (str(row.get("panel_case_id", "")), str(row.get("reviewer_code", "")))),
    }
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=str(target.parent), text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(tmp_name, target)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def upsert_review(
    payload: dict[str, Any],
    *,
    cases: list[PanelCase],
    template_rows: list[dict[str, str]],
    path: str | Path = DEFAULT_REVIEW_STORE_PATH,
) -> dict[str, Any]:
    record = normalize_review_payload(payload, cases=cases, template_rows=template_rows)
    records = [
        existing
        for existing in load_reviews(path)
        if not (
            existing.get("panel_case_id") == record["panel_case_id"]
            and existing.get("reviewer_code") == record["reviewer_code"]
        )
    ]
    records.append(record)
    save_reviews(records, path)
    return record


def normalize_review_payload(
    payload: dict[str, Any],
    *,
    cases: list[PanelCase],
    template_rows: list[dict[str, str]],
) -> dict[str, Any]:
    case_map = {case.panel_case_id: case for case in cases}
    assignment_map = {(row["panel_case_id"], row["reviewer_code"]): row for row in template_rows}
    panel_case_id = _text(payload.get("panel_case_id") or payload.get("case_id"))
    reviewer_code = _text(payload.get("reviewer_code"))
    if panel_case_id not in case_map:
        raise ValueError(f"Unknown panel_case_id: {panel_case_id}")
    if reviewer_code not in reviewer_codes(template_rows):
        raise ValueError(f"Unknown reviewer_code: {reviewer_code}")
    if (panel_case_id, reviewer_code) not in assignment_map:
        raise ValueError(f"Reviewer {reviewer_code} is not assigned to {panel_case_id}")

    case = case_map[panel_case_id]
    severity = _int_between(payload.get("severity_1_to_5"), "severity_1_to_5", 1, 5)
    confidence = _int_between(payload.get("confidence"), "confidence", 1, 5)
    likely_harm = _choice(payload.get("likely_harm_if_copied"), "likely_harm_if_copied", YES_NO_UNCLEAR)
    should_stay = _choice(payload.get("should_this_case_stay_in_benchmark"), "should_this_case_stay_in_benchmark", STAY_CHOICES)
    patient_data_flag = _choice(
        payload.get("possible_patient_data_flag") or "no",
        "possible_patient_data_flag",
        PATIENT_DATA_CHOICES,
    )

    return {
        "panel_case_id": panel_case_id,
        "reviewer_code": reviewer_code,
        "language": _text(payload.get("language")) or case.language,
        "clinical_domain": case.domain,
        "severity_1_to_5": severity,
        "likely_harm_if_copied": likely_harm,
        "missing_safety_gate": _text(payload.get("missing_safety_gate")),
        "failure_tags": _text(payload.get("failure_tags")),
        "confidence": confidence,
        "free_text_note": _text(payload.get("free_text_note")),
        "should_this_case_stay_in_benchmark": should_stay,
        "possible_patient_data_flag": patient_data_flag,
        "updated_at_utc": utc_now(),
    }


def progress_summary(
    cases: list[PanelCase],
    template_rows: list[dict[str, str]],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    assignments = {(row["panel_case_id"], row["reviewer_code"]) for row in template_rows}
    completed = {
        (str(row.get("panel_case_id")), str(row.get("reviewer_code")))
        for row in records
        if row.get("severity_1_to_5") not in ("", None)
    }
    by_reviewer: dict[str, dict[str, int]] = {}
    for reviewer in reviewer_codes(template_rows):
        assigned_count = sum(1 for _, reviewer_code in assignments if reviewer_code == reviewer)
        completed_count = sum(1 for _, reviewer_code in completed if reviewer_code == reviewer)
        by_reviewer[reviewer] = {"assigned": assigned_count, "completed": completed_count}
    completed_cases = {
        case.panel_case_id: sum(1 for review_case, _ in completed if review_case == case.panel_case_id)
        for case in cases
    }
    return {
        "case_count": len(cases),
        "assignment_count": len(assignments),
        "completed_count": len(completed & assignments),
        "by_reviewer": by_reviewer,
        "completed_cases": completed_cases,
    }


def cohen_kappa(
    records: list[dict[str, Any]],
    *,
    reviewer_a: str = "R01",
    reviewer_b: str = "R02",
    field: str = "severity_1_to_5",
) -> dict[str, Any]:
    by_reviewer: dict[str, dict[str, Any]] = {reviewer_a: {}, reviewer_b: {}}
    for row in records:
        reviewer = str(row.get("reviewer_code", ""))
        case_id = str(row.get("panel_case_id", ""))
        value = row.get(field)
        if reviewer in by_reviewer and case_id and value not in ("", None):
            by_reviewer[reviewer][case_id] = value

    shared_cases = sorted(set(by_reviewer[reviewer_a]) & set(by_reviewer[reviewer_b]))
    n = len(shared_cases)
    if not n:
        return {"reviewer_a": reviewer_a, "reviewer_b": reviewer_b, "field": field, "n": 0, "kappa": None}

    values_a = [by_reviewer[reviewer_a][case_id] for case_id in shared_cases]
    values_b = [by_reviewer[reviewer_b][case_id] for case_id in shared_cases]
    observed = sum(1 for left, right in zip(values_a, values_b) if left == right) / n
    counts_a = Counter(values_a)
    counts_b = Counter(values_b)
    labels = set(counts_a) | set(counts_b)
    expected = sum((counts_a[label] / n) * (counts_b[label] / n) for label in labels)
    if expected == 1:
        kappa_value = 1.0 if observed == 1 else None
    else:
        kappa_value = (observed - expected) / (1 - expected)
    return {
        "reviewer_a": reviewer_a,
        "reviewer_b": reviewer_b,
        "field": field,
        "n": n,
        "observed_agreement": round(observed, 4),
        "expected_agreement": round(expected, 4),
        "kappa": None if kappa_value is None else round(kappa_value, 4),
    }


def write_reviews_csv(records: list[dict[str, Any]], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        for row in records:
            writer.writerow({column: row.get(column, "") for column in REVIEW_COLUMNS})


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _require_unique(rows: list[dict[str, str]], column: str, path: Path) -> None:
    seen: set[str] = set()
    for index, row in enumerate(rows, start=2):
        value = row[column]
        if value in seen:
            raise SchemaValidationError(f"{path}:{index} duplicates {column} {value}")
        seen.add(value)


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _int_between(value: Any, label: str, minimum: int, maximum: int) -> int:
    text = _text(value)
    if not text:
        raise ValueError(f"{label} is required")
    try:
        integer = int(text)
    except ValueError as exc:
        raise ValueError(f"{label} must be an integer") from exc
    if not minimum <= integer <= maximum:
        raise ValueError(f"{label} must be between {minimum} and {maximum}")
    return integer


def _choice(value: Any, label: str, allowed: set[str]) -> str:
    text = _text(value).lower()
    if text not in allowed:
        raise ValueError(f"{label} must be one of: {', '.join(sorted(allowed))}")
    return text
