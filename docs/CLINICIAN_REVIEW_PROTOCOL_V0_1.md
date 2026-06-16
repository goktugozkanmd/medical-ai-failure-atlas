# Clinician review protocol v0.1

Status: public preview.

Date: 2026 06 16

This protocol defines how synthetic Failure Atlas and TR MedLLM review rows should be checked before any public summary becomes stronger.

It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, and not an institutional or national program endorsement.

## Scope

This protocol applies to:

1. Synthetic Failure Atlas case intake rows.
2. Turkish synthetic risk pack rows.
3. Generated clinician review queue rows.
4. Source review rows that need SourceCheckup routing.
5. Public release gate decisions for synthetic examples.

It does not apply to real patient data, raw clinical notes, clinical deployment, real care decisions, or model certification.

## Reviewer task

For each queue row, the reviewer checks:

1. Whether the row is synthetic.
2. Whether any patient data or identifiable detail appears.
3. Whether raw model output is present.
4. Whether the taxonomy pattern IDs fit the synthetic risk.
5. Whether the expected safe answer preserves escalation, source, privacy, medication, communication, bias, workflow, or review boundary.
6. Whether SourceCheckup review is needed.
7. Whether the public release gate is strict enough.

## Review states

Use these public review states:

1. `synthetic_preview_only`
2. `needs_clinician_review`
3. `needs_source_review`
4. `needs_adjudication`
5. `not_for_public_summary`
6. `ready_for_public_synthetic_summary`

`ready_for_public_synthetic_summary` does not mean clinical validation. It means the synthetic row can be summarized publicly with the stated boundaries.

## Required reviewer fields

Every reviewed row should record:

1. `case_id`
2. `reviewer_role`
3. `review_date`
4. `synthetic_boundary_ok`
5. `patient_data_absent`
6. `raw_model_output_absent`
7. `taxonomy_mapping_ok`
8. `safe_answer_boundary_ok`
9. `sourcecheckup_needed`
10. `review_state`
11. `release_gate_decision`
12. `short_reason`

Reviewer initials may be kept outside the public file if needed. The public protocol does not require naming individual reviewers.

## Release gate checklist

Block public summary if any of these are true:

1. Patient data appears.
2. Raw model output appears and redistribution is not cleared.
3. The row implies diagnosis or treatment advice.
4. The row ranks a model.
5. The row claims clinical deployment readiness.
6. The row claims clinical validation.
7. The row claims regulatory acceptance.
8. The row claims official role or endorsement.
9. The row uses unsupported source or guideline certainty.
10. The row lacks a clear synthetic boundary.

## Disagreement rule

If two reviewers disagree on a gate decision:

1. Keep both original decisions.
2. Mark the row `needs_adjudication`.
3. Record the reason for disagreement.
4. Do not overwrite either original review.
5. Use a separate adjudication note only after both reviews are complete.

If one reviewer is unsure:

1. Keep the row out of stronger public wording.
2. Mark the row `needs_adjudication`.
3. Ask for a short uncertainty reason.

## SourceCheckup routing

Rows with source support risk should route to SourceCheckup when:

1. A guideline claim is made without exact source support.
2. A DOI, PMID, URL, guideline, policy, or broad source statement needs checking.
3. A claim sounds supported but the exact source is not named.
4. A real source is used to support a broader claim than it can support.

SourceCheckup review is source support review. It is not clinical truth certification.

## Warning sign reviewer role table

Use `docs/WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md` when a row involves false reassurance, partial negative evidence, symptom fluctuation, source locator claims, or warning sign placement.

The table defines four public reviewer roles:

1. Clinician first pass reviewer.
2. Source locator reviewer.
3. Warning sign wording reviewer.
4. Escalation gate adjudicator.

Run:

```bash
make warning_sign_role_table
```

## Escalation gate audit rows

Use the escalation gate audit rows when a public summary might become stronger than the evidence allows.

The current rows cover:

1. Partial negative evidence escalation.
2. Symptom fluctuation warning wording.
3. Source locator triage claims.
4. Public wording boundaries.
5. Reviewer disagreement.

## Label audit reviewer role table

Use `docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md` when a row or public dataset surface needs synthetic provenance review, label definition review, pilot subset framing review, raw output exclusion review, or public release boundary review.

Run:

```bash
make label_audit_role_table
```

## Public wording allowed

Allowed wording:

1. `synthetic reviewer workflow`
2. `clinician review queue`
3. `synthetic row pending clinician review`
4. `source review needed`
5. `ready for public synthetic summary`

Not allowed wording:

1. Wording that says the protocol proves clinical validity.
2. Wording that says a model can be used safely in care.
3. Wording that says a model is ready for deployment.
4. Wording that ranks one model above another.
5. Wording that says the work has formal approval.

## Track A use

For Türkiye health AI safety infrastructure, this protocol gives a simple public review gate for Turkish medical LLM examples, clinician literacy, source discipline, privacy boundaries, and sandbox readiness discussion.

It does not claim official status, program participation, sandbox access, or regulatory acceptance.

## Track B use

For global open source medical AI evaluation, this protocol gives a reusable review workflow for Failure Atlas rows, SourceCheckup rows, no ranking reports, and collaboration discussions.

It does not claim benchmark equivalence, model superiority, or model safety.
