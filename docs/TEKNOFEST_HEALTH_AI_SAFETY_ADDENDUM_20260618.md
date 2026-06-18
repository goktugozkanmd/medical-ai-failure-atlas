# TEKNOFEST Health AI Safety Addendum

Date: 2026 06 18

Status: field readiness public preview.

Purpose: give health AI teams a short safety addendum they can use while preparing project detail reports, especially for data quality, label uncertainty, source support, and claim boundaries.

This is not an official TEKNOFEST document, not a submission, not a partner claim, and not an endorsement claim.

## Source signals

### THASA001: TEKNOFEST Sağlıkta Yapay Zeka public page

Official source: https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/

Checked fact: The public page lists a 2026 health AI competition and says the competition aims to produce solutions for health problems and increase knowledge and trained human capacity.

Field read: Contestant facing safety guidance can create timely field value.

### THASA002: TEKNOFEST Sağlıkta Yapay Zeka public page

Official source: https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/

Checked fact: The university and above category focuses on predicting whether genetic variants are pathogenic or benign.

Field read: Data quality, label uncertainty, and clinical claim boundaries are directly relevant.

### THASA003: TEKNOFEST Sağlıkta Yapay Zeka public page

Official source: https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/

Checked fact: The project detail report deadline is listed as 29 June 2026 at 17:00.

Field read: A public safety addendum is time sensitive before the detail report deadline.

## Safety addendum checks

### THASC001: Health claim boundary

Question: Does the report avoid clinical deployment, diagnosis, treatment, or validation claims?

Why it matters: A competition model should not be framed as ready for care.

### THASC002: Label uncertainty

Question: Does the report explain uncertain, conflicting, or evolving labels?

Why it matters: Genetic variant classification can depend on evidence context and update over time.

### THASC003: Data leakage

Question: Does the report describe how leakage between training and evaluation data was checked?

Why it matters: Leakage can create false confidence and inflated performance.

### THASC004: Population and context limits

Question: Does the report state where the data may not represent the intended use setting?

Why it matters: A model can fail outside the data distribution that shaped it.

### THASC005: Source support

Question: Does each medical claim have source support, not only a citation nearby?

Why it matters: Citation presence is not the same as support for a specific claim.

### THASC006: Human review handoff

Question: Does the report define what a clinician, geneticist, or domain reviewer would need to check next?

Why it matters: A safe report shows the next human review step instead of implying autonomy.

### THASC007: Failure examples

Question: Does the report include examples where the system should abstain, ask for more context, or flag uncertainty?

Why it matters: Failure modes are more useful for safety than only success examples.

## Boundary

1. No official TEKNOFEST endorsement claim.
2. No submission claim.
3. No clinical deployment claim.
4. No clinical validation claim.
5. No patient data included.
6. No diagnosis or treatment advice.
7. No model ranking.
8. No score certification.
9. No partner claim.
10. No route access claim.

## Field action

Publish as a public safety addendum and use it as a conversation starter for health AI teams only after Dr. Ozkan clears the outreach route.

No email, application, official route, partner claim, payment, terms acceptance, clinical deployment, clinical validation, or official endorsement is made by this addendum.

## Runnable check

```bash
make teknofest_health_ai_safety_addendum
```
