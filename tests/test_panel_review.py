from __future__ import annotations

import json
from pathlib import Path

from failure_atlas.panel_review import (
    cohen_kappa,
    load_panel_cases,
    load_rating_template,
    load_reviews,
    normalize_review_payload,
    progress_summary,
    reviewer_codes,
    upsert_review,
    write_reviews_csv,
)


ROOT = Path(__file__).resolve().parents[1]


def test_load_panel_cases_are_synthetic() -> None:
    cases = load_panel_cases(ROOT / "data" / "panel_pilot" / "clinician_panel_pilot_cases_v0_1.tsv")

    assert len(cases) == 15
    assert cases[0].panel_case_id == "MFB_PANEL_001"
    assert all("synthetic" in case.patient_data_status for case in cases)


def test_rating_template_assigns_two_reviewers_per_case() -> None:
    rows = load_rating_template(ROOT / "data" / "panel_pilot" / "clinician_panel_rating_sheet_v0_1.tsv")

    assert reviewer_codes(rows) == ["R01", "R02"]
    assert len(rows) == 30


def test_normalize_review_payload_validates_required_fields() -> None:
    cases = load_panel_cases(ROOT / "data" / "panel_pilot" / "clinician_panel_pilot_cases_v0_1.tsv")
    template = load_rating_template(ROOT / "data" / "panel_pilot" / "clinician_panel_rating_sheet_v0_1.tsv")

    record = normalize_review_payload(
        {
            "panel_case_id": "MFB_PANEL_001",
            "reviewer_code": "R01",
            "severity_1_to_5": "4",
            "confidence": "5",
            "likely_harm_if_copied": "yes",
            "missing_safety_gate": "missed_urgent_escalation",
            "failure_tags": "false_reassurance",
            "should_this_case_stay_in_benchmark": "yes",
            "possible_patient_data_flag": "no",
        },
        cases=cases,
        template_rows=template,
    )

    assert record["clinical_domain"] == "Cardiology"
    assert record["severity_1_to_5"] == 4
    assert record["confidence"] == 5
    assert record["likely_harm_if_copied"] == "yes"


def test_upsert_review_and_progress_summary(tmp_path: Path) -> None:
    cases = load_panel_cases(ROOT / "data" / "panel_pilot" / "clinician_panel_pilot_cases_v0_1.tsv")
    template = load_rating_template(ROOT / "data" / "panel_pilot" / "clinician_panel_rating_sheet_v0_1.tsv")
    store = tmp_path / "reviews.json"

    upsert_review(
        {
            "panel_case_id": "MFB_PANEL_001",
            "reviewer_code": "R01",
            "severity_1_to_5": 3,
            "confidence": 4,
            "likely_harm_if_copied": "unclear",
            "should_this_case_stay_in_benchmark": "revise",
            "possible_patient_data_flag": "no",
        },
        cases=cases,
        template_rows=template,
        path=store,
    )
    upsert_review(
        {
            "panel_case_id": "MFB_PANEL_001",
            "reviewer_code": "R01",
            "severity_1_to_5": 4,
            "confidence": 4,
            "likely_harm_if_copied": "yes",
            "should_this_case_stay_in_benchmark": "yes",
            "possible_patient_data_flag": "no",
        },
        cases=cases,
        template_rows=template,
        path=store,
    )

    records = load_reviews(store)
    assert len(records) == 1
    assert records[0]["severity_1_to_5"] == 4
    summary = progress_summary(cases, template, records)
    assert summary["assignment_count"] == 30
    assert summary["completed_count"] == 1
    assert summary["by_reviewer"]["R01"] == {"assigned": 15, "completed": 1}


def test_cohen_kappa_and_csv_export(tmp_path: Path) -> None:
    records = [
        {"panel_case_id": "A", "reviewer_code": "R01", "severity_1_to_5": 4},
        {"panel_case_id": "A", "reviewer_code": "R02", "severity_1_to_5": 4},
        {"panel_case_id": "B", "reviewer_code": "R01", "severity_1_to_5": 3},
        {"panel_case_id": "B", "reviewer_code": "R02", "severity_1_to_5": 2},
    ]

    result = cohen_kappa(records)
    assert result["n"] == 2
    assert result["observed_agreement"] == 0.5
    assert result["kappa"] == 0.3333

    out = tmp_path / "reviews.csv"
    write_reviews_csv(records, out)
    assert "panel_case_id,reviewer_code" in out.read_text(encoding="utf-8")


def test_review_store_schema_is_json_object(tmp_path: Path) -> None:
    cases = load_panel_cases(ROOT / "data" / "panel_pilot" / "clinician_panel_pilot_cases_v0_1.tsv")
    template = load_rating_template(ROOT / "data" / "panel_pilot" / "clinician_panel_rating_sheet_v0_1.tsv")
    store = tmp_path / "reviews.json"

    upsert_review(
        {
            "panel_case_id": "MFB_PANEL_002",
            "reviewer_code": "R02",
            "severity_1_to_5": 5,
            "confidence": 5,
            "likely_harm_if_copied": "yes",
            "should_this_case_stay_in_benchmark": "yes",
            "possible_patient_data_flag": "no",
        },
        cases=cases,
        template_rows=template,
        path=store,
    )

    payload = json.loads(store.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "clinician_review_console_v0_1"
    assert payload["records"][0]["panel_case_id"] == "MFB_PANEL_002"
