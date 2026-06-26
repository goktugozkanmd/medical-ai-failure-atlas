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
ATLAS_NODE_ID = "mia_mmi_075"

REWRITE_CANDIDATES = ROOT / "data" / "multilingual_medical_intelligence_public_wording_rewrite_candidates_v0_1_20260625.jsonl"
CROSS_LANGUAGE_CONTROLS = ROOT / "data" / "mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_controls_v0_1_20260625.jsonl"
OUTPUT_JSON = ROOT / "data" / "mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_report_v0_1_20260625.json"
OUTPUT_MARKDOWN = ROOT / "docs" / "MMI_075_ARCHIVE_REUSE_RELEASE_HANDOFF_CLOSURE_ARCHIVE_REUSE_RELEASE_HANDOFF_CLOSURE_REPORT_V0_1_20260625.md"

SIGNAL_ORDER = [
    "source_closeout_id_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "exported_ledger_row_id_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "owner_final_state_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "dissent_note_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "unresolved_branch_archive_boundary_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "archive_snapshot_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "archive_reopenability_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
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
    "language_pair",
    "clinical_domain",
    "control_type",
    "english_text",
    "turkish_ascii_text",
    "source_exception_control_id",
    "source_exception_claim_id",
    "archive_reuse_release_handoff_closure_archive_reuse_release_control_id",
    "source_archive_reuse_release_handoff_closure_archive_reuse_release_control_id",
    "source_archive_reuse_release_handoff_closure_archive_reuse_release_claim_id",
    "archive_reuse_release_handoff_closure_archive_reuse_release_map",
    "archive_reuse_release_handoff_closure_archive_reuse_release_signals",
    "expected_status",
    "expected_decision_route",
    "expected_failure_reasons",
    "expected_review_outcome",
    "release_boundary",
}

ALLOWED_CONTROL_TYPES = {
    "aligned_source_closeout_id_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
    "source_closeout_id_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "aligned_exported_ledger_row_id_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
    "exported_ledger_row_id_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "aligned_owner_final_state_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
    "owner_final_state_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "aligned_dissent_note_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
    "dissent_note_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "aligned_unresolved_branch_archive_boundary_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
    "unresolved_branch_archive_boundary_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "aligned_archive_snapshot_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
    "archive_snapshot_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "aligned_archive_reopenability_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
    "archive_reopenability_archive_reuse_release_handoff_closure_archive_reuse_release_lost",
    "aligned_authority_or_clearance_claim_absent",
    "authority_or_clearance_claim_created",
}

EXPECTED_BOUNDARY_FLAGS = {
    "synthetic_only": True,
    "patient_data_used": False,
    "patient_data_requested": False,
    "private_clinical_text_used": False,
    "raw_clinical_notes_used": False,
    "private_model_outputs_used": False,
    "endpoint_results_used": False,
    "diagnosis_or_treatment_instruction_allowed": False,
    "model_comparison_claim_made": False,
    "partner_claim_made": False,
    "institution_claim_made": False,
    "regulatory_claim_made": False,
    "publication_claim_made": False,
    "authority_claim_made": False,
    "clearance_claim_made": False,
    "endorsement_claim_made": False,
    "requires_user_approval_before_outward_use": True,
    "clinical_use_allowed": False,
    "clinical_advice_allowed": False,
    "external_urls_present": False,
    "regulatory_clearance_claim_made": False,
    "publication_readiness_claim_made": False,
    "clinical_use_clearance_claim_made": False,
    "clinical_validation_claim_made": False,
    "clinical_deployment_claim_made": False,
    "model_ranking_claim_made": False,
    "model_superiority_claim_made": False,
    "partner_or_institution_claim_made": False,
    "authority_or_clearance_claim_made": False,
    "score_certification_claim_made": False,
    "source_truth_certification_claim_made": False,
    "external_publication_clearance": False,
}

REPLAY_MAP_REQUIRED_FIELDS = {
    "claim_id",
    "source_scope",
    "source_exception_control_id",
    "source_exception_claim_id",
    "source_closeout_id_replay_to_keep",
    "exported_ledger_row_id_replay_to_keep",
    "owner_final_state_replay_to_keep",
    "dissent_note_replay_to_keep",
    "unresolved_branch_archive_boundary_replay_to_keep",
    "exception_reason_replay_to_keep",
    "recheck_trace_to_keep",
    "handoff_trace_to_keep",
    "replay_result_to_match",
    "source_decision_route_to_match",
    "exported_decision_route_to_match",
    "recheck_handoff_replay_boundary",
    "forbidden_authority_or_clearance_claim",
    "reuse_boundary",
    "source_exception_replay_archive_control_id",
    "source_exception_replay_archive_claim_id",
    "archive_snapshot_reopenability_to_keep",
    "rollup_summary_boundary",
    "rollup_reopenability_to_keep",
    "archive_rollup_result_to_match",
    "rollup_forbidden_claim_boundary",
    "source_archive_reuse_release_handoff_closure_archive_reuse_release_control_id",
    "source_archive_reuse_release_handoff_closure_archive_reuse_release_claim_id",
    "closure_archive_reuse_boundary",
    "closure_archive_reuse_reopenability_to_keep",
}

ALLOWED_DECISION_ROUTES = {"reviewer_hold", "compare", "reject"}
SIGNAL_PATTERNS = {
    "source_closeout_id_archive_reuse_release_handoff_closure_archive_reuse_release_lost": re.compile(r"\b(source closeout id archive reuse release handoff closure archive reuse release handoff closure lost|kaynak kapanis id archive reuse release handoff closure archive reuse release handoff closure kayboldu)\b", re.IGNORECASE),
    "exported_ledger_row_id_archive_reuse_release_handoff_closure_archive_reuse_release_lost": re.compile(r"\b(exported ledger row id archive reuse release handoff closure archive reuse release handoff closure lost|exported ledger row id archive reuse release handoff closure archive reuse release handoff closure kayboldu)\b", re.IGNORECASE),
    "owner_final_state_archive_reuse_release_handoff_closure_archive_reuse_release_lost": re.compile(r"\b(owner final state archive reuse release handoff closure archive reuse release handoff closure lost|sahip son durum archive reuse release handoff closure archive reuse release handoff closure kayboldu)\b", re.IGNORECASE),
    "dissent_note_archive_reuse_release_handoff_closure_archive_reuse_release_lost": re.compile(r"\b(dissent note archive reuse release handoff closure archive reuse release handoff closure lost|itiraz notu archive reuse release handoff closure archive reuse release handoff closure kayboldu)\b", re.IGNORECASE),
    "unresolved_branch_archive_boundary_archive_reuse_release_handoff_closure_archive_reuse_release_lost": re.compile(r"\b(unresolved branch archive boundary archive reuse release handoff closure archive reuse release handoff closure lost|cozulmemis dal kapanis siniri archive reuse release handoff closure archive reuse release handoff closure kayboldu)\b", re.IGNORECASE),
    "archive_snapshot_archive_reuse_release_handoff_closure_archive_reuse_release_lost": re.compile(r"\b(archive snapshot archive reuse release handoff closure archive reuse release handoff closure lost|archive snapshot archive reuse release handoff closure archive reuse release handoff closure kayboldu)\b", re.IGNORECASE),
    "archive_reopenability_archive_reuse_release_handoff_closure_archive_reuse_release_lost": re.compile(r"\b(archive reopenability archive reuse release handoff closure archive reuse release handoff closure lost|archive reopenability archive reuse release handoff closure archive reuse release handoff closure kayboldu)\b", re.IGNORECASE),
    "authority_or_clearance_claim_created": re.compile(
        r"\b(authority or clearance claim created|officially cleared|publication ready|accepted for publication|peer reviewed|journal cleared|"
        r"clinically validated|validated on real patient data|validated for clinical use|safe for clinical use|ready for deployment in clinics|"
        r"clinical deployment ready|hospital ready|clinical grade|partner approved|partner confirmed|official partner|institutional backing|"
        r"institutional support|regulatory cleared|cleared by regulators|fda approved|ce marked|ministry approved|official guidance|"
        r"best model|top performing|ranked first|benchmark winner|outperforms|superior model|sota|"
        r"otorite veya clearance iddiasi olusturuldu|resmen onaylandi|klinik olarak valide|klinik kullanim icin onayli|"
        r"sahada kullanima hazir|hastane kullanimi icin hazir|en iyi model|birinci sirada|partner onayli|kurum onayli|"
        r"bakanlik onayli|regulasyon onayi|yayin icin hazir|hakemden gecti)\b",
        re.IGNORECASE,
    ),
}


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def detected_signals(row: dict[str, Any]) -> dict[str, bool]:
    joined = f"{row.get('english_text', '')} {row.get('turkish_ascii_text', '')}"
    return {signal: bool(pattern.search(joined)) for signal, pattern in SIGNAL_PATTERNS.items()}


def signal_object(signals: list[str]) -> dict[str, bool]:
    signal_set = set(signals)
    return {signal: signal in signal_set for signal in SIGNAL_ORDER}


def true_signals(row: dict[str, Any]) -> list[str]:
    signals = row.get("archive_reuse_release_handoff_closure_archive_reuse_release_signals")
    if not isinstance(signals, dict):
        return []
    return [signal for signal in SIGNAL_ORDER if signals.get(signal) is True]


def observed_decision_route(row: dict[str, Any], detected: list[str]) -> str:
    if detected:
        return "reject"
    control_type = str(row.get("control_type", ""))
    if control_type in {
        "aligned_owner_final_state_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
        "aligned_unresolved_branch_archive_boundary_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
        "aligned_archive_snapshot_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
        "aligned_archive_reopenability_exception_replay_archive_rollup_release_handoff_archive_reuse_release_handoff_closure_archive_reuse_release_attached",
    }:
        return "compare"
    if control_type == "aligned_authority_or_clearance_claim_absent":
        return "reject"
    return "reviewer_hold"


def validate_control_rows(controls: list[dict[str, Any]], rewrite_candidates: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    candidates_by_id = {str(row.get("candidate_id")): row for row in rewrite_candidates}
    if len(controls) != 16:
        errors.append(f"Expected 16 archive reuse release handoff closure archive reuse release handoff closure controls, found {len(controls)}")
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
        if not isinstance(control_id, str) or not re.fullmatch(r"MMI_CROSS_LANGUAGE_REVIEWER_ARCHIVE_REUSE_RELEASE_HANDOFF_CLOSURE_ARCHIVE_REUSE_RELEASE_HANDOFF_CLOSURE_CLOSURE_HANDOFF_\d{3}", control_id):
            errors.append(f"{label}: control_id must match MMI_CROSS_LANGUAGE_REVIEWER_ARCHIVE_REUSE_RELEASE_HANDOFF_CLOSURE_ARCHIVE_REUSE_RELEASE_HANDOFF_CLOSURE_CLOSURE_HANDOFF_NNN")
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
        replay_map = row.get("archive_reuse_release_handoff_closure_archive_reuse_release_map")
        if not isinstance(replay_map, list) or not replay_map:
            errors.append(f"{label}: archive_reuse_release_handoff_closure_archive_reuse_release_map must be a nonempty list")
        else:
            for map_index, map_row in enumerate(replay_map, 1):
                if not isinstance(map_row, dict):
                    errors.append(f"{label}: replay map row {map_index} must be an object")
                    continue
                missing_map_fields = sorted(REPLAY_MAP_REQUIRED_FIELDS - set(map_row))
                if missing_map_fields:
                    errors.append(f"{label}: replay map row {map_index} missing fields: {', '.join(missing_map_fields)}")
                identifier_fields = {
                    "source_exception_control_id",
                    "source_exception_claim_id",
                    "source_exception_replay_archive_control_id",
                    "source_exception_replay_archive_claim_id",
                    "source_archive_reuse_release_handoff_closure_archive_reuse_release_control_id",
                    "source_archive_reuse_release_handoff_closure_archive_reuse_release_claim_id",
                }
                for map_field in REPLAY_MAP_REQUIRED_FIELDS:
                    map_value = map_row.get(map_field)
                    if map_field == "claim_id":
                        if not isinstance(map_value, str) or not re.fullmatch(r"mmi_closeout_ledger_reconciliation_archive_reuse_release_handoff_closure_archive_reuse_release_claim_\d{3}", map_value):
                            errors.append(f"{label}: replay map claim_id must match mmi_closeout_ledger_reconciliation_archive_reuse_release_handoff_closure_archive_reuse_release_claim_NNN")
                    elif map_field in identifier_fields:
                        if not isinstance(map_value, str) or len(map_value) < 8:
                            errors.append(f"{label}: replay map {map_field} must be a stable identifier")
                    elif not isinstance(map_value, str) or len(map_value.split()) < 3:
                        errors.append(f"{label}: replay map {map_field} must contain at least 3 words")
        expected_status = row.get("expected_status")
        if expected_status == "pass":
            pass_count += 1
        elif expected_status == "fail":
            fail_count += 1
        else:
            errors.append(f"{label}: expected_status must be pass or fail")
        if row.get("expected_decision_route") not in ALLOWED_DECISION_ROUTES:
            errors.append(f"{label}: expected_decision_route must be reviewer_hold, compare, or reject")
        if row.get("expected_review_outcome") != "routes_to_cross_language_reviewer_closeout_ledger_reconciliation_exception_replay_archive_rollup_release_handoff_closure_archive_reuse_release_handoff_closure_archive_reuse_release_state":
            errors.append(f"{label}: expected_review_outcome must route to reviewer closeout ledger reconciliation exception replay archive rollup release handoff archive reuse state")
        declared_signals = row.get("archive_reuse_release_handoff_closure_archive_reuse_release_signals")
        expected_reasons = row.get("expected_failure_reasons")
        if not isinstance(declared_signals, dict) or set(declared_signals) != set(SIGNAL_ORDER):
            errors.append(f"{label}: replay signals must exactly match required signal keys")
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
    if pass_count != 8:
        errors.append(f"Expected 8 pass controls, found {pass_count}")
    if fail_count != 8:
        errors.append(f"Expected 8 fail controls, found {fail_count}")
    if len(covered_candidate_ids) != 8:
        errors.append(f"Expected replay controls to cover 8 source candidates, found {len(covered_candidate_ids)}")
    return errors


def build_report(controls: list[dict[str, Any]], rewrite_candidates: list[dict[str, Any]]) -> dict[str, Any]:
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
        review_outcome = "routes_to_cross_language_reviewer_closeout_ledger_reconciliation_exception_replay_archive_rollup_release_handoff_closure_archive_reuse_release_handoff_closure_archive_reuse_release_state"
        if observed_status == "pass":
            pass_controls.append(str(control["control_id"]))
        else:
            blocked_controls.append(str(control["control_id"]))
        results.append({
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
            "archive_reuse_release_handoff_closure_archive_reuse_release_map": control["archive_reuse_release_handoff_closure_archive_reuse_release_map"],
            "detected_archive_reuse_release_handoff_closure_archive_reuse_release_signals": detected,
            "archive_reuse_release_handoff_closure_archive_reuse_release_signals_declared": signal_object(declared),
            "archive_reuse_release_handoff_closure_archive_reuse_release_signals_detected": signal_object(detected),
            "source_candidate_expected_status": candidate["expected_status"],
            "boundary_pass": True,
        })
    return {
        "report_id": "mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_report_v0_1_20260625",
        "report_type": "machine_readable_mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_report",
        "report_version": VERSION,
        "generated_date": DATE_TOKEN,
        "atlas_layer": ATLAS_LAYER,
        "atlas_node_id": ATLAS_NODE_ID,
        "status": "local_fixture_pass",
        "report_scope": "local_fixture_mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_only",
        "scope": "Local synthetic cross language controls for handing off released archive reuse packets while preserving source attachments, archive snapshot, and reopenability during downstream handoff review without authority or clearance claim.",
        "artifact_paths": {
            "rewrite_candidates": repo_relative(REWRITE_CANDIDATES),
            "cross_language_controls": repo_relative(CROSS_LANGUAGE_CONTROLS),
            "cross_language_report_json": repo_relative(OUTPUT_JSON),
            "cross_language_report_markdown": repo_relative(OUTPUT_MARKDOWN),
            "scorer": "scripts/score_mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_controls_v0_1_20260625.py",
            "validator": "scripts/validate_mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_report_v0_1_20260625.py",
        },
        "validation": {
            "scorer_command": "python3 scripts/score_mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_controls_v0_1_20260625.py --check",
            "validator_command": "python3 scripts/validate_mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_report_v0_1_20260625.py",
            "make_target": "make mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_controls",
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
            "mismatch_count": sum(1 for result in results if result["archive_reuse_release_handoff_closure_archive_reuse_release_signals_declared"] != result["archive_reuse_release_handoff_closure_archive_reuse_release_signals_detected"]),
        },
        "failure_reason_counts": {signal: failure_counts.get(signal, 0) for signal in SIGNAL_ORDER},
        "control_results": results,
        "pass_control_ids": pass_controls,
        "blocked_control_ids": blocked_controls,
        "reviewer_closeout_ledger_reconciliation_exception_replay_archive_rollup_release_handoff_closure_archive": {
            "primary_question": "Can closed archive reuse release handoff closure packets be archived while source closeout id, exported ledger row id, owner final state, dissent note, unresolved branch archive boundary, archive snapshot, and reopenability stay preserved without authority or clearance claim.",
            "decision_order": SIGNAL_ORDER,
            "blocked_use": ["patient care", "clinical advice", "patient data use", "clinical validation claim", "clinical deployment claim", "model ranking claim", "partner claim", "institution claim", "regulatory clearance claim", "publication readiness claim", "authority claim", "clearance claim"],
        },
        "release_boundary": {
            "synthetic_only": True,
            "patient_data_used": False,
    "patient_data_requested": False,
    "private_clinical_text_used": False,
    "raw_clinical_notes_used": False,
    "private_model_outputs_used": False,
    "endpoint_results_used": False,
    "diagnosis_or_treatment_instruction_allowed": False,
    "model_comparison_claim_made": False,
    "partner_claim_made": False,
    "institution_claim_made": False,
    "regulatory_claim_made": False,
    "publication_claim_made": False,
    "authority_claim_made": False,
    "clearance_claim_made": False,
    "endorsement_claim_made": False,
    "requires_user_approval_before_outward_use": True,
            "clinical_use_allowed": False,
            "clinical_advice_allowed": False,
            "external_urls_present": False,
            "regulatory_clearance_claim_made": False,
            "publication_readiness_claim_made": False,
            "clinical_use_clearance_claim_made": False,
            "translation_clearance_claim_made": False,
            "reviewer_closeout_ledger_reconciliation_exception_replay_archive_rollup_release_handoff_closure_archive_clearance_claim_made": False,
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
            "allowed_use": "Repo local synthetic archive reuse release handoff closure archive reuse release handoff closure scoring before downstream release review.",
            "not_allowed_use": "Patient care, clinical advice, patient data use, private clinical text, raw clinical notes, private model outputs, endpoint results, clinical validation, clinical deployment, model comparison, model ranking, score certification, source truth certification, regulatory clearance, publication clearance, publication readiness, partner status, institution approval, endorsement, authority approval, or clinical use clearance.",
        },
        "blockers": [],
        "exact_next_action": "Add archive reuse release handoff closure archive reuse release handoff closure controls so reused archive reuse release handoff closure archive packets remain source linked and reopenable during downstream release review without losing source attachments or creating authority or clearance claim.",
    }


def markdown_list(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["score_summary"]
    lines = [
        "# Multilingual Medical Intelligence MMI 075 Archive Reuse Release Handoff Closure Archive Reuse Release Controls v0.1",
        "",
        f"Date: {DATE}",
        "",
        "Status: ready for local repo review only",
        "",
        "## Purpose",
        "",
        "This report checks whether closed archive reuse release handoff closure packets can be archived while staying reproducible during downstream archive reuse review in English and Turkish ASCII variants.",
        "",
        "It blocks reuse drift when one language loses source closeout id, exported ledger row id, owner final state, dissent note, unresolved branch archive boundary, archive snapshot, reopenability, or creates an authority or clearance claim.",
        "",
        "It keeps source closeout id, exported ledger row id, owner final state, dissent note, unresolved branch archive boundary, exception reason, archive snapshot, and reopenability attached before reviewer hold, compare, reject, and downstream release decisions.",
        "",
        "The controls use synthetic rows only. They contain no patient data and make no diagnosis, treatment instruction, clinical validation, clinical deployment, model ranking, partner, institutional, regulatory, publication, authority, or clearance claim.",
        "",
        "## Score Summary",
        "",
        *markdown_list([
            f"Control rows: {summary['control_count']}.",
            f"Expected pass controls: {summary['expected_pass_controls']}.",
            f"Expected fail controls: {summary['expected_fail_controls']}.",
            f"Observed pass controls: {summary['observed_pass_controls']}.",
            f"Observed blocked controls: {summary['observed_blocked_controls']}.",
            f"Source candidate coverage count: {summary['source_candidate_coverage_count']}.",
            f"Source row coverage count: {summary['source_row_coverage_count']}.",
        ]),
        "",
        "## Cross Language Signal Counts",
        "",
    ]
    declared = report["cross_language_signal_counts"]["declared_true"]
    detected = report["cross_language_signal_counts"]["detected_true"]
    lines.extend(markdown_list([f"`{signal}`: declared {declared[signal]}, detected {detected[signal]}." for signal in SIGNAL_ORDER]))
    lines.extend(["", "## Decision Route Counts", ""])
    lines.extend(markdown_list([f"`{route}`: expected {report['decision_route_counts']['expected'][route]}, observed {report['decision_route_counts']['observed'][route]}." for route in sorted(ALLOWED_DECISION_ROUTES)]))
    lines.extend([
        "", "## Reviewer Closeout Ledger Reconciliation Exception Replay Archive Rollup Release Handoff Closure Archive Reuse Release Handoff", "",
        report["reviewer_closeout_ledger_reconciliation_exception_replay_archive_rollup_release_handoff_closure_archive"]["primary_question"], "",
        "Decision order:", "",
        *markdown_list([f"`{signal}`" for signal in SIGNAL_ORDER]), "",
        "Plain signal names: source closeout id archive reuse release handoff closure archive reuse release handoff closure lost; exported ledger row id archive reuse release handoff closure archive reuse release handoff closure lost; owner final state archive reuse release handoff closure archive reuse release handoff closure lost; dissent note archive reuse release handoff closure archive reuse release handoff closure lost; unresolved branch archive boundary archive reuse release handoff closure archive reuse release handoff closure lost; archive snapshot archive reuse release handoff closure archive reuse release handoff closure lost; archive reopenability archive reuse release handoff closure archive reuse release handoff closure lost; authority or clearance claim created.", "",
        "## Release Boundary", "",
        "MMI 075 is a repo local synthetic safety wording gate only. It uses repo local synthetic fixtures and cleared repository review text only. It does not use or request patient data, private clinical text, raw clinical notes, private model outputs, endpoint results, or real care data.", "",
        "MMI 075 is not clinical advice, clinical validation, clinical deployment, model comparison, model ranking, score certification, source truth certification, regulatory clearance, publication clearance, external publication readiness, partner status, institution approval, endorsement, authority approval, or clinical use clearance.", "",
        "Any wording that implies patient data use, clinical validation, clinical deployment, model ranking, partner or institution status, regulatory clearance, publication readiness, authority approval, or clearance must be rejected or held for explicit source review and user approval before outward use.", "",
        "## Validation Command", "",
        "`make mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_controls`", "",
        "Direct check:", "",
        "`python3 scripts/score_mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_controls_v0_1_20260625.py --check`", "",
        "## Exact Next Action", "",
        report["exact_next_action"], "",
    ])
    return "\n".join(lines)


def validate_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("report_id") != "mmi_075_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_report_v0_1_20260625":
        errors.append("report_id mismatch")
    if report.get("atlas_node_id") != ATLAS_NODE_ID:
        errors.append(f"atlas_node_id must be {ATLAS_NODE_ID}")
    summary = report.get("score_summary", {})
    expected_summary = {
        "control_count": 16,
        "expected_pass_controls": 8,
        "expected_fail_controls": 8,
        "observed_pass_controls": 8,
        "observed_blocked_controls": 8,
        "source_candidate_coverage_count": 8,
        "source_row_coverage_count": 8,
        "status_mismatch_count": 0,
        "decision_route_mismatch_count": 0,
        "review_outcome_mismatch_count": 0,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"score_summary.{key} must be {expected}")
    observed_routes = report.get("decision_route_counts", {}).get("observed", {})
    if observed_routes != {"compare": 4, "reject": 9, "reviewer_hold": 3}:
        errors.append("observed decision route counts must be compare 4, reject 9, reviewer_hold 3")
    declared = report.get("cross_language_signal_counts", {}).get("declared_true", {})
    detected = report.get("cross_language_signal_counts", {}).get("detected_true", {})
    for signal in SIGNAL_ORDER:
        expected = 1 if signal in SIGNAL_ORDER else 0
        if declared.get(signal) != expected or detected.get(signal) != expected:
            errors.append(f"signal count mismatch for {signal}")
    boundary = report.get("release_boundary", {})
    for key in (
        "synthetic_only", "patient_data_used", "clinical_use_allowed", "clinical_advice_allowed",
        "reviewer_closeout_ledger_reconciliation_exception_replay_archive_rollup_release_handoff_closure_archive_clearance_claim_made",
        "authority_or_clearance_claim_made", "regulatory_clearance_claim_made", "publication_readiness_claim_made",
        "clinical_use_clearance_claim_made", "clinical_validation_claim_made", "clinical_deployment_claim_made",
        "model_superiority_claim_made", "partner_or_institution_claim_made", "external_publication_clearance",
    ):
        if key == "synthetic_only":
            if boundary.get(key) is not True:
                errors.append(f"release_boundary.{key} must be true")
        elif boundary.get(key) is not False:
            errors.append(f"release_boundary.{key} must be false")
    return errors


def validate_markdown(markdown: str) -> list[str]:
    required = [
        "MMI 075 Archive Reuse Release Handoff Closure Archive Reuse Release Controls v0.1",
        "source closeout id archive reuse release handoff closure archive reuse release handoff closure lost",
        "exported ledger row id archive reuse release handoff closure archive reuse release handoff closure lost",
        "owner final state archive reuse release handoff closure archive reuse release handoff closure lost",
        "dissent note archive reuse release handoff closure archive reuse release handoff closure lost",
        "unresolved branch archive boundary archive reuse release handoff closure archive reuse release handoff closure lost",
        "authority or clearance claim created",
        "not clinical advice, clinical validation, clinical deployment, model comparison, model ranking, score certification, source truth certification, regulatory clearance, publication clearance, external publication readiness, partner status, institution approval, endorsement, authority approval, or clinical use clearance",
    ]
    return [f"Markdown missing required phrase: {phrase}" for phrase in required if phrase not in markdown]


def as_json_text(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2) + "\n"


def write_outputs() -> dict[str, Any]:
    rewrite_candidates = load_jsonl(REWRITE_CANDIDATES)
    controls = load_jsonl(CROSS_LANGUAGE_CONTROLS)
    errors = validate_control_rows(controls, rewrite_candidates)
    if errors:
        raise SystemExit("\n".join(errors))
    report = build_report(controls, rewrite_candidates)
    errors = validate_report(report)
    if errors:
        raise SystemExit("\n".join(errors))
    markdown = render_markdown(report)
    errors = validate_markdown(markdown)
    if errors:
        raise SystemExit("\n".join(errors))
    OUTPUT_JSON.write_text(as_json_text(report), encoding="utf-8")
    OUTPUT_MARKDOWN.write_text(markdown, encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate existing generated outputs instead of writing them")
    args = parser.parse_args()
    try:
        rewrite_candidates = load_jsonl(REWRITE_CANDIDATES)
        controls = load_jsonl(CROSS_LANGUAGE_CONTROLS)
    except ValueError as error:
        print(f"FAIL archive reuse release handoff closure archive reuse release handoff closure controls: {error}")
        return 1
    errors = validate_control_rows(controls, rewrite_candidates)
    report = build_report(controls, rewrite_candidates) if not errors else {}
    if report:
        errors.extend(validate_report(report))
    expected_json_text = as_json_text(report) if report else ""
    expected_markdown = render_markdown(report) if report else ""
    if args.check:
        if not OUTPUT_JSON.exists():
            errors.append(f"missing JSON report: {repo_relative(OUTPUT_JSON)}")
        elif OUTPUT_JSON.read_text(encoding="utf-8") != expected_json_text:
            errors.append(f"stale JSON report: {repo_relative(OUTPUT_JSON)}")
        if not OUTPUT_MARKDOWN.exists():
            errors.append(f"missing Markdown report: {repo_relative(OUTPUT_MARKDOWN)}")
        elif OUTPUT_MARKDOWN.read_text(encoding="utf-8") != expected_markdown:
            errors.append(f"stale Markdown report: {repo_relative(OUTPUT_MARKDOWN)}")
    else:
        if not errors:
            OUTPUT_JSON.write_text(expected_json_text, encoding="utf-8")
            OUTPUT_MARKDOWN.write_text(expected_markdown, encoding="utf-8")
    if errors:
        print("FAIL archive reuse release handoff closure archive reuse release handoff closure controls")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS archive reuse release handoff closure archive reuse release handoff closure controls")
    print(f"controls={report['score_summary']['control_count']}")
    print(f"blocked_controls={report['score_summary']['observed_blocked_controls']}")
    print(f"pass_controls={report['score_summary']['observed_pass_controls']}")
    print(f"json={repo_relative(OUTPUT_JSON)}")
    print(f"markdown={repo_relative(OUTPUT_MARKDOWN)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
