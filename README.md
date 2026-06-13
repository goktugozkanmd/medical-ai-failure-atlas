# Clinician led medical AI safety evaluation

Status: public v0.1 release.

Date: 2026 06 13

## Purpose

This project builds physician authored synthetic draft evaluation resources for medical AI systems across medicine, pending final clinician review.

The goal is to help model builders, clinical AI teams, and academic collaborators inspect whether model answers are safe, calibrated, evidence aware, and useful before clinical use.

## Current contents

1. A 150 scenario synthetic medicine wide case bank.
2. A 70 row prompt set across pilot, hard thirty, and V3 scale prompts.
3. A V0.2 taxonomy that defines the route toward a larger draft benchmark structure.
4. A physician authored scoring rubric.
5. Two completed internal model run layers across three models.
6. 180 captured raw outputs kept internal.
7. Preliminary strict triage tables.
8. Three draft Failure Atlas entries.
9. MedHELM oriented metric draft.
10. Medmarks style local proof pack.
11. Scripts for validation, model capture, scoring dry run, benchmark report generation, and public candidate sanitation.

## What this is

1. A clinician led evaluation and feedback resource.
2. A starting point for medical AI safety evaluation work.
3. A structure for open source model feedback.
4. A collaboration seed for labs that work on medical language models.

## What this is not

1. It is not clinical advice.
2. It is not patient data.
3. It is not a claim that any model is safe for clinical use.
4. It is not a final external validation study.

## License and citation

Code is licensed under the Apache License, Version 2.0.

Synthetic scenario data, documentation, evaluation cards, and other non code text are licensed under Creative Commons Attribution 4.0 International unless otherwise noted.

Raw model outputs and logs are not included in the public v0.1 release.

Citation metadata is provided in `CITATION.cff`.

## Quick start

Run the public validation check:

```bash
make validate
```

## Folder structure

```text
data/
  scenario_taxonomy_v0_2.tsv
  scenario_bank_v1.tsv
  scenario_bank_v2_hard_addendum.tsv
  scenario_bank_v3_scale_seed.tsv
  prompt_set_v2_hard_30.tsv
  prompt_set_v3_scale_30.tsv
  failure_atlas_external_sample_v0_1.jsonl
  medhelm_remote_rescue_metric_v0_1.json
  scoring_rubric_v0_1.json
docs/
  clinician_evaluation_rubric.md
  failure_atlas_entry_001_insulin_sick_day_wording_draft.md
  failure_atlas_entry_002_protocol_overprecision_draft.md
  failure_atlas_entry_003_remote_rescue_protocols_draft.md
  MEDHELM_CROSSWALK_DRAFT.md
  MEDHELM_REMOTE_RESCUE_BOUNDARY_METRIC_PACKAGE_DRAFT.md
  MEDMARKS_COMPATIBILITY_DRAFT.md
  scoring_model_v0_1.md
medmarks_candidate_env_v0_20260613/
  configs/
  environments/
  VALIDATION_REPORT.md
scripts/
  benchmark_runner.py
  validate_external_sample_jsonl.py
  validate_medhelm_metric_json.py
  validate_model_run_json.py
  validate_public_release.py
  validate_scoring_rubric_v0_1.py
  run_prompt_set_openai_compatible_v2.py
  run_prompt_set_hf_transformers_v2.py
CONTRIBUTING.md
```

## Current signal

The first ten prompts were run on three models. The early signal is not mainly missed diagnosis. The more useful signal is calibration: protocol over detail, broad antibiotic alternatives, uneven evidence verification, incomplete uncertainty handling, and medication wording risk.

The hard addendum and V3 scale seed have completed internal model run layers. The public release contains the scenario banks, rubric, external sample, and draft atlas entries, but not raw model outputs.

Hard thirty run:

The hard thirty prompt set was run on three models and produced 90 raw outputs. Local JSON validation passed for all three model files. Strict preliminary triage found 2 high priority rows and 30 medium priority rows. The strongest immediate Failure Atlas candidate is insulin sick day wording risk in scenario `H008`.

Failure atlas draft:

The first draft atlas entry is `docs/failure_atlas_entry_001_insulin_sick_day_wording_draft.md`. It is not confirmed and should not be used publicly until clinician review.

The second draft atlas entry is `docs/failure_atlas_entry_002_protocol_overprecision_draft.md`. It summarizes the repeated medium priority pattern where models recognize emergencies but over specify protocol details without enough patient or institutional context.

The third draft atlas entry is `docs/failure_atlas_entry_003_remote_rescue_protocols_draft.md`. It summarizes V3 high priority signals where models generated overly specific remote rescue, reversal, insulin, or pregnancy emergency protocol language.

The first external ecosystem sample is in `data/failure_atlas_external_sample_v0_1.jsonl`. It contains three synthetic cases mapped toward MedHELM and Medmarks discussion routes.

The first MedHELM oriented metric draft is in `data/medhelm_remote_rescue_metric_v0_1.json` and `docs/MEDHELM_REMOTE_RESCUE_BOUNDARY_METRIC_PACKAGE_DRAFT.md`.

The first Medmarks style local proof pack is in `medmarks_candidate_env_v0_20260613/`.

Benchmark runner:

`scripts/benchmark_runner.py`

The runner validates prompt rows, synthetic scenario banks, raw model captures, the internal scoring rubric, and strict triage files. It writes preliminary review artifacts under `benchmark_report/`, including per row scores, model summary, gate summary, clinician review queue, Failure Atlas candidate JSONL, and a run report. These are preliminary triage signals only, not final clinical performance scores.

Public release boundaries are tracked in `PUBLIC_RELEASE_BOUNDARY_V0_1.md` and `RELEASE_MANIFEST_V0_1_DRAFT.md`.

Dataset and evaluation card draft:

`DATASET_EVALUATION_CARD_V0_1_DRAFT.md`

This remains preliminary until clinician review confirms the scoring and public wording.

## Next release gate

1. Review the 6 high priority rows.
2. Review repeated medium priority clusters for Failure Atlas patterns.
3. Add model output excerpts only if copyright and platform terms allow.
4. Prepare separately audited MedHELM and Medmarks discussion posts.
5. Prepare the resource preprint only after clinician review status is stronger.
