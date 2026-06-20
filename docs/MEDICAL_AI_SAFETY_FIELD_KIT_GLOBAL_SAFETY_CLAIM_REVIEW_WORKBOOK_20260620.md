# Medical AI Safety Field Kit Global Safety Claim Review Workbook

Date: 2026 06 20

Status: public workbook for bounded safety claim review.

This workbook is the main public action surface for the Medical AI Safety Field Kit. It turns scattered safety concerns into one practical review route for medical AI wording, source support, benchmark misuse, Turkish medical language, hospital readiness, data quality, reviewer roles, and governance claims.

The goal is simple: make weak safety language easier to attack before it becomes trusted public language.

## Boundary page

Use this workbook only with synthetic or public examples.

Do not use patient data, private clinical text, diagnosis advice, treatment advice, raw private model output, hidden prompts, private emails, institution details, unpublished clinical material, clinical validation claims, clinical deployment claims, benchmark ranking claims, score certification claims, source truth claims, partner claims, institution approval claims, endorsement claims, funding requests, payment claims, terms claims, TBYS action, PRODIS action, formal application text, budget action, procurement claims, or private authority claims.

This workbook is not clinical advice, clinical validation, deployment readiness, institution approval, partner status, endorsement, funding, payment, terms acceptance, TBYS action, PRODIS action, procurement action, or a formal application.

## Public route map

1. Main public intake: https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149
2. Source support starter: https://github.com/v0id-lab/medical-ai-failure-atlas/issues/150
3. Turkish wording starter: https://github.com/v0id-lab/medical-ai-failure-atlas/issues/151
4. Hospital readiness starter: https://github.com/v0id-lab/medical-ai-failure-atlas/issues/152
5. Reviewer start page: https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_REVIEWER_START_HERE_20260619.md

## Claim review matrix

Claim type one: source link becomes source support.

Unsafe claim shape: the answer links a source, so the statement sounds supported.

Missing evidence: the source must support the exact medical wording, not only the broad topic.

Reviewer role: source support reviewer.

Blocked wording: the source confirms this recommendation.

Safer wording: this source is visible, but exact support still needs review.

Issue route: issue 150.

Claim type two: fluent Turkish becomes clinical certainty.

Unsafe claim shape: fluent Turkish wording sounds clinically certain or urgent.

Missing evidence: a Turkish clinical language reviewer must check urgency, certainty, patient instruction, and clinician responsibility.

Reviewer role: Turkish medical language reviewer.

Blocked wording: this Turkish phrasing is clinically safe.

Safer wording: this phrasing is understandable, but the safety meaning still needs review.

Issue route: issue 151.

Claim type three: demo success becomes hospital readiness.

Unsafe claim shape: a public demo sounds ready for hospital workflow use.

Missing evidence: workflow, governance, user role, data, deployment, monitoring, and escalation gates are not cleared.

Reviewer role: hospital quality reviewer.

Blocked wording: ready for hospital use.

Safer wording: public demo only, with hospital readiness not assessed.

Issue route: issue 152.

Claim type four: benchmark score becomes safety proof.

Unsafe claim shape: a benchmark signal sounds like a model is safe or better for clinical work.

Missing evidence: score meaning, task scope, risk class, failure modes, reviewer role, and clinical boundary are not resolved.

Reviewer role: benchmark maintainer.

Blocked wording: best model for medical use.

Safer wording: one benchmark signal, not a safety claim.

Issue route: issue 149.

Claim type five: governance wording becomes approval.

Unsafe claim shape: responsible AI language sounds like an approval or compliance claim.

Missing evidence: approval body, route authority, terms, scope, and decision state are not established.

Reviewer role: governance reviewer.

Blocked wording: approved responsible health AI.

Safer wording: governance concern identified, with approval not claimed.

Issue route: issue 149.

## Safe Failure Card mapping

SFC001 maps to benchmark misuse. Review whether a score is being used as proof of clinical safety.

SFC002 maps to source support. Review whether the visible source supports the exact wording.

SFC003 maps to Turkish wording. Review whether language shifts urgency, certainty, instruction, or responsibility.

SFC004 maps to hospital readiness. Review whether a demo sounds like workflow readiness.

SFC005 maps to synthetic evidence boundary. Review whether a synthetic card is being used as real case evidence.

SFC006 maps to policy wording. Review whether broad policy language becomes patient instruction.

SFC007 maps to data fitness. Review whether public dataset access is treated as medical AI safety fitness.

SFC008 maps to human review role. Review whether a human gate has a named role, trigger, authority, and record.

SFC009 maps to vendor language. Review whether general capability wording becomes medical assurance.

SFC010 maps to sandbox boundary. Review whether route exploration sounds like deployment readiness.

## Synthetic walkthrough

Synthetic public claim:

Our medical AI demo uses public sources, works well in Turkish, and is ready for hospital quality review.

Step one: source support review.

Question: which exact sentence is supported by which source.

Possible objection: the link is visible, but exact support is not shown.

Route: issue 150.

Step two: Turkish wording review.

Question: could the Turkish wording shift urgency or certainty.

Possible objection: the phrase may sound more certain than the evidence allows.

Route: issue 151.

Step three: hospital readiness review.

Question: does demo success sound like hospital workflow readiness.

Possible objection: no workflow, monitoring, escalation, or user role gate is shown.

Route: issue 152.

Step four: release gate review.

Question: should the public claim be blocked, narrowed, or routed to a reviewer.

Possible answer: public demo only. No hospital readiness, clinical validation, or deployment claim.

Route: issue 149.

## Reviewer comment templates

Clinician reviewer:

```text
Lane:
Clinical wording risk:
Missing gate:
Safer wording:
```

Source support reviewer:

```text
Lane:
Source support risk:
Missing evidence:
Safer wording:
```

Turkish language reviewer:

```text
Lane:
Turkish phrase:
Possible meaning shift:
Safer wording:
```

Benchmark maintainer:

```text
Lane:
Benchmark misuse risk:
Missing boundary:
Safer wording:
```

Hospital quality reviewer:

```text
Lane:
Readiness risk:
Missing workflow gate:
Safer wording:
```

Governance reviewer:

```text
Lane:
Governance wording risk:
Missing authority gate:
Safer wording:
```

## Objection counting rule

Only visible third party comments count.

A comment counts only when it comes from a person who is not maintaining this repository and is not posting through a project account.

Maintainer, project account, and controlled seed comments do not count as outside review or external validation.

Do not invent reviewer rows.

Do not count private intent, silent agreement, internal notes, email sends, acknowledgements, or maintainer comments as external review.

A useful objection must name a lane, risk, and missing gate.

## Maintainer closeout rule

For each useful public objection:

1. Link it from issue 149.
2. Route it to one starter lane.
3. Decide whether it becomes a Safe Failure Card, a wording gate, a source support gate, or a reviewer role gate.
4. Record the boundary without claiming validation, approval, endorsement, deployment, partnership, or safety proof.

## Done condition

This workbook is useful when at least one visible third party account that is not maintaining this repository and is not posting through a project account identifies a risk and a missing gate.

Until that happens, this is a public review surface, not evidence of review.

## Maintainer command

Run:

```bash
make medical_ai_safety_field_kit_global_safety_claim_review_workbook
```
