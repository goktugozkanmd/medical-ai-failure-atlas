# MedHELM crosswalk draft

Status: internal draft only.

Date: 2026 06 13

## Purpose

This document maps the local Medical AI Failure Atlas work to MedHELM so the project can become a credible open source contribution rather than a standalone small benchmark.

This is not cleared for external posting.

## Source anchors checked

Checked on 2026 06 13:

1. MedHELM website: https://medhelm.org/
2. MedHELM GitHub: https://github.com/PacificAI/medhelm

Official MedHELM positioning observed:

1. Open community led benchmark for language models on medical tasks.
2. 121 clinical tasks.
3. 22 subcategories.
4. 31 datasets.
5. 5 clinical categories.
6. Measures accuracy, calibration, robustness, and writing style.
7. Contribution routes include adding clinical scenarios, refining LLM jury prompts, and GitHub issue based requests.

## Fit decision

The local project should not present itself as a competitor to MedHELM.

The stronger positioning is:

Physician authored synthetic failure mechanism layer for medical model outputs, pending final clinician review.

This means the local asset can help MedHELM users interpret why an answer that looks medically competent may still be risky because of unsafe precision, weak calibration, missing variables, or poor separation between triage and protocol.

## Local asset summary

Current local resource:

1. 150 synthetic medicine wide scenarios.
2. 70 prompt rows.
3. 180 captured model outputs from hard30 and V3 scale30 runs.
4. 3 draft Failure Atlas entries.
5. Strict triage CSV files with high priority and medium priority review queues.
6. A clinician evaluation rubric.

Boundary:

These are internal development signals. They are not public model performance claims and not clinical validation.

## Crosswalk to MedHELM categories

### Clinical Decision Support

Local patterns:

1. Correct escalation with unsafe protocol over precision.
2. Remote rescue or reversal protocol generation.
3. False reassurance after early normal tests.
4. Omission or under escalation in rare lethal presentations.

MedHELM fit:

This is the strongest fit. The local scenarios test whether a model can stay calibrated when asked for action in incomplete clinical contexts.

Contribution angle:

Add a failure mechanism review layer around clinical decision support outputs, focused on whether the model separates high level triage from institution specific treatment protocol.

### Patient Communication and Education

Local patterns:

1. Insulin sick day wording with unsafe remote dose precision.
2. Home blood pressure and pregnancy danger communication.
3. Patient facing anticoagulation or toxicity advice.
4. When to seek urgent care after a partial or normal early test.

MedHELM fit:

This fits patient education and care instruction tasks because the danger often comes from wording, not knowledge absence.

Contribution angle:

Add patient facing wording risk tags, especially when the model gives exact medication or rescue details that could be copied directly by a patient.

### Medical Research Assistance

Local patterns:

1. Evidence reliability prompt.
2. Citation support and unsupported guideline sounding claims.
3. Overconfident explanation of a literature based recommendation.

MedHELM fit:

This is a secondary fit. It can help evaluate source support, claim precision, and whether models distinguish evidence from inference.

Contribution angle:

Add evidence reliability tags and source support checks for open ended answers.

### Administration and Workflow

Local patterns:

1. Local protocol awareness.
2. Referral pathway specificity.
3. Transfer or emergency pathway wording without institutional context.

MedHELM fit:

This is useful where the model is asked to support workflow or routing decisions.

Contribution angle:

Add workflow context gap tags when a model speaks as if local pathway details are universal.

### Clinical Note Generation

Local patterns:

1. Lower immediate fit in the current version.
2. Potential future fit for discharge instruction and safety netting text.

MedHELM fit:

Not the first route. It becomes relevant after patient instruction examples are converted into note or discharge style tasks.

Contribution angle:

Park for later.

## Crosswalk to MedHELM metric dimensions

### Calibration

Local addition:

Does the model express uncertainty when key variables are missing?

Example failure:

The model recognizes a dangerous condition but gives exact treatment detail without INR, renal function, pregnancy status, glucose trend, ketone data, severity, or local protocol.

### Robustness

Local addition:

Does the model preserve the same safety boundary when the prompt wording changes?

Example failure:

The model gives safe high level escalation in one wording but gives dose or rescue protocol detail when the wording asks what to do now.

### Writing Style

Local addition:

Does the wording prevent unsafe copying into patient action?

Example failure:

The model says urgent evaluation is needed but also includes exact dose ranges or protocol language that dominates the safety message.

### Accuracy

Local addition:

Accuracy should not stop at recognizing the correct diagnosis or danger.

Example failure:

The answer is directionally correct about an emergency but not safe as a clinical assistant output because it misses patient specific variables or local supervision requirements.

## Candidate contribution package

Best first external package after approval:

1. A short MedHELM GitHub discussion or issue.
2. A one page Failure Atlas crosswalk.
3. Three synthetic example scenarios.
4. One sample scoring row per scenario.
5. No model ranking.
6. No patient data.
7. Clear statement that the asset is for model development feedback, not clinical advice.

Recommended three examples:

1. Insulin sick day advice with vomiting and poor oral intake.
2. Warfarin complication with black stool and reversal wording risk.
3. Severe headache in pregnancy with possible preeclampsia and remote protocol risk.

## Draft external question

Not cleared for posting.

Title:

Clinician reviewed Failure Atlas crosswalk for calibration, unsafe precision, and patient facing medication safety wording

Body:

I am a physician building a small clinician review layer for medical model outputs across medicine.

The goal is not to create a competing benchmark or claim clinical validation. The goal is to describe failure mechanisms that may be useful when interpreting open ended clinical decision support or patient communication outputs.

The current internal draft includes synthetic scenarios and captured model outputs focused on:

1. Unsafe remote medication or rescue dosing.
2. Correct emergency recognition with excessive protocol detail.
3. Evidence reliability and citation support.
4. False reassurance after early normal tests.
5. Missing variables and local workflow context gaps.

Would a compact Failure Atlas crosswalk be useful for MedHELM as a discussion, issue, or small example suite?

I can keep the first version limited to three synthetic examples, clinician review tags, and no model ranking.

## Do not post until

1. User approves external posting.
2. License and citation route are decided.
3. Clinician review status is stated accurately.
4. Academic submission audit is completed for the exact external text.
5. The local repo publish route is decided.
