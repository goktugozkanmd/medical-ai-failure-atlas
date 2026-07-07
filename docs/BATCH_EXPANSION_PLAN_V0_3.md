# Batch Expansion Plan: 300–500 Vignette / 15–20 Model

**Status:** Planning | **Author:** C0R3 | **Date:** 2026-07-07 12:30 TRT

## Rationale

Current leaderboard has 10 models with uneven prompt counts (5–30). 
The project needs:
1. **Equal footing** — all models tested on same prompt set for fair comparison
2. **Western model coverage** — currently only Llama 3.1-8B
3. **Scenario depth** — expand from ~150 scenario-bank rows toward 300–500
4. **Statistical significance** — 5-prompt runs produce noisy signals

## Phase 1: Equalize to 30 Prompts (All Existing Models)

Bring every current model to 30 prompts using existing scenario bank.

| Model | Current | Needed | New prompts needed |
|-------|---------|--------|--------------------|
| Llama 3.1-8B | 5 | 30 | 25 |
| Qwen 2.5-7B | 5 | 30 | 25 |
| DeepSeek V4 Pro | 5 | 30 | 25 |
| DeepSeek V4 Flash | 5 | 30 | 25 |
| DeepSeek V3.2 | 5 | 30 | 25 |
| Kimi K2.6 | 6 | 30 | 24 |
| Kimi K2.7 Code | 5 | 30 | 25 |
| Qwen 3.6 Plus | 30 | 30 | 0 |
| Qwen 3.7 Max | 30 | 30 | 0 |
| GLM-5.2 | 28 | 30 | 2 |
| **Total** | **124** | **300** | **176 new runs** |

**Effort:** ~176 API calls. At ~5s per call = ~15 min. At 1–2 min per model pipeline = ~2 hours agent time.

**Risk:** Low. Same scenario bank, same scorer, same pipeline. Pure scale operation.

## Phase 2: Add Western Frontier Models

The biggest strategic gap. Current leaderboard has 9 Chinese + 1 Western (Llama).

| Model | Priority | Rationale | Access |
|-------|----------|-----------|--------|
| **GPT-4o** | P0 | Most widely used clinical AI | OpenRouter |
| **Claude 4 Opus / Sonnet** | P0 | Strong medical reasoning | OpenRouter |
| **Gemini 2.5 Pro** | P0 | Google's medical ML ecosystem | OpenRouter |
| **GPT-5 Nano** | P1 | Already has run metadata in weekly preview | OpenRouter |
| **Mistral Large 2** | P2 | Strong EU alternative | OpenRouter |
| **Llama 4** (if public) | P2 | Next-gen Meta model | OpenRouter |

**Effort:** 6 models × 30 prompts = 180 API calls + pipeline eval.

**Risk:** Cost. Need OpenRouter credits. Estimation: ~60M tokens input + ~6M output at ~$0.50–2.00 total depending on model pricing. Low technical risk.

## Phase 3: Expand Scenario Bank to 500 Rows

### Strategy: Tiered Expansion

| Tier | Description | New rows | Total |
|------|-------------|----------|-------|
| Core v1 | Current safety-gate scenarios | 150 | 150 |
| Core v2 | Extend severity/gate coverage | 100 | 250 |
| Specialty | Cardiology, nephrology, ER, geriatrics | 100 | 350 |
| Language drift | TR-EN across all new scenarios | 50 | 400 |
| Rare edge cases | Multi-condition, drug interactions, guideline conflicts | 100 | 500 |

### Scenario source approach
- **No patient data** — synthetic vignettes only
- **Clinician-authored** — G creates or approves the clinical logic
- **Pattern-based generation** — use scenario template system to create systematic variations
- **Prompt variety** — each scenario produces 2–3 prompt variations (direct, masked, escalation-framed)
- **Validation** — all new scenarios go through existing validator + pytest gate

## Phase 4: Priority Sequencing

```
Week 1-2: Phase 1 (equalize existing models to 30 prompts)
          + Phase 2 top-3 Western models (GPT-4o, Claude, Gemini)
Week 3-4: Phase 3 tier 1-2 (Core v2 + Specialty: +200 rows)
Week 5-6: Phase 2 remaining (GPT-5 Nano, Mistral, Llama 4)
          + Phase 3 tier 3 (Language drift: +50 rows)
Week 7-8: Phase 3 tier 4 (Rare edge cases: +100 rows)
          + Full re-eval all models on complete 500-scenario set
```

## Pre-Execution Checklist

- [ ] All new prompts pass `make validate-public`
- [ ] No patient data in any new scenario
- [ ] All model runs use same system prompt and scoring rubric
- [ ] CI passes after each push
- [ ] Public claims updated: "X scenarios, Y models, clinician-authored"
- [ ] STATE_LEDGER and BAGLAM2 updated

## Blockers

1. **Western model cost** — needs G confirmation on OpenRouter budget
2. **G approval** — Phase 2 (Western models) needs G go-ahead before API calls
3. **Phase 3 scenario design** — G needs to sign off on new clinical vignette logic

## Immediate Next Action

**Start Phase 1 now** — equalize existing 10 models to 30 prompts each. This uses existing scenarios and pipeline, costs nothing extra, and produces the biggest immediate signal improvement.

Ready to start: `python3 -m src.batch_eval --models "llama3.1-8b,qwen2.5-7b,deepseek-v4-pro,deepseek-v4-flash,deepseek-v3.2,kimi-k2.6,kimi-k2.7-code,glm-5.2" --prompts ./data/scenario_bank_v1 --output model_runs/batch_phase1_20260707`