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
3. External sample JSONL.
4. MedHELM oriented metric JSON.

Docs:

1. Data dictionary.
2. Clinician evaluation rubric.
3. Failure Atlas draft entries.
4. MedHELM metric package draft.
5. Medmarks style local proof pack documentation.
6. Public boundary statement.
7. Dataset and evaluation card draft.

Scripts:

1. Repository validator.
2. JSONL sample validator.
3. MedHELM metric validator.
4. Medmarks style smoke runner.
5. OpenAI compatible prompt set runner.
6. Hugging Face Transformers prompt set runner.

## Proposed excluded assets

1. Raw model outputs.
2. Logs.
3. Local opencode run scripts with absolute paths.
4. Internal outreach drafts.
5. Internal contribution drafts.
6. Any file not cleared by release audit.

## Current constraints

1. Clinician review status is preliminary and must be described accurately.
2. Raw model output platform terms are not cleared, so raw outputs are excluded.
3. Open model run terms and execution route are not locked.
4. External ecosystem posts require separate audit and user approval.

## Next build action

Maintain the public release with sanitized files only and no absolute local paths.
