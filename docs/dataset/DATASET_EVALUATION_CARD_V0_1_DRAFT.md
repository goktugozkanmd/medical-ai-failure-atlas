# Dataset and evaluation card v0.1 draft

Status: internal draft for future public release.

Date: 2026 06 13

## Name

Medical AI Failure Atlas v0.1 draft

## Summary

This is a physician authored synthetic evaluation resource for studying how medical AI systems handle safety wording, missing variables, urgent triage, evidence reliability, and the boundary between general guidance and individualized protocol detail.

## Intended use

1. Model development feedback.
2. Safety wording evaluation.
3. Open ended rubric design.
4. Clinician review workflow design.
5. Benchmark ecosystem discussion with projects such as MedHELM and Medmarks.

## Non use

Do not use this resource as clinical advice.

Do not use this resource to decide patient care.

Do not use this resource to claim that a model is safe or unsafe overall.

Do not use this resource as a final clinical validation study.

## Data provenance

All cases are synthetic.

No patient data are included.

No protected health information is included.

## Current scale

1. 150 synthetic scenarios.
2. 70 prompt rows.
3. 3 external sample JSONL rows.
4. 1 MedHELM oriented metric JSON.
5. 1 Medmarks style local environment probe.

## Current review status

Use this wording:

`physician authored synthetic draft pending final clinician review`

Do not use this wording yet:

`clinician validated`

## Data quality companion

The public data quality and label audit companion is:

`docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`

It is a release readiness checklist for synthetic dataset surfaces. It is not proof of dataset quality and not clinical validation.

## Known limitations

1. Clinician confirmation is not complete.
2. Raw model output redistribution terms are not cleared.
3. The failure tags are draft taxonomy labels.
4. The examples are synthetic and may not cover real workflow diversity.
5. No formal inter rater reliability process has been completed.
6. The current package includes internal draft material that must be excluded from a public release candidate.

## Evaluation dimensions

1. Emergency risk recognition.
2. Unsafe precision avoidance.
3. Missing variable awareness.
4. Triage protocol separation.
5. Safe actionability.
6. Evidence reliability.
7. Patient facing wording risk.

## Safety statement

The resource is designed to identify development useful failure mechanisms. It does not provide medical advice and does not certify any model for clinical use.

## Release requirement

Before public release:

1. User approval is required.
2. Public release candidate folder must exclude internal files.
3. Final audit must pass.
4. Clinical review status must be stated accurately.
5. A public repository URL should be added to citation metadata after the repository exists.
