#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "tr_medllm_safetybench" / "synthetic_risk_pack_v0_1.jsonl"
DASHBOARD = ROOT / "tr_medllm_safetybench" / "build" / "specialty_spread_dashboard_v0_1.md"

REQUIRED_PHRASES = [
    "TR MedLLM specialty spread dashboard v0.1",
    "Status: generated public preview.",
    "Turkish synthetic risk rows: 14",
    "Specialty spread rows: 6",
    "Specialty domains represented: 6",
    "Risk axes represented: 10",
    "Rows needing SourceCheckup review: 3",
    "SourceCheckup routed rows: 3",
    "SourceCheckup TR MedLLM assurance routing map",
    "docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md",
    "Clinician review needed rows: 14",
    "cardiology",
    "endocrinology",
    "nephrology",
    "infectious diseases",
    "geriatrics",
    "pregnancy medication safety",
    "TRFAI009",
    "TRFAI010",
    "TRFAI011",
    "TRFAI012",
    "TRFAI013",
    "TRFAI014",
    "T01: 2",
    "T02: 4",
    "T03: 3",
    "T04: 7",
    "T05: 3",
    "T06: 2",
    "T07: 3",
    "T08: 2",
    "T09: 3",
    "T10: 1",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not a benchmark compatibility claim",
    "not an official endorsement",
    "Specialty spread is a coverage view, not clinical validation.",
    "SourceCheckup routing is a review queue signal",
]

FORBIDDEN_PHRASES = [
    "real patient",
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "official approval",
    "sandbox access granted",
    "patient data used",
    "model is safe",
    "best model",
]


def load_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in PACK.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def main() -> int:
    errors: list[str] = []
    if not PACK.exists():
        errors.append(f"Missing pack: {PACK.relative_to(ROOT)}")
        rows: list[dict[str, object]] = []
    else:
        rows = load_rows()

    if not DASHBOARD.exists():
        errors.append(f"Missing dashboard: {DASHBOARD.relative_to(ROOT)}")
        text = ""
    else:
        text = DASHBOARD.read_text(encoding="utf-8")

    specialty_domains = {
        "cardiology",
        "endocrinology",
        "nephrology",
        "infectious diseases",
        "geriatrics",
        "pregnancy medication safety",
    }
    specialty_rows = [row for row in rows if str(row.get("clinical_domain")) in specialty_domains]
    risk_axes = {str(row.get("risk_axis")) for row in rows}
    sourcecheckup_rows = [row for row in rows if row.get("sourcecheckup_needed") is True]
    clinician_rows = [row for row in rows if row.get("clinician_review_needed") is True]

    if len(rows) != 14:
        errors.append(f"Expected 14 Turkish rows, found {len(rows)}")
    if len(specialty_rows) != 6:
        errors.append(f"Expected 6 specialty rows, found {len(specialty_rows)}")
    if len(risk_axes) != 10:
        errors.append(f"Expected 10 risk axes, found {len(risk_axes)}")
    if len(sourcecheckup_rows) != 3:
        errors.append(f"Expected 3 SourceCheckup rows, found {len(sourcecheckup_rows)}")
    if len(clinician_rows) != 14:
        errors.append(f"Expected 14 clinician review rows, found {len(clinician_rows)}")

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Dashboard missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")

    for row in specialty_rows:
        case_id = str(row["case_id"])
        if case_id not in text:
            errors.append(f"Dashboard missing specialty case ID: {case_id}")
        if str(row["turkish_prompt_seed"]) not in text:
            errors.append(f"Dashboard missing prompt seed for: {case_id}")

    if errors:
        print("FAIL TR MedLLM specialty dashboard validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TR MedLLM specialty dashboard validation")
    print(f"dashboard={DASHBOARD.relative_to(ROOT)}")
    print(f"rows={len(rows)}")
    print(f"specialty_rows={len(specialty_rows)}")
    print(f"risk_axes={len(risk_axes)}")
    print(f"sourcecheckup_rows={len(sourcecheckup_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
