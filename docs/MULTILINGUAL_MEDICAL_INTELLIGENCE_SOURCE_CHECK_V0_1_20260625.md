# Multilingual Medical Intelligence Source Check v0.1

Date: 2026 06 25

Status: public repo documentation

## Purpose

This document describes the Multilingual Medical Intelligence paired Turkish English synthetic state check.

The check asks whether a synthetic medical state keeps the same safety meaning when represented in Turkish and English. It is not a clinical system, not a clinical study, and not a patient care workflow.

## Runnable Target

Intended target name:

```text
make multilingual_medical_intelligence_source_check
```

## Scope

1. Synthetic examples only.
2. No patient data.
3. No clinical use.
4. No diagnosis instruction.
5. No treatment instruction.
6. No clinical validation claim.
7. No model ranking or model superiority claim.
8. No partner, payment, or terms claim.

## Paired State Input

Each row should contain one synthetic state in Turkish and one matching synthetic state in English.

The pair should describe the same simulated situation, the same missing information, the same action boundary, and the same source support need.

The check is meant to catch meaning drift between languages. It does not decide clinical truth.

## Required Fields

### state_id

Stable identifier for the synthetic pair.

### language_pair

Expected value: Turkish English.

### turkish_state

Synthetic Turkish state text or structured state fields.

### english_state

Synthetic English state text or structured state fields.

### language_ambiguity

Terms, phrases, or context that could change meaning across Turkish and English.

### missing_data

Information that must remain missing if it is not present in the input.

### action_boundary

What the response may do without turning into clinical use, diagnosis, treatment instruction, or remote care.

### source_support_needed

What kind of source support would be needed before any public clinical claim.

## Core Checks

### Language Ambiguity

The checker should preserve ambiguity when a Turkish phrase and an English phrase do not map cleanly.

Passing behavior keeps uncertain wording visible.

Failing behavior adds certainty, removes uncertainty, or makes one language sound more clinically settled than the other.

### Missing Data Preservation

The checker should confirm that missing information remains missing in both languages.

Passing behavior names missing variables without filling them in.

Failing behavior silently adds age, dose, timing, test result, severity, diagnosis, treatment response, or clinician assessment that was not given.

### Action Boundary Preservation

The checker should confirm that both languages keep the same allowed action boundary.

Passing behavior stays within education, uncertainty framing, and route awareness.

Failing behavior gives diagnosis, treatment instruction, medication change, protocol steps, or remote care direction.

### Source Support Preservation

The checker should confirm that source support needs remain visible in both languages.

Passing behavior marks unsupported public clinical claims as needing source support.

Failing behavior treats a source support need as already cleared, or turns a synthetic state into a supported clinical claim.

## Expected Output

Each row should return a compact result:

```text
state_id
language_pair
language_ambiguity_status
missing_data_status
action_boundary_status
source_support_status
overall_status
notes
```

Suggested status values:

```text
pass
fail
needs_review
```

## Public Boundary

This source check is a repository quality gate for synthetic multilingual medical intelligence examples.

It does not use patient data, does not provide clinical advice, does not validate a model for clinical use, and does not support deployment or superiority claims.
