#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "sourcecheckup" / "build" / "sourcecheckup_medical_cli_report_20260708.json"
REPORT_MD = ROOT / "sourcecheckup" / "build" / "sourcecheckup_medical_cli_report_20260708.md"
JSON_PATH = ROOT / "docs" / "sourcecheckup_medical_cli_report_20260708.json"
MD_PATH = ROOT / "docs" / "SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md"


SAMPLE_PROMPT = "Synthetic medical AI answer source support review."
SAMPLE_ANSWER = (
    "The answer cites DOI 10.5555/sourcecheckup.synthetic.cli and says guidelines recommend "
    "remote medication dose adjustment. This is a synthetic parser and review example."
)
SAMPLE_SOURCES = [
    {
        "source_id": "S1",
        "type": "doi",
        "value": "10.5555/sourcecheckup.synthetic.cli",
        "verification_status": "format_checked_only",
        "supports_claim_ids": ["C1"],
    }
]
SAMPLE_CLAIMS = [
    {
        "claim_id": "C1",
        "claim_type": "guideline",
        "text": "Guidelines recommend remote medication dose adjustment.",
        "source_ids": ["S1"],
        "central_to_answer": True,
    }
]


def main() -> int:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "scripts/sourcecheckup_medical.py",
        "report",
        "--answer-id",
        "SOURCECHECKUP_CLI_P3_SMOKE",
        "--prompt",
        SAMPLE_PROMPT,
        "--answer",
        SAMPLE_ANSWER,
        "--declared-sources-json",
        json.dumps(SAMPLE_SOURCES, ensure_ascii=True, sort_keys=True),
        "--declared-claims-json",
        json.dumps(SAMPLE_CLAIMS, ensure_ascii=True, sort_keys=True),
        "--out-json",
        str(REPORT_JSON),
        "--out-md",
        str(REPORT_MD),
    ]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        print(completed.stdout, end="")
        print(completed.stderr, end="", file=sys.stderr)
        return completed.returncode

    report = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    item = report["items"][0]
    manifest = {
        "artifact_id": "sourcecheckup_medical_cli_report_20260708",
        "status": "local_cli_report_ready",
        "created_date": "2026-07-08",
        "phase": "P3",
        "roadmap": "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
        "product_name": "Clinical AI Safety Ops / Health AI Assurance Kit",
        "sourcecheckup_version": report["sourcecheckup_version"],
        "report_schema": report["schema_version"],
        "report_mode": report["report_mode"],
        "command": "python3 scripts/sourcecheckup_medical.py report",
        "sample_report_json": str(REPORT_JSON.relative_to(ROOT)),
        "sample_report_md": str(REPORT_MD.relative_to(ROOT)),
        "features": [
            "single_answer_cli_report",
            "manual_answer_or_answer_file_input",
            "optional_declared_sources_json",
            "optional_declared_claims_json",
            "source_presence_vs_exact_claim_support_boundary",
            "markdown_and_json_output",
        ],
        "sample_result": {
            "answer_id": item["answer_id"],
            "external_use_gate": item["external_use_gate"],
            "source_claims_present": item["source_claims_present"],
            "declared_source_count": item["declared_source_count"],
            "declared_claim_count": item["declared_claim_count"],
            "verification_queue_count": len(item["verification_queue"]),
            "flag_codes": [flag["code"] for flag in item["flags"]],
        },
        "external_action_allowed": False,
        "provider_api_call_allowed": False,
        "automation_started": False,
        "new_cases_added": False,
        "agent_selected_physicians": False,
        "contains_patient_data": False,
        "no_clinical_validation_claim": True,
        "no_source_truth_certification_claim": True,
        "no_model_ranking": True,
        "no_regulatory_compliance_claim": True,
        "no_official_compatibility_claim": True,
        "blocked_actions": [
            "send_external_email_or_post_without_user_approval",
            "start_provider_api_calls_without_user_approval",
            "add_new_cases_without_user_approval",
            "claim_clinical_validation",
            "claim_source_truth_certification",
            "claim_regulatory_compliance",
            "claim_official_endorsement_or_compatibility",
            "rank_models_as_winners",
            "select_or_contact_physicians_by_agent",
        ],
        "next_safe_actions": [
            "connect this report output to a kit level assurance card",
            "keep external source verification separate from local format checks",
            "keep physician selection outside the agent scope",
        ],
    }
    JSON_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(manifest), encoding="utf-8")
    print(completed.stdout, end="")
    print(f"Wrote {JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")
    print(f"gate={item['external_use_gate']}")
    print(f"verification_queue_count={len(item['verification_queue'])}")
    return 0


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# SourceCheckup Medical CLI Report",
        "",
        "Date: 2026 07 08",
        "",
        "Status: local CLI report ready.",
        "",
        "Roadmap phase: P3 SourceCheckup Medical CLI.",
        "",
        "## Product Surface",
        "",
        "This adds a runnable single answer CLI report for medical AI source support review.",
        "",
        f"Command: `{manifest['command']}`.",
        "",
        f"Report schema: `{manifest['report_schema']}`.",
        "",
        "The report separates source presence from exact claim support. A locator, URL, DOI, PMID, guideline phrase, or policy phrase does not clear a medical claim by itself.",
        "",
        "## Boundary",
        "",
        "No external send, no provider API call, no automation start, no new case addition, no patient data, no physician selection, no clinical validation claim, no source truth certification claim, no regulatory compliance claim, no official compatibility claim, and no model ranking.",
        "",
        "## Features",
        "",
    ]
    for feature in manifest["features"]:
        lines.append(f"- `{feature}`.")
    sample = manifest["sample_result"]
    lines.extend(
        [
            "",
            "## Sample Smoke",
            "",
            f"- Answer id: `{sample['answer_id']}`.",
            f"- External use gate: `{sample['external_use_gate']}`.",
            f"- Source claims present: `{str(sample['source_claims_present']).lower()}`.",
            f"- Declared sources: {sample['declared_source_count']}.",
            f"- Declared claims: {sample['declared_claim_count']}.",
            f"- Verification queue count: {sample['verification_queue_count']}.",
            "",
            "## Outputs",
            "",
            f"- JSON report: `{manifest['sample_report_json']}`.",
            f"- Markdown report: `{manifest['sample_report_md']}`.",
            "",
            "## Next",
            "",
            "1. Connect this report output to the kit level assurance card.",
            "2. Keep public source support claims blocked until exact source support is checked.",
            "",
            "## Validation",
            "",
            "Run:",
            "",
            "```bash",
            "make sourcecheckup_medical_cli_report_20260708",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
