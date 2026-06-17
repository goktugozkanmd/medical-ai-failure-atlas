#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_MD = ROOT / "docs" / "sourcecheckup" / "SOURCECHECKUP_TURKISH_INSTITUTIONAL_WORDING_EXAMPLES_V0_1.md"
OUTPUT_JSON = ROOT / "docs" / "sourcecheckup" / "sourcecheckup_turkish_institutional_wording_examples_v0_1.json"


ROWS = [
    {
        "row_id": "STIWE001",
        "institutional_surface": "ministry wording",
        "synthetic_risky_wording": "This work is aligned with national health AI priorities.",
        "blocked_claim": "official endorsement",
        "safe_public_wording": "This public preview studies health AI safety questions and does not claim a Ministry role or endorsement.",
        "sourcecheckup_action": "replace alignment language with scope language",
        "review_lane": "institutional wording review",
    },
    {
        "row_id": "STIWE002",
        "institutional_surface": "TÜYZE wording",
        "synthetic_risky_wording": "The project is ready for a national AI ecosystem route.",
        "blocked_claim": "route access",
        "safe_public_wording": "The project prepares public review artifacts that could support a future route decision after verified clearance.",
        "sourcecheckup_action": "separate readiness from access",
        "review_lane": "route wording review",
    },
    {
        "row_id": "STIWE003",
        "institutional_surface": "TÜBİTAK wording",
        "synthetic_risky_wording": "This packet supports a TÜBİTAK application.",
        "blocked_claim": "submission claim",
        "safe_public_wording": "This packet records source boundaries and does not claim application submission.",
        "sourcecheckup_action": "replace support claim with boundary record",
        "review_lane": "submission wording review",
    },
    {
        "row_id": "STIWE004",
        "institutional_surface": "hospital wording",
        "synthetic_risky_wording": "The examples are ready for hospital workflow testing.",
        "blocked_claim": "clinical deployment",
        "safe_public_wording": "The examples are synthetic review material and are not for hospital workflow deployment.",
        "sourcecheckup_action": "block workflow testing language",
        "review_lane": "clinical deployment wording review",
    },
    {
        "row_id": "STIWE005",
        "institutional_surface": "university lab wording",
        "synthetic_risky_wording": "A university lab can validate this safety benchmark.",
        "blocked_claim": "validation claim",
        "safe_public_wording": "A future reviewer could inspect the method, but this public preview does not claim validation.",
        "sourcecheckup_action": "replace validation language with review language",
        "review_lane": "validation wording review",
    },
]


def main() -> None:
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "sourcecheckup_turkish_institutional_wording_examples_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "row_count": len(ROWS),
        "contains_patient_data": False,
        "not_for_clinical_use": True,
        "no_official_endorsement_claim": True,
        "no_route_access_claim": True,
        "no_submission_claim": True,
        "no_clinical_deployment_claim": True,
        "no_clinical_validation_claim": True,
        "rows": ROWS,
    }

    blocked_claims = sorted({row["blocked_claim"] for row in ROWS})
    review_lanes = sorted({row["review_lane"] for row in ROWS})

    lines: list[str] = [
        "# SourceCheckup Turkish institutional wording examples v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "These examples help reviewers separate institutional wording from unsupported endorsement, route access, submission, deployment, and validation claims.",
        "",
        "They use synthetic wording examples only. They are not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, not route access, not a submission claim, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Turkish institutional wording examples: {len(ROWS)}",
        "",
        f"Blocked claim types: {len(blocked_claims)}",
        "",
        f"Reviewer lanes: {len(review_lanes)}",
        "",
        "Linked SourceCheckup route: `SCQ_008`",
        "",
        "Linked assurance route: `ARG006`",
        "",
        "Linked public packet: `docs/tr%2Dmedai%2Dsafety%2Dsuite/TUBITAK_1711_COLLABORATION_READINESS_PACKET_V0_1.md`",
        "",
        "## Blocked claim coverage",
        "",
    ]
    for claim in blocked_claims:
        lines.extend([f"{claim}: 1", ""])

    lines.extend(["## Examples", ""])
    for row in ROWS:
        lines.extend(
            [
                f"### {row['row_id']}: {row['institutional_surface']}",
                "",
                f"Synthetic risky wording: {row['synthetic_risky_wording']}",
                "",
                f"Blocked claim: {row['blocked_claim']}",
                "",
                f"Safe public wording: {row['safe_public_wording']}",
                "",
                f"SourceCheckup action: {row['sourcecheckup_action']}",
                "",
                f"Review lane: {row['review_lane']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Review use",
            "",
            "1. Use these examples before public text names a Ministry, TÜYZE, TÜBİTAK, hospital, university lab, benchmark, or regulator.",
            "2. Replace alignment language with source boundary language unless there is verified external permission.",
            "3. Replace ready for route language with preparation language unless route access is verified.",
            "4. Replace application language with packet or source boundary language unless submission is actually executed and cleared.",
            "5. Replace validation language with review language unless an external validation record exists.",
            "",
            "## Boundary checks",
            "",
            "1. Every example is synthetic.",
            "2. Patient data is not used.",
            "3. No institutional endorsement is claimed.",
            "4. No route access is claimed.",
            "5. No submission is claimed.",
            "6. No clinical deployment is claimed.",
            "7. No clinical validation is claimed.",
            "",
            "## Public files",
            "",
            "1. Generated examples: `docs/sourcecheckup/SOURCECHECKUP_TURKISH_INSTITUTIONAL_WORDING_EXAMPLES_V0_1.md`",
            "2. Generated JSON: `docs/sourcecheckup/sourcecheckup_turkish_institutional_wording_examples_v0_1.json`",
            "3. Generator: `scripts/generate_sourcecheckup_turkish_institutional_wording_examples_v0_1.py`",
            "4. Validator: `scripts/validate_sourcecheckup_turkish_institutional_wording_examples_v0_1.py`",
            "5. Runnable target: `make sourcecheckup_turkish_institutional_wording`",
            "",
        ]
    )

    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_MD.relative_to(ROOT)}")
    print(f"wrote {OUTPUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
