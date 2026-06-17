# Reviewer question intake triage board v0.1

Status: generated public preview.

Date: 2026 06 17

This board turns synthetic reviewer question intake examples into maintainer actions, owner roles, triage status values, and next public wording decisions.

It is not clinical advice, not patient data, not raw model output, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.

## Summary

Maintainer triage rows: 4

Owner roles represented: 4

Maintainer actions represented: 4

Public wording decisions represented: 4

Triage status values represented: 1

## Owner role summary

1. `RQTR001 Source evidence reviewer`: 1

1. `RQTR002 Policy wording reviewer`: 1

1. `RQTR003 Escalation boundary reviewer`: 1

1. `RQTR004 Medication safety reviewer`: 1

## Triage status summary

1. `ready_for_maintainer_review`: 4

## Triage rows

### RQINT001: sourcecheckup_review

Reviewer question id: `BSRQ001`

Owner role: `RQTR001` Source evidence reviewer

Review state: `synthetic_preview_only`

Blocked public claim type: source truth certification

Maintainer action: route to source support queue

Triage status: `ready_for_maintainer_review`

Public wording decision: say locator is not evidence

Next public surface: SourceCheckup public contributor issue

Track A value: Turkish medical LLM source support discipline

Track B value: open source SourceCheckup intake example

### RQINT002: sourcecheckup_review

Reviewer question id: `BSRQ002`

Owner role: `RQTR002` Policy wording reviewer

Review state: `synthetic_preview_only`

Blocked public claim type: official policy proof

Maintainer action: route to policy wording review

Triage status: `ready_for_maintainer_review`

Public wording decision: say policy source is required

Next public surface: SourceCheckup public contributor issue

Track A value: Turkish institutional wording discipline

Track B value: public policy wording intake example

### RQINT003: synthetic_failure_case

Reviewer question id: `BSRQ005`

Owner role: `RQTR003` Escalation boundary reviewer

Review state: `synthetic_preview_only`

Blocked public claim type: false reassurance safety proof

Maintainer action: route to escalation boundary review

Triage status: `ready_for_maintainer_review`

Public wording decision: say escalation remains visible

Next public surface: Failure Atlas case intake checklist

Track A value: Turkish clinician literacy for escalation boundaries

Track B value: Failure Atlas intake example for realistic scenario review

### RQINT004: synthetic_failure_case

Reviewer question id: `BSRQ006`

Owner role: `RQTR004` Medication safety reviewer

Review state: `synthetic_preview_only`

Blocked public claim type: clinical advice

Maintainer action: route to medication safety review

Triage status: `ready_for_maintainer_review`

Public wording decision: say individualized medication advice is blocked

Next public surface: Failure Atlas case intake checklist

Track A value: Turkish medication safety review example

Track B value: Failure Atlas medication safety intake example

## Public files

1. Triage board JSON: `docs/reviewer_question_intake_triage_board_v0_1.json`
2. Intake examples: `docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md`
3. Intake examples JSON: `docs/reviewer_question_intake_examples_v0_1.json`
4. SourceCheckup contributor guide: `docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md`
5. Failure Atlas checklist: `failure_atlas/public/CASE_INTAKE_CHECKLIST_V0_1.md`

## Runnable check

Run:

```bash
make reviewer_question_intake_triage
```

## Next safe public action

Add a public wording decision log for reviewer question intake triage without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.
