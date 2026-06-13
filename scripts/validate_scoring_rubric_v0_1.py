#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUBRIC = ROOT / "data" / "scoring_rubric_v0_1.json"
EXPECTED_FINAL_LABELS = {
    "clinically_useful",
    "clinically_usable_with_caution",
    "needs_revision_before_clinical_use",
    "unsafe",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def require_text(value: object, message: str) -> None:
    require(isinstance(value, str) and bool(value.strip()), message)


def main() -> None:
    data = json.loads(RUBRIC.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "scoring_rubric_v0_1", "wrong schema_version")
    require(data.get("status") == "internal_draft", "status must be internal_draft")
    require(data.get("contains_patient_data") is False, "contains_patient_data must be false")
    require(data.get("not_for_clinical_use") is True, "not_for_clinical_use must be true")
    require(data.get("data_provenance") == "synthetic", "data_provenance must be synthetic")
    require(set(data.get("final_labels", [])) == EXPECTED_FINAL_LABELS, "final_labels mismatch")

    gates = data.get("safety_gates")
    require(isinstance(gates, list) and len(gates) >= 5, "at least five safety gates required")
    gate_ids = []
    for gate in gates:
        require(isinstance(gate, dict), "gate must be object")
        gate_id = gate.get("gate_id")
        require_text(gate_id, "gate_id missing")
        require_text(gate.get("definition"), f"{gate_id} definition missing")
        require_text(gate.get("positive_anchor"), f"{gate_id} positive_anchor missing")
        require_text(gate.get("negative_anchor"), f"{gate_id} negative_anchor missing")
        source_tags = gate.get("source_tags")
        require(isinstance(source_tags, list) and source_tags, f"{gate_id} source_tags missing")
        gate_ids.append(gate_id)
    require(len(gate_ids) == len(set(gate_ids)), "gate IDs are not unique")

    dimensions = data.get("graded_dimensions")
    require(isinstance(dimensions, list) and len(dimensions) >= 8, "at least eight graded dimensions required")
    dimension_ids = []
    for dimension in dimensions:
        require(isinstance(dimension, dict), "dimension must be object")
        dimension_id = dimension.get("dimension_id")
        require_text(dimension_id, "dimension_id missing")
        for level in ["level_0", "level_1", "level_2"]:
            require_text(dimension.get(level), f"{dimension_id} {level} missing")
        dimension_ids.append(dimension_id)
    require(len(dimension_ids) == len(set(dimension_ids)), "dimension IDs are not unique")

    rules = data.get("decision_rules")
    require(isinstance(rules, list) and len(rules) == 4, "exactly four decision rules required")
    rule_labels = {rule.get("final_label") for rule in rules if isinstance(rule, dict)}
    require(rule_labels == EXPECTED_FINAL_LABELS, "decision rules must cover each final label")

    summaries = data.get("retrospective_dry_run_summary")
    require(isinstance(summaries, list) and len(summaries) >= 2, "retrospective summary missing")
    for summary in summaries:
        require(isinstance(summary, dict), "retrospective summary item must be object")
        require_text(summary.get("source_file"), "retrospective source_file missing")
        rows = summary.get("rows")
        require(isinstance(rows, int) and rows > 0, "retrospective rows must be positive")
        gate_candidates = summary.get("gate_trigger_candidates")
        require(isinstance(gate_candidates, dict) and gate_candidates, "gate_trigger_candidates missing")

    print("PASS")
    print(f"Safety gates: {len(gates)}")
    print(f"Graded dimensions: {len(dimensions)}")
    print(f"Decision rules: {len(rules)}")
    print(f"Retrospective sources: {len(summaries)}")


if __name__ == "__main__":
    main()
