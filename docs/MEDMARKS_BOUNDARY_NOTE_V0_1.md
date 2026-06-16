# Medmarks boundary note v0.1

Date: 2026 06 16

Status: public preview.

This note explains how the local synthetic Medical AI Failure Atlas proof pack can be described as Medmarks style without claiming Medmarks acceptance or compatibility.

It does not claim Medmarks compatibility, benchmark equivalence, endorsement, clinical validation, clinical deployment readiness, model safety, model ranking, or official acceptance.

## Source anchors checked

Checked on 2026 06 16:

1. Medmarks GitHub: https://github.com/MedARC-AI/Medmarks
2. Medmarks technical report: https://arxiv.org/html/2605.01417v1

Current source summary:

1. Medmarks describes itself as an open source LLM benchmark suite for medical tasks.
2. The GitHub README describes 30 open source benchmarks across question answering, information extraction, consumer health questions, clinical reasoning, EHR interactions, medical calculations, and open ended medical tasks.
3. The GitHub README describes three practical subsets: verifiable tasks, open ended tasks, and training capable environments.
4. The technical report states that benchmark performance is not equivalent to clinical competence and must be interpreted with care.

## Local mapping boundary

The local repository can discuss a Medmarks style proof pack.

Allowed wording:

`Medmarks style local proof pack`

`Medmarks oriented boundary note`

`open ended safety wording probe`

`local dry run planning without endpoint calls`

Not allowed wording:

`Medmarks compatible`

`Medmarks accepted`

`Medmarks validated`

`same status as a Medmarks benchmark`

## Local assets

Current public local assets:

1. `medmarks_candidate_env_v1_20260614/VALIDATION_REPORT.md`
2. `medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/STAGING_MANIFEST.md`
3. `medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/configs/failure_atlas_safety_wording_30case_smoke.toml`
4. `medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/data/failure_atlas_medmarks_30_case_seed_v0_1.jsonl`
5. `medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/docs/MEDMARKS_FAILURE_PROBE_SET_DATASHEET_V0_1.md`
6. `medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/docs/MEDMARKS_FAILURE_PROBE_TAXONOMY_V0_1.md`

These assets are synthetic and are not a Medmarks issue, pull request, merged environment, model evaluation, judge evaluation, clinical validation, or benchmark performance report.

## Fit to Medmarks style subsets

### Verifiable task style

Current local fit is weak because the Failure Atlas examples are open ended and safety wording focused.

### Open ended task style

Current local fit is strongest here because each case needs rubric based review of safety wording, missing variables, and triage protocol separation.

### Training capable environment style

Current local fit is exploratory only. The current work is a probe set and local proof pack, not a training environment release.

## Dry run boundary

The local validation report supports only this claim:

`The Medmarks style staging package passed a local scratch checkout dependency smoke and dry run planning without endpoint calls.`

It does not support claims about:

1. Model performance.
2. Judge performance.
3. Clinical safety.
4. Medmarks acceptance.
5. Public pull request readiness.
6. Benchmark validity.

## Track A value

For Türkiye health AI safety infrastructure, this note helps separate open benchmark style experimentation from official sandbox, procurement, regulatory, or institutional claims.

## Track B value

For global open source medical AI evaluation, this note makes the local proof pack easier to inspect while keeping all acceptance and compatibility language blocked.

## Next safe public action

The next safe action is to keep the local proof pack inspectable and open a targeted maintainer issue only after exact text review and owner clearance.

Any external Medmarks issue must say:

1. Synthetic examples only.
2. No patient data.
3. No model endpoint call.
4. No judge endpoint call.
5. No model ranking.
6. No clinical validation.
7. No compatibility claim.
