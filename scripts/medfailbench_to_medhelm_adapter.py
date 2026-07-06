#!/usr/bin/env python3
"""MedFailBench to MedHELM-style scenario adapter (demo, v0.1).

This is a proof-of-concept adapter that exports 10 MedFailBench cases into a
MedHELM-style scenario structure so that the safety-gate taxonomy can be
proposed to the MedHELM community as a complementary scenario suite.

This is NOT a claim of MedHELM compatibility, equivalence, or endorsement.
The output is a discussion artifact for the upstream MedHELM discussion
(see PacificAI/medhelm discussions).

MedHELM scenarios typically carry:
- scenario name and description
- task family
- instance-level prompt
- reference / rubric fields

MedFailBench contributes a safety_gate dimension (which gate the case tests)
that MedHELM-style workflows can use as an additional eval axis.

Usage:
    python3 scripts/medfailbench_to_medhelm_adapter.py
    python3 scripts/medfailbench_to_medhelm_adapter.py --limit 10 --out outputs/medhelm_adapter_demo.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "failure_atlas" / "public" / "case_intake_examples_v0_1.jsonl"

# MedHELM task family approximation. MedFailBench cases are mostly
# "patient_communication" / "clinical_decision_support" style.
DOMAIN_TO_TASK_FAMILY = {
    "medication safety": "clinical_decision_support",
    "cardiology": "clinical_decision_support",
    "emergency and critical care": "patient_communication",
    "endocrinology": "clinical_decision_support",
    "neurology": "clinical_decision_support",
    "nephrology": "clinical_decision_support",
    "gastroenterology and hepatology": "clinical_decision_support",
    "obstetrics and women's health": "clinical_decision_support",
    "geriatrics and polypharmacy": "clinical_decision_support",
    "infectious diseases": "clinical_decision_support",
    "source integrity": "clinical_information_retrieval",
}


def adapt_case(row: dict) -> dict:
    """Convert one MedFailBench case-intake row to a MedHELM-style scenario."""
    case_id = row.get("case_id", "")
    domain = row.get("clinical_domain", "")
    return {
        "scenario_name": f"medfailbench_safety_gate_{case_id.lower()}",
        "medhelm_task_family": DOMAIN_TO_TASK_FAMILY.get(domain, "clinical_decision_support"),
        "source_case_id": case_id,
        "source_repository": "MedFailBench",
        "source_repository_url": "https://github.com/goktugozkanmd/medical-ai-failure-atlas",
        "description": row.get("synthetic_case_summary", ""),
        "prompt": row.get("synthetic_case_summary", ""),
        "safety_gate_contribution": {
            "failure_pattern": row.get("failure_pattern", ""),
            "taxonomy_pattern_ids": row.get("taxonomy_pattern_ids", []),
            "risk_axis": row.get("risk_axis", ""),
            "safe_answer_expectation": row.get("safe_answer_expectation", ""),
        },
        "synthetic_only": True,
        "patient_data_used": False,
        "license_note": "Same as MedFailBench (Apache-2.0 / CC-BY-4.0). Not a MedHELM-compatible or endorsed artifact.",
    }


def main() -> int:
    parser = ArgumentParserSafe()
    parser.add_argument("--source", default=str(SOURCE), help="Source JSONL (case-intake format)")
    parser.add_argument("--out", default=str(ROOT / "outputs" / "medhelm_adapter_demo_v0_1.json"),
                        help="Output JSON path")
    parser.add_argument("--limit", type=int, default=10, help="Max number of cases to export")
    args = parser.parse_args()

    src = Path(args.source)
    if not src.exists():
        print(f"Source not found: {src}", file=__import__('sys').stderr)
        return 1

    rows = []
    for line in src.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))

    adapted = [adapt_case(r) for r in rows[: args.limit]]
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "adapter_version": "0.1",
        "description": "MedFailBench safety-gate scenarios exported to a MedHELM-style structure for discussion. NOT a MedHELM-compatible or endorsed artifact.",
        "medhelm_discussion": "https://github.com/PacificAI/medhelm/discussions/31",
        "case_count": len(adapted),
        "scenarios": adapted,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(adapted)} MedHELM-style scenarios to {out_path.relative_to(ROOT)}")
    print(f"MedHELM discussion: https://github.com/PacificAI/medhelm/discussions/31")
    return 0


class ArgumentParserSafe(__import__('argparse').ArgumentParser):
    pass


if __name__ == "__main__":
    raise SystemExit(main())
