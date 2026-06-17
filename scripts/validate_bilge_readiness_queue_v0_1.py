#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "tr-medai-safety-suite"
JSON_PATH = OUT_DIR / "bilge_readiness_queue_v0_1.json"
MD_PATH = OUT_DIR / "BILGE_READINESS_QUEUE_V0_1.md"


REQUIRED_PHRASES = [
    "BİLGE readiness queue v0.1",
    "Official source:",
    "https://bilge.tubitak.gov.tr/",
    "Turkish large language model family",
    "TÜBİTAK BİLGEM",
    "1B",
    "9B",
    "27B",
    "122B",
    "health",
    "Queue rows: 5",
    "Official source rows: 1",
    "No access gate rows: 1",
    "Turkish clinical risk mapping rows: 1",
    "SourceCheckup Turkish institutional wording rows: 1",
    "Collaboration readiness bridge rows: 1",
    "no model access claim",
    "no model score claim",
    "no model safety claim",
    "no model ranking",
    "no benchmark compatibility claim",
    "not clinical deployment",
    "not clinical validation",
    "not official endorsement",
    "not sandbox access",
    "make bilge_readiness_queue",
]

FORBIDDEN_PHRASES = [
    "model access granted",
    "tested BİLGE",
    "BİLGE score",
    "clinically validated",
    "validated for clinical use",
    "officially endorsed",
    "sandbox access granted",
    "benchmark compatible",
    "best model",
    "patient data used",
    "model is safe",
]

REQUIRED_FLAGS = [
    "no_model_access_claim",
    "no_model_score_claim",
    "no_model_safety_claim",
    "no_model_ranking",
    "no_clinical_validation_claim",
    "no_clinical_deployment_claim",
    "no_official_endorsement_claim",
    "no_sandbox_access_claim",
    "no_benchmark_compatibility_claim",
]


def main() -> int:
    errors: list[str] = []
    if not JSON_PATH.exists():
        errors.append(f"Missing JSON: {JSON_PATH.relative_to(ROOT)}")
        payload = {}
    else:
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if not MD_PATH.exists():
        errors.append(f"Missing Markdown: {MD_PATH.relative_to(ROOT)}")
        text = ""
    else:
        text = MD_PATH.read_text(encoding="utf-8")

    if payload.get("official_source_url") != "https://bilge.tubitak.gov.tr/":
        errors.append("official source URL must match the BİLGE page")
    if payload.get("queue_row_count") != 5:
        errors.append("queue row count must be 5")
    if payload.get("official_source_rows") != 1:
        errors.append("official source row count must be 1")
    if payload.get("contains_patient_data") is not False:
        errors.append("contains_patient_data must be false")
    if payload.get("not_for_clinical_use") is not True:
        errors.append("not_for_clinical_use must be true")
    for flag in REQUIRED_FLAGS:
        if payload.get(flag) is not True:
            errors.append(f"{flag} must be true")

    boundaries = payload.get("official_source_boundaries", {})
    if boundaries.get("developer") != "TÜBİTAK BİLGEM":
        errors.append("developer must be TÜBİTAK BİLGEM")
    if set(boundaries.get("model_sizes", [])) != {"1B", "9B", "27B", "122B"}:
        errors.append("model sizes must be 1B 9B 27B 122B")
    if boundaries.get("health_domain_mentioned") is not True:
        errors.append("health domain mentioned must be true")

    row_ids = [row.get("queue_id") for row in payload.get("rows", [])]
    if row_ids != ["BILGEQ001", "BILGEQ002", "BILGEQ003", "BILGEQ004", "BILGEQ005"]:
        errors.append("queue IDs must be BILGEQ001 through BILGEQ005")

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing BİLGE readiness queue must not contain hyphen characters")

    if errors:
        print("FAIL BİLGE readiness queue validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS BİLGE readiness queue validation")
    print(f"file={MD_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
