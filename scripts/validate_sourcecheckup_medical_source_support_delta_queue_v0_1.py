#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SOURCECHECKUP_MEDICAL_SOURCE_SUPPORT_DELTA_QUEUE_V0_1.md"
DATA = ROOT / "docs" / "sourcecheckup_medical_source_support_delta_queue_v0_1.json"

REQUIRED_DOC_PHRASES = [
    "SourceCheckup Medical source support delta queue v0.1",
    "public preview",
    "Rows: 6",
    "SCSSDQ001",
    "SCSSDQ002",
    "SCSSDQ003",
    "SCSSDQ004",
    "SCSSDQ005",
    "SCSSDQ006",
    "No patient data.",
    "Synthetic only.",
    "Not for clinical use.",
    "No source truth certification.",
    "No clinical validation claim.",
    "No clinical deployment claim.",
    "No endpoint result.",
    "No score report.",
    "No model ranking.",
    "No benchmark compatibility claim.",
    "No benchmark equivalence claim.",
    "No route access claim.",
    "No official role claim.",
    "No partner claim.",
    "No submission claim.",
    "No terms acceptance.",
    "No payment.",
    "No endorsement claim.",
    "make sourcecheckup_medical_source_support_delta_queue",
]

REQUIRED_JSON_FLAGS = {
    "contains_patient_data": False,
    "synthetic_only": True,
    "not_for_clinical_use": True,
    "no_source_truth_certification": True,
    "no_clinical_validation_claim": True,
    "no_clinical_deployment_claim": True,
    "no_endpoint_result": True,
    "no_score_report": True,
    "no_model_ranking": True,
    "no_benchmark_compatibility_claim": True,
    "no_benchmark_equivalence_claim": True,
    "no_route_access_claim": True,
    "no_official_role_claim": True,
    "no_partner_claim": True,
    "no_submission_claim": True,
    "no_terms_acceptance": True,
    "no_payment": True,
    "no_endorsement_claim": True,
}

FORBIDDEN_PHRASES = [
    "source truth certified",
    "clinically validated",
    "validated for clinical use",
    "clinical deployment ready",
    "endpoint result reported",
    "score report completed",
    "model ranking report",
    "benchmark compatible",
    "benchmark equivalent",
    "route access granted",
    "official role confirmed",
    "partner confirmed",
    "submitted application",
    "terms accepted",
    "payment completed",
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
    rows = payload.get("rows", [])
    if payload.get("row_count") != 6 or len(rows) != 6:
        errors.append("Expected 6 source support delta rows")
    required_ids = {f"SCSSDQ{index:03d}" for index in range(1, 7)}
    found_ids = {row.get("row_id") for row in rows}
    missing_ids = sorted(required_ids - found_ids)
    if missing_ids:
        errors.append(f"Missing row ids: {', '.join(missing_ids)}")
    for row in rows:
        for field in ["claim_surface", "delta_question", "minimum_review", "blocked_claim", "next_action"]:
            if not row.get(field):
                errors.append(f"{row.get('row_id')}: missing {field}")

    if errors:
        print("FAIL SourceCheckup Medical source support delta queue validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup Medical source support delta queue validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
