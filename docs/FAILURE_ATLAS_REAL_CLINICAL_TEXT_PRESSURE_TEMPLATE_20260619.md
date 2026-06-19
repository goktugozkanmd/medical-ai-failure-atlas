# Failure Atlas Real Clinical Text Pressure Template

Date: 2026 06 19

Status: public template for benchmark pressure around real clinical text.

Purpose: turn BRIDGE and MedHELM pressure into a reusable Failure Atlas intake template for medical AI failure reports without patient data, benchmark answers, protected examples, model ranking, score certification, clinical validation, clinical deployment, procurement evidence, partner status, payment, terms acceptance, or endorsement.

This template is not a BRIDGE collaboration claim, not a MedHELM collaboration claim, not a benchmark result, not a leaderboard, not model ranking, not score certification, not clinical validation, not clinical deployment, not patient data access, not regulated data access, not source truth certification, not procurement evidence, not partner status, not institutional approval, not payment, not terms acceptance, and not endorsement.

## Start state

Live BAGLAM2 and portfolio trackers were read before build. Active Gmail outreach threads and targeted Gmail searches were checked before build. No new route owner reply was found. The prior Hacettepe acknowledgement remains the only reply and is not endorsement, validation, partnership, institutional support, official role, official course, hospital adoption, or clinical clearance.

## Source pressure

### Source 1: BRIDGE

Source: https://www.nature.com/articles/s41551-026-01719-2

Checked signal: the article published on 17 June 2026 describes BRIDGE as a multilingual benchmark with 87 tasks from 59 real world clinical data sources across 9 languages, 8 task types, and 14 clinical specialties. It also points to open data, leaderboard access, and evaluation code surfaces.

Template pressure: a public Failure Atlas row should not stop at generic unsafe answer language. It should name the task type, source type, specialty, document type, care stage, language, data boundary, failure mechanism, reviewer question, evidence needed, allowed public wording, blocked claim, and stop condition.

### Source 2: BRIDGE leaderboard surface

Source: https://huggingface.co/spaces/YLab-Open/BRIDGE-Medical-Leaderboard

Checked signal: the live leaderboard surface exists. It was used only as a public surface check. No ranking, score, model standing, submission, compatibility, or benchmark result claim is made.

Template pressure: a public row may say why a real clinical text task class matters. It must not imply that a model is better, safer, validated, deployed, or procurement ready because of a leaderboard.

### Source 3: MedHELM

Source: https://medhelm.org/

Checked signal: MedHELM describes an open community led benchmark for medical tasks with 121 clinical tasks, 22 subcategories, 31 datasets, and 5 categories. It reports accuracy, calibration, robustness, and writing style across clinical workflows.

Template pressure: a public row should carry workflow context, reviewer role, uncertainty, and stop condition before safety language is used.

## Template fields

### Field 1: row id

Allowed value: a stable public identifier for the synthetic or method level row.

Evidence needed: identifier only.

Blocked claim: real patient case identity.

### Field 2: task type

Allowed value: triage, information extraction, diagnosis support, prognosis support, billing coding, summarization, patient communication, source support, or other clearly named task class.

Evidence needed: short task class note.

Blocked claim: benchmark task coverage proves clinical safety.

### Field 3: source type

Allowed value: synthetic note, public guideline text, public article abstract, public policy text, public rubric description, internal non patient test note, or withheld regulated source.

Evidence needed: public source state or withheld boundary state.

Blocked claim: patient data clearance.

### Field 4: specialty

Allowed value: specialty or clinical area named at a high level.

Evidence needed: specialty label and reason for inclusion.

Blocked claim: broad specialty readiness.

### Field 5: document type

Allowed value: discharge style summary, consultation style note, radiology style report, pathology style report, medication list, laboratory trend, referral note, patient instruction, public guideline excerpt, or other document type.

Evidence needed: document type label.

Blocked claim: all clinical text readiness.

### Field 6: care stage

Allowed value: prevention, triage, emergency care, outpatient visit, inpatient care, discharge, follow up, chronic care, coding, audit, education, or governance.

Evidence needed: care stage label.

Blocked claim: deployment readiness across care settings.

### Field 7: language and local context

Allowed value: language, regional terminology, abbreviation risk, and translation boundary.

Evidence needed: language note and reviewer question.

Blocked claim: Turkish readiness or multilingual readiness without local review.

### Field 8: data boundary

Allowed value: public synthetic only, public source only, private source withheld, regulated data not accessed, patient data not used, or route unknown.

Evidence needed: boundary statement.

Blocked claim: regulated data access or patient data access.

### Field 9: failure mechanism

Allowed value: source unsupported claim, unsafe certainty, missing uncertainty, wrong triage priority, temporal error, medication safety error, diagnostic closure, hallucinated citation, missing contraindication, missing escalation, privacy leak risk, label ambiguity, or other named mechanism.

Evidence needed: mechanism note and reviewer question.

Blocked claim: model defect proven without review.

### Field 10: reviewer question

Allowed value: the narrow question a clinician, source reviewer, language reviewer, data steward, or governance reviewer should answer.

Evidence needed: role and question.

Blocked claim: clinician endorsement.

### Field 11: evidence needed

Allowed value: source support, source absence, uncertainty note, reviewer disagreement, data boundary, label provenance, missingness note, leakage note, allowed wording, or blocked wording.

Evidence needed: evidence checklist.

Blocked claim: evidence complete if a required field is missing.

### Field 12: public wording allowed

Allowed value: cautious public sentence that describes a method risk or review need.

Evidence needed: source support and reviewer route.

Blocked claim: score, ranking, safety proof, validation, deployment, partner, procurement, or endorsement.

### Field 13: blocked public claim

Allowed value: the exact sentence type that must not be used.

Evidence needed: blocked wording log.

Blocked claim: silent release when blocked wording remains.

### Field 14: stop condition

Allowed value: do not publish the row, do not rank, do not submit, do not contact maintainer, do not call ready, or do not reuse until evidence is supplied.

Evidence needed: stop condition owner.

Blocked claim: release readiness without stop rule.

## Example row skeleton

Row id: FA REALTEXT TEMPLATE 001

Task type: information extraction

Source type: synthetic note

Specialty: internal medicine

Document type: discharge style summary

Care stage: discharge

Language and local context: Turkish abbreviation review needed

Data boundary: public synthetic only and patient data not used

Failure mechanism: medication safety error and missing uncertainty

Reviewer question: would a clinician require escalation or clarification before this answer is shown?

Evidence needed: source support, medication list boundary, reviewer question, allowed wording, blocked wording, stop condition

Public wording allowed: this row describes a medication safety review need in a synthetic discharge style task.

Blocked public claim: this row proves that a model is clinically unsafe or clinically safe.

Stop condition: do not rank or publish as model performance unless reviewer evidence and data boundary are complete.

## Public use rules

1. Use synthetic or public source material unless a lawful private review route exists.
2. Do not copy benchmark examples, answer keys, hidden prompts, protected examples, private clinical text, or patient data.
3. Do not rank models.
4. Do not describe a benchmark score as clinical safety.
5. Do not describe leaderboard standing as procurement evidence.
6. Do not describe a public row as clinical validation.
7. Do not imply Turkish readiness without Turkish language and clinician review.
8. Do not imply specialty readiness without specialty, document type, and care stage fields.
9. Do not publish if source support, reviewer role, data boundary, or stop condition is missing.
10. Link benchmark adjacent notes back to issue #132 when the row is derived from global benchmark pressure.

## Immediate next actions

1. Convert this template into a small Failure Atlas public intake checklist.
2. Add a SourceCheckup Medical source support worksheet for benchmark adjacent rows.
3. Add a Turkish medical LLM coverage pressure addendum for language, abbreviation, specialty, document type, and care stage.
4. Add a clinician reviewer handoff protocol for rows that need human interpretation.

## Runnable check

```bash
make failure_atlas_real_clinical_text_pressure_template
```
