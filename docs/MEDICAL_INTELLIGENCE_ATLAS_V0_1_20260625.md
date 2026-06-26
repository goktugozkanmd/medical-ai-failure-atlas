# Medical Intelligence Atlas v0.1

Date: 2026 06 25

Status: repo construction map

## Purpose

Turn Clinical Intelligence Stack from documents into connected build targets with data, validators, risk gates, and next implementation steps.

## Global Boundaries

1. No patient data
2. No clinical validation claim
3. No clinical deployment claim
4. No diagnosis or treatment instruction
5. No model ranking claim
6. No partner or institutional support claim

## Build Nodes

### mia_csl_001 Clinical State Language

Artifact: clinical state record validator

Input: synthetic clinical state object

Output: normalized clinical state object

Validator: clinical state language schema check

Risk gate: missing data must be named before any reasoning step

Next build: canonical sample states with expected failures

### mia_csl_002 Clinical State Language

Artifact: state transition contract

Input: two or more synthetic states

Output: state change summary

Validator: timeline and risk state consistency check

Risk gate: a changed risk state must not erase earlier danger signals

Next build: transition diff tool

### mia_cte_001 Clinical Trajectory Engine

Artifact: trajectory row runner

Input: synthetic trajectory jsonl row

Output: trajectory event list

Validator: state count, turn order, and boundary check

Risk gate: each trajectory must mark synthetic only and clinical use false

Next build: trajectory summary table

### mia_cte_002 Clinical Trajectory Engine

Artifact: missing variable pressure test

Input: trajectory with incomplete state

Output: missing variable list by turn

Validator: missing variable presence check

Risk gate: empty missing variable lists fail the row

Next build: harder missing data fixture set

### mia_mrv_001 Medical Reasoning Verifier

Artifact: reasoning trace scorer

Input: model style reasoning trace on a synthetic case

Output: dimension level pass and fail report

Validator: state completeness, timeline, uncertainty, source support, and boundary checks

Risk gate: a trace cannot pass if it gives clinical use or model ranking claims

Next build: deterministic verifier fixture rows

### mia_mrv_002 Medical Reasoning Verifier

Artifact: source support gate

Input: claim and source support note

Output: supported, partial, or unsupported status

Validator: claim support field cannot be empty

Risk gate: source mention alone does not clear the claim

Next build: source support example bank

### mia_ams_001 Agentic Medicine Sandbox

Artifact: agent event protocol

Input: synthetic agent event

Output: safe next event candidates

Validator: agent role and action boundary check

Risk gate: patient, clinician, test, source, consultant, and follow up roles must stay separate

Next build: event protocol validator

### mia_ams_002 Agentic Medicine Sandbox

Artifact: tool use boundary map

Input: synthetic tool call request

Output: allowed, blocked, or needs human review

Validator: tool call cannot create patient data, payment, or clinical deployment claim

Risk gate: unclear tool action defaults to blocked

Next build: blocked action fixture set

### mia_mmi_001 Multilingual Medical Intelligence

Artifact: language context lock

Input: English and Turkish synthetic clinical wording

Output: language context and ambiguity flags

Validator: language context field must be explicit

Risk gate: translation must not add clinical certainty

Next build: cross language reviewer replay audit trail controls

### mia_mmi_002 Multilingual Medical Intelligence

Artifact: plain clinical language gate

Input: synthetic public explanation

Output: plain language review status, local drift triage report, cross language ambiguity report, negation audience report, scope anchor report, temporal progression report, uncertainty calibration report, source support scope reconciliation report, and source recency applicability report

Validator: public wording cannot give diagnosis or treatment instruction, and rewrite plus cross language reports must remain local fixture only

Risk gate: public wording must separate education from care

Next build: cross language reviewer replay audit trail controls

### mia_mmi_003 Multilingual Medical Intelligence

Artifact: cross language negation and audience role controls

Input: synthetic Turkish English negation and audience role control rows

Output: negation inversion and audience role drift report

Validator: negation and audience role report must remain local fixture only and must block role shift or warning inversion signals

Risk gate: translation must not invert warnings or shift who is being addressed

Next build: cross language reviewer replay audit trail controls

### mia_mmi_004 Multilingual Medical Intelligence

Artifact: cross language scope anchor controls

Input: synthetic Turkish English scope anchor control rows

Output: scope anchor drift report

Validator: scope anchor report must remain local fixture only and must block missing variable erasure, actor role change, action boundary drift, or local context detachment

Risk gate: translation must not detach missing variables, actor role, action boundary, or local context from the same record

Next build: cross language reviewer replay audit trail controls

### mia_mmi_005 Multilingual Medical Intelligence

Artifact: cross language temporal progression controls

Input: synthetic Turkish English temporal progression control rows

Output: temporal progression drift report

Validator: temporal progression report must remain local fixture only and must block duration shift, sequence reversal, follow up timing removal, interval precision loss, or care instruction creation

Risk gate: translation must not shift duration, reverse sequence, remove follow up timing, lose interval precision, or create care instructions

Next build: cross language reviewer replay audit trail controls

### mia_mmi_006 Multilingual Medical Intelligence

Artifact: cross language uncertainty calibration controls

Input: synthetic Turkish English uncertainty calibration control rows

Output: uncertainty calibration drift report

Validator: uncertainty calibration report must remain local fixture only and must block confidence inflation, uncertainty marker removal, evidence gap closure, reviewer state downgrade, or confidence score creation

Risk gate: translation must not inflate confidence, remove uncertainty, close unresolved evidence, downgrade reviewer state, or create confidence scores

Next build: cross language reviewer replay audit trail controls

### mia_mmi_007 Multilingual Medical Intelligence

Artifact: cross language source support scope reconciliation controls

Input: synthetic Turkish English source support scope reconciliation control rows

Output: source support scope reconciliation drift report

Validator: source support scope reconciliation report must remain local fixture only and must block source scope broadening, claim source mapping drift, source limit removal, unsupported source authority creation, or cross language source scope detachment

Risk gate: translation must not broaden source support needs, misalign claim source maps, remove source limits, invent source authority, or detach source scope across languages

Next build: cross language reviewer replay audit trail controls

### mia_mmi_008 Multilingual Medical Intelligence

Artifact: cross language source recency and applicability controls

Input: synthetic Turkish English source recency and applicability control rows

Output: source recency and applicability drift report

Validator: source recency applicability report must remain local fixture only and must block source date shift, recency status inflation, population broadening, setting broadening, or applicability limit removal

Risk gate: translation must not shift source date, inflate recency status, broaden population or setting, or remove applicability limits

Next build: cross language reviewer replay audit trail controls

### mia_mmi_009 Multilingual Medical Intelligence

Artifact: cross language source conflict and provenance controls

Input: synthetic Turkish English source conflict provenance control rows

Output: source conflict provenance drift report

Validator: source conflict provenance report must remain local fixture only and must block source conflict erasure, source version drift, provenance chain break, source attribution detachment, or unsupported conflict resolution

Risk gate: translation must not erase source conflict, drift source version, break provenance chain, detach attribution, or create unsupported conflict resolution

Next build: cross language reviewer replay audit trail controls

### mia_mmi_010 Multilingual Medical Intelligence

Artifact: cross language reviewer conflict triage controls

Input: synthetic Turkish English reviewer conflict triage control rows

Output: reviewer conflict triage routing report

Validator: reviewer conflict triage report must remain local fixture only and must route unresolved source disagreements to reviewer hold, compare, or reject without clearance claims

Risk gate: translation must not remove reviewer hold, collapse compare route, soften reject route, clear unresolved conflict, or relabel triage state as clearance

Next build: cross language reviewer replay audit trail controls

### mia_mmi_011 Multilingual Medical Intelligence

Artifact: cross language reviewer decision rationale controls

Input: synthetic Turkish English reviewer decision rationale control rows

Output: reviewer decision rationale routing report

Validator: reviewer decision rationale report must remain local fixture only and must preserve rationale, reviewer owner, unresolved state, decision boundary, and authority claim absence across reviewer hold, compare, and reject routes

Risk gate: translation must not remove rationale, change reviewer owner, erase unresolved state, broaden decision boundary, or create authority claims

Next build: cross language reviewer replay audit trail controls

### mia_mmi_012 Multilingual Medical Intelligence

Artifact: cross language reviewer handoff packet controls

Input: synthetic Turkish English reviewer handoff packet control rows

Output: reviewer handoff packet routing report

Validator: reviewer handoff packet report must remain local fixture only and must preserve rationale, reviewer owner, unresolved state, route, evidence summary, and authority claim absence across reviewer hold, compare, and reject routes

Risk gate: translation must not remove handoff packet, remove evidence summary, drift route state, drop reviewer owner, or create authority claims

Next build: cross language reviewer replay audit trail controls

### mia_mmi_013 Multilingual Medical Intelligence

Artifact: cross language reviewer handoff replay controls

Input: synthetic Turkish English reviewer handoff replay control rows

Output: reviewer handoff replay reproducibility report

Validator: reviewer handoff replay report must remain local fixture only and must preserve replay packet, recheck trace, appeal context, route owner handoff, route, evidence summary, and authority claim absence across reviewer hold, compare, and reject routes

Risk gate: translation must not remove replay packet, remove recheck trace, remove appeal context, drop route owner handoff, or create authority claims

Next build: cross language reviewer replay audit trail controls

### mia_mmi_014 Multilingual Medical Intelligence

Artifact: cross language reviewer replay audit trail controls

Input: synthetic Turkish English reviewer replay audit trail control rows

Output: reviewer replay audit trail reproducibility report

Validator: reviewer replay audit trail report must remain local fixture only and must preserve replay attempt, comparison result, owner signoff state, unresolved branch, route, and authority claim absence across reviewer hold, compare, and reject routes

Risk gate: translation must not remove audit trail, remove comparison result, remove owner signoff state, erase unresolved branch, or create authority claims

Next build: cross language reviewer replay audit trail closeout controls

### mia_mmi_015 Multilingual Medical Intelligence

Artifact: cross language reviewer replay audit trail closeout controls

Input: synthetic Turkish English reviewer replay audit trail closeout control rows

Output: reviewer replay audit trail closeout reproducibility report

Validator: reviewer replay audit trail closeout report must remain local fixture only and must preserve closeout decision, dissent note, owner final state, closure comparison result, unresolved branch closure boundary, and authority claim absence across reviewer hold, compare, and reject routes

Risk gate: translation must not remove closeout decision, remove dissent note, remove owner final state, erase unresolved branch closure boundary, remove closure comparison result, or create authority claims

Next build: cross language reviewer closeout ledger export controls

### mia_mmi_016 Multilingual Medical Intelligence

Artifact: cross language reviewer closeout ledger export controls

Input: synthetic Turkish English reviewer closeout ledger export control rows

Output: reviewer closeout ledger export reproducibility report

Validator: reviewer closeout ledger export report must remain local fixture only and must preserve closeout decision export, dissent note export, owner final state export, closure comparison result export, unresolved branch closure boundary export, and authority or clearance claim absence across reviewer hold, compare, and reject routes

Risk gate: translation must not remove closeout decision export, remove dissent note export, remove owner final state export, remove closure comparison result export, erase unresolved branch closure boundary export, or create authority or clearance claims

Next build: cross language reviewer closeout ledger reconciliation controls

### mia_mmi_017 Multilingual Medical Intelligence

Artifact: cross language reviewer closeout ledger reconciliation controls

Input: synthetic Turkish English reviewer closeout ledger reconciliation control rows

Output: reviewer closeout ledger reconciliation reproducibility report

Validator: reviewer closeout ledger reconciliation report must remain local fixture only and must match closeout decision, dissent note, owner final state, unresolved branch closure boundary, closure comparison result, and authority or clearance claim absence between source closeout and exported ledger rows

Risk gate: translation must not create closeout decision mismatch, dissent note mismatch, owner final state mismatch, unresolved branch closure boundary mismatch, closure comparison result mismatch, or authority or clearance claims during closeout ledger reconciliation

Next build: cross language reviewer closeout ledger reconciliation exception controls

### mia_mmi_018 Multilingual Medical Intelligence

Artifact: cross language reviewer closeout ledger reconciliation exception controls

Input: synthetic Turkish English reviewer closeout ledger reconciliation exception control rows

Output: reviewer closeout ledger reconciliation exception reproducibility report

Validator: reviewer closeout ledger reconciliation exception report must remain local fixture only and must keep source closeout id, exported ledger row id, owner final state, dissent note, unresolved branch closure boundary, and authority or clearance claim absence attached to reconciliation exceptions

Risk gate: translation must not detach source closeout id, detach exported ledger row id, detach owner final state, detach dissent note, erase unresolved branch closure boundary, or create authority or clearance claims during reconciliation exception handling

Next build: cross language reviewer closeout ledger reconciliation exception replay controls

### mia_mmi_019 Multilingual Medical Intelligence

Artifact: cross language reviewer closeout ledger reconciliation exception replay controls

Input: reconciliation exception rows with recheck and handoff replay state

Output: reproducible exception attachments before recheck and handoff reuse

Validator: replay controls must keep source closeout id exported ledger row id owner final state dissent note unresolved branch closure boundary and authority or clearance claim absence reproducible

Risk gate: exception replay cannot create clearance or close unresolved branch

Next build: cross language reviewer closeout ledger reconciliation exception replay closeout controls

### mia_mmi_020 Multilingual Medical Intelligence

Artifact: cross language reviewer closeout ledger reconciliation exception replay closeout controls

Input: replayed reconciliation exception rows with closeout snapshot state

Output: closed replay exception attachment snapshot before archive reuse

Validator: replay closeout controls must keep source closeout id exported ledger row id owner final state dissent note unresolved branch closure boundary recheck trace handoff trace and authority or clearance claim absence attached

Risk gate: exception replay closeout cannot create clearance or treat unresolved branch closure as authority

Next build: cross language reviewer closeout ledger reconciliation exception replay archive controls

### mia_mmi_021 Multilingual Medical Intelligence

Artifact: cross language reviewer closeout ledger reconciliation exception replay archive controls

Input: closed replay exception attachment rows with archive and reopenability state

Output: reopenable replay exception archive snapshot before rollup reuse

Validator: replay archive controls must keep source closeout id exported ledger row id owner final state dissent note unresolved branch closure boundary recheck trace handoff trace closeout snapshot and authority or clearance claim absence attached while preserving reopenability

Risk gate: exception replay archive cannot create clearance or make archived closeout snapshots unreopenable

Next build: cross language reviewer closeout ledger reconciliation exception replay archive rollup controls

### mia_mmi_022 Multilingual Medical Intelligence

Artifact: cross language reviewer closeout ledger reconciliation exception replay archive rollup controls

Input: archived replay exception attachment rows with rollup summary and reopenability state

Output: reopenable replay exception archive rollup summary before release reuse

Validator: replay archive rollup controls must keep source closeout id exported ledger row id owner final state dissent note unresolved branch closure boundary archive snapshot reopenability and authority or clearance claim absence attached while summarizing archived replay exceptions

Risk gate: exception replay archive rollup cannot create clearance or make archived replay exception summaries unreopenable

Next build: cross language reviewer closeout ledger reconciliation exception replay archive rollup release controls

### mia_mmi_023 Multilingual Medical Intelligence

Artifact: cross language reviewer closeout ledger reconciliation exception replay archive rollup release controls

Input: archived replay exception rollup summary rows with release reuse and reopenability state

Output: reopenable replay exception archive rollup release summary before handoff reuse

Validator: replay archive rollup release controls must keep source closeout id exported ledger row id owner final state dissent note unresolved branch closure boundary archive snapshot reopenability and authority or clearance claim absence attached before release reuse

Risk gate: exception replay archive rollup release cannot create clearance or make released rollup summaries unreopenable

Next build: cross language reviewer closeout ledger reconciliation exception replay archive rollup release handoff controls

### mia_atlas_001 Medical Intelligence Atlas

Artifact: node registry

Input: stack node definition

Output: buildable node with validator and risk gate

Validator: each node needs input, output, validator, risk gate, and next build

Risk gate: a node without a test path is not ready

Next build: atlas coverage dashboard

### mia_atlas_002 Medical Intelligence Atlas

Artifact: release readiness map

Input: node registry and validation logs

Output: ready, blocked, or needs source check

Validator: release state must name blocker or exact next action

Risk gate: public release cannot outrun validators

Next build: machine readable release gate

## Relationships

### Clinical State Language to Clinical Trajectory Engine

trajectory rows contain ordered clinical state records

### Clinical Trajectory Engine to Medical Reasoning Verifier

verifier scores the trace against state change and missing data

### Medical Reasoning Verifier to Agentic Medicine Sandbox

sandbox actions must pass reasoning and boundary gates

### Multilingual Medical Intelligence to Clinical State Language

language context is a first class state field

### Medical Intelligence Atlas to all layers

each layer exposes build targets, validators, and blockers

## Release States

### ready

synthetic data, validator, and boundary text pass

### blocked

missing validator, missing source support, or forbidden claim

### needs source check

public claim depends on external source verification

## Validation Command

`make medical_intelligence_atlas`
