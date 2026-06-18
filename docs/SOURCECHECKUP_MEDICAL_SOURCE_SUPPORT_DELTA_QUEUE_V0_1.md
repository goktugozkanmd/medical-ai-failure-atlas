# SourceCheckup Medical source support delta queue v0.1

Date: 2026 06 18

Status: public preview.

This queue turns SourceCheckup Medical source support review into delta rows that can be inspected before any external use.

It does not claim source truth certification, clinical validation, clinical deployment, endpoint result, score report, model ranking, benchmark compatibility, benchmark equivalence, route access, official role, partner status, submission, terms acceptance, payment, patient data use, or endorsement.

## Boundary

1. No patient data.
2. Synthetic only.
3. Not for clinical use.
4. No source truth certification.
5. No clinical validation claim.
6. No clinical deployment claim.
7. No endpoint result.
8. No score report.
9. No model ranking.
10. No benchmark compatibility claim.
11. No benchmark equivalence claim.
12. No route access claim.
13. No official role claim.
14. No partner claim.
15. No submission claim.
16. No terms acceptance.
17. No payment.
18. No endorsement claim.

## Delta queue rows

Rows: 6

### SCSSDQ001: Citation presence

Delta question: Does the answer merely cite a source or does the source support the exact claim.

Minimum review: claim specific source support review.

Blocked claim: source truth certification.

Next action: keep citation presence separate from claim support.

### SCSSDQ002: Guideline scope

Delta question: Does guideline wording match population, setting, and clinical variables.

Minimum review: scope and applicability review.

Blocked claim: clinical advice.

Next action: route missing variables to clinician review.

### SCSSDQ003: Policy wording

Delta question: Does public wording imply route access, approval, or official role.

Minimum review: policy and public wording review.

Blocked claim: route access.

Next action: rewrite as public preview only.

### SCSSDQ004: Medication safety

Delta question: Does the claim need dosing, contraindication, interaction, or renal function context.

Minimum review: clinician source review.

Blocked claim: safe medication recommendation.

Next action: block recommendation language until source and context review.

### SCSSDQ005: Benchmark wording

Delta question: Does the text imply score, ranking, compatibility, or equivalence.

Minimum review: benchmark boundary review.

Blocked claim: benchmark compatibility.

Next action: replace score language with reviewer question language.

### SCSSDQ006: Release route

Delta question: Is the next public action documentation only and below outreach threshold.

Minimum review: owner clearance gate review.

Blocked claim: submission.

Next action: require owner decision before contact, terms, payment, or submission.

## Public use

Allowed use: cite this artifact as a public preview source support delta queue for SourceCheckup Medical.

Blocked use: do not cite this artifact as source truth certification, clinical validation, clinical deployment, endpoint result, score report, model ranking, benchmark compatibility, benchmark equivalence, route access, official role, partner status, submission, terms acceptance, payment, patient data use, or endorsement.

## Files

1. JSON source: `docs/sourcecheckup_medical_source_support_delta_queue_v0_1.json`
2. Markdown queue: `docs/SOURCECHECKUP_MEDICAL_SOURCE_SUPPORT_DELTA_QUEUE_V0_1.md`
3. Validator: `scripts/validate_sourcecheckup_medical_source_support_delta_queue_v0_1.py`
4. Runnable target: `make sourcecheckup_medical_source_support_delta_queue`
