# Turkish Medical LLM Coverage Reviewer Intake Rows

Date: 2026 06 19

Status: public reviewer intake rows for Turkish medical LLM coverage review.

Purpose: turn Turkish medical LLM coverage pressure into reviewer intake rows that can be used before any public claim says Turkish medical coverage exists.

This intake is not a Turkish medical benchmark, not a benchmark result, not a leaderboard, not model ranking, not score certification, not source truth certification, not clinical validation, not clinical deployment, not patient data access, not regulated data access, not institutional approval, not partner status, not a formal application, not payment, not terms acceptance, and not endorsement.

## Start state

Live BAGLAM2 and portfolio trackers were read before build. Active Gmail outreach threads and targeted Gmail searches were checked before build. No new route owner reply was found. The prior Hacettepe acknowledgement remains the only reply and is not endorsement, validation, partnership, institutional support, official role, official course, hospital adoption, or clinical clearance.

## Intake source pressure

### Source 1: BRIDGE

Source: https://www.nature.com/articles/s41551-026-01719-2

Checked signal: the article published on 17 June 2026 describes BRIDGE as a multilingual benchmark with 87 tasks from 59 real world clinical data sources across 9 languages, 8 task types, and 14 clinical specialties. It also points to open data, leaderboard, and code surfaces.

Intake pressure: reviewer rows must ask whether Turkish medical work is real clinical text, synthetic safety text, public article text, exam style text, or unsupported language only.

### Source 2: HealthBench

Source: https://openai.com/tr-TR/index/healthbench/

Checked signal: HealthBench is presented in Turkish as a health AI evaluation with 5000 realistic health conversations, custom physician written rubrics, 262 physicians from 60 countries, multilingual and multi turn scenarios, and criteria that include global health and uncertainty handling.

Intake pressure: reviewer rows must ask for the reviewer role, rubric source, uncertainty handling, and whether the row is only a public safety question.

### Source 3: TurkBench

Source: https://arxiv.org/html/2601.07020v1

Checked signal: TurkBench is described as a Turkish language benchmark with 8151 data samples across 21 subtasks and six evaluation categories, with human expert validation for correctness, language grammar, and cultural sensitivity.

Intake pressure: reviewer rows must separate Turkish language and cultural review from medical source support and clinician review.

### Source 4: Turkish MMLU article

Source: https://arxiv.org/html/2508.13044v1

Checked signal: this article states that Turkish morphology and syntax create evaluation challenges that are often missed by criteria centered on widely used languages.

Intake pressure: reviewer rows must ask whether Turkish morphology, abbreviations, suffixes, and terminology shift the medical meaning.

## Reviewer intake rows

### TMI001: Turkish language presence row

Reviewer role: language reviewer.

Reviewer question: is the row actually Turkish, partly Turkish, translated Turkish, or non Turkish?

Evidence needed: prompt language, answer language, and reviewer note.

Allowed public wording: Turkish language presence is recorded.

Blocked public claim: Turkish medical safety coverage.

Stop condition: do not call the row Turkish medical coverage.

### TMI002: Medical scope row

Reviewer role: clinician reviewer.

Reviewer question: does the row concern diagnosis, treatment, triage, medication, discharge, coding, patient education, health data, or workflow?

Evidence needed: medical scope and risk axis.

Allowed public wording: medical scope requires review.

Blocked public claim: general Turkish language score proves medical readiness.

Stop condition: do not reuse general Turkish language evidence as medical evidence.

### TMI003: Clinical context row

Reviewer role: clinician reviewer.

Reviewer question: is the user a patient, clinician, student, maintainer, data steward, or unknown reader?

Evidence needed: user role, setting, urgency, and intended use boundary.

Allowed public wording: clinical context is unresolved.

Blocked public claim: workflow readiness.

Stop condition: do not publish as workflow ready until role and setting are explicit.

### TMI004: Source support row

Reviewer role: source reviewer.

Reviewer question: what exact source supports the medical statement?

Evidence needed: source URL, source type, claim sentence, population, date, and scope.

Allowed public wording: source support is under review.

Blocked public claim: source truth certification.

Stop condition: do not publish as source supported until exact claim support is checked.

### TMI005: Turkish terminology row

Reviewer role: language reviewer.

Reviewer question: could morphology, abbreviation, suffix, synonym, tone, or local term choice change clinical meaning?

Evidence needed: terminology note and unsafe ambiguity note.

Allowed public wording: terminology review is required.

Blocked public claim: translation safe.

Stop condition: do not call Turkish wording safe without language review.

### TMI006: Clinician review row

Reviewer role: clinician reviewer.

Reviewer question: what exact clinician judgment is needed before public wording?

Evidence needed: clinical risk question and reviewer route.

Allowed public wording: clinician review question is identified.

Blocked public claim: clinical validation.

Stop condition: do not call the row clinically safe or unsafe.

### TMI007: Data boundary row

Reviewer role: data steward.

Reviewer question: does the row imply patient data, real clinical text, regulated data, institutional data, or public only data?

Evidence needed: data source boundary and access boundary.

Allowed public wording: data boundary is public only or unresolved.

Blocked public claim: patient data access.

Stop condition: do not imply real patient data or regulated data access.

### TMI008: Ranking boundary row

Reviewer role: governance reviewer.

Reviewer question: does the row compare models, imply a score, or imply leaderboard standing?

Evidence needed: no ranking statement.

Allowed public wording: this is review intake, not ranking.

Blocked public claim: model ranking.

Stop condition: do not publish rank, score, or model standing.

### TMI009: Public route fit row

Reviewer role: maintainer.

Reviewer question: does the row imply official Turkish institutional approval, sandbox access, funding fit, route owner support, or partner status?

Evidence needed: written route evidence and Goktug clearance if action is proposed.

Allowed public wording: route fit is unresolved.

Blocked public claim: official route approval.

Stop condition: do not imply application, partner, official role, institutional support, payment, terms, or endorsement.

### TMI010: Release decision row

Reviewer role: maintainer.

Reviewer question: should the row be public, held for review, rewritten, or stopped?

Evidence needed: reviewer route, allowed wording, blocked claim, and stop condition.

Allowed public wording: public release is limited to the recorded boundary.

Blocked public claim: release ready without reviewer route.

Stop condition: do not release until all blockers are resolved.

## Intake output rule

Every Turkish medical LLM coverage row should produce:

1. Language state.
2. Medical scope.
3. Clinical context.
4. Source support state.
5. Terminology risk.
6. Clinician review question.
7. Data boundary.
8. Ranking boundary.
9. Public route fit.
10. Release decision.

## Public use rules

1. Use these rows before public Turkish medical LLM coverage claims.
2. Use these rows to decide whether review should go to language, source, clinician, data steward, governance, maintainer, or stop.
3. Do not use these rows to rank models.
4. Do not use these rows as clinical validation.
5. Do not use these rows as proof of Turkish health system readiness.
6. Do not use these rows as proof of any official route, partner, funding, sandbox, or institutional approval.
7. Link these rows to issues `#132`, `#133`, `#134`, and `#135` when benchmark coverage language is used.

## Recommended check

```bash
make turkish_medical_llm_coverage_reviewer_intake_rows
```
