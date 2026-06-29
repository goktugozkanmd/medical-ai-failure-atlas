from __future__ import annotations

import copy
import json
from pathlib import Path

from scripts.validate_demo_cases_v0_1 import DATA, SOURCE_NOTE, validate_files, validate_payload


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


def test_demo_cases_rejects_locked_case_order_drift() -> None:
    payload = load_seed_payload()
    payload["cases"] = [payload["cases"][1], payload["cases"][0], payload["cases"][2]]

    errors = validate_payload(payload)

    assert "cases[1].case_id: expected DEMO001 at position 1" in errors
    assert "cases[2].case_id: expected DEMO002 at position 2" in errors


def test_demo_cases_rejects_locked_danger_gate_drift() -> None:
    payload = load_seed_payload()
    case = copy.deepcopy(payload["cases"][0])
    case["danger_gate"] = "generic_medication_warning"
    payload["cases"][0] = case

    errors = validate_payload(payload)

    assert "cases[1].danger_gate: must be 'missed_anticoagulant_interaction'" in errors


def test_demo_cases_rejects_locked_safe_answer_term_drift() -> None:
    payload = load_seed_payload()
    case = copy.deepcopy(payload["cases"][0])
    case["expected_safe_answer"] = "Flag the interaction risk and recommend clinician review."
    payload["cases"][0] = case

    errors = validate_payload(payload)

    assert "cases[1].expected_safe_answer: missing locked demo term 'inr'" in errors
    assert "cases[1].expected_safe_answer: missing locked demo term 'monitoring'" in errors


def test_demo_cases_rejects_locked_source_host_drift() -> None:
    payload = load_seed_payload()
    case = copy.deepcopy(payload["cases"][2])
    case["source_anchors"][0]["url"] = payload["cases"][0]["source_anchors"][0]["url"]
    payload["cases"][2] = case

    errors = validate_payload(payload)

    assert "cases[3].source_anchors: missing locked source host 'www.kidney.org'" in errors


def test_demo_cases_rejects_locked_taxonomy_tag_drift() -> None:
    payload = load_seed_payload()
    case = copy.deepcopy(payload["cases"][1])
    case["taxonomy_tags"] = ["escalation_boundary", "risk_factor_context", "unsafe_reassurance"]
    payload["cases"][1] = case

    errors = validate_payload(payload)

    assert "cases[2].taxonomy_tags: missing locked demo tag 'cardiac_red_flag'" in errors


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


def test_demo_cases_source_note_must_contain_anchor_urls(tmp_path: Path) -> None:
    note = SOURCE_NOTE.read_text(encoding="utf-8")
    url = load_seed_payload()["cases"][0]["source_anchors"][0]["url"]
    source_note = tmp_path / "DEMO_CASE_SOURCE_VERIFICATION_V0_1.md"
    source_note.write_text(note.replace(url, "https://dailymed.nlm.nih.gov/"), encoding="utf-8")

    errors = validate_files(source_note_path=source_note)

    assert "source verification note: missing source URL for DEMO001 anchor 1" in errors


def test_demo_cases_data_path_is_versioned_json() -> None:
    assert Path(DATA).name == "clinical_safety_demo_cases_v0_1.json"
