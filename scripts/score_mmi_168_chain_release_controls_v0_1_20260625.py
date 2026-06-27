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
ATLAS_NODE_ID = "mia_mmi_168"
REPORT_LABEL = "MMI 168 chain release controls"
REVIEW_OUTCOME = "routes_to_mmi_168_chain_release_state"
NEXT_ACTION = "Add MMI 169 short stem chain handoff controls after MMI 168 release review while preserving source attachments, archive snapshot, and reopenability without authority or clearance claim."
REWRITE_CANDIDATES = ROOT / "data" / "multilingual_medical_intelligence_public_wording_rewrite_candidates_v0_1_20260625.jsonl"
CROSS_LANGUAGE_CONTROLS = ROOT / "data" / "mmi_168_chain_release_controls_v0_1_20260625.jsonl"
OUTPUT_JSON = ROOT / "data" / "mmi_168_chain_release_report_v0_1_20260625.json"
OUTPUT_MARKDOWN = ROOT / "docs" / "MMI_168_CHAIN_RELEASE_REPORT_V0_1_20260625.md"
SIGNAL_ORDER = [
    "source_closeout_id_chain_release_lost",
    "exported_ledger_row_id_chain_release_lost",
    "owner_final_state_chain_release_lost",
    "dissent_note_chain_release_lost",
    "unresolved_branch_archive_boundary_chain_release_lost",
    "archive_snapshot_chain_release_lost",
    "archive_reopenability_chain_release_lost",
    "authority_or_clearance_claim_created",
]
REQUIRED_CONTROL_FIELDS = {
    "control_id", "fixture_version", "atlas_layer", "atlas_node_id", "source_candidate_id",
    "source_row_id", "source_state_pair_id", "source_negative_control_id", "language_pair",
    "clinical_domain", "control_type", "english_text", "turkish_ascii_text",
    "source_exception_control_id", "source_exception_claim_id", "chain_release_control_id",
    "source_chain_release_control_id", "source_chain_release_claim_id", "chain_release_map",
    "chain_release_signals", "expected_status", "expected_decision_route",
    "expected_failure_reasons", "expected_review_outcome", "release_boundary",
}
ALLOWED_DECISION_ROUTES = {"reviewer_hold", "compare", "reject"}
COMPARE_CONTROL_TYPES = {
    "aligned_owner_final_state_chain_release_attached",
    "aligned_unresolved_branch_archive_boundary_chain_release_attached",
    "aligned_archive_snapshot_chain_release_attached",
    "aligned_archive_reopenability_chain_release_attached",
}
EXPECTED_BOUNDARY_FLAGS = {'synthetic_only': True, 'patient_data_used': False, 'patient_data_requested': False, 'private_clinical_text_used': False, 'raw_clinical_notes_used': False, 'private_model_outputs_used': False, 'endpoint_results_used': False, 'diagnosis_or_treatment_instruction_allowed': False, 'model_comparison_claim_made': False, 'partner_claim_made': False, 'institution_claim_made': False, 'regulatory_claim_made': False, 'publication_claim_made': False, 'authority_claim_made': False, 'clearance_claim_made': False, 'endorsement_claim_made': False, 'requires_user_approval_before_outward_use': True, 'clinical_use_allowed': False, 'clinical_advice_allowed': False, 'external_urls_present': False, 'regulatory_clearance_claim_made': False, 'publication_readiness_claim_made': False, 'clinical_use_clearance_claim_made': False, 'clinical_validation_claim_made': False, 'clinical_deployment_claim_made': False, 'model_ranking_claim_made': False, 'model_superiority_claim_made': False, 'partner_or_institution_claim_made': False, 'authority_or_clearance_claim_made': False, 'score_certification_claim_made': False, 'source_truth_certification_claim_made': False, 'external_publication_clearance': False}
SIGNAL_PATTERNS = {
    "source_closeout_id_chain_release_lost": re.compile(r"\b(source closeout id chain release lost|kaynak kapanis id chain release kayboldu)\b", re.IGNORECASE),
    "exported_ledger_row_id_chain_release_lost": re.compile(r"\b(exported ledger row id chain release lost|exported ledger row id chain release kayboldu)\b", re.IGNORECASE),
    "owner_final_state_chain_release_lost": re.compile(r"\b(owner final state chain release lost|sahip son durum chain release kayboldu)\b", re.IGNORECASE),
    "dissent_note_chain_release_lost": re.compile(r"\b(dissent note chain release lost|itiraz notu chain release kayboldu)\b", re.IGNORECASE),
    "unresolved_branch_archive_boundary_chain_release_lost": re.compile(r"\b(unresolved branch archive boundary chain release lost|cozulmemis dal archive siniri chain release kayboldu)\b", re.IGNORECASE),
    "archive_snapshot_chain_release_lost": re.compile(r"\b(archive snapshot chain release lost|archive snapshot chain release kayboldu)\b", re.IGNORECASE),
    "archive_reopenability_chain_release_lost": re.compile(r"\b(archive reopenability chain release lost|archive reopenability chain release kayboldu)\b", re.IGNORECASE),
    "authority_or_clearance_claim_created": re.compile(r"\b(authority or clearance claim created|otorite veya clearance iddiasi olusturuldu)\b", re.IGNORECASE),
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
    signals = row.get("chain_release_signals")
    return [signal for signal in SIGNAL_ORDER if isinstance(signals, dict) and signals.get(signal) is True]


def observed_decision_route(row: dict[str, Any], detected: list[str]) -> str:
    if detected:
        return "reject"
    if str(row.get("control_type")) in COMPARE_CONTROL_TYPES:
        return "compare"
    return "reviewer_hold"


def validate_control_rows(controls: list[dict[str, Any]], rewrite_candidates: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    candidates_by_id = {str(row.get("candidate_id")): row for row in rewrite_candidates}
    if len(controls) != 16:
        errors.append(f"Expected 16 {REPORT_LABEL}, found {len(controls)}")
    seen: set[str] = set()
    pass_count = fail_count = 0
    covered_candidate_ids: set[str] = set()
    for index, row in enumerate(controls, 1):
        control_id = row.get("control_id")
        label = control_id if isinstance(control_id, str) else f"control {index}"
        missing = sorted(REQUIRED_CONTROL_FIELDS - set(row))
        if missing:
            errors.append(f"{label}: missing fields: {', '.join(missing)}")
            continue
        if not isinstance(control_id, str) or not re.fullmatch(r"MMI_168_CHAIN_RELEASE_\d{3}_(?:PASS|FAIL)", control_id):
            errors.append(f"{label}: bad control_id")
        elif control_id in seen:
            errors.append(f"{label}: duplicate control_id")
        else:
            seen.add(control_id)
        if row.get("fixture_version") != VERSION:
            errors.append(f"{label}: fixture_version must be {VERSION}")
        if row.get("atlas_layer") != ATLAS_LAYER or row.get("atlas_node_id") != ATLAS_NODE_ID:
            errors.append(f"{label}: atlas layer or node mismatch")
        if row.get("language_pair") != "Turkish English":
            errors.append(f"{label}: language_pair must be Turkish English")
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
        if not isinstance(row.get("chain_release_map"), list) or not row["chain_release_map"]:
            errors.append(f"{label}: chain_release_map must be nonempty")
        else:
            for map_row in row["chain_release_map"]:
                for key in ("claim_id", "source_scope", "source_closeout_id_to_keep", "archive_reopenability_to_keep", "release_review_boundary", "focused_attachment"):
                    value = map_row.get(key) if isinstance(map_row, dict) else None
                    if not isinstance(value, str) or len(value.split()) < 1:
                        errors.append(f"{label}: chain_release_map.{key} must be present")
        status = row.get("expected_status")
        if status == "pass":
            pass_count += 1
        elif status == "fail":
            fail_count += 1
        else:
            errors.append(f"{label}: expected_status must be pass or fail")
        if row.get("expected_decision_route") not in ALLOWED_DECISION_ROUTES:
            errors.append(f"{label}: expected_decision_route is invalid")
        if row.get("expected_review_outcome") != REVIEW_OUTCOME:
            errors.append(f"{label}: expected_review_outcome mismatch")
        declared = row.get("chain_release_signals")
        reasons = row.get("expected_failure_reasons")
        if not isinstance(declared, dict) or set(declared) != set(SIGNAL_ORDER):
            errors.append(f"{label}: chain_release_signals must exactly match required keys")
            declared = {}
        if not isinstance(reasons, list):
            errors.append(f"{label}: expected_failure_reasons must be a list")
            reasons = []
        for reason in reasons:
            if reason not in SIGNAL_ORDER:
                errors.append(f"{label}: unsupported expected failure reason: {reason}")
            if declared.get(reason) is not True:
                errors.append(f"{label}: expected reason must have true signal: {reason}")
        if status == "pass" and reasons:
            errors.append(f"{label}: pass controls must not include failure reasons")
        if status == "fail" and not reasons:
            errors.append(f"{label}: fail controls must include failure reasons")
        observed = detected_signals(row)
        observed_names = [signal for signal, value in observed.items() if value is True]
        if row.get("expected_decision_route") != observed_decision_route(row, observed_names):
            errors.append(f"{label}: expected_decision_route does not match observed route")
        for signal, expected in declared.items():
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
        errors.append(f"Expected 8 source candidates, found {len(covered_candidate_ids)}")
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
        observed_status = "fail" if detected else "pass"
        declared_counts.update(declared)
        detected_counts.update(detected)
        failure_counts.update(expected_reasons)
        expected_route_counts.update([expected_route])
        observed_route_counts.update([observed_route])
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
            "observed_review_outcome": REVIEW_OUTCOME,
            "status_match": control["expected_status"] == observed_status,
            "review_outcome_match": control["expected_review_outcome"] == REVIEW_OUTCOME,
            "expected_failure_reasons": expected_reasons,
            "chain_release_map": control["chain_release_map"],
            "detected_chain_release_signals": detected,
            "chain_release_signals_declared": signal_object(declared),
            "chain_release_signals_detected": signal_object(detected),
            "source_candidate_expected_status": candidate["expected_status"],
            "boundary_pass": True,
        })
    return {
        "report_id": "mmi_168_chain_release_report_v0_1_20260625",
        "report_type": "machine_readable_mmi_168_chain_release_report",
        "report_version": VERSION,
        "generated_date": DATE_TOKEN,
        "atlas_layer": ATLAS_LAYER,
        "atlas_node_id": ATLAS_NODE_ID,
        "status": "local_fixture_pass",
        "report_scope": "local_fixture_mmi_168_chain_release_only",
        "scope": "Local synthetic cross language controls for checking whether reuse reviewed archived packets can be released during downstream release review while source attachments, archive snapshot, and reopenability remain attached without authority or clearance claim.",
        "artifact_paths": {
            "rewrite_candidates": repo_relative(REWRITE_CANDIDATES),
            "cross_language_controls": repo_relative(CROSS_LANGUAGE_CONTROLS),
            "cross_language_report_json": repo_relative(OUTPUT_JSON),
            "cross_language_report_markdown": repo_relative(OUTPUT_MARKDOWN),
            "scorer": "scripts/score_mmi_168_chain_release_controls_v0_1_20260625.py",
            "validator": "scripts/validate_mmi_168_chain_release_report_v0_1_20260625.py",
        },
        "validation": {
            "scorer_command": "python3 scripts/score_mmi_168_chain_release_controls_v0_1_20260625.py --check",
            "validator_command": "python3 scripts/validate_mmi_168_chain_release_report_v0_1_20260625.py",
            "make_target": "make mmi_168_chain_release_controls",
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
            "mismatch_count": sum(1 for result in results if result["chain_release_signals_declared"] != result["chain_release_signals_detected"]),
        },
        "failure_reason_counts": {signal: failure_counts.get(signal, 0) for signal in SIGNAL_ORDER},
        "control_results": results,
        "pass_control_ids": pass_controls,
        "blocked_control_ids": blocked_controls,
        "chain_release_review": {
            "primary_question": "Can reuse reviewed archived packets be released during downstream release review while source closeout id, exported ledger row id, owner final state, dissent note, unresolved branch archive boundary, archive snapshot, and reopenability stay preserved without authority or clearance claim.",
            "decision_order": SIGNAL_ORDER,
            "blocked_use": ["patient care", "clinical advice", "patient data use", "authority claim", "clearance claim"],
        },
        "release_boundary": EXPECTED_BOUNDARY_FLAGS | {
            "allowed_use": "Repo local synthetic chain release scoring for reuse reviewed archived packets only.",
            "not_allowed_use": "Patient care, clinical advice, patient data use, private clinical text, raw clinical notes, private model outputs, endpoint results, model comparison, model ranking, score certification, source truth certification, regulatory clearance, publication clearance, publication readiness, partner status, institution approval, endorsement, authority approval, or clinical use clearance.",
        },
        "blockers": [],
        "exact_next_action": NEXT_ACTION,
    }


def markdown_list(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["score_summary"]
    lines = [
        "# Multilingual Medical Intelligence MMI 168 Chain Release Controls v0.1",
        "",
        f"Date: {DATE}",
        "",
        "Status: ready for local repo review only",
        "",
        "## Purpose",
        "",
        "This report checks whether reuse reviewed archived packets can be released during downstream release review while staying reproducible in English and Turkish ASCII variants.",
        "",
        "It blocks release drift when one language loses source closeout id, exported ledger row id, owner final state, dissent note, unresolved branch archive boundary, archive snapshot, reopenability, or creates an authority or clearance claim.",
        "",
        "It keeps source closeout id, exported ledger row id, owner final state, dissent note, unresolved branch archive boundary, exception reason, archive snapshot, and reopenability attached during reviewer hold, compare, reject, and downstream release decisions.",
        "",
        "The controls use synthetic rows only. They contain no patient data and make no diagnosis, treatment instruction, clinical validation, clinical deployment, model ranking, model superiority, partner, institutional, regulatory, publication, authority, or clearance claim.",
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
        "", "## Chain Release Question", "",
        report["chain_release_review"]["primary_question"], "",
        "Decision order:", "",
        *markdown_list([f"`{signal}`" for signal in SIGNAL_ORDER]), "",
        "Plain signal names: source closeout id lost; exported ledger row id lost; owner final state lost; dissent note lost; unresolved branch archive boundary lost; archive snapshot lost; archive reopenability lost; authority or clearance claim created.", "",
        "## Use Boundary", "",
        "MMI 168 is a repo local synthetic safety wording gate only. It uses repo local synthetic fixtures and existing repository review text only. It does not use or request patient data, private clinical text, raw clinical notes, private model outputs, endpoint results, or real care data.", "",
        "MMI 168 is not clinical advice, clinical validation, clinical deployment, model comparison, model ranking, model superiority, score certification, source truth certification, regulatory clearance, publication clearance, external publication readiness, partner status, institution approval, endorsement, authority approval, or clinical use clearance.", "",
        "Any wording that implies patient data use, model ranking, partner or institution status, regulatory clearance, publication readiness, authority approval, or clearance must be rejected or held for explicit source review and user approval before outward use.", "",
        "## Validation Command", "",
        "`make mmi_168_chain_release_controls`", "",
        "Direct check:", "",
        "`python3 scripts/score_mmi_168_chain_release_controls_v0_1_20260625.py --check`", "",
        "## Exact Next Action", "",
        report["exact_next_action"], "",
    ])
    return "\n".join(lines)


def validate_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("report_id") != "mmi_168_chain_release_report_v0_1_20260625":
        errors.append("report_id mismatch")
    if report.get("report_type") != "machine_readable_mmi_168_chain_release_report":
        errors.append("report_type mismatch")
    if report.get("report_scope") != "local_fixture_mmi_168_chain_release_only":
        errors.append("report_scope mismatch")
    if report.get("atlas_node_id") != ATLAS_NODE_ID:
        errors.append("atlas_node_id mismatch")
    summary = report.get("score_summary", {})
    for key, value in {
        "control_count": 16,
        "expected_pass_controls": 8,
        "expected_fail_controls": 8,
        "observed_pass_controls": 8,
        "observed_blocked_controls": 8,
        "source_candidate_coverage_count": 8,
        "status_mismatch_count": 0,
        "decision_route_mismatch_count": 0,
        "review_outcome_mismatch_count": 0,
    }.items():
        if summary.get(key) != value:
            errors.append(f"score_summary.{key} expected {value}, found {summary.get(key)}")
    if report.get("cross_language_signal_counts", {}).get("mismatch_count") != 0:
        errors.append("signal mismatch count must be zero")
    if report.get("exact_next_action") != NEXT_ACTION:
        errors.append("exact_next_action mismatch")
    return errors


def validate_markdown(markdown: str) -> list[str]:
    required = [
        "MMI 168 Chain Release Controls",
        "reuse reviewed archived packets can be released during downstream release review",
        "source closeout id lost",
        "archive reopenability lost",
        "authority or clearance claim created",
        "make mmi_168_chain_release_controls",
        NEXT_ACTION,
    ]
    forbidden = [
        "MMI " + "123",
        "mmi_" + "123_" + "chain_" + "release",
        "MMI_" + "123_CHAIN_RELEASE",
        "Add MMI " + "124 short stem chain handoff controls",
        "MMI " + "127",
        "mmi_" + "127_" + "chain_" + "reuse",
        "MMI_" + "127_CHAIN_REUSE",
        "MMI " + "122",
        "mmi_" + "122_" + "chain_" + "reuse",
        "MMI_" + "122_CHAIN_REUSE",
        "chain_" + "reuse_controls",
        "chain_" + "reuse_signals",
        "downstream " + "reuse review",
        "can be " + "reused",
        "archive " + "reviewed " + "archived packets",
        "MMI " + "119 short stem chain handoff controls",
        "archive_reuse_release_handoff_" + "closure_archive_reuse_release",
    ]
    errors = [f"missing markdown phrase: {phrase}" for phrase in required if phrase not in markdown]
    errors.extend(f"stale markdown phrase: {phrase}" for phrase in forbidden if phrase in markdown)
    return errors


def as_json_text(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=f"Score {REPORT_LABEL}")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        rewrite_candidates = load_jsonl(REWRITE_CANDIDATES)
        controls = load_jsonl(CROSS_LANGUAGE_CONTROLS)
    except ValueError as error:
        print(f"FAIL {REPORT_LABEL}: {error}")
        return 1
    errors = validate_control_rows(controls, rewrite_candidates)
    report = build_report(controls, rewrite_candidates)
    errors.extend(validate_report(report))
    markdown = render_markdown(report)
    errors.extend(validate_markdown(markdown))
    if errors:
        print(f"FAIL {REPORT_LABEL}")
        for error in errors:
            print(f"- {error}")
        return 1
    json_text = as_json_text(report)
    if args.check:
        if not OUTPUT_JSON.exists() or OUTPUT_JSON.read_text(encoding="utf-8") != json_text:
            print(f"FAIL {REPORT_LABEL}: stale JSON report")
            return 1
        if not OUTPUT_MARKDOWN.exists() or OUTPUT_MARKDOWN.read_text(encoding="utf-8") != markdown:
            print(f"FAIL {REPORT_LABEL}: stale Markdown report")
            return 1
    else:
        OUTPUT_JSON.write_text(json_text, encoding="utf-8")
        OUTPUT_MARKDOWN.write_text(markdown, encoding="utf-8")
    print(f"PASS {REPORT_LABEL}")
    print(f"controls={len(controls)}")
    print(f"json={repo_relative(OUTPUT_JSON)}")
    print(f"markdown={repo_relative(OUTPUT_MARKDOWN)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
