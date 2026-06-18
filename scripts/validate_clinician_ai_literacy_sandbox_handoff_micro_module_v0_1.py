#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "CLINICIAN_AI_LITERACY_SANDBOX_HANDOFF_MICRO_MODULE_V0_1.md"
DATA = ROOT / "docs" / "clinician_ai_literacy_sandbox_handoff_micro_module_v0_1.json"

REQUIRED_DOC_PHRASES = [
    "Clinician AI literacy sandbox handoff micro module v0.1",
    "public preview",
    "documentation for public review only",
    "Total minutes: 18",
    "Steps: 6",
    "CLSH001",
    "CLSH002",
    "CLSH003",
    "CLSH004",
    "CLSH005",
    "CLSH006",
    "No patient data.",
    "Synthetic only.",
    "Not for clinical use.",
    "No clinical validation claim.",
    "No clinical deployment claim.",
    "No endpoint result.",
    "No score report.",
    "No model ranking.",
    "No benchmark compatibility claim.",
    "No route access claim.",
    "No official role claim.",
    "No partner claim.",
    "No submission claim.",
    "No terms acceptance.",
    "No payment.",
    "No endorsement claim.",
    "make clinician_ai_literacy_sandbox_handoff_micro_module",
]

REQUIRED_JSON_FLAGS = {
    "contains_patient_data": False,
    "synthetic_only": True,
    "not_for_clinical_use": True,
    "no_clinical_validation_claim": True,
    "no_clinical_deployment_claim": True,
    "no_endpoint_result": True,
    "no_score_report": True,
    "no_model_ranking": True,
    "no_benchmark_compatibility_claim": True,
    "no_route_access_claim": True,
    "no_official_role_claim": True,
    "no_partner_claim": True,
    "no_submission_claim": True,
    "no_terms_acceptance": True,
    "no_payment": True,
    "no_endorsement_claim": True,
}

FORBIDDEN_PHRASES = [
    "sandbox access granted",
    "route access granted",
    "official role confirmed",
    "partner confirmed",
    "submitted application",
    "terms accepted",
    "payment completed",
    "clinically validated",
    "validated for clinical use",
    "clinical deployment ready",
    "endpoint result reported",
    "score report completed",
    "model ranking report",
    "benchmark compatible",
    "patient data used",
    "endorsed by",
]


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"Missing doc: {DOC.relative_to(ROOT)}")
    if not DATA.exists():
        errors.append(f"Missing data: {DATA.relative_to(ROOT)}")

    text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    lower_text = text.lower()
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Doc contains forbidden phrase: {phrase}")
    if "-" in text:
        errors.append("Doc contains hyphen character")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_JSON_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    steps = payload.get("steps", [])
    if payload.get("step_count") != 6 or len(steps) != 6:
        errors.append("Expected 6 micro module steps")
    if payload.get("total_minutes") != 18:
        errors.append("Expected total_minutes 18")
    required_ids = {f"CLSH{index:03d}" for index in range(1, 7)}
    found_ids = {step.get("step_id") for step in steps}
    missing_ids = sorted(required_ids - found_ids)
    if missing_ids:
        errors.append(f"Missing step ids: {', '.join(missing_ids)}")
    for step in steps:
        for field in ["title", "learner_task", "handoff_signal", "blocked_claim", "next_evidence"]:
            if not step.get(field):
                errors.append(f"{step.get('step_id')}: missing {field}")

    if errors:
        print("FAIL clinician AI literacy sandbox handoff micro module validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS clinician AI literacy sandbox handoff micro module validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"steps={len(steps)}")
    print(f"minutes={payload.get('total_minutes')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
