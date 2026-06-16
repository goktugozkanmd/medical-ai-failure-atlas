# Health data quality and label audit card v0.1

Date: 2026 06 16

Status: public preview.

This card summarizes the synthetic data quality and label audit boundary for the Medical AI Failure Atlas public repository.

It is a synthetic dataset release readiness checklist. It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, and not an institutional or national program endorsement.

## Dataset surfaces

Current public source files:

1. `data/scenario_bank_v1.tsv`
2. `data/scenario_bank_v2_hard_addendum.tsv`
3. `data/scenario_bank_v3_scale_seed.tsv`
4. `data/prompt_set_v1.tsv`
5. `data/prompt_set_v2_hard_30.tsv`
6. `data/prompt_set_v3_scale_30.tsv`
7. `data/inter_rater_review_subset_v0_1.tsv`
8. `data/scoring_rubric_v0_1.json`
9. `docs/LABEL_DEFINITION_LOCK_V0_1.md`
10. `LABELING.md`
11. `sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl`

## Current counts

1. 150 synthetic scenario rows.
2. 70 prompt rows.
3. 24 pilot inter rater rows.
4. 8 Turkish synthetic risk rows.
5. 8 source claim review queue rows.

The 24 pilot inter rater rows are for protocol testing only. They are not a powered agreement study and they do not establish clinical validation.

## Provenance

1. Data provenance: synthetic only.
2. Patient data: absent.
3. Direct identifiers: absent.
4. Real clinical records: absent.
5. Raw model outputs: excluded from the public release.
6. Output redistribution terms: not cleared for raw output publication.

## Label method

Current public review wording:

`single physician authored synthetic draft pending additional clinician review`

Current label version:

`v0.1.0`

Current label lock:

`docs/LABEL_DEFINITION_LOCK_V0_1.md`

Current rubric:

`data/scoring_rubric_v0_1.json`

The label audit checks whether the label definitions, safety gates, pilot subset, and public wording are internally consistent. It does not prove that the labels are correct for real clinical use.

## Quality checks

This card tracks:

1. Synthetic provenance.
2. Patient data absence.
3. Identifier absence.
4. Scenario count.
5. Prompt count.
6. Pilot inter rater subset count.
7. Label version.
8. Label lock file.
9. Reviewer status.
10. Raw output exclusion.
11. SourceCheckup routing.
12. Public release gate.

## Known limitations

1. Scenario banks are synthetic and may not cover real workflow diversity.
2. The pilot inter rater subset is for protocol testing only.
3. Additional clinician review is still pending.
4. No agreement statistic is reported here.
5. Raw model outputs are not public.
6. This card does not evaluate any model.
7. This card does not approve any dataset for clinical deployment.

## SourceCheckup routing

Rows that make source, guideline, policy, or broad evidence claims should be routed to:

`sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl`

SourceCheckup routing is a review queue. It does not turn a citation, PMID, DOI, URL, guideline phrase, or policy phrase into evidence.

## Release gate

Current release gate:

`public_preview_allowed_synthetic_only`

Allowed public use:

1. Repository inspection.
2. Synthetic evaluation design discussion.
3. Contributor review of source claim and label audit structure.
4. Clinician review workflow design.

Not allowed public use:

1. Patient care.
2. Clinical deployment.
3. Clinical validation claims.
4. Model ranking.
5. Claims that one model is better than another.
6. Claims of formal approval.
7. Claims of sandbox access.
8. Claims of institutional backing.

## Maintenance owner

Maintainer: Dr. Goktug Ozkan, Internal Medicine Specialist.

Maintenance action:

Update this card whenever public scenario counts, prompt counts, label version, review status, or raw output release boundary changes.
