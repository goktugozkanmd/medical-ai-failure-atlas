#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_EXAMPLES_20260709.md"
JSON_PATH = ROOT / "docs" / "health_ai_assurance_feedback_triage_examples_20260709.json"
INTAKE_MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_FEEDBACK_INTAKE_20260708.md"
INTAKE_JSON_PATH = ROOT / "docs" / "health_ai_assurance_feedback_intake_20260708.json"
TRIAGE_MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_BOARD_20260708.md"
TRIAGE_JSON_PATH = ROOT / "docs" / "health_ai_assurance_feedback_triage_board_20260708.json"
README_PATH = ROOT / "README.md"

REQUIRED_FILES = [
    MD_PATH,
    JSON_PATH,
    INTAKE_MD_PATH,
    INTAKE_JSON_PATH,
    TRIAGE_MD_PATH,
    TRIAGE_JSON_PATH,
]

REQUIRED_MD_PHRASES = [
    "Health AI Assurance Feedback Triage Examples",
    "Status: public feedback triage examples ready.",
    "Roadmap phase: P11 feedback triage examples.",
    "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231",
    "docs/HEALTH_AI_ASSURANCE_FEEDBACK_INTAKE_20260708.md",
    "docs/health_ai_assurance_feedback_intake_20260708.json",
    "docs/HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_BOARD_20260708.md",
    "docs/health_ai_assurance_feedback_triage_board_20260708.json",
    "P11E001",
    "P11E002",
    "P11E003",
    "P11E004",
    "P11E005",
    "P11E006",
    "Documentation fix",
    "Source review queue",
    "Synthetic case queue",
    "Rewrite before acceptance",
    "Boundary close",
    "Owner review",
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

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "source proves",
    "best model",
    "patient data included",
    "official approval granted",
    "institution endorsed",
    "partner confirmed",
    "payment completed",
    "terms accepted",
]

REQUIRED_DECISIONS = {
    "documentation_fix",
    "source_review_queue",
    "synthetic_case_queue",
    "rewrite_before_acceptance",
    "boundary_close",
    "owner_review",
}

REQUIRED_IDS = {"P11E001", "P11E002", "P11E003", "P11E004", "P11E005", "P11E006"}

REQUIRED_STATES = {
    "accepted_for_docs",
    "accepted_for_queue",
    "needs_rewrite",
    "closed_boundary",
    "needs_owner_review",
}

REQUIRED_ROUTES = {
    "kit_feedback",
    "source_support_review",
    "synthetic_failure_case",
    "any",
}

REQUIRED_ALLOWED_OUTPUTS = {
    "documentation_fix": "documentation_fix",
    "source_review_queue": "source_review_queue_entry",
    "synthetic_case_queue": "synthetic_case_queue_entry",
    "rewrite_before_acceptance": "rewritten_issue_text",
    "boundary_close": "boundary_closure_note",
    "owner_review": "owner_review_note",
}

BOOLEAN_LOCKS = [
    ("contains_patient_data", False),
    ("contains_private_clinical_text", False),
    ("contains_raw_clinical_notes", False),
    ("contains_private_model_output", False),
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
    ("no_partnership_claim", True),
    ("no_payment_claim", True),
    ("no_terms_acceptance_claim", True),
]


def read_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    md_text = read_text(MD_PATH, errors)
    md_lower = md_text.lower()
    for phrase in REQUIRED_MD_PHRASES:
        if phrase.lower() not in md_lower:
            errors.append(f"{MD_PATH.relative_to(ROOT)} missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in md_lower:
            errors.append(f"{MD_PATH.relative_to(ROOT)} forbidden phrase present: {phrase}")

    try:
        manifest = json.loads(read_text(JSON_PATH, errors))
    except json.JSONDecodeError as exc:
        errors.append(f"{JSON_PATH.relative_to(ROOT)} invalid JSON: {exc}")
        manifest = {}

    if isinstance(manifest, dict):
        if manifest.get("artifact_id") != "health_ai_assurance_feedback_triage_examples_20260709":
            errors.append("Feedback triage examples artifact_id mismatch")
        if manifest.get("status") != "public_feedback_triage_examples_ready":
            errors.append("Feedback triage examples status must be public_feedback_triage_examples_ready")
        if manifest.get("phase") != "P11":
            errors.append("Feedback triage examples phase must be P11")
        if manifest.get("public_anchor") != "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231":
            errors.append("Feedback triage examples public anchor must point to issue 231")

        source_artifacts = manifest.get("source_artifacts", [])
        for artifact in [
            "docs/HEALTH_AI_ASSURANCE_FEEDBACK_INTAKE_20260708.md",
            "docs/health_ai_assurance_feedback_intake_20260708.json",
            "docs/HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_BOARD_20260708.md",
            "docs/health_ai_assurance_feedback_triage_board_20260708.json",
        ]:
            if artifact not in source_artifacts:
                errors.append(f"Feedback triage examples missing source artifact: {artifact}")
            if artifact not in md_text:
                errors.append(f"Feedback triage examples doc missing source artifact link: {artifact}")
            if not (ROOT / artifact).exists():
                errors.append(f"Feedback triage examples source artifact path missing: {artifact}")

        decisions = set(manifest.get("decision_types", []))
        if decisions != REQUIRED_DECISIONS:
            errors.append(f"Feedback triage examples decision types mismatch: {sorted(decisions)}")
        if manifest.get("decision_type_count") != 6:
            errors.append("Feedback triage examples must expose 6 decision types")

        records = manifest.get("example_records", [])
        if manifest.get("example_record_count") != 6:
            errors.append("Feedback triage examples must expose 6 example records")
        if not isinstance(records, list) or len(records) != 6:
            errors.append("Feedback triage examples records must be a 6 item list")
            records = []

        record_ids = {str(record.get("id")) for record in records if isinstance(record, dict)}
        if record_ids != REQUIRED_IDS:
            errors.append(f"Feedback triage examples ids mismatch: {sorted(record_ids)}")

        record_decisions = {str(record.get("decision")) for record in records if isinstance(record, dict)}
        if record_decisions != REQUIRED_DECISIONS:
            errors.append(f"Feedback triage examples record decisions mismatch: {sorted(record_decisions)}")

        record_states = {str(record.get("triage_state")) for record in records if isinstance(record, dict)}
        manifest_states = set(manifest.get("required_triage_states", []))
        if manifest_states != REQUIRED_STATES:
            errors.append(f"Feedback triage examples required_triage_states mismatch: {sorted(manifest_states)}")
        if not record_states <= REQUIRED_STATES:
            errors.append(f"Feedback triage examples unknown triage states: {sorted(record_states)}")
        if not REQUIRED_STATES <= record_states:
            errors.append(f"Feedback triage examples missing required states: {sorted(REQUIRED_STATES - record_states)}")

        record_routes = {str(record.get("incoming_route")) for record in records if isinstance(record, dict)}
        if not record_routes <= REQUIRED_ROUTES:
            errors.append(f"Feedback triage examples unknown routes: {sorted(record_routes)}")

        for record in records if isinstance(records, list) else []:
            if not isinstance(record, dict):
                errors.append(f"Feedback triage examples record is not an object: {record}")
                continue
            for key in [
                "id",
                "incoming_route",
                "example_feedback",
                "triage_state",
                "decision",
                "maintainer_action",
                "allowed_output",
                "blocked_claim_risk",
            ]:
                if key not in record:
                    errors.append(f"Feedback triage examples record missing {key}: {record}")
            if not isinstance(record.get("blocked_claim_risk"), bool):
                errors.append(f"Feedback triage examples blocked_claim_risk must be boolean: {record}")
            decision = record.get("decision")
            expected_allowed_output = REQUIRED_ALLOWED_OUTPUTS.get(str(decision))
            if expected_allowed_output and record.get("allowed_output") != expected_allowed_output:
                errors.append(
                    f"Feedback triage examples decision {decision} must use allowed_output {expected_allowed_output}"
                )

        for key, expected in BOOLEAN_LOCKS:
            if manifest.get(key) is not expected:
                errors.append(f"Feedback triage examples {key} must be {expected}")

    readme = read_text(README_PATH, errors)
    if "docs/HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_EXAMPLES_20260709.md" not in readme:
        errors.append("README missing Health AI Assurance feedback triage examples link")

    if errors:
        print("FAIL health AI assurance feedback triage examples validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS health AI assurance feedback triage examples validation")
    print(f"guide={MD_PATH.relative_to(ROOT)}")
    print(f"manifest={JSON_PATH.relative_to(ROOT)}")
    print("public_anchor=231")
    print(f"decisions={len(REQUIRED_DECISIONS)}")
    print(f"examples={manifest.get('example_record_count') if isinstance(manifest, dict) else 0}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
