# Medical AI Safety Field Kit Public Call

Date: 2026 06 19

Status: public flagship call for clinical and technical reviewers.

This is the public front door for the Medical AI Safety Field Kit. It turns the existing safety materials into one visible call for reviewers, builders, clinicians, health informatics teams, hospital quality teams, Turkish language reviewers, and open model maintainers.

## Challenge statement

Medical AI projects should not ask for trust until they can explain source support, data fitness, use boundary, human review role, Turkish context risk, and failure reporting route.

This call asks the field to attack those weak points in public. Strong objections are useful. Missing failure modes are useful. Reviewer comments are useful. Silent internal polish is not enough.

## What this field kit unifies

### FK001: TR MedLLM SafetyBench

Public ask: Review Turkish medical wording risk, specialty coverage gaps, and unsafe benchmark interpretation.

Twenty minute action: Comment with one Turkish medical term that can change meaning across context.

### FK002: Medical AI Failure Atlas Global

Public ask: Add failure modes that are clinically coherent but free of patient data.

Twenty minute action: Comment with one failure mode title and the harm pathway it tests.

### FK003: Turkish Clinical AI Assurance Lab

Public ask: Challenge the field readiness checklist for hospital quality and safety use.

Twenty minute action: Comment with one missing governance gate.

### FK004: SourceCheckup Medical

Public ask: Review whether a claim has enough source support before it is public facing.

Twenty minute action: Comment with one medical AI claim that needs a source support check.

### FK005: Clinician AI Literacy Academy Turkiye

Public ask: Review the clinician literacy flow for practical teaching value.

Twenty minute action: Comment with one clinician misconception that should be taught early.

### FK006: Health Data Quality and Label Audit Commons

Public ask: Review label quality, dataset boundary, and data fitness checks.

Twenty minute action: Comment with one label audit failure pattern.

## Reviewer roles we want now

R001. Clinician reviewer: Find clinical nonsense, missing safety context, and unrealistic workflow assumptions.

R002. Health informatics reviewer: Find weak data fitness, source support, terminology, and governance assumptions.

R003. Hospital quality reviewer: Find missing readiness gates before any public trust language.

R004. Open model maintainer: Find ways benchmark language can be misused as ranking or clinical proof.

R005. Turkish language reviewer: Find Turkish medical wording that changes meaning or safety boundary.

R006. Source support reviewer: Find unsupported claims and propose the minimum evidence needed.

## How to contribute in public

1. Pick one reviewer role.
2. Pick one platform lane.
3. Comment with one concrete objection, missing safety check, failure mode, source support gap, Turkish wording risk, or field readiness gap.
4. Keep examples synthetic and free of patient data.
5. Do not submit diagnosis, treatment, private clinical text, protected data, institutional statements, partner statements, or clinical deployment claims.

## What a useful comment looks like

Role: clinician reviewer.

Lane: Medical AI Failure Atlas Global.

Concern: this failure mode needs a clearer human review trigger before any public safety claim.

Suggested fix: add a release gate that blocks public wording until the reviewer can state the clinical action boundary.

## Public boundaries

1. No patient data.
2. No clinical validation claim.
3. No clinical deployment claim.
4. No diagnosis or treatment advice.
5. No benchmark ranking.
6. No score certification.
7. No source truth certification.
8. No partner claim.
9. No institution claim.
10. No endorsement claim.
11. No formal application claim.
12. No payment or terms acceptance.

## Start state checked before build

Live BAGLAM2, portfolio trackers, active Gmail outreach threads, and targeted Gmail searches were checked before this package. The only inbound state remains an earlier acknowledgement. No new substantive route owner reply was found before this public call was built.

## Maintainer command

Run:

```bash
make medical_ai_safety_field_kit_public_call
```
