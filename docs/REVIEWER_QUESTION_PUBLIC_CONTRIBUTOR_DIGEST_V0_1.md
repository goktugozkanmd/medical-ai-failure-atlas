# Reviewer question public contributor digest v0.1

Status: generated public preview.

Date: 2026 06 17

This digest gives contributors a short orientation path for using the reviewer question release index before opening or updating a synthetic SourceCheckup or Failure Atlas issue.

It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.

## Summary

Digest step rows: 5

Release index surface rows represented: 9

Issue history rows represented: 11

Digest decision: `ready_for_public_preview`

## Contributor steps

### RQCD001

Step name: Read the reviewer question release index

Public file: `docs/REVIEWER_QUESTION_PUBLIC_RELEASE_INDEX_V0_1.md`

Contributor action: start from the public route index

Digest status: `included_in_public_contributor_digest`

Boundary: synthetic only and not for clinical use

### RQCD002

Step name: Choose the matching reviewer question surface

Public file: `docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md`

Contributor action: select a source support, escalation, medication safety, missing context, policy wording, or warning sign question

Digest status: `included_in_public_contributor_digest`

Boundary: synthetic only and not for clinical use

### RQCD003

Step name: Match an intake example

Public file: `docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md`

Contributor action: match the proposed contribution to a synthetic intake example

Digest status: `included_in_public_contributor_digest`

Boundary: synthetic only and not for clinical use

### RQCD004

Step name: Check wording boundaries

Public file: `docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md`

Contributor action: avoid score, compatibility, endpoint, patient data, clinical validation, and endorsement wording

Digest status: `included_in_public_contributor_digest`

Boundary: synthetic only and not for clinical use

### RQCD005

Step name: Run the release index check

Public file: `Makefile`

Contributor action: run make reviewer_question_release_index before opening or updating an issue

Digest status: `included_in_public_contributor_digest`

Boundary: synthetic only and not for clinical use

## Runnable check

Run:

```bash
make reviewer_question_contributor_digest
```

## Next safe public action

Add a reviewer question maintainer release candidate summary without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.
