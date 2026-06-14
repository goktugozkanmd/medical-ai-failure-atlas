PYTHON ?= python3

.PHONY: validate validate-public

validate:
	$(PYTHON) scripts/validate_external_sample_jsonl.py data/failure_atlas_external_sample_v0_1.jsonl
	$(PYTHON) scripts/validate_medhelm_metric_json.py data/medhelm_remote_rescue_metric_v0_1.json
	$(PYTHON) scripts/validate_scoring_rubric_v0_1.py
	$(PYTHON) scripts/validate_failure_atlas_public_summary_v0_1.py
	$(PYTHON) scripts/validate_public_release.py --root .

validate-public: validate
