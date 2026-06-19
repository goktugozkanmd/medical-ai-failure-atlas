#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_EXTERNAL_ROUTE_SCOUT_BOARD_20260620.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_external_route_scout_board_20260620.json"
ISSUE_COMMENT = ROOT / "outputs" / "medical_ai_safety_field_kit_external_route_scout_issue153_comment_20260620.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_external_route_scout_public_action_audit_20260620.md"

REQUIRED_FILES = [DOC, DATA, ISSUE_COMMENT, AUDIT]

REQUIRED_PHRASES = [
    "Medical AI Safety Field Kit External Route Scout Board",
    "public scout board for choosing where not to post yet",
    "Post outside this repository only when all conditions are true",
    "Current route checks",
    "Best next outside route",
    "Contributor ladder for issue 153",
    "One outside comment is cleared after audit",
    "Public action cleared now",
    "comment on issue 153",
]

REQUIRED_URLS = [
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/153",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_GLOBAL_SAFETY_CLAIM_REVIEW_WORKBOOK_20260620.md",
    "https://github.com/The-AI-Alliance/trust-safety-evals/issues/50",
    "https://github.com/openai/simple-evals/issues/83",
    "https://github.com/openai/simple-evals/issues/109",
    "https://github.com/stanford-crfm/helm/issues/4187",
    "https://github.com/mlcommons/endpoints/issues/178",
    "https://github.com/YLab-Open/BRIDGE/issues/4",
]

FORBIDDEN = [
    "patient data used",
    "real patient",
    "clinically validated",
    "clinical deployment ready",
    "safe for clinical use",
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

FALSE_FLAGS = [
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
    comment_text = ISSUE_COMMENT.read_text(encoding="utf-8") if ISSUE_COMMENT.exists() else ""
    audit_text = AUDIT.read_text(encoding="utf-8") if AUDIT.exists() else ""

    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in doc_text.lower():
            errors.append(f"Doc missing required phrase: {phrase}")
    for url in REQUIRED_URLS:
        if url not in doc_text:
            errors.append(f"Doc missing URL: {url}")
        if url not in audit_text:
            errors.append(f"Audit missing URL: {url}")

    for phrase in ["One outside comment is cleared after audit", "Best watch candidate", "Boundary"]:
        if phrase.lower() not in comment_text.lower():
            errors.append(f"Issue comment missing phrase: {phrase}")

    check_text("Doc", doc_text, errors)
    check_text("Issue comment", comment_text, errors)
    check_text("Audit", audit_text, errors)

    if DATA.exists():
        payload = json.loads(DATA.read_text(encoding="utf-8"))
        if payload.get("artifact") != "medical_ai_safety_field_kit_external_route_scout_board":
            errors.append("Unexpected artifact id")
        if payload.get("primary_issue") != 153:
            errors.append("Primary issue must be 153")
        routes = payload.get("routes_checked", [])
        if len(routes) != 6:
            errors.append("Expected six routes checked")
        route_urls = {route.get("url") for route in routes}
        for url in REQUIRED_URLS[2:]:
            if url not in route_urls:
                errors.append(f"JSON missing route URL: {url}")
        decisions = {route.get("decision") for route in routes}
        if not {"post", "hold", "watch"}.issubset(decisions):
            errors.append("Expected post hold and watch decisions")
        if payload.get("outside_comment_cleared") is not True:
            errors.append("Expected outside comment cleared true")
        if payload.get("cleared_outside_route") != "https://github.com/The-AI-Alliance/trust-safety-evals/issues/50":
            errors.append("Unexpected cleared outside route")
        if payload.get("contributor_ladder") != [
            "route scout",
            "risk mapper",
            "comment drafter",
            "maintainer closeout",
        ]:
            errors.append("Unexpected contributor ladder")
        for flag in FALSE_FLAGS:
            if payload.get(flag) is not False:
                errors.append(f"Expected false flag: {flag}")

    if errors:
        print("FAIL external route scout board validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS external route scout board validation")
    print(f"doc={DOC.relative_to(ROOT)}")
    print(f"issue_comment={ISSUE_COMMENT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
