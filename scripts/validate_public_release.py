#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


BLOCKED_DIR_NAMES = {
    "__pycache__",
    "raw_outputs",
    "logs",
    "results",
    "review_forms",
}

BLOCKED_SUFFIXES = {
    ".pyc",
}

VCS_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
}

def joined(*parts: str) -> str:
    return "".join(parts)


BLOCKED_TEXT_PATTERNS = [
    joined("/", "Users", "/", "goktugozkan"),
    joined("--dangerously", "-", "skip", "-", "permissions"),
    joined("de", "AI"),
    joined("human", "ized"),
    joined("submit", "_audit"),
    joined("AI", " detector"),
]

REQUIRED_FILES = [
    "README.md",
    "Makefile",
    "DATA_DICTIONARY.md",
    "DATASET_EVALUATION_CARD_V0_1_DRAFT.md",
    "PUBLIC_RELEASE_BOUNDARY_V0_1.md",
    "RELEASE_MANIFEST_V0_1_DRAFT.md",
    "CONTRIBUTING.md",
    "PUBLIC_RELEASE_CANDIDATE_STATUS.md",
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
    "docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md",
    "docs/label_audit_reviewer_role_table_v0_1.json",
    "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    "docs/label_audit/label_audit_example_intake_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md",
    "docs/label_audit/label_audit_example_dashboard_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md",
    "docs/label_audit/label_audit_maintainer_triage_board_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/label_audit/label_audit_public_wording_decision_log_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md",
    "docs/label_audit/label_audit_release_gate_checklist_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
    "docs/label_audit/label_audit_release_gate_outcome_dashboard_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_RELEASE_NOTE_PACKET_V0_1.md",
    "docs/label_audit/label_audit_release_note_packet_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_CHANGELOG_V0_1.md",
    "docs/label_audit/label_audit_public_changelog_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_RELEASE_INDEX_V0_1.md",
    "docs/label_audit/label_audit_public_release_index_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_CONTRIBUTOR_DIGEST_V0_1.md",
    "docs/label_audit/label_audit_public_contributor_digest_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_HANDOFF_NOTES_V0_1.md",
    "docs/label_audit/label_audit_maintainer_handoff_notes_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md",
    "docs/label_audit/label_audit_maintainer_closeout_digest_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_RELEASE_READINESS_DIGEST_V0_1.md",
    "docs/label_audit/label_audit_maintainer_release_readiness_digest_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_EVIDENCE_MAP_V0_1.md",
    "docs/label_audit/label_audit_maintainer_evidence_map_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_AUDIT_TRAIL_PACKET_V0_1.md",
    "docs/label_audit/label_audit_maintainer_audit_trail_packet_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_RELEASE_CANDIDATE_SUMMARY_V0_1.md",
    "docs/label_audit/label_audit_maintainer_release_candidate_summary_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_PUBLIC_PREVIEW_DECISION_LOG_V0_1.md",
    "docs/label_audit/label_audit_maintainer_public_preview_decision_log_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_PUBLIC_PREVIEW_HANDOFF_SUMMARY_V0_1.md",
    "docs/label_audit/label_audit_maintainer_public_preview_handoff_summary_v0_1.json",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_PUBLIC_PREVIEW_CLOSURE_CHECKLIST_V0_1.md",
    "docs/label_audit/label_audit_maintainer_public_preview_closure_checklist_v0_1.json",
    "docs/tr-medai-safety-suite/BILGE_READINESS_QUEUE_V0_1.md",
    "docs/tr-medai-safety-suite/bilge_readiness_queue_v0_1.json",
    "docs/tr-medai-safety-suite/TUBITAK_1711_COLLABORATION_READINESS_PACKET_V0_1.md",
    "docs/tr-medai-safety-suite/tubitak_1711_collaboration_readiness_packet_v0_1.json",
    "docs/HEALTHBENCH_MEDHELM_MAPPING_NOTE_V0_1.md",
    "docs/healthbench_medhelm_mapping_note_v0_1.json",
    "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/benchmark_style_reviewer_questions_v0_1.json",
    "docs/CONTRIBUTOR_ISSUE_TEMPLATE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
    "docs/reviewer_question_intake_examples_v0_1.json",
    "scripts/generate_reviewer_question_intake_examples_v0_1.py",
    "scripts/validate_reviewer_question_intake_examples_v0_1.py",
    "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
    "docs/reviewer_question_intake_triage_board_v0_1.json",
    "scripts/generate_reviewer_question_intake_triage_board_v0_1.py",
    "scripts/validate_reviewer_question_intake_triage_board_v0_1.py",
    "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/reviewer_question_public_wording_decision_log_v0_1.json",
    "scripts/generate_reviewer_question_public_wording_decision_log_v0_1.py",
    "scripts/validate_reviewer_question_public_wording_decision_log_v0_1.py",
    "docs/REVIEWER_QUESTION_RELEASE_GATE_CHECKLIST_V0_1.md",
    "docs/reviewer_question_release_gate_checklist_v0_1.json",
    "scripts/generate_reviewer_question_release_gate_checklist_v0_1.py",
    "scripts/validate_reviewer_question_release_gate_checklist_v0_1.py",
    "docs/REVIEWER_QUESTION_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
    "docs/reviewer_question_release_gate_outcome_dashboard_v0_1.json",
    "scripts/generate_reviewer_question_release_gate_outcome_dashboard_v0_1.py",
    "scripts/validate_reviewer_question_release_gate_outcome_dashboard_v0_1.py",
    "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_PACKET_V0_1.md",
    "docs/reviewer_question_public_release_packet_v0_1.json",
    "scripts/generate_reviewer_question_public_release_packet_v0_1.py",
    "scripts/validate_reviewer_question_public_release_packet_v0_1.py",
    "docs/REVIEWER_QUESTION_PUBLIC_CHANGELOG_V0_1.md",
    "docs/reviewer_question_public_changelog_v0_1.json",
    "scripts/generate_reviewer_question_public_changelog_v0_1.py",
    "scripts/validate_reviewer_question_public_changelog_v0_1.py",
    "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_INDEX_V0_1.md",
    "docs/reviewer_question_public_release_index_v0_1.json",
    "scripts/generate_reviewer_question_public_release_index_v0_1.py",
    "scripts/validate_reviewer_question_public_release_index_v0_1.py",
    "docs/REVIEWER_QUESTION_PUBLIC_CONTRIBUTOR_DIGEST_V0_1.md",
    "docs/reviewer_question_public_contributor_digest_v0_1.json",
    "scripts/generate_reviewer_question_public_contributor_digest_v0_1.py",
    "scripts/validate_reviewer_question_public_contributor_digest_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_HANDOFF_NOTES_V0_1.md",
    "docs/reviewer_question_maintainer_handoff_notes_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_handoff_notes_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_handoff_notes_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md",
    "docs/reviewer_question_maintainer_closeout_digest_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_closeout_digest_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_closeout_digest_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_RELEASE_READINESS_DIGEST_V0_1.md",
    "docs/reviewer_question_maintainer_release_readiness_digest_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_release_readiness_digest_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_release_readiness_digest_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_EVIDENCE_MAP_V0_1.md",
    "docs/reviewer_question_maintainer_evidence_map_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_evidence_map_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_evidence_map_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_AUDIT_TRAIL_PACKET_V0_1.md",
    "docs/reviewer_question_maintainer_audit_trail_packet_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_audit_trail_packet_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_audit_trail_packet_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_RELEASE_CANDIDATE_SUMMARY_V0_1.md",
    "docs/reviewer_question_maintainer_release_candidate_summary_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_release_candidate_summary_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_release_candidate_summary_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_DECISION_LOG_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_decision_log_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_public_preview_decision_log_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_public_preview_decision_log_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_HANDOFF_SUMMARY_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_handoff_summary_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_public_preview_handoff_summary_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_public_preview_handoff_summary_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_CLOSURE_CHECKLIST_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_closure_checklist_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_public_preview_closure_checklist_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_public_preview_closure_checklist_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ARCHIVE_DIGEST_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_archive_digest_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_public_preview_archive_digest_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_public_preview_archive_digest_v0_1.py",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_INDEX_ROLLUP_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_index_rollup_v0_1.json",
    "scripts/generate_reviewer_question_maintainer_public_preview_index_rollup_v0_1.py",
    "scripts/validate_reviewer_question_maintainer_public_preview_index_rollup_v0_1.py",
    "docs/MEDHELM_BOUNDARY_NOTE_V0_1.md",
    "docs/MEDMARKS_BOUNDARY_NOTE_V0_1.md",
    "docs/ASSURANCE_CARD_TEMPLATE_V0_1.md",
    "docs/assurance_card_template_v0_1.json",
    "docs/ASSURANCE_RELEASE_GATE_EXAMPLE_MAP_V0_1.md",
    "docs/assurance_release_gate_example_map_v0_1.json",
    "docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md",
    "docs/sourcecheckup_tr_medllm_assurance_routing_map_v0_1.json",
    "docs/SOURCE_REVIEW_WORKSHEETS_V0_1.md",
    "docs/source_review_worksheets_v0_1.json",
    "docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md",
    "docs/red_flag_warning_checklist_v0_1.json",
    "docs/WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md",
    "docs/warning_sign_reviewer_role_table_v0_1.json",
    "docs/PLATFORM_DASHBOARD_INDEX_V0_1.md",
    "docs/CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md",
    "docs/clinician_literacy_release_gate_lesson_map_v0_1.json",
    "docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md",
    "docs/sourcecheckup/RED_FLAG_SOURCE_LOCATOR_CONTRIBUTOR_EXAMPLES_V0_1.md",
    "docs/sourcecheckup/SOURCECHECKUP_TURKISH_INSTITUTIONAL_WORDING_EXAMPLES_V0_1.md",
    "docs/sourcecheckup/sourcecheckup_turkish_institutional_wording_examples_v0_1.json",
    "docs/sourcecheckup/SOURCECHECKUP_REPO_RUN_GUIDE_V0_1.md",
    "docs/sourcecheckup/sourcecheckup_repo_run_guide_v0_1.json",
    "docs/sourcecheckup/sourcecheckup_repo_doctor_v0_1.json",
    ".github/ISSUE_TEMPLATE/label_audit_review.yml",
    "tr_medllm_safetybench/build/specialty_spread_dashboard_v0_1.md",
    "sourcecheckup/build/source_claim_example_expansion_v0_2.md",
    ".github/ISSUE_TEMPLATE/sourcecheckup_review.yml",
    ".gitignore",
    "data/scenario_bank_v1.tsv",
    "data/scenario_bank_v2_hard_addendum.tsv",
    "data/scenario_bank_v3_scale_seed.tsv",
    "data/scenario_taxonomy_v0_2.tsv",
    "data/failure_atlas_external_sample_v0_1.jsonl",
    "data/medhelm_remote_rescue_metric_v0_1.json",
    "data/scoring_rubric_v0_1.json",
    "data/inter_rater_review_subset_v0_1.tsv",
    "data/prompt_set_v1.tsv",
    "data/prompt_set_v2_hard_30.tsv",
    "data/prompt_set_v3_scale_30.tsv",
    "docs/clinician_evaluation_rubric.md",
    "docs/MEDHELM_REMOTE_RESCUE_BOUNDARY_METRIC_PACKAGE_DRAFT.md",
    "docs/MEDMARKS_COMPATIBILITY_DRAFT.md",
    "docs/scoring_model_v0_1.md",
    "failure_atlas/public/INDEX.md",
    "failure_atlas/public/METHODOLOGY.md",
    "scripts/validate_external_sample_jsonl.py",
    "scripts/validate_medhelm_metric_json.py",
    "scripts/validate_model_run_json.py",
    "scripts/validate_scoring_rubric_v0_1.py",
    "scripts/validate_failure_atlas_public_summary_v0_1.py",
    "scripts/validate_health_data_quality_card_v0_1.py",
    "scripts/generate_label_audit_reviewer_role_table_v0_1.py",
    "scripts/validate_label_audit_reviewer_role_table_v0_1.py",
    "scripts/validate_label_audit_public_contributor_issue_v0_1.py",
    "scripts/generate_label_audit_example_intake_v0_1.py",
    "scripts/validate_label_audit_example_intake_v0_1.py",
    "scripts/generate_label_audit_example_dashboard_v0_1.py",
    "scripts/validate_label_audit_example_dashboard_v0_1.py",
    "scripts/generate_label_audit_maintainer_triage_board_v0_1.py",
    "scripts/validate_label_audit_maintainer_triage_board_v0_1.py",
    "scripts/generate_label_audit_public_wording_decision_log_v0_1.py",
    "scripts/validate_label_audit_public_wording_decision_log_v0_1.py",
    "scripts/generate_label_audit_release_gate_checklist_v0_1.py",
    "scripts/validate_label_audit_release_gate_checklist_v0_1.py",
    "scripts/generate_label_audit_release_gate_outcome_dashboard_v0_1.py",
    "scripts/validate_label_audit_release_gate_outcome_dashboard_v0_1.py",
    "scripts/generate_label_audit_release_note_packet_v0_1.py",
    "scripts/validate_label_audit_release_note_packet_v0_1.py",
    "scripts/generate_label_audit_public_changelog_v0_1.py",
    "scripts/validate_label_audit_public_changelog_v0_1.py",
    "scripts/generate_label_audit_public_release_index_v0_1.py",
    "scripts/validate_label_audit_public_release_index_v0_1.py",
    "scripts/generate_label_audit_public_contributor_digest_v0_1.py",
    "scripts/validate_label_audit_public_contributor_digest_v0_1.py",
    "scripts/generate_label_audit_maintainer_handoff_notes_v0_1.py",
    "scripts/validate_label_audit_maintainer_handoff_notes_v0_1.py",
    "scripts/generate_label_audit_maintainer_closeout_digest_v0_1.py",
    "scripts/validate_label_audit_maintainer_closeout_digest_v0_1.py",
    "scripts/generate_label_audit_maintainer_release_readiness_digest_v0_1.py",
    "scripts/validate_label_audit_maintainer_release_readiness_digest_v0_1.py",
    "scripts/generate_label_audit_maintainer_evidence_map_v0_1.py",
    "scripts/validate_label_audit_maintainer_evidence_map_v0_1.py",
    "scripts/generate_label_audit_maintainer_audit_trail_packet_v0_1.py",
    "scripts/validate_label_audit_maintainer_audit_trail_packet_v0_1.py",
    "scripts/generate_label_audit_maintainer_release_candidate_summary_v0_1.py",
    "scripts/validate_label_audit_maintainer_release_candidate_summary_v0_1.py",
    "scripts/generate_label_audit_maintainer_public_preview_decision_log_v0_1.py",
    "scripts/validate_label_audit_maintainer_public_preview_decision_log_v0_1.py",
    "scripts/generate_label_audit_maintainer_public_preview_handoff_summary_v0_1.py",
    "scripts/validate_label_audit_maintainer_public_preview_handoff_summary_v0_1.py",
    "scripts/generate_label_audit_maintainer_public_preview_closure_checklist_v0_1.py",
    "scripts/validate_label_audit_maintainer_public_preview_closure_checklist_v0_1.py",
    "scripts/generate_bilge_readiness_queue_v0_1.py",
    "scripts/validate_bilge_readiness_queue_v0_1.py",
    "scripts/generate_tubitak_1711_collaboration_readiness_packet_v0_1.py",
    "scripts/validate_tubitak_1711_collaboration_readiness_packet_v0_1.py",
    "scripts/validate_boundary_notes_v0_1.py",
    "scripts/validate_assurance_card_template_v0_1.py",
    "scripts/generate_assurance_release_gate_example_map_v0_1.py",
    "scripts/validate_assurance_release_gate_example_map_v0_1.py",
    "scripts/generate_sourcecheckup_tr_medllm_assurance_routing_map_v0_1.py",
    "scripts/validate_sourcecheckup_tr_medllm_assurance_routing_map_v0_1.py",
    "scripts/generate_source_review_worksheets_v0_1.py",
    "scripts/validate_source_review_worksheets_v0_1.py",
    "scripts/generate_red_flag_warning_checklist_v0_1.py",
    "scripts/validate_red_flag_warning_checklist_v0_1.py",
    "scripts/generate_warning_sign_reviewer_role_table_v0_1.py",
    "scripts/validate_warning_sign_reviewer_role_table_v0_1.py",
    "scripts/generate_red_flag_contributor_examples_v0_1.py",
    "scripts/validate_red_flag_contributor_examples_v0_1.py",
    "scripts/generate_sourcecheckup_turkish_institutional_wording_examples_v0_1.py",
    "scripts/validate_sourcecheckup_turkish_institutional_wording_examples_v0_1.py",
    "scripts/sourcecheckup_repo_doctor_v0_1.py",
    "scripts/generate_sourcecheckup_repo_run_guide_v0_1.py",
    "scripts/validate_sourcecheckup_repo_run_guide_v0_1.py",
    "scripts/generate_healthbench_medhelm_mapping_note_v0_1.py",
    "scripts/validate_healthbench_medhelm_mapping_note_v0_1.py",
    "scripts/generate_benchmark_style_reviewer_questions_v0_1.py",
    "scripts/validate_benchmark_style_reviewer_questions_v0_1.py",
    "scripts/validate_benchmark_reviewer_question_issue_templates_v0_1.py",
    "scripts/validate_tr_medllm_specialty_spread_v0_1.py",
    "scripts/generate_tr_medllm_specialty_spread_dashboard_v0_1.py",
    "scripts/validate_tr_medllm_specialty_dashboard_v0_1.py",
    "scripts/validate_platform_dashboard_index_v0_1.py",
    "scripts/generate_clinician_literacy_release_gate_lesson_map_v0_1.py",
    "scripts/validate_clinician_literacy_release_gate_lesson_map_v0_1.py",
    "scripts/validate_sourcecheckup_public_contributor_issue_v0_1.py",
    "scripts/generate_sourcecheckup_example_expansion_dashboard_v0_2.py",
    "scripts/validate_sourcecheckup_example_expansion_dashboard_v0_2.py",
    "scripts/validate_public_release.py",
    "scripts/run_prompt_set_openai_compatible_v2.py",
    "scripts/run_prompt_set_hf_transformers_v2.py",
    "medmarks_candidate_env_v1_20260614/VALIDATION_REPORT.md",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/STAGING_MANIFEST.md",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/configs/failure_atlas_safety_wording_30case_smoke.toml",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/failure_atlas_safety_wording.py",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/judge_prompts.py",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/pyproject.toml",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/data/failure_atlas_medmarks_30_case_seed_v0_1.jsonl",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/docs/MEDMARKS_FAILURE_PROBE_SET_DATASHEET_V0_1.md",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/docs/MEDMARKS_FAILURE_PROBE_TAXONOMY_V0_1.md",
]

STRICT_REQUIRED_FILES = [
    "LICENSE",
    "CITATION.cff",
]


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in {
        "",
        ".cff",
        ".csv",
        ".json",
        ".jsonl",
        ".md",
        ".py",
        ".toml",
        ".tsv",
        ".txt",
        ".yml",
        ".yaml",
    }


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_jsonl(path: Path, errors: list[str]) -> None:
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(errors, f"{path}: line {line_number} invalid JSON: {exc}")
            continue
        if row.get("contains_patient_data") is not False:
            fail(errors, f"{path}: line {line_number} contains_patient_data must be false")
        if row.get("not_for_clinical_use") is not True:
                fail(errors, f"{path}: line {line_number} not_for_clinical_use must be true")


def count_tsv_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle, delimiter="\t"))


def validate(root: Path, strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not root.exists():
        return [f"Release candidate path does not exist: {root}"], warnings

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).exists():
            fail(errors, f"Missing required public candidate file: {relative_path}")

    if strict:
        for relative_path in STRICT_REQUIRED_FILES:
            if not (root / relative_path).exists():
                fail(errors, f"Strict release blocker: missing {relative_path}")
    else:
        for relative_path in STRICT_REQUIRED_FILES:
            if not (root / relative_path).exists():
                warnings.append(f"Draft blocker remains before public release: missing {relative_path}")

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] in VCS_DIR_NAMES:
            continue
        if relative.parts and relative.parts[0] == "review_forms":
            fail(errors, f"Internal review form path present in public candidate: {relative}")
            continue
        if relative.parts and relative.parts[0] == "results":
            fail(errors, f"Internal result path present in public candidate: {relative}")
            continue
        if (
            len(relative.parts) >= 2
            and relative.parts[0] == "docs"
            and path.name.startswith("HEALTHBENCH_")
            and path.name != "HEALTHBENCH_MEDHELM_MAPPING_NOTE_V0_1.md"
        ):
            fail(errors, f"Internal HealthBench workflow doc present in public candidate: {relative}")
            continue
        if path.is_dir() and path.name in BLOCKED_DIR_NAMES:
            fail(errors, f"Blocked directory present: {relative}")
            continue
        if path.is_file() and path.suffix in BLOCKED_SUFFIXES:
            fail(errors, f"Blocked bytecode file present: {relative}")
        if path.is_file() and is_text_file(path):
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in BLOCKED_TEXT_PATTERNS:
                if pattern in text:
                    fail(errors, f"Blocked text pattern {pattern!r} found in {relative}")

    external_sample = root / "data" / "failure_atlas_external_sample_v0_1.jsonl"
    if external_sample.exists():
        validate_jsonl(external_sample, errors)

    medhelm_metric = root / "data" / "medhelm_remote_rescue_metric_v0_1.json"
    if medhelm_metric.exists():
        metric = json.loads(medhelm_metric.read_text(encoding="utf-8"))
        if metric.get("contains_patient_data") is not False:
            fail(errors, "MedHELM metric contains_patient_data must be false")
        if metric.get("not_for_clinical_use") is not True:
            fail(errors, "MedHELM metric not_for_clinical_use must be true")

    readme = root / "README.md"
    readme_text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    if readme.exists():
        if "failure_atlas/public/INDEX.md" not in readme_text:
            fail(errors, "README must link to failure_atlas/public/INDEX.md")
        if "failure_atlas/public/METHODOLOGY.md" not in readme_text:
            fail(errors, "README must link to failure_atlas/public/METHODOLOGY.md")
        if "Raw model outputs and logs are not included" not in readme_text:
            fail(errors, "README must state that raw model outputs and logs are not included")
        if "docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md" not in readme_text:
            fail(errors, "README must link to the SourceCheckup public contributor issue guide")
        if "make sourcecheckup_public_issue" not in readme_text:
            fail(errors, "README must document the SourceCheckup public issue validation command")
        if "docs/PLATFORM_DASHBOARD_INDEX_V0_1.md" not in readme_text:
            fail(errors, "README must link to the platform dashboard index")
        if "make platform_dashboard" not in readme_text:
            fail(errors, "README must document the platform dashboard validation command")
        if "tr_medllm_safetybench/build/specialty_spread_dashboard_v0_1.md" not in readme_text:
            fail(errors, "README must link to the TR MedLLM specialty spread dashboard")
        if "make tr_medllm_specialty_dashboard" not in readme_text:
            fail(errors, "README must document the TR MedLLM specialty dashboard command")
        if "sourcecheckup/build/source_claim_example_expansion_v0_2.md" not in readme_text:
            fail(errors, "README must link to the SourceCheckup expansion dashboard")
        if "make sourcecheckup_expansion_dashboard" not in readme_text:
            fail(errors, "README must document the SourceCheckup expansion dashboard command")
        if "docs/CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md" not in readme_text:
            fail(errors, "README must link to the clinician literacy release gate lesson map")
        if "make clinician_literacy_map" not in readme_text:
            fail(errors, "README must document the clinician literacy lesson map command")
        if "docs/ASSURANCE_RELEASE_GATE_EXAMPLE_MAP_V0_1.md" not in readme_text:
            fail(errors, "README must link to the assurance release gate example map")
        if "make assurance_release_gate_map" not in readme_text:
            fail(errors, "README must document the assurance release gate map command")
        if "docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md" not in readme_text:
            fail(errors, "README must link to the SourceCheckup TR MedLLM assurance routing map")
        if "make sourcecheckup_tr_medllm_routing" not in readme_text:
            fail(errors, "README must document the SourceCheckup TR MedLLM routing command")
        if "docs/SOURCE_REVIEW_WORKSHEETS_V0_1.md" not in readme_text:
            fail(errors, "README must link to the source review worksheets")
        if "make source_review_worksheets" not in readme_text:
            fail(errors, "README must document the source review worksheets command")
        if "docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the red flag warning checklist")
        if "make red_flag_warning_checklist" not in readme_text:
            fail(errors, "README must document the red flag warning checklist command")
        if "docs/WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md" not in readme_text:
            fail(errors, "README must link to the warning sign reviewer role table")
        if "make warning_sign_role_table" not in readme_text:
            fail(errors, "README must document the warning sign reviewer role table command")
        if "docs/sourcecheckup/RED_FLAG_SOURCE_LOCATOR_CONTRIBUTOR_EXAMPLES_V0_1.md" not in readme_text:
            fail(errors, "README must link to red flag contributor examples")
        if "make red_flag_contributor_examples" not in readme_text:
            fail(errors, "README must document the red flag contributor examples command")
        if "docs/sourcecheckup/SOURCECHECKUP_TURKISH_INSTITUTIONAL_WORDING_EXAMPLES_V0_1.md" not in readme_text:
            fail(errors, "README must link to SourceCheckup Turkish institutional wording examples")
        if "make sourcecheckup_turkish_institutional_wording" not in readme_text:
            fail(errors, "README must document the SourceCheckup Turkish institutional wording command")
        if "docs/sourcecheckup/SOURCECHECKUP_REPO_RUN_GUIDE_V0_1.md" not in readme_text:
            fail(errors, "README must link to SourceCheckup repo run guide")
        if "make sourcecheckup_repo_run_guide" not in readme_text:
            fail(errors, "README must document the SourceCheckup repo run guide command")
        if "docs/REVIEWER_QUESTION_PUBLIC_RELEASE_INDEX_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question public release index")
        if "make reviewer_question_release_index" not in readme_text:
            fail(errors, "README must document the reviewer question public release index command")
        if "docs/REVIEWER_QUESTION_PUBLIC_CONTRIBUTOR_DIGEST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question public contributor digest")
        if "make reviewer_question_contributor_digest" not in readme_text:
            fail(errors, "README must document the reviewer question public contributor digest command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_HANDOFF_NOTES_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer handoff notes")
        if "make reviewer_question_maintainer_handoff" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer handoff command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer closeout digest")
        if "make reviewer_question_maintainer_closeout_digest" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer closeout digest command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_RELEASE_READINESS_DIGEST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer release readiness digest")
        if "make reviewer_question_maintainer_release_readiness_digest" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer release readiness digest command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_EVIDENCE_MAP_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer evidence map")
        if "make reviewer_question_maintainer_evidence_map" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer evidence map command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_AUDIT_TRAIL_PACKET_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer audit trail packet")
        if "make reviewer_question_maintainer_audit_trail_packet" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer audit trail packet command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_RELEASE_CANDIDATE_SUMMARY_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer release candidate summary")
        if "make reviewer_question_maintainer_release_candidate_summary" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer release candidate summary command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_DECISION_LOG_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer public preview decision log")
        if "make reviewer_question_maintainer_public_preview_decision_log" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer public preview decision log command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_HANDOFF_SUMMARY_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer public preview handoff summary")
        if "make reviewer_question_maintainer_public_preview_handoff_summary" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer public preview handoff summary command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_CLOSURE_CHECKLIST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer public preview closure checklist")
        if "make reviewer_question_maintainer_public_preview_closure_checklist" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer public preview closure checklist command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ARCHIVE_DIGEST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer public preview archive digest")
        if "make reviewer_question_maintainer_public_preview_archive_digest" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer public preview archive digest command")
        if "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_INDEX_ROLLUP_V0_1.md" not in readme_text:
            fail(errors, "README must link to the reviewer question maintainer public preview index rollup")
        if "make reviewer_question_maintainer_public_preview_index_rollup" not in readme_text:
            fail(errors, "README must document the reviewer question maintainer public preview index rollup command")
        if "docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit reviewer role table")
        if "make label_audit_role_table" not in readme_text:
            fail(errors, "README must document the label audit reviewer role table command")
        if "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit public contributor issue guide")
        if "make label_audit_public_issue" not in readme_text:
            fail(errors, "README must document the label audit public issue validation command")
        if "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit example intake rows")
        if "make label_audit_examples" not in readme_text:
            fail(errors, "README must document the label audit example intake command")
        if "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit example dashboard")
        if "make label_audit_dashboard" not in readme_text:
            fail(errors, "README must document the label audit example dashboard command")
        if "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit maintainer triage board")
        if "make label_audit_triage" not in readme_text:
            fail(errors, "README must document the label audit maintainer triage command")
        if "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit public wording decision log")
        if "make label_audit_wording_log" not in readme_text:
            fail(errors, "README must document the label audit public wording decision command")
        if "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit release gate checklist")
        if "make label_audit_release_gates" not in readme_text:
            fail(errors, "README must document the label audit release gate checklist command")
        if "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit release gate outcome dashboard")
        if "make label_audit_outcome_dashboard" not in readme_text:
            fail(errors, "README must document the label audit release gate outcome dashboard command")
        if "docs/label_audit/LABEL_AUDIT_RELEASE_NOTE_PACKET_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit release note packet")
        if "make label_audit_release_packet" not in readme_text:
            fail(errors, "README must document the label audit release note packet command")
        if "docs/label_audit/LABEL_AUDIT_PUBLIC_CHANGELOG_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit public changelog")
        if "make label_audit_changelog" not in readme_text:
            fail(errors, "README must document the label audit public changelog command")
        if "docs/label_audit/LABEL_AUDIT_PUBLIC_RELEASE_INDEX_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit public release index")
        if "make label_audit_release_index" not in readme_text:
            fail(errors, "README must document the label audit public release index command")
        if "docs/label_audit/LABEL_AUDIT_PUBLIC_CONTRIBUTOR_DIGEST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit public contributor digest")
        if "make label_audit_contributor_digest" not in readme_text:
            fail(errors, "README must document the label audit public contributor digest command")
        if "docs/label_audit/LABEL_AUDIT_MAINTAINER_HANDOFF_NOTES_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit maintainer handoff notes")
        if "make label_audit_maintainer_handoff" not in readme_text:
            fail(errors, "README must document the label audit maintainer handoff command")
        if "docs/label_audit/LABEL_AUDIT_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit maintainer closeout digest")
        if "make label_audit_maintainer_closeout_digest" not in readme_text:
            fail(errors, "README must document the label audit maintainer closeout digest command")
        if "docs/label_audit/LABEL_AUDIT_MAINTAINER_RELEASE_READINESS_DIGEST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit maintainer release readiness digest")
        if "make label_audit_maintainer_release_readiness_digest" not in readme_text:
            fail(errors, "README must document the label audit maintainer release readiness digest command")
        if "docs/label_audit/LABEL_AUDIT_MAINTAINER_EVIDENCE_MAP_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit maintainer evidence map")
        if "make label_audit_maintainer_evidence_map" not in readme_text:
            fail(errors, "README must document the label audit maintainer evidence map command")
        if "docs/label_audit/LABEL_AUDIT_MAINTAINER_AUDIT_TRAIL_PACKET_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit maintainer audit trail packet")
        if "make label_audit_maintainer_audit_trail_packet" not in readme_text:
            fail(errors, "README must document the label audit maintainer audit trail packet command")
        if "docs/label_audit/LABEL_AUDIT_MAINTAINER_RELEASE_CANDIDATE_SUMMARY_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit maintainer release candidate summary")
        if "make label_audit_maintainer_release_candidate_summary" not in readme_text:
            fail(errors, "README must document the label audit maintainer release candidate summary command")
        if "docs/label_audit/LABEL_AUDIT_MAINTAINER_PUBLIC_PREVIEW_DECISION_LOG_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit maintainer public preview decision log")
        if "make label_audit_maintainer_public_preview_decision_log" not in readme_text:
            fail(errors, "README must document the label audit maintainer public preview decision log command")
        if "docs/label_audit/LABEL_AUDIT_MAINTAINER_PUBLIC_PREVIEW_HANDOFF_SUMMARY_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit maintainer public preview handoff summary")
        if "make label_audit_maintainer_public_preview_handoff_summary" not in readme_text:
            fail(errors, "README must document the label audit maintainer public preview handoff summary command")
        if "docs/label_audit/LABEL_AUDIT_MAINTAINER_PUBLIC_PREVIEW_CLOSURE_CHECKLIST_V0_1.md" not in readme_text:
            fail(errors, "README must link to the label audit maintainer public preview closure checklist")
        if "make label_audit_maintainer_public_preview_closure_checklist" not in readme_text:
            fail(errors, "README must document the label audit maintainer public preview closure checklist command")
        if "docs/tr%2Dmedai%2Dsafety%2Dsuite/BILGE_READINESS_QUEUE_V0_1.md" not in readme_text:
            fail(errors, "README must link to the BİLGE readiness queue")
        if "make bilge_readiness_queue" not in readme_text:
            fail(errors, "README must document the BİLGE readiness queue command")
        if "docs/tr%2Dmedai%2Dsafety%2Dsuite/TUBITAK_1711_COLLABORATION_READINESS_PACKET_V0_1.md" not in readme_text:
            fail(errors, "README must link to the TÜBİTAK 1711 collaboration readiness packet")
        if "make tubitak_1711_readiness_packet" not in readme_text:
            fail(errors, "README must document the TÜBİTAK 1711 readiness packet command")

    prompt_files = [
        root / "data" / "prompt_set_v1.tsv",
        root / "data" / "prompt_set_v2_hard_30.tsv",
        root / "data" / "prompt_set_v3_scale_30.tsv",
    ]
    if all(path.exists() for path in prompt_files):
        prompt_rows = sum(count_tsv_rows(path) for path in prompt_files)
        if prompt_rows != 70:
            fail(errors, f"Public prompt set count must be 70 rows, found {prompt_rows}")
        if readme.exists() and "70 row prompt set" not in readme_text:
            fail(errors, "README must describe the public prompt set count as 70 rows")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a sanitized public release candidate tree.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--strict", action="store_true", help="Require final LICENSE and CITATION.cff.")
    args = parser.parse_args()

    errors, warnings = validate(args.root.resolve(), args.strict)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        sys.exit(1)
    print("PASS public release sanitation")
    print(f"Warnings: {len(warnings)}")


if __name__ == "__main__":
    main()
