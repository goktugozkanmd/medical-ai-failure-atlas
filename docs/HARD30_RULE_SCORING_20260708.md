# Hard30 Rule Scoring Closure

Status: prompt-linked rescoring corrected and externally audited on 2026-07-11. No new model API call was made.

## Scope

The existing Qwen and DeepSeek hard30 raw outputs were rescored locally with `failure_atlas.scorer.score_raw_output` and `data/scoring_rubric_v0_3.json`.

## Scorer correction

The pre-send audit found false positives in `unsafe_discharge_reassurance`. The scorer treated negated warnings such as “do not wait until morning” and benign uses of “reassuring” as unsafe discharge advice. A later audit found that the first corrected rerun omitted `prompt_text` from the legacy raw artifacts, which disabled prompt-dependent checks. The raw artifacts now carry the canonical prompts, and the scorer rejects promptless rows.

## Corrected results

| Model run | Rows | Empty answers | Safety-gate triggers | Mean rule safety |
|-----------|------|---------------|----------------------|------------------|
| DeepSeek V4 Pro hard30 | 30 | 0 | 6 | 3.8 / 5.0 |
| Qwen3 Max hard30 | 30 | 0 | 4 | 4.0 / 5.0 |

## Interpretation lock

These are local lexical rule-screen outputs from synthetic cases. A trigger is not a clinician-confirmed safety failure. Technical review found several keyword mismatches and two DeepSeek output-quality defects involving self-referential or truncated answers. Blinded clinician review remains pending. The results are not external leaderboard claims, deployment recommendations, clinical validation, or safety certifications.

## External record

- Qwen follow-up: https://github.com/QwenLM/Qwen3/issues/1877#issuecomment-4944990823
- DeepSeek first contact: https://github.com/deepseek-ai/DeepSeek-V3/issues/1489
- Scorer correction: https://github.com/goktugozkanmd/medical-ai-failure-atlas/commit/a2cef1d4744fd82db15ab8900976b98769d05a28
