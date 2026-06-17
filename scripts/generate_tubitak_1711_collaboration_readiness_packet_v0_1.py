#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "tr-medai-safety-suite"
JSON_PATH = OUT_DIR / "tubitak_1711_collaboration_readiness_packet_v0_1.json"
MD_PATH = OUT_DIR / "TUBITAK_1711_COLLABORATION_READINESS_PACKET_V0_1.md"

OFFICIAL_ANNOUNCEMENT_URL = "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi"
OFFICIAL_ANNOUNCEMENT_URL_VISIBLE = "https://tubitak.gov.tr/tr/duyuru/1711%2Dyapay%2Dzeka%2Dekosistem%2D2026%2Dyili%2Dcagrisi%2Dacildi"
OFFICIAL_CALL_TEXT_URL = "https://tubitak.gov.tr/sites/default/files/2026-06/1711_Yapay_Zeka_Ekosistem_Cagrisi_2026_Cagri_Metni.pdf"
OFFICIAL_CALL_TEXT_URL_VISIBLE = "https://tubitak.gov.tr/sites/default/files/2026%2D06/1711_Yapay_Zeka_Ekosistem_Cagrisi_2026_Cagri_Metni.pdf"


ROWS = [
    {
        "row_id": "T1711Q001",
        "lane": "official call boundary",
        "source_basis": "TÜBİTAK 2026 announcement",
        "readiness_action": "record that the fifth 1711 call opened on 15 June 2026",
        "blocked_claim": "submission claim",
        "next_public_action": "keep call boundary visible without submission language",
    },
    {
        "row_id": "T1711Q002",
        "lane": "consortium role map",
        "source_basis": "TÜBİTAK support page",
        "readiness_action": "map customer organization technology provider laboratory and institute roles",
        "blocked_claim": "partner claim",
        "next_public_action": "prepare role neutral collaboration checklist",
    },
    {
        "row_id": "T1711Q003",
        "lane": "priority area fit check",
        "source_basis": "TÜBİTAK 2026 priority list",
        "readiness_action": "record that health is not listed among the five stated 2026 priority areas",
        "blocked_claim": "health priority claim",
        "next_public_action": "keep health AI safety as readiness infrastructure only",
    },
    {
        "row_id": "T1711Q004",
        "lane": "health AI assurance bridge",
        "source_basis": "public assurance lab artifacts",
        "readiness_action": "map assurance cards source support and review gates to future collaboration preparation",
        "blocked_claim": "official endorsement",
        "next_public_action": "connect assurance lab files to collaboration packet",
    },
    {
        "row_id": "T1711Q005",
        "lane": "no submission release gate",
        "source_basis": "public external action policy",
        "readiness_action": "block any application claim funding claim payment terms action or route access claim",
        "blocked_claim": "funding claim",
        "next_public_action": "open a public issue that records packet completion only",
    },
]


FLAGS = {
    "contains_patient_data": False,
    "not_for_clinical_use": True,
    "no_submission_claim": True,
    "no_application_claim": True,
    "no_funding_claim": True,
    "no_official_endorsement_claim": True,
    "no_partner_claim": True,
    "no_health_priority_claim": True,
    "no_route_access_claim": True,
    "no_terms_acceptance": True,
    "no_payment": True,
    "no_clinical_validation_claim": True,
    "no_clinical_deployment_claim": True,
    "no_patient_data_use": True,
}


PRIORITY_AREAS = [
    "Akıllı Üretim Sistemleri",
    "Akıllı Tarım Gıda ve Hayvancılık",
    "Finans Teknolojileri",
    "İklim Değişikliği ve Sürdürülebilirlik",
    "Akıllı Eğitim Teknolojileri",
]


def build_payload() -> dict:
    return {
        "version": "tubitak_1711_collaboration_readiness_packet_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "official_announcement_url": OFFICIAL_ANNOUNCEMENT_URL,
        "official_call_text_url": OFFICIAL_CALL_TEXT_URL,
        "official_source_boundaries": {
            "call_name": "1711 Yapay Zekâ Ekosistem 2026 Yılı Çağrısı",
            "opening_date": "15 June 2026",
            "announcement_date": "16 June 2026",
            "application_system": "PRODİS",
            "application_window": "15 June 2026 to 18 September 2026",
            "pre_registration_deadline": "14 September 2026 17:30",
            "priority_areas": PRIORITY_AREAS,
            "health_listed_as_priority_area": False,
            "consortium_required": True,
            "customer_organization_required": True,
            "technology_provider_required": True,
            "experienced_research_laboratory_or_center_required": True,
            "tubitak_ai_institute_role_mentioned": True,
        },
        "queue_row_count": len(ROWS),
        "official_call_boundary_rows": 1,
        "consortium_role_rows": 1,
        "priority_area_fit_rows": 1,
        "health_ai_assurance_bridge_rows": 1,
        "no_submission_gate_rows": 1,
        **FLAGS,
        "rows": ROWS,
    }


def build_markdown(payload: dict) -> str:
    lines = [
        "# 1711 collaboration readiness packet v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This packet records preparation boundaries for a future Turkish health AI safety collaboration route around the TÜBİTAK 1711 Yapay Zekâ Ekosistem 2026 call.",
        "",
        "Official announcement source: `" + OFFICIAL_ANNOUNCEMENT_URL_VISIBLE + "`",
        "",
        "Official call text source: `" + OFFICIAL_CALL_TEXT_URL_VISIBLE + "`",
        "",
        "## Official source boundaries",
        "",
        "1. Official source says the fifth 1711 Yapay Zekâ Ekosistem call opened on 15 June 2026.",
        "2. Official source announcement date is 16 June 2026.",
        "3. Official source says 2026 applications are received through PRODİS.",
        "4. Official source says the application window is 15 June 2026 to 18 September 2026.",
        "5. Official source says pre registration must be completed by 14 September 2026 at 17:30.",
        "6. Official source lists five priority areas.",
        "7. The five stated priority areas are Akıllı Üretim Sistemleri, Akıllı Tarım Gıda ve Hayvancılık, Finans Teknolojileri, İklim Değişikliği ve Sürdürülebilirlik, and Akıllı Eğitim Teknolojileri.",
        "8. Health is not listed as one of the five stated 2026 priority areas in the official source.",
        "9. Official source describes a consortium model that brings together a customer organization, technology provider, experienced research laboratory or center, and TÜBİTAK Yapay Zekâ Enstitüsü role.",
        "",
        "## Public boundary",
        "",
        "1. This packet has no submission claim.",
        "2. This packet has no application claim.",
        "3. This packet has no funding claim.",
        "4. This packet has no official endorsement claim.",
        "5. This packet has no partner claim.",
        "6. This packet has no health priority claim.",
        "7. This packet has no route access claim.",
        "8. This packet has no terms acceptance and no payment.",
        "9. This packet has no patient data, not clinical deployment, and not clinical validation.",
        "",
        "## Queue summary",
        "",
        f"1. Queue rows: {payload['queue_row_count']}",
        f"2. Official call boundary rows: {payload['official_call_boundary_rows']}",
        f"3. Consortium role rows: {payload['consortium_role_rows']}",
        f"4. Priority area fit rows: {payload['priority_area_fit_rows']}",
        f"5. Health AI assurance bridge rows: {payload['health_ai_assurance_bridge_rows']}",
        f"6. No submission gate rows: {payload['no_submission_gate_rows']}",
        "",
        "## Readiness rows",
        "",
    ]
    for index, row in enumerate(payload["rows"], start=1):
        lines.extend(
            [
                f"### {index}. {row['row_id']}",
                "",
                f"Lane: {row['lane']}",
                "",
                f"Source basis: {row['source_basis']}",
                "",
                f"Readiness action: {row['readiness_action']}",
                "",
                f"Blocked claim: {row['blocked_claim']}",
                "",
                f"Next public action: {row['next_public_action']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Runnable check",
            "",
            "```bash",
            "make tubitak_1711_readiness_packet",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MD_PATH.write_text(build_markdown(payload), encoding="utf-8")
    print(f"wrote {MD_PATH.relative_to(ROOT)}")
    print(f"wrote {JSON_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
