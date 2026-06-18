#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TEKNOFEST_HEALTH_AI_SAFETY_ADDENDUM_20260618.md"
DATA = ROOT / "docs" / "teknofest_health_ai_safety_addendum_20260618.json"


SOURCE_SIGNALS = [
    {
        "source_id": "THASA001",
        "source": "TEKNOFEST Sağlıkta Yapay Zeka public page",
        "url": "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
        "checked_fact": "The public page lists a 2026 health AI competition and says the competition aims to produce solutions for health problems and increase knowledge and trained human capacity.",
        "field_read": "Contestant facing safety guidance can create timely field value.",
    },
    {
        "source_id": "THASA002",
        "source": "TEKNOFEST Sağlıkta Yapay Zeka public page",
        "url": "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
        "checked_fact": "The university and above category focuses on predicting whether genetic variants are pathogenic or benign.",
        "field_read": "Data quality, label uncertainty, and clinical claim boundaries are directly relevant.",
    },
    {
        "source_id": "THASA003",
        "source": "TEKNOFEST Sağlıkta Yapay Zeka public page",
        "url": "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
        "checked_fact": "The project detail report deadline is listed as 29 June 2026 at 17:00.",
        "field_read": "A public safety addendum is time sensitive before the detail report deadline.",
    },
]


ADDENDUM_CHECKS = [
    {
        "check_id": "THASC001",
        "name": "Health claim boundary",
        "question": "Does the report avoid clinical deployment, diagnosis, treatment, or validation claims?",
        "why_it_matters": "A competition model should not be framed as ready for care.",
    },
    {
        "check_id": "THASC002",
        "name": "Label uncertainty",
        "question": "Does the report explain uncertain, conflicting, or evolving labels?",
        "why_it_matters": "Genetic variant classification can depend on evidence context and update over time.",
    },
    {
        "check_id": "THASC003",
        "name": "Data leakage",
        "question": "Does the report describe how leakage between training and evaluation data was checked?",
        "why_it_matters": "Leakage can create false confidence and inflated performance.",
    },
    {
        "check_id": "THASC004",
        "name": "Population and context limits",
        "question": "Does the report state where the data may not represent the intended use setting?",
        "why_it_matters": "A model can fail outside the data distribution that shaped it.",
    },
    {
        "check_id": "THASC005",
        "name": "Source support",
        "question": "Does each medical claim have source support, not only a citation nearby?",
        "why_it_matters": "Citation presence is not the same as support for a specific claim.",
    },
    {
        "check_id": "THASC006",
        "name": "Human review handoff",
        "question": "Does the report define what a clinician, geneticist, or domain reviewer would need to check next?",
        "why_it_matters": "A safe report shows the next human review step instead of implying autonomy.",
    },
    {
        "check_id": "THASC007",
        "name": "Failure examples",
        "question": "Does the report include examples where the system should abstain, ask for more context, or flag uncertainty?",
        "why_it_matters": "Failure modes are more useful for safety than only success examples.",
    },
]


BOUNDARIES = [
    "No official TEKNOFEST endorsement claim.",
    "No submission claim.",
    "No clinical deployment claim.",
    "No clinical validation claim.",
    "No patient data included.",
    "No diagnosis or treatment advice.",
    "No model ranking.",
    "No score certification.",
    "No partner claim.",
    "No route access claim.",
]


def write_json() -> None:
    payload = {
        "artifact": "teknofest_health_ai_safety_addendum_20260618",
        "status": "field readiness public preview",
        "date": "2026 06 18",
        "source_signals": SOURCE_SIGNALS,
        "checks": ADDENDUM_CHECKS,
        "check_count": len(ADDENDUM_CHECKS),
        "boundaries": BOUNDARIES,
        "contains_patient_data": False,
        "claims_official_endorsement": False,
        "claims_submission": False,
        "claims_partner": False,
        "claims_clinical_validation": False,
        "claims_clinical_deployment": False,
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines: list[str] = [
        "# TEKNOFEST Health AI Safety Addendum",
        "",
        "Date: 2026 06 18",
        "",
        "Status: field readiness public preview.",
        "",
        "Purpose: give health AI teams a short safety addendum they can use while preparing project detail reports, especially for data quality, label uncertainty, source support, and claim boundaries.",
        "",
        "This is not an official TEKNOFEST document, not a submission, not a partner claim, and not an endorsement claim.",
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
    lines.extend(["## Safety addendum checks", ""])
    for check in ADDENDUM_CHECKS:
        lines.extend(
            [
                f"### {check['check_id']}: {check['name']}",
                "",
                f"Question: {check['question']}",
                "",
                f"Why it matters: {check['why_it_matters']}",
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
            "Publish as a public safety addendum and use it as a conversation starter for health AI teams only after Dr. Ozkan clears the outreach route.",
            "",
            "No email, application, official route, partner claim, payment, terms acceptance, clinical deployment, clinical validation, or official endorsement is made by this addendum.",
            "",
            "## Runnable check",
            "",
            "```bash",
            "make teknofest_health_ai_safety_addendum",
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
    print(f"checks={len(ADDENDUM_CHECKS)}")


if __name__ == "__main__":
    main()
