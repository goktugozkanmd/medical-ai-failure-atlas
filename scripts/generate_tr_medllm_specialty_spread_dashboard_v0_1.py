#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "tr_medllm_safetybench" / "synthetic_risk_pack_v0_1.jsonl"
OUTPUT = ROOT / "tr_medllm_safetybench" / "build" / "specialty_spread_dashboard_v0_1.md"

SPECIALTY_DOMAINS = {
    "cardiology",
    "endocrinology",
    "nephrology",
    "infectious diseases",
    "geriatrics",
    "pregnancy medication safety",
}


def load_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in PACK.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def yes_no(value: object) -> str:
    return "yes" if value is True else "no"


def main() -> None:
    rows = load_rows()
    risk_counts: Counter[str] = Counter(str(row["risk_axis"]) for row in rows)
    domain_counts: Counter[str] = Counter(str(row["clinical_domain"]) for row in rows)
    gate_counts: Counter[str] = Counter(str(row["release_gate"]) for row in rows)
    taxonomy_counts: Counter[str] = Counter(
        str(pattern_id)
        for row in rows
        for pattern_id in row["taxonomy_pattern_ids"]
    )
    source_rows = [row for row in rows if row.get("sourcecheckup_needed") is True]
    clinician_rows = [row for row in rows if row.get("clinician_review_needed") is True]
    specialty_rows = [row for row in rows if str(row["clinical_domain"]) in SPECIALTY_DOMAINS]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# TR MedLLM specialty spread dashboard v0.1",
        "",
        "Status: generated public preview.",
        "",
        "This dashboard summarizes the Turkish synthetic risk pack by specialty domain, risk axis, release gate, and SourceCheckup routing.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not a benchmark compatibility claim, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Turkish synthetic risk rows: {len(rows)}",
        "",
        f"Specialty spread rows: {len(specialty_rows)}",
        "",
        f"Specialty domains represented: {len(SPECIALTY_DOMAINS)}",
        "",
        f"Risk axes represented: {len(risk_counts)}",
        "",
        f"Rows needing SourceCheckup review: {len(source_rows)}",
        "",
        f"SourceCheckup routed rows: {len(source_rows)}",
        "",
        "SourceCheckup TR MedLLM assurance routing map: `docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md`",
        "",
        "Source review worksheets: `docs/SOURCE_REVIEW_WORKSHEETS_V0_1.md`",
        "",
        f"Clinician review needed rows: {len(clinician_rows)}",
        "",
        "## Specialty spread rows",
        "",
    ]

    for row in sorted(specialty_rows, key=lambda item: str(item["case_id"])):
        taxonomy_ids = ", ".join(str(item) for item in row["taxonomy_pattern_ids"])
        lines.extend(
            [
                f"### {row['case_id']}: {row['clinical_domain']}",
                "",
                f"Risk axis: `{row['risk_axis']}`",
                "",
                f"Release gate: `{row['release_gate']}`",
                "",
                f"Taxonomy pattern IDs: {taxonomy_ids}",
                "",
                f"SourceCheckup needed: `{yes_no(row.get('sourcecheckup_needed'))}`",
                "",
                f"Synthetic prompt seed: {row['turkish_prompt_seed']}",
                "",
                f"Safe answer expectation: {row['safe_answer_expectation']}",
                "",
                f"Track A value: {row['track_a_relevance']}",
                "",
                f"Track B value: {row['track_b_relevance']}",
                "",
            ]
        )

    lines.extend(["## Risk axis coverage", ""])
    for risk_axis, count in sorted(risk_counts.items()):
        lines.extend([f"{risk_axis}: {count}", ""])

    lines.extend(["## Clinical domain coverage", ""])
    for domain, count in sorted(domain_counts.items()):
        lines.extend([f"{domain}: {count}", ""])

    lines.extend(["## Release gate coverage", ""])
    for gate, count in sorted(gate_counts.items()):
        lines.extend([f"{gate}: {count}", ""])

    lines.extend(["## Taxonomy coverage", ""])
    for pattern_id, count in sorted(taxonomy_counts.items()):
        lines.extend([f"{pattern_id}: {count}", ""])

    lines.extend(["## SourceCheckup routed rows", ""])
    for row in source_rows:
        lines.extend(
            [
                f"{row['case_id']}: `{row['clinical_domain']}` uses risk axis `{row['risk_axis']}` and release gate `{row['release_gate']}`.",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. Every row is synthetic.",
            "2. Patient data is not used.",
            "3. Clinical use is not allowed.",
            "4. Specialty spread is a coverage view, not clinical validation.",
            "5. SourceCheckup routing is a review queue signal, not proof that a medical claim is true.",
            "6. This dashboard does not rank models or claim benchmark compatibility.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"rows={len(rows)}")
    print(f"specialty_rows={len(specialty_rows)}")
    print(f"risk_axes={len(risk_counts)}")
    print(f"sourcecheckup_rows={len(source_rows)}")
    print(f"clinician_review_rows={len(clinician_rows)}")


if __name__ == "__main__":
    main()
