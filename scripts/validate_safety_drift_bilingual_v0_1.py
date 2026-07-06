#!/usr/bin/env python3
"""Validate TR-EN Clinical Safety Drift Dataset v0.1.

Checks the bilingual paired dataset:
- exactly 50 EN + 50 TR rows (100 total)
- every DRIFT-EN-NNN has a matching DRIFT-TR-NNN with the same drift_pair_id
- TR rows carry language="tr" and a non-empty turkish_prompt_seed
- every required case-intake field is present and valid
- taxonomy T01-T10 collectively covered
- at least 5 distinct risk axes
- drift_dimension values are from the allowed set
- no forbidden phrases

Run: python3 scripts/validate_safety_drift_bilingual_v0_1.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "failure_atlas" / "public" / "case_intake_safety_drift_bilingual_v0_1.jsonl"

REQUIRED_FIELDS = [
    "case_id", "clinical_domain", "setting", "synthetic_case_summary",
    "failure_pattern", "taxonomy_pattern_ids", "risk_axis",
    "sourcecheckup_needed", "clinician_review_needed", "safe_answer_expectation",
    "release_gate", "track_a_relevance", "track_b_relevance",
    "synthetic_only", "patient_data_used", "clinical_use_allowed",
    "drift_pair_id", "drift_dimension",
]

ALLOWED_RISK_AXES = {
    "false_reassurance", "medication_safety", "source_support", "missing_context",
    "rare_danger", "over_treatment", "communication_risk",
    "bias_or_premature_closure", "workflow_mismatch", "privacy_or_provenance",
}

ALLOWED_DRIFT_DIMS = {
    "urgency_clarity", "missing_variable_request",
    "unsafe_reassurance", "source_honesty",
}

ALLOWED_RELEASE_GATES = {
    "synthetic_preview_only", "needs_source_review",
    "needs_clinician_review", "not_for_public_summary",
}

FORBIDDEN_PHRASES = [
    "real patient", "clinical validation", "validated for clinical use",
    "safe for clinical use", "approved by", "official endorsement",
    "model is safe", "best model",
]


def main() -> int:
    errors: list[str] = []
    if not INPUT.exists():
        print(f"FAIL Safety drift bilingual validation")
        print(f"- Missing input: {INPUT.relative_to(ROOT)}")
        return 1

    rows: list[dict] = []
    for line_number, line in enumerate(INPUT.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {line_number}: row must be an object")
            continue
        rows.append(row)

    if len(rows) != 100:
        errors.append(f"Expected exactly 100 rows (50 EN + 50 TR), got {len(rows)}")

    seen_ids: set[str] = set()
    en_pairs: dict[str, str] = {}   # pair_id -> en case_id
    tr_pairs: dict[str, str] = {}   # pair_id -> tr case_id
    risk_axes: set[str] = set()
    taxonomy_seen: set[str] = set()

    for index, row in enumerate(rows, start=1):
        case_id = str(row.get("case_id", ""))
        if case_id in seen_ids:
            errors.append(f"Row {index}: duplicate case_id {case_id}")
        seen_ids.add(case_id)

        for field in REQUIRED_FIELDS:
            if field not in row:
                errors.append(f"Row {index} ({case_id}): missing {field}")
            elif isinstance(row[field], str) and not str(row[field]).strip():
                errors.append(f"Row {index} ({case_id}): empty {field}")

        # Boolean enforcement
        if row.get("synthetic_only") is not True:
            errors.append(f"Row {index} ({case_id}): synthetic_only must be true")
        if row.get("patient_data_used") is not False:
            errors.append(f"Row {index} ({case_id}): patient_data_used must be false")
        if row.get("clinical_use_allowed") is not False:
            errors.append(f"Row {index} ({case_id}): clinical_use_allowed must be false")
        if not isinstance(row.get("sourcecheckup_needed"), bool):
            errors.append(f"Row {index} ({case_id}): sourcecheckup_needed must be boolean")
        if not isinstance(row.get("clinician_review_needed"), bool):
            errors.append(f"Row {index} ({case_id}): clinician_review_needed must be boolean")

        # risk_axis
        risk_axis = str(row.get("risk_axis", ""))
        risk_axes.add(risk_axis)
        if risk_axis not in ALLOWED_RISK_AXES:
            errors.append(f"Row {index} ({case_id}): invalid risk_axis {risk_axis!r}")

        # release_gate
        if str(row.get("release_gate", "")) not in ALLOWED_RELEASE_GATES:
            errors.append(f"Row {index} ({case_id}): invalid release_gate {row.get('release_gate')!r}")

        # drift_dimension
        drift_dim = str(row.get("drift_dimension", ""))
        if drift_dim not in ALLOWED_DRIFT_DIMS:
            errors.append(f"Row {index} ({case_id}): invalid drift_dimension {drift_dim!r}")

        # sourcecheckup implies T03
        if row.get("sourcecheckup_needed") is True and "T03" not in row.get("taxonomy_pattern_ids", []):
            errors.append(f"Row {index} ({case_id}): SourceCheckup rows should include taxonomy pattern T03")

        # taxonomy
        pattern_ids = row.get("taxonomy_pattern_ids")
        if not isinstance(pattern_ids, list) or not pattern_ids:
            errors.append(f"Row {index} ({case_id}): taxonomy_pattern_ids must be a non-empty list")
        else:
            local_seen: set[str] = set()
            for pid in pattern_ids:
                if not isinstance(pid, str):
                    errors.append(f"Row {index} ({case_id}): taxonomy_pattern_ids must contain strings")
                    continue
                if pid in local_seen:
                    errors.append(f"Row {index} ({case_id}): duplicate taxonomy pattern {pid}")
                local_seen.add(pid)
                taxonomy_seen.add(pid)

        # pair tracking
        pair_id = str(row.get("drift_pair_id", ""))
        if not pair_id.startswith("PAIR-"):
            errors.append(f"Row {index} ({case_id}): drift_pair_id must be PAIR-NNN, got {pair_id!r}")
        else:
            if case_id.startswith("DRIFT-EN"):
                if pair_id in en_pairs:
                    errors.append(f"Row {index}: duplicate EN pair {pair_id}")
                en_pairs[pair_id] = case_id
            elif case_id.startswith("DRIFT-TR"):
                if pair_id in tr_pairs:
                    errors.append(f"Row {index}: duplicate TR pair {pair_id}")
                tr_pairs[pair_id] = case_id
                # TR rows must carry language + seed
                if row.get("language") != "tr":
                    errors.append(f"Row {index} ({case_id}): DRIFT-TR rows must set language to tr")
                if not str(row.get("turkish_prompt_seed", "")).strip():
                    errors.append(f"Row {index} ({case_id}): DRIFT-TR rows need a turkish_prompt_seed")
            else:
                errors.append(f"Row {index}: case_id must start with DRIFT-EN or DRIFT-TR, got {case_id!r}")

        # forbidden phrases
        row_text = " ".join(str(v).lower() for v in row.values())
        for phrase in FORBIDDEN_PHRASES:
            if phrase in row_text:
                errors.append(f"Row {index} ({case_id}): forbidden phrase {phrase!r}")

    # Pair integrity: every EN must have a matching TR
    en_only = set(en_pairs) - set(tr_pairs)
    tr_only = set(tr_pairs) - set(en_pairs)
    if en_only:
        errors.append(f"EN rows without a matching TR pair: {sorted(en_only)}")
    if tr_only:
        errors.append(f"TR rows without a matching EN pair: {sorted(tr_only)}")
    if len(en_pairs) != 50:
        errors.append(f"Expected exactly 50 EN pairs, got {len(en_pairs)}")
    if len(tr_pairs) != 50:
        errors.append(f"Expected exactly 50 TR pairs, got {len(tr_pairs)}")

    # Coverage
    if len(risk_axes) < 5:
        errors.append(f"Expected at least 5 distinct risk axes, got {len(risk_axes)}")
    required_taxonomy = {f"T{n:02d}" for n in range(1, 11)}
    missing_taxonomy = required_taxonomy - taxonomy_seen
    if missing_taxonomy:
        errors.append(f"Expected coverage of T01-T10; missing {sorted(missing_taxonomy)}")

    if errors:
        print("FAIL Safety drift bilingual validation")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PASS Safety drift bilingual validation")
    print(f"rows={len(rows)}")
    print(f"pairs={len(en_pairs)}")
    print(f"risk_axes={len(risk_axes)}")
    print(f"taxonomy_patterns={len(taxonomy_seen)}")
    print(f"drift_dimensions={len(ALLOWED_DRIFT_DIMS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
