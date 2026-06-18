#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SOURCECHECKUP_MEDICAL_BENCHMARK_BOUNDARY_DELTA_NOTE_V0_1.md"
DATA = ROOT / "docs" / "sourcecheckup_medical_benchmark_boundary_delta_note_v0_1.json"

REQUIRED_DOC_PHRASES = [
    "SourceCheckup Medical benchmark boundary delta note v0.1",
    "benchmark style review",
    "boundary delta note, not a benchmark report",
    "No patient data.",
    "Synthetic only.",
    "Not for clinical use.",
    "No endpoint result.",
    "No score report.",
    "No model ranking.",
    "No benchmark compatibility claim.",
    "No benchmark equivalence claim.",
    "No clinical validation claim.",
    "No clinical deployment claim.",
    "No official role claim.",
    "No route access claim.",
    "No submission claim.",
    "No partner claim.",
    "No terms acceptance.",
    "No payment.",
    "No endorsement claim.",
    "SCBBD001",
    "SCBBD002",
    "SCBBD003",
    "SCBBD004",
    "SCBBD005",
    "SCBBD006",
    "make sourcecheckup_medical_benchmark_boundary_delta",
]

REQUIRED_JSON_FLAGS = {
    "contains_patient_data": False,
    "synthetic_only": True,
    "not_for_clinical_use": True,
    "no_endpoint_result": True,
    "no_score_report": True,
    "no_model_ranking": True,
    "no_benchmark_compatibility_claim": True,
    "no_benchmark_equivalence_claim": True,
    "no_clinical_validation_claim": True,
    "no_clinical_deployment_claim": True,
    "no_official_role_claim": True,
    "no_route_access_claim": True,
    "no_submission_claim": True,
    "no_partner_claim": True,
    "no_terms_acceptance": True,
    "no_payment": True,
    "no_endorsement_claim": True,
}

FORBIDDEN_PHRASES = [
    "benchmark compatible",
    "benchmark equivalent",
    "endpoint result reported",
    "score report completed",
    "model ranking report",
    "clinically validated",
    "validated for clinical use",
    "clinical deployment ready",
    "patient data used",
    "official role confirmed",
    "route access granted",
    "partner confirmed",
    "submitted application",
    "payment completed",
    "terms accepted",
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
    deltas = payload.get("deltas", [])
    if payload.get("delta_count") != 6 or len(deltas) != 6:
        errors.append("Expected 6 benchmark boundary delta rows")
    required_ids = {f"SCBBD{index:03d}" for index in range(1, 7)}
    found_ids = {delta.get("delta_id") for delta in deltas}
    missing_ids = sorted(required_ids - found_ids)
    if missing_ids:
        errors.append(f"Missing delta ids: {', '.join(missing_ids)}")
    for delta in deltas:
        for field in ["source_surface", "boundary_delta", "public_use", "blocked_claim", "next_review_action"]:
            if not delta.get(field):
                errors.append(f"{delta.get('delta_id')}: missing {field}")

    if errors:
        print("FAIL SourceCheckup Medical benchmark boundary delta note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup Medical benchmark boundary delta note validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"deltas={len(deltas)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
