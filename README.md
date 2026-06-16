# Clinician led medical AI safety evaluation

Status: public v0.1 release.

Date: 2026 06 13

## 2026 06 16 public preview update

New visible build surfaces are now staged in this public repository:

1. [TR MedAI Safety Suite public release card](docs/tr-medai-safety-suite/PUBLIC_REPO_RELEASE_CARD_20260616.md)
2. [SourceCheckup Medical public demo matrix](docs/sourcecheckup/PUBLIC_DEMO_MATRIX_20260616.md)
3. [Turkish Clinical AI Assurance Lab governance matrix](docs/tr-medai-safety-suite/ASSURANCE_LAB_TPLC_GOVERNANCE_MATRIX_20260616.md)
4. [Clinician AI Literacy 30 minute Turkish facilitator packet](docs/tr-medai-safety-suite/CLINICIAN_AI_LITERACY_30MIN_TR_20260616.md)
5. [Runnable SourceCheckup Medical tool](sourcecheckup/README.md)
6. [Failure Atlas taxonomy public preview](failure_atlas/public/TAXONOMY_PREVIEW_20260616.md)
7. [SourceCheckup workflow example](sourcecheckup/WORKFLOW_EXAMPLE_20260616.md)
8. [June 2026 public roadmap](docs/ROADMAP_2026_06.md)
9. [No ranking leaderboard design](docs/LEADERBOARD_DESIGN_V0_1.md)
10. [Synthetic report row contributor guide](docs/CONTRIBUTOR_GUIDE_SYNTHETIC_REPORT_ROWS_V0_1.md)
11. [Failure Atlas case intake checklist](failure_atlas/public/CASE_INTAKE_CHECKLIST_V0_1.md)
12. [SourceCheckup contributor checklist v0.2](docs/sourcecheckup/CONTRIBUTOR_CHECKLIST_V0_2.md)

These are public preview artifacts for open medical AI evaluation infrastructure. They use synthetic examples only. They are not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety proof, and not an official institutional or national program endorsement.

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
8. Three legacy draft Failure Atlas entries plus a public summary index for raw withheld cases.
9. MedHELM oriented metric draft.
10. Medmarks style local proof pack.
11. Versioned labeling and review workflow with a 24 row pilot inter rater review subset.
12. Internal reviewer form, source key, and adjudication log templates for the pilot subset, held out of public release until raw output redistribution is cleared.
13. Scripts for validation, model capture, scoring dry run, benchmark report generation, and public candidate sanitation.

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

## Failure Atlas public summaries

Start with [failure_atlas/public/INDEX.md](failure_atlas/public/INDEX.md). The methodology note is [failure_atlas/public/METHODOLOGY.md](failure_atlas/public/METHODOLOGY.md).

These summaries intentionally do not include raw model outputs, full prompts, model scores, model rankings, or clinical validation claims. They are for evaluation design discussion only.

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

Run the public SourceCheckup Medical preview:

```bash
make sourcecheckup
```

Run the larger SourceCheckup v0.2 example set:

```bash
make sourcecheckup_v02
```

Validate the no ranking leaderboard template:

```bash
make leaderboard
```

Generate the no ranking leaderboard report:

```bash
make leaderboard_report
```

Generate the Failure Atlas case intake report:

```bash
make case_intake
```

Validate SourceCheckup contribution examples:

```bash
make sourcecheckup_contrib_v02
```

## Folder structure

```text
data/
  scenario_taxonomy_v0_2.tsv
  scenario_bank_v1.tsv
  scenario_bank_v2_hard_addendum.tsv
  scenario_bank_v3_scale_seed.tsv
  prompt_set_v1.tsv
  prompt_set_v2_hard_30.tsv
  prompt_set_v3_scale_30.tsv
  inter_rater_review_subset_v0_1.tsv
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
  LABEL_DEFINITION_LOCK_V0_1.md
  CLINICIAN_REVIEW_DISAGREEMENT_PROTOCOL_V0_1.md
  INTER_RATER_REVIEW_SUBSET_PLAN_V0_1.md
  LABELING_PACKAGE_INDEX_V0_1.md
  scoring_model_v0_1.md
failure_atlas/
  public/
    INDEX.md
    METHODOLOGY.md
rubric/
  v0.1.0/
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

Failure Atlas public summary layer:

The public raw withheld summary index is `failure_atlas/public/INDEX.md`. The public methodology note is `failure_atlas/public/METHODOLOGY.md`. These files summarize selected failure patterns without raw outputs, model scores, or model rankings.

Legacy draft atlas entries remain in `docs/failure_atlas_entry_001_insulin_sick_day_wording_draft.md`, `docs/failure_atlas_entry_002_protocol_overprecision_draft.md`, and `docs/failure_atlas_entry_003_remote_rescue_protocols_draft.md`. They are draft notes, not clinical advice or validation claims.

The first external ecosystem sample is in `data/failure_atlas_external_sample_v0_1.jsonl`. It contains three synthetic cases mapped toward MedHELM and Medmarks discussion routes.

The first MedHELM oriented metric draft is in `data/medhelm_remote_rescue_metric_v0_1.json` and `docs/MEDHELM_REMOTE_RESCUE_BOUNDARY_METRIC_PACKAGE_DRAFT.md`.

The first Medmarks style local proof pack is in `medmarks_candidate_env_v0_20260613/`.

Labeling and review workflow:

`LABELING.md` defines the current labeling workflow. The first versioned rubric package is under `rubric/v0.1.0/`. The 24 row pilot inter rater review subset is in `data/inter_rater_review_subset_v0_1.tsv`. Internal reviewer forms are generated locally but are not included in the public release while raw model output redistribution remains uncleared.

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
