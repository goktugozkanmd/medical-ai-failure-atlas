#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "tr-medai-safety-suite"
JSON_PATH = OUT_DIR / "bilge_readiness_queue_v0_1.json"
MD_PATH = OUT_DIR / "BILGE_READINESS_QUEUE_V0_1.md"


ROWS = [
    {
        "queue_id": "BILGEQ001",
        "lane": "official source boundary",
        "source_basis": "official BİLGE page",
        "readiness_action": "record source boundaries without claiming model access",
        "blocked_claim": "official endorsement",
        "next_public_action": "keep source boundary visible in readiness queue",
    },
    {
        "queue_id": "BILGEQ002",
        "lane": "no access gate",
        "source_basis": "access state not established",
        "readiness_action": "keep all model evaluation pending until access terms and cost state are explicit",
        "blocked_claim": "model score",
        "next_public_action": "prepare disabled run plan only after endpoint terms are clear",
    },
    {
        "queue_id": "BILGEQ003",
        "lane": "Turkish clinical risk mapping",
        "source_basis": "TR MedLLM risk axis map",
        "readiness_action": "map future BİLGE review to Turkish clinical risk axes without running the model",
        "blocked_claim": "model safety proof",
        "next_public_action": "reuse synthetic risk rows for future review design",
    },
    {
        "queue_id": "BILGEQ004",
        "lane": "SourceCheckup Turkish institutional wording",
        "source_basis": "SourceCheckup claim discipline",
        "readiness_action": "prepare Turkish official claim discipline examples for future source review",
        "blocked_claim": "benchmark compatibility",
        "next_public_action": "connect institutional wording checks to SourceCheckup rows",
    },
    {
        "queue_id": "BILGEQ005",
        "lane": "1711 collaboration readiness bridge",
        "source_basis": "public collaboration readiness route",
        "readiness_action": "connect future collaboration packet without application or endorsement claim",
        "blocked_claim": "sandbox access",
        "next_public_action": "build 1711 collaboration readiness packet with no submission claim",
    },
]


FLAGS = {
    "contains_patient_data": False,
    "not_for_clinical_use": True,
    "no_model_access_claim": True,
    "no_model_score_claim": True,
    "no_model_safety_claim": True,
    "no_model_ranking": True,
    "no_clinical_validation_claim": True,
    "no_clinical_deployment_claim": True,
    "no_official_endorsement_claim": True,
    "no_sandbox_access_claim": True,
    "no_benchmark_compatibility_claim": True,
}


def build_payload() -> dict:
    return {
        "version": "bilge_readiness_queue_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "official_source_url": "https://bilge.tubitak.gov.tr/",
        "source_claim_support": "official BİLGE page",
        "queue_row_count": len(ROWS),
        "official_source_rows": 1,
        "no_access_gate_rows": 1,
        "turkish_clinical_risk_mapping_rows": 1,
        "sourcecheckup_turkish_institutional_wording_rows": 1,
        "collaboration_readiness_bridge_rows": 1,
        "official_source_boundaries": {
            "developer": "TÜBİTAK BİLGEM",
            "model_family": "BİLGE Turkish large language model family",
            "model_sizes": ["1B", "9B", "27B", "122B"],
            "health_domain_mentioned": True,
        },
        **FLAGS,
        "rows": ROWS,
    }


def build_markdown(payload: dict) -> str:
    lines = [
        "# BİLGE readiness queue v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This readiness queue records preparation steps for future Turkish medical language model evaluation around BİLGE.",
        "",
        "Official source: `https://bilge.tubitak.gov.tr/`",
        "",
        "## Verified official source boundaries",
        "",
        "1. Official source says BİLGE is a Turkish large language model family developed by TÜBİTAK BİLGEM.",
        "2. Official source lists 1B, 9B, 27B, and 122B model sizes.",
        "3. Official source includes health among possible ecosystem domains.",
        "4. This queue has no model access claim, no model score claim, no model safety claim, no model ranking, no benchmark compatibility claim, not clinical deployment, not clinical validation, not official endorsement, and not sandbox access.",
        "",
        "## Queue summary",
        "",
        f"1. Queue rows: {payload['queue_row_count']}",
        f"2. Official source rows: {payload['official_source_rows']}",
        f"3. No access gate rows: {payload['no_access_gate_rows']}",
        f"4. Turkish clinical risk mapping rows: {payload['turkish_clinical_risk_mapping_rows']}",
        f"5. SourceCheckup Turkish institutional wording rows: {payload['sourcecheckup_turkish_institutional_wording_rows']}",
        f"6. Collaboration readiness bridge rows: {payload['collaboration_readiness_bridge_rows']}",
        "",
        "## Readiness rows",
        "",
    ]
    for index, row in enumerate(payload["rows"], start=1):
        lines.extend(
            [
                f"### {index}. {row['queue_id']}",
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
            "make bilge_readiness_queue",
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
