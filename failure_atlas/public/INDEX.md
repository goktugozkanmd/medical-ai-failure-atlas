# Failure Atlas public index

Status: public safe draft.

Not for clinical use.

This index is a raw output withheld view of selected internal Failure Atlas cases. It is designed to show the type of safety boundary being studied without publishing model transcripts, model rankings, patient data, or clinical validation claims.

## What is included

The entries below describe internal case packs at a high level only.

The current failure mode taxonomy preview is available at [TAXONOMY_PREVIEW_20260616.md](TAXONOMY_PREVIEW_20260616.md).

The public case intake checklist is available at [CASE_INTAKE_CHECKLIST_V0_1.md](CASE_INTAKE_CHECKLIST_V0_1.md).

The generated case intake report is available at [build/case_intake_report_v0_1.md](build/case_intake_report_v0_1.md).

### FA_PUBLIC_001

Internal case: case 0001.

Clinical area: diabetes acute illness triage.

Failure mode family: remote dosing pressure under missing variables.

Abstracted safety boundary: a model response may move from urgent risk recognition into individualized rescue dosing when ketone status, hydration, local emergency pathway, and clinician review are missing.

Public status: Raw output withheld.

### FA_PUBLIC_002

Internal case: case 0002.

Clinical area: anticoagulation interaction triage.

Failure mode family: local protocol boundary collapse.

Abstracted safety boundary: a model response may name a compact management sequence for anticoagulation interaction concern before local protocol, current labs, bleeding severity, and prescribing context are established.

Public status: Raw output withheld.

### FA_PUBLIC_003

Internal case: case 0003.

Clinical area: obstetric emergency triage.

Failure mode family: protocol detail boundary.

Abstracted safety boundary: a model response may recognize a pregnancy emergency while still presenting a portable emergency treatment sequence that should remain tied to local obstetric pathway and patient specific variables.

Public status: Raw output withheld.

## What is excluded

The public index does not include:

1. Raw model outputs.
2. Full prompts.
3. Output hashes.
4. Model performance scores.
5. Model rankings.
6. Patient data.
7. Clinical validation claims.
8. Guideline concordance claims.
9. Deployment safety claims.

## Current interpretation

These entries are candidate failure mechanism examples for clinician review. They are not final determinations that a model is unsafe, and they are not evidence that any model is safe.

The intended use is method development: defining review questions, claim boundaries, reviewer intake fields, and safer public release formats for clinician led medical AI evaluation.

## Current blocker

The internal raw case packs are not public release ready because raw output redistribution terms are not cleared and each safety interpretation still needs additional independent clinician review.
