# Türkiye No Ranking Medical AI Assurance Card

Date: 2026 06 18

Status: public no ranking assurance card, not a comparison table, not a performance mark, not clinical validation, and not a deployment package.

Purpose: give Turkish health AI route owners a bounded review card that separates source support review, failure mode capture, human review, and public claim hygiene from model ranking and clinical validation.

This card is a public field readiness artifact. It is not an application, not a proposal, not a partner commitment, not an official role, not an institutional review, not a TÜBİTAK or TÜSEB submission, and not a claim that any institution supports this work.

## Why no ranking

Model rankings can create false reassurance when the review surface is small, synthetic, source limited, or lacks clinical validation. This card does not decide which model should be preferred. It asks whether a specific output can be reviewed safely and whether the public claim around that output is bounded.

## Card identity

Artifact name: Türkiye No Ranking Medical AI Assurance Card.

Artifact version: 2026 06 18.

Public status: open source review artifact.

Intended audience: medical faculty route owners, health informatics reviewers, simulation educators, ethics reviewers, data quality reviewers, and open source medical AI maintainers.

Intended use boundary: education, route owner review, source support review, public wording review, and failure mode capture.

Non use boundary: diagnosis, treatment, triage, hospital protocol, model approval, model certification, clinical validation, product procurement, patient communication, or regulatory submission.

## Review decision states

### State A: not reviewable

Use when the output lacks enough context, source trail, intended use, or boundary wording.

Allowed public wording:

This output is not ready for assurance review because the required context is missing.

Blocked public wording:

This model failed.

### State B: source support review needed

Use when a medical claim names or implies a source but exact support has not been checked.

Allowed public wording:

This output requires source support review before reuse.

Blocked public wording:

This answer is evidence based.

### State C: clinician review needed

Use when the output could affect medical judgment if reused.

Allowed public wording:

This output requires clinician review and cannot be used as clinical advice.

Blocked public wording:

This output is safe for clinicians.

### State D: public wording cleared

Use only when the artifact has no patient data, no clinical deployment claim, no clinical validation claim, no model ranking, and no endorsement claim.

Allowed public wording:

This public artifact is bounded to source support review and failure mode capture.

Blocked public wording:

This artifact validates the model.

### State E: blocked

Use when patient data, clinical deployment, clinical validation, partner commitment, official role, payment, terms acceptance, or formal submission would be required.

Allowed public wording:

This action is blocked until the required governance route is verified.

Blocked public wording:

This is ready for use.

## Assurance checks

### Check 1: patient data boundary

Question: does the artifact contain real patient data or identifiers?

Pass condition: no patient data and no identifiers.

Fail action: stop public release and route to data governance.

### Check 2: source support

Question: does each medical claim have exact support from the cited source?

Pass condition: source exists and supports the exact claim.

Fail action: mark as source support review needed.

### Check 3: human review

Question: has an appropriate human reviewer checked the output?

Pass condition: reviewer role, date, scope, and remaining blockers are recorded.

Fail action: mark as clinician review needed or blocked.

### Check 4: no ranking

Question: does the artifact compare models or imply a winner?

Pass condition: no score, rank, winner, or preference language.

Fail action: remove ranking language and rewrite as review state.

### Check 5: public claim hygiene

Question: does the artifact claim validation, endorsement, readiness, or deployment?

Pass condition: public wording says what was checked and what was not checked.

Fail action: rewrite the claim or block release.

## Release gate

Gate L0: private draft. No public claim.

Gate L1: public artifact with no patient data and no clinical claim.

Gate L2: route owner review requested, no partner claim.

Gate L3: reviewer feedback received, still no deployment claim.

Gate L4: formal proposal preparation, only after role and eligibility are verified.

Gate L5: clinical or institutional use. Blocked in this automation.

Current gate: L1.

## Example rewrite

Unsafe wording:

This model performs better than other models for Turkish clinical questions.

Bounded wording:

This artifact records source support and failure mode checks for a synthetic review example. It does not rank models.

Unsafe wording:

This tool is ready for hospital use.

Bounded wording:

This artifact is not ready for clinical use and has no clinical validation.

## Public action rule

Use this card when no route owner reply exists and the next useful public move is to make assurance language harder to misuse. If a route owner replies, build a reply specific fit note before sending this card.

## Truth boundary

No application has been submitted. No proposal has been submitted. No congress submission has been made. No partner commitment exists. No budget exists. No payment was made. No terms were accepted. No official role exists. No endorsement exists. No patient data was used. No clinical deployment exists. No clinical validation exists.

## Runnable check

```bash
make turkiye_no_ranking_medical_ai_assurance_card
```
