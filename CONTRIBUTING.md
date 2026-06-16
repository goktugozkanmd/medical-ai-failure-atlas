# Contributing

Status: public contribution guide.

## Scope

This project is a physician authored synthetic medical AI evaluation resource.

It is not clinical advice.

It is not a clinical validation study.

It must not include patient data.

## Contribution rules

1. Do not submit real patient cases.
2. Do not include protected health information.
3. Do not include dates, locations, identifiers, or rare details from real patients.
4. Use synthetic cases only.
5. Mark every case with data provenance.
6. Keep clinical safety wording conservative.
7. Do not claim a model is safe or unsafe overall from one case.
8. Do not add external model outputs unless platform terms allow redistribution.
9. Do not add clinical advice for patients.
10. Do not remove release boundary notes without review.

## Case proposal minimum fields

1. Scenario ID.
2. Clinical domain.
3. Care setting.
4. Synthetic patient summary.
5. Task for model.
6. Expected safety focus.
7. Failure mechanism tags.
8. Missing variables that determine safe action.
9. Patient facing risk if wording is copied.
10. Review question for a clinician.

## Review status wording

Allowed:

`physician authored synthetic draft pending final clinician review`

Not allowed unless explicitly confirmed:

`clinician validated`

Not allowed:

`safe for clinical use`

## External communication

Repository issues and pull requests should stay focused on synthetic examples, source support review, failure taxonomy, validation scripts, and documentation.

Do not use this repository to request patient data, clinical deployment, clinical validation, institutional endorsement, model ranking claims, or private benchmark access.

## Label audit issue route

Use `.github/ISSUE_TEMPLATE/label_audit_review.yml` for synthetic data quality and label audit examples.

This route is for synthetic provenance, label definition lock, pilot subset framing, raw output exclusion, and public release boundary review.

It does not allow patient data, raw model outputs, clinical advice, clinical validation claims, dataset quality proof, or outward use without maintainer review.

Public example intake rows are available at `docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md`.

Run:

```bash
make label_audit_examples
```

The compact dashboard for these rows is available at `docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md`.

Run:

```bash
make label_audit_dashboard
```

The maintainer triage board is available at `docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md`.

Run:

```bash
make label_audit_triage
```

The public wording decision log is available at `docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md`.

Run:

```bash
make label_audit_wording_log
```
