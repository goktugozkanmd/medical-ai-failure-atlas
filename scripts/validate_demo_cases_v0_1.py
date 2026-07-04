#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "clinical_safety_demo_cases_v0_1.json"
SOURCE_NOTE = ROOT / "docs" / "DEMO_CASE_SOURCE_VERIFICATION_V0_1.md"

SCHEMA_VERSION = "clinical_safety_demo_cases_v0_1"
EXPECTED_CASE_ORDER = ("DEMO001", "DEMO002", "DEMO003")
EXPECTED_CASE_IDS = set(EXPECTED_CASE_ORDER)
EXPECTED_CASE_PROFILES = {
    "DEMO001": {
        "danger_gate": "missed_anticoagulant_interaction",
        "source_hosts": ("dailymed.nlm.nih.gov",),
        "source_support_terms": ("warfarin", "prothrombin", "inr"),
        "required_tags": (
            "drug_interaction",
            "monitoring_omission",
            "anticoagulation_safety",
            "unsafe_reassurance",
        ),
        "required_field_terms": {
            "title": ("warfarin", "sulfamethoxazole", "trimethoprim"),
            "scenario_prompt": (
                "warfarin",
                "sulfamethoxazole",
                "trimethoprim",
                "monitoring",
            ),
            "clinical_risk": ("interaction", "monitoring"),
            "expected_safe_answer": ("interaction", "inr", "monitoring"),
        },
    },
    "DEMO002": {
        "danger_gate": "unsafe_reassurance_for_possible_acute_coronary_syndrome",
        "source_hosts": ("professional.heart.org",),
        "source_support_terms": ("diabetes", "elderly", "abdominal", "structured"),
        "required_tags": (
            "escalation_boundary",
            "cardiac_red_flag",
            "risk_factor_context",
            "unsafe_reassurance",
        ),
        "required_field_terms": {
            "title": ("diabetes", "upper abdominal"),
            "scenario_prompt": (
                "older",
                "diabetes",
                "upper abdominal",
                "nausea",
                "sweating",
            ),
            "clinical_risk": ("ischemic", "urgent"),
            "expected_safe_answer": ("urgent", "emergency", "acute coronary syndrome"),
        },
    },
    "DEMO003": {
        "danger_gate": "kidney_risk_ignored_for_nsaid",
        "source_hosts": ("www.kidney.org",),
        "source_support_terms": ("chronic kidney disease", "nsaid", "egfr", "60"),
        "required_tags": (
            "kidney_safety",
            "over_the_counter_medication",
            "contraindication_context",
            "unsafe_reassurance",
        ),
        "required_field_terms": {
            "title": ("kidney", "nsaid"),
            "scenario_prompt": ("chronic kidney disease", "egfr", "ibuprofen", "naproxen"),
            "clinical_risk": ("kidney risk", "clinician review"),
            "expected_safe_answer": ("nsaid", "kidney risk", "clinician"),
        },
    },
}
ALLOWED_SOURCE_HOSTS = {
    "dailymed.nlm.nih.gov",
    "professional.heart.org",
    "www.kidney.org",
}
REQUIRED_CASE_KEYS = {
    "case_id",
    "title",
    "synthetic_only",
    "contains_patient_data",
    "clinical_advice_allowed",
    "scenario_prompt",
    "unsafe_model_answer",
    "danger_gate",
    "clinical_risk",
    "expected_safe_answer",
    "taxonomy_tags",
    "scoring_expectation",
    "source_anchors",
}
REQUIRED_BOUNDARY_PHRASES = [
    "synthetic",
    "not clinical advice",
    "not patient data",
    "not clinical validation",
    "not clinical deployment",
]
FORBIDDEN_PUBLIC_CLAIMS = [
    "clinically validated",
    "deployment ready",
    "clinical deployment ready",
    "approved by",
    "endorsed by",
    "ranked best",
    "model ranking confirmed",
    "score certified",
    "source truth certified",
    "patient data used",
    "real patient",
]
PRIVATE_DATA_PATTERNS = [
    ("email address", re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")),
    ("phone or long numeric identifier", re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{10,}\d)(?!\d)")),
    ("secret token marker", re.compile(r"\b(api[_ -]?key|token|secret|password)\b", re.IGNORECASE)),
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def iter_strings(value: object) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            strings.extend(iter_strings(item))
    elif isinstance(value, list):
        for item in value:
            strings.extend(iter_strings(item))
    return strings


def validate_text_safety(value: object, label: str, errors: list[str]) -> None:
    text = "\n".join(iter_strings(value))
    lower_text = text.lower()
    for phrase in FORBIDDEN_PUBLIC_CLAIMS:
        if phrase in lower_text:
            fail(errors, f"{label}: forbidden public claim {phrase!r}")
    for name, pattern in PRIVATE_DATA_PATTERNS:
        if pattern.search(text):
            fail(errors, f"{label}: private data pattern {name!r}")


def validate_required_terms(
    value: object,
    label: str,
    terms: tuple[str, ...],
    errors: list[str],
) -> None:
    if not isinstance(value, str):
        return

    lower_value = value.lower()
    for term in terms:
        if term not in lower_value:
            fail(errors, f"{label}: missing locked demo term {term!r}")


def collect_source_anchor_urls(payload: object) -> list[tuple[str, int, str]]:
    if not isinstance(payload, dict):
        return []

    cases = payload.get("cases")
    if not isinstance(cases, list):
        return []

    urls: list[tuple[str, int, str]] = []
    for case_index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            continue
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            case_id = f"cases[{case_index}]"

        anchors = case.get("source_anchors")
        if not isinstance(anchors, list):
            continue
        for anchor_index, anchor in enumerate(anchors, start=1):
            if not isinstance(anchor, dict):
                continue
            url = anchor.get("url")
            if isinstance(url, str) and url.strip():
                urls.append((case_id, anchor_index, url.strip()))
    return urls


def validate_source_anchor(anchor: object, label: str, errors: list[str]) -> None:
    if not isinstance(anchor, dict):
        fail(errors, f"{label}: source anchor must be an object")
        return

    for key in ("label", "url", "supports"):
        value = anchor.get(key)
        if not isinstance(value, str) or not value.strip():
            fail(errors, f"{label}.{key}: missing text")

    url = anchor.get("url")
    if isinstance(url, str) and url.strip():
        parsed = urlparse(url)
        if parsed.scheme != "https":
            fail(errors, f"{label}.url: source URL must use https")
        if parsed.netloc not in ALLOWED_SOURCE_HOSTS:
            fail(errors, f"{label}.url: source host is not trusted")


def validate_locked_case_profile(
    case: dict[str, object],
    case_id: str,
    label: str,
    errors: list[str],
) -> None:
    profile = EXPECTED_CASE_PROFILES.get(case_id)
    if not profile:
        return

    danger_gate = case.get("danger_gate")
    expected_danger_gate = profile["danger_gate"]
    if isinstance(danger_gate, str) and danger_gate != expected_danger_gate:
        fail(errors, f"{label}.danger_gate: must be {expected_danger_gate!r}")

    tags = case.get("taxonomy_tags")
    if isinstance(tags, list):
        tag_set = {tag for tag in tags if isinstance(tag, str)}
        for tag in profile["required_tags"]:
            if tag not in tag_set:
                fail(errors, f"{label}.taxonomy_tags: missing locked demo tag {tag!r}")

    field_terms = profile["required_field_terms"]
    for field, terms in field_terms.items():
        validate_required_terms(case.get(field), f"{label}.{field}", terms, errors)

    source_anchors = case.get("source_anchors")
    source_text = "\n".join(iter_strings(source_anchors))
    lower_source_text = source_text.lower()
    for term in profile["source_support_terms"]:
        if term not in lower_source_text:
            fail(errors, f"{label}.source_anchors: missing locked source support term {term!r}")

    source_hosts: set[str] = set()
    if isinstance(source_anchors, list):
        for anchor in source_anchors:
            if not isinstance(anchor, dict):
                continue
            url = anchor.get("url")
            if isinstance(url, str):
                source_hosts.add(urlparse(url).netloc)

    for host in profile["source_hosts"]:
        if host not in source_hosts:
            fail(errors, f"{label}.source_anchors: missing locked source host {host!r}")


def validate_case(case: object, index: int, errors: list[str]) -> str | None:
    label = f"cases[{index}]"
    if not isinstance(case, dict):
        fail(errors, f"{label}: case must be an object")
        return None

    missing_keys = sorted(REQUIRED_CASE_KEYS - set(case))
    for key in missing_keys:
        fail(errors, f"{label}.{key}: missing field")

    unexpected_keys = sorted(set(case) - REQUIRED_CASE_KEYS)
    for key in unexpected_keys:
        fail(errors, f"{label}.{key}: unexpected field")

    case_id = case.get("case_id")
    if not isinstance(case_id, str) or not case_id.strip():
        fail(errors, f"{label}.case_id: missing case id")
        case_id = None

    if case.get("synthetic_only") is not True:
        fail(errors, f"{label}.synthetic_only: must be true")
    if case.get("contains_patient_data") is not False:
        fail(errors, f"{label}.contains_patient_data: must be false")
    if case.get("clinical_advice_allowed") is not False:
        fail(errors, f"{label}.clinical_advice_allowed: must be false")

    for key in (
        "title",
        "scenario_prompt",
        "unsafe_model_answer",
        "danger_gate",
        "clinical_risk",
        "expected_safe_answer",
    ):
        value = case.get(key)
        if not isinstance(value, str) or not value.strip():
            fail(errors, f"{label}.{key}: missing text")

    tags = case.get("taxonomy_tags")
    if not isinstance(tags, list) or len(tags) < 3:
        fail(errors, f"{label}.taxonomy_tags: must contain at least three tags")
    elif any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        fail(errors, f"{label}.taxonomy_tags: tags must be non empty strings")

    scoring = case.get("scoring_expectation")
    if not isinstance(scoring, dict) or not scoring:
        fail(errors, f"{label}.scoring_expectation: must be a non empty object")
    elif scoring.get("danger_gate_required") is not True:
        fail(errors, f"{label}.scoring_expectation.danger_gate_required: must be true")

    source_anchors = case.get("source_anchors")
    if not isinstance(source_anchors, list) or not source_anchors:
        fail(errors, f"{label}.source_anchors: must contain at least one source anchor")
    else:
        for anchor_index, anchor in enumerate(source_anchors, start=1):
            validate_source_anchor(anchor, f"{label}.source_anchors[{anchor_index}]", errors)

    validate_text_safety(case, label, errors)

    if case_id:
        validate_locked_case_profile(case, case_id, label, errors)
    return case_id


def validate_payload(payload: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["Demo case file must contain a JSON object"]

    if payload.get("schema_version") != SCHEMA_VERSION:
        fail(errors, f"schema_version must be {SCHEMA_VERSION}")

    intended_use = payload.get("intended_use")
    if not isinstance(intended_use, str) or not intended_use.strip():
        fail(errors, "intended_use: missing text")
    else:
        lower_intended_use = intended_use.lower()
        for phrase in REQUIRED_BOUNDARY_PHRASES:
            if phrase not in lower_intended_use:
                fail(errors, f"intended_use: missing boundary phrase {phrase!r}")

    # Compare with POSIX-style separators so the check is portable across
    # Windows (\), macOS/Linux (/) and CI runners. The seed JSON stores a
    # forward-slash relative path.
    if payload.get("source_verification_note") != SOURCE_NOTE.relative_to(ROOT).as_posix():
        fail(errors, "source_verification_note: must point to the visible source note")

    cases = payload.get("cases")
    if not isinstance(cases, list):
        fail(errors, "cases: must be a list")
        cases = []

    if payload.get("case_count") != len(cases):
        fail(errors, "case_count: must match cases length")
    if len(cases) != 3:
        fail(errors, "cases: must contain exactly three demo cases")

    seen_case_ids: set[str] = set()
    for index, case in enumerate(cases, start=1):
        case_id = validate_case(case, index, errors)
        if case_id:
            if index <= len(EXPECTED_CASE_ORDER):
                expected_case_id = EXPECTED_CASE_ORDER[index - 1]
                if case_id != expected_case_id:
                    fail(
                        errors,
                        f"cases[{index}].case_id: expected {expected_case_id} at position {index}",
                    )
            if case_id in seen_case_ids:
                fail(errors, f"cases[{index}].case_id: duplicate case id {case_id}")
            seen_case_ids.add(case_id)

    if seen_case_ids and seen_case_ids != EXPECTED_CASE_IDS:
        fail(errors, "cases: case ids must be DEMO001, DEMO002, and DEMO003")

    validate_text_safety(payload, "payload", errors)
    return errors


def validate_files(data_path: Path = DATA, source_note_path: Path = SOURCE_NOTE) -> list[str]:
    errors: list[str] = []
    if not data_path.exists():
        return [f"Missing demo case file: {data_path.relative_to(ROOT)}"]
    if not source_note_path.exists():
        errors.append(f"Missing source verification note: {source_note_path.relative_to(ROOT)}")

    try:
        payload = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON: {exc}"]

    errors.extend(validate_payload(payload))

    if source_note_path.exists():
        note_text = source_note_path.read_text(encoding="utf-8")
        for case_id in EXPECTED_CASE_IDS:
            if case_id not in note_text:
                fail(errors, f"source verification note: missing {case_id}")
        for case_id, anchor_index, url in collect_source_anchor_urls(payload):
            if url not in note_text:
                fail(
                    errors,
                    "source verification note: missing source URL "
                    f"for {case_id} anchor {anchor_index}",
                )
        validate_text_safety(note_text, "source verification note", errors)

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("FAIL demo cases validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS demo cases validation")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_note={SOURCE_NOTE.relative_to(ROOT)}")
    print("cases=3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
