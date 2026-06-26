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
ATLAS_NODE_ID = "mia_mmi_012"

REWRITE_CANDIDATES = ROOT / "data" / "multilingual_medical_intelligence_public_wording_rewrite_candidates_v0_1_20260625.jsonl"
CROSS_LANGUAGE_CONTROLS = ROOT / "data" / "multilingual_medical_intelligence_rewrite_candidate_cross_language_reviewer_handoff_packet_controls_v0_1_20260625.jsonl"
OUTPUT_JSON = ROOT / "data" / "multilingual_medical_intelligence_cross_language_reviewer_handoff_packet_report_v0_1_20260625.json"
OUTPUT_MARKDOWN = ROOT / "docs" / "MULTILINGUAL_MEDICAL_INTELLIGENCE_CROSS_LANGUAGE_REVIEWER_HANDOFF_PACKET_REPORT_V0_1_20260625.md"

SIGNAL_ORDER = [
    "english_handoff_packet_removed",
    "turkish_handoff_packet_removed",
    "evidence_summary_removed",
    "route_state_drifted",
    "reviewer_owner_missing",
    "authority_claim_created",
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
    "reviewer_handoff_packet_map",
    "expected_status",
    "expected_decision_route",
    "expected_failure_reasons",
    "reviewer_handoff_packet_signals",
    "expected_review_outcome",
    "release_boundary",
}

ALLOWED_CONTROL_TYPES = {
    "aligned_english_handoff_packet_preserved",
    "english_handoff_packet_removed",
    "aligned_turkish_handoff_packet_preserved",
    "turkish_handoff_packet_removed",
    "aligned_evidence_summary_preserved",
    "evidence_summary_removed",
    "aligned_route_state_preserved",
    "route_state_drifted",
    "aligned_reviewer_owner_preserved",
    "reviewer_owner_missing",
    "aligned_authority_claim_absent",
    "authority_claim_created",
}

EXPECTED_BOUNDARY_FLAGS = {
    "synthetic_only": True,
    "patient_data_used": False,
    "clinical_use_allowed": False,
    "clinical_advice_allowed": False,
    "external_urls_present": False,
}

REVIEWER_HANDOFF_PACKET_MAP_REQUIRED_FIELDS = {
    "claim_id",
    "source_scope",
    "rationale_to_preserve",
    "reviewer_owner_to_preserve",
    "unresolved_state_to_preserve",
    "decision_route_to_preserve",
    "evidence_summary_to_preserve",
    "handoff_packet_boundary",
    "forbidden_authority_claim",
    "reuse_boundary",
}

ALLOWED_DECISION_ROUTES = {"reviewer_hold", "compare", "reject"}

ENGLISH_HANDOFF_PACKET_REMOVED_RE = re.compile(
    r"\b(english handoff packet removed|english handoff packet is removed|handoff packet omitted in english)\b",
    re.IGNORECASE,
)
TURKISH_HANDOFF_PACKET_REMOVED_RE = re.compile(
    r"\b(turkish handoff packet removed|turkish handoff packet is removed)\b|"
    r"\b(devir paketi kaldirildi|aktarim paketi kaldirildi)\b",
    re.IGNORECASE,
)
EVIDENCE_SUMMARY_REMOVED_RE = re.compile(
    r"\b(evidence summary removed|evidence summary is removed|kanit ozeti kaldirildi)\b",
    re.IGNORECASE,
)
ROUTE_STATE_DRIFTED_RE = re.compile(
    r"\b(route state drifted|route state changed|review route changed)\b",
    re.IGNORECASE,
)
REVIEWER_OWNER_MISSING_RE = re.compile(
    r"\b(reviewer owner missing|reviewer owner removed|owner missing)\b",
    re.IGNORECASE,
)
AUTHORITY_CLAIM_CREATED_RE = re.compile(
    r"\b(authority claim created|authority claim is created|reviewer route becomes authority)\b",
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
        "english_handoff_packet_removed": bool(ENGLISH_HANDOFF_PACKET_REMOVED_RE.search(english_text)),
        "turkish_handoff_packet_removed": bool(TURKISH_HANDOFF_PACKET_REMOVED_RE.search(turkish_text)),
        "evidence_summary_removed": bool(EVIDENCE_SUMMARY_REMOVED_RE.search(joined)),
        "route_state_drifted": bool(ROUTE_STATE_DRIFTED_RE.search(joined)),
        "reviewer_owner_missing": bool(REVIEWER_OWNER_MISSING_RE.search(joined)),
        "authority_claim_created": bool(AUTHORITY_CLAIM_CREATED_RE.search(joined)),
    }


def signal_object(signals: list[str]) -> dict[str, bool]:
    signal_set = set(signals)
    return {signal: signal in signal_set for signal in SIGNAL_ORDER}


def true_signals(row: dict[str, Any]) -> list[str]:
    signals = row.get("reviewer_handoff_packet_signals")
    if not isinstance(signals, dict):
        return []
    return [signal for signal in SIGNAL_ORDER if signals.get(signal) is True]


def observed_decision_route(row: dict[str, Any], detected: list[str]) -> str:
    if detected:
        return "reject"
    control_type = str(row.get("control_type", ""))
    if control_type in {"aligned_evidence_summary_preserved", "aligned_reviewer_owner_preserved"}:
        return "compare"
    if control_type == "aligned_authority_claim_absent":
        return "reject"
    return "reviewer_hold"


def validate_control_rows(
    controls: list[dict[str, Any]],
    rewrite_candidates: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    candidates_by_id = {str(row.get("candidate_id")): row for row in rewrite_candidates}

    if len(controls) != 12:
        errors.append(f"Expected 12 cross language reviewer handoff packet controls, found {len(controls)}")

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
            r"MMI_CROSS_LANGUAGE_REVIEWER_HANDOFF_PACKET_\d{3}", control_id
        ):
            errors.append(f"{label}: control_id must match MMI_CROSS_LANGUAGE_REVIEWER_HANDOFF_PACKET_NNN")
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

        packet_map = row.get("reviewer_handoff_packet_map")
        if not isinstance(packet_map, list) or not packet_map:
            errors.append(f"{label}: reviewer_handoff_packet_map must be a nonempty list")
        else:
            for map_index, map_row in enumerate(packet_map, 1):
                if not isinstance(map_row, dict):
                    errors.append(f"{label}: reviewer_handoff_packet_map[{map_index}] must be an object")
                    continue
                missing_map_fields = sorted(REVIEWER_HANDOFF_PACKET_MAP_REQUIRED_FIELDS - set(map_row))
                if missing_map_fields:
                    errors.append(
                        f"{label}: reviewer_handoff_packet_map[{map_index}] missing fields: {', '.join(missing_map_fields)}"
                    )
                for map_field in REVIEWER_HANDOFF_PACKET_MAP_REQUIRED_FIELDS:
                    map_value = map_row.get(map_field)
                    if map_field == "claim_id":
                        if not isinstance(map_value, str) or not re.fullmatch(r"mmi_handoff_claim_\d{3}", map_value):
                            errors.append(
                                f"{label}: reviewer_handoff_packet_map[{map_index}].claim_id must match mmi_handoff_claim_NNN"
                            )
                        continue
                    if not isinstance(map_value, str) or len(map_value.split()) < 3:
                        errors.append(
                            f"{label}: reviewer_handoff_packet_map[{map_index}].{map_field} must contain at least 3 words"
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
        if row.get("expected_review_outcome") != "routes_to_cross_language_reviewer_handoff_packet_state":
            errors.append(f"{label}: expected_review_outcome must route to reviewer handoff packet state")

        declared_signals = row.get("reviewer_handoff_packet_signals")
        expected_reasons = row.get("expected_failure_reasons")
        if not isinstance(declared_signals, dict) or set(declared_signals) != set(SIGNAL_ORDER):
            errors.append(f"{label}: reviewer_handoff_packet_signals must exactly match required signal keys")
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
            f"Expected cross language reviewer handoff packet controls to cover 6 source candidates, found {len(covered_candidate_ids)}"
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
        review_outcome = "routes_to_cross_language_reviewer_handoff_packet_state"
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
                "reviewer_handoff_packet_map": control["reviewer_handoff_packet_map"],
                "detected_reviewer_handoff_packet_signals": detected,
                "reviewer_handoff_packet_signals_declared": signal_object(declared),
                "reviewer_handoff_packet_signals_detected": signal_object(detected),
                "source_candidate_expected_status": candidate["expected_status"],
                "boundary_pass": True,
            }
        )

    return {
        "report_id": "multilingual_medical_intelligence_cross_language_reviewer_handoff_packet_report_v0_1_20260625",
        "report_type": "machine_readable_cross_language_reviewer_handoff_packet_report",
        "report_version": VERSION,
        "generated_date": DATE_TOKEN,
        "atlas_layer": ATLAS_LAYER,
        "atlas_node_id": ATLAS_NODE_ID,
        "status": "local_fixture_pass",
        "report_scope": "local_fixture_cross_language_reviewer_handoff_packet_gate_only",
        "scope": "Local synthetic cross language controls for reviewer handoff packet rationale, owner, unresolved state, route, evidence summary, and authority claim drift.",
        "artifact_paths": {
            "rewrite_candidates": repo_relative(REWRITE_CANDIDATES),
            "cross_language_controls": repo_relative(CROSS_LANGUAGE_CONTROLS),
            "cross_language_report_json": repo_relative(OUTPUT_JSON),
            "cross_language_report_markdown": repo_relative(OUTPUT_MARKDOWN),
            "scorer": "scripts/score_multilingual_medical_intelligence_cross_language_reviewer_handoff_packet_controls_v0_1_20260625.py",
            "validator": "scripts/validate_multilingual_medical_intelligence_cross_language_reviewer_handoff_packet_report_v0_1_20260625.py",
        },
        "validation": {
            "scorer_command": "python3 scripts/score_multilingual_medical_intelligence_cross_language_reviewer_handoff_packet_controls_v0_1_20260625.py --check",
            "validator_command": "python3 scripts/validate_multilingual_medical_intelligence_cross_language_reviewer_handoff_packet_report_v0_1_20260625.py",
            "make_target": "make multilingual_medical_intelligence_cross_language_reviewer_handoff_packet_controls",
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
                if result["reviewer_handoff_packet_signals_declared"]
                != result["reviewer_handoff_packet_signals_detected"]
            ),
        },
        "failure_reason_counts": {signal: failure_counts.get(signal, 0) for signal in SIGNAL_ORDER},
        "control_results": results,
        "pass_control_ids": pass_controls,
        "blocked_control_ids": blocked_controls,
        "reviewer_handoff_packet": {
            "primary_question": "Does either language remove the handoff packet, remove evidence summary, drift route state, drop reviewer owner, or create authority claim.",
            "decision_order": SIGNAL_ORDER,
            "blocked_use": [
                "patient care",
                "clinical advice",
                "translation clearance",
                "reviewer handoff packet clearance",
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
            "reviewer_handoff_packet_clearance_claim_made": False,
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
            "allowed_use": "Repo local synthetic cross language reviewer handoff packet scoring before public wording reuse.",
            "not_allowed_use": "Patient care, clinical advice, translation clearance, reviewer handoff packet clearance, external publication clearance, model ranking, or authority claim.",
        },
        "blockers": [],
        "exact_next_action": "Add cross language reviewer handoff replay controls so packets remain reproducible across recheck, appeal, and route owner handoff.",
    }


def markdown_list(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["score_summary"]
    lines = [
        "# Multilingual Medical Intelligence Cross Language Reviewer Handoff Packet Controls v0.1",
        "",
        f"Date: {DATE}",
        "",
        "Status: ready for local repo review only",
        "",
        "## Purpose",
        "",
        "This report checks whether English and Turkish ASCII variants preserve a reviewer handoff packet across the same synthetic record.",
        "",
        "It blocks packet drift when one language removes the handoff packet, removes evidence summary, changes route state, drops reviewer owner, or creates an authority claim.",
        "",
        "It keeps rationale, reviewer owner, unresolved state, route, and evidence summary attached before reviewer hold, compare, and reject reuse decisions.",
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
        markdown_list(
            [
                f"`{signal}`: declared {declared[signal]}, detected {detected[signal]}."
                for signal in SIGNAL_ORDER
            ]
        )
    )
    lines.extend(["", "## Decision Route Counts", ""])
    route_expected = report["decision_route_counts"]["expected"]
    route_observed = report["decision_route_counts"]["observed"]
    lines.extend(
        markdown_list(
            [
                f"`{route}`: expected {route_expected[route]}, observed {route_observed[route]}."
                for route in sorted(ALLOWED_DECISION_ROUTES)
            ]
        )
    )
    lines.extend(
        [
            "",
            "## Reviewer Handoff Packet",
            "",
            "Does either language remove the handoff packet, remove evidence summary, drift route state, drop reviewer owner, or create authority claim.",
            "",
            "Decision order:",
            "",
            *markdown_list([f"`{signal}`" for signal in SIGNAL_ORDER]),
            "",
            "## Release Boundary",
            "",
            "This report supports repo local review only. It does not clear text for patient care, clinical advice, translation clearance, reviewer handoff packet clearance, clinical validation, clinical deployment, model comparison, institutional use, or external publication.",
            "",
            "Boundary note: not score certification, not source clearance, not clinical validation, not clinical deployment, not translation clearance, not reviewer handoff packet clearance, not authority claim, and not external publication clearance.",
            "",
            "## Validation Command",
            "",
            "`make multilingual_medical_intelligence_cross_language_reviewer_handoff_packet_controls`",
            "",
            "Direct check:",
            "",
            "`python3 scripts/score_multilingual_medical_intelligence_cross_language_reviewer_handoff_packet_controls_v0_1_20260625.py --check`",
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
    if report.get("status") != "local_fixture_pass":
        errors.append("report status must be local_fixture_pass")
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
    release = report.get("release_boundary", {})
    for key in [
        "patient_data_used",
        "clinical_use_allowed",
        "clinical_advice_allowed",
        "translation_clearance_claim_made",
        "reviewer_handoff_packet_clearance_claim_made",
        "authority_claim_made",
        "clinical_validation_claim_made",
        "clinical_deployment_claim_made",
        "model_superiority_claim_made",
        "external_publication_clearance",
    ]:
        if release.get(key) is not False:
            errors.append(f"release_boundary.{key} must be false")
    if release.get("synthetic_only") is not True:
        errors.append("release_boundary.synthetic_only must be true")
    if report.get("blockers") != []:
        errors.append("report blockers must be empty")
    return errors


def validate_markdown(markdown: str) -> list[str]:
    errors: list[str] = []
    required = [
        "Reviewer Handoff Packet Controls",
        "ready for local repo review only",
        "rationale, reviewer owner, unresolved state, route, and evidence summary",
        "not reviewer handoff packet clearance",
        "not authority claim",
        "make multilingual_medical_intelligence_cross_language_reviewer_handoff_packet_controls",
    ]
    lower = markdown.lower()
    for phrase in required:
        if phrase.lower() not in lower:
            errors.append(f"markdown missing required phrase: {phrase}")
    return errors


def as_json_text(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        rewrite_candidates = load_jsonl(REWRITE_CANDIDATES)
        controls = load_jsonl(CROSS_LANGUAGE_CONTROLS)
    except ValueError as error:
        print(f"FAIL cross language reviewer handoff packet controls: {error}")
        return 1

    errors = validate_control_rows(controls, rewrite_candidates)
    report = build_report(controls, rewrite_candidates)
    errors.extend(validate_report(report))
    markdown = render_markdown(report)
    errors.extend(validate_markdown(markdown))

    json_text = as_json_text(report)
    if args.check:
        if not OUTPUT_JSON.exists():
            errors.append(f"missing JSON report: {repo_relative(OUTPUT_JSON)}")
        elif OUTPUT_JSON.read_text(encoding="utf-8") != json_text:
            errors.append(f"stale JSON report: {repo_relative(OUTPUT_JSON)}")
        if not OUTPUT_MARKDOWN.exists():
            errors.append(f"missing Markdown report: {repo_relative(OUTPUT_MARKDOWN)}")
        elif OUTPUT_MARKDOWN.read_text(encoding="utf-8") != markdown:
            errors.append(f"stale Markdown report: {repo_relative(OUTPUT_MARKDOWN)}")
    else:
        OUTPUT_JSON.write_text(json_text, encoding="utf-8")
        OUTPUT_MARKDOWN.write_text(markdown, encoding="utf-8")

    if errors:
        print("FAIL cross language reviewer handoff packet controls")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS cross language reviewer handoff packet controls")
    print(f"json={repo_relative(OUTPUT_JSON)}")
    print(f"markdown={repo_relative(OUTPUT_MARKDOWN)}")
    print(f"controls={report['score_summary']['control_count']}")
    print(f"blocked_controls={report['score_summary']['observed_blocked_controls']}")
    print(f"pass_controls={report['score_summary']['observed_pass_controls']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
