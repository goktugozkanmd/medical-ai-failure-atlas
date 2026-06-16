# SourceCheckup contributor checklist v0.2

Status: public contributor checklist.

Date: 2026 06 16

This checklist defines how to propose source claim review examples for SourceCheckup Medical.

This is not a clinical case intake form. Use it only for source discipline, locator integrity, claim support, and rewrite or review routing.

## Purpose

The checklist helps contributors describe:

1. The exact source surface.
2. The exact claim text.
3. Whether the claim is central to the answer.
4. Which evidence checks are required.
5. Whether a locator, guideline, policy, or broad source phrase needs review.
6. Whether the row can be converted into the existing SourceCheckup input format.

## Required boundaries

Every row must state:

1. No patient data is included.
2. No external action has been executed.
3. Outward use is not allowed by the contributor.
4. Maintainer review is required before any public use beyond synthetic preview.
5. SourceCheckup output is a review queue, not proof that a medical claim is true.

## Required fields

1. `contribution_id`
2. `source_surface`
3. `synthetic_answer_excerpt`
4. `exact_claim_text`
5. `central_to_answer`
6. `declared_sources`
7. `required_evidence_checks`
8. `proposed_public_action`
9. `maintainer_review_status`
10. `contains_patient_data`
11. `external_actions_executed`
12. `outward_use_allowed`

## Allowed source surfaces

1. `doi`
2. `pmid`
3. `url`
4. `guideline`
5. `policy`
6. `broad_source_language`
7. `none`

## Required evidence checks

Use one or more of:

1. `locator_format`
2. `source_exists`
3. `metadata_match`
4. `exact_claim_support`
5. `guideline_scope`
6. `policy_jurisdiction`
7. `rewrite_without_source_claim`

## Run

```bash
make sourcecheckup_contrib_v02
```

## Current public files

1. `sourcecheckup/schemas/sourcecheckup_contribution_schema_v0_2.json`
2. `sourcecheckup/examples/sourcecheckup_contribution_examples_v0_2.jsonl`
3. `scripts/validate_sourcecheckup_contribution_v0_2.py`
