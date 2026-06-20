#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_ONE_OBJECTION_GATEWAY_20260620.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_one_objection_gateway_20260620.json"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_one_objection_gateway_public_action_audit_20260620.md"
SOURCE_SUPPORT = ROOT / "outputs" / "medical_ai_safety_field_kit_one_objection_gateway_manual_source_support_20260620.md"
LAUNCH = ROOT / "outputs" / "medical_ai_safety_field_kit_one_objection_gateway_manual_launch_seed_20260620.md"

REQUIRED_FILES = [DOC, DATA, AUDIT, SOURCE_SUPPORT, LAUNCH]

REQUIRED_DOC_PHRASES = [
    "Medical AI Safety Field Kit One Objection Gateway",
    "The whole ask is one objection.",
    "Pick one role. Pick one lane. Leave one bounded objection",
    "Every lane lands in the same issue first:",
    "Name the lane in your comment.",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/154",
    "Count only outside comments as outside review.",
    "make medical_ai_safety_field_kit_one_objection_gateway",
]

FORBIDDEN = [
    "patient data used",
    "real patient evidence confirmed",
    "clinically validated",
    "clinical deployment ready",
    "safe for clinical use",
    "diagnosis advice provided",
    "treatment advice provided",
    "benchmark ranking confirmed",
    "score certified",
    "source truth certified",
    "partner confirmed",
    "institution approved",
    "endorsed by",
    "formal application submitted",
    "payment completed",
    "terms accepted",
    "TBYS submitted",
    "PRODIS submitted",
    "official guidance",
    "compliance certified",
    "de" + "AI",
    "human" + "ized",
    "AI " + "detector",
    "submit" + "_audit",
]

REQUIRED_FALSE_FLAGS = [
    "contains_patient_data",
    "claims_clinical_validation",
    "claims_clinical_deployment",
    "claims_benchmark_ranking",
    "claims_score_certification",
    "claims_source_truth_certification",
    "claims_partner",
    "claims_institutional_approval",
    "claims_endorsement",
    "claims_formal_application",
    "claims_payment",
    "claims_terms_acceptance",
    "requires_tbys_action",
    "requires_prodis_action",
]


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def check_text(label: str, text: str, errors: list[str]) -> None:
    lower_text = text.lower()
    for phrase in FORBIDDEN:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append(f"{label} contains non URL hyphen character")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing file: {path.relative_to(ROOT)}")

    doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    audit_text = AUDIT.read_text(encoding="utf-8") if AUDIT.exists() else ""
    support_text = SOURCE_SUPPORT.read_text(encoding="utf-8") if SOURCE_SUPPORT.exists() else ""
    launch_text = LAUNCH.read_text(encoding="utf-8") if LAUNCH.exists() else ""

    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in doc_text.lower():
            errors.append(f"Doc missing required phrase: {phrase}")
    if "Allowed action: public GitHub commit after validation." not in audit_text:
        errors.append("Audit missing allowed action boundary")
    if "navigation claims only" not in support_text:
        errors.append("Source support missing navigation claim boundary")
    if "manual post seed only" not in launch_text.lower():
        errors.append("Launch seed missing manual only boundary")

    check_text("Doc", doc_text, errors)
    check_text("Audit", audit_text, errors)
    check_text("Source support", support_text, errors)
    check_text("Launch", launch_text, errors)

    if DATA.exists():
        payload = json.loads(DATA.read_text(encoding="utf-8"))
        if payload.get("artifact") != "medical_ai_safety_field_kit_one_objection_gateway":
            errors.append("Unexpected artifact id")
        if payload.get("primary_goal") != "convert outside readers into one bounded public objection":
            errors.append("Unexpected primary goal")
        if payload.get("primary_issue") != 154:
            errors.append("Expected primary issue 154")
        if len(payload.get("routes", [])) != 6:
            errors.append("Expected six reviewer routes")
        for index, route in enumerate(payload.get("routes", []), start=1):
            if route.get("target") != "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/154":
                errors.append(f"Route {index} does not land on issue 154")
        for flag in REQUIRED_FALSE_FLAGS:
            if payload.get(flag) is not False:
                errors.append(f"Expected false flag: {flag}")

    if errors:
        print("FAIL One Objection Gateway validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS One Objection Gateway validation")
    print(f"doc={DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
