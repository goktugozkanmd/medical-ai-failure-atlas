#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_CALL_20260619.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_public_call_20260619.json"
ISSUE_BODY = ROOT / "outputs" / "medical_ai_safety_field_kit_public_call_issue_body_20260619.md"
RELEASE_NOTES = ROOT / "outputs" / "medical_ai_safety_field_kit_public_call_release_notes_20260619.md"
PUBLIC_POST_SEED = ROOT / "outputs" / "medical_ai_safety_field_kit_public_call_public_post_seed_20260619.md"


GMAIL_CHECK = {
    "checked_at": "2026 06 19 18:35 TRT",
    "active_thread_ids_checked": [
        "19edcafe5c2dfa60",
        "19eda863ce89f083",
        "19edaa3a3868fd0f",
        "19edac07e13052fa",
        "19edb2e645ca1f6d",
        "19edb491af3d687b",
        "19edb64c4ae9fec6",
        "19edb8289b165cc0",
        "19edb9dc297ad804",
    ],
    "targeted_searches_checked": [
        "Gozdem Hacettepe medical ai failure atlas",
        "Acibadem CASE SEBIT medical ai failure atlas",
        "TUYZE TUSEB DEU KTU route owner no ranking",
        "health data data steward TUBITAK TUSEB medical ai failure atlas",
        "A4 UM TUSEB route fit info tuseb",
    ],
    "reply_state": "Earlier Hacettepe health informatics acknowledgement only. No new substantive route owner reply.",
}


PLATFORMS = [
    {
        "platform_id": "FK001",
        "name": "TR MedLLM SafetyBench",
        "public_ask": "Review Turkish medical wording risk, specialty coverage gaps, and unsafe benchmark interpretation.",
        "twenty_minute_action": "Comment with one Turkish medical term that can change meaning across context.",
    },
    {
        "platform_id": "FK002",
        "name": "Medical AI Failure Atlas Global",
        "public_ask": "Add failure modes that are clinically coherent but free of patient data.",
        "twenty_minute_action": "Comment with one failure mode title and the harm pathway it tests.",
    },
    {
        "platform_id": "FK003",
        "name": "Turkish Clinical AI Assurance Lab",
        "public_ask": "Challenge the field readiness checklist for hospital quality and safety use.",
        "twenty_minute_action": "Comment with one missing governance gate.",
    },
    {
        "platform_id": "FK004",
        "name": "SourceCheckup Medical",
        "public_ask": "Review whether a claim has enough source support before it is public facing.",
        "twenty_minute_action": "Comment with one medical AI claim that needs a source support check.",
    },
    {
        "platform_id": "FK005",
        "name": "Clinician AI Literacy Academy Turkiye",
        "public_ask": "Review the clinician literacy flow for practical teaching value.",
        "twenty_minute_action": "Comment with one clinician misconception that should be taught early.",
    },
    {
        "platform_id": "FK006",
        "name": "Health Data Quality and Label Audit Commons",
        "public_ask": "Review label quality, dataset boundary, and data fitness checks.",
        "twenty_minute_action": "Comment with one label audit failure pattern.",
    },
]


REVIEW_ROLES = [
    {
        "role_id": "R001",
        "role": "Clinician reviewer",
        "ask": "Find clinical nonsense, missing safety context, and unrealistic workflow assumptions.",
    },
    {
        "role_id": "R002",
        "role": "Health informatics reviewer",
        "ask": "Find weak data fitness, source support, terminology, and governance assumptions.",
    },
    {
        "role_id": "R003",
        "role": "Hospital quality reviewer",
        "ask": "Find missing readiness gates before any public trust language.",
    },
    {
        "role_id": "R004",
        "role": "Open model maintainer",
        "ask": "Find ways benchmark language can be misused as ranking or clinical proof.",
    },
    {
        "role_id": "R005",
        "role": "Turkish language reviewer",
        "ask": "Find Turkish medical wording that changes meaning or safety boundary.",
    },
    {
        "role_id": "R006",
        "role": "Source support reviewer",
        "ask": "Find unsupported claims and propose the minimum evidence needed.",
    },
]


BOUNDARIES = [
    "No patient data.",
    "No clinical validation claim.",
    "No clinical deployment claim.",
    "No diagnosis or treatment advice.",
    "No benchmark ranking.",
    "No score certification.",
    "No source truth certification.",
    "No partner claim.",
    "No institution claim.",
    "No endorsement claim.",
    "No formal application claim.",
    "No payment or terms acceptance.",
]


def write_json() -> None:
    payload = {
        "artifact": "medical_ai_safety_field_kit_public_call_20260619",
        "status": "public flagship call for clinical and technical reviewers",
        "checked_after_reading_baglam2": True,
        "checked_after_reading_trackers": True,
        "checked_gmail_before_build": True,
        "gmail_check": GMAIL_CHECK,
        "platform_count": len(PLATFORMS),
        "platform_ids": [platform["platform_id"] for platform in PLATFORMS],
        "review_role_count": len(REVIEW_ROLES),
        "review_role_ids": [role["role_id"] for role in REVIEW_ROLES],
        "boundary_count": len(BOUNDARIES),
        "contains_patient_data": False,
        "claims_clinical_validation": False,
        "claims_clinical_deployment": False,
        "claims_diagnosis_or_treatment_advice": False,
        "claims_benchmark_ranking": False,
        "claims_score_certification": False,
        "claims_source_truth_certification": False,
        "claims_partner": False,
        "claims_institutional_approval": False,
        "claims_endorsement": False,
        "claims_formal_application": False,
        "claims_payment": False,
        "claims_terms_acceptance": False,
        "public_call": {
            "primary_action": "Comment on the public issue with one reviewer role and one concrete objection or missing safety check.",
            "secondary_action": "Open a small issue that names one platform lane and one safety gap.",
            "target_response_time": "twenty minutes",
        },
        "next_action": "Publish the public call issue and release, then use it as the single review link for targeted outreach after Goktug approves exact outbound messages.",
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines = [
        "# Medical AI Safety Field Kit Public Call",
        "",
        "Date: 2026 06 19",
        "",
        "Status: public flagship call for clinical and technical reviewers.",
        "",
        "This is the public front door for the Medical AI Safety Field Kit. It turns the existing safety materials into one visible call for reviewers, builders, clinicians, health informatics teams, hospital quality teams, Turkish language reviewers, and open model maintainers.",
        "",
        "## Challenge statement",
        "",
        "Medical AI projects should not ask for trust until they can explain source support, data fitness, use boundary, human review role, Turkish context risk, and failure reporting route.",
        "",
        "This call asks the field to attack those weak points in public. Strong objections are useful. Missing failure modes are useful. Reviewer comments are useful. Silent internal polish is not enough.",
        "",
        "## What this field kit unifies",
        "",
    ]
    for platform in PLATFORMS:
        lines.extend(
            [
                f"### {platform['platform_id']}: {platform['name']}",
                "",
                f"Public ask: {platform['public_ask']}",
                "",
                f"Twenty minute action: {platform['twenty_minute_action']}",
                "",
            ]
        )
    lines.extend(["## Reviewer roles we want now", ""])
    for role in REVIEW_ROLES:
        lines.extend(
            [
                f"{role['role_id']}. {role['role']}: {role['ask']}",
                "",
            ]
        )
    lines.extend(
        [
            "## How to contribute in public",
            "",
            "1. Pick one reviewer role.",
            "2. Pick one platform lane.",
            "3. Comment with one concrete objection, missing safety check, failure mode, source support gap, Turkish wording risk, or field readiness gap.",
            "4. Keep examples synthetic and free of patient data.",
            "5. Do not submit diagnosis, treatment, private clinical text, protected data, institutional statements, partner statements, or clinical deployment claims.",
            "",
            "## What a useful comment looks like",
            "",
            "Role: clinician reviewer.",
            "",
            "Lane: Medical AI Failure Atlas Global.",
            "",
            "Concern: this failure mode needs a clearer human review trigger before any public safety claim.",
            "",
            "Suggested fix: add a release gate that blocks public wording until the reviewer can state the clinical action boundary.",
            "",
            "## Public boundaries",
            "",
        ]
    )
    lines.extend(f"{index}. {boundary}" for index, boundary in enumerate(BOUNDARIES, start=1))
    lines.extend(
        [
            "",
            "## Start state checked before build",
            "",
            "Live BAGLAM2, portfolio trackers, active Gmail outreach threads, and targeted Gmail searches were checked before this package. The only inbound state remains an earlier acknowledgement. No new substantive route owner reply was found before this public call was built.",
            "",
            "## Maintainer command",
            "",
            "Run:",
            "",
            "```bash",
            "make medical_ai_safety_field_kit_public_call",
            "```",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def write_issue_body() -> None:
    lines = [
        "# Medical AI Safety Field Kit Public Call",
        "",
        "This issue is the public front door for the Medical AI Safety Field Kit.",
        "",
        "The ask is direct: clinicians, health informatics reviewers, hospital quality teams, Turkish language reviewers, source support reviewers, and open model maintainers should attack the weak points before medical AI safety language is trusted.",
        "",
        "Useful comments:",
        "",
        "1. One missing failure mode.",
        "2. One unsafe benchmark interpretation.",
        "3. One Turkish medical wording risk.",
        "4. One source support gap.",
        "5. One hospital readiness gate.",
        "6. One clinician literacy misconception.",
        "",
        "Use this format:",
        "",
        "Role:",
        "",
        "Lane:",
        "",
        "Concern:",
        "",
        "Suggested fix:",
        "",
        "Boundary: this is not clinical validation, not clinical deployment, not diagnosis or treatment advice, not patient data work, not benchmark ranking, not score certification, not source truth certification, not partner status, not institutional approval, not formal application, not payment, not terms acceptance, and not endorsement.",
        "",
        "Validation:",
        "",
        "1. `make medical_ai_safety_field_kit_public_call`",
        "2. Full `make validate`",
        "3. Public release sanitation",
        "4. Public text safety audit record",
        "5. Reference extraction check",
        "6. Manual source support note",
        "",
        "Artifacts:",
        "",
        "1. `docs/MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_CALL_20260619.md`",
        "2. `docs/medical_ai_safety_field_kit_public_call_20260619.json`",
        "3. `scripts/generate_medical_ai_safety_field_kit_public_call_20260619.py`",
        "4. `scripts/validate_medical_ai_safety_field_kit_public_call_20260619.py`",
        "",
    ]
    ISSUE_BODY.write_text("\n".join(lines), encoding="utf-8")


def write_release_notes() -> None:
    lines = [
        "# Medical AI Safety Field Kit Public Call",
        "",
        "This release adds a flagship public call for clinical and technical reviewers.",
        "",
        "It unifies six platform lanes into one public review surface: TR MedLLM SafetyBench, Medical AI Failure Atlas Global, Turkish Clinical AI Assurance Lab, SourceCheckup Medical, Clinician AI Literacy Academy Turkiye, and Health Data Quality and Label Audit Commons.",
        "",
        "The release is designed for public participation: a reviewer can spend twenty minutes and add one concrete objection, missing failure mode, source support gap, Turkish wording risk, hospital readiness gate, or unsafe benchmark interpretation.",
        "",
        "Boundary: no patient data, no clinical validation, no clinical deployment, no diagnosis or treatment advice, no benchmark ranking, no score certification, no source truth certification, no partner claim, no institution claim, no endorsement, no formal application, no payment, and no terms acceptance.",
        "",
        "Validation passed:",
        "",
        "1. `make medical_ai_safety_field_kit_public_call`",
        "2. Full `make validate`",
        "3. Public release sanitation",
        "4. Public text safety audit record",
        "5. Reference extraction check",
        "6. Manual source support note",
        "",
    ]
    RELEASE_NOTES.write_text("\n".join(lines), encoding="utf-8")


def write_public_post_seed() -> None:
    lines = [
        "# Public post seed",
        "",
        "Medical AI Safety Field Kit is now open for clinical and technical review.",
        "",
        "The point is simple: medical AI projects should not ask for trust until source support, data fitness, use boundary, human review, Turkish context risk, and failure reporting are visible.",
        "",
        "I am asking clinicians, health informatics reviewers, hospital quality teams, Turkish medical language reviewers, source support reviewers, and open model maintainers to attack the weak points in public.",
        "",
        "A useful review can take twenty minutes: pick one lane, name one concern, and suggest one concrete fix.",
        "",
        "No patient data. No clinical validation claim. No deployment claim. No ranking claim. Just practical safety pressure before public trust language.",
        "",
    ]
    PUBLIC_POST_SEED.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DATA.parent.mkdir(parents=True, exist_ok=True)
    ISSUE_BODY.parent.mkdir(parents=True, exist_ok=True)
    write_json()
    write_doc()
    write_issue_body()
    write_release_notes()
    write_public_post_seed()
    print(f"wrote {DOC.relative_to(ROOT)}")
    print(f"wrote {DATA.relative_to(ROOT)}")
    print(f"wrote {ISSUE_BODY.relative_to(ROOT)}")
    print(f"wrote {RELEASE_NOTES.relative_to(ROOT)}")
    print(f"wrote {PUBLIC_POST_SEED.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
