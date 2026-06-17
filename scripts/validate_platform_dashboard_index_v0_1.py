#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "docs" / "PLATFORM_DASHBOARD_INDEX_V0_1.md"

REQUIRED_PHRASES = [
    "Public platform dashboard index v0.1",
    "TR MedLLM SafetyBench",
    "Top public entry files",
    "Medical AI Failure Atlas Global",
    "Turkish Clinical AI Assurance Lab",
    "SourceCheckup Medical",
    "Clinician AI Literacy Academy Turkiye",
    "Health Data Quality and Label Audit Commons",
    "19 synthetic intake rows",
    "14 Turkish synthetic risk rows",
    "10 risk axes",
    "10 of 10 Failure Atlas taxonomy pattern IDs represented",
    "19 clinician review queue rows",
    "12 source claim review queue rows",
    "11 SourceCheckup contributor examples",
    "24 pilot inter rater rows",
    "150 synthetic scenario rows",
    "70 prompt rows",
    "6 clinician literacy release gate lessons",
    "6 assurance release gate examples",
    "7 SourceCheckup TR MedLLM assurance routes",
    "2 source review worksheets",
    "3 red flag warning checklists",
    "4 warning sign reviewer roles",
    "5 escalation gate audit rows",
    "4 label audit reviewer roles",
    "5 label audit escalation gate rows",
    "1 label audit public contributor issue route",
    "5 label audit example intake rows",
    "5 label audit example dashboard rows",
    "5 label audit maintainer triage rows",
    "5 label audit public wording decision rows",
    "5 label audit release gate rows",
    "5 label audit release gate outcome rows",
    "7 label audit release note packet rows",
    "8 label audit public changelog rows",
    "9 label audit public release index surface rows",
    "10 label audit issue history rows",
    "5 label audit public contributor digest rows",
    "5 label audit maintainer handoff rows",
    "5 label audit maintainer closeout digest rows",
    "5 label audit maintainer release readiness digest rows",
    "5 label audit maintainer evidence map rows",
    "5 label audit maintainer audit trail packet rows",
    "5 label audit maintainer release candidate summary rows",
    "5 label audit maintainer public preview decision rows",
    "5 label audit maintainer public preview handoff rows",
    "5 label audit maintainer public preview closure rows",
    "3 red flag source locator contributor examples",
    "5 BİLGE readiness queue rows",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model safety proof",
    "not a model ranking",
    "not a regulatory claim",
    "not a benchmark compatibility claim",
    "not an official endorsement",
    "make tr_medllm_pack",
    "make tr_medllm_specialty_dashboard",
    "make taxonomy_dashboard",
    "make leaderboard_report",
    "make assurance_card_template",
    "make assurance_release_gate_map",
    "make sourcecheckup_tr_medllm_routing",
    "make source_review_worksheets",
    "make red_flag_warning_checklist",
    "make warning_sign_role_table",
    "make red_flag_contributor_examples",
    "make sourcecheckup_public_issue",
    "make sourcecheckup_expansion_dashboard",
    "make clinician_literacy_map",
    "make clinician_review_protocol",
    "make health_data_quality_card",
    "make label_audit_role_table",
    "make label_audit_public_issue",
    "make label_audit_examples",
    "make label_audit_dashboard",
    "make label_audit_triage",
    "make label_audit_wording_log",
    "make label_audit_release_gates",
    "make label_audit_outcome_dashboard",
    "make label_audit_release_packet",
    "make label_audit_changelog",
    "make label_audit_release_index",
    "make label_audit_contributor_digest",
    "make label_audit_maintainer_handoff",
    "make label_audit_maintainer_closeout_digest",
    "make label_audit_maintainer_release_readiness_digest",
    "make label_audit_maintainer_evidence_map",
    "make label_audit_maintainer_audit_trail_packet",
    "make label_audit_maintainer_release_candidate_summary",
    "make label_audit_maintainer_public_preview_decision_log",
    "make label_audit_maintainer_public_preview_handoff_summary",
    "make label_audit_maintainer_public_preview_closure_checklist",
    "make bilge_readiness_queue",
    "BİLGE readiness queue",
    "no access claim",
    "no score claim",
    "no endorsement claim",
    "1711 collaboration readiness packet",
]

REQUIRED_LINK_TARGETS = [
    "README.md",
    "docs/tr-medai-safety-suite/PUBLIC_PREVIEW_INDEX_20260616.md",
    "docs/tr-medai-safety-suite/PUBLIC_REPO_RELEASE_CARD_20260616.md",
    "docs/tr-medai-safety-suite/BILGE_READINESS_QUEUE_V0_1.md",
    "docs/tr-medai-safety-suite/bilge_readiness_queue_v0_1.json",
    "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
    "docs/ROADMAP_2026_06.md",
    "tr_medllm_safetybench/README.md",
    "tr_medllm_safetybench/synthetic_risk_pack_v0_1.jsonl",
    "tr_medllm_safetybench/build/specialty_spread_dashboard_v0_1.md",
    "failure_atlas/public/INDEX.md",
    "failure_atlas/public/METHODOLOGY.md",
    "failure_atlas/public/build/case_intake_report_v0_1.md",
    "failure_atlas/public/build/taxonomy_dashboard_v0_1.md",
    "failure_atlas/public/build/clinician_review_queue_v0_1.md",
    "leaderboard/build/synthetic_report_v0_1.md",
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
    "docs/tr-medai-safety-suite/ASSURANCE_LAB_TPLC_GOVERNANCE_MATRIX_20260616.md",
    "sourcecheckup/README.md",
    "sourcecheckup/WORKFLOW_EXAMPLE_20260616.md",
    "docs/sourcecheckup/SOURCE_CLAIM_REVIEW_QUEUE_V0_1.md",
    "docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md",
    "docs/sourcecheckup/RED_FLAG_SOURCE_LOCATOR_CONTRIBUTOR_EXAMPLES_V0_1.md",
    "sourcecheckup/build/sourcecheckup_seed_report.md",
    "sourcecheckup/build/source_surface_examples_v0_2_report.md",
    "sourcecheckup/build/source_claim_example_expansion_v0_2.md",
    "docs/tr-medai-safety-suite/CLINICIAN_AI_LITERACY_30MIN_TR_20260616.md",
    "docs/CLINICIAN_REVIEW_PROTOCOL_V0_1.md",
    "failure_atlas/public/clinician_review_states_v0_1.json",
    "docs/CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md",
    "docs/clinician_literacy_release_gate_lesson_map_v0_1.json",
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
    ".github/ISSUE_TEMPLATE/label_audit_review.yml",
    "DATASET_EVALUATION_CARD_V0_1_DRAFT.md",
    "DATA_DICTIONARY.md",
    "data/inter_rater_review_subset_v0_1.tsv",
    "LABELING.md",
    "docs/LABEL_DEFINITION_LOCK_V0_1.md",
    "docs/LABELING_PACKAGE_INDEX_V0_1.md",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "officially endorsed",
    "regulatory approved",
    "sandbox access granted",
    "patient data used",
    "model is safe",
    "best model",
]


def dashboard_mentions(text: str, relative_path: str) -> bool:
    root_relative = relative_path
    dashboard_relative = str(Path(relative_path).relative_to("docs")) if relative_path.startswith("docs/") else "../" + relative_path
    candidates = {
        root_relative,
        root_relative.replace("-", "%2D"),
        dashboard_relative,
        dashboard_relative.replace("-", "%2D"),
    }
    return any(token in text for token in candidates)


def main() -> int:
    errors: list[str] = []
    if not DASHBOARD.exists():
        errors.append(f"Missing dashboard: {DASHBOARD.relative_to(ROOT)}")
        text = ""
    else:
        text = DASHBOARD.read_text(encoding="utf-8")

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")

    for relative_path in REQUIRED_LINK_TARGETS:
        if not (ROOT / relative_path).exists():
            errors.append(f"Missing linked public file: {relative_path}")
        if not dashboard_mentions(text, relative_path):
            errors.append(f"Dashboard does not mention required target: {relative_path}")

    for link in text.split("](")[1:]:
        target = link.split(")", 1)[0]
        if target.startswith("http"):
            continue
        normalized = unquote(target)
        candidate = (DASHBOARD.parent / normalized).resolve()
        try:
            candidate.relative_to(ROOT)
        except ValueError:
            errors.append(f"Link escapes repo root: {target}")
            continue
        if not candidate.exists():
            errors.append(f"Linked file does not exist: {target}")

    if errors:
        print("FAIL platform dashboard index validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS platform dashboard index validation")
    print(f"dashboard={DASHBOARD.relative_to(ROOT)}")
    print("platforms=6")
    return 0


if __name__ == "__main__":
    sys.exit(main())
