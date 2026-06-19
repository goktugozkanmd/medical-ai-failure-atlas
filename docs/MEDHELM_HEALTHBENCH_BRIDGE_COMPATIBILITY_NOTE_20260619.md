# MedHELM HealthBench BRIDGE Compatibility Note

Date: 2026 06 19

Status: public compatibility note for benchmark aware medical AI safety work.

Purpose: connect Medical AI Failure Atlas, SourceCheckup Medical, clinician review, Turkish medical LLM evaluation, and data quality work to three current health AI evaluation surfaces without claiming official compatibility, benchmark submission, leaderboard standing, model ranking, clinical validation, clinical deployment, partner status, official role, endorsement, patient data use, payment, or terms acceptance.

This note is not an official MedHELM, OpenAI HealthBench, or BRIDGE statement. It is not a benchmark result, not a score report, not a model comparison, not a validation study, not a medical device claim, not a regulatory claim, not a clinical recommendation, and not a route access claim.

## Live source anchors

1. MedHELM describes an open community led benchmark for language models on 121 clinical tasks in a clinician validated taxonomy, with 22 subcategories, 31 datasets, and 5 categories. It reports accuracy, calibration, robustness, and writing style across clinical workflows.

Source: https://medhelm.org/

Readiness meaning: a safety portfolio should map failure cases to clinical task type, workflow context, calibration, robustness, writing style, and reviewer role before any public benchmark language is used.

2. MedHELM says the project is open to contributions and tracks issues and suggestions for new test suites, including HealthBench and multi step clinical reasoning.

Source: https://medhelm.org/

Readiness meaning: public work can prepare clear contribution ready notes, but must avoid claiming accepted compatibility or maintainer approval.

3. OpenAI HealthBench describes 5000 realistic health conversations, multilingual and multi turn scenarios, physician written rubric criteria for each conversation, and 48562 unique rubric criteria. OpenAI also asks that examples from the dataset not be revealed online to reduce leakage risk.

Source: https://openai.com/index/healthbench/

Readiness meaning: any public companion note must avoid copying examples, must not expose benchmark items, and should focus on review method, source support, leakage control, and public wording boundaries.

4. BRIDGE describes a multilingual benchmark with 87 real world clinical text tasks across 9 languages and more than one million samples. The repository lists 9 task types, 14 clinical specialties, 7 clinical document types, 20 clinical applications, and 6 clinical stages of patient care.

Source: https://github.com/YLab-Open/BRIDGE

Readiness meaning: Turkish medical AI safety work needs language, specialty, document type, and care stage coverage checks before any local evaluation is described as broad or representative.

5. BRIDGE says open access datasets are released through BRIDGE Open while regulated access clinical datasets cannot be directly published, and it releases task descriptions and original data sources for regulated access parts.

Source: https://github.com/YLab-Open/BRIDGE

Readiness meaning: public work should separate open sample inspection, regulated data boundaries, task descriptions, and source claims. No private clinical data should be included.

## Compatibility lanes

1. Failure mode complement

Public artifact question: Does each row explain the unsafe response pattern rather than only mark a model answer as wrong.

Evidence to prepare: Failure Atlas taxonomy row, risk mechanism note, reviewer question.

Blocked claim: benchmark score.

2. Source support

Public artifact question: Can every public medical or policy claim be traced to a source without implying clinical advice.

Evidence to prepare: SourceCheckup claim row, source URL, support state, uncertainty state.

Blocked claim: source truth certification.

3. Clinician review

Public artifact question: Is clinician review a visible gate for interpretation rather than a decoration after scoring.

Evidence to prepare: reviewer role table, adjudication question, disagreement capture.

Blocked claim: clinical validation.

4. No ranking public reporting

Public artifact question: Does the public output avoid ranking models when the evidence only supports safety inspection.

Evidence to prepare: no ranking wording card, blocked wording log, release note boundary.

Blocked claim: model superiority.

5. Multilingual and Turkish readiness

Public artifact question: Is Turkish language scope treated as a coverage question rather than a translated afterthought.

Evidence to prepare: Turkish specialty spread row, language boundary note, medical terminology review.

Blocked claim: broad Turkish representativeness.

6. Specialty and care stage coverage

Public artifact question: Are specialties, document types, and care stages recorded before broad medical AI claims are made.

Evidence to prepare: specialty spread dashboard, document type label, care stage label.

Blocked claim: general medical coverage.

7. Data quality and label audit

Public artifact question: Are label provenance, leakage, missingness, and regulated data boundaries visible.

Evidence to prepare: label audit row, data quality card, leakage statement, regulated access note.

Blocked claim: patient data clearance.

8. Leakage and example protection

Public artifact question: Does the artifact avoid copying benchmark examples or ground truth into public text.

Evidence to prepare: example protection statement, source summary, public safe paraphrase.

Blocked claim: HealthBench example disclosure.

9. Release boundary

Public artifact question: Can a reader distinguish a public companion note from an official benchmark contribution or submission.

Evidence to prepare: boundary paragraph, issue body, release note, audit record.

Blocked claim: official compatibility.

## Türkiye health AI use

1. Use this note as a bridge between national health AI readiness work and global medical AI benchmark literacy.
2. Pair it with TR MedLLM SafetyBench when Turkish language coverage is the immediate issue.
3. Pair it with SourceCheckup Medical when source support and public claim hygiene are the immediate issue.
4. Pair it with Medical AI Failure Atlas when failure mechanism and reviewer questions are the immediate issue.
5. Pair it with Health Data Quality and Label Audit Commons when data fitness, leakage, missingness, or regulated access boundaries are the immediate issue.
6. Do not use it as a benchmark result, clinical validation, official compatibility statement, leaderboard submission, partner claim, or regulatory evidence.

## Immediate public action queue

1. Convert the nine lanes into a clinician reviewer worksheet that can be reused without patient data.
2. Add a no ranking benchmark misuse warning that names common unsafe public report patterns.
3. Add a Turkish language and specialty spread addendum for local medical LLM evaluation planning.
4. Prepare a future MedHELM issue or discussion reply only if a maintainer response or contribution route makes the target exact.

## Runnable check

```bash
make medhelm_healthbench_bridge_compatibility_note
```
