#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "sourcecheckup_tr_medllm_assurance_routing_map_v0_1.json"
MAP = ROOT / "docs" / "SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md"

REQUIRED_SOURCECHECKUP_ROWS = {f"SCQ_{index:03d}" for index in range(1, 13)}
REQUIRED_TR_CASES = {f"TRFAI{index:03d}" for index in range(1, 15)}
REQUIRED_ASSURANCE_EXAMPLES = {f"ARG{index:03d}" for index in range(1, 7)}
REQUIRED_SOURCE_SURFACES = {
    "guideline",
    "doi",
    "pmid",
    "url",
    "policy",
    "broad_source_language",
    "evidence",
    "none",
}
REQUIRED_RISK_AXES = {
    "medication_safety",
    "source_support",
    "false_reassurance",
    "privacy_or_provenance",
    "communication_risk",
    "over_treatment",
    "bias_or_premature_closure",
    "workflow_mismatch",
    "rare_danger",
    "missing_context",
}
REQUIRED_GATE_LEVELS = {"L0", "L1", "L2", "L3", "L4", "L5"}
REQUIRED_DECISIONS = {
    "needs_source_review",
    "needs_clinician_source_review",
    "needs_clinician_review",
    "blocked_official_or_deployment_claim",
    "public_candidate_boundary_ready",
    "blocked_data_provenance_claim",
    "synthetic_positive_control_only",
}

REQUIRED_PHRASES = [
    "SourceCheckup TR MedLLM assurance routing map v0.1",
    "Status: generated public preview.",
    "Routes: 7",
    "SourceCheckup queue rows covered: 12",
    "TR MedLLM cases covered: 14",
    "Assurance release gate examples covered: 6",
    "Source surfaces represented: 8",
    "Risk axes represented: 10",
    "Release gate levels represented: 6",
    "Routing decisions represented: 7",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not source truth certification",
    "not regulatory approval",
    "not an official endorsement",
    "Policy, sandbox, pilot, official route, and deployment language remains blocked",
    "SourceCheckup routing is a review path",
    "make sourcecheckup_tr_medllm_routing",
    "Source review worksheets",
    "docs/SOURCE_REVIEW_WORKSHEETS_V0_1.md",
    "Red flag source locator and warning sign checklist",
    "docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "officially endorsed",
    "regulatory approved",
    "sandbox access granted",
    "patient data used",
    "source proves",
    "model is safe",
    "best model",
]


def flatten(routes: list[dict[str, Any]], key: str) -> set[str]:
    values: set[str] = set()
    for route in routes:
        values.update(str(value) for value in route.get(key, []))
    return values


def main() -> int:
    errors: list[str] = []
    if not SOURCE.exists():
        errors.append(f"Missing source JSON: {SOURCE.relative_to(ROOT)}")
        data: dict[str, Any] = {"routes": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    routes = data.get("routes", [])
    if not isinstance(routes, list):
        errors.append("routes must be a list")
        routes = []
    if data.get("route_count") != 7:
        errors.append("route_count must be 7")
    if len(routes) != 7:
        errors.append(f"Expected 7 routes, found {len(routes)}")

    for field in [
        "contains_patient_data",
        "synthetic_examples_only",
        "not_for_clinical_use",
        "no_clinical_deployment_claim",
        "no_clinical_validation_claim",
        "no_model_safety_claim",
        "no_model_ranking",
        "no_source_truth_certification",
        "no_official_endorsement_claim",
    ]:
        expected = False if field == "contains_patient_data" else True
        if data.get(field) is not expected:
            errors.append(f"{field} must be {expected}")

    seen_ids: set[str] = set()
    for index, route in enumerate(routes, start=1):
        route_id = str(route.get("route_id", ""))
        if not route_id.startswith("STM"):
            errors.append(f"Route {index}: route_id must start with STM")
        if route_id in seen_ids:
            errors.append(f"Duplicate route_id: {route_id}")
        seen_ids.add(route_id)
        for key in [
            "title",
            "sourcecheckup_queue_ids",
            "tr_medllm_case_ids",
            "assurance_example_ids",
            "source_surfaces",
            "risk_axes",
            "release_gate_levels",
            "routing_decision",
            "claim_hazard",
            "public_use_boundary",
            "track_a_value",
            "track_b_value",
            "next_public_action",
        ]:
            if key not in route:
                errors.append(f"{route_id}: missing {key}")
        allowed_boundary = str(route.get("public_use_boundary", "")).lower()
        for blocked_phrase in ["clinically validated", "safe for clinical use", "deployment ready"]:
            if blocked_phrase in allowed_boundary:
                errors.append(f"{route_id}: public_use_boundary contains unsafe phrase")

    checks = [
        ("SourceCheckup rows", REQUIRED_SOURCECHECKUP_ROWS, flatten(routes, "sourcecheckup_queue_ids")),
        ("TR MedLLM cases", REQUIRED_TR_CASES, flatten(routes, "tr_medllm_case_ids")),
        ("Assurance examples", REQUIRED_ASSURANCE_EXAMPLES, flatten(routes, "assurance_example_ids")),
        ("Source surfaces", REQUIRED_SOURCE_SURFACES, flatten(routes, "source_surfaces")),
        ("Risk axes", REQUIRED_RISK_AXES, flatten(routes, "risk_axes")),
        ("Release gate levels", REQUIRED_GATE_LEVELS, flatten(routes, "release_gate_levels")),
        ("Routing decisions", REQUIRED_DECISIONS, {str(route.get("routing_decision", "")) for route in routes}),
    ]
    for label, required, found in checks:
        missing = sorted(required - found)
        if missing:
            errors.append(f"Missing {label}: {', '.join(missing)}")

    if not MAP.exists():
        errors.append(f"Missing generated map: {MAP.relative_to(ROOT)}")
        text = ""
    else:
        text = MAP.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Map missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing map must not contain hyphen characters")

    if errors:
        print("FAIL SourceCheckup TR MedLLM routing map validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup TR MedLLM routing map validation")
    print(f"map={MAP.relative_to(ROOT)}")
    print(f"routes={len(routes)}")
    print(f"sourcecheckup_rows={len(flatten(routes, 'sourcecheckup_queue_ids'))}")
    print(f"tr_cases={len(flatten(routes, 'tr_medllm_case_ids'))}")
    print(f"assurance_examples={len(flatten(routes, 'assurance_example_ids'))}")
    print(f"source_surfaces={len(flatten(routes, 'source_surfaces'))}")
    print(f"risk_axes={len(flatten(routes, 'risk_axes'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
