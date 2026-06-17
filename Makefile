PYTHON ?= python3

.PHONY: validate validate-public platform_dashboard sourcecheckup sourcecheckup_v02 sourcecheckup_contrib_v02 sourcecheckup_public_issue sourcecheckup_repo_run_guide healthbench_medhelm_mapping benchmark_reviewer_questions reviewer_question_issue_templates reviewer_question_intake_examples reviewer_question_intake_triage reviewer_question_wording_log reviewer_question_release_gates reviewer_question_gate_outcomes reviewer_question_release_packet reviewer_question_changelog reviewer_question_release_index label_audit_public_issue label_audit_examples label_audit_dashboard label_audit_triage label_audit_wording_log label_audit_release_gates label_audit_outcome_dashboard label_audit_release_packet label_audit_changelog label_audit_release_index label_audit_contributor_digest label_audit_maintainer_handoff label_audit_maintainer_closeout_digest label_audit_maintainer_release_readiness_digest label_audit_maintainer_evidence_map label_audit_maintainer_audit_trail_packet label_audit_maintainer_release_candidate_summary label_audit_maintainer_public_preview_decision_log label_audit_maintainer_public_preview_handoff_summary label_audit_maintainer_public_preview_closure_checklist sourcecheckup_expansion_dashboard sourcecheckup_tr_medllm_routing sourcecheckup_turkish_institutional_wording source_review_worksheets red_flag_warning_checklist red_flag_contributor_examples warning_sign_role_table label_audit_role_table bilge_readiness_queue tubitak_1711_readiness_packet source_claim_queue health_data_quality_card boundary_notes assurance_card_template assurance_release_gate_map clinician_literacy_map tr_medllm_specialty_spread tr_medllm_specialty_dashboard leaderboard leaderboard_report case_intake taxonomy_dashboard tr_medllm_pack clinician_review_queue clinician_review_protocol release_note

validate:
	$(PYTHON) scripts/validate_external_sample_jsonl.py data/failure_atlas_external_sample_v0_1.jsonl
	$(PYTHON) scripts/validate_medhelm_metric_json.py data/medhelm_remote_rescue_metric_v0_1.json
	$(PYTHON) scripts/validate_scoring_rubric_v0_1.py
	$(PYTHON) scripts/validate_failure_atlas_public_summary_v0_1.py
	$(PYTHON) scripts/validate_clinician_review_protocol_v0_1.py
	$(PYTHON) scripts/validate_source_claim_review_queue_v0_1.py
	$(PYTHON) scripts/validate_sourcecheckup_public_contributor_issue_v0_1.py
	$(PYTHON) scripts/validate_label_audit_public_contributor_issue_v0_1.py
	$(PYTHON) scripts/validate_label_audit_example_intake_v0_1.py
	$(PYTHON) scripts/validate_label_audit_example_dashboard_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_triage_board_v0_1.py
	$(PYTHON) scripts/validate_label_audit_public_wording_decision_log_v0_1.py
	$(PYTHON) scripts/validate_label_audit_release_gate_checklist_v0_1.py
	$(PYTHON) scripts/validate_label_audit_release_gate_outcome_dashboard_v0_1.py
	$(PYTHON) scripts/validate_label_audit_release_note_packet_v0_1.py
	$(PYTHON) scripts/validate_label_audit_public_changelog_v0_1.py
	$(PYTHON) scripts/validate_label_audit_public_release_index_v0_1.py
	$(PYTHON) scripts/validate_label_audit_public_contributor_digest_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_handoff_notes_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_closeout_digest_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_release_readiness_digest_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_evidence_map_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_audit_trail_packet_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_release_candidate_summary_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_public_preview_decision_log_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_public_preview_handoff_summary_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_public_preview_closure_checklist_v0_1.py
	$(PYTHON) scripts/validate_bilge_readiness_queue_v0_1.py
	$(PYTHON) scripts/validate_tubitak_1711_collaboration_readiness_packet_v0_1.py
	$(PYTHON) scripts/validate_sourcecheckup_contribution_v0_2.py
	$(PYTHON) scripts/validate_red_flag_contributor_examples_v0_1.py
	$(PYTHON) scripts/validate_sourcecheckup_turkish_institutional_wording_examples_v0_1.py
	$(PYTHON) scripts/validate_sourcecheckup_repo_run_guide_v0_1.py
	$(PYTHON) scripts/validate_healthbench_medhelm_mapping_note_v0_1.py
	$(PYTHON) scripts/validate_benchmark_style_reviewer_questions_v0_1.py
	$(PYTHON) scripts/validate_benchmark_reviewer_question_issue_templates_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_intake_examples_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_intake_triage_board_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_public_wording_decision_log_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_release_gate_checklist_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_release_gate_outcome_dashboard_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_public_release_packet_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_public_changelog_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_public_release_index_v0_1.py
	$(PYTHON) scripts/validate_sourcecheckup_example_expansion_dashboard_v0_2.py
	$(PYTHON) scripts/validate_health_data_quality_card_v0_1.py
	$(PYTHON) scripts/validate_boundary_notes_v0_1.py
	$(PYTHON) scripts/validate_assurance_card_template_v0_1.py
	$(PYTHON) scripts/validate_assurance_release_gate_example_map_v0_1.py
	$(PYTHON) scripts/validate_clinician_literacy_release_gate_lesson_map_v0_1.py
	$(PYTHON) scripts/validate_sourcecheckup_tr_medllm_assurance_routing_map_v0_1.py
	$(PYTHON) scripts/validate_source_review_worksheets_v0_1.py
	$(PYTHON) scripts/validate_red_flag_warning_checklist_v0_1.py
	$(PYTHON) scripts/validate_tr_medllm_specialty_spread_v0_1.py
	$(PYTHON) scripts/validate_warning_sign_reviewer_role_table_v0_1.py
	$(PYTHON) scripts/validate_label_audit_reviewer_role_table_v0_1.py
	$(PYTHON) scripts/validate_tr_medllm_specialty_dashboard_v0_1.py
	$(PYTHON) scripts/validate_platform_dashboard_index_v0_1.py
	$(PYTHON) scripts/validate_public_release_note_v0_1.py
	$(PYTHON) scripts/validate_public_release.py --root .

validate-public: validate

platform_dashboard:
	$(PYTHON) scripts/validate_platform_dashboard_index_v0_1.py

sourcecheckup:
	$(PYTHON) scripts/sourcecheckup_medical.py self-test
	$(PYTHON) scripts/sourcecheckup_medical.py validate --input sourcecheckup/examples/sourcecheckup_seed_answers.jsonl --out-json sourcecheckup/build/sourcecheckup_seed_report.json --out-md sourcecheckup/build/sourcecheckup_seed_report.md

sourcecheckup_v02:
	$(PYTHON) scripts/sourcecheckup_medical.py validate --input sourcecheckup/examples/source_surface_examples_v0_2.jsonl --out-json sourcecheckup/build/source_surface_examples_v0_2_report.json --out-md sourcecheckup/build/source_surface_examples_v0_2_report.md

sourcecheckup_contrib_v02:
	$(PYTHON) scripts/validate_sourcecheckup_contribution_v0_2.py
	$(PYTHON) scripts/generate_red_flag_contributor_examples_v0_1.py
	$(PYTHON) scripts/validate_red_flag_contributor_examples_v0_1.py

sourcecheckup_public_issue:
	$(PYTHON) scripts/validate_sourcecheckup_public_contributor_issue_v0_1.py

sourcecheckup_repo_run_guide:
	$(PYTHON) scripts/sourcecheckup_repo_doctor_v0_1.py
	$(PYTHON) scripts/generate_sourcecheckup_repo_run_guide_v0_1.py
	$(PYTHON) scripts/validate_sourcecheckup_repo_run_guide_v0_1.py

healthbench_medhelm_mapping:
	$(PYTHON) scripts/generate_healthbench_medhelm_mapping_note_v0_1.py
	$(PYTHON) scripts/validate_healthbench_medhelm_mapping_note_v0_1.py

benchmark_reviewer_questions:
	$(PYTHON) scripts/generate_benchmark_style_reviewer_questions_v0_1.py
	$(PYTHON) scripts/validate_benchmark_style_reviewer_questions_v0_1.py

reviewer_question_issue_templates:
	$(PYTHON) scripts/validate_benchmark_reviewer_question_issue_templates_v0_1.py

reviewer_question_intake_examples:
	$(PYTHON) scripts/generate_reviewer_question_intake_examples_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_intake_examples_v0_1.py

reviewer_question_intake_triage:
	$(PYTHON) scripts/generate_reviewer_question_intake_triage_board_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_intake_triage_board_v0_1.py

reviewer_question_wording_log:
	$(PYTHON) scripts/generate_reviewer_question_public_wording_decision_log_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_public_wording_decision_log_v0_1.py

reviewer_question_release_gates:
	$(PYTHON) scripts/generate_reviewer_question_release_gate_checklist_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_release_gate_checklist_v0_1.py

reviewer_question_gate_outcomes:
	$(PYTHON) scripts/generate_reviewer_question_release_gate_outcome_dashboard_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_release_gate_outcome_dashboard_v0_1.py

reviewer_question_release_packet:
	$(PYTHON) scripts/generate_reviewer_question_public_release_packet_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_public_release_packet_v0_1.py

reviewer_question_changelog:
	$(PYTHON) scripts/generate_reviewer_question_public_changelog_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_public_changelog_v0_1.py

reviewer_question_release_index:
	$(PYTHON) scripts/generate_reviewer_question_public_release_index_v0_1.py
	$(PYTHON) scripts/validate_reviewer_question_public_release_index_v0_1.py

label_audit_public_issue:
	$(PYTHON) scripts/validate_label_audit_public_contributor_issue_v0_1.py

label_audit_examples:
	$(PYTHON) scripts/generate_label_audit_example_intake_v0_1.py
	$(PYTHON) scripts/validate_label_audit_example_intake_v0_1.py

label_audit_dashboard:
	$(PYTHON) scripts/generate_label_audit_example_dashboard_v0_1.py
	$(PYTHON) scripts/validate_label_audit_example_dashboard_v0_1.py

label_audit_triage:
	$(PYTHON) scripts/generate_label_audit_maintainer_triage_board_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_triage_board_v0_1.py

label_audit_wording_log:
	$(PYTHON) scripts/generate_label_audit_public_wording_decision_log_v0_1.py
	$(PYTHON) scripts/validate_label_audit_public_wording_decision_log_v0_1.py

label_audit_release_gates:
	$(PYTHON) scripts/generate_label_audit_release_gate_checklist_v0_1.py
	$(PYTHON) scripts/validate_label_audit_release_gate_checklist_v0_1.py

label_audit_outcome_dashboard:
	$(PYTHON) scripts/generate_label_audit_release_gate_outcome_dashboard_v0_1.py
	$(PYTHON) scripts/validate_label_audit_release_gate_outcome_dashboard_v0_1.py

label_audit_release_packet:
	$(PYTHON) scripts/generate_label_audit_release_note_packet_v0_1.py
	$(PYTHON) scripts/validate_label_audit_release_note_packet_v0_1.py

label_audit_changelog:
	$(PYTHON) scripts/generate_label_audit_public_changelog_v0_1.py
	$(PYTHON) scripts/validate_label_audit_public_changelog_v0_1.py

label_audit_release_index:
	$(PYTHON) scripts/generate_label_audit_public_release_index_v0_1.py
	$(PYTHON) scripts/validate_label_audit_public_release_index_v0_1.py

label_audit_contributor_digest:
	$(PYTHON) scripts/generate_label_audit_public_contributor_digest_v0_1.py
	$(PYTHON) scripts/validate_label_audit_public_contributor_digest_v0_1.py

label_audit_maintainer_handoff:
	$(PYTHON) scripts/generate_label_audit_maintainer_handoff_notes_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_handoff_notes_v0_1.py

label_audit_maintainer_closeout_digest:
	$(PYTHON) scripts/generate_label_audit_maintainer_closeout_digest_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_closeout_digest_v0_1.py

label_audit_maintainer_release_readiness_digest:
	$(PYTHON) scripts/generate_label_audit_maintainer_release_readiness_digest_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_release_readiness_digest_v0_1.py

label_audit_maintainer_evidence_map:
	$(PYTHON) scripts/generate_label_audit_maintainer_evidence_map_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_evidence_map_v0_1.py

label_audit_maintainer_audit_trail_packet:
	$(PYTHON) scripts/generate_label_audit_maintainer_audit_trail_packet_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_audit_trail_packet_v0_1.py

label_audit_maintainer_release_candidate_summary:
	$(PYTHON) scripts/generate_label_audit_maintainer_release_candidate_summary_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_release_candidate_summary_v0_1.py

label_audit_maintainer_public_preview_decision_log:
	$(PYTHON) scripts/generate_label_audit_maintainer_public_preview_decision_log_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_public_preview_decision_log_v0_1.py

label_audit_maintainer_public_preview_handoff_summary:
	$(PYTHON) scripts/generate_label_audit_maintainer_public_preview_handoff_summary_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_public_preview_handoff_summary_v0_1.py

label_audit_maintainer_public_preview_closure_checklist:
	$(PYTHON) scripts/generate_label_audit_maintainer_public_preview_closure_checklist_v0_1.py
	$(PYTHON) scripts/validate_label_audit_maintainer_public_preview_closure_checklist_v0_1.py

bilge_readiness_queue:
	$(PYTHON) scripts/generate_bilge_readiness_queue_v0_1.py
	$(PYTHON) scripts/validate_bilge_readiness_queue_v0_1.py

tubitak_1711_readiness_packet:
	$(PYTHON) scripts/generate_tubitak_1711_collaboration_readiness_packet_v0_1.py
	$(PYTHON) scripts/validate_tubitak_1711_collaboration_readiness_packet_v0_1.py

sourcecheckup_expansion_dashboard:
	$(PYTHON) scripts/sourcecheckup_medical.py validate --input sourcecheckup/examples/source_surface_examples_v0_2.jsonl --out-json sourcecheckup/build/source_surface_examples_v0_2_report.json --out-md sourcecheckup/build/source_surface_examples_v0_2_report.md
	$(PYTHON) scripts/validate_sourcecheckup_contribution_v0_2.py
	$(PYTHON) scripts/generate_red_flag_contributor_examples_v0_1.py
	$(PYTHON) scripts/validate_red_flag_contributor_examples_v0_1.py
	$(PYTHON) scripts/validate_source_claim_review_queue_v0_1.py
	$(PYTHON) scripts/generate_sourcecheckup_example_expansion_dashboard_v0_2.py
	$(PYTHON) scripts/validate_sourcecheckup_example_expansion_dashboard_v0_2.py

sourcecheckup_tr_medllm_routing:
	$(PYTHON) scripts/generate_sourcecheckup_tr_medllm_assurance_routing_map_v0_1.py
	$(PYTHON) scripts/validate_sourcecheckup_tr_medllm_assurance_routing_map_v0_1.py

source_review_worksheets:
	$(PYTHON) scripts/generate_source_review_worksheets_v0_1.py
	$(PYTHON) scripts/validate_source_review_worksheets_v0_1.py

red_flag_warning_checklist:
	$(PYTHON) scripts/generate_red_flag_warning_checklist_v0_1.py
	$(PYTHON) scripts/validate_red_flag_warning_checklist_v0_1.py

red_flag_contributor_examples:
	$(PYTHON) scripts/validate_sourcecheckup_contribution_v0_2.py
	$(PYTHON) scripts/generate_red_flag_contributor_examples_v0_1.py
	$(PYTHON) scripts/validate_red_flag_contributor_examples_v0_1.py

sourcecheckup_turkish_institutional_wording:
	$(PYTHON) scripts/generate_sourcecheckup_turkish_institutional_wording_examples_v0_1.py
	$(PYTHON) scripts/validate_sourcecheckup_turkish_institutional_wording_examples_v0_1.py

warning_sign_role_table:
	$(PYTHON) scripts/generate_warning_sign_reviewer_role_table_v0_1.py
	$(PYTHON) scripts/validate_warning_sign_reviewer_role_table_v0_1.py

label_audit_role_table:
	$(PYTHON) scripts/generate_label_audit_reviewer_role_table_v0_1.py
	$(PYTHON) scripts/validate_label_audit_reviewer_role_table_v0_1.py

source_claim_queue:
	$(PYTHON) scripts/validate_source_claim_review_queue_v0_1.py

health_data_quality_card:
	$(PYTHON) scripts/validate_health_data_quality_card_v0_1.py

boundary_notes:
	$(PYTHON) scripts/validate_boundary_notes_v0_1.py

assurance_card_template:
	$(PYTHON) scripts/validate_assurance_card_template_v0_1.py

assurance_release_gate_map:
	$(PYTHON) scripts/generate_assurance_release_gate_example_map_v0_1.py
	$(PYTHON) scripts/validate_assurance_release_gate_example_map_v0_1.py

clinician_literacy_map:
	$(PYTHON) scripts/generate_clinician_literacy_release_gate_lesson_map_v0_1.py
	$(PYTHON) scripts/validate_clinician_literacy_release_gate_lesson_map_v0_1.py

leaderboard:
	$(PYTHON) scripts/validate_leaderboard_template_v0_1.py

leaderboard_report:
	$(PYTHON) scripts/validate_leaderboard_template_v0_1.py
	$(PYTHON) scripts/generate_leaderboard_report_v0_1.py

case_intake:
	$(PYTHON) scripts/validate_failure_atlas_case_intake_v0_1.py
	$(PYTHON) scripts/generate_failure_atlas_case_intake_report_v0_1.py

taxonomy_dashboard:
	$(PYTHON) scripts/validate_failure_atlas_case_intake_v0_1.py
	$(PYTHON) scripts/generate_failure_atlas_taxonomy_dashboard_v0_1.py

tr_medllm_pack:
	$(PYTHON) scripts/validate_failure_atlas_case_intake_v0_1.py --input tr_medllm_safetybench/synthetic_risk_pack_v0_1.jsonl
	$(PYTHON) scripts/validate_tr_medllm_specialty_spread_v0_1.py

tr_medllm_specialty_spread:
	$(PYTHON) scripts/validate_tr_medllm_specialty_spread_v0_1.py
	$(PYTHON) scripts/generate_tr_medllm_specialty_spread_dashboard_v0_1.py
	$(PYTHON) scripts/validate_tr_medllm_specialty_dashboard_v0_1.py

tr_medllm_specialty_dashboard:
	$(PYTHON) scripts/generate_tr_medllm_specialty_spread_dashboard_v0_1.py
	$(PYTHON) scripts/validate_tr_medllm_specialty_dashboard_v0_1.py

clinician_review_queue:
	$(PYTHON) scripts/validate_failure_atlas_case_intake_v0_1.py
	$(PYTHON) scripts/generate_clinician_review_queue_v0_1.py

clinician_review_protocol:
	$(PYTHON) scripts/validate_clinician_review_protocol_v0_1.py

release_note:
	$(PYTHON) scripts/validate_public_release_note_v0_1.py
