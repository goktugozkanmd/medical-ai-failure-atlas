# Label audit example dashboard v0.1

Status: generated public preview.

Date: 2026 06 17

This dashboard summarizes the public synthetic label audit example intake rows by reviewer role, audit row, review state, and blocked public claim type.

It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.

## Summary

Label audit example dashboard rows: 5

Reviewer roles represented: 4

Audit rows represented: 5

Review states represented: 4

Blocked public claim types represented: 5

## Role summary

1. `LAR001` Synthetic provenance reviewer: 1

1. `LAR002` Label definition reviewer: 1

1. `LAR003` Pilot subset reviewer: 1

1. `LAR004` Public release boundary reviewer: 2

## Audit row summary

1. `LAA001` Synthetic provenance audit: 1

1. `LAA002` Label definition lock audit: 1

1. `LAA003` Pilot inter rater subset audit: 1

1. `LAA004` Raw output exclusion audit: 1

1. `LAA005` Public release boundary audit: 1

## Review state summary

1. `needs_adjudication`: 1

1. `needs_clinician_review`: 1

1. `not_for_public_summary`: 2

1. `synthetic_preview_only`: 1

## Blocked public claim types

1. clinical validation claim: 1

1. dataset quality proof claim: 1

1. population performance claim: 1

1. raw model output release claim: 1

1. real care record coverage claim: 1

## Dashboard rows

### LAE001: Synthetic provenance overclaim

Reviewer role: `LAR001` Synthetic provenance reviewer

Audit row: `LAA001` Synthetic provenance audit

Review state: `synthetic_preview_only`

Blocked public claim type: real care record coverage claim

Required check count: 4

### LAE002: Label definition drift

Reviewer role: `LAR002` Label definition reviewer

Audit row: `LAA002` Label definition lock audit

Review state: `needs_clinician_review`

Blocked public claim type: clinical validation claim

Required check count: 4

### LAE003: Pilot subset overinterpretation

Reviewer role: `LAR003` Pilot subset reviewer

Audit row: `LAA003` Pilot inter rater subset audit

Review state: `needs_adjudication`

Blocked public claim type: population performance claim

Required check count: 4

### LAE004: Raw output exclusion boundary

Reviewer role: `LAR004` Public release boundary reviewer

Audit row: `LAA004` Raw output exclusion audit

Review state: `not_for_public_summary`

Blocked public claim type: raw model output release claim

Required check count: 4

### LAE005: Dataset quality proof boundary

Reviewer role: `LAR004` Public release boundary reviewer

Audit row: `LAA005` Public release boundary audit

Review state: `not_for_public_summary`

Blocked public claim type: dataset quality proof claim

Required check count: 4

## Public files

1. Intake rows: `docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md`
2. Intake JSON: `docs/label_audit/label_audit_example_intake_v0_1.json`
3. Dashboard JSON: `docs/label_audit/label_audit_example_dashboard_v0_1.json`
4. Reviewer role table: `docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md`
5. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`

## Runnable check

Run:

```bash
make label_audit_dashboard
```
