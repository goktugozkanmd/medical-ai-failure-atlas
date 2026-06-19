# Medical AI Safety Field Kit Reviewer Start Here

Date: 2026 06 19

Status: public entry page for fast reviewer action.

This page is the shortest public route into the Medical AI Safety Field Kit. It is for people who want to help by finding weak source support, unsafe benchmark wording, Turkish clinical language risk, missing readiness gates, or unclear reviewer roles.

## Pick a route

1. Public intake: [issue 149](https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149)
2. Source support starter: [issue 150](https://github.com/v0id-lab/medical-ai-failure-atlas/issues/150)
3. Turkish wording starter: [issue 151](https://github.com/v0id-lab/medical-ai-failure-atlas/issues/151)
4. Safe Failure Card issue template: [template](https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/.github/ISSUE_TEMPLATE/safe_failure_card_objection.yml)
5. BRIDGE public route: [issue 4 comment](https://github.com/YLab-Open/BRIDGE/issues/4#issuecomment-4754548346)

## Fast reviewer paths

Clinician reviewer: start with issue 151 and comment on one Turkish clinical phrase that could change urgency, certainty, patient instruction, or clinician responsibility.

Source support reviewer: start with issue 150 and comment on one medical AI claim where a visible source link still does not support the exact wording.

Benchmark maintainer: start with the BRIDGE public route and comment on wording that could turn a benchmark signal into a ranking, safety proof, or deployment claim.

Hospital quality reviewer: start with issue 149 and name one readiness gate that should block public trust language.

Open model maintainer: start with the Safe Failure Card template and add one synthetic reviewer objection that can be checked without patient data.

Turkish language reviewer: start with issue 151 and suggest safer Turkish wording or a review gate.

## Comment shape

Use this shape when possible:

```text
Lane:
Risk:
Fix:
```

Good comments are short, concrete, and critical. They do not need to solve the full system. One clear objection is useful.

## Boundaries

Do not submit patient data, private clinical text, diagnosis advice, treatment advice, clinical validation claims, clinical deployment claims, benchmark ranking claims, score certification claims, source truth claims, partner claims, institution claims, endorsement claims, funding requests, payment claims, or terms claims.

This is not a request for study approval, authorship, data collection, clinical endorsement, formal institutional approval, clinical deployment, or patient review.

## Maintainer next action

Route useful comments into the public objection ledger, then turn repeated objections into starter issues or Safe Failure Cards.

## Maintainer command

Run:

```bash
make medical_ai_safety_field_kit_reviewer_start_here
```
