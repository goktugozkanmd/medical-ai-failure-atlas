# Clinician led medical AI safety evaluation

Status: public v0.1 release.

Date: 2026 06 13

## 2026 06 16 public preview update

New visible build surfaces are now staged in this public repository:

1. TR MedAI Safety Suite public release card.
2. [SourceCheckup Medical public demo matrix](docs/sourcecheckup/PUBLIC_DEMO_MATRIX_20260616.md)
3. Turkish Clinical AI Assurance Lab governance matrix.
4. Clinician AI Literacy 30 minute Turkish facilitator packet.
5. [Runnable SourceCheckup Medical tool](sourcecheckup/README.md)
6. [Failure Atlas taxonomy public preview](failure_atlas/public/TAXONOMY_PREVIEW_20260616.md)
7. [SourceCheckup workflow example](sourcecheckup/WORKFLOW_EXAMPLE_20260616.md)
8. [June 2026 public roadmap](docs/ROADMAP_2026_06.md)
9. [No ranking leaderboard design](docs/LEADERBOARD_DESIGN_V0_1.md)
10. [Synthetic report row contributor guide](docs/CONTRIBUTOR_GUIDE_SYNTHETIC_REPORT_ROWS_V0_1.md)
11. [Failure Atlas case intake checklist](failure_atlas/public/CASE_INTAKE_CHECKLIST_V0_1.md)
12. [SourceCheckup contributor checklist v0.2](docs/sourcecheckup/CONTRIBUTOR_CHECKLIST_V0_2.md)
13. [Failure Atlas taxonomy dashboard](failure_atlas/public/build/taxonomy_dashboard_v0_1.md)
14. [TR MedLLM synthetic risk pack](tr_medllm_safetybench/README.md)
15. [Clinician review queue](failure_atlas/public/build/clinician_review_queue_v0_1.md)
16. [Public infrastructure release note v0.1](docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md)
17. [Clinician review protocol v0.1](docs/CLINICIAN_REVIEW_PROTOCOL_V0_1.md)
18. [Health data quality and label audit card v0.1](docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md)
19. [MedHELM boundary note v0.1](docs/MEDHELM_BOUNDARY_NOTE_V0_1.md)
20. [Medmarks boundary note v0.1](docs/MEDMARKS_BOUNDARY_NOTE_V0_1.md)
21. [Medical language model assurance card template v0.1](docs/ASSURANCE_CARD_TEMPLATE_V0_1.md)
22. [SourceCheckup public contributor issue guide v0.1](docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md)
23. [Six platform dashboard index v0.1](docs/PLATFORM_DASHBOARD_INDEX_V0_1.md)
24. [TR MedLLM specialty spread dashboard v0.1](tr_medllm_safetybench/build/specialty_spread_dashboard_v0_1.md)
25. [SourceCheckup source claim example expansion v0.2](sourcecheckup/build/source_claim_example_expansion_v0_2.md)
26. [Clinician literacy release gate lesson map v0.1](docs/CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md)
27. [Assurance release gate example map v0.1](docs/ASSURANCE_RELEASE_GATE_EXAMPLE_MAP_V0_1.md)
28. [SourceCheckup TR MedLLM assurance routing map v0.1](docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md)
29. [Source review worksheets v0.1](docs/SOURCE_REVIEW_WORKSHEETS_V0_1.md)
30. [Red flag source locator and warning sign checklist v0.1](docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md)
31. [Red flag source locator contributor examples v0.1](docs/sourcecheckup/RED_FLAG_SOURCE_LOCATOR_CONTRIBUTOR_EXAMPLES_V0_1.md)
32. [Warning sign reviewer role table v0.1](docs/WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md)
33. [Label audit reviewer role table v0.1](docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md)
34. [Label audit public contributor issue guide v0.1](docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md)
35. [Label audit example intake rows v0.1](docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md)

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
14. A 14 row Turkish synthetic risk pack with specialty spread rows across cardiology, endocrinology, nephrology, infectious diseases, geriatrics, and pregnancy medication safety.

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

Generate the Failure Atlas taxonomy dashboard:

```bash
make taxonomy_dashboard
```

Validate the TR MedLLM synthetic risk pack:

```bash
make tr_medllm_pack
```

Validate the TR MedLLM specialty spread:

```bash
make tr_medllm_specialty_spread
```

Generate the TR MedLLM specialty spread dashboard:

```bash
make tr_medllm_specialty_dashboard
```

Generate the clinician review queue:

```bash
make clinician_review_queue
```

Validate the clinician review protocol:

```bash
make clinician_review_protocol
```

Generate the clinician literacy release gate lesson map:

```bash
make clinician_literacy_map
```

Validate the public release note:

```bash
make release_note
```

Validate the health data quality and label audit card:

```bash
make health_data_quality_card
```

Validate the MedHELM and Medmarks boundary notes:

```bash
make boundary_notes
```

Validate the assurance card template:

```bash
make assurance_card_template
```

Generate the assurance release gate example map:

```bash
make assurance_release_gate_map
```

Generate the SourceCheckup TR MedLLM assurance routing map:

```bash
make sourcecheckup_tr_medllm_routing
```

Generate the source review worksheets:

```bash
make source_review_worksheets
```

Generate the red flag source locator and warning sign checklist:

```bash
make red_flag_warning_checklist
```

Validate SourceCheckup contribution examples:

```bash
make sourcecheckup_contrib_v02
```

Generate the red flag source locator contributor examples:

```bash
make red_flag_contributor_examples
```

Generate the warning sign reviewer role table:

```bash
make warning_sign_role_table
```

Generate the label audit reviewer role table:

```bash
make label_audit_role_table
```

Validate the label audit public contributor issue route:

```bash
make label_audit_public_issue
```

Generate the label audit example intake rows:

```bash
make label_audit_examples
```

Validate the SourceCheckup public contributor issue route:

```bash
make sourcecheckup_public_issue
```

Generate the SourceCheckup source claim expansion dashboard:

```bash
make sourcecheckup_expansion_dashboard
```

Validate the six platform dashboard index:

```bash
make platform_dashboard
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
  HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md
  MEDHELM_BOUNDARY_NOTE_V0_1.md
  MEDMARKS_BOUNDARY_NOTE_V0_1.md
  ASSURANCE_CARD_TEMPLATE_V0_1.md
  ASSURANCE_RELEASE_GATE_EXAMPLE_MAP_V0_1.md
  SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md
  SOURCE_REVIEW_WORKSHEETS_V0_1.md
  RED_FLAG_WARNING_CHECKLIST_V0_1.md
  PLATFORM_DASHBOARD_INDEX_V0_1.md
  CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md
  assurance_card_template_v0_1.json
  assurance_release_gate_example_map_v0_1.json
  sourcecheckup_tr_medllm_assurance_routing_map_v0_1.json
  source_review_worksheets_v0_1.json
  red_flag_warning_checklist_v0_1.json
  clinician_literacy_release_gate_lesson_map_v0_1.json
  scoring_model_v0_1.md
  sourcecheckup/
    CONTRIBUTOR_CHECKLIST_V0_2.md
    PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md
    RED_FLAG_SOURCE_LOCATOR_CONTRIBUTOR_EXAMPLES_V0_1.md
  label_audit/
    PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md
    LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md
    label_audit_example_intake_v0_1.json
sourcecheckup/
  build/
    source_claim_example_expansion_v0_2.md
  review_queue/
    source_claim_review_queue_v0_1.jsonl
failure_atlas/
  public/
    INDEX.md
    METHODOLOGY.md
tr_medllm_safetybench/
  README.md
  build/
    specialty_spread_dashboard_v0_1.md
  synthetic_risk_pack_v0_1.jsonl
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
  validate_assurance_card_template_v0_1.py
  validate_assurance_release_gate_example_map_v0_1.py
  validate_red_flag_warning_checklist_v0_1.py
  validate_red_flag_contributor_examples_v0_1.py
  validate_tr_medllm_specialty_spread_v0_1.py
  validate_tr_medllm_specialty_dashboard_v0_1.py
  validate_sourcecheckup_example_expansion_dashboard_v0_2.py
  validate_clinician_literacy_release_gate_lesson_map_v0_1.py
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
