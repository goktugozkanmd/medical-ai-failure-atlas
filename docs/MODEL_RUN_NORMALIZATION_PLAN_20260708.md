# Model Run Normalization Plan

Date: 2026 07 08

Status: local manifest and score table plan.

Purpose: move the current public model run surface toward one shared 30 prompt hard set without adding cases or starting provider calls.

## Boundary

No external action, no provider API call, no new case addition, no patient data, no physician selection, no clinical validation claim, no official compatibility claim, and no model ranking.

## Current Gap

- Public models tracked: 10.
- Target prompt count per public model: 30.
- Public normalization gap: 176 rows.
- Rows that require future provider generation if approved: 149.
- Rows already available locally but not yet fully reflected in the public score table: 27.

## Score Table Draft

| Model | Public rows | Local rows found | Public gap | Provider generation gap | Local score or promotion gap | State |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Llama 3.1-8B-Instruct | 5 | 5 | 25 | 25 | 0 | provider_generation_needed_later |
| Qwen 2.5-7B-Instruct | 5 | 5 | 25 | 25 | 0 | provider_generation_needed_later |
| Kimi K2.6 | 6 | 6 | 24 | 24 | 0 | provider_generation_needed_later |
| Qwen 3.7 Max | 30 | 30 | 0 | 0 | 0 | public_already_30 |
| Qwen 3.6 Plus | 30 | 30 | 0 | 0 | 0 | public_already_30 |
| DeepSeek V3.2 | 5 | 5 | 25 | 25 | 0 | provider_generation_needed_later |
| Kimi K2.7 Code | 5 | 5 | 25 | 25 | 0 | provider_generation_needed_later |
| GLM-5.2 | 28 | 30 | 2 | 0 | 2 | local_30_available_public_table_lagging |
| DeepSeek V4 Pro | 5 | 30 | 25 | 0 | 25 | local_30_available_public_table_lagging |
| DeepSeek V4 Flash | 5 | 5 | 25 | 25 | 0 | provider_generation_needed_later |

## Immediate Work Order

1. Promote or rescore the existing DeepSeek V4 Pro hard30 local artifacts into the draft score table.
2. Close the GLM 5.2 table gap from the existing local 30 row output before any provider call.
3. Park models with missing local rows until the user explicitly approves provider generation.

## Validation

Run:

```bash
make model_run_normalization_plan_20260708
```
