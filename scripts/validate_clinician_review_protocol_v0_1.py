#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs" / "CLINICIAN_REVIEW_PROTOCOL_V0_1.md"
STATES = ROOT / "failure_atlas" / "public" / "clinician_review_states_v0_1.json"

REQUIRED_PROTOCOL_PHRASES = [
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "synthetic_preview_only",
    "needs_clinician_review",
    "needs_source_review",
    "needs_adjudication",
    "not_for_public_summary",
    "ready_for_public_synthetic_summary",
    "Release gate checklist",
    "Disagreement rule",
    "SourceCheckup routing",
    "Warning sign reviewer role table",
    "Label audit reviewer role table",
    "Escalation gate audit rows",
    "make warning_sign_role_table",
    "make label_audit_role_table",
    "Track A use",
    "Track B use",
]

REQUIRED_STATES = {
    "synthetic_preview_only",
    "needs_clinician_review",
    "needs_source_review",
    "needs_adjudication",
    "not_for_public_summary",
    "ready_for_public_synthetic_summary",
}

REQUIRED_FIELDS = {
    "case_id",
    "reviewer_role",
    "review_date",
    "synthetic_boundary_ok",
    "patient_data_absent",
    "raw_model_output_absent",
    "taxonomy_mapping_ok",
    "safe_answer_boundary_ok",
    "sourcecheckup_needed",
    "review_state",
    "release_gate_decision",
    "short_reason",
}

FORBIDDEN_PHRASES = [
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "best model",
    "officially approved for use",
    "patient data used",
]


def main() -> int:
    errors: list[str] = []
    if not PROTOCOL.exists():
        errors.append(f"Missing protocol: {PROTOCOL}")
        protocol_text = ""
    else:
        protocol_text = PROTOCOL.read_text(encoding="utf-8")
    lower_protocol = protocol_text.lower()

    for phrase in REQUIRED_PROTOCOL_PHRASES:
        if phrase.lower() not in lower_protocol:
            errors.append(f"Protocol missing required phrase: {phrase}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_protocol:
            errors.append(f"Protocol contains forbidden phrase: {phrase}")

    if not STATES.exists():
        errors.append(f"Missing states file: {STATES}")
        states_data: dict[str, object] = {}
    else:
        states_data = json.loads(STATES.read_text(encoding="utf-8"))

    state_ids = {
        str(item.get("id"))
        for item in states_data.get("states", [])
        if isinstance(item, dict) and item.get("id")
    }
    missing_states = REQUIRED_STATES - state_ids
    if missing_states:
        errors.append("Missing states: " + ", ".join(sorted(missing_states)))

    fields = set(str(item) for item in states_data.get("required_reviewer_fields", []))
    missing_fields = REQUIRED_FIELDS - fields
    if missing_fields:
        errors.append("Missing reviewer fields: " + ", ".join(sorted(missing_fields)))

    boundary_text = str(states_data.get("boundary", "")).lower()
    for phrase in ["not clinical advice", "not patient data", "not clinical deployment", "not clinical validation"]:
        if phrase not in boundary_text:
            errors.append(f"States boundary missing: {phrase}")

    if errors:
        print("FAIL clinician review protocol validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS clinician review protocol validation")
    print(f"protocol={PROTOCOL.relative_to(ROOT)}")
    print(f"states={STATES.relative_to(ROOT)}")
    print(f"states_count={len(state_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
