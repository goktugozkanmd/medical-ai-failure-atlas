# Clinician literacy release gate lesson map v0.1

Status: generated public preview.

Date: 2026 06 16

This map turns clinician AI literacy into release gate training. It links synthetic Turkish medical language model rows, SourceCheckup review queue rows, clinician review states, and assurance gate levels.

It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.

## Summary

Lessons: 6

Total minutes: 30

TR MedLLM cases covered: 14

SourceCheckup queue rows covered: 12

Clinician review states represented: 3

Release gate decisions represented: 6

Assurance gate levels represented: 5

## Release gate coverage

blocked_missing_source_support: 5

blocked_pending_source_verification: 3

needs_clinician_review: 3

needs_source_review: 2

pass_local_sourcecheckup: 2

synthetic_preview_only: 2

## Lesson outlines

### CLRG001: Red flag escalation and false reassurance

Minutes: 5

Learning goal: Spot when a calm answer hides urgent clinical uncertainty.

TR MedLLM rows: TRFAI003, TRFAI009

SourceCheckup rows: SCQ_003

Clinician review states: needs_clinician_review

Release gate decisions: needs_clinician_review, blocked_pending_source_verification

Assurance gate levels: L1, L2

Learner task: Mark the red flag, name the missing urgency variable, and write one safe escalation sentence.

Facilitator check: The learner does not let partial improvement or a locator style reference remove urgent review.

Track A value: Turkish clinician literacy for red flag triage boundary discipline.

Track B value: Failure Atlas false reassurance lesson for global medical AI review.

### CLRG002: Medication safety under missing variables

Minutes: 5

Learning goal: Block personalized dose, stop, start, or protocol advice when critical variables are absent.

TR MedLLM rows: TRFAI001, TRFAI010, TRFAI011, TRFAI014

SourceCheckup rows: SCQ_002, SCQ_009

Clinician review states: needs_clinician_review, needs_source_review

Release gate decisions: needs_clinician_review, needs_source_review, blocked_missing_source_support, blocked_pending_source_verification

Assurance gate levels: L1, L2

Learner task: List missing medication, kidney, pregnancy, intake, and danger context before any answer is strengthened.

Facilitator check: The learner keeps clinician review visible and rejects remote individualized medication changes.

Track A value: Turkish medication safety stop rule practice for assurance lab readiness.

Track B value: Reusable medication risk lesson for Failure Atlas and SourceCheckup review.

### CLRG003: Source support and guideline discipline

Minutes: 5

Learning goal: Separate a source looking sentence from an actually supported exact claim.

TR MedLLM rows: TRFAI002, TRFAI012, TRFAI014

SourceCheckup rows: SCQ_001, SCQ_004, SCQ_010

Clinician review states: needs_source_review

Release gate decisions: needs_source_review, blocked_missing_source_support, blocked_pending_source_verification

Assurance gate levels: L1, L2, L3

Learner task: Identify whether the answer uses a guideline, policy, URL, DOI, PMID, or broad source phrase, then mark it as unsupported or pending support.

Facilitator check: The learner states that SourceCheckup creates a review queue, not proof that a medical claim is true.

Track A value: Turkish source discipline exercise for clinician literacy and national route wording safety.

Track B value: SourceCheckup lesson that can be reused by open source maintainers.

### CLRG004: Privacy, provenance, and data quality boundary

Minutes: 5

Learning goal: Stop movement of real clinical text into public or unsecured AI workflows.

TR MedLLM rows: TRFAI004

SourceCheckup rows: SCQ_007, SCQ_012

Clinician review states: synthetic_preview_only

Release gate decisions: synthetic_preview_only, blocked_missing_source_support, pass_local_sourcecheckup

Assurance gate levels: L0, L1

Learner task: Rewrite a risky prompt into a synthetic only prompt and name the provenance field that must be checked.

Facilitator check: The learner keeps patient data absent and does not treat synthetic rows as real world deployment evidence.

Track A value: Health data quality and privacy practice for Turkish assurance discussions.

Track B value: Data provenance lesson for public dataset release readiness.

### CLRG005: Communication, bias, and premature closure

Minutes: 5

Learning goal: Prevent reassuring wording, age bias, and anxiety framing from hiding uncertainty.

TR MedLLM rows: TRFAI005, TRFAI007, TRFAI013

SourceCheckup rows: SCQ_006, SCQ_008

Clinician review states: needs_clinician_review

Release gate decisions: needs_clinician_review, blocked_missing_source_support, pass_local_sourcecheckup

Assurance gate levels: L1, L2

Learner task: Move warning signs to the visible part of the answer and remove premature benign framing.

Facilitator check: The learner names the bias or communication risk without turning the lesson into patient advice.

Track A value: Turkish clinician communication practice for safe AI assisted patient messaging.

Track B value: Failure Atlas bias and communication lesson for wider medical domains.

### CLRG006: Workflow, official wording, and public release boundary

Minutes: 5

Learning goal: Separate local evaluation infrastructure from deployment, compliance, sandbox, or official role claims.

TR MedLLM rows: TRFAI006, TRFAI008

SourceCheckup rows: SCQ_005, SCQ_011

Clinician review states: synthetic_preview_only, needs_source_review

Release gate decisions: synthetic_preview_only, blocked_missing_source_support

Assurance gate levels: L0, L1, L3, L5

Learner task: Rewrite a public claim so it says local evaluation infrastructure rather than official approval, sandbox access, compliance, or deployment.

Facilitator check: The learner keeps official route relevance separate from official acceptance or external pilot clearance.

Track A value: Turkish national route wording safety for assurance lab and sandbox readiness packets.

Track B value: Open source public release wording lesson for global medical AI projects.

## Boundary checks

1. Every lesson uses synthetic examples only.
2. Patient data is not used.
3. Local pass does not mean clinical truth, source truth, model safety, or deployment readiness.
4. SourceCheckup rows are review queue rows, not proof that a medical claim is true.
5. Assurance gate L5 remains blocked for this automation.
6. External workshop, institutional use, endpoint run, or clinical deployment requires separate explicit clearance.

## Public files

1. JSON source: `docs/clinician_literacy_release_gate_lesson_map_v0_1.json`
2. Generated map: `docs/CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md`
3. Validator: `scripts/validate_clinician_literacy_release_gate_lesson_map_v0_1.py`
4. Runnable target: `make clinician_literacy_map`
