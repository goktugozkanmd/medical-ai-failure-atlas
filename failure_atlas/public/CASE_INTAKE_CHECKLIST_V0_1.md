# Failure Atlas case intake checklist v0.1

Status: public contributor checklist.

Date: 2026 06 16

This checklist defines how to propose synthetic failure cases for the Medical AI Failure Atlas.

It is designed for public review work, not clinical use.

## Purpose

The checklist turns a broad concern into a reviewable case packet:

1. What the synthetic setting is.
2. What failure pattern is being tested.
3. What a safer answer should do.
4. What source support or clinician review is still required.
5. Which public release gate applies.

## Required boundaries

Every intake case must state:

1. The case is synthetic.
2. No patient data is included.
3. No private model output is included.
4. No clinical advice is being given.
5. No clinical validation claim is being made.
6. No model safety or superiority claim is being made.

## Required fields

1. `case_id`
2. `clinical_domain`
3. `setting`
4. `synthetic_case_summary`
5. `failure_pattern`
6. `risk_axis`
7. `sourcecheckup_needed`
8. `clinician_review_needed`
9. `safe_answer_expectation`
10. `release_gate`
11. `track_a_relevance`
12. `track_b_relevance`

## Allowed risk axes

1. `false_reassurance`
2. `medication_safety`
3. `source_support`
4. `missing_context`
5. `rare_danger`
6. `over_treatment`
7. `communication_risk`
8. `bias_or_premature_closure`
9. `workflow_mismatch`
10. `privacy_or_provenance`

## Release gates

1. `synthetic_preview_only`
2. `needs_source_review`
3. `needs_clinician_review`
4. `not_for_public_summary`

## Track A relevance

Track A fields should describe why the case matters for Turkish health AI safety, clinician literacy, source discipline, assurance lab work, or health data quality.

Do not claim official national acceptance, institutional endorsement, regulatory approval, sandbox access, or compliance.

## Track B relevance

Track B fields should describe how the case strengthens the global public Failure Atlas, SourceCheckup Medical, no ranking report design, benchmark compatibility notes, or open source contribution workflow.

Do not claim benchmark superiority or compatibility unless separately verified.

## Current public files

1. `failure_atlas/public/case_intake_examples_v0_1.jsonl`
2. `failure_atlas/public/build/case_intake_report_v0_1.md`
3. `scripts/validate_failure_atlas_case_intake_v0_1.py`
4. `scripts/generate_failure_atlas_case_intake_report_v0_1.py`

## Run

```bash
make case_intake
```
