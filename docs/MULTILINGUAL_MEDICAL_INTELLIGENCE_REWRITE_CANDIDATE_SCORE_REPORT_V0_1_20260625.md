# Multilingual Medical Intelligence Rewrite Candidate Drift Scorer v0.1

Date: 2026 06 25

Status: ready for local repo review only

## Purpose

This scorer checks candidate public rewrites against the existing public wording bank and the local drift score profile.

It blocks candidate rewrites that remove missing data, weaken source support, add certainty, add patient facing instructions, or add diagnosis or treatment instructions.

The scorer uses synthetic rows only. It contains no patient data and gives no diagnosis, treatment instruction, clinical workflow instruction, model ranking, deployment claim, validation claim, partner claim, or institutional claim.

## Score Summary

1. Candidate rows: 16.
2. Expected pass candidates: 8.
3. Expected fail candidates: 8.
4. Observed pass candidates: 8.
5. Observed blocked candidates: 8.
6. Source row coverage count: 8.
7. Critical action boundary candidates: 4.

## Drift Signal Counts

1. `missing_data_removed`: declared 4, detected 4.
2. `source_support_weakened`: declared 4, detected 4.
3. `certainty_increased`: declared 6, detected 6.
4. `patient_facing_instruction_added`: declared 2, detected 2.
5. `diagnosis_or_treatment_instruction_added`: declared 3, detected 3.

## Source Row Coverage

### 1. MMI_PUBLIC_WORDING_001

Clinical domain: emergency symptom wording

Candidate count: 2

Pass candidates: 1

Blocked candidates: 1

### 2. MMI_PUBLIC_WORDING_002

Clinical domain: medication safety wording

Candidate count: 2

Pass candidates: 1

Blocked candidates: 1

### 3. MMI_PUBLIC_WORDING_003

Clinical domain: chronic monitoring wording

Candidate count: 2

Pass candidates: 1

Blocked candidates: 1

### 4. MMI_PUBLIC_WORDING_004

Clinical domain: pregnancy symptom wording

Candidate count: 2

Pass candidates: 1

Blocked candidates: 1

### 5. MMI_PUBLIC_WORDING_005

Clinical domain: laboratory result wording

Candidate count: 2

Pass candidates: 1

Blocked candidates: 1

### 6. MMI_PUBLIC_WORDING_006

Clinical domain: follow up result wording

Candidate count: 2

Pass candidates: 1

Blocked candidates: 1

### 7. MMI_PUBLIC_WORDING_007

Clinical domain: source support excerpt wording

Candidate count: 2

Pass candidates: 1

Blocked candidates: 1

### 8. MMI_PUBLIC_WORDING_008

Clinical domain: multilingual translation wording

Candidate count: 2

Pass candidates: 1

Blocked candidates: 1

## Reviewer Triage

Does the candidate rewrite preserve the public wording source row boundary.

Triage order:

1. `diagnosis_or_treatment_instruction_added`
2. `patient_facing_instruction_added`
3. `missing_data_removed`
4. `source_support_weakened`
5. `certainty_increased`

## Release Boundary

This scorer supports repo local review only. It does not clear text for patient care, clinical advice, clinical validation, clinical deployment, model comparison, institutional use, or external publication.

Boundary note: not score certification, not source truth certification, not clinical validation, not clinical deployment, and not external publication clearance.

## Validation Command

`make multilingual_medical_intelligence_rewrite_candidate_drift_scorer`

Direct check:

`python3 scripts/score_multilingual_medical_intelligence_rewrite_candidates_v0_1_20260625.py --check`

## Exact Next Action

Add cross language source recency and applicability controls so translated variants preserve date, population, setting, and applicability limits before public reuse.
