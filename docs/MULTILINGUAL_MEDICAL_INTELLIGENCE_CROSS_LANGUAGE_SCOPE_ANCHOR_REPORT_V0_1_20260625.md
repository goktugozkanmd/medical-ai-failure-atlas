# Multilingual Medical Intelligence Cross Language Scope Anchor Controls v0.1

Date: 2026 06 25

Status: ready for local repo review only

## Purpose

This report checks whether English and Turkish ASCII variants preserve missing variable anchors, actor role anchors, action boundary anchors, and local context anchors in the same record.

It blocks cross language scope anchor drift when one language erases missing variables, changes the actor role, expands or removes the action boundary, or detaches local context.

It keeps missing variables, actor role, action boundary, and local review context attached to the same synthetic source record.

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

1. `english_missing_variable_erased`: declared 1, detected 1.
2. `turkish_missing_variable_erased`: declared 1, detected 1.
3. `actor_role_changed`: declared 1, detected 1.
4. `action_boundary_expanded`: declared 1, detected 1.
5. `action_boundary_removed`: declared 1, detected 1.
6. `local_context_detached`: declared 1, detected 1.

## Reviewer Triage

Does either language erase missing variables, change the actor role, expand or remove the action boundary, or detach local context from the same record.

Triage order:

1. `english_missing_variable_erased`
2. `turkish_missing_variable_erased`
3. `actor_role_changed`
4. `action_boundary_expanded`
5. `action_boundary_removed`
6. `local_context_detached`

## Release Boundary

This report supports repo local review only. It does not clear text for patient care, clinical advice, translation clearance, scope anchor clearance, clinical validation, clinical deployment, model comparison, institutional use, or external publication.

Boundary note: not score certification, not source truth certification, not clinical validation, not clinical deployment, not translation clearance, not scope anchor clearance, and not external publication clearance.

## Validation Command

`make multilingual_medical_intelligence_cross_language_scope_anchor_controls`

Direct check:

`python3 scripts/score_multilingual_medical_intelligence_cross_language_scope_anchor_controls_v0_1_20260625.py --check`

## Exact Next Action

Add cross language source recency and applicability controls so translated variants preserve date, population, setting, and applicability limits before public reuse.
