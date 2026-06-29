from __future__ import annotations

import copy
import json
from pathlib import Path

from scripts.validate_demo_cases_v0_1 import DATA, validate_payload


def load_seed_payload() -> dict[str, object]:
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_demo_cases_seed_file_validates() -> None:
    assert validate_payload(load_seed_payload()) == []


def test_demo_cases_requires_exact_three_case_set() -> None:
    payload = load_seed_payload()
    payload["cases"] = payload["cases"][:2]
    payload["case_count"] = 2

    errors = validate_payload(payload)

    assert "cases: must contain exactly three demo cases" in errors


def test_demo_cases_rejects_missing_source_anchor() -> None:
    payload = load_seed_payload()
    case = copy.deepcopy(payload["cases"][0])
    case["source_anchors"] = []
    payload["cases"][0] = case

    errors = validate_payload(payload)

    assert "cases[1].source_anchors: must contain at least one source anchor" in errors


def test_demo_cases_rejects_untrusted_source_anchor_host() -> None:
    payload = load_seed_payload()
    case = copy.deepcopy(payload["cases"][0])
    case["source_anchors"][0]["url"] = "https://example.com/source"
    payload["cases"][0] = case

    errors = validate_payload(payload)

    assert "cases[1].source_anchors[1].url: source host is not trusted" in errors


def test_demo_cases_rejects_clinical_deployment_claim() -> None:
    payload = load_seed_payload()
    case = copy.deepcopy(payload["cases"][1])
    case["expected_safe_answer"] = "This is clinical deployment ready."
    payload["cases"][1] = case

    errors = validate_payload(payload)

    assert "cases[2]: forbidden public claim 'deployment ready'" in errors


def test_demo_cases_rejects_private_contact_details() -> None:
    payload = load_seed_payload()
    case = copy.deepcopy(payload["cases"][2])
    case["unsafe_model_answer"] = "Send details to reviewer@example.com."
    payload["cases"][2] = case

    errors = validate_payload(payload)

    assert "cases[3]: private data pattern 'email address'" in errors


def test_demo_cases_data_path_is_versioned_json() -> None:
    assert Path(DATA).name == "clinical_safety_demo_cases_v0_1.json"
