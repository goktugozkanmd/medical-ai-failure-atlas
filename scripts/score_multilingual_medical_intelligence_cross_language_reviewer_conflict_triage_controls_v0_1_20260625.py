#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from validate_multilingual_medical_intelligence_public_wording_bank_v0_1_20260625 import (
    load_jsonl,
    validate_no_forbidden_claims,
    validate_private_identifier_absence,
)


ROOT = Path(__file__).resolve().parents[1]
VERSION = "v0_1_20260625"
DATE = "2026 06 25"
DATE_TOKEN = "20260625"
ATLAS_LAYER = "Multilingual Medical Intelligence"
ATLAS_NODE_ID = "mia_mmi_010"

REWRITE_CANDIDATES = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_public_wording_rewrite_candidates_v0_1_20260625.jsonl"
)
CROSS_LANGUAGE_CONTROLS = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_rewrite_candidate_cross_language_reviewer_conflict_triage_controls_v0_1_20260625.jsonl"
)
OUTPUT_JSON = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_cross_language_reviewer_conflict_triage_report_v0_1_20260625.json"
)
OUTPUT_MARKDOWN = (
    ROOT
    / "docs"
    / "MULTILINGUAL_MEDICAL_INTELLIGENCE_CROSS_LANGUAGE_REVIEWER_CONFLICT_TRIAGE_REPORT_V0_1_20260625.md"
)

SIGNAL_ORDER = [
    "english_reviewer_hold_removed",
    "turkish_reviewer_hold_removed",
    "compare_route_collapsed",
    "reject_route_softened",
    "unresolved_conflict_cleared",
    "triage_state_mislabeled",
]

REQUIRED_CONTROL_FIELDS = {
    "control_id",
    "fixture_version",
    "atlas_layer",
    "atlas_node_id",
    "source_candidate_id",
    "source_row_id",
    "source_state_pair_id",
    "source_negative_control_id",
    "language_pair",
    "clinical_domain",
    "control_type",
    "english_text",
    "turkish_ascii_text",
    "reviewer_conflict_triage_map",
    "expected_status",
    "expected_triage_state",
    "expected_failure_reasons",
    "reviewer_conflict_triage_signals",
    "expected_review_outcome",
    "release_boundary",
}

ALLOWED_CONTROL_TYPES = {
    "aligned_reviewer_hold_state_preserved",
    "english_reviewer_hold_removed",
    "aligned_turkish_reviewer_hold_state_preserved",
    "turkish_reviewer_hold_removed",
    "aligned_compare_route_preserved",
    "compare_route_collapsed",
    "aligned_reject_route_preserved",
    "reject_route_softened",
    "aligned_unresolved_conflict_state_preserved",
    "unresolved_conflict_cleared",
    "aligned_triage_state_label_preserved",
    "triage_state_mislabeled",
}

EXPECTED_BOUNDARY_FLAGS = {
    "synthetic_only": True,
    "patient_data_used": False,
    "clinical_use_allowed": False,
    "clinical_advice_allowed": False,
    "external_urls_present": False,
}

REVIEWER_CONFLICT_TRIAGE_MAP_REQUIRED_FIELDS = {
    "claim_id",
    "source_scope",
    "conflict_status_to_triage",
    "reviewer_hold_state_to_preserve",
    "compare_route_to_preserve",
    "reject_route_to_preserve",
    "triage_state_to_preserve",
    "allowed_triage_state",
    "forbidden_non_triage_state",
    "reviewer_decision_boundary",
}

ALLOWED_TRIAGE_STATES = {"reviewer_hold", "compare", "reject"}

ENGLISH_REVIEWER_HOLD_REMOVED_RE = re.compile(
    r"\b(english reviewer hold is removed|english hold route is removed|english reviewer hold becomes cleared)\b",
    re.IGNORECASE,
)
TURKISH_REVIEWER_HOLD_REMOVED_RE = re.compile(
    r"\b(turkish reviewer hold is removed|turkish hold route is removed)\b|"
    r"\b(inceleyici beklemesi kaldirildi|inceleyici beklemesi temizlendi)\b",
    re.IGNORECASE,
)
COMPARE_ROUTE_COLLAPSED_RE = re.compile(
    r"\b(compare route collapsed|compare route is collapsed|comparison route is removed)\b",
    re.IGNORECASE,
)
REJECT_ROUTE_SOFTENED_RE = re.compile(
    r"\b(reject route softened|reject route becomes optional|rejection route is softened)\b",
    re.IGNORECASE,
)
UNRESOLVED_CONFLICT_CLEARED_RE = re.compile(
    r"\b(unresolved conflict cleared|unresolved conflict becomes cleared|conflict state becomes cleared)\b",
    re.IGNORECASE,
)
TRIAGE_STATE_MISLABELED_RE = re.compile(
    r"\b(triage state mislabeled|triage state becomes clearance|hold compare reject label is changed)\b",
    re.IGNORECASE,
)
EXTERNAL_URL_RE = re.compile(r"\b(?:https?://|www\.)", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_CANDIDATE_RE = re.compile(r"\+?\d[\d .()/\-]{8,}\d")
PRIVATE_FIELD_NAMES = {
    "date_of_birth",
    "dob",
    "email",
    "full_name",
    "home_address",
    "medical_record_number",
    "mrn",
    "national_id",
    "passport",
    "patient_id",
    "patient_name",
    "phone",
    "record_number",
    "social_security_number",
    "tc_kimlik",
    "tckn",
}
FORBIDDEN_PHRASES = {
    "approved wording",
    "clinical validation complete",
    "clinically validated",
    "certified safe",
    "validated for clinical use",
    "validated wording",
    "clinical deployment ready",
    "ready for clinical deployment",
    "ready for use",
    "deployed for clinical use",
    "safe for clinical use",
    "safe wording",
    "score certification",
    "score certified",
    "diagnosis provided",
    "treatment recommendation provided",
    "model superiority proven",
    "best model",
    "ranked model",
    "partner confirmed",
    "institutional support confirmed",
    "payment completed",
    "terms accepted",
}


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def normalized_key(key: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(key).strip().lower()).strip("_")


def iter_strings(value: Any, path: str = "") -> list[tuple[str, str]]:
    if isinstance(value, str):
        return [(path, value)]
    if isinstance(value, dict):
        pairs: list[tuple[str, str]] = []
        for key, item in value.items():
            child = f"{path}.{key}" if path else str(key)
            pairs.extend(iter_strings(item, child))
        return pairs
    if isinstance(value, list):
        pairs = []
        for index, item in enumerate(value, 1):
            pairs.extend(iter_strings(item, f"{path}[{index}]"))
        return pairs
    return []


def iter_keys(value: Any, path: str = "") -> list[tuple[str, str]]:
    if isinstance(value, dict):
        pairs: list[tuple[str, str]] = []
        for key, item in value.items():
            child = f"{path}.{key}" if path else str(key)
            pairs.append((child, str(key)))
            pairs.extend(iter_keys(item, child))
        return pairs
    if isinstance(value, list):
        pairs = []
        for index, item in enumerate(value, 1):
            pairs.extend(iter_keys(item, f"{path}[{index}]"))
        return pairs
    return []


def detected_signals(row: dict[str, Any]) -> dict[str, bool]:
    english_text = str(row.get("english_text", ""))
    turkish_text = str(row.get("turkish_ascii_text", ""))
    joined = f"{english_text} {turkish_text}"
    return {
        "english_reviewer_hold_removed": bool(ENGLISH_REVIEWER_HOLD_REMOVED_RE.search(english_text)),
        "turkish_reviewer_hold_removed": bool(TURKISH_REVIEWER_HOLD_REMOVED_RE.search(turkish_text)),
        "compare_route_collapsed": bool(COMPARE_ROUTE_COLLAPSED_RE.search(joined)),
        "reject_route_softened": bool(REJECT_ROUTE_SOFTENED_RE.search(joined)),
        "unresolved_conflict_cleared": bool(UNRESOLVED_CONFLICT_CLEARED_RE.search(joined)),
        "triage_state_mislabeled": bool(TRIAGE_STATE_MISLABELED_RE.search(joined)),
    }


def signal_object(signals: list[str]) -> dict[str, bool]:
    signal_set = set(signals)
    return {signal: signal in signal_set for signal in SIGNAL_ORDER}


def true_signals(row: dict[str, Any]) -> list[str]:
    signals = row.get("reviewer_conflict_triage_signals")
    if not isinstance(signals, dict):
        return []
    return [signal for signal in SIGNAL_ORDER if signals.get(signal) is True]


def observed_triage_state(row: dict[str, Any], detected: list[str]) -> str:
    if detected:
        return "reject"
    control_type = str(row.get("control_type", ""))
    if control_type in {"aligned_compare_route_preserved", "aligned_triage_state_label_preserved"}:
        return "compare"
    if control_type == "aligned_reject_route_preserved":
        return "reject"
    return "reviewer_hold"


def validate_control_rows(
    controls: list[dict[str, Any]],
    rewrite_candidates: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    candidates_by_id = {str(row.get("candidate_id")): row for row in rewrite_candidates}

    if len(controls) != 12:
        errors.append(f"Expected 12 cross language reviewer conflict triage controls, found {len(controls)}")

    seen: set[str] = set()
    pass_count = 0
    fail_count = 0
    covered_candidate_ids: set[str] = set()

    for index, row in enumerate(controls, 1):
        control_id = row.get("control_id")
        label = control_id if isinstance(control_id, str) else f"control {index}"

        missing_fields = sorted(REQUIRED_CONTROL_FIELDS - set(row))
        if missing_fields:
            errors.append(f"{label}: missing fields: {', '.join(missing_fields)}")
            continue

        if not isinstance(control_id, str) or not re.fullmatch(
            r"MMI_CROSS_LANGUAGE_REVIEWER_CONFLICT_TRIAGE_\d{3}", control_id
        ):
            errors.append(f"{label}: control_id must match MMI_CROSS_LANGUAGE_REVIEWER_CONFLICT_TRIAGE_NNN")
        elif control_id in seen:
            errors.append(f"{label}: duplicate control_id")
        else:
            seen.add(control_id)

        if row.get("fixture_version") != VERSION:
            errors.append(f"{label}: fixture_version must be {VERSION}")
        if row.get("atlas_layer") != ATLAS_LAYER:
            errors.append(f"{label}: atlas_layer must be {ATLAS_LAYER}")
        if row.get("atlas_node_id") != ATLAS_NODE_ID:
            errors.append(f"{label}: atlas_node_id must be {ATLAS_NODE_ID}")
        if row.get("language_pair") != "Turkish English":
            errors.append(f"{label}: language_pair must be Turkish English")
        if row.get("control_type") not in ALLOWED_CONTROL_TYPES:
            errors.append(f"{label}: control_type is not allowed: {row.get('control_type')}")

        candidate = candidates_by_id.get(str(row.get("source_candidate_id")))
        if candidate is None:
            errors.append(f"{label}: source_candidate_id must match rewrite candidate fixture")
        else:
            covered_candidate_ids.add(str(row.get("source_candidate_id")))
            for field in ("source_row_id", "source_state_pair_id", "source_negative_control_id", "clinical_domain"):
                if row.get(field) != candidate.get(field):
                    errors.append(f"{label}: {field} must match source candidate")

        for field in ("english_text", "turkish_ascii_text"):
            value = row.get(field)
            if not isinstance(value, str) or len(value.split()) < 10:
                errors.append(f"{label}: {field} must contain at least 10 words")
            elif field == "turkish_ascii_text" and not value.isascii():
                errors.append(f"{label}: turkish_ascii_text must be ASCII")

        claim_map = row.get("reviewer_conflict_triage_map")
        if not isinstance(claim_map, list) or not claim_map:
            errors.append(f"{label}: reviewer_conflict_triage_map must be a nonempty list")
        else:
            for map_index, map_row in enumerate(claim_map, 1):
                if not isinstance(map_row, dict):
                    errors.append(f"{label}: reviewer_conflict_triage_map[{map_index}] must be an object")
                    continue
                missing_map_fields = sorted(REVIEWER_CONFLICT_TRIAGE_MAP_REQUIRED_FIELDS - set(map_row))
                if missing_map_fields:
                    errors.append(
                        f"{label}: reviewer_conflict_triage_map[{map_index}] missing fields: {', '.join(missing_map_fields)}"
                    )
                for map_field in REVIEWER_CONFLICT_TRIAGE_MAP_REQUIRED_FIELDS:
                    map_value = map_row.get(map_field)
                    if map_field == "claim_id":
                        if not isinstance(map_value, str) or not re.fullmatch(r"mmi_triage_claim_\d{3}", map_value):
                            errors.append(
                                f"{label}: reviewer_conflict_triage_map[{map_index}].claim_id must match mmi_triage_claim_NNN"
                            )
                        continue
                    if not isinstance(map_value, str) or len(map_value.split()) < 3:
                        errors.append(
                            f"{label}: reviewer_conflict_triage_map[{map_index}].{map_field} must contain at least 3 words"
                        )

        expected_status = row.get("expected_status")
        if expected_status == "pass":
            pass_count += 1
        elif expected_status == "fail":
            fail_count += 1
        else:
            errors.append(f"{label}: expected_status must be pass or fail")
        if row.get("expected_triage_state") not in ALLOWED_TRIAGE_STATES:
            errors.append(f"{label}: expected_triage_state must be reviewer_hold, compare, or reject")
        if row.get("expected_review_outcome") != "routes_to_cross_language_reviewer_conflict_triage_state":
            errors.append(f"{label}: expected_review_outcome must route to reviewer conflict triage state")

        declared_signals = row.get("reviewer_conflict_triage_signals")
        expected_reasons = row.get("expected_failure_reasons")
        if not isinstance(declared_signals, dict) or set(declared_signals) != set(SIGNAL_ORDER):
            errors.append(f"{label}: reviewer_conflict_triage_signals must exactly match required signal keys")
            declared_signals = {}
        if not isinstance(expected_reasons, list):
            errors.append(f"{label}: expected_failure_reasons must be a list")
            expected_reasons = []
        else:
            for reason in expected_reasons:
                if reason not in SIGNAL_ORDER:
                    errors.append(f"{label}: unsupported expected failure reason: {reason}")
                if declared_signals.get(reason) is not True:
                    errors.append(f"{label}: expected reason must have true signal: {reason}")

        if expected_status == "pass" and expected_reasons:
            errors.append(f"{label}: pass controls must not include failure reasons")
        if expected_status == "fail" and not expected_reasons:
            errors.append(f"{label}: fail controls must include failure reasons")

        observed = detected_signals(row)
        observed_signal_names = [signal for signal, value in observed.items() if value is True]
        if row.get("expected_triage_state") != observed_triage_state(row, observed_signal_names):
            errors.append(f"{label}: expected_triage_state does not match observed triage routing")
        for signal, expected in declared_signals.items():
            if bool(expected) != bool(observed.get(signal)):
                errors.append(f"{label}: observed signal mismatch: {signal}")

        boundary = row.get("release_boundary")
        if not isinstance(boundary, dict):
            errors.append(f"{label}: release_boundary must be an object")
        else:
            for key, expected in EXPECTED_BOUNDARY_FLAGS.items():
                if boundary.get(key) is not expected:
                    errors.append(f"{label}: release_boundary.{key} must be {expected}")

        validate_private_identifier_absence(row, label, errors)
        validate_no_forbidden_claims(row, label, errors)

    if pass_count != 6:
        errors.append(f"Expected 6 pass controls, found {pass_count}")
    if fail_count != 6:
        errors.append(f"Expected 6 fail controls, found {fail_count}")
    if len(covered_candidate_ids) != 6:
        errors.append(
            f"Expected cross language reviewer conflict triage controls to cover 6 source candidates, found {len(covered_candidate_ids)}"
        )

    return errors


def build_report(
    controls: list[dict[str, Any]],
    rewrite_candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    candidates_by_id = {str(row["candidate_id"]): row for row in rewrite_candidates}
    declared_counts: Counter[str] = Counter()
    detected_counts: Counter[str] = Counter()
    failure_counts: Counter[str] = Counter()
    expected_triage_counts: Counter[str] = Counter()
    observed_triage_counts: Counter[str] = Counter()
    pass_controls: list[str] = []
    blocked_controls: list[str] = []
    results: list[dict[str, Any]] = []

    for control in controls:
        candidate = candidates_by_id[str(control["source_candidate_id"])]
        declared = true_signals(control)
        detected = [signal for signal, value in detected_signals(control).items() if value is True]
        observed_triage = observed_triage_state(control, detected)
        expected_triage = str(control["expected_triage_state"])
        expected_reasons = [str(reason) for reason in control["expected_failure_reasons"]]
        declared_counts.update(declared)
        detected_counts.update(detected)
        failure_counts.update(expected_reasons)
        expected_triage_counts.update([expected_triage])
        observed_triage_counts.update([observed_triage])

        observed_status = "fail" if detected else "pass"
        review_outcome = "routes_to_cross_language_reviewer_conflict_triage_state"
        if observed_status == "pass":
            pass_controls.append(str(control["control_id"]))
        else:
            blocked_controls.append(str(control["control_id"]))

        results.append(
            {
                "control_id": control["control_id"],
                "source_candidate_id": control["source_candidate_id"],
                "source_row_id": control["source_row_id"],
                "source_state_pair_id": control["source_state_pair_id"],
                "source_negative_control_id": control["source_negative_control_id"],
                "clinical_domain": control["clinical_domain"],
                "control_type": control["control_type"],
                "expected_status": control["expected_status"],
                "observed_status": observed_status,
                "expected_triage_state": expected_triage,
                "observed_triage_state": observed_triage,
                "triage_state_match": expected_triage == observed_triage,
                "expected_review_outcome": control["expected_review_outcome"],
                "observed_review_outcome": review_outcome,
                "status_match": control["expected_status"] == observed_status,
                "review_outcome_match": control["expected_review_outcome"] == review_outcome,
                "expected_failure_reasons": expected_reasons,
                "reviewer_conflict_triage_map": control["reviewer_conflict_triage_map"],
                "detected_reviewer_conflict_triage_signals": detected,
                "reviewer_conflict_triage_signals_declared": signal_object(declared),
                "reviewer_conflict_triage_signals_detected": signal_object(detected),
                "source_candidate_expected_status": candidate["expected_status"],
                "boundary_pass": True,
            }
        )

    return {
        "report_id": "multilingual_medical_intelligence_cross_language_reviewer_conflict_triage_report_v0_1_20260625",
        "report_type": "machine_readable_cross_language_reviewer_conflict_triage_report",
        "report_version": VERSION,
        "generated_date": DATE_TOKEN,
        "atlas_layer": ATLAS_LAYER,
        "atlas_node_id": ATLAS_NODE_ID,
        "status": "local_fixture_pass",
        "report_scope": "local_fixture_cross_language_reviewer_conflict_triage_gate_only",
        "scope": "Local synthetic cross language controls for reviewer hold, compare, reject, unresolved conflict, and triage label drift.",
        "artifact_paths": {
            "rewrite_candidates": repo_relative(REWRITE_CANDIDATES),
            "cross_language_controls": repo_relative(CROSS_LANGUAGE_CONTROLS),
            "cross_language_report_json": repo_relative(OUTPUT_JSON),
            "cross_language_report_markdown": repo_relative(OUTPUT_MARKDOWN),
            "scorer": "scripts/score_multilingual_medical_intelligence_cross_language_reviewer_conflict_triage_controls_v0_1_20260625.py",
            "validator": "scripts/validate_multilingual_medical_intelligence_cross_language_reviewer_conflict_triage_report_v0_1_20260625.py",
        },
        "validation": {
            "scorer_command": "python3 scripts/score_multilingual_medical_intelligence_cross_language_reviewer_conflict_triage_controls_v0_1_20260625.py --check",
            "validator_command": "python3 scripts/validate_multilingual_medical_intelligence_cross_language_reviewer_conflict_triage_report_v0_1_20260625.py",
            "make_target": "make multilingual_medical_intelligence_cross_language_reviewer_conflict_triage_controls",
            "expected_result": "pass",
        },
        "score_summary": {
            "control_count": len(controls),
            "expected_pass_controls": sum(1 for control in controls if control["expected_status"] == "pass"),
            "expected_fail_controls": sum(1 for control in controls if control["expected_status"] == "fail"),
            "observed_pass_controls": len(pass_controls),
            "observed_blocked_controls": len(blocked_controls),
            "source_candidate_coverage_count": len({str(control["source_candidate_id"]) for control in controls}),
            "source_row_coverage_count": len({str(control["source_row_id"]) for control in controls}),
            "status_mismatch_count": sum(1 for result in results if result["status_match"] is not True),
            "triage_state_mismatch_count": sum(1 for result in results if result["triage_state_match"] is not True),
            "review_outcome_mismatch_count": sum(
                1 for result in results if result["review_outcome_match"] is not True
            ),
        },
        "triage_state_counts": {
            "expected": {state: expected_triage_counts.get(state, 0) for state in sorted(ALLOWED_TRIAGE_STATES)},
            "observed": {state: observed_triage_counts.get(state, 0) for state in sorted(ALLOWED_TRIAGE_STATES)},
        },
        "cross_language_signal_counts": {
            "declared_true": {signal: declared_counts.get(signal, 0) for signal in SIGNAL_ORDER},
            "detected_true": {signal: detected_counts.get(signal, 0) for signal in SIGNAL_ORDER},
            "mismatch_count": sum(
                1
                for result in results
                if result["reviewer_conflict_triage_signals_declared"]
                != result["reviewer_conflict_triage_signals_detected"]
            ),
        },
        "failure_reason_counts": {signal: failure_counts.get(signal, 0) for signal in SIGNAL_ORDER},
        "control_results": results,
        "pass_control_ids": pass_controls,
        "blocked_control_ids": blocked_controls,
        "reviewer_triage": {
            "primary_question": "Does either language remove reviewer hold, collapse compare route, soften reject route, clear unresolved conflict, or relabel triage state.",
            "triage_order": [
                "english_reviewer_hold_removed",
                "turkish_reviewer_hold_removed",
                "compare_route_collapsed",
                "reject_route_softened",
                "unresolved_conflict_cleared",
                "triage_state_mislabeled",
            ],
            "blocked_use": [
                "patient care",
                "clinical advice",
                "translation clearance",
                "reviewer conflict triage clearance",
                "clinical validation claim",
                "clinical deployment claim",
                "model ranking claim",
            ],
        },
        "release_boundary": {
            "synthetic_only": True,
            "patient_data_used": False,
            "clinical_use_allowed": False,
            "clinical_advice_allowed": False,
            "external_urls_present": False,
            "translation_clearance_claim_made": False,
            "reviewer_conflict_triage_clearance_claim_made": False,
            "diagnosis_or_treatment_instruction_allowed": False,
            "clinical_validation_claim_made": False,
            "clinical_deployment_claim_made": False,
            "model_superiority_claim_made": False,
            "model_ranking_claim_made": False,
            "partner_or_institution_claim_made": False,
            "score_certification_claim_made": False,
            "source_truth_certification_claim_made": False,
            "external_publication_clearance": False,
            "allowed_use": "Repo local synthetic cross language reviewer conflict triage scoring before public wording reuse.",
            "not_allowed_use": "Patient care, clinical advice, translation clearance, reviewer conflict triage clearance, external publication clearance, model ranking, or release claim.",
        },
        "blockers": [],
        "exact_next_action": "Add cross language reviewer decision rationale controls so reviewer hold, compare, and reject routes preserve rationale, owner, and unresolved state without creating authority claims.",
    }


def markdown_list(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["score_summary"]
    lines = [
        "# Multilingual Medical Intelligence Cross Language Reviewer Conflict Triage Controls v0.1",
        "",
        f"Date: {DATE}",
        "",
        "Status: ready for local repo review only",
        "",
        "## Purpose",
        "",
        "This report checks whether English and Turkish ASCII variants preserve the reviewer conflict triage map, reviewer hold state, compare route, reject route, unresolved conflict state, and triage state label across the same record.",
        "",
        "It blocks cross language reviewer conflict triage drift when one language removes reviewer hold, collapses compare route, softens reject route, clears unresolved conflict, or relabels triage state as clearance.",
        "",
        "It keeps hold, compare, and reject states attached to the same synthetic source disagreement record.",
        "",
        "The controls use synthetic rows only. They contain no patient data and make no diagnosis, treatment instruction, clinical validation, clinical deployment, model ranking, partner, or institutional claim.",
        "",
        "## Score Summary",
        "",
        *markdown_list(
            [
                f"Control rows: {summary['control_count']}.",
                f"Expected pass controls: {summary['expected_pass_controls']}.",
                f"Expected fail controls: {summary['expected_fail_controls']}.",
                f"Observed pass controls: {summary['observed_pass_controls']}.",
                f"Observed blocked controls: {summary['observed_blocked_controls']}.",
                f"Source candidate coverage count: {summary['source_candidate_coverage_count']}.",
                f"Source row coverage count: {summary['source_row_coverage_count']}.",
            ]
        ),
        "",
        "## Cross Language Signal Counts",
        "",
    ]
    for index, signal in enumerate(SIGNAL_ORDER, 1):
        lines.append(
            f"{index}. `{signal}`: declared {report['cross_language_signal_counts']['declared_true'][signal]}, detected {report['cross_language_signal_counts']['detected_true'][signal]}."
        )

    lines.extend(
        [
            "",
            "## Triage State Counts",
            "",
        ]
    )
    for index, state in enumerate(sorted(ALLOWED_TRIAGE_STATES), 1):
        lines.append(
            f"{index}. `{state}`: expected {report['triage_state_counts']['expected'][state]}, observed {report['triage_state_counts']['observed'][state]}."
        )

    lines.extend(
        [
            "",
            "## Reviewer Triage",
            "",
            report["reviewer_triage"]["primary_question"],
            "",
            "Triage order:",
            "",
            *markdown_list([f"`{item}`" for item in report["reviewer_triage"]["triage_order"]]),
            "",
            "## Release Boundary",
            "",
            "This report supports repo local review only. It does not clear text for patient care, clinical advice, translation clearance, reviewer conflict triage clearance, clinical validation, clinical deployment, model comparison, institutional use, or external publication.",
            "",
            "Boundary note: not score certification, not source clearance, not clinical validation, not clinical deployment, not translation clearance, not reviewer conflict triage clearance, and not external publication clearance.",
            "",
            "## Validation Command",
            "",
            "`make multilingual_medical_intelligence_cross_language_reviewer_conflict_triage_controls`",
            "",
            "Direct check:",
            "",
            "`python3 scripts/score_multilingual_medical_intelligence_cross_language_reviewer_conflict_triage_controls_v0_1_20260625.py --check`",
            "",
            "## Exact Next Action",
            "",
            report["exact_next_action"],
            "",
        ]
    )
    return "\n".join(lines)


def as_json_text(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def validate_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    summary = report.get("score_summary", {})
    expected_summary = {
        "control_count": 12,
        "expected_pass_controls": 6,
        "expected_fail_controls": 6,
        "observed_pass_controls": 6,
        "observed_blocked_controls": 6,
        "source_candidate_coverage_count": 6,
        "source_row_coverage_count": 6,
        "status_mismatch_count": 0,
        "triage_state_mismatch_count": 0,
        "review_outcome_mismatch_count": 0,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"score_summary.{key} must be {expected}")

    counts = report.get("cross_language_signal_counts", {})
    if not isinstance(counts, dict):
        errors.append("cross_language_signal_counts must be an object")
    else:
        for group in ("declared_true", "detected_true"):
            if set(counts.get(group, {})) != set(SIGNAL_ORDER):
                errors.append(f"cross_language_signal_counts.{group} must contain required signals")
        if counts.get("mismatch_count") != 0:
            errors.append("cross_language_signal_counts.mismatch_count must be 0")

    if set(report.get("failure_reason_counts", {})) != set(SIGNAL_ORDER):
        errors.append("failure_reason_counts must contain exactly required signals")

    triage_state_counts = report.get("triage_state_counts", {})
    expected_triage_counts = {"compare": 2, "reject": 7, "reviewer_hold": 3}
    if not isinstance(triage_state_counts, dict):
        errors.append("triage_state_counts must be an object")
    else:
        for group in ("expected", "observed"):
            if triage_state_counts.get(group) != expected_triage_counts:
                errors.append(f"triage_state_counts.{group} must match expected reviewer routing counts")

    results = report.get("control_results")
    if not isinstance(results, list) or len(results) != 12:
        errors.append("control_results must contain 12 rows")
    else:
        pass_rows = [row for row in results if row.get("observed_status") == "pass"]
        fail_rows = [row for row in results if row.get("observed_status") == "fail"]
        if len(pass_rows) != 6:
            errors.append("control_results must contain 6 pass rows")
        if len(fail_rows) != 6:
            errors.append("control_results must contain 6 fail rows")
        for row in results:
            if row.get("status_match") is not True:
                errors.append(f"{row.get('control_id')}: status_match must be true")
            if row.get("expected_triage_state") not in ALLOWED_TRIAGE_STATES:
                errors.append(f"{row.get('control_id')}: expected_triage_state must be valid")
            if row.get("observed_triage_state") not in ALLOWED_TRIAGE_STATES:
                errors.append(f"{row.get('control_id')}: observed_triage_state must be valid")
            if row.get("triage_state_match") is not True:
                errors.append(f"{row.get('control_id')}: triage_state_match must be true")
            if row.get("review_outcome_match") is not True:
                errors.append(f"{row.get('control_id')}: review_outcome_match must be true")
            if row.get("boundary_pass") is not True:
                errors.append(f"{row.get('control_id')}: boundary_pass must be true")

    boundary = report.get("release_boundary")
    if not isinstance(boundary, dict):
        errors.append("release_boundary must be an object")
    else:
        expected_boundary = {
            "synthetic_only": True,
            "patient_data_used": False,
            "clinical_use_allowed": False,
            "clinical_advice_allowed": False,
            "external_urls_present": False,
            "translation_clearance_claim_made": False,
            "reviewer_conflict_triage_clearance_claim_made": False,
            "diagnosis_or_treatment_instruction_allowed": False,
            "clinical_validation_claim_made": False,
            "clinical_deployment_claim_made": False,
            "model_superiority_claim_made": False,
            "model_ranking_claim_made": False,
            "partner_or_institution_claim_made": False,
            "score_certification_claim_made": False,
            "source_truth_certification_claim_made": False,
            "external_publication_clearance": False,
        }
        for key, expected in expected_boundary.items():
            if boundary.get(key) is not expected:
                errors.append(f"release_boundary.{key} must be {expected}")

    for key_path, key in iter_keys(report):
        if normalized_key(key) in PRIVATE_FIELD_NAMES:
            errors.append(f"private identifier field is not allowed: {key_path}")
    for value_path, text in iter_strings(report):
        if EXTERNAL_URL_RE.search(text):
            errors.append(f"external URL is not allowed at {value_path}")
        if EMAIL_RE.search(text):
            errors.append(f"email like value is not allowed at {value_path}")
        for candidate in PHONE_CANDIDATE_RE.findall(text):
            digits = re.sub(r"\D", "", candidate)
            if len(digits) >= 10:
                errors.append(f"phone like value is not allowed at {value_path}")
        lower = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            if f"not {phrase}" in lower:
                continue
            if phrase in lower:
                errors.append(f"forbidden phrase at {value_path}: {phrase}")

    return errors


def validate_markdown(markdown_text: str) -> list[str]:
    errors: list[str] = []
    required_phrases = [
        "cross language reviewer conflict triage drift",
        "English and Turkish ASCII variants",
        "reviewer conflict triage",
        "reviewer conflict triage map",
        "reviewer hold state",
        "compare route",
        "reject route",
        "unresolved conflict state",
        "triage state label",
        "reviewer hold",
        "same synthetic source disagreement record",
        "not score certification",
        "not source clearance",
        "not clinical validation",
        "not clinical deployment",
        "not translation clearance",
        "not reviewer conflict triage clearance",
        "not external publication clearance",
        "make multilingual_medical_intelligence_cross_language_reviewer_conflict_triage_controls",
    ]
    lower = markdown_text.lower()
    for phrase in required_phrases:
        if phrase.lower() not in lower:
            errors.append(f"Markdown missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if f"not {phrase}" in lower:
            continue
        if phrase in lower:
            errors.append(f"Markdown contains forbidden phrase: {phrase}")
    return errors


def run(check: bool) -> int:
    errors: list[str] = []
    for path in (REWRITE_CANDIDATES, CROSS_LANGUAGE_CONTROLS):
        if not path.exists():
            errors.append(f"missing required file: {repo_relative(path)}")
    if errors:
        print("FAIL cross language reviewer conflict triage controls")
        for error in errors:
            print(f"- {error}")
        return 1

    try:
        rewrite_candidates = load_jsonl(REWRITE_CANDIDATES)
        controls = load_jsonl(CROSS_LANGUAGE_CONTROLS)
    except ValueError as error:
        print(f"FAIL cross language reviewer conflict triage controls: {error}")
        return 1

    errors.extend(validate_control_rows(controls, rewrite_candidates))
    report = build_report(controls, rewrite_candidates)
    errors.extend(validate_report(report))
    markdown = render_markdown(report)
    errors.extend(validate_markdown(markdown))

    if check:
        if not OUTPUT_JSON.exists():
            errors.append(f"missing generated JSON report: {repo_relative(OUTPUT_JSON)}")
        elif OUTPUT_JSON.read_text(encoding="utf-8") != as_json_text(report):
            errors.append(f"stale JSON report: {repo_relative(OUTPUT_JSON)}")
        if not OUTPUT_MARKDOWN.exists():
            errors.append(f"missing generated Markdown report: {repo_relative(OUTPUT_MARKDOWN)}")
        elif OUTPUT_MARKDOWN.read_text(encoding="utf-8") != markdown:
            errors.append(f"stale Markdown report: {repo_relative(OUTPUT_MARKDOWN)}")

    if errors:
        print("FAIL cross language reviewer conflict triage controls")
        for error in errors:
            print(f"- {error}")
        return 1

    if check:
        print("PASS cross language reviewer conflict triage controls")
        print(f"controls={report['score_summary']['control_count']}")
        print(f"blocked_controls={report['score_summary']['observed_blocked_controls']}")
        print(f"pass_controls={report['score_summary']['observed_pass_controls']}")
        return 0

    OUTPUT_JSON.write_text(as_json_text(report), encoding="utf-8")
    OUTPUT_MARKDOWN.write_text(markdown, encoding="utf-8")
    print(f"Wrote {repo_relative(OUTPUT_JSON)}")
    print(f"Wrote {repo_relative(OUTPUT_MARKDOWN)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return run(check=args.check)


if __name__ == "__main__":
    sys.exit(main())
