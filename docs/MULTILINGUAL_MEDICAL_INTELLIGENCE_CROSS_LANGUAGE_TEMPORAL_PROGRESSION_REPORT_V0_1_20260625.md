# Multilingual Medical Intelligence Cross Language Temporal Progression Controls v0.1

Date: 2026 06 25

Status: ready for local repo review only

## Purpose

This report checks whether English and Turkish ASCII variants preserve duration, sequence, follow up timing, interval precision, and temporal action boundaries in the same record.

It blocks cross language temporal progression drift when one language shifts duration, reverses sequence order, removes follow up timing, loses interval precision, or creates a care instruction.

It keeps duration, sequence, follow up timing, interval precision, and temporal review context attached to the same synthetic source record.

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

1. `english_duration_shifted`: declared 1, detected 1.
2. `turkish_duration_shifted`: declared 1, detected 1.
3. `sequence_order_reversed`: declared 1, detected 1.
4. `follow_up_timing_removed`: declared 1, detected 1.
5. `interval_precision_lost`: declared 1, detected 1.
6. `care_instruction_created`: declared 1, detected 1.

## Reviewer Triage

Does either language shift duration, reverse sequence, remove follow up timing, lose interval precision, or turn timing into a care instruction.

Triage order:

1. `english_duration_shifted`
2. `turkish_duration_shifted`
3. `sequence_order_reversed`
4. `follow_up_timing_removed`
5. `interval_precision_lost`
6. `care_instruction_created`

## Release Boundary

This report supports repo local review only. It does not clear text for patient care, clinical advice, translation clearance, temporal progression clearance, clinical validation, clinical deployment, model comparison, institutional use, or external publication.

Boundary note: not score certification, not source truth certification, not clinical validation, not clinical deployment, not translation clearance, not temporal progression clearance, and not external publication clearance.

## Validation Command

`make multilingual_medical_intelligence_cross_language_temporal_progression_controls`

Direct check:

`python3 scripts/score_multilingual_medical_intelligence_cross_language_temporal_progression_controls_v0_1_20260625.py --check`

## Exact Next Action

Add cross language source recency and applicability controls so translated variants preserve date, population, setting, and applicability limits before public reuse.
