# TEKNOFEST Health AI Detail Report Final Gate

Date: 2026 06 18

Status: time sensitive public final gate for report language and safety claims.

Purpose: give TEKNOFEST health AI teams a short final review gate before project detail report submission, especially for data provenance, label uncertainty, leakage, source support, human review, and public claim hygiene.

This is not an official TEKNOFEST document, not a submission, not a route access claim, not a partner claim, and not an endorsement claim.

## Source signals

### THADG001: TEKNOFEST Sağlıkta Yapay Zeka public page

Official source: https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/

Checked fact: The public page lists a 2026 Sağlıkta Yapay Zeka competition and states that the competition aims to support AI solutions for health problems and increase knowledge and trained human capacity.

Field read: A final safety gate can help teams keep report language useful without implying clinical readiness.

### THADG002: TEKNOFEST Sağlıkta Yapay Zeka public page

Official source: https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/

Checked fact: The university and above category focuses on predicting whether genetic variants are pathogenic or benign.

Field read: Variant classification work needs visible label provenance, uncertainty handling, and human review language.

### THADG003: TEKNOFEST Sağlıkta Yapay Zeka public page

Official source: https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/

Checked fact: The public page lists the project detail report deadline as 29 June 2026 at 17:00.

Field read: The useful window is immediate. The artifact should be short enough for teams to apply before the detail report deadline.

## Final gate

Use this gate before any public or competition report language is finalized.

### Gate 1: data permission and privacy

Pass question: Does the report state the data source, data access boundary, and whether any real patient data is included?

Block language: We used real patient data safely.

Allowed language: This report does not include patient level data in the public artifact. Data access and sharing rights require separate verification.

### Gate 2: label provenance

Pass question: Does the report say where pathogenic or benign labels came from and how uncertain labels were handled?

Block language: The labels are ground truth.

Allowed language: Labels are treated as review labels and may depend on evolving clinical evidence.

### Gate 3: leakage check

Pass question: Does the report explain how overlap between training, validation, and test records was checked?

Block language: High accuracy proves the model is reliable.

Allowed language: Performance language is limited until leakage checks and external review are documented.

### Gate 4: missingness and representation

Pass question: Does the report state which populations, variant types, or data sources may be under represented?

Block language: The model generalizes to clinical practice.

Allowed language: Generalization is unknown outside the evaluated data context.

### Gate 5: source support

Pass question: Does each medical or biological claim have source support that directly supports the claim?

Block language: A citation is present, so the claim is supported.

Allowed language: Each medical claim should be checked against the cited source and marked unsupported if the source does not directly support it.

### Gate 6: human review handoff

Pass question: Does the report say what a clinician, geneticist, or domain reviewer must check next?

Block language: The model can make diagnostic decisions.

Allowed language: The model output is a research or competition artifact and needs domain review before any clinical interpretation.

### Gate 7: failure mode examples

Pass question: Does the report include cases where the system should abstain, request more evidence, or flag uncertainty?

Block language: The system always returns an answer.

Allowed language: The system can return uncertainty or require more information when evidence is insufficient.

### Gate 8: no ranking and no validation

Pass question: Does the report avoid ranking models, claiming clinical validation, or claiming deployment readiness?

Block language: Our model has completed clinical validation or is ready for care.

Allowed language: The report describes a competition project and does not establish clinical validation or deployment readiness.

### Gate 9: public claim hygiene

Pass question: Can every public sentence survive this test: no official role, no endorsement, no partner claim, no submission claim unless actually submitted, no clinical claim unless actually validated?

Block language: TEKNOFEST or any institution approved this safety review.

Allowed language: This is an independent public safety review aid and not an official TEKNOFEST document.

## Decision states

1. Green: report language is bounded and can be shared as a competition project description.
2. Amber: source support, label provenance, or leakage language needs revision.
3. Red: patient data, clinical validation, official endorsement, partner, deployment, or model ranking claim appears without verified clearance.

## Boundary

1. No official TEKNOFEST endorsement claim.
2. No official TEKNOFEST role claim.
3. No submission claim.
4. No application claim.
5. No partner claim.
6. No patient data included in this public artifact.
7. No diagnosis or treatment advice.
8. No clinical deployment claim.
9. No clinical validation claim.
10. No model ranking.
11. No score certification.
12. No payment.
13. No terms acceptance.

## Field action

Publish as a public final gate and link it from the repository TEKNOFEST section. It can be used by teams reviewing their own detail reports before the 29 June 2026 deadline.

No email, public social post, application, submission, official route, partner claim, payment, terms acceptance, patient data, clinical deployment, clinical validation, or official endorsement is made by this final gate.

## Runnable check

```bash
make teknofest_health_ai_detail_report_final_gate
```
