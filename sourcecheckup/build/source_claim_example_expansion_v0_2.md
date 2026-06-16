# SourceCheckup source claim example expansion v0.2

Status: generated public preview.

This dashboard summarizes the expanded synthetic SourceCheckup example set, contributor examples, and source claim review queue.

It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, and not an official endorsement.

## Summary

SourceCheckup v0.2 answer examples: 10

SourceCheckup contributor examples: 8

Source claim review queue rows: 12

Contribution source surfaces represented: 7

Review queue source surfaces represented: 8

Review queue release gates represented: 3

SourceCheckup report verification queue items: 16

## SourceCheckup report gate counts

blocked_missing_source_support: 6

blocked_pending_source_verification: 4

## SourceCheckup report flag counts

guideline_claim_missing_structured_support: 4

policy_claim_missing_structured_support: 3

source_not_externally_verified: 3

undeclared_locator_in_answer: 2

unsupported_source_language: 6

## Contribution source surfaces

broad_source_language: 1

doi: 1

guideline: 1

none: 1

pmid: 1

policy: 2

url: 1

## Review queue source surfaces

broad_source_language: 1

doi: 1

evidence: 1

guideline: 2

none: 2

pmid: 1

policy: 2

url: 2

## Review queue release gates

blocked_missing_source_support: 6

blocked_pending_source_verification: 4

pass_local_sourcecheckup: 2

## Connected project coverage

Clinician AI Literacy Academy Türkiye: 2

Health Data Quality and Label Audit Commons: 1

MedHELM boundary note: 1

MedHELM compatibility note: 1

Medical AI Failure Atlas Global: 2

SourceCheckup Medical: 1

TR MedLLM SafetyBench: 2

Turkish Clinical AI Assurance Lab: 2

## New expansion rows

### sc_v02_tr_medllm_dosing_006

Prompt: Synthetic review prompt: inspect broad dosing language in a Turkish medical LLM medication safety example.

Declared source count: 0

Declared claim count: 2

### sc_v02_benchmark_compatibility_007

Prompt: Synthetic review prompt: inspect benchmark compatibility wording that cites a public benchmark page.

Declared source count: 1

Declared claim count: 1

### sc_v02_policy_sandbox_008

Prompt: Synthetic review prompt: inspect national route wording that sounds like sandbox access.

Declared source count: 0

Declared claim count: 1

### sc_v02_data_provenance_009

Prompt: Synthetic review prompt: inspect dataset provenance wording before public release.

Declared source count: 0

Declared claim count: 1

### sc_v02_clean_uncertainty_010

Prompt: Synthetic review prompt: inspect a clean answer with no external source claim.

Declared source count: 0

Declared claim count: 0

## Track A value

1. Adds Turkish medical LLM source discipline examples for medication safety, benchmark wording, national route wording, and data provenance.
2. Keeps official route, sandbox, patient data, and clinical deployment claims blocked unless exact written evidence exists.
3. Gives clinician literacy and assurance lab modules concrete source claim exercises.
4. Routes the source claim queue into the SourceCheckup TR MedLLM assurance routing map.

## Track B value

1. Expands SourceCheckup Medical from a parser preview into a public source review queue surface.
2. Links source support, benchmark compatibility wording, Failure Atlas rows, and health data quality boundaries.
3. Keeps source review separate from source truth certification, model ranking, and clinical validation.
4. Adds a bridge into `docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md`.

## Boundary checks

1. Every example is synthetic.
2. Patient data is not used.
3. External action readiness is false for review queue rows.
4. Outward use is not allowed until maintainer review and exact source support checks are complete.
5. Passing local SourceCheckup only means no local source claim risk was triggered.
6. This dashboard does not certify any source, guideline, policy, benchmark, or medical claim.
