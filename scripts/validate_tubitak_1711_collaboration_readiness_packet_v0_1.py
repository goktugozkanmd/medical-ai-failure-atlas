#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "tr-medai-safety-suite"
JSON_PATH = OUT_DIR / "tubitak_1711_collaboration_readiness_packet_v0_1.json"
MD_PATH = OUT_DIR / "TUBITAK_1711_COLLABORATION_READINESS_PACKET_V0_1.md"


REQUIRED_PHRASES = [
    "1711 collaboration readiness packet v0.1",
    "Official source boundaries",
    "15 June 2026",
    "16 June 2026",
    "18 September 2026",
    "14 September 2026",
    "PRODİS",
    "five priority areas",
    "Akıllı Üretim Sistemleri",
    "Akıllı Tarım Gıda ve Hayvancılık",
    "Finans Teknolojileri",
    "İklim Değişikliği ve Sürdürülebilirlik",
    "Akıllı Eğitim Teknolojileri",
    "Health is not listed",
    "customer organization",
    "technology provider",
    "experienced research laboratory or center",
    "TÜBİTAK Yapay Zekâ Enstitüsü",
    "no submission claim",
    "no application claim",
    "no funding claim",
    "no official endorsement claim",
    "no partner claim",
    "no health priority claim",
    "no route access claim",
    "no terms acceptance and no payment",
    "not clinical deployment",
    "not clinical validation",
    "Queue rows: 5",
    "Official call boundary rows: 1",
    "Consortium role rows: 1",
    "Priority area fit rows: 1",
    "Health AI assurance bridge rows: 1",
    "No submission gate rows: 1",
    "make tubitak_1711_readiness_packet",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "funding awarded",
    "officially endorsed",
    "partner secured",
    "health priority route",
    "route access granted",
    "terms accepted",
    "payment made",
    "patient data used",
    "clinically validated",
    "validated for clinical use",
]

REQUIRED_FLAGS = [
    "no_submission_claim",
    "no_application_claim",
    "no_funding_claim",
    "no_official_endorsement_claim",
    "no_partner_claim",
    "no_health_priority_claim",
    "no_route_access_claim",
    "no_terms_acceptance",
    "no_payment",
    "no_clinical_validation_claim",
    "no_clinical_deployment_claim",
    "no_patient_data_use",
]


def main() -> int:
    errors: list[str] = []
    if not JSON_PATH.exists():
        errors.append(f"Missing JSON: {JSON_PATH.relative_to(ROOT)}")
        payload = {}
    else:
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if not MD_PATH.exists():
        errors.append(f"Missing Markdown: {MD_PATH.relative_to(ROOT)}")
        text = ""
    else:
        text = MD_PATH.read_text(encoding="utf-8")

    if payload.get("queue_row_count") != 5:
        errors.append("queue row count must be 5")
    if payload.get("contains_patient_data") is not False:
        errors.append("contains_patient_data must be false")
    if payload.get("not_for_clinical_use") is not True:
        errors.append("not_for_clinical_use must be true")
    for flag in REQUIRED_FLAGS:
        if payload.get(flag) is not True:
            errors.append(f"{flag} must be true")

    boundaries = payload.get("official_source_boundaries", {})
    if boundaries.get("opening_date") != "15 June 2026":
        errors.append("opening date must be 15 June 2026")
    if boundaries.get("application_system") != "PRODİS":
        errors.append("application system must be PRODİS")
    if boundaries.get("health_listed_as_priority_area") is not False:
        errors.append("health_listed_as_priority_area must be false")
    if len(boundaries.get("priority_areas", [])) != 5:
        errors.append("there must be five priority areas")
    if boundaries.get("consortium_required") is not True:
        errors.append("consortium_required must be true")

    row_ids = [row.get("row_id") for row in payload.get("rows", [])]
    if row_ids != ["T1711Q001", "T1711Q002", "T1711Q003", "T1711Q004", "T1711Q005"]:
        errors.append("row IDs must be T1711Q001 through T1711Q005")

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing 1711 packet must not contain hyphen characters")

    if errors:
        print("FAIL 1711 collaboration readiness packet validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS 1711 collaboration readiness packet validation")
    print(f"file={MD_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
