# Benchmark Language Reviewer Handoff Card

Date: 2026 06 19

Status: public reviewer handoff card for benchmark based safety wording.

Purpose: turn the No Ranking Benchmark Misuse Warning into a short reviewer handoff card for any public release, proposal, outreach note, benchmark note, score language, or safety report that mentions benchmark performance.

This card is not a benchmark result, not model comparison, not ranking, not leaderboard, not score certification, not procurement evidence, not clinical validation, not clinical deployment, not patient data, not official compatibility, not an official MedHELM, HealthBench, BRIDGE, OpenAI, CHAI, Joint Commission, hospital, university, regulator, vendor, or partner statement, not payment, and not terms acceptance.

## Source anchors

1. Public issue route

Source: https://github.com/v0id-lab/medical-ai-failure-atlas/issues/124

Use in this card: issue 124 defines the no ranking misuse warning and the ten blocked claim patterns that this card turns into reviewer handoff steps.

2. MedHELM

Source: https://medhelm.org/

Use in this card: benchmark language needs task context, clinical workflow context, calibration, robustness, writing style, and reviewer role.

3. OpenAI HealthBench

Source: https://openai.com/index/healthbench/

Use in this card: rubric based health evaluations need leakage control, source support, uncertainty, and careful public wording.

4. BRIDGE

Source: https://github.com/YLab-Open/BRIDGE

Use in this card: multilingual clinical text evaluation needs language, specialty, document type, care stage, access, and data boundary context.

5. CHAI AI Governance

Source: https://www.chai.org/workgroup/cross-cutting/ai-governance

Use in this card: public benchmark language should connect to governance lanes before safety wording is released.

## Reviewer handoff

### Step 1. Identify the proposed public sentence

Reviewer asks: what exact sentence will appear in public.

Required record: proposed sentence, target surface, intended audience, release owner.

Pass state: sentence is captured exactly.

Block state: sentence is too vague to review.

### Step 2. Name the benchmark surface

Reviewer asks: which benchmark, metric, or score is being mentioned.

Required record: benchmark name, metric name if known, source URL, date checked.

Pass state: benchmark source is named and dated.

Block state: benchmark source is not named.

### Step 3. Convert score language into task language

Reviewer asks: what task, user, care setting, and workflow does the statement actually support.

Required record: task context, user context, care setting, workflow boundary.

Pass state: task context is visible.

Block state: score is still framed as general safety.

### Step 4. Check the blocked claim list

Reviewer asks: does the sentence imply safety proof, procurement evidence, clinical validation, deployment readiness, Turkish representativeness, broad medical coverage, source truth certification, patient data clearance, clinician endorsed safety, or clean benchmark evidence.

Required record: blocked claim decision for each of the ten misuse patterns.

Pass state: every blocked claim is explicitly absent.

Block state: any blocked claim is present or ambiguous.

### Step 5. Request the evidence packet

Reviewer asks: what evidence would a reader need before trusting the public wording.

Required record: task map, source support row, data boundary note, clinical reviewer role, uncertainty statement, release boundary.

Pass state: evidence packet exists or the public sentence is downgraded.

Block state: evidence packet is missing and the sentence still sounds like a safety claim.

### Step 6. Protect examples and hidden test content

Reviewer asks: does the public text copy benchmark examples, answer keys, hidden prompts, or protected test rows.

Required record: example protection statement, contamination check, public safe summary.

Pass state: no protected example content is exposed.

Block state: benchmark example or answer content is exposed.

### Step 7. Add the no ranking wording

Reviewer asks: does the public sentence tell the reader what the benchmark can and cannot show.

Required record: no ranking boundary, uncertainty sentence, source support state.

Pass state: the sentence is limited to readiness, inspection, or reviewer question language.

Block state: the sentence still reads as ranking, superiority, or certified safety.

## Allowed public wording

1. This benchmark signal is used as a reviewer question, not as a safety proof.
2. This score language needs task context, source support, data boundary, clinician reviewer role, and uncertainty before public use.
3. This note does not rank models and does not claim clinical validation.
4. This public wording is limited to benchmark literacy and safety claim hygiene.

## Blocked public wording

1. This model is safe because it scored well.
2. This leaderboard position proves procurement readiness.
3. This benchmark pass validates clinical use.
4. This demo is deployment ready.
5. This English score proves Turkish medical readiness.
6. This average score proves broad medical coverage.
7. This fluent answer is source verified.
8. This benchmark use clears patient data risk.
9. This automated score is clinician endorsed safety.
10. This benchmark result is clean even though example leakage was not checked.

## Minimum pass condition

Do not publish benchmark based safety wording unless the proposed sentence, source, task context, blocked claim review, evidence packet, example protection state, and no ranking boundary are all recorded.

## Public next use

1. Use this card before any public benchmark based safety sentence.
2. Use this card as the handoff object when a clinician, maintainer, reviewer, or collaborator asks what needs to be checked.
3. Pair with the No Ranking Benchmark Misuse Warning, the Hospital AI Governance Intake Worksheet, and the MedHELM HealthBench BRIDGE Compatibility Note.

## Runnable check

```bash
make benchmark_language_reviewer_handoff_card
```
