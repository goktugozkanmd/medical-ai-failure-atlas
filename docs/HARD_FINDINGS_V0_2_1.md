# Hard Findings v0.2.1 — MedFailBench

Generated: 2026-07-06

Source files:
- `leaderboard/submissions.json`
- `model_runs/worst_case_safety_report_v0_1.json`

Scope:
- Current public leaderboard: 10 models.
- Rule-based scoring only.
- External clinician panel validation pending.
- Synthetic cases only. No patient data.
- This is not a model ranking and not clinical validation.

## Current leaderboard plus worst-case view

| Model | Prompts | Avg safety | Source support | Clinical boundary | Min safety | Unsafe-tier count | Unsafe rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| Llama 3.1-8B-Instruct | 5 | 60.0 | 56.0 | 63.2 | 3/5 | 0/5 | 0.0% |
| Qwen 2.5-7B-Instruct | 5 | 52.0 | 64.0 | 63.2 | 1/5 | 1/5 | 20.0% |
| Kimi K2.6 | 6 | 40.0 | 53.3 | 60.7 | 1/5 | 3/6 | 50.0% |
| Qwen 3.7 Max | 30 | 45.3 | 56.0 | 59.9 | 1/5 | 14/30 | 46.7% |
| Qwen 3.6 Plus | 30 | 46.7 | 60.0 | 62.0 | 1/5 | 11/30 | 36.7% |
| DeepSeek V3.2 | 5 | 44.0 | 48.0 | 59.2 | 1/5 | 2/5 | 40.0% |
| Kimi K2.7 Code | 5 | 36.0 | 64.0 | 60.8 | 1/5 | 3/5 | 60.0% |
| GLM-5.2 | 28 | 47.1 | 57.1 | 61.6 | 1/5 | 11/28 | 39.3% |
| DeepSeek V4 Pro | 5 | 52.0 | 48.0 | 59.2 | 1/5 | 1/5 | 20.0% |
| DeepSeek V4 Flash | 5 | 44.0 | 48.0 | 59.2 | 1/5 | 2/5 | 40.0% |

## Finding 1 — Average safety hides unsafe-tier answers

Several models have average safety scores in the 40-50 range while still dropping to safety 1/5 on individual prompts.

Most visible examples:

- Kimi K2.7 Code: 3/5 unsafe-tier prompts, 60.0% unsafe rate.
- Kimi K2.6: 3/6 unsafe-tier prompts, 50.0% unsafe rate.
- Qwen 3.7 Max: 14/30 unsafe-tier prompts, 46.7% unsafe rate.
- GLM-5.2: 11/28 unsafe-tier prompts, 39.3% unsafe rate.
- Qwen 3.6 Plus: 11/30 unsafe-tier prompts, 36.7% unsafe rate.

Interpretation: mean score alone is not enough for medical AI safety review. The clinically relevant question is what happens on the worst high-acuity prompt.

## Finding 2 — Minimum safety reaches 1/5 in 9 of 10 current leaderboard models

Only Llama 3.1-8B-Instruct avoided the unsafe tier in this current leaderboard snapshot, with min safety 3/5 and 0/5 unsafe-tier prompts.

Every other current leaderboard model has at least one prompt with min safety 1/5.

Interpretation: even when average performance looks usable-with-caution, worst-case safety failures remain visible.

## Finding 3 — Chinese frontier family coverage is the strongest current visibility angle

The current leaderboard includes 9 Chinese-family model runs across Qwen, DeepSeek, GLM, and Kimi, plus one Llama baseline.

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

Interpretation: this gives a concrete route for targeted model-team feedback. The message is not "these models are bad." The message is: these models show measurable medical safety boundary failures on an open synthetic benchmark, and the prompt-level data can help teams inspect failure modes.

## Finding 4 — DeepSeek source-support scores are consistently low in this snapshot

DeepSeek V3.2, V4 Flash, and V4 Pro each show source support score 48.0 in the current leaderboard.

Interpretation: this is a clean feedback angle for DeepSeek: source support and evidence-boundary behavior should be inspected separately from average safety.

## External-use wording

Safe public wording:

> MedFailBench v0.2.1 shows that average medical AI safety scores can hide worst-case unsafe-tier answers. In this rule-based, synthetic, clinician-authored benchmark, 9 of 10 current leaderboard models reached safety 1/5 on at least one prompt. External clinician validation is pending.

Do not claim:

- clinical validation
- real patient outcome prediction
- model ranking superiority
- that a model is unsafe in clinical deployment based on this alone
- that all 241 active working rows are the same validation tier
