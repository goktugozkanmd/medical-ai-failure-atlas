# Turkish Medical LLM Reviewer Issue Template

Date: 2026 06 19

Status: public issue template for Turkish medical LLM review routing.

Purpose: turn the open issue chain from global benchmark pressure to Turkish medical coverage intake into one contributor issue template. The template is used before a Turkish medical LLM row is accepted for public review.

This template is not a Turkish medical benchmark, not a benchmark result, not a leaderboard, not model ranking, not score certification, not source truth certification, not clinical validation, not clinical deployment, not patient data access, not regulated data access, not institutional approval, not partner status, not a formal application, not payment, not terms acceptance, and not endorsement.

## Start state

Live BAGLAM2 and portfolio trackers were read before build. Active Gmail outreach threads and targeted Gmail searches were checked before build. No new route owner reply was found. The prior Hacettepe acknowledgement remains the only reply and is not endorsement, validation, partnership, institutional support, official role, official course, hospital adoption, or clinical clearance.

## Linked public issue chain

1. Issue `#132`: Global Benchmark Pressure Response.
2. Issue `#133`: Failure Atlas Real Clinical Text Pressure Template.
3. Issue `#134`: SourceCheckup Medical Benchmark Source Support Worksheet.
4. Issue `#135`: Turkish Medical LLM Coverage Pressure Addendum.
5. Issue `#136`: Turkish Medical LLM Coverage Reviewer Intake Rows.

## Template fields

### Field 1: Issue intent

Question: is this row asking for language review, medical scope review, source support review, clinician review, data boundary review, governance review, or release decision?

Allowed answer: one primary intent and any secondary intent.

Stop condition: stop if the issue intent is model ranking, score reporting, leaderboard standing, clinical deployment, patient data access, or official approval.

### Field 2: Linked context

Question: which public context issue is the row linked to?

Allowed answer: one or more of `#132`, `#133`, `#134`, `#135`, and `#136`.

Stop condition: stop if the row uses benchmark pressure without linking a public context issue.

### Field 3: Turkish language state

Question: is the text Turkish, translated Turkish, mixed Turkish, non Turkish, or only a claim about Turkish?

Allowed answer: language state plus evidence.

Stop condition: stop if Turkish language presence is reused as Turkish medical coverage.

### Field 4: Medical scope

Question: what medical task or workflow is being reviewed?

Allowed answer: diagnosis, treatment, triage, medication, discharge, coding, patient education, health data, workflow, or other with explanation.

Stop condition: stop if a general language example is presented as medical readiness.

### Field 5: Clinical context

Question: who is the expected reader or user?

Allowed answer: patient, clinician, student, maintainer, data steward, governance reviewer, unknown, or other with explanation.

Stop condition: stop if the row implies workflow readiness without user role and setting.

### Field 6: Source support

Question: what exact public source supports the medical or safety claim?

Allowed answer: source URL, claim sentence, support state, uncertainty state, and reviewer note.

Stop condition: stop if source existence is treated as source support.

### Field 7: Turkish terminology risk

Question: could morphology, suffix, abbreviation, synonym, tone, or local term choice change the medical meaning?

Allowed answer: terminology risk note and language reviewer route.

Stop condition: stop if translated wording is called safe without language review.

### Field 8: Clinician review question

Question: what exact clinical judgment is needed?

Allowed answer: focused clinician question plus risk axis.

Stop condition: stop if the row claims clinical validation, clinical safety, or clinical deployment readiness.

### Field 9: Data boundary

Question: what data type is implied?

Allowed answer: public only, synthetic safety text, public article text, benchmark adjacent summary, real clinical text without access, patient data, regulated data, unknown, or other with explanation.

Stop condition: stop if patient data, regulated data, or institutional data is implied without explicit clearance.

### Field 10: Ranking boundary

Question: does the issue compare models, imply a score, or imply leaderboard standing?

Allowed answer: no ranking statement.

Stop condition: stop if the row asks for rank, score, model standing, or score certification.

### Field 11: Public route fit

Question: does the issue imply formal application, official route approval, partner status, institutional support, payment, terms, or endorsement?

Allowed answer: route fit unresolved or written evidence provided.

Stop condition: stop if any official route claim appears without written evidence and explicit Goktug clearance.

### Field 12: Release decision

Question: should the issue be accepted, held for review, rewritten, routed to another reviewer, or stopped?

Allowed answer: accepted, held, rewritten, routed, or stopped with reason.

Stop condition: stop if any required boundary field is missing.

## Contributor issue body skeleton

```text
Title:

Issue intent:

Linked context:

Turkish language state:

Medical scope:

Clinical context:

Source support:

Turkish terminology risk:

Clinician review question:

Data boundary:

Ranking boundary:

Public route fit:

Release decision:

Blocked claims checked:
No patient data.
No benchmark item copying.
No answer keys or hidden prompts.
No Turkish medical benchmark claim.
No model ranking.
No leaderboard claim.
No score certification.
No source truth certification.
No clinical validation.
No clinical deployment.
No institutional approval.
No partner, payment, terms, formal application, or endorsement claim.
```

## Maintainer triage rule

1. Accept only if all required fields are present and all blocked claims are absent.
2. Route to language review if Turkish state or terminology risk is unresolved.
3. Route to clinician review if medical scope or clinical judgment is unresolved.
4. Route to source review if source support is unresolved.
5. Route to data steward review if data boundary is unresolved.
6. Route to governance review if ranking boundary or public route fit is unresolved.
7. Stop if the issue asks for ranking, score, clinical validation, deployment, patient data, regulated data, institutional approval, partner status, payment, terms, formal application, or endorsement.

## Recommended check

```bash
make turkish_medical_llm_reviewer_issue_template
```
