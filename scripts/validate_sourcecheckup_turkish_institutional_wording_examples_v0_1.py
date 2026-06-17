#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "docs" / "sourcecheckup" / "SOURCECHECKUP_TURKISH_INSTITUTIONAL_WORDING_EXAMPLES_V0_1.md"
JSON_PATH = ROOT / "docs" / "sourcecheckup" / "sourcecheckup_turkish_institutional_wording_examples_v0_1.json"

REQUIRED_ROW_IDS = {"STIWE001", "STIWE002", "STIWE003", "STIWE004", "STIWE005"}
REQUIRED_BLOCKED_CLAIMS = {
    "official endorsement",
    "route access",
    "submission claim",
    "clinical deployment",
    "validation claim",
}
REQUIRED_PHRASES = [
    "SourceCheckup Turkish institutional wording examples v0.1",
    "Status: generated public preview.",
    "Turkish institutional wording examples: 5",
    "Blocked claim types: 5",
    "Reviewer lanes: 5",
    "Linked SourceCheckup route: `SCQ_008`",
    "Linked assurance route: `ARG006`",
    "TUBITAK_1711_COLLABORATION_READINESS_PACKET_V0_1.md",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not regulatory approval",
    "not route access",
    "not a submission claim",
    "not an official endorsement",
    "No institutional endorsement is claimed",
    "No route access is claimed",
    "No submission is claimed",
    "No clinical deployment is claimed",
    "No clinical validation is claimed",
    "make sourcecheckup_turkish_institutional_wording",
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
    "partner secured",
    "application submitted",
    "funding awarded",
    "route access granted",
]


def main() -> int:
    errors: list[str] = []
    if not MARKDOWN.exists():
        errors.append(f"Missing Markdown file: {MARKDOWN.relative_to(ROOT)}")
        text = ""
    else:
        text = MARKDOWN.read_text(encoding="utf-8")
    if not JSON_PATH.exists():
        errors.append(f"Missing JSON file: {JSON_PATH.relative_to(ROOT)}")
        payload = {}
    else:
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing examples must not contain hyphen characters")

    rows = payload.get("rows", [])
    if payload.get("row_count") != 5 or len(rows) != 5:
        errors.append("JSON must contain exactly 5 rows")
    if payload.get("contains_patient_data") is not False:
        errors.append("contains_patient_data must be false")
    if payload.get("not_for_clinical_use") is not True:
        errors.append("not_for_clinical_use must be true")
    for key in [
        "no_official_endorsement_claim",
        "no_route_access_claim",
        "no_submission_claim",
        "no_clinical_deployment_claim",
        "no_clinical_validation_claim",
    ]:
        if payload.get(key) is not True:
            errors.append(f"{key} must be true")

    row_ids = {str(row.get("row_id")) for row in rows}
    missing_ids = sorted(REQUIRED_ROW_IDS - row_ids)
    if missing_ids:
        errors.append(f"Missing row ids: {', '.join(missing_ids)}")
    blocked_claims = {str(row.get("blocked_claim")) for row in rows}
    missing_claims = sorted(REQUIRED_BLOCKED_CLAIMS - blocked_claims)
    if missing_claims:
        errors.append(f"Missing blocked claim types: {', '.join(missing_claims)}")
    for row in rows:
        row_id = str(row.get("row_id"))
        for field in [
            "institutional_surface",
            "synthetic_risky_wording",
            "blocked_claim",
            "safe_public_wording",
            "sourcecheckup_action",
            "review_lane",
        ]:
            if not str(row.get(field, "")).strip():
                errors.append(f"{row_id}: missing {field}")
        safe_wording = str(row.get("safe_public_wording", "")).lower()
        if "endorsement" in safe_wording and "does not claim" not in safe_wording:
            errors.append(f"{row_id}: endorsement wording must be negated")
        if "validation" in safe_wording and "does not claim" not in safe_wording:
            errors.append(f"{row_id}: validation wording must be negated")

    if errors:
        print("FAIL SourceCheckup Turkish institutional wording validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup Turkish institutional wording validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"json={JSON_PATH.relative_to(ROOT)}")
    print(f"rows={len(rows)}")
    print(f"blocked_claim_types={len(blocked_claims)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
