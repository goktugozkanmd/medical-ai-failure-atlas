#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "docs" / "sourcecheckup" / "SOURCECHECKUP_REPO_RUN_GUIDE_V0_1.md"
RUN_JSON = ROOT / "docs" / "sourcecheckup" / "sourcecheckup_repo_run_guide_v0_1.json"
DOCTOR_JSON = ROOT / "docs" / "sourcecheckup" / "sourcecheckup_repo_doctor_v0_1.json"

REQUIRED_COMMANDS = {
    "make sourcecheckup",
    "make sourcecheckup_v02",
    "make source_claim_queue",
    "make sourcecheckup_expansion_dashboard",
    "make sourcecheckup_turkish_institutional_wording",
    "make sourcecheckup_repo_run_guide",
}

REQUIRED_PHRASES = [
    "SourceCheckup repo run guide v0.1",
    "Status: generated public preview.",
    "Run guide rows: 6",
    "Doctor output: `docs/sourcecheckup/sourcecheckup_repo_doctor_v0_1.json`",
    "Runnable target: `make sourcecheckup_repo_run_guide`",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not source truth certification",
    "not a model safety claim",
    "not a model ranking",
    "not a benchmark compatibility claim",
    "not an official endorsement",
    "External calls are not required",
    "Model calls are not required",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "officially endorsed",
    "benchmark compatible",
    "patient data used",
    "source proves",
    "model is safe",
]


def main() -> int:
    errors: list[str] = []
    if not MARKDOWN.exists():
        errors.append(f"Missing Markdown: {MARKDOWN.relative_to(ROOT)}")
        text = ""
    else:
        text = MARKDOWN.read_text(encoding="utf-8")
    if not RUN_JSON.exists():
        errors.append(f"Missing run JSON: {RUN_JSON.relative_to(ROOT)}")
        run_payload = {}
    else:
        run_payload = json.loads(RUN_JSON.read_text(encoding="utf-8"))
    if not DOCTOR_JSON.exists():
        errors.append(f"Missing doctor JSON: {DOCTOR_JSON.relative_to(ROOT)}")
        doctor_payload = {}
    else:
        doctor_payload = json.loads(DOCTOR_JSON.read_text(encoding="utf-8"))

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing run guide must not contain hyphen characters")

    rows = run_payload.get("rows", [])
    if run_payload.get("row_count") != 6 or len(rows) != 6:
        errors.append("Run guide JSON must contain exactly 6 rows")
    commands = {str(row.get("command")) for row in rows}
    missing_commands = sorted(REQUIRED_COMMANDS - commands)
    if missing_commands:
        errors.append(f"Missing commands: {', '.join(missing_commands)}")
    for key in ["contains_patient_data", "not_for_clinical_use", "no_external_calls", "no_model_calls", "no_source_truth_certification"]:
        expected = False if key == "contains_patient_data" else True
        if run_payload.get(key) is not expected:
            errors.append(f"{key} must be {expected}")

    if doctor_payload.get("status") != "pass":
        errors.append("Doctor status must be pass")
    if doctor_payload.get("required_file_count") != 10:
        errors.append("Doctor must check 10 required files")
    if doctor_payload.get("jsonl_count_checks") != 4:
        errors.append("Doctor must check 4 JSONL row counts")
    if doctor_payload.get("errors"):
        errors.append("Doctor errors must be empty")

    if errors:
        print("FAIL SourceCheckup repo run guide validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup repo run guide validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"run_json={RUN_JSON.relative_to(ROOT)}")
    print(f"doctor_json={DOCTOR_JSON.relative_to(ROOT)}")
    print(f"rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
