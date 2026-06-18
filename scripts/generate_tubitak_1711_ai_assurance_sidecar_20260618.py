#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUBITAK_1711_AI_ASSURANCE_SIDECAR_20260618.md"
DATA = ROOT / "docs" / "tubitak_1711_ai_assurance_sidecar_20260618.json"


SOURCE_FACTS = [
    {
        "fact_id": "T1711F001",
        "source": "TÜBİTAK 1711 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "checked_fact": "The 2026 call opened on 15 June 2026.",
        "field_read": "There is a live national AI ecosystem call.",
    },
    {
        "fact_id": "T1711F002",
        "source": "TÜBİTAK 1711 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "checked_fact": "The official page lists application intake from 15 June 2026 to 18 September 2026.",
        "field_read": "The window is long enough for scouting and decision work.",
    },
    {
        "fact_id": "T1711F003",
        "source": "TÜBİTAK 1711 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "checked_fact": "The official page lists pre registration completion by 14 September 2026 at 17:30.",
        "field_read": "A decision should happen well before September.",
    },
    {
        "fact_id": "T1711F004",
        "source": "TÜBİTAK 1711 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "checked_fact": "The listed priority areas are smart production systems, smart agriculture, food and livestock, financial technologies, climate change and sustainability, and smart education technologies.",
        "field_read": "Direct health AI fit is weak and should not be forced.",
    },
    {
        "fact_id": "T1711F005",
        "source": "TÜBİTAK 1711 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "checked_fact": "The official page says the model expects a consortium including a customer organization, at least one technology provider company, and at least one experienced university research lab, center, public research center, or institute.",
        "field_read": "Dr. Ozkan cannot act alone as an applicant without a consortium route.",
    },
    {
        "fact_id": "T1711F006",
        "source": "TÜBİTAK 1711 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "checked_fact": "The official page says the consortium is expected to meet TÜBİTAK Yapay Zeka Enstitüsü before application and include an intent declaration form.",
        "field_read": "Any real application path needs early route clearance and partner commitment.",
    },
]


SIDECAR_MODULES = [
    {
        "module_id": "T1711S001",
        "name": "Fit warning",
        "content": "State that health is not a listed 2026 priority area and that the sidecar is only adjacent AI assurance infrastructure.",
        "decision_value": "Prevents an overclaimed health fit.",
    },
    {
        "module_id": "T1711S002",
        "name": "Consortium readiness gate",
        "content": "List the customer organization, technology provider, and research lab roles that would need to exist before any action.",
        "decision_value": "Separates public proof of work from actual application eligibility.",
    },
    {
        "module_id": "T1711S003",
        "name": "AI assurance sidecar scope",
        "content": "Offer data quality gates, source support review, no ranking failure reports, and human review protocols as cross domain AI safety support.",
        "decision_value": "Creates a useful angle without pretending to be the core funded product.",
    },
    {
        "module_id": "T1711S004",
        "name": "Non submission boundary",
        "content": "Block application, intent declaration, meeting request, partner commitment, budget, and terms language until Dr. Ozkan clears a route.",
        "decision_value": "Protects against accidental formal action.",
    },
    {
        "module_id": "T1711S005",
        "name": "Scouting list",
        "content": "Prepare a short list of possible eligible domain routes only after a health adjacent or assurance aligned fit is selected.",
        "decision_value": "Turns the call into an opportunity radar rather than a rushed submission.",
    },
]


BOUNDARIES = [
    "No application submission.",
    "No intent declaration.",
    "No partner commitment.",
    "No budget claim.",
    "No terms acceptance.",
    "No payment.",
    "No health priority fit claim.",
    "No official role claim.",
    "No endorsement claim.",
    "No patient data.",
    "No clinical deployment claim.",
    "No clinical validation claim.",
]


def write_json() -> None:
    payload = {
        "artifact": "tubitak_1711_ai_assurance_sidecar_20260618",
        "status": "field readiness public preview",
        "source_facts": SOURCE_FACTS,
        "sidecar_modules": SIDECAR_MODULES,
        "source_fact_count": len(SOURCE_FACTS),
        "module_count": len(SIDECAR_MODULES),
        "direct_health_fit": "weak",
        "requires_goktug_clearance_before_scouting": True,
        "boundaries": BOUNDARIES,
        "contains_patient_data": False,
        "claims_submission": False,
        "claims_partner": False,
        "claims_official_role": False,
        "claims_health_priority_fit": False,
        "claims_clinical_validation": False,
        "claims_clinical_deployment": False,
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines = [
        "# TÜBİTAK 1711 AI Assurance Sidecar",
        "",
        "Date: 2026 06 18",
        "",
        "Status: field readiness public preview.",
        "",
        "Purpose: create an aggressive but truthful way to track TÜBİTAK 1711 as an AI ecosystem opportunity without forcing a direct health AI fit.",
        "",
        "This is not an application, not an intent declaration, not a partner commitment, not a budget claim, and not a meeting request.",
        "",
        "## Current verdict",
        "",
        "Direct health fit is weak because health is not listed among the official 2026 priority areas checked on the TÜBİTAK page.",
        "",
        "The strongest truthful move is an AI assurance sidecar: data quality gates, source support review, no ranking failure reports, and human review protocols that could support an eligible AI consortium if Dr. Ozkan chooses to scout one.",
        "",
        "## Source facts",
        "",
    ]
    for fact in SOURCE_FACTS:
        lines.extend(
            [
                f"### {fact['fact_id']}: {fact['source']}",
                "",
                f"Official source: {fact['url']}",
                "",
                f"Checked fact: {fact['checked_fact']}",
                "",
                f"Field read: {fact['field_read']}",
                "",
            ]
        )
    lines.extend(["## Sidecar modules", ""])
    for module in SIDECAR_MODULES:
        lines.extend(
            [
                f"### {module['module_id']}: {module['name']}",
                "",
                f"Content: {module['content']}",
                "",
                f"Decision value: {module['decision_value']}",
                "",
            ]
        )
    lines.extend(["## Boundary", ""])
    lines.extend(f"{index}. {boundary}" for index, boundary in enumerate(BOUNDARIES, start=1))
    lines.extend(
        [
            "",
            "## Decision needed",
            "",
            "Dr. Ozkan must decide whether to scout a 1711 adjacent route despite weak direct health fit. If yes, the next work should identify a possible eligible customer organization, technology provider, and research lab route before any contact.",
            "",
            "## Runnable check",
            "",
            "```bash",
            "make tubitak_1711_ai_assurance_sidecar",
            "```",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_json()
    write_doc()
    print(f"generated={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"facts={len(SOURCE_FACTS)}")
    print(f"modules={len(SIDECAR_MODULES)}")


if __name__ == "__main__":
    main()
