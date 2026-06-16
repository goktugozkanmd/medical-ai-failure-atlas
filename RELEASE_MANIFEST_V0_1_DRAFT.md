# Release manifest v0.1 draft

Status: public v0.1 release manifest.

Date: 2026 06 13

## Proposed release name

Medical AI Failure Atlas v0.1

## Proposed release description

A physician authored synthetic evaluation resource for studying medical model safety wording, unsafe precision, missing variable awareness, and separation of urgent triage from individualized protocol detail.

This release is not clinical advice and not clinical validation.

## Proposed included assets

Release metadata:

1. License file.
2. Citation metadata file.

Data:

1. Scenario banks.
2. Scenario taxonomy.
3. Prompt sets.
4. Pilot inter rater review subset.
5. External sample JSONL.
6. MedHELM oriented metric JSON.
7. Scoring rubric JSON.

Docs:

1. Data dictionary.
2. Clinician evaluation rubric.
3. Failure Atlas draft entries.
4. MedHELM metric package draft.
5. Medmarks style local proof pack documentation.
6. Public boundary statement.
7. Dataset and evaluation card draft.
8. Label definition lock.
9. Clinician review disagreement protocol.
10. Pilot inter rater review subset plan.
11. Labeling package index.
12. Health data quality and label audit card.
13. Internal review form generation notes are retained locally until raw model output redistribution is cleared.

Scripts:

1. Repository validator.
2. JSONL sample validator.
3. MedHELM metric validator.
4. Medmarks style smoke runner.
5. OpenAI compatible prompt set runner.
6. Hugging Face Transformers prompt set runner.
7. Inter rater review form validator.
8. Health data quality card validator.

## Proposed excluded assets

1. Raw model outputs.
2. Logs.
3. Local opencode run scripts with absolute paths.
4. Internal outreach drafts.
5. Internal contribution drafts.
6. Any file not cleared by release audit.
7. Reviewer facing forms that contain raw model answer text until output redistribution terms are cleared.

## Current constraints

1. Clinician review status is preliminary and must be described accurately.
2. Raw model output platform terms are not cleared, so raw outputs are excluded.
3. Open model run terms and execution route are not locked.
4. External ecosystem posts require separate audit and user approval.
5. Public GitHub updates after the initial release require separate audit and user approval.

## Next build action

Maintain the public release with sanitized files only and no absolute local paths.
