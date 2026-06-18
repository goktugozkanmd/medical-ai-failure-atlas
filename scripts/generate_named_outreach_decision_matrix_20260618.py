#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "NAMED_OUTREACH_DECISION_MATRIX_20260618.md"
DATA = ROOT / "docs" / "named_outreach_decision_matrix_20260618.json"


ROUTES = [
    {
        "route_id": "NODM001",
        "name": "TÜYZE institutional readiness route",
        "source": "Türkiye Sağlık Veri Araştırmaları ve Yapay Zeka Uygulamaları Enstitüsü",
        "url": "https://tuyze.tuseb.gov.tr/",
        "fit": "high",
        "live_signal": "TÜYZE lists health data, medical decision support, medical device technology units, health data and AI boards, and recent health AI activity.",
        "prepared_package": "Türkiye Health AI Safety Readiness Kit",
        "decision_needed": "Choose whether to prepare a named TÜYZE readiness outreach draft for Dr. Ozkan review.",
        "blocker": "No email is sent without clearance, no official role is claimed, no partner claim is made, and no institutional commitment is implied.",
    },
    {
        "route_id": "NODM002",
        "name": "TEKNOFEST contestant safety route",
        "source": "TEKNOFEST Sağlıkta Yapay Zeka Yarışması",
        "url": "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
        "fit": "high and time sensitive",
        "live_signal": "The public competition page lists a university and above task on predicting whether genetic variants are pathogenic or benign and a project detail report deadline of 29 June 2026 at 17:00.",
        "prepared_package": "TEKNOFEST Health AI Safety Addendum",
        "decision_needed": "Choose public share, mentor route, or team route before any outward action.",
        "blocker": "No submission is made, no official TEKNOFEST endorsement is claimed, no team relationship is claimed, and no route access is implied.",
    },
    {
        "route_id": "NODM003",
        "name": "TÜBİTAK 1711 adjacent AI assurance route",
        "source": "TÜBİTAK 1711 Yapay Zeka Ekosistem 2026 call announcement",
        "url": "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
        "fit": "medium because direct health fit is weak",
        "live_signal": "The public call page lists priority areas outside direct health AI and requires a consortium route with a customer organization, technology provider, and research lab.",
        "prepared_package": "TÜBİTAK 1711 AI Assurance Sidecar",
        "decision_needed": "Choose whether to scout an eligible adjacent consortium path despite weak direct health fit.",
        "blocker": "No application is submitted, no intent declaration is made, no partner commitment is made, no budget is stated, and no terms are accepted.",
    },
    {
        "route_id": "NODM004",
        "name": "CHAI applied model card companion route",
        "source": "Coalition for Health AI Applied Model Card",
        "url": "https://www.chai.org/workgroup/applied-model",
        "fit": "medium global credibility route",
        "live_signal": "The public CHAI page describes an applied model card for health AI use cases and links current draft documentation and template outputs.",
        "prepared_package": "SourceCheckup Medical source support companion note",
        "decision_needed": "Choose whether to build a public companion note that maps SourceCheckup evidence fields to applied model card transparency fields.",
        "blocker": "No CHAI affiliation, endorsement, registry claim, membership claim, submission, or partner commitment is made.",
    },
    {
        "route_id": "NODM005",
        "name": "MedHELM benchmark boundary companion route",
        "source": "MedHELM public benchmark pages",
        "url": "https://medhelm.org/",
        "fit": "medium global benchmark literacy route",
        "live_signal": "Public MedHELM materials describe medical task evaluation infrastructure, which creates a visible need for benchmark misuse warnings and boundary notes.",
        "prepared_package": "Benchmark misuse boundary companion note",
        "decision_needed": "Choose whether to publish a companion note that warns against score ranking misuse, clinical deployment claims, and source support overclaims.",
        "blocker": "No compatibility claim, benchmark score claim, clinical validation claim, deployment claim, or endorsement claim is made.",
    },
]


BOUNDARIES = [
    "No email is sent.",
    "No submission is made.",
    "No application is submitted.",
    "No partner commitment is made.",
    "No official role is claimed.",
    "No endorsement is claimed.",
    "No payment is made.",
    "No terms are accepted.",
    "No patient data is used.",
    "No clinical deployment is claimed.",
    "No clinical validation is claimed.",
]


def write_json() -> None:
    payload = {
        "artifact": "named_outreach_decision_matrix_20260618",
        "status": "field readiness public preview",
        "route_count": len(ROUTES),
        "routes": ROUTES,
        "boundaries": BOUNDARIES,
        "requires_goktug_clearance_before_outreach": True,
        "contains_patient_data": False,
        "claims_submission": False,
        "claims_partner": False,
        "claims_official_role": False,
        "claims_endorsement": False,
        "claims_clinical_validation": False,
        "claims_clinical_deployment": False,
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines = [
        "# Named outreach decision matrix",
        "",
        "Date: 2026 06 18",
        "",
        "Status: field readiness public preview.",
        "",
        "Purpose: turn live national and global medical AI opportunity signals into named decision routes without pretending that outreach, submission, partnership, endorsement, or clinical validation has happened.",
        "",
        "## Route matrix",
        "",
    ]
    for route in ROUTES:
        lines.extend(
            [
                f"### {route['route_id']}: {route['name']}",
                "",
                f"Source: {route['source']}",
                "",
                f"Official or public source: {route['url']}",
                "",
                f"Fit: {route['fit']}",
                "",
                f"Live signal: {route['live_signal']}",
                "",
                f"Prepared package: {route['prepared_package']}",
                "",
                f"Decision needed: {route['decision_needed']}",
                "",
                f"Blocker: {route['blocker']}",
                "",
            ]
        )
    lines.extend(["## Boundary", ""])
    lines.extend(f"{index}. {boundary}" for index, boundary in enumerate(BOUNDARIES, start=1))
    lines.extend(
        [
            "",
            "## Immediate review packet",
            "",
            "The next useful field action is a three option review packet for Dr. Ozkan: TÜYZE readiness outreach draft, TEKNOFEST public share draft, and TÜBİTAK 1711 consortium scouting brief. Each remains blocked before send until explicit clearance.",
            "",
            "## Runnable check",
            "",
            "```bash",
            "make named_outreach_decision_matrix",
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
    print(f"routes={len(ROUTES)}")


if __name__ == "__main__":
    main()
