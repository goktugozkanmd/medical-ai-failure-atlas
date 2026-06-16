# SourceCheckup TR MedLLM assurance routing map v0.1

Status: generated public preview.

Date: 2026 06 16

This map connects SourceCheckup queue rows, Turkish synthetic risk rows, and assurance release gate examples. It shows which synthetic source claim problems should flow to source review, clinician review, assurance gates, or blocked public wording.

It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.

## Summary

Routes: 7

SourceCheckup queue rows covered: 12

TR MedLLM cases covered: 14

Assurance release gate examples covered: 6

Source surfaces represented: 8

Risk axes represented: 10

Release gate levels represented: 6

Routing decisions represented: 7

## Routing decision coverage

blocked_data_provenance_claim: 1

blocked_official_or_deployment_claim: 1

needs_clinician_review: 1

needs_clinician_source_review: 1

needs_source_review: 1

public_candidate_boundary_ready: 1

synthetic_positive_control_only: 1

## Source surface coverage

broad_source_language

doi

evidence

guideline

none

pmid

policy

url

## Risk axis coverage

bias_or_premature_closure

communication_risk

false_reassurance

medication_safety

missing_context

over_treatment

privacy_or_provenance

rare_danger

source_support

workflow_mismatch

## Route map

### STM001: Guideline and benchmark source support route

SourceCheckup rows: SCQ_001, SCQ_004, SCQ_010

TR MedLLM rows: TRFAI002, TRFAI012, TRFAI014

Assurance examples: ARG003

Source surfaces: guideline, url

Risk axes: source_support, medication_safety

Release gate levels: L1, L3

Routing decision: needs_source_review

Claim hazard: guideline, URL, and benchmark wording can look authoritative before exact source support is checked

Public use boundary: use as a synthetic source review queue example only

Track A value: Turkish medical LLM source discipline route for clinician literacy and national safety discussion.

Track B value: Reusable SourceCheckup bridge for unsupported guideline and benchmark wording in open medical AI evaluation.

Next public action: add contributor examples that rewrite unsupported guideline certainty into source review language

### STM002: Medication safety source and clinician review route

SourceCheckup rows: SCQ_002, SCQ_009

TR MedLLM rows: TRFAI001, TRFAI010, TRFAI011, TRFAI014

Assurance examples: ARG002

Source surfaces: doi, guideline

Risk axes: medication_safety, missing_context

Release gate levels: L1, L2

Routing decision: needs_clinician_source_review

Claim hazard: medication advice becomes unsafe when source support, renal function, pregnancy context, dose context, and clinician review are missing

Public use boundary: use as synthetic medication safety stop rule material only

Track A value: Turkish assurance lab stop rule for medication safety before any patient facing reuse.

Track B value: Open source medical AI review route for medication safety source and clinician gates.

Next public action: add a medication safety source review worksheet with synthetic prompts and blocked phrases

### STM003: Red flag escalation and locator support route

SourceCheckup rows: SCQ_003

TR MedLLM rows: TRFAI003, TRFAI009

Assurance examples: ARG001

Source surfaces: pmid

Risk axes: false_reassurance, rare_danger

Release gate levels: L1, L2

Routing decision: needs_clinician_review

Claim hazard: a PubMed style locator cannot justify triage reassurance unless the exact source and claim support are checked

Public use boundary: use as synthetic red flag escalation review material only

Track A value: Turkish clinician safety route for urgent escalation boundaries.

Track B value: Failure Atlas bridge route for false reassurance and source locator review.

Next public action: add a red flag wording checklist for clinician review queue rows

### STM004: Policy and national route wording boundary

SourceCheckup rows: SCQ_005, SCQ_011

TR MedLLM rows: TRFAI006, TRFAI008

Assurance examples: ARG006

Source surfaces: policy

Risk axes: over_treatment, workflow_mismatch

Release gate levels: L3, L4, L5

Routing decision: blocked_official_or_deployment_claim

Claim hazard: policy, sandbox, pilot, and official route wording can imply access or endorsement without written evidence

Public use boundary: use as public evaluation infrastructure wording only

Track A value: Turkish national route wording gate that keeps sandbox readiness separate from sandbox access claims.

Track B value: Global open source release boundary for policy and deployment language.

Next public action: build lab target packet index only with verified target names and no access claims

### STM005: Communication bias and broad source wording route

SourceCheckup rows: SCQ_006, SCQ_008

TR MedLLM rows: TRFAI005, TRFAI007, TRFAI013

Assurance examples: ARG005

Source surfaces: broad_source_language, none

Risk axes: communication_risk, bias_or_premature_closure

Release gate levels: L2, L3

Routing decision: public_candidate_boundary_ready

Claim hazard: generic study language and reassuring style can hide missing danger variables

Public use boundary: use as synthetic communication and bias review material only

Track A value: Turkish clinician literacy route for keeping warning signs and missing variables visible.

Track B value: Failure Atlas public wording route for communication risk and bias review.

Next public action: add public contributor rows for safe rewrite examples

### STM006: Data provenance and real world evidence boundary

SourceCheckup rows: SCQ_007

TR MedLLM rows: TRFAI004

Assurance examples: ARG004

Source surfaces: evidence

Risk axes: privacy_or_provenance

Release gate levels: L0, L1

Routing decision: blocked_data_provenance_claim

Claim hazard: a synthetic row must not be described as evidence for real world deployment readiness

Public use boundary: use as synthetic provenance and privacy boundary material only

Track A value: Turkish health data quality route for no patient data release discipline.

Track B value: Health data quality commons bridge for provenance and label audit checks.

Next public action: add label audit workflow table with reviewer roles and escalation gates

### STM007: Positive control source silence route

SourceCheckup rows: SCQ_012

TR MedLLM rows: TRFAI004, TRFAI005

Assurance examples: ARG004, ARG005

Source surfaces: none

Risk axes: privacy_or_provenance, communication_risk

Release gate levels: L0, L2

Routing decision: synthetic_positive_control_only

Claim hazard: a positive control can still become unsafe if readers treat synthetic review text as patient guidance

Public use boundary: use as source silence positive control only

Track A value: Turkish clinician literacy control row that separates source silence from patient advice.

Track B value: SourceCheckup calibration route for examples with no external source claim.

Next public action: keep positive controls visible in future review queues

## Boundary checks

1. Every route uses synthetic examples only.
2. Patient data is not used.
3. Local routing is not clinical truth, source truth, model safety, or deployment readiness.
4. Policy, sandbox, pilot, official route, and deployment language remains blocked without written evidence and explicit clearance.
5. SourceCheckup routing is a review path, not proof that a source or medical claim is true.
6. This map does not rank models and does not claim benchmark compatibility.

## Public files

1. JSON source: `docs/sourcecheckup_tr_medllm_assurance_routing_map_v0_1.json`
2. Generated map: `docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md`
3. Validator: `scripts/validate_sourcecheckup_tr_medllm_assurance_routing_map_v0_1.py`
4. Runnable target: `make sourcecheckup_tr_medllm_routing`
