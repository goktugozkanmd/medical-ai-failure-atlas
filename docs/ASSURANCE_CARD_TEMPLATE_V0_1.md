# Medical language model assurance card template v0.1

Status: public preview.

Date: 2026 06 16

This template is a pre release assurance card for medical language model evaluation artifacts. It helps a clinician led team record intended use, risk, data quality, source support, human review, audit trail, and public wording boundaries before any external release or sandbox discussion.

It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not official endorsement.

## Who should use this

1. Medical AI builders preparing a synthetic evaluation artifact.
2. Clinician reviewers checking whether risk and source support have been recorded.
3. Open source maintainers deciding whether a public release note is bounded enough.
4. Turkish health AI safety teams preparing a discussion packet without claiming official status.

## Card identity

Required fields:

1. Artifact name.
2. Artifact version.
3. Owner or maintainer.
4. Date.
5. Repository path.
6. Public status.
7. Intended audience.
8. Intended use boundary.
9. Non use boundary.

Required public wording:

1. This card is for evaluation design.
2. This card is not for clinical use.
3. This card does not claim model safety.
4. This card does not claim clinical validation.

## Model card

Required fields:

1. Model name if a model was run.
2. Provider or local route.
3. Version or run identifier.
4. Endpoint or local execution state.
5. Terms state.
6. Raw output publication state.
7. Model ranking state.
8. Known limitations.

Current public example rule:

1. No model endpoint call is required for this template.
2. No judge endpoint call is required for this template.
3. Raw model outputs are not public unless terms and release rights are separately cleared.
4. Model ranking is not part of this card.

## Patient data and privacy boundary

Required fields:

1. Patient data present.
2. Identifiers present.
3. Synthetic data status.
4. Provenance note.
5. Privacy review state.
6. Release blocker.

Current public example rule:

1. patient_data_present must be false for this public example.
2. identifiers_present must be false for this public example.
3. Synthetic examples only.
4. Any real patient data route is blocked in this automation.

## Risk card

Required fields:

1. Clinical domain.
2. Risk theme.
3. False reassurance risk.
4. Red flag omission risk.
5. Medication safety risk.
6. Source hallucination risk.
7. Privacy risk.
8. Severity.
9. Likelihood.
10. Mitigation.
11. Residual risk.
12. Reviewer concern.

Allowed severity values:

1. low.
2. medium.
3. high.
4. critical.

## Data card

Required fields:

1. Synthetic or real data status.
2. Scenario count.
3. Prompt count.
4. Label method.
5. Label version.
6. Reviewer status.
7. Bias or coverage limitation.
8. Data quality blocker.
9. Release decision.

Related public surface:

1. Health data quality and label audit card.
2. Label definition lock.
3. Clinician review protocol.

## Source support card

Required fields:

1. Claim text.
2. Claim type.
3. Source locator.
4. Support status.
5. Required action.
6. Public wording decision.

Allowed support status values:

1. verified.
2. unsupported.
3. insufficient.
4. stale.
5. not checked.

Related public surface:

1. SourceCheckup Medical.
2. Source claim review queue.
3. MedHELM and Medmarks boundary notes.

## Human review card

Required fields:

1. Reviewer role.
2. Review date.
3. Case count reviewed.
4. High risk rows reviewed.
5. Disagreement count.
6. Second review required.
7. Final release recommendation.
8. Remaining blocker.

Review state values:

1. not reviewed.
2. clinician first pass.
3. second review needed.
4. adjudication needed.
5. public wording cleared.
6. blocked.

## Audit trail

Required fields:

1. Artifact id.
2. Version.
3. Build command or creation route.
4. Validation command.
5. Validator result.
6. Source files.
7. Reviewer status.
8. External action status.
9. Release decision.
10. Next action.

## Release gate levels

L0 concept:

Idea or outline only. External use is not allowed.

L1 local build:

Local artifact exists and validates. External use is not allowed by default.

L2 clinician reviewed:

At least one clinician review pass is recorded. Public wording still needs a separate gate.

L3 public candidate:

License, citation, privacy, source, wording, and review gates are addressed. External release still needs exact action clearance.

L4 external pilot:

Exact external target and use case are cleared. This requires explicit Goktug clearance.

L5 clinical deployment:

Clinical deployment evaluation. L5 clinical deployment is blocked in this automation.

Current public template state:

release_gate_level L1.

## Public action checklist

Before any external action:

1. Exact target is known.
2. Exact public text is known.
3. Source claims are checked.
4. Cost state is no spend.
5. Terms state is no terms acceptance.
6. Patient data risk is none.
7. Clinical deployment risk is none.
8. Clinical validation claim risk is none.
9. Official endorsement risk is none.
10. Package publication or legal release risk is none.

## JSON companion

The companion template is:

`docs/assurance_card_template_v0_1.json`

The validator is:

`scripts/validate_assurance_card_template_v0_1.py`

Run:

```bash
make assurance_card_template
```

## Track A value

For Turkiye health AI safety infrastructure, this card gives a concrete way to discuss Turkish medical LLM evaluation, clinician review, data quality, source support, and sandbox readiness boundaries without claiming official status or deployment readiness.

## Track B value

For global open source medical AI evaluation, this card gives maintainers a reusable public release gate that connects Failure Atlas, SourceCheckup Medical, clinician review, data quality, and benchmark boundary notes without model ranking or clinical validation claims.
