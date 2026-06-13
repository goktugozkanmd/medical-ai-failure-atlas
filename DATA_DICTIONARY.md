# Data dictionary

Status: internal draft.

## data/scenario_bank_v1.tsv

Columns:

1. `scenario_id`: Stable scenario identifier.
2. `theme`: Main evaluation theme.
3. `domain`: Clinical domain.
4. `setting`: Care setting.
5. `patient_summary`: Synthetic patient summary.
6. `task_for_model`: Requested task.
7. `expected_safety_focus`: Main safety issue the evaluator should watch.
8. `development_feedback_signal`: Expected model improvement signal.
9. `suggested_prompt_style`: Prompt type.

## data/scenario_bank_v2_hard_addendum.tsv

This file uses the same columns as `scenario_bank_v1.tsv`.

Purpose:

1. Add harder safety traps.
2. Increase false reassurance cases.
3. Add abstention cases where exact advice would be unsafe.
4. Add evidence reliability and model critique cases.
5. Prepare the next model run beyond the first ten prompts.

## data/scenario_bank_v3_scale_seed.tsv

This file uses the same columns as `scenario_bank_v1.tsv`.

Purpose:

1. Add the next 50 scenarios toward scale.
2. Balance false reassurance, unsafe dosing, evidence reliability, abstention, under triage, over treatment, communication risk, bias, workflow context, and model critique.
3. Prepare the project for larger batch runs beyond the hard thirty pilot.

## data/scenario_taxonomy_v0_2.tsv

Columns:

1. `axis_id`: Stable taxonomy identifier.
2. `axis_type`: Taxonomy level.
3. `name`: Axis name.
4. `description`: What the axis captures.
5. `target_count`: Planned contribution toward a 300 case benchmark.

Purpose:

This file prevents the scenario bank from becoming a random list. It defines the failure pattern, clinical domain, and setting axes needed for scaling.

## data/prompt_set_v1.tsv

Columns:

1. `scenario_id`: Scenario identifier linked to the scenario bank.
2. `prompt_text`: Prompt sent to each model.
3. `output_capture_instruction`: Rule for saving the model output.

## data/prompt_set_v2_hard_30.tsv

This file uses the same columns as `prompt_set_v1.tsv`.

Purpose:

1. Prepare the next harder model run.
2. Use 30 scenarios from the hard addendum.
3. Stress false reassurance, dangerous remote dosing, evidence reliability, and escalation.

## data/prompt_set_v3_scale_30.tsv

This file uses the same columns as `prompt_set_v1.tsv`.

Purpose:

1. Run 30 selected scenarios from the V3 scale seed.
2. Stress remote dosing, rescue protocol wording, evidence reliability, abstention, under triage, and communication risk.
3. Produce a second model output layer beyond the hard thirty run.

## data/failure_atlas_external_sample_v0_1.jsonl

Internal draft JSONL sample for possible external benchmark ecosystem discussion.

Required fields:

1. `case_id`: Stable sample case identifier.
2. `source_scenario_id`: Original local scenario identifier.
3. `task_family`: Broad task type.
4. `medhelm_category_guess`: Draft MedHELM category mapping.
5. `medmarks_subset_guess`: Draft Medmarks subset mapping.
6. `clinical_domain`: Clinical domain.
7. `data_provenance`: Must be `synthetic`.
8. `contains_patient_data`: Must be `false`.
9. `not_for_clinical_use`: Must be `true`.
10. `external_status`: Must be `internal_draft` until release approval.
11. `prompt`: Prompt text for model output generation.
12. `expected_safety_focus`: Expected safety behavior focus.
13. `failure_mechanism_tags`: List of failure mechanism tags.
14. `clinician_review_question`: Question for clinician review.
15. `rubric`: List of criterion objects with `criterion_id` and `positive_behavior`.

## data/medhelm_remote_rescue_metric_v0_1.json

Internal draft metric package for a MedHELM oriented LLM jury refinement discussion.

Required fields:

1. `metric_id`: Stable metric identifier.
2. `status`: Must remain `internal_draft` until release approval.
3. `not_for_clinical_use`: Must be `true`.
4. `contains_patient_data`: Must be `false`.
5. `data_provenance`: Must be `synthetic`.
6. `intended_route`: Draft route for discussion.
7. `purpose`: Metric purpose.
8. `source_case_ids`: External sample case IDs.
9. `source_scenario_ids`: Local scenario IDs.
10. `score_scale`: Defines scores 0, 1, and 2.
11. `criteria`: List of criterion objects with `criterion_id` and `score_focus`.
12. `judge_prompt_draft`: Draft judge prompt text.
13. `failure_tags`: Candidate tags.
14. `release_boundary`: External release limits.

## results/first10_preliminary_screening_scores_20260613.csv

Columns:

1. `model_name`: Model name visible during the run.
2. `scenario_id`: Scenario identifier.
3. `clinical_correctness`: Score from 0 to 2.
4. `diagnostic_reasoning`: Score from 0 to 2.
5. `safety_and_escalation`: Score from 0 to 2.
6. `guideline_fit`: Score from 0 to 2.
7. `evidence_reliability`: Score from 0 to 2.
8. `clinical_actionability`: Score from 0 to 2.
9. `uncertainty_handling`: Score from 0 to 2.
10. `open_source_feedback_value`: Score from 0 to 2.
11. `high_risk_safety_flag`: Preliminary safety flag.
12. `development_feedback_note`: Short clinician feedback note.
13. `total_score`: Sum of the eight domain scores.

## Important boundary

The current score file is a preliminary internal screen. It must not be described as final model performance.
