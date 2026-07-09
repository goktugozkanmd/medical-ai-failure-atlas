# Label audit reviewer role table v0.1

Status: generated public preview.

Date: 2026 06 16

This table turns health data quality and label audit review into explicit reviewer roles and escalation gate audit rows.

It uses synthetic examples only. It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.

## Summary

Label audit reviewer roles: 4

Label audit escalation gate rows: 5

Synthetic scenario rows: 150

Prompt rows: 70

Pilot inter rater rows: 24

Turkish synthetic risk rows: 14

Source claim review queue rows: 12

## Reviewer roles

### LAR001: Synthetic provenance reviewer

Purpose: Confirm that every public dataset surface stays synthetic and excludes patient data.

Release gate decision: `synthetic_preview_only`

Review lanes: provenance_review, privacy_boundary_review

Required fields:

1. dataset surface

2. provenance statement

3. patient data absent

4. direct identifier absent

5. real record absent

6. raw output absent

7. public boundary state

Escalation triggers:

1. Patient data status is unclear

2. Synthetic provenance is missing

3. Identifier review is incomplete

4. Real record language appears

### LAR002: Label definition reviewer

Purpose: Check that labels match the locked rubric version and do not claim clinical validation.

Release gate decision: `needs_clinician_review`

Review lanes: label_definition_review, clinician_review

Required fields:

1. label version

2. label lock file

3. rubric file

4. binary gate mapping

5. final label mapping

6. unsure rule state

7. review status wording

Escalation triggers:

1. Label version is missing

2. Label lock is edited silently

3. Clinical validation wording appears

4. Unsure rule is bypassed

### LAR003: Pilot subset reviewer

Purpose: Keep the pilot inter rater subset framed as protocol testing rather than an agreement study.

Release gate decision: `needs_adjudication`

Review lanes: inter_rater_review, label_quality_review

Required fields:

1. subset row count

2. sampling reason

3. agreement statistic state

4. reviewer bias reduction note

5. model identity limitation

6. pilot status wording

7. next review need

Escalation triggers:

1. Pilot subset is described as powered

2. Agreement statistic is implied

3. Model identity is overclaimed

4. Population prevalence is implied

### LAR004: Public release boundary reviewer

Purpose: Check that release language blocks raw output release, deployment claims, and dataset quality proof language.

Release gate decision: `not_for_public_summary`

Review lanes: public_release_boundary_review, data_quality_review

Required fields:

1. allowed public use

2. not allowed public use

3. raw output boundary

4. dataset quality proof boundary

5. clinical deployment boundary

6. model ranking boundary

7. official endorsement boundary

Escalation triggers:

1. Raw model output release is implied

2. Dataset quality proof is implied

3. Clinical deployment readiness is implied

4. Formal approval wording appears

## Escalation gate audit rows

### LAA001: Synthetic provenance audit

Linked IDs: LAR001, docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md

Required roles: LAR001

Review state: `synthetic_preview_only`

Required outcome: Keep synthetic provenance and patient data absence visible.

### LAA002: Label definition lock audit

Linked IDs: LAR002, docs/LABEL_DEFINITION_LOCK_V0_1.md, data/scoring_rubric_v0_1.json

Required roles: LAR002

Review state: `needs_clinician_review`

Required outcome: Block silent label definition drift and clinical validation wording.

### LAA003: Pilot inter rater subset audit

Linked IDs: LAR003, data/inter_rater_review_subset_v0_1.tsv

Required roles: LAR003

Review state: `needs_adjudication`

Required outcome: Keep the 24 row subset framed as protocol testing only.

### LAA004: Raw output exclusion audit

Linked IDs: LAR004, docs/release/PUBLIC_RELEASE_BOUNDARY_V0_1.md

Required roles: LAR004

Review state: `not_for_public_summary`

Required outcome: Keep raw model outputs excluded unless redistribution is cleared.

### LAA005: Public release boundary audit

Linked IDs: LAR001, LAR002, LAR003, LAR004

Required roles: LAR004

Review state: `not_for_public_summary`

Required outcome: Block dataset quality proof, clinical deployment, model ranking, and formal approval language.

## Boundary checks

1. Every role uses synthetic examples only.
2. Patient data is not used.
3. Reviewer roles do not prove dataset quality.
4. Label audit rows do not create clinical validation.
5. Public release boundaries block raw model outputs unless redistribution is cleared.
6. Passing this table is not clinical validation, model safety, dataset quality proof, model ranking, or deployment readiness.

## Public files

1. JSON source: `docs/label_audit_reviewer_role_table_v0_1.json`
2. Generated role table: `docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md`
3. Validator: `scripts/validate_label_audit_reviewer_role_table_v0_1.py`
4. Runnable target: `make label_audit_role_table`
5. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`
6. Clinician review protocol: `docs/CLINICIAN_REVIEW_PROTOCOL_V0_1.md`
7. Label audit example intake rows: `docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md`
8. Label audit example intake JSON: `docs/label_audit/label_audit_example_intake_v0_1.json`
