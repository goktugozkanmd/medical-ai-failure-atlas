#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_GLOBAL_SAFETY_CLAIM_REVIEW_WORKBOOK_20260620.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_global_safety_claim_review_workbook_20260620.json"
ISSUE_COMMENT = ROOT / "outputs" / "medical_ai_safety_field_kit_global_workbook_issue149_comment_20260620.md"
RELEASE_NOTES = ROOT / "outputs" / "medical_ai_safety_field_kit_global_workbook_release_notes_20260620.md"

REQUIRED_FILES = [DOC, DATA, ISSUE_COMMENT, RELEASE_NOTES]

REQUIRED_DOC_PHRASES = [
    "Medical AI Safety Field Kit Global Safety Claim Review Workbook",
    "public workbook for bounded safety claim review",
    "make weak safety language easier to attack before it becomes trusted public language",
    "Boundary page",
    "Public route map",
    "Claim review matrix",
    "Safe Failure Card mapping",
    "Synthetic walkthrough",
    "Reviewer comment templates",
    "Objection counting rule",
    "Only visible third party comments count",
    "A comment counts only when it comes from a person who is not maintaining this repository and is not posting through a project account.",
    "Maintainer, project account, and controlled seed comments do not count as outside review or external validation.",
    "Do not invent reviewer rows",
    "Maintainer closeout rule",
    "make medical_ai_safety_field_kit_global_safety_claim_review_workbook",
]

REQUIRED_URLS = [
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/150",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/151",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/152",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_REVIEWER_START_HERE_20260619.md",
]

REQUIRED_SFC = [f"SFC{i:03d}" for i in range(1, 11)]

REQUIRED_SFC_MAPPINGS = [
    "SFC005 maps to synthetic evidence boundary",
    "SFC006 maps to policy wording",
    "SFC007 maps to data fitness",
    "SFC008 maps to human review role",
    "SFC009 maps to vendor language",
    "SFC010 maps to sandbox boundary",
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
    issue_text = ISSUE_COMMENT.read_text(encoding="utf-8") if ISSUE_COMMENT.exists() else ""
    release_text = RELEASE_NOTES.read_text(encoding="utf-8") if RELEASE_NOTES.exists() else ""

    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in doc_text.lower():
            errors.append(f"Doc missing phrase: {phrase}")
    for url in REQUIRED_URLS:
        if url not in doc_text:
            errors.append(f"Doc missing URL: {url}")
    for card_id in REQUIRED_SFC:
        if card_id not in doc_text:
            errors.append(f"Doc missing card id: {card_id}")
    for mapping in REQUIRED_SFC_MAPPINGS:
        if mapping.lower() not in doc_text.lower():
            errors.append(f"Doc missing canonical card mapping: {mapping}")
    for phrase in ["Route:", "Risk:", "Missing gate:", "Safer wording:"]:
        if phrase not in issue_text:
            errors.append(f"Issue comment missing phrase: {phrase}")
    for phrase in ["This release adds the Global Safety Claim Review Workbook", "SFC001 through SFC010", "Boundary"]:
        if phrase.lower() not in release_text.lower():
            errors.append(f"Release notes missing phrase: {phrase}")

    check_text("Doc", doc_text, errors)
    check_text("Issue comment", issue_text, errors)
    check_text("Release notes", release_text, errors)

    if DATA.exists():
        payload = json.loads(DATA.read_text(encoding="utf-8"))
        if payload.get("artifact") != "medical_ai_safety_field_kit_global_safety_claim_review_workbook":
            errors.append("Unexpected artifact id")
        if payload.get("hub_issue") != 149:
            errors.append("Hub issue must be 149")
        if payload.get("starter_issues") != [150, 151, 152]:
            errors.append("Starter issues must be 150 151 152")
        if payload.get("safe_failure_cards_mapped") != 10:
            errors.append("Expected ten Safe Failure Cards mapped")
        if payload.get("objection_counting_rule") != "Only visible third party comments count":
            errors.append("Unexpected objection counting rule")
        urls = set(payload.get("route_urls", []))
        for url in REQUIRED_URLS:
            if url not in urls:
                errors.append(f"JSON missing URL: {url}")
        for flag in FALSE_FLAGS:
            if payload.get(flag) is not False:
                errors.append(f"Expected false flag: {flag}")

    if errors:
        print("FAIL global safety claim review workbook validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS global safety claim review workbook validation")
    print(f"doc={DOC.relative_to(ROOT)}")
    print(f"issue_comment={ISSUE_COMMENT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
