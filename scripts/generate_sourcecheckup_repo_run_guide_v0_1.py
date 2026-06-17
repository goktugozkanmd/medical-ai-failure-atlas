#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_MD = ROOT / "docs" / "sourcecheckup" / "SOURCECHECKUP_REPO_RUN_GUIDE_V0_1.md"
OUTPUT_JSON = ROOT / "docs" / "sourcecheckup" / "sourcecheckup_repo_run_guide_v0_1.json"

RUN_ROWS = [
    {
        "row_id": "SCRUN001",
        "step": "basic source scan",
        "command": "make sourcecheckup",
        "checks": "seed examples and report generation",
    },
    {
        "row_id": "SCRUN002",
        "step": "expanded example scan",
        "command": "make sourcecheckup_v02",
        "checks": "ten public source surface examples",
    },
    {
        "row_id": "SCRUN003",
        "step": "review queue check",
        "command": "make source_claim_queue",
        "checks": "twelve source claim review rows",
    },
    {
        "row_id": "SCRUN004",
        "step": "expansion dashboard check",
        "command": "make sourcecheckup_expansion_dashboard",
        "checks": "public expansion dashboard and queue surface",
    },
    {
        "row_id": "SCRUN005",
        "step": "institutional wording check",
        "command": "make sourcecheckup_turkish_institutional_wording",
        "checks": "five Turkish institutional wording examples",
    },
    {
        "row_id": "SCRUN006",
        "step": "repo doctor check",
        "command": "make sourcecheckup_repo_run_guide",
        "checks": "required files and row counts",
    },
]


def main() -> None:
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "sourcecheckup_repo_run_guide_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "row_count": len(RUN_ROWS),
        "contains_patient_data": False,
        "not_for_clinical_use": True,
        "no_external_calls": True,
        "no_model_calls": True,
        "no_source_truth_certification": True,
        "rows": RUN_ROWS,
    }

    lines: list[str] = [
        "# SourceCheckup repo run guide v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This guide gives contributors one practical route for running the SourceCheckup Medical surfaces from this repository.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not source truth certification, not a model safety claim, not a model ranking, not a benchmark compatibility claim, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Run guide rows: {len(RUN_ROWS)}",
        "",
        "Doctor output: `docs/sourcecheckup/sourcecheckup_repo_doctor_v0_1.json`",
        "",
        "Guide JSON: `docs/sourcecheckup/sourcecheckup_repo_run_guide_v0_1.json`",
        "",
        "Runnable target: `make sourcecheckup_repo_run_guide`",
        "",
        "## Recommended path",
        "",
    ]
    for index, row in enumerate(RUN_ROWS, start=1):
        lines.extend(
            [
                f"{index}. `{row['command']}`",
                "",
                f"Check: {row['checks']}.",
                "",
            ]
        )

    lines.extend(["## Run rows", ""])
    for row in RUN_ROWS:
        lines.extend(
            [
                f"### {row['row_id']}: {row['step']}",
                "",
                f"Command: `{row['command']}`",
                "",
                f"Checks: {row['checks']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. Patient data is not used.",
            "2. External calls are not required.",
            "3. Model calls are not required.",
            "4. Passing local SourceCheckup does not certify a medical source.",
            "5. Passing local SourceCheckup does not validate clinical use.",
            "6. Passing local SourceCheckup does not create benchmark compatibility.",
            "",
            "## Public files",
            "",
            "1. Run guide: `docs/sourcecheckup/SOURCECHECKUP_REPO_RUN_GUIDE_V0_1.md`",
            "2. Run guide JSON: `docs/sourcecheckup/sourcecheckup_repo_run_guide_v0_1.json`",
            "3. Doctor JSON: `docs/sourcecheckup/sourcecheckup_repo_doctor_v0_1.json`",
            "4. Generator: `scripts/generate_sourcecheckup_repo_run_guide_v0_1.py`",
            "5. Doctor: `scripts/sourcecheckup_repo_doctor_v0_1.py`",
            "6. Validator: `scripts/validate_sourcecheckup_repo_run_guide_v0_1.py`",
            "7. Runnable target: `make sourcecheckup_repo_run_guide`",
            "",
        ]
    )

    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_MD.relative_to(ROOT)}")
    print(f"wrote {OUTPUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
