# Medical AI Safety Field Kit SFC005 Synthetic Evidence Starter

Date: 2026 06 20

Status: public starter route for one concrete reviewer objection.

## Purpose

SFC005 blocks a common medical AI safety mistake: a synthetic failure card is cited as if it proves real world harm frequency, model performance, or clinical outcome.

The useful public action is small. A reviewer should name one sentence that turns a synthetic pattern seed into an evidence claim, then rewrite it so the evidence boundary is clear.

## Start Here

Primary card pack:

https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/PUBLIC_SAFE_FAILURE_CARDS_20260619.md

Global workbook:

https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_GLOBAL_SAFETY_CLAIM_REVIEW_WORKBOOK_20260620.md

Main intake:

https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149

## Reviewer Task

Pick one public or synthetic sentence and test whether it treats a synthetic pattern as stronger evidence than it is.

Use this comment shape:

```text
Role:
Card id: SFC005
Risk:
Evidence claim that goes too far:
Missing gate:
Safer wording:
```

## Evidence Boundary Checks

1. Pattern seed check: does the wording say pattern, possibility, or review seed.
2. Frequency check: does the wording imply incidence, prevalence, commonness, or rate.
3. Outcome check: does the wording imply patient harm, mortality, morbidity, delay, or clinical outcome.
4. Model check: does the wording imply a model failed or passed in real use.
5. Generalization check: does the wording imply the issue applies across hospitals, countries, languages, or specialties.
6. Source support check: does a public source support the exact claim, or only the general topic.

## Safe Rewrite Patterns

Weak wording:

This card shows that the model causes harm in practice.

Safer wording:

This synthetic card describes a plausible failure pattern for review. It does not measure incidence, model performance, patient harm, or clinical outcome.

Weak wording:

This failure is common in hospital use.

Safer wording:

This card names a risk that should be checked before any hospital readiness language is used. It does not estimate real world frequency.

Weak wording:

The example proves that the benchmark misses patient safety risk.

Safer wording:

The example suggests a safety question that a benchmark result may not answer by itself.

## Stop Rules

Block public wording when it claims or implies:

1. Real patient evidence from a synthetic card.
2. Incidence, prevalence, commonness, or rate.
3. Patient harm frequency or clinical outcome.
4. Model failure in real deployment.
5. Hospital readiness or procurement fitness.
6. Benchmark safety failure as a measured result.
7. Institution approval, partner approval, or endorsement.

## Maintainer Route

1. Route SFC005 comments into the main public intake.
2. Convert repeated objections into a clearer Safe Failure Card note.
3. Keep maintainer, project account, and controlled seed comments separate from true third party outside review.
4. Do not count this as validation or field evidence.

## Boundary

Use synthetic or public examples only. Do not include patient data, private clinical text, raw private model output, diagnosis advice, treatment advice, clinical validation, clinical deployment, benchmark ranking, score certification, source truth certification, partner claim, institution claim, endorsement, formal application, payment, terms action, budget action, procurement claim, or official role claim.

## Done Condition

This starter succeeds when one reviewer adds a concrete SFC005 objection that names the overclaim, the missing evidence gate, and safer wording.

Runnable check:

```bash
make medical_ai_safety_field_kit_sfc005_synthetic_evidence_starter
```
