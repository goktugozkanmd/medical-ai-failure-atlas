#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "docs" / "HEALTH_AI_ASSURANCE_FEEDBACK_INTAKE_20260708.md"
JSON_PATH = ROOT / "docs" / "health_ai_assurance_feedback_intake_20260708.json"
TEMPLATE_PATH = ROOT / ".github" / "ISSUE_TEMPLATE" / "health_ai_assurance_feedback.yml"

REQUIRED_FILES = [
    MD_PATH,
    JSON_PATH,
    TEMPLATE_PATH,
    ROOT / ".github" / "ISSUE_TEMPLATE" / "sourcecheckup_review.yml",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "synthetic_failure_case.yml",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "evidence_concern.yml",
    ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md",
    ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
    ROOT / "docs" / "HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
    ROOT / "docs" / "PROJECT_GROWTH_BUILDOUT_INDEX_20260708.md",
]

REQUIRED_MD_PHRASES = [
    "Health AI Assurance Feedback Intake",
    "Status: public feedback intake ready.",
    "Roadmap phase: P9 external feedback intake.",
    "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231",
    ".github/ISSUE_TEMPLATE/health_ai_assurance_feedback.yml",
    ".github/ISSUE_TEMPLATE/sourcecheckup_review.yml",
    ".github/ISSUE_TEMPLATE/synthetic_failure_case.yml",
    ".github/ISSUE_TEMPLATE/evidence_concern.yml",
    "Do Not Ask For",
    "Provider API runs",
    "Physician selection by the agent",
    "Clinical validation",
    "Model ranking",
    "Source truth certification",
    "Regulatory compliance",
    "Official compatibility",
    "Institution support",
]

REQUIRED_TEMPLATE_PHRASES = [
    "Health AI Assurance Kit feedback",
    "labels: [\"documentation\", \"assurance-lab\"]",
    "Use synthetic or public information only.",
    "artifact_reviewed",
    "feedback_type",
    "exact_location",
    "feedback_summary",
    "suggested_fix",
    "requested_route",
    "Move to SourceCheckup source review",
    "Move to synthetic failure case",
    "Move to evidence concern",
    "This includes no patient data, private clinical data, raw clinical note, or private model output.",
    "This does not ask the maintainer to select physicians.",
    "This does not claim clinical validation, model ranking, source truth certification, regulatory compliance, official compatibility, institution support, partnership, payment, or terms acceptance.",
]

REQUIRED_ROUTE_IDS = {
    "kit_feedback",
    "source_support_review",
    "synthetic_failure_case",
    "evidence_concern",
}

REQUIRED_TASK_IDS = {"P9T001", "P9T002", "P9T003", "P9T004", "P9T005"}

REQUIRED_TRIAGE_STATES = {
    "needs_route",
    "needs_rewrite",
    "accepted_for_docs",
    "accepted_for_queue",
    "closed_boundary",
}

REQUIRED_BLOCKED_CLAIMS = {
    "patient_data",
    "real_clinical_notes",
    "private_model_output",
    "provider_api_run",
    "new_case_without_review",
    "physician_selection_by_agent",
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
    template_text = require_phrases(TEMPLATE_PATH, REQUIRED_TEMPLATE_PHRASES, errors)

    try:
        manifest = json.loads(read_text(JSON_PATH, errors))
    except json.JSONDecodeError as exc:
        errors.append(f"{JSON_PATH.relative_to(ROOT)} invalid JSON: {exc}")
        manifest = {}

    if isinstance(manifest, dict):
        if manifest.get("artifact_id") != "health_ai_assurance_feedback_intake_20260708":
            errors.append("Feedback intake artifact_id mismatch")
        if manifest.get("status") != "public_feedback_intake_ready":
            errors.append("Feedback intake status must be public_feedback_intake_ready")
        if manifest.get("phase") != "P9":
            errors.append("Feedback intake phase must be P9")
        if manifest.get("public_anchor") != "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231":
            errors.append("Feedback intake public anchor must point to issue 231")
        if manifest.get("route_count") != 4:
            errors.append("Feedback intake must expose 4 routes")
        if manifest.get("small_task_count") != 5:
            errors.append("Feedback intake must expose 5 small tasks")

        routes = manifest.get("routes", [])
        route_ids = {str(route.get("id")) for route in routes if isinstance(route, dict)}
        if route_ids != REQUIRED_ROUTE_IDS:
            errors.append(f"Feedback intake route ids mismatch: {sorted(route_ids)}")

        for route in routes if isinstance(routes, list) else []:
            template = route.get("template") if isinstance(route, dict) else None
            if not isinstance(template, str) or not (ROOT / template).exists():
                errors.append(f"Feedback intake route template missing: {template}")
            elif template not in md_text and template not in template_text:
                errors.append(f"Feedback intake route template not visible in public text: {template}")

        tasks = manifest.get("small_tasks", [])
        task_ids = {str(task.get("id")) for task in tasks if isinstance(task, dict)}
        if task_ids != REQUIRED_TASK_IDS:
            errors.append(f"Feedback intake task ids mismatch: {sorted(task_ids)}")

        triage_states = {str(state) for state in manifest.get("triage_states", [])}
        if triage_states != REQUIRED_TRIAGE_STATES:
            errors.append(f"Feedback intake triage states mismatch: {sorted(triage_states)}")

        blocked_claims = {str(claim) for claim in manifest.get("blocked_claims", [])}
        missing_claims = REQUIRED_BLOCKED_CLAIMS - blocked_claims
        if missing_claims:
            errors.append(f"Feedback intake blocked claims missing: {sorted(missing_claims)}")

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
                errors.append(f"Feedback intake {key} must be {expected}")

    for phrase in [
        "patient data",
        "clinical validation",
        "model ranking",
        "source truth certification",
        "regulatory compliance",
        "official compatibility",
        "institution support",
        "physician selection",
    ]:
        if phrase not in md_text.lower() or phrase not in template_text.lower():
            errors.append(f"Boundary phrase must appear in both guide and template: {phrase}")

    if errors:
        print("FAIL health AI assurance feedback intake validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS health AI assurance feedback intake validation")
    print(f"guide={MD_PATH.relative_to(ROOT)}")
    print(f"manifest={JSON_PATH.relative_to(ROOT)}")
    print(f"template={TEMPLATE_PATH.relative_to(ROOT)}")
    print(f"routes={manifest.get('route_count')}")
    print(f"small_tasks={manifest.get('small_task_count')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
