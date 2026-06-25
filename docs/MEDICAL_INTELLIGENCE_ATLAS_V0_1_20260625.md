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

Next build: paired state drift regression set

### mia_mmi_002 Multilingual Medical Intelligence

Artifact: plain clinical language gate

Input: synthetic public explanation

Output: plain language review status

Validator: public wording cannot give diagnosis or treatment instruction

Risk gate: public wording must separate education from care

Next build: public wording drift negative controls

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
