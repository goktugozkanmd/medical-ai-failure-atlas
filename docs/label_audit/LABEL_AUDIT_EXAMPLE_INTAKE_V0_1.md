# Label audit example intake v0.1

Status: generated public preview.

Date: 2026 06 17

This file gives synthetic label audit example intake rows for public maintainer review.

It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.

## Summary

Label audit examples: 5

Synthetic scenario rows: 150

Prompt rows: 70

Pilot inter rater rows: 24

Turkish synthetic risk rows: 14

Source claim review queue rows: 12

## Public links

1. Public issue template: `.github/ISSUE_TEMPLATE/label_audit_review.yml`
2. Public contributor guide: `docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md`
3. Reviewer role table: `docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md`
4. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`
5. JSON source: `docs/label_audit/label_audit_example_intake_v0_1.json`

## Example rows

### LAE001: Synthetic provenance overclaim

Audit surface: synthetic provenance

Suggested reviewer role: `LAR001`

Linked audit row: `LAA001`

Exact boundary to review: Public text implies real care record coverage or unclear provenance.

Review state: `synthetic_preview_only`

Proposed public action: `rewrite_public_wording`

Required checks:

1. `synthetic_provenance`

2. `patient_data_absence`

3. `direct_identifier_absence`

4. `public_boundary_state`

### LAE002: Label definition drift

Audit surface: label definition lock

Suggested reviewer role: `LAR002`

Linked audit row: `LAA002`

Exact boundary to review: A label explanation no longer matches the locked rubric version.

Review state: `needs_clinician_review`

Proposed public action: `route_to_clinician_review`

Required checks:

1. `label_lock_match`

2. `rubric_version_match`

3. `unsure_rule_state`

4. `clinical_validation_boundary`

### LAE003: Pilot subset overinterpretation

Audit surface: pilot inter rater subset

Suggested reviewer role: `LAR003`

Linked audit row: `LAA003`

Exact boundary to review: A 24 row pilot subset is framed as if it measured population performance.

Review state: `needs_adjudication`

Proposed public action: `add_protocol_testing_wording`

Required checks:

1. `pilot_subset_framing`

2. `no_agreement_statistic`

3. `sampling_reason`

4. `no_population_prevalence`

### LAE004: Raw output exclusion boundary

Audit surface: raw output exclusion

Suggested reviewer role: `LAR004`

Linked audit row: `LAA004`

Exact boundary to review: A public summary could be read as releasing raw model outputs.

Review state: `not_for_public_summary`

Proposed public action: `keep_raw_outputs_withheld`

Required checks:

1. `raw_output_exclusion`

2. `redistribution_terms_state`

3. `private_output_absence`

4. `public_release_boundary`

### LAE005: Dataset quality proof boundary

Audit surface: public release boundary

Suggested reviewer role: `LAR004`

Linked audit row: `LAA005`

Exact boundary to review: A public card sounds as if it proves dataset quality or readiness.

Review state: `not_for_public_summary`

Proposed public action: `block_stronger_public_claim`

Required checks:

1. `dataset_quality_proof_boundary`

2. `clinical_deployment_boundary`

3. `model_ranking_boundary`

4. `formal_approval_boundary`

## Boundary checks

1. The examples are synthetic only.
2. Patient data is not used.
3. Raw model outputs are not released.
4. The examples do not prove dataset quality.
5. The examples do not create clinical validation.
6. The examples do not support clinical deployment.
7. The examples do not rank models.
8. The examples do not claim regulatory approval.
9. The examples do not claim official endorsement.

## Runnable check

Run:

```bash
make label_audit_examples
```
