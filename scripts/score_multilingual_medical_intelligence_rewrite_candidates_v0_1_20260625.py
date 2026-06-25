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
    detected_drift_signals,
    load_jsonl,
    validate_no_forbidden_claims,
    validate_private_identifier_absence,
)


ROOT = Path(__file__).resolve().parents[1]
VERSION = "v0_1_20260625"
DATE = "2026 06 25"
DATE_TOKEN = "20260625"
ATLAS_LAYER = "Multilingual Medical Intelligence"
ATLAS_NODE_ID = "mia_mmi_002"

PUBLIC_WORDING_BANK = (
    ROOT / "data" / "multilingual_medical_intelligence_public_wording_bank_v0_1_20260625.jsonl"
)
DRIFT_NEGATIVE_CONTROLS = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_public_wording_drift_negative_controls_v0_1_20260625.jsonl"
)
DRIFT_SCORE_REPORT = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_public_wording_drift_score_report_v0_1_20260625.json"
)
REWRITE_CANDIDATES = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_public_wording_rewrite_candidates_v0_1_20260625.jsonl"
)
OUTPUT_JSON = (
    ROOT
    / "data"
    / "multilingual_medical_intelligence_rewrite_candidate_score_report_v0_1_20260625.json"
)
OUTPUT_MARKDOWN = (
    ROOT
    / "docs"
    / "MULTILINGUAL_MEDICAL_INTELLIGENCE_REWRITE_CANDIDATE_SCORE_REPORT_V0_1_20260625.md"
)

DRIFT_SIGNAL_ORDER = [
    "missing_data_removed",
    "source_support_weakened",
    "certainty_increased",
    "patient_facing_instruction_added",
    "diagnosis_or_treatment_instruction_added",
]

REQUIRED_CANDIDATE_FIELDS = {
    "candidate_id",
    "fixture_version",
    "atlas_layer",
    "atlas_node_id",
    "source_row_id",
    "source_state_pair_id",
    "source_negative_control_id",
    "language_pair",
    "clinical_domain",
    "candidate_type",
    "drift_type",
    "candidate_public_wording_en",
    "candidate_public_wording_tr_ascii",
    "expected_status",
    "expected_failure_reasons",
    "drift_signals",
    "must_fail_review_gate",
    "expected_review_outcome",
    "must_match_source_boundary",
    "release_boundary",
}

ALLOWED_DRIFT_TYPES = {
    "boundary_preserving_rewrite",
    "missing_data_removed",
    "source_support_weakened",
    "certainty_increased",
    "patient_facing_instruction_added",
    "diagnosis_or_treatment_instruction_added",
    "translation_certainty_increased",
}

EXPECTED_BOUNDARY_FLAGS = {
    "synthetic_only": True,
    "patient_data_used": False,
    "clinical_use_allowed": False,
    "clinical_advice_allowed": False,
    "external_urls_present": False,
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


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def signal_object(signals: list[str]) -> dict[str, bool]:
    signal_set = set(signals)
    return {signal: signal in signal_set for signal in DRIFT_SIGNAL_ORDER}


def true_signals(row: dict[str, Any]) -> list[str]:
    drift_signals = row.get("drift_signals")
    if not isinstance(drift_signals, dict):
        return []
    return [signal for signal in DRIFT_SIGNAL_ORDER if drift_signals.get(signal) is True]


def candidate_as_negative_control(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "mutated_public_wording_en": candidate.get("candidate_public_wording_en", ""),
        "mutated_public_wording_tr_ascii": candidate.get(
            "candidate_public_wording_tr_ascii", ""
        ),
    }


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


def load_score_profile(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{repo_relative(path)} root must be an object")
    return payload


def validate_candidate_rows(
    candidates: list[dict[str, Any]],
    public_rows: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    score_profile: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    public_by_id = {str(row.get("row_id")): row for row in public_rows}
    controls_by_id = {str(row.get("control_id")): row for row in controls}

    if len(candidates) != 16:
        errors.append(f"Expected 16 rewrite candidate rows, found {len(candidates)}")

    if score_profile.get("status") != "local_fixture_pass":
        errors.append("drift score profile status must be local_fixture_pass")

    seen: set[str] = set()
    pass_count = 0
    fail_count = 0
    covered_sources: set[str] = set()

    for index, row in enumerate(candidates, 1):
        candidate_id = row.get("candidate_id")
        label = candidate_id if isinstance(candidate_id, str) else f"candidate {index}"

        missing_fields = sorted(REQUIRED_CANDIDATE_FIELDS - set(row))
        if missing_fields:
            errors.append(f"{label}: missing fields: {', '.join(missing_fields)}")
            continue

        if not isinstance(candidate_id, str) or not re.fullmatch(
            r"MMI_PUBLIC_WORDING_REWRITE_CANDIDATE_\d{3}", candidate_id
        ):
            errors.append(f"{label}: candidate_id must match rewrite candidate pattern")
        elif candidate_id in seen:
            errors.append(f"{label}: duplicate candidate_id")
        else:
            seen.add(candidate_id)

        if row.get("fixture_version") != VERSION:
            errors.append(f"{label}: fixture_version must be {VERSION}")
        if row.get("atlas_layer") != ATLAS_LAYER:
            errors.append(f"{label}: atlas_layer must be {ATLAS_LAYER}")
        if row.get("atlas_node_id") != ATLAS_NODE_ID:
            errors.append(f"{label}: atlas_node_id must be {ATLAS_NODE_ID}")
        if row.get("language_pair") != "Turkish English":
            errors.append(f"{label}: language_pair must be Turkish English")
        if row.get("must_match_source_boundary") is not True:
            errors.append(f"{label}: must_match_source_boundary must be true")

        source_row = public_by_id.get(str(row.get("source_row_id")))
        source_control = controls_by_id.get(str(row.get("source_negative_control_id")))
        if source_row is None:
            errors.append(f"{label}: source_row_id must match public wording bank")
        else:
            covered_sources.add(str(row.get("source_row_id")))
            if row.get("source_state_pair_id") != source_row.get("source_state_pair_id"):
                errors.append(f"{label}: source_state_pair_id must match source row")
            if row.get("clinical_domain") != source_row.get("clinical_domain"):
                errors.append(f"{label}: clinical_domain must match source row")

        if source_control is None:
            errors.append(f"{label}: source_negative_control_id must match drift controls")
        else:
            if row.get("source_row_id") != source_control.get("source_row_id"):
                errors.append(f"{label}: source_negative_control_id must match source row")
            if row.get("source_state_pair_id") != source_control.get("source_state_pair_id"):
                errors.append(f"{label}: source_negative_control_id must match source pair")

        expected_status = row.get("expected_status")
        if expected_status == "pass":
            pass_count += 1
            if row.get("must_fail_review_gate") is not False:
                errors.append(f"{label}: pass candidates must not fail review gate")
            if row.get("expected_review_outcome") != "passes_local_rewrite_candidate_gate":
                errors.append(f"{label}: pass candidate review outcome mismatch")
        elif expected_status == "fail":
            fail_count += 1
            if row.get("must_fail_review_gate") is not True:
                errors.append(f"{label}: fail candidates must fail review gate")
            if row.get("expected_review_outcome") != "blocked_expected_fail_candidate":
                errors.append(f"{label}: fail candidate review outcome mismatch")
        else:
            errors.append(f"{label}: expected_status must be pass or fail")

        drift_type = row.get("drift_type")
        if drift_type not in ALLOWED_DRIFT_TYPES:
            errors.append(f"{label}: unsupported drift_type: {drift_type}")

        for field in ("candidate_public_wording_en", "candidate_public_wording_tr_ascii"):
            value = row.get(field)
            if not isinstance(value, str) or len(value.split()) < 10:
                errors.append(f"{label}: {field} must contain at least 10 words")
            elif field.endswith("_tr_ascii") and not value.isascii():
                errors.append(f"{label}: {field} must be ASCII")

        declared_signals = row.get("drift_signals")
        expected_reasons = row.get("expected_failure_reasons")
        if not isinstance(declared_signals, dict) or set(declared_signals) != set(
            DRIFT_SIGNAL_ORDER
        ):
            errors.append(f"{label}: drift_signals must exactly match drift signal keys")
            declared_signals = {}
        if not isinstance(expected_reasons, list):
            errors.append(f"{label}: expected_failure_reasons must be a list")
            expected_reasons = []
        else:
            for reason in expected_reasons:
                if reason not in DRIFT_SIGNAL_ORDER:
                    errors.append(f"{label}: unsupported expected failure reason: {reason}")
                if declared_signals.get(reason) is not True:
                    errors.append(f"{label}: expected reason must have true drift signal: {reason}")

        if expected_status == "pass" and expected_reasons:
            errors.append(f"{label}: pass candidates must not include failure reasons")
        if expected_status == "fail" and not expected_reasons:
            errors.append(f"{label}: fail candidates must include failure reasons")
        if expected_status == "pass" and any(value is True for value in declared_signals.values()):
            errors.append(f"{label}: pass candidates must not declare drift signals")
        if expected_status == "fail" and not any(value is True for value in declared_signals.values()):
            errors.append(f"{label}: fail candidates must declare at least one drift signal")

        observed = detected_drift_signals(candidate_as_negative_control(row))
        for signal, expected in declared_signals.items():
            if bool(expected) != bool(observed.get(signal)):
                errors.append(f"{label}: observed drift signal mismatch: {signal}")

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
        errors.append(f"Expected 8 pass candidates, found {pass_count}")
    if fail_count != 8:
        errors.append(f"Expected 8 fail candidates, found {fail_count}")
    if covered_sources != set(public_by_id):
        errors.append("Rewrite candidates must cover every public wording source row")

    return errors


def build_report(
    public_rows: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    score_profile: dict[str, Any],
) -> dict[str, Any]:
    public_by_id = {str(row["row_id"]): row for row in public_rows}
    controls_by_id = {str(row["control_id"]): row for row in controls}
    detected_counts: Counter[str] = Counter()
    declared_counts: Counter[str] = Counter()
    failure_counts: Counter[str] = Counter()

    candidate_results: list[dict[str, Any]] = []
    pass_candidates: list[str] = []
    blocked_candidates: list[str] = []
    critical_action_boundary_candidates = 0

    for candidate in candidates:
        source = public_by_id[str(candidate["source_row_id"])]
        control = controls_by_id[str(candidate["source_negative_control_id"])]
        declared = true_signals(candidate)
        detected = [
            signal
            for signal, value in detected_drift_signals(candidate_as_negative_control(candidate)).items()
            if value is True
        ]
        expected_reasons = [str(reason) for reason in candidate["expected_failure_reasons"]]
        declared_counts.update(declared)
        detected_counts.update(detected)
        failure_counts.update(expected_reasons)

        observed_status = "fail" if detected else "pass"
        expected_status = str(candidate["expected_status"])
        review_outcome = (
            "blocked_expected_fail_candidate"
            if observed_status == "fail"
            else "passes_local_rewrite_candidate_gate"
        )
        if observed_status == "pass":
            pass_candidates.append(str(candidate["candidate_id"]))
        else:
            blocked_candidates.append(str(candidate["candidate_id"]))
        if (
            "patient_facing_instruction_added" in detected
            or "diagnosis_or_treatment_instruction_added" in detected
        ):
            critical_action_boundary_candidates += 1

        candidate_results.append(
            {
                "candidate_id": candidate["candidate_id"],
                "source_row_id": candidate["source_row_id"],
                "source_state_pair_id": candidate["source_state_pair_id"],
                "source_negative_control_id": candidate["source_negative_control_id"],
                "clinical_domain": candidate["clinical_domain"],
                "candidate_type": candidate["candidate_type"],
                "drift_type": candidate["drift_type"],
                "expected_status": expected_status,
                "observed_status": observed_status,
                "expected_review_outcome": candidate["expected_review_outcome"],
                "observed_review_outcome": review_outcome,
                "status_match": expected_status == observed_status,
                "review_outcome_match": candidate["expected_review_outcome"] == review_outcome,
                "expected_failure_reasons": expected_reasons,
                "detected_drift_signals": detected,
                "drift_signals_declared": signal_object(declared),
                "drift_signals_detected": signal_object(detected),
                "source_row_missing_data_preserved": source["missing_data_to_preserve"],
                "source_row_support_preserved": source["source_support_to_preserve"],
                "source_control_failure_profile": control["expected_failure_reasons"],
                "boundary_pass": True,
            }
        )

    source_row_coverage = []
    for source_row_id in sorted(public_by_id):
        related = [
            result
            for result in candidate_results
            if result["source_row_id"] == source_row_id
        ]
        source_row_coverage.append(
            {
                "source_row_id": source_row_id,
                "source_state_pair_id": public_by_id[source_row_id]["source_state_pair_id"],
                "clinical_domain": public_by_id[source_row_id]["clinical_domain"],
                "candidate_count": len(related),
                "pass_candidate_count": sum(
                    1 for result in related if result["observed_status"] == "pass"
                ),
                "blocked_candidate_count": sum(
                    1 for result in related if result["observed_status"] == "fail"
                ),
                "candidate_ids": [result["candidate_id"] for result in related],
            }
        )

    return {
        "report_id": "multilingual_medical_intelligence_rewrite_candidate_score_report_v0_1_20260625",
        "report_type": "machine_readable_rewrite_candidate_drift_score_report",
        "report_version": VERSION,
        "generated_date": DATE_TOKEN,
        "atlas_layer": ATLAS_LAYER,
        "atlas_node_id": ATLAS_NODE_ID,
        "status": "local_fixture_pass",
        "report_scope": "local_fixture_rewrite_candidate_gate_only",
        "scope": "Local synthetic rewrite candidate drift scorer for public wording attempts.",
        "artifact_paths": {
            "public_wording_bank": repo_relative(PUBLIC_WORDING_BANK),
            "drift_negative_controls": repo_relative(DRIFT_NEGATIVE_CONTROLS),
            "drift_score_profile": repo_relative(DRIFT_SCORE_REPORT),
            "rewrite_candidates": repo_relative(REWRITE_CANDIDATES),
            "score_report_json": repo_relative(OUTPUT_JSON),
            "score_report_markdown": repo_relative(OUTPUT_MARKDOWN),
            "scorer": "scripts/score_multilingual_medical_intelligence_rewrite_candidates_v0_1_20260625.py",
            "validator": "scripts/validate_multilingual_medical_intelligence_rewrite_candidate_score_report_v0_1_20260625.py",
        },
        "validation": {
            "score_profile_status": score_profile.get("status"),
            "scorer_command": "python3 scripts/score_multilingual_medical_intelligence_rewrite_candidates_v0_1_20260625.py --check",
            "validator_command": "python3 scripts/validate_multilingual_medical_intelligence_rewrite_candidate_score_report_v0_1_20260625.py",
            "make_target": "make multilingual_medical_intelligence_rewrite_candidate_drift_scorer",
            "expected_result": "pass",
        },
        "score_summary": {
            "candidate_count": len(candidates),
            "expected_pass_candidates": sum(
                1 for candidate in candidates if candidate["expected_status"] == "pass"
            ),
            "expected_fail_candidates": sum(
                1 for candidate in candidates if candidate["expected_status"] == "fail"
            ),
            "observed_pass_candidates": len(pass_candidates),
            "observed_blocked_candidates": len(blocked_candidates),
            "source_row_coverage_count": len(
                {str(candidate["source_row_id"]) for candidate in candidates}
            ),
            "source_state_pair_count": len(
                {str(candidate["source_state_pair_id"]) for candidate in candidates}
            ),
            "critical_action_boundary_candidates": critical_action_boundary_candidates,
            "status_mismatch_count": sum(
                1 for result in candidate_results if result["status_match"] is not True
            ),
            "review_outcome_mismatch_count": sum(
                1 for result in candidate_results if result["review_outcome_match"] is not True
            ),
        },
        "drift_signal_counts": {
            "declared_true": {
                signal: declared_counts.get(signal, 0) for signal in DRIFT_SIGNAL_ORDER
            },
            "detected_true": {
                signal: detected_counts.get(signal, 0) for signal in DRIFT_SIGNAL_ORDER
            },
            "mismatch_count": sum(
                1
                for result in candidate_results
                if result["drift_signals_declared"] != result["drift_signals_detected"]
            ),
        },
        "failure_reason_counts": {
            signal: failure_counts.get(signal, 0) for signal in DRIFT_SIGNAL_ORDER
        },
        "source_row_coverage": source_row_coverage,
        "candidate_results": candidate_results,
        "pass_candidate_ids": pass_candidates,
        "blocked_candidate_ids": blocked_candidates,
        "reviewer_triage": {
            "primary_question": "Does the candidate rewrite preserve the public wording source row boundary.",
            "triage_order": [
                "diagnosis_or_treatment_instruction_added",
                "patient_facing_instruction_added",
                "missing_data_removed",
                "source_support_weakened",
                "certainty_increased",
            ],
            "blocked_use": [
                "patient care",
                "clinical advice",
                "clinical validation claim",
                "clinical deployment claim",
                "model ranking claim",
                "partner or institution claim",
            ],
        },
        "release_boundary": {
            "synthetic_only": True,
            "patient_data_used": False,
            "clinical_use_allowed": False,
            "clinical_advice_allowed": False,
            "external_urls_present": False,
            "diagnosis_or_treatment_instruction_allowed": False,
            "clinical_validation_claim_made": False,
            "clinical_deployment_claim_made": False,
            "model_superiority_claim_made": False,
            "model_ranking_claim_made": False,
            "partner_or_institution_claim_made": False,
            "score_certification_claim_made": False,
            "source_truth_certification_claim_made": False,
            "external_publication_clearance": False,
            "allowed_use": "Repo local synthetic rewrite candidate scoring before any public wording is reused.",
            "not_allowed_use": "Patient care, clinical advice, external publication clearance, model ranking, or release claim.",
            "not_model_ranking": True,
            "not_clinical_validation": True,
        },
        "blockers": [],
        "exact_next_action": "Add cross language negation and audience role controls so translations cannot invert warnings or shift who the wording addresses.",
    }


def markdown_list(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["score_summary"]
    lines = [
        "# Multilingual Medical Intelligence Rewrite Candidate Drift Scorer v0.1",
        "",
        f"Date: {DATE}",
        "",
        "Status: ready for local repo review only",
        "",
        "## Purpose",
        "",
        "This scorer checks candidate public rewrites against the existing public wording bank and the local drift score profile.",
        "",
        "It blocks candidate rewrites that remove missing data, weaken source support, add certainty, add patient facing instructions, or add diagnosis or treatment instructions.",
        "",
        "The scorer uses synthetic rows only. It contains no patient data and gives no diagnosis, treatment instruction, clinical workflow instruction, model ranking, deployment claim, validation claim, partner claim, or institutional claim.",
        "",
        "## Score Summary",
        "",
        *markdown_list(
            [
                f"Candidate rows: {summary['candidate_count']}.",
                f"Expected pass candidates: {summary['expected_pass_candidates']}.",
                f"Expected fail candidates: {summary['expected_fail_candidates']}.",
                f"Observed pass candidates: {summary['observed_pass_candidates']}.",
                f"Observed blocked candidates: {summary['observed_blocked_candidates']}.",
                f"Source row coverage count: {summary['source_row_coverage_count']}.",
                f"Critical action boundary candidates: {summary['critical_action_boundary_candidates']}.",
            ]
        ),
        "",
        "## Drift Signal Counts",
        "",
    ]
    for index, signal in enumerate(DRIFT_SIGNAL_ORDER, 1):
        lines.append(
            f"{index}. `{signal}`: declared {report['drift_signal_counts']['declared_true'][signal]}, detected {report['drift_signal_counts']['detected_true'][signal]}."
        )

    lines.extend(["", "## Source Row Coverage", ""])
    for index, row in enumerate(report["source_row_coverage"], 1):
        lines.extend(
            [
                f"### {index}. {row['source_row_id']}",
                "",
                f"Clinical domain: {row['clinical_domain']}",
                "",
                f"Candidate count: {row['candidate_count']}",
                "",
                f"Pass candidates: {row['pass_candidate_count']}",
                "",
                f"Blocked candidates: {row['blocked_candidate_count']}",
                "",
            ]
        )

    lines.extend(
        [
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
            "This scorer supports repo local review only. It does not clear text for patient care, clinical advice, clinical validation, clinical deployment, model comparison, institutional use, or external publication.",
            "",
            "Boundary note: not score certification, not source truth certification, not clinical validation, not clinical deployment, and not external publication clearance.",
            "",
            "## Validation Command",
            "",
            "`make multilingual_medical_intelligence_rewrite_candidate_drift_scorer`",
            "",
            "Direct check:",
            "",
            "`python3 scripts/score_multilingual_medical_intelligence_rewrite_candidates_v0_1_20260625.py --check`",
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
        "candidate_count": 16,
        "expected_pass_candidates": 8,
        "expected_fail_candidates": 8,
        "observed_pass_candidates": 8,
        "observed_blocked_candidates": 8,
        "source_row_coverage_count": 8,
        "critical_action_boundary_candidates": 4,
        "status_mismatch_count": 0,
        "review_outcome_mismatch_count": 0,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"score_summary.{key} must be {expected}")

    drift_counts = report.get("drift_signal_counts", {})
    if not isinstance(drift_counts, dict):
        errors.append("drift_signal_counts must be an object")
    else:
        for group in ("declared_true", "detected_true"):
            if set(drift_counts.get(group, {})) != set(DRIFT_SIGNAL_ORDER):
                errors.append(f"drift_signal_counts.{group} must contain required signals")
        if drift_counts.get("mismatch_count") != 0:
            errors.append("drift_signal_counts.mismatch_count must be 0")

    if set(report.get("failure_reason_counts", {})) != set(DRIFT_SIGNAL_ORDER):
        errors.append("failure_reason_counts must contain exactly the drift signals")

    candidate_results = report.get("candidate_results")
    if not isinstance(candidate_results, list) or len(candidate_results) != 16:
        errors.append("candidate_results must contain 16 rows")
    else:
        pass_rows = [row for row in candidate_results if row.get("observed_status") == "pass"]
        fail_rows = [row for row in candidate_results if row.get("observed_status") == "fail"]
        if len(pass_rows) != 8:
            errors.append("candidate_results must contain 8 pass rows")
        if len(fail_rows) != 8:
            errors.append("candidate_results must contain 8 fail rows")
        for row in candidate_results:
            if row.get("status_match") is not True:
                errors.append(f"{row.get('candidate_id')}: status_match must be true")
            if row.get("review_outcome_match") is not True:
                errors.append(f"{row.get('candidate_id')}: review_outcome_match must be true")
            if row.get("boundary_pass") is not True:
                errors.append(f"{row.get('candidate_id')}: boundary_pass must be true")

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
        "candidate public rewrites",
        "local drift score profile",
        "remove missing data",
        "weaken source support",
        "add certainty",
        "patient facing instructions",
        "diagnosis or treatment instructions",
        "not score certification",
        "not source truth certification",
        "not clinical validation",
        "not clinical deployment",
        "not external publication clearance",
        "make multilingual_medical_intelligence_rewrite_candidate_drift_scorer",
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
    for path in (PUBLIC_WORDING_BANK, DRIFT_NEGATIVE_CONTROLS, DRIFT_SCORE_REPORT, REWRITE_CANDIDATES):
        if not path.exists():
            errors.append(f"missing required file: {repo_relative(path)}")
    if errors:
        print("FAIL rewrite candidate drift scorer")
        for error in errors:
            print(f"- {error}")
        return 1

    try:
        public_rows = load_jsonl(PUBLIC_WORDING_BANK)
        controls = load_jsonl(DRIFT_NEGATIVE_CONTROLS)
        candidates = load_jsonl(REWRITE_CANDIDATES)
        score_profile = load_score_profile(DRIFT_SCORE_REPORT)
    except (ValueError, json.JSONDecodeError) as error:
        print(f"FAIL rewrite candidate drift scorer: {error}")
        return 1

    errors.extend(validate_candidate_rows(candidates, public_rows, controls, score_profile))
    report = build_report(public_rows, controls, candidates, score_profile)
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
        print("FAIL rewrite candidate drift scorer")
        for error in errors:
            print(f"- {error}")
        return 1

    if check:
        print("PASS rewrite candidate drift scorer")
        print(f"candidates={report['score_summary']['candidate_count']}")
        print(f"blocked_candidates={report['score_summary']['observed_blocked_candidates']}")
        print(f"pass_candidates={report['score_summary']['observed_pass_candidates']}")
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
