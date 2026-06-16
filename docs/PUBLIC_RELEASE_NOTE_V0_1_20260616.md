# Public infrastructure release note v0.1

Date: 2026 06 16

Status: public preview.

This release note summarizes the public medical AI evaluation infrastructure now visible in this repository.

It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not a regulatory claim, and not an institutional or national program endorsement.

## What is now inspectable

1. Failure Atlas public taxonomy.
2. Failure Atlas case intake workflow.
3. SourceCheckup Medical source review workflow.
4. No ranking synthetic report design.
5. TR MedLLM synthetic risk pack.
6. Clinician review queue.
7. Contribution templates for synthetic cases and source review.
8. Public roadmap for the next build steps.
9. Clinician review protocol v0.1.
10. Source claim review queue v0.1.
11. Health data quality and label audit card v0.1.
12. MedHELM and Medmarks boundary notes v0.1.
13. Medical language model assurance card template v0.1.

## Current public coverage

1. 19 synthetic intake rows.
2. 14 Turkish synthetic risk rows.
3. 10 risk axes.
4. 10 of 10 Failure Atlas taxonomy pattern IDs represented.
5. 19 clinician review queue rows.
6. 4 source review rows.
7. 6 public review states.
8. 8 source claim review queue rows.
9. 150 synthetic scenario rows.
10. 70 prompt rows.
11. 24 pilot inter rater rows.

## Reproducible checks

Run:

```bash
make validate
make case_intake
make taxonomy_dashboard
make tr_medllm_pack
make tr_medllm_specialty_spread
make clinician_review_queue
make source_claim_queue
make health_data_quality_card
make boundary_notes
make assurance_card_template
make sourcecheckup_contrib_v02
make leaderboard_report
```

These commands check public data boundaries, generate public reports, validate synthetic review rows, and keep the release away from patient data, raw model outputs, model ranking, and clinical claims.

## Track A value

For Türkiye health AI safety infrastructure, this public preview gives a concrete clinician led foundation for:

1. Turkish medical LLM safety cases.
2. Review gates before any sandbox or workflow discussion.
3. Clinician AI literacy examples.
4. Source support discipline.
5. Health data privacy and provenance boundaries.
6. Source claim review queue for Turkish medical language model examples.
7. Data quality and label audit card for synthetic release readiness.
8. Boundary notes that separate benchmark mapping from compatibility or endorsement claims.
9. Assurance card template for intended use, risk, source support, human review, and release gate boundaries.

This does not claim official status, program participation, regulatory access, sandbox access, or institutional endorsement.

## Track B value

For global open source medical AI evaluation, this public preview gives:

1. A reusable failure taxonomy.
2. A synthetic intake contract.
3. A generated review queue.
4. A SourceCheckup contribution path.
5. A no ranking report path.
6. A visible foundation for collaboration with benchmark and model builder communities.
7. A source claim review queue that separates citation presence from evidence support.
8. A data quality and label audit checklist for synthetic dataset release readiness.
9. Boundary notes for MedHELM and Medmarks oriented mapping without compatibility claims.
10. A reusable assurance card template for public medical language model evaluation releases.

This does not claim benchmark equivalence, clinical validation, or model superiority.

## Next public build gates

1. Additional Turkish risk rows for specialty spread.
2. Public dashboard index for the six seed platforms.
3. SourceCheckup contributor issue for source claim review examples.
4. External maintainer issue draft only after exact owner clearance.
