#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_BOARD_20260708.md"
JSON_PATH = ROOT / "docs" / "health_ai_assurance_feedback_triage_board_20260708.json"
INTAKE_MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_FEEDBACK_INTAKE_20260708.md"
INTAKE_JSON_PATH = ROOT / "docs" / "health_ai_assurance_feedback_intake_20260708.json"

REQUIRED_FILES = [
    MD_PATH,
    JSON_PATH,
    INTAKE_MD_PATH,
    INTAKE_JSON_PATH,
    ROOT / ".github" / "ISSUE_TEMPLATE" / "health_ai_assurance_feedback.yml",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "sourcecheckup_review.yml",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "synthetic_failure_case.yml",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "evidence_concern.yml",
]

REQUIRED_MD_PHRASES = [
    "Health AI Assurance Feedback Triage Board",
    "Status: public feedback triage board ready.",
    "Roadmap phase: P10 feedback triage board.",
    "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231",
    ".github/ISSUE_TEMPLATE/health_ai_assurance_feedback.yml",
    ".github/ISSUE_TEMPLATE/sourcecheckup_review.yml",
    ".github/ISSUE_TEMPLATE/synthetic_failure_case.yml",
    ".github/ISSUE_TEMPLATE/evidence_concern.yml",
    "needs_route",
    "needs_rewrite",
    "accepted_for_docs",
    "accepted_for_queue",
    "closed_boundary",
    "needs_owner_review",
    "P10R001",
    "P10R002",
    "P10R003",
    "P10R004",
    "P10R005",
    "P10R006",
    "patient data",
    "private clinical text",
    "provider API runs",
    "physician selection by the agent",
    "clinical validation",
    "model ranking",
    "source truth certification",
    "regulatory compliance",
    "official compatibility",
    "institution support",
]

REQUIRED_ROUTE_IDS = {
    "kit_feedback",
    "source_support_review",
    "synthetic_failure_case",
    "evidence_concern",
}

REQUIRED_ROW_IDS = {"P10R001", "P10R002", "P10R003", "P10R004", "P10R005", "P10R006"}

REQUIRED_TRIAGE_STATES = {
    "needs_route",
    "needs_rewrite",
    "accepted_for_docs",
    "accepted_for_queue",
    "closed_boundary",
    "needs_owner_review",
}

REQUIRED_BLOCKED_CLAIMS = {
    "patient_data",
    "private_clinical_text",
    "real_clinical_notes",
    "private_model_output",
    "provider_api_run",
    "new_case_without_review",
    "physician_selection_by_agent",
    "medical_advice",
    "clinical_validation",
    "model_ranking",
    "source_truth_certification",
    "regulatory_compliance",
    "official_compatibility",
    "institution_support",
    "partnership_claim",
    "payment_claim",
    "terms_acceptance_claim",
}

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "source proves",
    "best model",
    "patient data included",
    "official approval granted",
    "institution endorsed",
]


def read_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def require_phrases(path: Path, phrases: list[str], errors: list[str]) -> str:
    text = read_text(path, errors)
    lower = text.lower()
    for phrase in phrases:
        if phrase.lower() not in lower:
            errors.append(f"{path.relative_to(ROOT)} missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower:
            errors.append(f"{path.relative_to(ROOT)} forbidden phrase present: {phrase}")
    return text


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    md_text = require_phrases(MD_PATH, REQUIRED_MD_PHRASES, errors)
    intake_md_text = read_text(INTAKE_MD_PATH, errors)

    try:
        manifest = json.loads(read_text(JSON_PATH, errors))
    except json.JSONDecodeError as exc:
        errors.append(f"{JSON_PATH.relative_to(ROOT)} invalid JSON: {exc}")
        manifest = {}

    try:
        intake_manifest = json.loads(read_text(INTAKE_JSON_PATH, errors))
    except json.JSONDecodeError as exc:
        errors.append(f"{INTAKE_JSON_PATH.relative_to(ROOT)} invalid JSON: {exc}")
        intake_manifest = {}

    if isinstance(manifest, dict):
        if manifest.get("artifact_id") != "health_ai_assurance_feedback_triage_board_20260708":
            errors.append("Feedback triage board artifact_id mismatch")
        if manifest.get("status") != "public_feedback_triage_board_ready":
            errors.append("Feedback triage board status must be public_feedback_triage_board_ready")
        if manifest.get("phase") != "P10":
            errors.append("Feedback triage board phase must be P10")
        if manifest.get("public_anchor") != "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231":
            errors.append("Feedback triage board public anchor must point to issue 231")
        if manifest.get("input_route_count") != 4:
            errors.append("Feedback triage board must expose 4 input routes")
        if manifest.get("triage_state_count") != 6:
            errors.append("Feedback triage board must expose 6 triage states")
        if manifest.get("board_row_count") != 6:
            errors.append("Feedback triage board must expose 6 board rows")

        input_routes = manifest.get("input_routes", [])
        route_ids = {str(route.get("id")) for route in input_routes if isinstance(route, dict)}
        if route_ids != REQUIRED_ROUTE_IDS:
            errors.append(f"Feedback triage board route ids mismatch: {sorted(route_ids)}")

        intake_route_ids: set[str] = set()
        if isinstance(intake_manifest, dict):
            intake_routes = intake_manifest.get("routes", [])
            intake_route_ids = {str(route.get("id")) for route in intake_routes if isinstance(route, dict)}
        if intake_route_ids and route_ids != intake_route_ids:
            errors.append(f"Feedback triage board routes do not match intake routes: {sorted(route_ids)}")

        for route in input_routes if isinstance(input_routes, list) else []:
            template = route.get("template") if isinstance(route, dict) else None
            if not isinstance(template, str) or not (ROOT / template).exists():
                errors.append(f"Feedback triage board route template missing: {template}")
            elif template not in md_text or template not in intake_md_text:
                errors.append(f"Feedback triage board route template not visible in both public guides: {template}")

        triage_states = {str(state) for state in manifest.get("triage_states", [])}
        if triage_states != REQUIRED_TRIAGE_STATES:
            errors.append(f"Feedback triage board states mismatch: {sorted(triage_states)}")

        rows = manifest.get("board_rows", [])
        row_ids = {str(row.get("id")) for row in rows if isinstance(row, dict)}
        if row_ids != REQUIRED_ROW_IDS:
            errors.append(f"Feedback triage board row ids mismatch: {sorted(row_ids)}")

        row_states = {str(row.get("triage_state")) for row in rows if isinstance(row, dict)}
        if not row_states <= REQUIRED_TRIAGE_STATES:
            errors.append(f"Feedback triage board row states include unknown values: {sorted(row_states)}")
        if not REQUIRED_TRIAGE_STATES <= row_states | {"closed_boundary"}:
            errors.append(f"Feedback triage board row states do not cover required states: {sorted(row_states)}")

        for row in rows if isinstance(rows, list) else []:
            allowed_output = row.get("allowed_output") if isinstance(row, dict) else None
            next_action = row.get("next_action") if isinstance(row, dict) else None
            if not isinstance(allowed_output, str) or not allowed_output:
                errors.append(f"Feedback triage board row missing allowed_output: {row}")
            if not isinstance(next_action, str) or not next_action:
                errors.append(f"Feedback triage board row missing next_action: {row}")

        blocked_claims = {str(claim) for claim in manifest.get("blocked_claims", [])}
        missing_claims = REQUIRED_BLOCKED_CLAIMS - blocked_claims
        if missing_claims:
            errors.append(f"Feedback triage board blocked claims missing: {sorted(missing_claims)}")

        boolean_locks = [
            ("contains_patient_data", False),
            ("provider_api_call_allowed", False),
            ("new_cases_added", False),
            ("agent_selected_physicians", False),
            ("no_medical_advice", True),
            ("no_clinical_validation_claim", True),
            ("no_model_ranking", True),
            ("no_source_truth_certification_claim", True),
            ("no_regulatory_compliance_claim", True),
            ("no_official_compatibility_claim", True),
            ("no_institution_support_claim", True),
        ]
        for key, expected in boolean_locks:
            if manifest.get(key) is not expected:
                errors.append(f"Feedback triage board {key} must be {expected}")

    for phrase in [
        "patient data",
        "private clinical text",
        "provider api runs",
        "clinical validation",
        "model ranking",
        "source truth certification",
        "regulatory compliance",
        "official compatibility",
        "institution support",
        "physician selection",
    ]:
        if phrase not in md_text.lower():
            errors.append(f"Boundary phrase must appear in triage guide: {phrase}")

    if errors:
        print("FAIL health AI assurance feedback triage board validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS health AI assurance feedback triage board validation")
    print(f"guide={MD_PATH.relative_to(ROOT)}")
    print(f"manifest={JSON_PATH.relative_to(ROOT)}")
    print(f"routes={manifest.get('input_route_count')}")
    print(f"states={manifest.get('triage_state_count')}")
    print(f"rows={manifest.get('board_row_count')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
