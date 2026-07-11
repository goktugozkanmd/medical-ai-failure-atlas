# Controlled Batch Expansion Plan v0.3

Date: 2026 07 08

Status: local planning gate. This plan replaces the older 300 to 500 row expansion idea.

## Decision

Do not expand the public core as one large mixed benchmark. Keep a hard cap of 300 public core scenario bank rows for the next release cycle.

The project already has several useful layers, but they are not one validation tier:

1. Core scenario bank rows
2. Public prompt sets
3. SafetyGuard prompt surface
4. Turkish safety rows
5. Turkish and English drift rows
6. Panel pilot rows
7. Failure Atlas intake rows

The next growth step is controlled normalization, not raw row inflation.

## Live Counts From Repository

| Layer | Current count | Source |
| --- | ---: | --- |
| Core scenario bank | 150 | `data/scenario_bank_v1.tsv`, `data/scenario_bank_v2_hard_addendum.tsv`, `data/scenario_bank_v3_scale_seed.tsv` |
| Public prompt sets | 70 | `data/prompt_set_v1.tsv`, `data/prompt_set_v2_hard_30.tsv`, `data/prompt_set_v3_scale_30.tsv` |
| SafetyGuard prompt surface | 222 | `safetyguard/data/medfailbench_prompts_v0_2.tsv` |
| Leaderboard prompt surface | 222 | `leaderboard/medfailbench_prompts_v0_2.jsonl` |
| Turkish MedLLM synthetic set | 44 | `data/tr_medllm_synthetic_eval_set_v0_3.jsonl` |
| Turkish and English drift probe | 10 | `data/tr_en_drift_glm_probe_v0_1.tsv` |
| Panel pilot cases | 15 | `data/panel_pilot/clinician_panel_pilot_cases_v0_1.tsv` |

These counts must stay described separately in public text.

## Phase 1: Normalize Current Model Runs

Goal: bring existing leaderboard models toward the same 30 prompt public prompt set where local outputs already exist or where G approves provider cost.

Allowed now:

1. Use existing prompt sets only.
2. Generate local manifests and run plans.
3. Prepare score table templates.
4. Keep model result claims tied to actual run counts.

Blocked without G approval:

1. Paid provider calls.
2. New external outreach.
3. Public release note.
4. Claims that unequal model runs are directly comparable.

## Phase 2: Expand Core Scenario Bank To 220

Goal: add at most 70 new core scenario rows after G approves clinical logic.

Rules:

1. New rows must be synthetic.
2. G approves the clinical logic.
3. No patient data.
4. No hidden patient derived text.
5. Each row has a safety focus, domain, setting, task, and expected safety gate.
6. New rows stay draft until validator and release notes pass.

## Phase 3: Expand Core Scenario Bank To 300

Goal: reach the hard cap only if Phase 2 passes.

Rules:

1. Final core public cap is 300 scenario bank rows.
2. Turkish rows, drift rows, panel pilot rows, and intake rows remain separate layers.
3. Public copy must keep working rows separated by release layer and review status.
4. External clinician panel status remains pending until external scores exist.

## What This Unlocks

1. Cleaner model run comparison.
2. Safer v0.3.0 release planning.
3. Better Health AI Safety Ops story without benchmark bloat.
4. A visible path from 150 core rows to 300 core rows.
5. A guardrail against inflated public claims.

## Blocked Claims

Do not claim:

1. 300 rows exist now.
2. All 222 SafetyGuard rows are one validated public core tier.
3. Turkish, drift, panel, and intake rows are the same release layer.
4. External clinician validation is complete.
5. New cases were added in this planning step.
6. Any model is clinically safe or unsafe for deployment based on this plan.

## Immediate Next Action

Use the validator:

```bash
make controlled_batch_expansion_20260708
```

Then use the resulting JSON manifest as the gate before any new row generation or provider run.
