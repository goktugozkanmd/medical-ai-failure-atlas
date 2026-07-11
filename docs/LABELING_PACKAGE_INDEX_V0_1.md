# Labeling package index v0.1

Status: internal package index. Not yet pushed.

Read the labeling package in this order:

1. `dataset/LABELING.md`
2. `docs/LABEL_DEFINITION_LOCK_V0_1.md`
3. `docs/CLINICIAN_REVIEW_DISAGREEMENT_PROTOCOL_V0_1.md`
4. `docs/INTER_RATER_REVIEW_SUBSET_PLAN_V0_1.md`
5. `data/inter_rater_review_subset_v0_1.tsv`
6. `rubric/v0.1.0/README.md`
7. `rubric/v0.1.0/CHANGELOG.md`
8. `review_forms/inter_rater_review_form_v0_1.tsv`
9. `review_forms/inter_rater_review_source_key_v0_1.tsv`
10. `review_forms/adjudication_log_template_v0_1.tsv`
11. `review_forms/README.md`

## What this package does

It defines the first structured labeling workflow for Medical AI Failure Atlas.

It turns the current rubric from an internal idea into a versioned review process.

## What this package does not do

It does not claim clinical validation.

It does not claim model safety.

It does not claim model ranking.

It does not claim deployment readiness.

## Current subset status

The current 24 row subset is a pilot subset for protocol testing.

It is not powered to estimate a stable Cohen kappa value.

Agreement metrics should be treated as exploratory until a larger independently reviewed subset is planned.

The reviewer facing form generated from this subset excludes source priority, possible failure tags, source triage file, and prior short reason fields to reduce first pass reviewer bias.

## Why the subset is not proportional

The subset intentionally over samples high risk and boundary rows.

Reason:

This first review pass is designed to stress test safety gate definitions and disagreement handling, not estimate population prevalence.

## Model identity limitation

The subset uses model route labels from the 2026 06 13 opencode go runs.

Provider snapshot or revision was not pinned for those earlier runs.

Future formal model comparisons should pin provider, endpoint, date, and model revision where available.
