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
ATLAS_NODE_ID = "mia_mmi_017"

REWRITE_CANDIDATES = ROOT / "data" / "multilingual_medical_intelligence_public_wording_rewrite_candidates_v0_1_20260625.jsonl"
CROSS_LANGUAGE_CONTROLS = ROOT / "data" / "multilingual_medical_intelligence_rewrite_candidate_cross_language_reviewer_closeout_ledger_reconciliation_controls_v0_1_20260625.jsonl"
OUTPUT_JSON = ROOT / "data" / "multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_report_v0_1_20260625.json"
OUTPUT_MARKDOWN = ROOT / "docs" / "MULTILINGUAL_MEDICAL_INTELLIGENCE_CROSS_LANGUAGE_REVIEWER_CLOSEOUT_LEDGER_RECONCILIATION_REPORT_V0_1_20260625.md"

SIGNAL_ORDER = [
    "closeout_decision_reconciliation_mismatch",
    "dissent_note_reconciliation_mismatch",
    "owner_final_state_reconciliation_mismatch",
    "unresolved_branch_closure_boundary_reconciliation_mismatch",
    "closure_comparison_result_reconciliation_mismatch",
    "authority_or_clearance_claim_created",
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
    "source_closeout_control_id",
    "source_closeout_claim_id",
    "export_control_id",
    "exported_ledger_claim_id",
    "language_pair",
    "clinical_domain",
    "control_type",
    "english_text",
    "turkish_ascii_text",
    "reviewer_closeout_ledger_reconciliation_map",
    "expected_status",
    "expected_decision_route",
    "expected_failure_reasons",
    "reviewer_closeout_ledger_reconciliation_signals",
    "expected_review_outcome",
    "release_boundary",
}

ALLOWED_CONTROL_TYPES = {
    "aligned_closeout_decision_reconciled",
    "closeout_decision_reconciliation_mismatch",
    "aligned_dissent_note_reconciled",
    "dissent_note_reconciliation_mismatch",
    "aligned_owner_final_state_reconciled",
    "owner_final_state_reconciliation_mismatch",
    "aligned_unresolved_branch_closure_boundary_reconciled",
    "unresolved_branch_closure_boundary_reconciliation_mismatch",
    "aligned_closure_comparison_result_reconciled",
    "closure_comparison_result_reconciliation_mismatch",
    "aligned_authority_or_clearance_claim_absent",
    "authority_or_clearance_claim_created",
}

EXPECTED_BOUNDARY_FLAGS = {
    "synthetic_only": True,
    "patient_data_used": False,
    "clinical_use_allowed": False,
    "clinical_advice_allowed": False,
    "external_urls_present": False,
}

REVIEWER_CLOSEOUT_LEDGER_RECONCILIATION_MAP_REQUIRED_FIELDS = {
    "claim_id",
    "source_scope",
    "source_closeout_control_id",
    "source_closeout_claim_id",
    "export_control_id",
    "exported_ledger_claim_id",
    "source_closeout_decision_to_match",
    "exported_closeout_decision_to_match",
    "source_dissent_note_to_match",
    "exported_dissent_note_to_match",
    "source_owner_final_state_to_match",
    "exported_owner_final_state_to_match",
    "source_unresolved_branch_closure_boundary_to_match",
    "exported_unresolved_branch_closure_boundary_to_match",
    "source_closure_comparison_result_to_match",
    "exported_closure_comparison_result_to_match",
    "source_decision_route_to_match",
    "exported_decision_route_to_match",
    "ledger_reconciliation_boundary",
    "forbidden_authority_or_clearance_claim",
    "reuse_boundary",
}

ALLOWED_DECISION_ROUTES = {"reviewer_hold", "compare", "reject"}

CLOSEOUT_DECISION_RECONCILIATION_MISMATCH_RE = re.compile(
    r"\b(closeout decision reconciliation mismatch|kapanis karari uzlastirma uyusmazligi)\b",
    re.IGNORECASE,
)
DISSENT_NOTE_RECONCILIATION_MISMATCH_RE = re.compile(
    r"\b(dissent note reconciliation mismatch|itiraz notu uzlastirma uyusmazligi)\b",
    re.IGNORECASE,
)
OWNER_FINAL_STATE_RECONCILIATION_MISMATCH_RE = re.compile(
    r"\b(owner final state reconciliation mismatch|sahip son durum uzlastirma uyusmazligi)\b",
    re.IGNORECASE,
)
UNRESOLVED_BRANCH_CLOSURE_BOUNDARY_RECONCILIATION_MISMATCH_RE = re.compile(
    r"\b(unresolved branch closure boundary reconciliation mismatch|cozulmemis dal kapanis siniri uzlastirma uyusmazligi)\b",
    re.IGNORECASE,
)
CLOSURE_COMPARISON_RESULT_RECONCILIATION_MISMATCH_RE = re.compile(
    r"\b(closure comparison result reconciliation mismatch|kapanis karsilastirma sonucu uzlastirma uyusmazligi)\b",
    re.IGNORECASE,
)
AUTHORITY_OR_CLEARANCE_CLAIM_CREATED_RE = re.compile(
    r"\b(authority or clearance claim created|authority or clearance claim is created|otorite veya clearance iddiasi olusturuldu)\b",
    re.IGNORECASE,
)


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def detected_signals(row: dict[str, Any]) -> dict[str, bool]:
    english_text = str(row.get("english_text", ""))
    turkish_text = str(row.get("turkish_ascii_text", ""))
    joined = f"{english_text} {turkish_text}"
    return {
        "closeout_decision_reconciliation_mismatch": bool(CLOSEOUT_DECISION_RECONCILIATION_MISMATCH_RE.search(joined)),
        "dissent_note_reconciliation_mismatch": bool(DISSENT_NOTE_RECONCILIATION_MISMATCH_RE.search(joined)),
        "owner_final_state_reconciliation_mismatch": bool(OWNER_FINAL_STATE_RECONCILIATION_MISMATCH_RE.search(joined)),
        "unresolved_branch_closure_boundary_reconciliation_mismatch": bool(UNRESOLVED_BRANCH_CLOSURE_BOUNDARY_RECONCILIATION_MISMATCH_RE.search(joined)),
        "closure_comparison_result_reconciliation_mismatch": bool(CLOSURE_COMPARISON_RESULT_RECONCILIATION_MISMATCH_RE.search(joined)),
        "authority_or_clearance_claim_created": bool(AUTHORITY_OR_CLEARANCE_CLAIM_CREATED_RE.search(joined)),
    }


def signal_object(signals: list[str]) -> dict[str, bool]:
    signal_set = set(signals)
    return {signal: signal in signal_set for signal in SIGNAL_ORDER}


def true_signals(row: dict[str, Any]) -> list[str]:
    signals = row.get("reviewer_closeout_ledger_reconciliation_signals")
    if not isinstance(signals, dict):
        return []
    return [signal for signal in SIGNAL_ORDER if signals.get(signal) is True]


def observed_decision_route(row: dict[str, Any], detected: list[str]) -> str:
    if detected:
        return "reject"
    control_type = str(row.get("control_type", ""))
    if control_type in {"aligned_owner_final_state_reconciled", "aligned_closure_comparison_result_reconciled"}:
        return "compare"
    if control_type == "aligned_authority_or_clearance_claim_absent":
        return "reject"
    return "reviewer_hold"


def validate_control_rows(
    controls: list[dict[str, Any]],
    rewrite_candidates: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    candidates_by_id = {str(row.get("candidate_id")): row for row in rewrite_candidates}

    if len(controls) != 12:
        errors.append(f"Expected 12 cross language reviewer closeout ledger reconciliation controls, found {len(controls)}")

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
            r"MMI_CROSS_LANGUAGE_REVIEWER_CLOSEOUT_LEDGER_RECONCILIATION_\d{3}", control_id
        ):
            errors.append(f"{label}: control_id must match MMI_CROSS_LANGUAGE_REVIEWER_CLOSEOUT_LEDGER_RECONCILIATION_NNN")
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

        reconciliation_map = row.get("reviewer_closeout_ledger_reconciliation_map")
        if not isinstance(reconciliation_map, list) or not reconciliation_map:
            errors.append(f"{label}: reviewer_closeout_ledger_reconciliation_map must be a nonempty list")
        else:
            for map_index, map_row in enumerate(reconciliation_map, 1):
                if not isinstance(map_row, dict):
                    errors.append(f"{label}: reviewer_closeout_ledger_reconciliation_map[{map_index}] must be an object")
                    continue
                missing_map_fields = sorted(REVIEWER_CLOSEOUT_LEDGER_RECONCILIATION_MAP_REQUIRED_FIELDS - set(map_row))
                if missing_map_fields:
                    errors.append(
                        f"{label}: reviewer_closeout_ledger_reconciliation_map[{map_index}] missing fields: {', '.join(missing_map_fields)}"
                    )
                identifier_fields = {
                    "source_closeout_control_id",
                    "source_closeout_claim_id",
                    "export_control_id",
                    "exported_ledger_claim_id",
                }
                for map_field in REVIEWER_CLOSEOUT_LEDGER_RECONCILIATION_MAP_REQUIRED_FIELDS:
                    map_value = map_row.get(map_field)
                    if map_field == "claim_id":
                        if not isinstance(map_value, str) or not re.fullmatch(r"mmi_closeout_ledger_reconciliation_claim_\d{3}", map_value):
                            errors.append(
                                f"{label}: reviewer_closeout_ledger_reconciliation_map[{map_index}].claim_id must match mmi_closeout_ledger_reconciliation_claim_NNN"
                            )
                        continue
                    if map_field in identifier_fields:
                        if not isinstance(map_value, str) or len(map_value) < 8:
                            errors.append(
                                f"{label}: reviewer_closeout_ledger_reconciliation_map[{map_index}].{map_field} must be a stable identifier"
                            )
                        continue
                    if not isinstance(map_value, str) or len(map_value.split()) < 3:
                        errors.append(
                            f"{label}: reviewer_closeout_ledger_reconciliation_map[{map_index}].{map_field} must contain at least 3 words"
                        )

        expected_status = row.get("expected_status")
        if expected_status == "pass":
            pass_count += 1
        elif expected_status == "fail":
            fail_count += 1
        else:
            errors.append(f"{label}: expected_status must be pass or fail")
        if row.get("expected_decision_route") not in ALLOWED_DECISION_ROUTES:
            errors.append(f"{label}: expected_decision_route must be reviewer_hold, compare, or reject")
        if row.get("expected_review_outcome") != "routes_to_cross_language_reviewer_closeout_ledger_reconciliation_state":
            errors.append(f"{label}: expected_review_outcome must route to reviewer closeout ledger reconciliation state")

        declared_signals = row.get("reviewer_closeout_ledger_reconciliation_signals")
        expected_reasons = row.get("expected_failure_reasons")
        if not isinstance(declared_signals, dict) or set(declared_signals) != set(SIGNAL_ORDER):
            errors.append(f"{label}: reviewer_closeout_ledger_reconciliation_signals must exactly match required signal keys")
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
        if row.get("expected_decision_route") != observed_decision_route(row, observed_signal_names):
            errors.append(f"{label}: expected_decision_route does not match observed decision routing")
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
            f"Expected cross language reviewer closeout ledger reconciliation controls to cover 6 source candidates, found {len(covered_candidate_ids)}"
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
    expected_route_counts: Counter[str] = Counter()
    observed_route_counts: Counter[str] = Counter()
    pass_controls: list[str] = []
    blocked_controls: list[str] = []
    results: list[dict[str, Any]] = []

    for control in controls:
        candidate = candidates_by_id[str(control["source_candidate_id"])]
        declared = true_signals(control)
        detected = [signal for signal, value in detected_signals(control).items() if value is True]
        observed_route = observed_decision_route(control, detected)
        expected_route = str(control["expected_decision_route"])
        expected_reasons = [str(reason) for reason in control["expected_failure_reasons"]]
        declared_counts.update(declared)
        detected_counts.update(detected)
        failure_counts.update(expected_reasons)
        expected_route_counts.update([expected_route])
        observed_route_counts.update([observed_route])

        observed_status = "fail" if detected else "pass"
        review_outcome = "routes_to_cross_language_reviewer_closeout_ledger_reconciliation_state"
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
                "expected_decision_route": expected_route,
                "observed_decision_route": observed_route,
                "decision_route_match": expected_route == observed_route,
                "expected_review_outcome": control["expected_review_outcome"],
                "observed_review_outcome": review_outcome,
                "status_match": control["expected_status"] == observed_status,
                "review_outcome_match": control["expected_review_outcome"] == review_outcome,
                "expected_failure_reasons": expected_reasons,
                "reviewer_closeout_ledger_reconciliation_map": control["reviewer_closeout_ledger_reconciliation_map"],
                "detected_reviewer_closeout_ledger_reconciliation_signals": detected,
                "reviewer_closeout_ledger_reconciliation_signals_declared": signal_object(declared),
                "reviewer_closeout_ledger_reconciliation_signals_detected": signal_object(detected),
                "source_candidate_expected_status": candidate["expected_status"],
                "boundary_pass": True,
            }
        )

    return {
        "report_id": "multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_report_v0_1_20260625",
        "report_type": "machine_readable_cross_language_reviewer_closeout_ledger_reconciliation_report",
        "report_version": VERSION,
        "generated_date": DATE_TOKEN,
        "atlas_layer": ATLAS_LAYER,
        "atlas_node_id": ATLAS_NODE_ID,
        "status": "local_fixture_pass",
        "report_scope": "local_fixture_cross_language_reviewer_closeout_ledger_reconciliation_gate_only",
        "scope": "Local synthetic cross language controls for reconciling exported closeout ledger rows back to source closeout state, source closeout id, exported ledger row id, reconciliation comparison key, source closeout state, ledger source state match result, and authority or clearance claim drift.",
        "artifact_paths": {
            "rewrite_candidates": repo_relative(REWRITE_CANDIDATES),
            "cross_language_controls": repo_relative(CROSS_LANGUAGE_CONTROLS),
            "cross_language_report_json": repo_relative(OUTPUT_JSON),
            "cross_language_report_markdown": repo_relative(OUTPUT_MARKDOWN),
            "scorer": "scripts/score_multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_controls_v0_1_20260625.py",
            "validator": "scripts/validate_multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_report_v0_1_20260625.py",
        },
        "validation": {
            "scorer_command": "python3 scripts/score_multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_controls_v0_1_20260625.py --check",
            "validator_command": "python3 scripts/validate_multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_report_v0_1_20260625.py",
            "make_target": "make multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_controls",
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
            "decision_route_mismatch_count": sum(1 for result in results if result["decision_route_match"] is not True),
            "review_outcome_mismatch_count": sum(1 for result in results if result["review_outcome_match"] is not True),
        },
        "decision_route_counts": {
            "expected": {route: expected_route_counts.get(route, 0) for route in sorted(ALLOWED_DECISION_ROUTES)},
            "observed": {route: observed_route_counts.get(route, 0) for route in sorted(ALLOWED_DECISION_ROUTES)},
        },
        "cross_language_signal_counts": {
            "declared_true": {signal: declared_counts.get(signal, 0) for signal in SIGNAL_ORDER},
            "detected_true": {signal: detected_counts.get(signal, 0) for signal in SIGNAL_ORDER},
            "mismatch_count": sum(
                1
                for result in results
                if result["reviewer_closeout_ledger_reconciliation_signals_declared"]
                != result["reviewer_closeout_ledger_reconciliation_signals_detected"]
            ),
        },
        "failure_reason_counts": {signal: failure_counts.get(signal, 0) for signal in SIGNAL_ORDER},
        "control_results": results,
        "pass_control_ids": pass_controls,
        "blocked_control_ids": blocked_controls,
        "reviewer_closeout_ledger_reconciliation": {
            "primary_question": "Can exported closeout ledger rows be compared back to source closeout state without closeout decision mismatch, dissent note mismatch, owner final state mismatch, unresolved branch closure boundary mismatch, closure comparison result mismatch, or authority or clearance claim.",
            "decision_order": SIGNAL_ORDER,
            "blocked_use": [
                "patient care",
                "clinical advice",
                "translation clearance",
                "reviewer closeout ledger reconciliation clearance",
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
            "reviewer_closeout_ledger_reconciliation_clearance_claim_made": False,
            "authority_or_clearance_claim_made": False,
            "authority_claim_made": False,
            "diagnosis_or_treatment_instruction_allowed": False,
            "clinical_validation_claim_made": False,
            "clinical_deployment_claim_made": False,
            "model_superiority_claim_made": False,
            "model_ranking_claim_made": False,
            "partner_or_institution_claim_made": False,
            "score_certification_claim_made": False,
            "source_truth_certification_claim_made": False,
            "external_publication_clearance": False,
            "allowed_use": "Repo local synthetic cross language reviewer closeout ledger reconciliation scoring before public wording reuse.",
            "not_allowed_use": "Patient care, clinical advice, translation clearance, reviewer closeout ledger reconciliation clearance, external publication clearance, model ranking, or authority or clearance claim.",
        },
        "blockers": [],
        "exact_next_action": "Add cross language reviewer closeout ledger reconciliation exception controls so mismatch exceptions keep source closeout id, exported ledger row id, owner final state, dissent note, and unresolved branch closure boundary attached without authority or clearance claim.",
    }


def markdown_list(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["score_summary"]
    lines = [
        "# Multilingual Medical Intelligence Cross Language Reviewer Closeout Ledger Reconciliation Controls v0.1",
        "",
        f"Date: {DATE}",
        "",
        "Status: ready for local repo review only",
        "",
        "## Purpose",
        "",
        "This report checks whether exported closeout ledger rows can be compared back to source closeout state in English and Turkish ASCII variants.",
        "",
        "It blocks reconciliation drift when one language creates closeout decision mismatch, dissent note mismatch, owner final state mismatch, unresolved branch closure boundary mismatch, closure comparison result mismatch, or creates an authority or clearance claim.",
        "",
        "It keeps source closeout id, exported ledger row id, closeout decision, dissent note, owner final state, unresolved branch closure boundary, closure comparison result, source route, and exported route attached before reviewer hold, compare, reject, and ledger reuse decisions.",
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
    declared = report["cross_language_signal_counts"]["declared_true"]
    detected = report["cross_language_signal_counts"]["detected_true"]
    lines.extend(
        markdown_list([f"`{signal}`: declared {declared[signal]}, detected {detected[signal]}." for signal in SIGNAL_ORDER])
    )
    lines.extend(
        [
            "",
            "## Decision Route Counts",
            "",
        ]
    )
    lines.extend(
        markdown_list(
            [
                f"`{route}`: expected {report['decision_route_counts']['expected'][route]}, "
                f"observed {report['decision_route_counts']['observed'][route]}."
                for route in sorted(ALLOWED_DECISION_ROUTES)
            ]
        )
    )
    lines.extend(
        [
            "",
            "## Reviewer Closeout Ledger Reconciliation",
            "",
            report["reviewer_closeout_ledger_reconciliation"]["primary_question"],
            "",
            "Decision order:",
            "",
            *markdown_list([f"`{signal}`" for signal in SIGNAL_ORDER]),
            "",
            "Plain signal names: closeout decision reconciliation mismatch; dissent note reconciliation mismatch; owner final state reconciliation mismatch; unresolved branch closure boundary reconciliation mismatch; closure comparison result reconciliation mismatch; authority or clearance claim created.",
            "",
            "## Release Boundary",
            "",
            "This report supports repo local review only. It does not clear text for patient care, clinical advice, translation clearance, reviewer closeout ledger reconciliation clearance, clinical validation, clinical deployment, model comparison, institutional use, or external publication.",
            "",
            "Boundary note: not score certification, not source clearance, not clinical validation, not clinical deployment, not translation clearance, not reviewer closeout ledger reconciliation clearance, not authority or clearance claim, and not external publication clearance.",
            "",
            "## Validation Command",
            "",
            "`make multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_controls`",
            "",
            "Direct check:",
            "",
            "`python3 scripts/score_multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_controls_v0_1_20260625.py --check`",
            "",
            "## Exact Next Action",
            "",
            report["exact_next_action"],
            "",
        ]
    )
    return "\n".join(lines)


def validate_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("report_id") != "multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_report_v0_1_20260625":
        errors.append("report_id mismatch")
    if report.get("atlas_node_id") != ATLAS_NODE_ID:
        errors.append(f"atlas_node_id must be {ATLAS_NODE_ID}")
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
        "decision_route_mismatch_count": 0,
        "review_outcome_mismatch_count": 0,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"score_summary.{key} must be {expected}")
    signal_counts = report.get("cross_language_signal_counts", {})
    declared = signal_counts.get("declared_true", {})
    detected = signal_counts.get("detected_true", {})
    for signal in SIGNAL_ORDER:
        if declared.get(signal) != 1:
            errors.append(f"declared signal count for {signal} must be 1")
        if detected.get(signal) != 1:
            errors.append(f"detected signal count for {signal} must be 1")
    if signal_counts.get("mismatch_count") != 0:
        errors.append("signal mismatch count must be 0")
    routes = report.get("decision_route_counts", {})
    if routes.get("expected") != {"compare": 2, "reject": 7, "reviewer_hold": 3}:
        errors.append("expected decision route counts mismatch")
    if routes.get("observed") != {"compare": 2, "reject": 7, "reviewer_hold": 3}:
        errors.append("observed decision route counts mismatch")
    boundary = report.get("release_boundary", {})
    required_false = [
        "clinical_validation_claim_made",
        "clinical_deployment_claim_made",
        "model_superiority_claim_made",
        "model_ranking_claim_made",
        "partner_or_institution_claim_made",
        "reviewer_closeout_ledger_reconciliation_clearance_claim_made",
        "authority_or_clearance_claim_made",
        "external_publication_clearance",
    ]
    if boundary.get("synthetic_only") is not True:
        errors.append("release boundary must be synthetic only")
    for key in required_false:
        if boundary.get(key) is not False:
            errors.append(f"release_boundary.{key} must be false")
    return errors


def validate_markdown(markdown: str) -> list[str]:
    errors: list[str] = []
    required = [
        "Cross Language Reviewer Closeout Ledger Reconciliation Controls",
        "closeout decision reconciliation mismatch",
        "dissent note reconciliation mismatch",
        "owner final state reconciliation mismatch",
        "unresolved branch closure boundary reconciliation mismatch",
        "closure comparison result reconciliation mismatch",
        "reviewer closeout ledger reconciliation clearance",
        "not authority or clearance claim",
        "make multilingual_medical_intelligence_cross_language_reviewer_closeout_ledger_reconciliation_controls",
    ]
    lower = markdown.lower()
    for phrase in required:
        if phrase.lower() not in lower:
            errors.append(f"markdown missing phrase: {phrase}")
    return errors


def as_json_text(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rewrite_candidates = load_jsonl(REWRITE_CANDIDATES)
    controls = load_jsonl(CROSS_LANGUAGE_CONTROLS)
    errors = validate_control_rows(controls, rewrite_candidates)
    report = build_report(controls, rewrite_candidates)
    errors.extend(validate_report(report))
    markdown = render_markdown(report)
    errors.extend(validate_markdown(markdown))

    if errors:
        print("FAIL cross language reviewer closeout ledger reconciliation controls")
        for error in errors:
            print(f"- {error}")
        return 1

    json_text = as_json_text(report)
    if args.check:
        stale = []
        if not OUTPUT_JSON.exists() or OUTPUT_JSON.read_text(encoding="utf-8") != json_text:
            stale.append(repo_relative(OUTPUT_JSON))
        if not OUTPUT_MARKDOWN.exists() or OUTPUT_MARKDOWN.read_text(encoding="utf-8") != markdown:
            stale.append(repo_relative(OUTPUT_MARKDOWN))
        if stale:
            print("FAIL cross language reviewer closeout ledger reconciliation controls: stale outputs")
            for path in stale:
                print(f"- {path}")
            return 1
    else:
        OUTPUT_JSON.write_text(json_text, encoding="utf-8")
        OUTPUT_MARKDOWN.write_text(markdown, encoding="utf-8")

    print("PASS cross language reviewer closeout ledger reconciliation controls")
    print(f"controls={report['score_summary']['control_count']}")
    print(f"blocked_controls={report['score_summary']['observed_blocked_controls']}")
    print(f"pass_controls={report['score_summary']['observed_pass_controls']}")
    print(f"json={repo_relative(OUTPUT_JSON)}")
    print(f"markdown={repo_relative(OUTPUT_MARKDOWN)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
