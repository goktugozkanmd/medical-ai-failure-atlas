# Contributing

Status: internal draft for future public release.

## Scope

This project is a physician authored synthetic medical AI evaluation resource.

It is not clinical advice.

It is not a clinical validation study.

It must not include patient data.

## Contribution rules

1. Do not submit real patient cases.
2. Do not include protected health information.
3. Do not include dates, locations, identifiers, or rare details from real patients.
4. Use synthetic cases only.
5. Mark every case with data provenance.
6. Keep clinical safety wording conservative.
7. Do not claim a model is safe or unsafe overall from one case.
8. Do not add external model outputs unless platform terms allow redistribution.
9. Do not add clinical advice for patients.
10. Do not remove release boundary notes without review.

## Case proposal minimum fields

1. Scenario ID.
2. Clinical domain.
3. Care setting.
4. Synthetic patient summary.
5. Task for model.
6. Expected safety focus.
7. Failure mechanism tags.
8. Missing variables that determine safe action.
9. Patient facing risk if wording is copied.
10. Review question for a clinician.

## Review status wording

Allowed:

`physician authored synthetic draft pending final clinician review`

Not allowed unless explicitly confirmed:

`clinician validated`

Not allowed:

`safe for clinical use`

## External communication

Do not open external issues, pull requests, discussions, or emails from this project without explicit user approval and final audit.
