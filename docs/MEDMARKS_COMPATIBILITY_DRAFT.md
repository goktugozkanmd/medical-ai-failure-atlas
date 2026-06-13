# Medmarks compatibility draft

Status: internal draft only.

Date: 2026 06 13

## Purpose

This note converts the Failure Atlas project into a possible Medmarks oriented discussion direction.

It is not cleared for external posting.

## Source anchors checked

Checked on 2026 06 13:

1. Medmarks GitHub: https://github.com/MedARC-AI/Medmarks
2. Medmarks technical report: https://arxiv.org/html/2605.01417v1

Observed fit:

1. Medmarks is a runnable open source benchmark suite for medical tasks.
2. The suite includes verifiable tasks, open ended tasks evaluated with LLM as judge, and training capable environments.
3. The local Failure Atlas examples fit best as an open ended safety and wording evaluation, not as a deterministic multiple choice benchmark.

## Discussion direction

The first useful output is a small external sample file, not a full benchmark submission.

Local sample:

`data/failure_atlas_external_sample_v0_1.jsonl`

Validation:

`scripts/validate_external_sample_jsonl.py data/failure_atlas_external_sample_v0_1.jsonl`

The sample includes three synthetic cases:

1. Type 1 diabetes vomiting with hyperglycemia and no ketone strips.
2. Warfarin dosing error with black stool.
3. Pregnancy severe headache and visual symptoms.

## Why these three cases

They are compact, medicine wide, and show failure mechanisms that standard accuracy scoring may miss:

1. Unsafe remote medication or rescue dosing.
2. Protocol detail crossing into patient facing advice.
3. Missing variable awareness.
4. Urgent escalation without unsafe specificity.
5. Safe wording under incomplete context.

## Proposed Medmarks issue question

Not cleared for posting.

Title:

Compatibility question for a small physician authored safety wording sample

Body:

I am a physician building a draft clinician review workflow for medical model outputs across medicine.

The local draft focuses on open ended clinical safety and patient facing wording rather than multiple choice knowledge.

I prepared a three case synthetic JSONL sample with:

1. Prompt text.
2. Expected safety focus.
3. Failure mechanism tags.
4. Clinician review question.
5. Rubric criteria.

The current fit appears closest to an open ended Medmarks task evaluated with a judge or rubric.

Would the maintainers prefer this type of contribution as:

1. A discussion first.
2. A small external example repository.
3. A proposed new open ended benchmark folder.

No patient data are used. The examples are for model development feedback, not clinical advice or clinical validation.

## Release boundary

Do not post or publish until:

1. User approves.
2. License and citation are chosen.
3. The local repo publication route is chosen.
4. The exact external text passes final audit.
5. Clinician review status is described accurately.
