#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "tr_medllm_safetybench" / "synthetic_risk_pack_v0_1.jsonl"

REQUIRED_CASE_IDS = {f"TRFAI{index:03d}" for index in range(1, 15)}
REQUIRED_DOMAINS = {
    "cardiology",
    "endocrinology",
    "nephrology",
    "infectious diseases",
    "geriatrics",
    "pregnancy medication safety",
}
REQUIRED_RISK_AXES = {
    "false_reassurance",
    "medication_safety",
    "source_support",
    "missing_context",
    "rare_danger",
    "over_treatment",
    "communication_risk",
    "bias_or_premature_closure",
    "workflow_mismatch",
    "privacy_or_provenance",
}
FORBIDDEN_PHRASES = [
    "real patient",
    "clinical validation",
    "validated for clinical use",
    "safe for clinical use",
    "approved by",
    "official endorsement",
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
        print(f"FAIL missing pack: {PACK.relative_to(ROOT)}")
        return 1

    rows = load_rows()
    case_ids = {str(row.get("case_id", "")) for row in rows}
    domains = {str(row.get("clinical_domain", "")) for row in rows}
    risk_axes = {str(row.get("risk_axis", "")) for row in rows}
    sourcecheckup_count = sum(1 for row in rows if row.get("sourcecheckup_needed") is True)

    if len(rows) != 14:
        errors.append(f"Expected 14 Turkish synthetic risk rows, found {len(rows)}")
    missing_case_ids = REQUIRED_CASE_IDS - case_ids
    if missing_case_ids:
        errors.append(f"Missing required case IDs: {sorted(missing_case_ids)}")
    missing_domains = REQUIRED_DOMAINS - domains
    if missing_domains:
        errors.append(f"Missing specialty domains: {sorted(missing_domains)}")
    missing_risk_axes = REQUIRED_RISK_AXES - risk_axes
    if missing_risk_axes:
        errors.append(f"Missing risk axes: {sorted(missing_risk_axes)}")
    if sourcecheckup_count < 3:
        errors.append(f"Expected at least 3 SourceCheckup routed rows, found {sourcecheckup_count}")

    for index, row in enumerate(rows, start=1):
        if row.get("language") != "tr":
            errors.append(f"Row {index}: language must be tr")
        if row.get("synthetic_only") is not True:
            errors.append(f"Row {index}: synthetic_only must be true")
        if row.get("patient_data_used") is not False:
            errors.append(f"Row {index}: patient_data_used must be false")
        if row.get("clinical_use_allowed") is not False:
            errors.append(f"Row {index}: clinical_use_allowed must be false")
        if not str(row.get("turkish_prompt_seed", "")).strip():
            errors.append(f"Row {index}: turkish_prompt_seed is required")
        if not str(row.get("safe_answer_expectation", "")).strip():
            errors.append(f"Row {index}: safe_answer_expectation is required")
        row_text = " ".join(str(value).lower() for value in row.values())
        for phrase in FORBIDDEN_PHRASES:
            if phrase in row_text:
                errors.append(f"Row {index}: forbidden phrase {phrase!r}")

    if errors:
        print("FAIL TR MedLLM specialty spread validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TR MedLLM specialty spread validation")
    print(f"rows={len(rows)}")
    print(f"specialty_domains={len(REQUIRED_DOMAINS)}")
    print(f"risk_axes={len(risk_axes)}")
    print(f"sourcecheckup_rows={sourcecheckup_count}")
    print(f"file={PACK.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
