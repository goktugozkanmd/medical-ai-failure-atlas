# Medical AI Safety Field Kit Reviewer Sprint Board

Date: 2026 06 20

Status: public sprint board for one concrete reviewer objection.

This board turns the field kit into a short public sprint. It is for clinicians, hospital quality reviewers, health informatics reviewers, Turkish medical language reviewers, source support reviewers, and open model maintainers who can leave one useful objection without joining any project.

## Sprint target

Get one public objection that improves a safety boundary.

The objection can be small. A missing gate, safer wording, or source support concern is enough.

## Start here

1. Reviewer start page: https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_REVIEWER_START_HERE_20260619.md
2. Main public intake: https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149
3. Source support starter: https://github.com/v0id-lab/medical-ai-failure-atlas/issues/150
4. Turkish wording starter: https://github.com/v0id-lab/medical-ai-failure-atlas/issues/151
5. Hospital readiness starter: https://github.com/v0id-lab/medical-ai-failure-atlas/issues/152

## Pick one lane

Source support lane:

Use issue 150 when a medical AI answer has a source link, but the visible source does not support the exact wording.

Turkish wording lane:

Use issue 151 when a Turkish medical phrase could shift urgency, certainty, patient instruction, or clinician responsibility.

Hospital readiness lane:

Use issue 152 when demo success language could sound like hospital workflow readiness.

Main intake lane:

Use issue 149 when the objection does not fit the three starter lanes.

## Comment shape

Use this shape:

```text
Lane:
Risk:
Missing gate:
Safer wording:
```

## What counts as done

One public comment is enough when it names a risk and a missing gate.

Good comments attack weak wording. They do not need to evaluate a model or solve the full system.

## Maintainer routing

Route each useful comment to one lane:

1. Source support
2. Turkish wording
3. Hospital readiness
4. Benchmark misuse
5. Data quality
6. Reviewer role
7. Governance wording

Then turn repeated objections into a Safe Failure Card, issue template improvement, or public wording gate.

## Boundary

Use synthetic or public examples only.

Do not submit patient data, private clinical text, diagnosis advice, treatment advice, raw private model output, hidden prompts, private emails, institution details, unpublished clinical material, clinical validation claims, clinical deployment claims, benchmark ranking claims, score certification claims, source truth claims, partner claims, institution approval claims, endorsement claims, funding requests, payment claims, terms claims, TBYS action, PRODIS action, formal application text, or procurement claims.

This board is not clinical advice, clinical validation, deployment readiness, institutional approval, partner status, endorsement, funding, payment, terms acceptance, TBYS action, PRODIS action, or a formal application.

## Maintainer command

Run:

```bash
make medical_ai_safety_field_kit_reviewer_sprint_board
```
