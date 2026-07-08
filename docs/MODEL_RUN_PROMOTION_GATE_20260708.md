# Model Run Promotion Gate

Date: 2026 07 08

Status: local score table promotion gate.

Purpose: close the local part of the 30 prompt normalization gap for DeepSeek V4 Pro and GLM 5.2 without provider calls.

## Boundary

No external action, no provider API call, no new case addition, no patient data, no physician selection, no clinical validation claim, no official compatibility claim, and no model ranking.

## Local Rows

- Models ready for local promotion review: 2.
- Local rows scored in this gate: 60.
- Public rows that this can close from existing local artifacts: 27.
- Provider generation rows used: 0.

## Draft Score Table

| Model | Public rows before | Scored local rows | Local gap closed | Promotion status | Score file |
| --- | ---: | ---: | ---: | --- | --- |
| DeepSeek V4 Pro | 5 | 30 | 25 | ready_for_local_review_not_public | `model_runs/model_run_normalization_20260708/deepseek_v4_pro_hard30_enriched_rule_scores.json` |
| GLM-5.2 | 28 | 30 | 2 | ready_for_local_review_not_public | `model_runs/model_run_normalization_20260708/glm_5_2_hard30_enriched_rule_scores.json` |

## Next

1. Review schema and row consistency for the two local score files.
2. Decide whether these rows should update a public leaderboard draft.
3. Keep the remaining provider generation gap blocked until explicit approval.

## Validation

Run:

```bash
make model_run_promotion_gate_20260708
```
