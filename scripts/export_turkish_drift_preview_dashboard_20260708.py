#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DRIFT_PROBE_JSON = ROOT / "docs" / "tr_en_drift_glm_probe_v0_1.json"
DRIFT_PROBE_TSV = ROOT / "data" / "tr_en_drift_glm_probe_v0_1.tsv"
TR_MEDLLM_JSONL = ROOT / "data" / "tr_medllm_synthetic_eval_set_v0_3.jsonl"
JSON_PATH = ROOT / "docs" / "turkish_drift_preview_dashboard_20260708.json"
MD_PATH = ROOT / "docs" / "TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md"


def main() -> int:
    probe = read_json(DRIFT_PROBE_JSON)
    probe_prompt_rows = read_tsv(DRIFT_PROBE_TSV)
    tr_rows = read_jsonl(TR_MEDLLM_JSONL)

    sourcecheckup_rows = [row for row in tr_rows if row.get("sourcecheckup_needed") is True]
    high_severity_rows = [row for row in tr_rows if int(row.get("severity_1_to_5") or 0) >= 5]
    manifest = {
        "artifact_id": "turkish_drift_preview_dashboard_20260708",
        "status": "local_preview_dashboard_ready",
        "created_date": "2026-07-08",
        "phase": "P4",
        "roadmap": "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
        "product_name": "Clinical AI Safety Ops / Health AI Assurance Kit",
        "sources": {
            "tr_en_probe_json": str(DRIFT_PROBE_JSON.relative_to(ROOT)),
            "tr_en_probe_prompt_tsv": str(DRIFT_PROBE_TSV.relative_to(ROOT)),
            "tr_medllm_jsonl": str(TR_MEDLLM_JSONL.relative_to(ROOT)),
        },
        "validation_tiers": [
            {
                "id": "tier_small_live_output_probe",
                "source": str(DRIFT_PROBE_JSON.relative_to(ROOT)),
                "row_count": int(probe["outputs_evaluated"]),
                "claim_boundary": "small probe only, not a benchmark claim",
            },
            {
                "id": "tier_existing_turkish_synthetic_set",
                "source": str(TR_MEDLLM_JSONL.relative_to(ROOT)),
                "row_count": len(tr_rows),
                "claim_boundary": "existing synthetic rows only, not a new case release",
            },
        ],
        "tr_en_probe": {
            "model": probe["model"],
            "pairs_evaluated": probe["pairs_evaluated"],
            "outputs_evaluated": probe["outputs_evaluated"],
            "prompt_rows": len(probe_prompt_rows),
            "en_boundaries_met": probe["summary"]["en_boundaries_met"],
            "tr_boundaries_met": probe["summary"]["tr_boundaries_met"],
            "notable_drift_count": probe["summary"]["notable_drift_count"],
            "rows": probe["rows"],
        },
        "turkish_synthetic_set": {
            "rows": len(tr_rows),
            "language_counts": dict(sorted(Counter(str(row.get("language")) for row in tr_rows).items())),
            "domain_counts": dict(sorted(Counter(str(row.get("clinical_domain")) for row in tr_rows).items())),
            "risk_axis_counts": dict(sorted(Counter(str(row.get("risk_axis")) for row in tr_rows).items())),
            "safety_gate_counts": dict(sorted(Counter(str(row.get("safety_gate")) for row in tr_rows).items())),
            "severity_counts": dict(sorted(Counter(str(row.get("severity_1_to_5")) for row in tr_rows).items())),
            "release_gate_counts": dict(sorted(Counter(str(row.get("release_gate")) for row in tr_rows).items())),
            "sourcecheckup_needed_rows": len(sourcecheckup_rows),
            "high_severity_rows": len(high_severity_rows),
            "top_high_severity_examples": [
                summarize_row(row) for row in sorted(high_severity_rows, key=lambda item: str(item["case_id"]))[:6]
            ],
            "sourcecheckup_route_examples": [
                summarize_row(row) for row in sorted(sourcecheckup_rows, key=lambda item: str(item["case_id"]))[:6]
            ],
        },
        "dashboard_views": [
            "validation_tier_split",
            "tr_en_pair_boundary_table",
            "turkish_risk_axis_counts",
            "turkish_domain_counts",
            "sourcecheckup_route_examples",
            "high_severity_examples",
        ],
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
        "blocked_actions": [
            "send_external_email_or_post_without_user_approval",
            "start_provider_api_calls_without_user_approval",
            "add_new_cases_without_user_approval",
            "claim_clinical_validation",
            "claim_regulatory_compliance",
            "claim_official_endorsement_or_compatibility",
            "rank_models_as_winners",
            "select_or_contact_physicians_by_agent",
        ],
        "next_safe_actions": [
            "connect this dashboard to the kit level assurance card",
            "keep TR EN probe separate from the Turkish synthetic set",
            "keep new Turkish cases blocked until explicit user approval",
        ],
    }
    JSON_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(manifest), encoding="utf-8")
    print(f"Wrote {JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")
    print(f"pairs={manifest['tr_en_probe']['pairs_evaluated']}")
    print(f"turkish_rows={manifest['turkish_synthetic_set']['rows']}")
    print(f"sourcecheckup_needed_rows={manifest['turkish_synthetic_set']['sourcecheckup_needed_rows']}")
    return 0


def summarize_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": row.get("case_id"),
        "clinical_domain": row.get("clinical_domain"),
        "risk_axis": row.get("risk_axis"),
        "safety_gate": row.get("safety_gate"),
        "severity_1_to_5": row.get("severity_1_to_5"),
        "release_gate": row.get("release_gate"),
        "safe_answer_expectation": row.get("safe_answer_expectation"),
    }


def render_markdown(manifest: dict[str, Any]) -> str:
    probe = manifest["tr_en_probe"]
    tr_set = manifest["turkish_synthetic_set"]
    lines = [
        "# Turkish Drift Preview Dashboard",
        "",
        "Date: 2026 07 08",
        "",
        "Status: local preview dashboard ready.",
        "",
        "Roadmap phase: P4 Turkish Drift Preview.",
        "",
        "## Boundary",
        "",
        "No external send, no provider API call, no automation start, no new case addition, no patient data, no physician selection, no clinical validation claim, no regulatory compliance claim, no official compatibility claim, and no model ranking.",
        "",
        "This dashboard keeps validation tiers separate. The TR EN probe is a small live output probe, not a benchmark claim. The Turkish synthetic set is an existing local synthetic set, not a new case release.",
        "",
        "## Validation Tiers",
        "",
        "| Tier | Source | Rows | Claim boundary |",
        "| --- | --- | ---: | --- |",
    ]
    for tier in manifest["validation_tiers"]:
        lines.append(f"| `{tier['id']}` | `{tier['source']}` | {tier['row_count']} | {tier['claim_boundary']} |")
    lines.extend(
        [
            "",
            "## TR EN Probe",
            "",
            f"- Model: `{probe['model']}`.",
            f"- Pairs evaluated: {probe['pairs_evaluated']}.",
            f"- Outputs evaluated: {probe['outputs_evaluated']}.",
            f"- Prompt rows: {probe['prompt_rows']}.",
            f"- EN safety boundaries met: {probe['en_boundaries_met']}.",
            f"- TR safety boundaries met: {probe['tr_boundaries_met']}.",
            f"- Notable drift count: {probe['notable_drift_count']}.",
            "",
            "| Pair | Domain | Risk axis | EN boundary | TR boundary | Drift note |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in probe["rows"]:
        en = "pass" if row["en_safety_boundary_met"] else "hold"
        tr = "pass" if row["tr_safety_boundary_met"] else "hold"
        lines.append(f"| {row['pair_id']} | {row['domain']} | `{row['risk_axis']}` | {en} | {tr} | {row['drift_note']} |")
    lines.extend(
        [
            "",
            "## Turkish Synthetic Set",
            "",
            f"- Rows: {tr_set['rows']}.",
            f"- High severity rows: {tr_set['high_severity_rows']}.",
            f"- SourceCheckup needed rows: {tr_set['sourcecheckup_needed_rows']}.",
            "",
            "### Risk Axis Counts",
            "",
        ]
    )
    for key, value in tr_set["risk_axis_counts"].items():
        lines.append(f"- `{key}`: {value}.")
    lines.extend(["", "### Domain Counts", ""])
    for key, value in tr_set["domain_counts"].items():
        lines.append(f"- `{key}`: {value}.")
    lines.extend(["", "### Severity Counts", ""])
    for key, value in tr_set["severity_counts"].items():
        lines.append(f"- `{key}`: {value}.")
    lines.extend(["", "## SourceCheckup Route Examples", ""])
    for row in tr_set["sourcecheckup_route_examples"]:
        lines.append(
            f"- `{row['case_id']}` `{row['clinical_domain']}` `{row['risk_axis']}` "
            f"severity {row['severity_1_to_5']}: {row['safe_answer_expectation']}"
        )
    lines.extend(["", "## High Severity Examples", ""])
    for row in tr_set["top_high_severity_examples"]:
        lines.append(
            f"- `{row['case_id']}` `{row['clinical_domain']}` `{row['risk_axis']}` "
            f"gate `{row['safety_gate']}`: {row['safe_answer_expectation']}"
        )
    lines.extend(
        [
            "",
            "## Next",
            "",
            "1. Connect this dashboard to the kit level assurance card.",
            "2. Keep TR EN probe, Turkish synthetic set, and any future clinician panel result as separate validation tiers.",
            "3. Do not add new Turkish cases without explicit user approval.",
            "",
            "## Validation",
            "",
            "Run:",
            "",
            "```bash",
            "make turkish_drift_preview_dashboard_20260708",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path.relative_to(ROOT)} must be a JSON object")
    return payload


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise TypeError(f"{path.relative_to(ROOT)}:{line_number} must be a JSON object")
        rows.append(row)
    return rows


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


if __name__ == "__main__":
    raise SystemExit(main())
