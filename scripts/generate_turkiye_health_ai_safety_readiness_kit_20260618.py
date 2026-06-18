#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_HEALTH_AI_SAFETY_READINESS_KIT_20260618.md"
DATA = ROOT / "docs" / "turkiye_health_ai_safety_readiness_kit_20260618.json"


SOURCE_SIGNALS = [
    {
        "source_id": "THAIS001",
        "source": "TÜYZE public site",
        "url": "https://tuyze.tuseb.gov.tr/",
        "checked_fact": "TÜYZE is the Türkiye Sağlık Veri Araştırmaları ve Yapay Zeka Uygulamaları Enstitüsü public site.",
        "field_read": "Direct national health AI fit.",
    },
    {
        "source_id": "THAIS002",
        "source": "TÜYZE public site",
        "url": "https://tuyze.tuseb.gov.tr/",
        "checked_fact": "The site lists a Sağlıkta Yapay Zeka Seminerleri program with Marmara University Faculty of Medicine from 08 April to 20 May 2026.",
        "field_read": "Clinician education route exists.",
    },
    {
        "source_id": "THAIS003",
        "source": "TÜYZE public site",
        "url": "https://tuyze.tuseb.gov.tr/",
        "checked_fact": "The site lists health AI and health data related institutional activity with public, university, and technology actors.",
        "field_read": "A readiness kit can be framed as public field preparation, not as a partner claim.",
    },
]


KIT_MODULES = [
    {
        "module_id": "THAIK001",
        "name": "Public health AI safety brief",
        "field_user": "health AI educator or lab coordinator",
        "artifact": "One page brief explaining why source support, data quality, clinician review, and no ranking language matter.",
        "decision_value": "Gives a reviewer enough context to decide whether a meeting or review is worth considering.",
    },
    {
        "module_id": "THAIK002",
        "name": "Clinician AI literacy micro module",
        "field_user": "clinician educator",
        "artifact": "Short handoff module that explains no patient data, no clinical validation, and no deployment claims.",
        "decision_value": "Converts abstract AI safety into teachable clinician review language.",
    },
    {
        "module_id": "THAIK003",
        "name": "Source support delta queue",
        "field_user": "source reviewer",
        "artifact": "Queue for separating citation presence from source support and source truth certification.",
        "decision_value": "Shows a practical review path without ranking a model.",
    },
    {
        "module_id": "THAIK004",
        "name": "Health data quality handoff",
        "field_user": "data quality lead",
        "artifact": "Checklist for label uncertainty, leakage, missing context, data provenance, and reviewer disagreement.",
        "decision_value": "Moves the conversation from model performance to data readiness.",
    },
    {
        "module_id": "THAIK005",
        "name": "Sandbox readiness boundary",
        "field_user": "governance or program reviewer",
        "artifact": "Boundary note that blocks route access, approval, validation, and deployment claims.",
        "decision_value": "Lets a group discuss sandbox readiness without implying access or endorsement.",
    },
    {
        "module_id": "THAIK006",
        "name": "First outreach packet",
        "field_user": "Dr. Goktug Ozkan after explicit clearance",
        "artifact": "Short introduction draft and attachment list for a named national health AI route.",
        "decision_value": "Turns proof of work into a field conversation while preserving decision gates.",
    },
]


BOUNDARIES = [
    "No patient data.",
    "No clinical advice.",
    "No clinical deployment claim.",
    "No clinical validation claim.",
    "No official role claim.",
    "No partner claim.",
    "No route access claim.",
    "No submission claim.",
    "No terms acceptance.",
    "No payment.",
    "No endorsement claim.",
]


def write_json() -> None:
    payload = {
        "artifact": "turkiye_health_ai_safety_readiness_kit_20260618",
        "status": "field readiness public preview",
        "date": "2026 06 18",
        "source_signals": SOURCE_SIGNALS,
        "modules": KIT_MODULES,
        "module_count": len(KIT_MODULES),
        "boundaries": BOUNDARIES,
        "requires_goktug_clearance_before_outreach": True,
        "contains_patient_data": False,
        "claims_official_role": False,
        "claims_partner": False,
        "claims_endorsement": False,
        "claims_submission": False,
        "claims_clinical_validation": False,
        "claims_clinical_deployment": False,
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines: list[str] = [
        "# Türkiye Health AI Safety Readiness Kit",
        "",
        "Date: 2026 06 18",
        "",
        "Status: field readiness public preview.",
        "",
        "Purpose: prepare a national health AI safety conversation around Turkish medical AI evaluation, clinician AI literacy, health data quality, source support, and sandbox readiness.",
        "",
        "This is a field package, not a submission, not a partnership claim, not an institutional role claim, and not a clinical validation claim.",
        "",
        "## Source signals",
        "",
    ]
    for signal in SOURCE_SIGNALS:
        lines.extend(
            [
                f"### {signal['source_id']}: {signal['source']}",
                "",
                f"Official source: {signal['url']}",
                "",
                f"Checked fact: {signal['checked_fact']}",
                "",
                f"Field read: {signal['field_read']}",
                "",
            ]
        )
    lines.extend(["## Kit modules", ""])
    for module in KIT_MODULES:
        lines.extend(
            [
                f"### {module['module_id']}: {module['name']}",
                "",
                f"Field user: {module['field_user']}",
                "",
                f"Artifact: {module['artifact']}",
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
            "## Field action",
            "",
            "Prepare a named TÜYZE style review packet only after Dr. Ozkan chooses the route and clears outreach.",
            "",
            "No email, application, partner statement, official role statement, payment, terms acceptance, patient data use, clinical deployment, or clinical validation claim is made by this kit.",
            "",
            "## Runnable check",
            "",
            "```bash",
            "make turkiye_health_ai_safety_readiness_kit",
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
    print(f"modules={len(KIT_MODULES)}")


if __name__ == "__main__":
    main()
