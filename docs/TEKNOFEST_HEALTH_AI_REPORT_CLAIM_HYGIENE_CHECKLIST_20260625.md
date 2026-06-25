# TEKNOFEST Health AI report claim hygiene checklist

Date: 2026 06 25

Status: public preview.

Purpose: help Health AI competition teams write safer project detail reports without turning model development language into clinical readiness, diagnosis, deployment, or patient benefit claims.

Source basis: the 2026 TEKNOFEST Health AI competition page describes EKG classification for high school teams, pathogenic or benign variant prediction for university and above teams, and a project detail report deadline on 2026 06 29 at 17:00.

Source: https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/

This checklist is not a TEKNOFEST submission, not a competition team claim, not official instruction, not medical advice, not clinical validation, not clinical deployment, not a diagnostic statement, not a patient benefit claim, not a regulatory claim, and not proof that any model is safe.

It uses no patient data.

## How to use this checklist

Use this before a project detail report leaves the team folder.

For each report sentence that mentions performance, safety, clinical use, patient impact, data, explainability, fairness, or deployment, ask four questions:

1. What exact evidence supports this sentence?
2. Does the evidence come from the competition data, a public source, synthetic testing, or private data?
3. Would a reader mistake the sentence for a clinical claim?
4. What sentence would stay true if the model failed outside the competition setting?

If the fourth answer is unclear, rewrite the claim.

## Gate 1. Scope lock

Allowed wording:

1. This project explores a model development approach for the competition task.
2. This report describes evaluation within the stated competition setting.
3. This model was not evaluated for clinical deployment.
4. This work should be read as a competition prototype.

Blocked wording:

1. This model can move into care.
2. This model can diagnose patients.
3. This model improves patient outcomes.
4. This model is safe for hospital use.
5. This model can replace clinician review.

Reviewer question:

Does the report keep the model inside the competition task, or does it imply a clinical product?

## Gate 2. Dataset meaning

Allowed wording:

1. The data support evaluation under the competition task definition.
2. Dataset labels and splits determine what this report can claim.
3. Any external use would need separate data review.
4. The report does not claim population level safety.

Blocked wording:

1. The dataset proves real world accuracy.
2. The dataset represents all patients.
3. The model generalizes to clinical practice.
4. The labels are the clinical truth.
5. Data quality is guaranteed.

Reviewer question:

Does the report explain what the dataset can and cannot prove?

## Gate 3. EKG classification language

Allowed wording:

1. The model classifies competition EKG inputs according to the task labels.
2. The report describes signal preprocessing, label handling, validation split, and error review.
3. Any clinical interpretation of EKG output would need clinician review and separate validation.
4. False negative and false positive patterns should be described.

Blocked wording:

1. The model detects disease in patients.
2. The model can screen the public.
3. The output is a clinical rhythm diagnosis.
4. The model can be used in emergency care.
5. A high score proves clinical reliability.

Reviewer question:

Does the EKG section separate label classification from clinical interpretation?

## Gate 4. Variant prediction language

Allowed wording:

1. The model predicts pathogenic or benign labels within the competition task.
2. The report describes feature source, label source, class balance, and error examples.
3. Any genetic interpretation would need domain review and separate validation.
4. The report should identify uncertain or borderline patterns.

Blocked wording:

1. The model tells whether a patient has a genetic disease.
2. The model can guide treatment.
3. The output is a clinical genetics report.
4. The model can be used for counseling.
5. The model proves variant pathogenicity.

Reviewer question:

Does the variant section avoid clinical genetics advice?

## Gate 5. Performance reporting

Allowed wording:

1. Report the metric, split, sample size, and uncertainty.
2. Show at least one failure mode.
3. Separate leaderboard performance from safety evidence.
4. State that competition performance does not prove clinical deployment readiness.

Blocked wording:

1. Best score means safest model.
2. High accuracy proves readiness.
3. The model has no safety risk.
4. The model outperforms clinicians.
5. The model works across all settings.

Reviewer question:

Does the report explain where the model fails?

## Gate 6. Error analysis

Minimum error analysis rows:

1. False negative pattern.
2. False positive pattern.
3. Low confidence correct result.
4. High confidence wrong result.
5. Data quality issue.
6. Preprocessing sensitivity.
7. Missing input or corrupted input behavior.
8. Subgroup or category where performance drops.

Reviewer question:

Can a reader see at least one concrete failure mode before seeing any success claim?

## Gate 7. Human oversight

Allowed wording:

1. A clinician or domain expert would need to review any clinical use.
2. The current report does not establish an oversight workflow.
3. Human review should focus on uncertain, high risk, and failure pattern outputs.
4. The model should not act as the final decision maker.

Blocked wording:

1. No expert review is needed.
2. The system can run autonomously in care.
3. The model reduces the need for clinicians.
4. The model can make the final call.

Reviewer question:

Does the report name where human review would be required?

## Gate 8. User information

Allowed wording:

1. Users should know the model was evaluated in a competition context.
2. Users should know the model has not been clinically validated.
3. Users should know the intended task and the forbidden interpretations.
4. Users should see a warning when the model is uncertain or outside scope.

Blocked wording:

1. Users can rely on the model output.
2. Users do not need to understand the limits.
3. The report can hide uncertainty.
4. The model is self explanatory.

Reviewer question:

Would a non expert reader understand the model limits?

## Gate 9. Regulatory and device boundary

Allowed wording:

1. This report does not claim medical device status.
2. This report does not claim regulatory approval.
3. This report does not claim AI Act compliance.
4. This report does not claim FDA authorization.

Blocked wording:

1. The model is approved.
2. The model meets regulatory standards.
3. The model is compliant.
4. The model is a deployable device.

Reviewer question:

Does the report avoid legal and regulatory conclusions?

## Gate 10. Safer sentence patterns

Replace this:

1. Our model diagnoses arrhythmia.

Use this:

1. Our model classifies competition EKG inputs according to the task labels.

Replace this:

1. Our model predicts pathogenic variants for clinical use.

Use this:

1. Our model predicts task labels for pathogenic or benign variants within the competition setting.

Replace this:

1. This system is safe and accurate.

Use this:

1. This report shows task performance and failure patterns under the tested split.

Replace this:

1. The model can help doctors.

Use this:

1. Any clinician use would need separate validation, oversight design, and institutional review.

Replace this:

1. The model is ready for deployment.

Use this:

1. The model remains a competition prototype.

## One page report insert

Suggested report boundary paragraph:

This project is a competition prototype. The report evaluates model behavior only inside the stated task setting. The results do not establish clinical validation, clinical deployment readiness, medical device status, regulatory approval, patient benefit, or clinician substitution. Any future clinical use would need separate data review, expert review, oversight design, safety testing, and institutional authorization.

## Release boundary

Before sharing the report, confirm:

1. No patient data appears.
2. No private clinical text appears.
3. No diagnosis advice appears.
4. No treatment advice appears.
5. No clinical validation claim appears.
6. No deployment claim appears.
7. No regulatory approval claim appears.
8. No official endorsement claim appears.
9. No partner claim appears.
10. No score meaning claim appears.

## Runnable check

```bash
python3 scripts/validate_teknofest_health_ai_report_claim_hygiene_checklist_20260625.py
```
