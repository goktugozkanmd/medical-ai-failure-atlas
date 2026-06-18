#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "CURRENT_MEDICAL_AI_INTELLIGENCE_PRIORITY_UPDATE_20260618_V0_1.md"
DATA = ROOT / "docs" / "current_medical_ai_intelligence_priority_update_20260618_v0_1.json"


SOURCE_ROWS = [
    {
        "source_id": "CMIPU001",
        "source_name": "TÜBİTAK 1711 Yapay Zekâ Ekosistem 2026 announcement",
        "source_url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "source_date": "16 June 2026",
        "observed_claim": "The fifth 1711 call opened on 15 June 2026, lists five 2026 priority areas, and receives applications through PRODİS.",
        "portfolio_impact": "Keep the 1711 readiness packet active but do not claim a health priority route because health is not listed among the five stated 2026 areas.",
        "decision_lock": "Any application, partner, non medical pivot, terms step, budget step, or submission needs Dr. Ozkan clearance.",
    },
    {
        "source_id": "CMIPU002",
        "source_name": "Ankara İl Sağlık Müdürlüğü AI studies ethics page",
        "source_url": "https://ankaraism.saglik.gov.tr/TR-371527/yapay-zeka-ile-ilgili-calismalar.html",
        "source_date": "30 January 2026",
        "observed_claim": "The page says AI related studies presented to that ethics committee will be suspended until new regulation.",
        "portfolio_impact": "Add a Türkiye ethics status verification gate before any ethics, clinical study, deployment, or validation claim.",
        "decision_lock": "Do not generalize this local page into a national rule without separate verification.",
    },
    {
        "source_id": "CMIPU003",
        "source_name": "Sağlık Bilgi Sistemleri Genel Müdürlüğü Yapay Zekâ ve Yenilikçi Teknolojiler Daire Başkanlığı page",
        "source_url": "https://sbsgm.saglik.gov.tr/TR-104172/yapay-zeka-ve-yenilikci-teknolojiler-daire-baskanligi.html",
        "source_date": "21 August 2024",
        "observed_claim": "The page lists tasks including identifying AI improvable processes, producing or procuring AI solutions, following AI technologies, building stakeholder collaborations, interoperability, and education materials.",
        "portfolio_impact": "Track A should emphasize assurance lab, clinician literacy, interoperability, and education surfaces without claiming official role or endorsement.",
        "decision_lock": "No ministry role, route access, or endorsement claim without explicit verified authorization.",
    },
    {
        "source_id": "CMIPU004",
        "source_name": "OpenAI HealthBench public page",
        "source_url": "https://openai.com/index/healthbench/",
        "source_date": "2025",
        "observed_claim": "HealthBench describes realistic health conversations, physician expert rubrics, 262 physicians, 60 countries, and 5000 conversations.",
        "portfolio_impact": "Track B should keep building clinician rubric literacy, reviewer question fields, and no ranking safety reports without claiming benchmark compatibility.",
        "decision_lock": "No HealthBench compatibility, score, or benchmark equivalence claim without explicit benchmark owner aligned validation.",
    },
    {
        "source_id": "CMIPU005",
        "source_name": "MedHELM public site",
        "source_url": "https://medhelm.org/",
        "source_date": "2026",
        "observed_claim": "MedHELM presents an open community benchmark with 121 clinical tasks, 22 subcategories, 31 datasets, 5 categories, and measures including accuracy, calibration, robustness, and writing style.",
        "portfolio_impact": "Track B should add benchmark compatibility notes that explain what local synthetic artifacts can and cannot map to.",
        "decision_lock": "No MedHELM compatibility, leaderboard, model comparison, or clinical workflow deployment claim.",
    },
    {
        "source_id": "CMIPU006",
        "source_name": "Google MedGemma Health AI Developer Foundations page",
        "source_url": "https://developers.google.com/health-ai-developer-foundations/medgemma",
        "source_date": "2026",
        "observed_claim": "The page describes MedGemma models for medical text and image comprehension and states that use cases require validation.",
        "portfolio_impact": "Add open model boundary notes that separate model availability from local clinical validation or deployment readiness.",
        "decision_lock": "No model run, endpoint use, terms acceptance, clinical validation, or deployment claim without clearance.",
    },
    {
        "source_id": "CMIPU007",
        "source_name": "European Commission AI in healthcare page",
        "source_url": "https://health.ec.europa.eu/ehealth-digital-health-and-care/artificial-intelligence-healthcare_en",
        "source_date": "2026",
        "observed_claim": "The page says the EU AI Act entered into force on 1 August 2024 and high risk AI systems such as AI based software intended for medical purposes must meet requirements including risk mitigation, data quality, user information, and human oversight.",
        "portfolio_impact": "Track A and Track B should keep no deployment and no regulatory claim language, while adding risk management and human oversight checklist fields.",
        "decision_lock": "No EU compliance, conformity, or regulatory readiness claim without legal and product scope review.",
    },
    {
        "source_id": "CMIPU008",
        "source_name": "FDA AI Enabled Medical Devices page",
        "source_url": "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices",
        "source_date": "2026",
        "observed_claim": "The page says the FDA AI Enabled Medical Device List identifies authorized marketed AI enabled devices and is updated periodically.",
        "portfolio_impact": "Track B should add transparent boundary wording that public evaluation tools are not devices, not marketing submissions, and not authorization claims.",
        "decision_lock": "No FDA authorization, device, SaMD, or marketing claim without formal regulatory scope review.",
    },
]


PRIORITY_ROWS = [
    {
        "priority_id": "CMIPUP001",
        "platform": "TR MedLLM SafetyBench",
        "priority_update": "Add local ethics status check fields and separate national readiness language from local ethics page observations.",
        "next_safe_build": "Türkiye AI ethics status gate note",
    },
    {
        "priority_id": "CMIPUP002",
        "platform": "Medical AI Failure Atlas Global",
        "priority_update": "Keep failure atlas as synthetic failure pattern infrastructure and add benchmark compatibility boundary notes.",
        "next_safe_build": "public benchmark boundary delta note",
    },
    {
        "priority_id": "CMIPUP003",
        "platform": "Turkish Clinical AI Assurance Lab",
        "priority_update": "Move assurance lab wording toward risk mitigation, human oversight, source support, interoperability, and education material gates.",
        "next_safe_build": "assurance lab ethics and oversight gate",
    },
    {
        "priority_id": "CMIPUP004",
        "platform": "SourceCheckup Medical",
        "priority_update": "Use HealthBench and MedHELM signals to deepen source support and clinician rubric fields without scoring claims.",
        "next_safe_build": "source support benchmark note",
    },
    {
        "priority_id": "CMIPUP005",
        "platform": "Clinician AI Literacy Academy Turkiye",
        "priority_update": "Turn current policy and benchmark observations into clinician literacy lessons on limits, oversight, and non deployment boundaries.",
        "next_safe_build": "clinician literacy current intelligence lesson",
    },
    {
        "priority_id": "CMIPUP006",
        "platform": "Health Data Quality and Label Audit Commons",
        "priority_update": "Add data quality, label provenance, and reviewer state fields aligned with high quality data and human oversight language.",
        "next_safe_build": "data quality oversight field note",
    },
]


FLAGS = {
    "contains_patient_data": False,
    "not_for_clinical_use": True,
    "no_submission_claim": True,
    "no_application_claim": True,
    "no_partner_claim": True,
    "no_official_role_claim": True,
    "no_endorsement_claim": True,
    "no_clinical_validation_claim": True,
    "no_clinical_deployment_claim": True,
    "no_model_ranking": True,
    "no_score_report": True,
    "no_endpoint_call": True,
    "no_terms_acceptance": True,
    "no_payment": True,
}


def build_payload() -> dict:
    return {
        "artifact": "current_medical_ai_intelligence_priority_update_20260618_v0_1",
        "status": "public_preview",
        "checked_at": "2026 06 18 09:04 TRT",
        "source_row_count": len(SOURCE_ROWS),
        "priority_row_count": len(PRIORITY_ROWS),
        "real_opportunity_detected": True,
        "real_opportunity": {
            "name": "TÜBİTAK 1711 Yapay Zekâ Ekosistem 2026 call",
            "announcement_date": "16 June 2026",
            "call_opening_date": "15 June 2026",
            "application_window": "15 June 2026 to 18 September 2026, source page states 25:59 UTC plus 3",
            "pre_registration_deadline": "14 September 2026 17:30",
            "blocker": "2026 priority areas do not list health, and any application needs partner commitment, scope decision, terms review, budget decision, and Dr. Ozkan clearance",
            "prepared_artifact": "docs/CURRENT_MEDICAL_AI_INTELLIGENCE_PRIORITY_UPDATE_20260618_V0_1.md",
        },
        **FLAGS,
        "sources": SOURCE_ROWS,
        "priority_updates": PRIORITY_ROWS,
        "next_safe_public_build": "Add a Türkiye AI ethics status gate note and a reviewer question maintainer public preview acceptance archive public handoff closure note without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
    }


def build_markdown(payload: dict) -> str:
    lines = [
        "# Current medical AI intelligence priority update v0.1",
        "",
        "Status: public preview.",
        "",
        "Checked at: 2026 06 18 09:04 TRT.",
        "",
        "This note records a current web intelligence pass for the two track medical AI build portfolio.",
        "",
        "It is not a submission, application, partner claim, clinical deployment claim, clinical validation claim, model ranking, score report, endpoint result, route access claim, official role claim, or endorsement claim.",
        "",
        "It uses no patient data.",
        "",
        "## Source rows",
        "",
    ]
    for index, row in enumerate(payload["sources"], start=1):
        lines.extend(
            [
                f"### {index}. {row['source_id']}",
                "",
                f"Source: {row['source_name']}",
                "",
                f"Source date: {row['source_date']}",
                "",
                f"Observed claim: {row['observed_claim']}",
                "",
                f"Portfolio impact: {row['portfolio_impact']}",
                "",
                f"Decision lock: {row['decision_lock']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Priority updates",
            "",
        ]
    )
    for index, row in enumerate(payload["priority_updates"], start=1):
        lines.extend(
            [
                f"### {index}. {row['priority_id']}",
                "",
                f"Platform: {row['platform']}",
                "",
                f"Priority update: {row['priority_update']}",
                "",
                f"Next safe build: {row['next_safe_build']}",
                "",
            ]
        )
    opportunity = payload["real_opportunity"]
    lines.extend(
        [
            "## Opportunity and blocker",
            "",
            f"Opportunity: {opportunity['name']}",
            "",
            f"Announcement date: {opportunity['announcement_date']}",
            "",
            f"Call opening date: {opportunity['call_opening_date']}",
            "",
            f"Application window: {opportunity['application_window']}",
            "",
            f"Pre registration deadline: {opportunity['pre_registration_deadline']}",
            "",
            f"Blocker: {opportunity['blocker']}",
            "",
            f"Prepared artifact: {opportunity['prepared_artifact']}",
            "",
            "Decision needed: Dr. Ozkan must decide whether to pursue a non medical pivot, partner route, or no action. Codex cannot submit or accept terms.",
            "",
            "## Next safe public build",
            "",
            payload["next_safe_public_build"],
            "",
            "## Runnable check",
            "",
            "```bash",
            "make current_medical_ai_intelligence_priority_update",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    payload = build_payload()
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    DOC.write_text(build_markdown(payload), encoding="utf-8")
    print(f"generated={DATA.relative_to(ROOT)}")
    print(f"generated={DOC.relative_to(ROOT)}")
    print(f"source_rows={payload['source_row_count']}")
    print(f"priority_rows={payload['priority_row_count']}")


if __name__ == "__main__":
    main()
