# Label audit public contributor issue guide v0.1

Status: public preview.

Date: 2026 06 16

This guide defines how contributors can open a public label audit issue for synthetic data quality and label audit review examples.

It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, and not an institutional or national program endorsement.

## Purpose

The public issue route helps contributors submit synthetic examples where a medical AI dataset or review artifact might overstate:

1. Synthetic provenance.
2. Label definition stability.
3. Pilot inter rater subset meaning.
4. Raw model output release status.
5. Public release boundary.
6. Dataset quality proof.
7. Clinical validation.

The issue route does not approve a dataset. It creates a maintainer review queue.

## Public issue template

Use:

`.github/ISSUE_TEMPLATE/label_audit_review.yml`

The template requires:

1. Audit surface.
2. Synthetic audit example.
3. Suggested reviewer role.
4. Exact boundary to review.
5. Proposed public action.
6. Required checks.
7. Boundaries.

## Required contributor boundaries

Every issue must state:

1. The example is synthetic and contains no patient data.
2. Raw model outputs and private benchmark content are not included.
3. Dataset quality is not proven.
4. No external action has been executed.
5. Outward use is not allowed without maintainer review.
6. The issue is not clinical advice and not a clinical validation claim.

## Maintainer triage

Maintainers should route accepted issues into one of:

1. `docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md`
2. `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`
3. `DATASET_EVALUATION_CARD_V0_1_DRAFT.md`
4. `DATA_DICTIONARY.md`
5. `docs/LABEL_DEFINITION_LOCK_V0_1.md`
6. `docs/LABELING_PACKAGE_INDEX_V0_1.md`
7. A closed issue comment explaining why the row is not suitable.

## Required checks

Use one or more of:

1. `synthetic_provenance`
2. `patient_data_absence`
3. `label_lock_match`
4. `pilot_subset_framing`
5. `raw_output_exclusion`
6. `public_release_boundary`
7. `dataset_quality_proof_boundary`

## Example public issue body

Audit surface:

`pilot inter rater subset`

Synthetic audit example:

`A public note describes a 24 row pilot subset as representative of real deployment conditions.`

Suggested reviewer role:

`Pilot subset reviewer`

Exact boundary to review:

`The 24 row pilot subset should be framed as protocol testing only.`

Required checks:

1. Confirm the subset row count.
2. Confirm sampling reason.
3. Confirm no agreement statistic is implied.
4. Confirm no population prevalence is implied.
5. Rewrite public wording if needed.

Boundary:

Synthetic only. No patient data. No raw model output. No external action. No clinical advice. No clinical validation claim. No dataset quality proof.

## Track A value

For Turkiye health AI safety infrastructure, this issue route creates a public data quality and label audit intake surface for Turkish medical LLM review, clinician AI literacy, and sandbox readiness discussions without claiming official status or sandbox access.

## Track B value

For global open source medical AI evaluation, this issue route gives Health Data Quality and Label Audit Commons a public contributor path that can grow provenance, label lock, pilot subset, and release boundary examples without publishing patient data, model rankings, clinical validation claims, or dataset quality proof claims.
