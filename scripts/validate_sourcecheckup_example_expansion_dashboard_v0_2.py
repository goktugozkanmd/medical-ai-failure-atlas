#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SURFACE_EXAMPLES = ROOT / "sourcecheckup" / "examples" / "source_surface_examples_v0_2.jsonl"
CONTRIBUTION_EXAMPLES = ROOT / "sourcecheckup" / "examples" / "sourcecheckup_contribution_examples_v0_2.jsonl"
REVIEW_QUEUE = ROOT / "sourcecheckup" / "review_queue" / "source_claim_review_queue_v0_1.jsonl"
DASHBOARD = ROOT / "sourcecheckup" / "build" / "source_claim_example_expansion_v0_2.md"

REQUIRED_PHRASES = [
    "SourceCheckup source claim example expansion v0.2",
    "Status: generated public preview.",
    "SourceCheckup v0.2 answer examples: 10",
    "SourceCheckup contributor examples: 8",
    "Source claim review queue rows: 12",
    "Contribution source surfaces represented: 7",
    "Review queue source surfaces represented: 8",
    "Review queue release gates represented: 3",
    "SourceCheckup report verification queue items: 16",
    "blocked_missing_source_support: 6",
    "blocked_pending_source_verification: 4",
    "sc_v02_tr_medllm_dosing_006",
    "sc_v02_benchmark_compatibility_007",
    "sc_v02_policy_sandbox_008",
    "sc_v02_data_provenance_009",
    "sc_v02_clean_uncertainty_010",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not source truth certification",
    "not an official endorsement",
    "Every example is synthetic.",
    "External action readiness is false for review queue rows.",
    "Outward use is not allowed until maintainer review",
    "SourceCheckup TR MedLLM assurance routing map",
    "docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md",
    "source review worksheets",
    "docs/SOURCE_REVIEW_WORKSHEETS_V0_1.md",
    "red flag source locator review",
    "docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "officially endorsed",
    "regulatory approved",
    "sandbox access granted",
    "patient data used",
    "source proves",
    "model is safe",
    "best model",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path.relative_to(ROOT)}:{line_number}: invalid JSON: {exc}") from exc
        rows.append(row)
    return rows


def main() -> int:
    errors: list[str] = []
    surface_rows = load_jsonl(SURFACE_EXAMPLES)
    contribution_rows = load_jsonl(CONTRIBUTION_EXAMPLES)
    queue_rows = load_jsonl(REVIEW_QUEUE)

    if len(surface_rows) != 10:
        errors.append(f"Expected 10 SourceCheckup answer examples, found {len(surface_rows)}")
    if len(contribution_rows) != 8:
        errors.append(f"Expected 8 contribution examples, found {len(contribution_rows)}")
    if len(queue_rows) != 12:
        errors.append(f"Expected 12 queue rows, found {len(queue_rows)}")

    contribution_surfaces = {str(row.get("source_surface")) for row in contribution_rows}
    queue_surfaces = {str(row.get("source_surface")) for row in queue_rows}
    queue_gates = {str(row.get("release_gate")) for row in queue_rows}
    for required in {"doi", "pmid", "url", "guideline", "policy", "broad_source_language", "none"}:
        if required not in contribution_surfaces:
            errors.append(f"Contribution examples missing surface: {required}")
    for required in {"blocked_missing_source_support", "blocked_pending_source_verification", "pass_local_sourcecheckup"}:
        if required not in queue_gates:
            errors.append(f"Queue missing release gate: {required}")
    for row in queue_rows:
        if row.get("patient_data") is not False:
            errors.append(f"{row.get('queue_id')}: patient_data must be false")
        if row.get("external_action_ready") is not False:
            errors.append(f"{row.get('queue_id')}: external_action_ready must be false")
        if row.get("outward_use_allowed") is not False:
            errors.append(f"{row.get('queue_id')}: outward_use_allowed must be false")

    if not DASHBOARD.exists():
        errors.append(f"Missing dashboard: {DASHBOARD.relative_to(ROOT)}")
        text = ""
    else:
        text = DASHBOARD.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Dashboard missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")

    if errors:
        print("FAIL SourceCheckup example expansion dashboard validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup example expansion dashboard validation")
    print(f"dashboard={DASHBOARD.relative_to(ROOT)}")
    print(f"surface_examples={len(surface_rows)}")
    print(f"contribution_examples={len(contribution_rows)}")
    print(f"queue_rows={len(queue_rows)}")
    print(f"queue_surfaces={len(queue_surfaces)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
