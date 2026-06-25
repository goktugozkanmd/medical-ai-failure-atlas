# Multilingual Medical Intelligence Cross Language Negation Audience Controls v0.1

Date: 2026 06 25

Status: ready for local repo review only

## Purpose

This report checks whether English and Turkish ASCII variants preserve negation boundaries and audience role boundaries.

It blocks cross language negation inversion when one language turns cannot prove into can prove, turns does not rule out into can rule out, or softens a warning.

It also blocks audience role drift when a public wording row shifts toward a patient reader, clinician reader, or model route owner.

The controls use synthetic rows only. They contain no patient data and make no diagnosis, treatment instruction, clinical validation, clinical deployment, model ranking, partner, or institutional claim.

## Score Summary

1. Control rows: 12.
2. Expected pass controls: 6.
3. Expected fail controls: 6.
4. Observed pass controls: 6.
5. Observed blocked controls: 6.
6. Source candidate coverage count: 6.
7. Source row coverage count: 6.

## Cross Language Signal Counts

1. `english_negation_inverted`: declared 1, detected 1.
2. `turkish_negation_inverted`: declared 1, detected 1.
3. `warning_softened`: declared 1, detected 1.
4. `patient_audience_shift`: declared 1, detected 1.
5. `clinician_audience_shift`: declared 1, detected 1.
6. `model_audience_shift`: declared 1, detected 1.

## Reviewer Triage

Does either language invert a negation, soften a warning, or shift the audience role to patient, clinician, or model.

Triage order:

1. `english_negation_inverted`
2. `turkish_negation_inverted`
3. `warning_softened`
4. `patient_audience_shift`
5. `clinician_audience_shift`
6. `model_audience_shift`

## Release Boundary

This report supports repo local review only. It does not clear text for patient care, clinical advice, translation clearance, audience role clearance, clinical validation, clinical deployment, model comparison, institutional use, or external publication.

Boundary note: not score certification, not source truth certification, not clinical validation, not clinical deployment, not translation clearance, not audience role clearance, and not external publication clearance.

## Validation Command

`make multilingual_medical_intelligence_cross_language_negation_audience_controls`

Direct check:

`python3 scripts/score_multilingual_medical_intelligence_cross_language_negation_audience_controls_v0_1_20260625.py --check`

## Exact Next Action

Add cross language source recency and applicability controls so translated variants preserve date, population, setting, and applicability limits before public reuse.
