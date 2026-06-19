#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_OBJECTION_INTAKE_20260619.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_public_objection_intake_20260619.json"
ISSUE_COMMENT = ROOT / "outputs" / "medical_ai_safety_field_kit_public_objection_intake_issue149_comment_20260619.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_public_objection_intake_public_action_audit_20260619.md"


REQUIRED_FILES = [DOC, DATA, ISSUE_COMMENT, AUDIT]
REQUIRED_DOC_PHRASES = [
    "Medical AI Safety Field Kit Public Objection Intake",
    "first contribution menu for issue 149",
    "Issue state checked at build: open",
    "Issue comment count at build: 2",
    "First contribution menu",
    "Reply format",
    "Minimum useful comment",
    "Stop rules",
    "make medical_ai_safety_field_kit_public_objection_intake",
]
REQUIRED_COMMENT_PHRASES = [
    "Maintainer note for issue 149",
    "first contribution menu",
    "Lane:",
    "Risk:",
    "Fix:",
    "Examples must be synthetic or public",
    "only a public routing and criticism surface",
]
REQUIRED_LANES = {
    "source claim that needs stronger support",
    "Turkish medical wording that could mislead",
    "safety gate that should block public trust language",
    "evaluation result that could be misused",
    "missing failure mode in the field kit",
    "reviewer role that should be asked next without naming a specific organization",
}
REQUIRED_FALSE_FLAGS = [
    "release_should_be_opened",
    "contains_patient_data",
    "claims_clinical_validation",
    "claims_clinical_deployment",
    "claims_diagnosis_or_treatment_advice",
    "claims_benchmark_ranking",
    "claims_score_certification",
    "claims_source_truth_certification",
    "claims_partner",
    "claims_institutional_approval",
    "claims_official_route_access",
    "claims_public_authority_guidance",
    "claims_endorsement",
    "claims_formal_application",
    "claims_payment",
    "claims_terms_acceptance",
    "release_published",
    "email_sent",
    "social_posted",
]
FORBIDDEN_WORDING = [
    "reviewer recruitment",
    "official reviewer intake",
    "apply to review",
    "accepted reviewer",
    "validated by clinicians",
    "deployment ready",
    "safe for clinical use",
    "hospital ready",
    "approved by",
    "endorsed by",
    "in partnership with",
    "institutional review",
    "TUSEB reviewer",
    "TUYZE route owner approved",
    "Hacettepe collaboration",
    "Ministry route",
    "certified source support",
    "model ranking",
    "score certification",
    "best model",
    "submit patient cases",
    "share real cases",
    "send examples from practice",
    "terms accepted",
    "paid review",
]
FORBIDDEN_AFFIRMATIVE_CLAIMS = [
    "patient data used",
    "real patient case",
    "private case details:",
    "clinically validated",
    "clinical deployment ready",
    "diagnosis advice provided",
    "treatment advice provided",
    "benchmark ranking confirmed",
    "score certified",
    "source truth certified",
    "partner confirmed",
    "institution approved",
    "official route access confirmed",
    "formal application submitted",
    "payment completed",
]
FORBIDDEN_INTERNAL_LABELS = [
    "de" + "AI",
    "human" + "ized",
    "AI " + "detector",
    "submit" + "_audit",
]


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def add_text_checks(errors: list[str], label: str, text: str) -> None:
    lower_text = text.lower()
    for phrase in FORBIDDEN_WORDING + FORBIDDEN_AFFIRMATIVE_CLAIMS:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains forbidden wording: {phrase}")
    for phrase in FORBIDDEN_INTERNAL_LABELS:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains internal process label: {phrase}")
    if "-" in text_without_urls(text):
        errors.append(f"{label} contains non URL hyphen character")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing artifact: {path.relative_to(ROOT)}")

    texts = {
        "Doc": DOC.read_text(encoding="utf-8") if DOC.exists() else "",
        "Issue comment": ISSUE_COMMENT.read_text(encoding="utf-8") if ISSUE_COMMENT.exists() else "",
        "Audit": AUDIT.read_text(encoding="utf-8") if AUDIT.exists() else "",
    }

    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in texts["Doc"].lower():
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in REQUIRED_COMMENT_PHRASES:
        if phrase.lower() not in texts["Issue comment"].lower():
            errors.append(f"Issue comment missing required phrase: {phrase}")
    for label, text in texts.items():
        add_text_checks(errors, label, text)

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}

    for key in ["checked_after_reading_baglam2", "checked_after_reading_trackers", "checked_gmail_before_build"]:
        if payload.get(key) is not True:
            errors.append(f"JSON flag {key} expected True")
    for key in REQUIRED_FALSE_FLAGS:
        if payload.get(key) is not False:
            errors.append(f"JSON flag {key} expected False")

    if payload.get("source_issue_number") != 149:
        errors.append("source issue must be 149")
    if payload.get("issue_state_checked") != "OPEN":
        errors.append("issue state must be OPEN")
    if payload.get("issue_comment_count_at_build") != 2:
        errors.append("issue comment count at build must be two")
    if payload.get("public_action_shape") != "single issue 149 maintainer comment":
        errors.append("public action shape must stay one issue comment")
    if "No new substantive route owner reply" not in payload.get("gmail_reply_state", ""):
        errors.append("Gmail reply state must state no new substantive route owner reply")

    if set(payload.get("lanes", [])) != REQUIRED_LANES:
        errors.append("lane set mismatch")

    reply_format = payload.get("reply_format", "")
    for field in ["Lane:", "Risk:", "Fix:"]:
        if field not in reply_format:
            errors.append(f"reply format missing field: {field}")

    minimum = payload.get("minimum_valid_public_comment", {})
    for key in [
        "has_lane",
        "has_risk",
        "has_fix",
        "uses_synthetic_or_public_information_only",
        "does_not_name_specific_organization_unless_public_self_identified",
        "does_not_claim_validation_or_partnership",
    ]:
        if minimum.get(key) is not True:
            errors.append(f"minimum useful comment flag {key} expected True")

    if errors:
        print("FAIL Medical AI Safety Field Kit public objection intake validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Medical AI Safety Field Kit public objection intake validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"issue_comment={ISSUE_COMMENT.relative_to(ROOT)}")
    print(f"audit={AUDIT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
