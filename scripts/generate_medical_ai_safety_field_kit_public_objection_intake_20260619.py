#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_OBJECTION_INTAKE_20260619.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_public_objection_intake_20260619.json"
ISSUE_COMMENT = ROOT / "outputs" / "medical_ai_safety_field_kit_public_objection_intake_issue149_comment_20260619.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_public_objection_intake_public_action_audit_20260619.md"


ISSUE_URL = "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149"
INTAKE_URL = "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_OBJECTION_INTAKE_20260619.md"
PUBLIC_CALL = "docs/MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_CALL_20260619.md"
TARGET_INDEX = "docs/MEDICAL_AI_SAFETY_FIELD_KIT_TARGET_DISTRIBUTION_INDEX_20260619.md"
OBJECTION_LEDGER = "docs/MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_OBJECTION_LEDGER_20260619.md"


lanes = [
    "source claim that needs stronger support",
    "Turkish medical wording that could mislead",
    "safety gate that should block public trust language",
    "evaluation result that could be misused",
    "missing failure mode in the field kit",
    "reviewer role that should be asked next without naming a specific organization",
]

reply_format = """Lane:
Risk:
Fix:
"""

payload = {
    "artifact_id": "medical_ai_safety_field_kit_public_objection_intake_20260619",
    "created_at_trt": "2026 06 19 20 20 TRT",
    "source_issue_number": 149,
    "source_issue_url": ISSUE_URL,
    "issue_state_checked": "OPEN",
    "issue_comment_count_at_build": 2,
    "public_call_doc": PUBLIC_CALL,
    "target_distribution_index_doc": TARGET_INDEX,
    "public_objection_ledger_doc": OBJECTION_LEDGER,
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "gmail_reply_state": "Prior Hacettepe health informatics acknowledgement only. No new substantive route owner reply.",
    "artifact_role": "lower first public comment friction for issue 149",
    "public_action_shape": "single issue 149 maintainer comment",
    "release_should_be_opened": False,
    "lanes": lanes,
    "reply_format": reply_format,
    "minimum_valid_public_comment": {
        "has_lane": True,
        "has_risk": True,
        "has_fix": True,
        "uses_synthetic_or_public_information_only": True,
        "does_not_name_specific_organization_unless_public_self_identified": True,
        "does_not_claim_validation_or_partnership": True,
    },
    "blocked_wording": [
        "reviewer recruitment",
        "official reviewer intake",
        "apply to review",
        "accepted reviewer",
        "clinical validation",
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
        "source truth",
        "certified source support",
        "model ranking",
        "score certification",
        "best model",
        "submit patient cases",
        "share real cases",
        "send examples from practice",
        "terms accepted",
        "paid review",
    ],
    "blocked_claims": [
        "patient data",
        "private case details",
        "clinical validation",
        "clinical deployment",
        "diagnosis or treatment advice",
        "benchmark ranking",
        "score certification",
        "source truth certification",
        "partner status",
        "institution approval",
        "official route access",
        "public authority guidance",
        "formal application",
        "payment",
        "terms acceptance",
        "endorsement",
    ],
    "contains_patient_data": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_diagnosis_or_treatment_advice": False,
    "claims_benchmark_ranking": False,
    "claims_score_certification": False,
    "claims_source_truth_certification": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_official_route_access": False,
    "claims_public_authority_guidance": False,
    "claims_endorsement": False,
    "claims_formal_application": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "release_published": False,
    "email_sent": False,
    "social_posted": False,
    "next_non_sending_action": "Add one issue 149 maintainer comment linking the public objection intake menu.",
}


doc = f"""# Medical AI Safety Field Kit Public Objection Intake

Date: 2026 06 19

Status: first contribution menu for issue 149.

Issue state checked at build: open.

Issue comment count at build: 2.

Public front door:

1. {ISSUE_URL}

Companion artifacts:

1. {PUBLIC_CALL}
2. {TARGET_INDEX}
3. {OBJECTION_LEDGER}

## Purpose

This artifact lowers the first comment ask. A useful public contribution can be one lane, one risk, and one fix. The goal is to turn a broad public review call into short objections that can be routed into the public objection ledger.

## First contribution menu
"""

for index, lane in enumerate(lanes, start=1):
    doc += f"\n{index}. {lane}.\n"

doc += f"""

## Reply format

Copy this into issue 149:

```text
{reply_format.rstrip()}
```

## Minimum useful comment

1. Pick one lane.
2. Write one risk in one or two sentences.
3. Suggest one fix or next check.
4. Use only synthetic or public information.
5. Do not name a specific organization unless it publicly self identifies in the issue.
6. Do not include patient data, private case details, images, records, dates, institutions, or identifiers.

## Stop rules

Do not use this menu to claim formal review, approval, partnership, authority direction, clinical validation, clinical deployment, diagnosis advice, treatment advice, safety proof, ranked model meaning, certified score meaning, source truth status, formal application, payment, terms acceptance, or endorsement.

## Maintainer use

When a public comment arrives, route it to the objection ledger only if it is visible on issue 149 and it follows the lane, risk, fix shape.

## Public action boundary

This artifact only prepares a public issue comment route. It sends no email, makes no social post, opens no release, submits no application, accepts no terms, makes no payment, and uses no patient data.

## Maintainer command

Run:

```bash
make medical_ai_safety_field_kit_public_objection_intake
```
"""


issue_comment = f"""Maintainer note for issue 149:

I am switching this from a broad review call to a first contribution menu.

Pick one lane and leave one short comment. A useful comment can be three lines:

Lane:
Risk:
Fix:

Choose one:

1. Source claim that needs stronger support.
2. Turkish medical wording that could mislead.
3. Safety gate that should block public trust language.
4. Evaluation result that could be misused.
5. Missing failure mode in the field kit.
6. Reviewer role that should be asked next, without naming a specific organization.

Examples must be synthetic or public. Do not include private case details.

Template:

{INTAKE_URL}

This is only a public routing and criticism surface. It is not evidence of formal review, approval, partnership, authority direction, clinical rollout readiness, safety proof, score meaning, source truth, or external endorsement.
"""


audit = """# Public Action Audit

Artifact: Medical AI Safety Field Kit Public Objection Intake

Date: 2026 06 19

Gmail state: active medical AI outreach threads and targeted searches were checked before build. The only inbound item remains the prior Hacettepe health informatics acknowledgement. No new substantive route owner reply was found.

Issue state: issue 149 was checked as open. The issue had two maintainer comments at build time and no visible external objection comments.

External material state: one issue comment body was prepared for the first contribution menu. No email, social post, application, release, or external repository action was performed by this artifact before validation.

Public action allowed after validation: repository commit and one issue 149 maintainer comment.

External actions not performed: no mail, no social post, no release, no application, no TBYS, no PRODIS, no payment, no terms acceptance, no partner claim, no institution claim, no official route access claim, no authority direction claim, no endorsement, no patient data, no clinical validation, no clinical deployment, no clinical advice, no ranked model meaning, and no certified score meaning.
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    write(DOC, doc)
    write(DATA, json.dumps(payload, ensure_ascii=False, indent=2))
    write(ISSUE_COMMENT, issue_comment)
    write(AUDIT, audit)


if __name__ == "__main__":
    main()
