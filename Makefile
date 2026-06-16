PYTHON ?= python3

.PHONY: validate validate-public sourcecheckup sourcecheckup_v02 sourcecheckup_contrib_v02 source_claim_queue health_data_quality_card leaderboard leaderboard_report case_intake taxonomy_dashboard tr_medllm_pack clinician_review_queue clinician_review_protocol release_note

validate:
	$(PYTHON) scripts/validate_external_sample_jsonl.py data/failure_atlas_external_sample_v0_1.jsonl
	$(PYTHON) scripts/validate_medhelm_metric_json.py data/medhelm_remote_rescue_metric_v0_1.json
	$(PYTHON) scripts/validate_scoring_rubric_v0_1.py
	$(PYTHON) scripts/validate_failure_atlas_public_summary_v0_1.py
	$(PYTHON) scripts/validate_clinician_review_protocol_v0_1.py
	$(PYTHON) scripts/validate_source_claim_review_queue_v0_1.py
	$(PYTHON) scripts/validate_health_data_quality_card_v0_1.py
	$(PYTHON) scripts/validate_public_release_note_v0_1.py
	$(PYTHON) scripts/validate_public_release.py --root .

validate-public: validate

sourcecheckup:
	$(PYTHON) scripts/sourcecheckup_medical.py self-test
	$(PYTHON) scripts/sourcecheckup_medical.py validate --input sourcecheckup/examples/sourcecheckup_seed_answers.jsonl --out-json sourcecheckup/build/sourcecheckup_seed_report.json --out-md sourcecheckup/build/sourcecheckup_seed_report.md

sourcecheckup_v02:
	$(PYTHON) scripts/sourcecheckup_medical.py validate --input sourcecheckup/examples/source_surface_examples_v0_2.jsonl --out-json sourcecheckup/build/source_surface_examples_v0_2_report.json --out-md sourcecheckup/build/source_surface_examples_v0_2_report.md

sourcecheckup_contrib_v02:
	$(PYTHON) scripts/validate_sourcecheckup_contribution_v0_2.py

source_claim_queue:
	$(PYTHON) scripts/validate_source_claim_review_queue_v0_1.py

health_data_quality_card:
	$(PYTHON) scripts/validate_health_data_quality_card_v0_1.py

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

clinician_review_queue:
	$(PYTHON) scripts/validate_failure_atlas_case_intake_v0_1.py
	$(PYTHON) scripts/generate_clinician_review_queue_v0_1.py

clinician_review_protocol:
	$(PYTHON) scripts/validate_clinician_review_protocol_v0_1.py

release_note:
	$(PYTHON) scripts/validate_public_release_note_v0_1.py
