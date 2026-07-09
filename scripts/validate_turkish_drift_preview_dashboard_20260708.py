#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DRIFT_PROBE_JSON = ROOT / "docs" / "tr_en_drift_glm_probe_v0_1.json"
DRIFT_PROBE_TSV = ROOT / "data" / "tr_en_drift_glm_probe_v0_1.tsv"
TR_MEDLLM_JSONL = ROOT / "data" / "tr_medllm_synthetic_eval_set_v0_3.jsonl"
JSON_PATH = ROOT / "docs" / "turkish_drift_preview_dashboard_20260708.json"
MD_PATH = ROOT / "docs" / "TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md"

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "regulatory compliance achieved",
    "officially compatible",
    "patient data used",
    "agent selected physicians",
    "best model",
    "model winner",
]


def main() -> int:
    errors: list[str] = []
    for path in [DRIFT_PROBE_JSON, DRIFT_PROBE_TSV, TR_MEDLLM_JSONL, JSON_PATH, MD_PATH]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    manifest = read_json(JSON_PATH, errors)
    probe = read_json(DRIFT_PROBE_JSON, errors)
    prompt_rows = read_tsv(DRIFT_PROBE_TSV, errors)
    tr_rows = read_jsonl(TR_MEDLLM_JSONL, errors)

    if manifest:
        expected_flags = {
            "external_action_allowed": False,
            "provider_api_call_allowed": False,
            "automation_started": False,
            "new_cases_added": False,
            "agent_selected_physicians": False,
            "contains_patient_data": False,
            "no_clinical_validation_claim": True,
            "no_model_ranking": True,
            "no_regulatory_compliance_claim": True,
            "no_official_compatibility_claim": True,
        }
        for key, expected in expected_flags.items():
            if manifest.get(key) is not expected:
                errors.append(f"Turkish drift dashboard {key} must be {expected!r}")
        if manifest.get("status") != "local_preview_dashboard_ready":
            errors.append("Turkish drift dashboard status mismatch")
        if manifest.get("phase") != "P4":
            errors.append("Turkish drift dashboard phase must be P4")
        if manifest.get("product_name") != "Clinical AI Safety Ops / Health AI Assurance Kit":
            errors.append("Turkish drift dashboard product_name mismatch")
        tiers = manifest.get("validation_tiers", [])
        if not isinstance(tiers, list) or [tier.get("id") for tier in tiers if isinstance(tier, dict)] != [
            "tier_small_live_output_probe",
            "tier_existing_turkish_synthetic_set",
        ]:
            errors.append("Turkish drift dashboard validation tiers mismatch")
        validate_probe_section(manifest, probe, prompt_rows, errors)
        validate_turkish_set_section(manifest, tr_rows, errors)
        blocked = set(manifest.get("blocked_actions", []))
        for required in {
            "send_external_email_or_post_without_user_approval",
            "start_provider_api_calls_without_user_approval",
            "add_new_cases_without_user_approval",
            "claim_clinical_validation",
            "claim_regulatory_compliance",
            "claim_official_endorsement_or_compatibility",
            "rank_models_as_winners",
            "select_or_contact_physicians_by_agent",
        }:
            if required not in blocked:
                errors.append(f"Turkish drift dashboard blocked_actions missing {required}")

    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in [
            "Turkish Drift Preview Dashboard",
            "P4 Turkish Drift Preview",
            "No external send",
            "no provider API call",
            "no new case addition",
            "no patient data",
            "no physician selection",
            "no clinical validation claim",
            "no model ranking",
            "validation tiers separate",
            "TR EN probe",
            "Turkish synthetic set",
            "make turkish_drift_preview_dashboard_20260708",
        ]:
            if phrase.lower() not in lowered:
                errors.append(f"Turkish drift dashboard markdown missing required phrase: {phrase}")

    for path in [JSON_PATH, MD_PATH]:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                errors.append(f"Forbidden phrase present in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("FAIL Turkish drift preview dashboard validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Turkish drift preview dashboard validation")
    print("pairs=5")
    print("turkish_rows=44")
    print("sourcecheckup_needed_rows=6")
    return 0


def validate_probe_section(
    manifest: dict[str, Any],
    probe: dict[str, Any],
    prompt_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    section = manifest.get("tr_en_probe", {})
    if not isinstance(section, dict):
        errors.append("Turkish drift dashboard tr_en_probe must be an object")
        return
    expected = {
        "model": probe.get("model"),
        "pairs_evaluated": 5,
        "outputs_evaluated": 10,
        "prompt_rows": 10,
        "en_boundaries_met": 5,
        "tr_boundaries_met": 5,
        "notable_drift_count": 3,
    }
    for key, value in expected.items():
        if section.get(key) != value:
            errors.append(f"Turkish drift dashboard tr_en_probe {key} mismatch: {section.get(key)!r}")
    if len(prompt_rows) != 10:
        errors.append(f"Expected 10 prompt rows, found {len(prompt_rows)}")
    rows = section.get("rows", [])
    if not isinstance(rows, list) or len(rows) != 5:
        errors.append("Turkish drift dashboard must include five probe rows")
    for row in rows if isinstance(rows, list) else []:
        if row.get("en_safety_boundary_met") is not True or row.get("tr_safety_boundary_met") is not True:
            errors.append(f"Probe row boundary not met: {row.get('pair_id')}")


def validate_turkish_set_section(manifest: dict[str, Any], tr_rows: list[dict[str, Any]], errors: list[str]) -> None:
    section = manifest.get("turkish_synthetic_set", {})
    if not isinstance(section, dict):
        errors.append("Turkish drift dashboard turkish_synthetic_set must be an object")
        return
    expected_counts = {
        "rows": len(tr_rows),
        "language_counts": dict(sorted(Counter(str(row.get("language")) for row in tr_rows).items())),
        "domain_counts": dict(sorted(Counter(str(row.get("clinical_domain")) for row in tr_rows).items())),
        "risk_axis_counts": dict(sorted(Counter(str(row.get("risk_axis")) for row in tr_rows).items())),
        "safety_gate_counts": dict(sorted(Counter(str(row.get("safety_gate")) for row in tr_rows).items())),
        "severity_counts": dict(sorted(Counter(str(row.get("severity_1_to_5")) for row in tr_rows).items())),
        "release_gate_counts": dict(sorted(Counter(str(row.get("release_gate")) for row in tr_rows).items())),
        "sourcecheckup_needed_rows": sum(1 for row in tr_rows if row.get("sourcecheckup_needed") is True),
        "high_severity_rows": sum(1 for row in tr_rows if int(row.get("severity_1_to_5") or 0) >= 5),
    }
    for key, value in expected_counts.items():
        if section.get(key) != value:
            errors.append(f"Turkish drift dashboard Turkish set {key} mismatch")
    if expected_counts["rows"] != 44:
        errors.append(f"Expected 44 Turkish rows, found {expected_counts['rows']}")
    if expected_counts["sourcecheckup_needed_rows"] != 6:
        errors.append("Expected 6 SourceCheckup needed Turkish rows")
    if expected_counts["high_severity_rows"] != 23:
        errors.append("Expected 23 high severity Turkish rows")
    if section.get("language_counts") != {"tr": 44}:
        errors.append("Turkish set language count must be tr=44")
    if len(section.get("sourcecheckup_route_examples", [])) != 6:
        errors.append("Turkish dashboard must include six SourceCheckup route examples")
    if len(section.get("top_high_severity_examples", [])) != 6:
        errors.append("Turkish dashboard must include six high severity examples")


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"JSON must be an object: {path.relative_to(ROOT)}")
        return {}
    return payload


def read_jsonl(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSONL {path.relative_to(ROOT)}:{line_number}: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"JSONL row must be an object: {path.relative_to(ROOT)}:{line_number}")
            continue
        rows.append(row)
    return rows


def read_tsv(path: Path, errors: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter="\t"))
    except csv.Error as exc:
        errors.append(f"Invalid TSV {path.relative_to(ROOT)}: {exc}")
        return []


if __name__ == "__main__":
    sys.exit(main())
