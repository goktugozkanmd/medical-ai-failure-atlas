# Chinese Frontier Medical AI Safety Snapshot v0.2.1

Generated: 2026-07-06

Purpose: a short, data-backed report for targeted feedback to Qwen, DeepSeek, GLM/ZhipuAI, and Kimi/Moonshot teams.

Sources:
- `leaderboard/submissions.json`
- `model_runs/worst_case_safety_report_v0_1.json`

Scope and limits:
- 9 Chinese-family model runs are included.
- Prompt counts differ by model: 5, 6, 28, or 30 prompts.
- Rule-based scoring only.
- External clinician panel validation pending.
- Synthetic cases only. No patient data.
- This is not a model ranking and not clinical validation.

## Executive summary

1. Average scores are not enough. Every Chinese-family model in this snapshot reached min safety 1/5 on at least one prompt.
2. Kimi K2.7 Code and Kimi K2.6 have the highest unsafe-tier rates in this snapshot, but prompt counts are small.
3. Qwen 3.7 Max has the most stable high-sample warning signal: 14/30 unsafe-tier prompts, 46.7% unsafe rate.
4. GLM-5.2 has 11/28 unsafe-tier prompts, 39.3% unsafe rate, despite a moderate average safety score.
5. DeepSeek's three current runs share the same source-support score: 48.0.

## All Chinese-family runs

| Model | Prompts | Avg safety | Source support | Clinical boundary | Min safety | Unsafe-tier count | Unsafe rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen 2.5-7B-Instruct | 5 | 52.0 | 64.0 | 63.2 | 1/5 | 1/5 | 20.0% |
| Kimi K2.6 | 6 | 40.0 | 53.3 | 60.7 | 1/5 | 3/6 | 50.0% |
| Qwen 3.7 Max | 30 | 45.3 | 56.0 | 59.9 | 1/5 | 14/30 | 46.7% |
| Qwen 3.6 Plus | 30 | 46.7 | 60.0 | 62.0 | 1/5 | 11/30 | 36.7% |
| DeepSeek V3.2 | 5 | 44.0 | 48.0 | 59.2 | 1/5 | 2/5 | 40.0% |
| Kimi K2.7 Code | 5 | 36.0 | 64.0 | 60.8 | 1/5 | 3/5 | 60.0% |
| GLM-5.2 | 28 | 47.1 | 57.1 | 61.6 | 1/5 | 11/28 | 39.3% |
| DeepSeek V4 Pro | 5 | 52.0 | 48.0 | 59.2 | 1/5 | 1/5 | 20.0% |
| DeepSeek V4 Flash | 5 | 44.0 | 48.0 | 59.2 | 1/5 | 2/5 | 40.0% |

## Qwen

| Model | Prompts | Avg safety | Source support | Clinical boundary | Min safety | Unsafe-tier count | Unsafe rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen 2.5-7B-Instruct | 5 | 52.0 | 64.0 | 63.2 | 1/5 | 1/5 | 20.0% |
| Qwen 3.7 Max | 30 | 45.3 | 56.0 | 59.9 | 1/5 | 14/30 | 46.7% |
| Qwen 3.6 Plus | 30 | 46.7 | 60.0 | 62.0 | 1/5 | 11/30 | 36.7% |

Main follow-up angle: inspect prompt-level failures for **Qwen 3.7 Max**, which has the highest unsafe-tier rate in this family snapshot (14/30, 46.7%).
## DeepSeek

| Model | Prompts | Avg safety | Source support | Clinical boundary | Min safety | Unsafe-tier count | Unsafe rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| DeepSeek V3.2 | 5 | 44.0 | 48.0 | 59.2 | 1/5 | 2/5 | 40.0% |
| DeepSeek V4 Pro | 5 | 52.0 | 48.0 | 59.2 | 1/5 | 1/5 | 20.0% |
| DeepSeek V4 Flash | 5 | 44.0 | 48.0 | 59.2 | 1/5 | 2/5 | 40.0% |

Main follow-up angle: inspect prompt-level failures for **DeepSeek V3.2**, which has the highest unsafe-tier rate in this family snapshot (2/5, 40.0%).
## GLM/ZhipuAI

| Model | Prompts | Avg safety | Source support | Clinical boundary | Min safety | Unsafe-tier count | Unsafe rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| GLM-5.2 | 28 | 47.1 | 57.1 | 61.6 | 1/5 | 11/28 | 39.3% |

Main follow-up angle: inspect prompt-level failures for **GLM-5.2**, which has the highest unsafe-tier rate in this family snapshot (11/28, 39.3%).
## Kimi/Moonshot

| Model | Prompts | Avg safety | Source support | Clinical boundary | Min safety | Unsafe-tier count | Unsafe rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| Kimi K2.6 | 6 | 40.0 | 53.3 | 60.7 | 1/5 | 3/6 | 50.0% |
| Kimi K2.7 Code | 5 | 36.0 | 64.0 | 60.8 | 1/5 | 3/5 | 60.0% |

Main follow-up angle: inspect prompt-level failures for **Kimi K2.7 Code**, which has the highest unsafe-tier rate in this family snapshot (3/5, 60.0%).

## Recommended outreach framing

Use this frame:

> I ran your model family through a synthetic, clinician-authored medical AI safety benchmark. This is not a ranking and not clinical validation. The useful part is the prompt-level failure pattern: where the model crosses safety boundaries, misses escalation, or gives over-specific medical detail. If useful, I can share the prompt-level JSON and adapt the suite for your internal QA format.

Avoid this frame:

> Your model is unsafe.

## Next required checks before sending to teams

- Verify every cited prompt-level example against raw model output.
- Attach only synthetic, non-patient prompts.
- Keep all claims as rule-based benchmark findings.
- Ask for feedback or collaboration; do not accuse.
