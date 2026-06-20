#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_REVIEWER_SPRINT_BOARD_20260620.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_reviewer_sprint_board_20260620.json"
ISSUE_BODY = ROOT / "outputs" / "medical_ai_safety_field_kit_reviewer_sprint_board_issue_body_20260620.md"
RELEASE_NOTES = ROOT / "outputs" / "medical_ai_safety_field_kit_reviewer_sprint_board_release_notes_20260620.md"

REQUIRED_FILES = [DOC, DATA, ISSUE_BODY, RELEASE_NOTES]

REQUIRED_PHRASES = [
    "Medical AI Safety Field Kit Reviewer Sprint Board",
    "public sprint board for one concrete reviewer objection",
    "Get one public objection that improves a safety boundary",
    "Reviewer start page",
    "Main public intake",
    "Source support starter",
    "Turkish wording starter",
    "Hospital readiness starter",
    "Lane:",
    "Risk:",
    "Missing gate:",
    "Safer wording:",
    "One visible third party comment is enough",
    "not maintaining this repository and is not posting through a project account",
    "controlled seed comments do not count as outside review or external validation",
    "Route each useful comment to one lane",
    "Use synthetic or public examples only",
    "make medical_ai_safety_field_kit_reviewer_sprint_board",
]

REQUIRED_URLS = [
    "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_REVIEWER_START_HERE_20260619.md",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/150",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/151",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/152",
]

FORBIDDEN = [
    "patient data used",
    "real patient",
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
    issue_text = ISSUE_BODY.read_text(encoding="utf-8") if ISSUE_BODY.exists() else ""
    release_text = RELEASE_NOTES.read_text(encoding="utf-8") if RELEASE_NOTES.exists() else ""

    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in doc_text.lower():
            errors.append(f"Doc missing required phrase: {phrase}")
    for url in REQUIRED_URLS:
        if url not in doc_text:
            errors.append(f"Doc missing required URL: {url}")
    for phrase in [
        "Done condition",
        "At least one visible third party account that is not maintaining this repository and is not posting through a project account",
        "Maintainer, project account, and controlled seed comments do not count.",
        "Boundary",
    ]:
        if phrase.lower() not in issue_text.lower():
            errors.append(f"Issue body missing required phrase: {phrase}")
    for phrase in ["This release adds a public sprint board", "Hospital readiness starter issue 152", "Boundary"]:
        if phrase.lower() not in release_text.lower():
            errors.append(f"Release notes missing required phrase: {phrase}")

    check_text("Doc", doc_text, errors)
    check_text("Issue body", issue_text, errors)
    check_text("Release notes", release_text, errors)

    if DATA.exists():
        payload = json.loads(DATA.read_text(encoding="utf-8"))
        if payload.get("artifact") != "medical_ai_safety_field_kit_reviewer_sprint_board":
            errors.append("Unexpected artifact id")
        if payload.get("primary_goal") != "get one true third party public objection that improves a safety boundary":
            errors.append("Unexpected primary goal")
        routes = payload.get("routes", [])
        if len(routes) != 5:
            errors.append("Expected five routes")
        route_urls = {route.get("url") for route in routes}
        for url in REQUIRED_URLS:
            if url not in route_urls:
                errors.append(f"JSON missing URL: {url}")
        for flag in REQUIRED_FALSE_FLAGS:
            if payload.get(flag) is not False:
                errors.append(f"Expected false flag: {flag}")

    if errors:
        print("FAIL reviewer sprint board validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer sprint board validation")
    print(f"doc={DOC.relative_to(ROOT)}")
    print(f"issue_body={ISSUE_BODY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
