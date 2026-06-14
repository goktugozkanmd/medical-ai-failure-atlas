# Failure Atlas public methodology

Status: public safe draft.

Not for clinical use.

## Purpose

The Failure Atlas studies how medical language model answers can appear clinically careful while still crossing a safety boundary. The current public layer is intentionally conservative. It exposes failure mode categories and review questions, not raw model transcripts.

## Raw output withheld policy

Internal case packs may contain exact prompts, exact model answers, hashes, source row identifiers, and reviewer notes. The public layer withholds those materials unless all of the following are true:

1. Redistribution terms for the relevant model output are cleared.
2. The case has additional clinician review.
3. Patient data risk is checked and remains absent.
4. The text has an audit that confirms no clinical validation, model ranking, or deployment safety claim is being made.
5. The release has a public sanitation check that blocks raw output leakage.

## Case abstraction

Each public entry uses an abstracted safety boundary rather than a transcript. The abstraction may name the clinical area and failure mode family, but it should avoid patient shaped detail, exact model wording, model scores, or treatment instructions.

## Claim limits

The public layer can support these claims:

1. The project contains synthetic medical AI safety evaluation materials.
2. The project separates internal raw review material from public summaries.
3. The project has local validators that check public release boundaries.
4. The listed cases are candidate failure mechanism examples for further clinician review.

The public layer cannot support these claims:

1. A model is clinically safe.
2. A model is clinically unsafe.
3. A model is better or worse than another model.
4. A prompt set is representative of clinical practice.
5. A response is guideline concordant.
6. The work is clinical validation.
7. The resource is patient advice.

## Review workflow

The workflow is:

1. Internal case capture from synthetic prompts and model outputs.
2. Local provenance and hash recording.
3. Candidate safety gate assignment.
4. Clinician review queue creation.
5. Raw output withheld public summary creation.
6. Public sanitation validation before any public release candidate is rebuilt.

## Release boundary

A public release can include this methodology and the public index only if the validator confirms that no internal raw output, prompt text, prompt hash, raw output hash, case directory, or patient data is present in the public summary files.
