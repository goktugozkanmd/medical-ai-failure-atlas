# Turkish Medical LLM Coverage Pressure Addendum

Date: 2026 06 19

Status: public coverage pressure addendum for Turkish medical LLM safety work.

Purpose: connect global medical benchmark pressure with Turkish language evaluation pressure without claiming that Turkish clinical coverage already exists, without ranking models, and without presenting any clinical validation.

This addendum is not a Turkish medical LLM benchmark, not a benchmark result, not a model ranking, not a leaderboard, not a score certificate, not source truth certification, not clinical validation, not clinical deployment, not patient data access, not regulated data access, not institutional approval, not partner status, not a formal application, not payment, not terms acceptance, and not endorsement.

## Start state

Live BAGLAM2 and portfolio trackers were read before build. Active Gmail outreach threads and targeted Gmail searches were checked before build. No new route owner reply was found. The prior Hacettepe acknowledgement remains the only reply and is not endorsement, validation, partnership, institutional support, official role, official course, hospital adoption, or clinical clearance.

## Why this addendum exists

Global medical AI evaluation is moving toward clinical text, realistic health conversations, rubric based assessment, and multilingual pressure. Turkish LLM evaluation is also developing, but general Turkish language evaluation does not by itself prove Turkish medical LLM safety coverage. A public Turkish medical LLM safety surface should therefore state what is covered, what is missing, and what must stop until evidence exists.

## Source pressure

### Source 1: BRIDGE

Source: https://www.nature.com/articles/s41551-026-01719-2

Checked signal: the article published on 17 June 2026 describes BRIDGE as a multilingual benchmark with 87 tasks from 59 real world clinical data sources across 9 languages, 8 task types, and 14 clinical specialties. The article also points to open data, leaderboard access, and evaluation code surfaces.

Coverage pressure: Turkish medical LLM work should not claim real clinical text coverage, clinical specialty coverage, or workflow coverage unless the exact Turkish source surface and access boundary are verified.

### Source 2: HealthBench

Source: https://openai.com/tr-TR/index/healthbench/

Checked signal: HealthBench is presented in Turkish as a health AI evaluation with 5000 realistic health conversations, custom physician written rubrics, 262 physicians from 60 countries, multilingual and multi turn scenarios, and criteria that include global health and uncertainty handling.

Coverage pressure: Turkish medical LLM work should separate Turkish language ability from health specific safety behavior, uncertainty handling, clinician review, and global health context.

### Source 3: TurkBench

Source: https://arxiv.org/html/2601.07020v1

Checked signal: TurkBench is described as a Turkish language benchmark with 8151 data samples across 21 subtasks and six evaluation categories, with human expert validation for correctness, language grammar, and cultural sensitivity. The paper states that existing Turkish LLM resources focus mainly on exam style tasks or omit open ended instruction following, safety and content moderation, and fine grained grammar and vocabulary control.

Coverage pressure: Turkish language evaluation can provide useful language and culture pressure, but it does not automatically clear medical source support, clinical risk, data provenance, clinician review, or deployment wording.

### Source 4: Turkish MMLU article

Source: https://arxiv.org/html/2508.13044v1

Checked signal: this article states that evaluating LLM capability remains challenging for resource limited languages such as Turkish, and that Turkish morphology and syntax create evaluation challenges that are often missed by criteria centered on widely used languages.

Coverage pressure: Turkish medical LLM work needs a language reviewer gate because tokenization, morphology, terminology, and meaning drift can change medical safety review even before a clinical reviewer sees the answer.

## Coverage pressure checklist

### TCPA001: Turkish language presence

Question: is Turkish language support present in the evaluated artifact?

Evidence needed: explicit Turkish prompt, Turkish answer, Turkish source, Turkish reviewer note, or Turkish evaluation row.

Blocked claim: Turkish medical safety coverage.

Allowed wording: Turkish language presence is recorded and medical safety coverage is not established.

Stop condition: do not call the row Turkish medical coverage until medical context and review route are present.

### TCPA002: Medical domain scope

Question: does the row concern medical information, health workflow, patient facing advice, clinician facing work, or health data?

Evidence needed: domain scope note and risk axis.

Blocked claim: general Turkish score proves medical readiness.

Allowed wording: general Turkish language evidence does not by itself establish medical readiness.

Stop condition: do not reuse general Turkish language results as medical safety evidence.

### TCPA003: Clinical context

Question: is there a clear clinical setting, user role, and intended use boundary?

Evidence needed: user role, care setting, urgency state, and intended use boundary.

Blocked claim: clinical workflow readiness.

Allowed wording: clinical context is unresolved.

Stop condition: do not publish as workflow ready until setting and user role are defined.

### TCPA004: Source support

Question: does the answer cite or depend on a source, guideline, paper, policy, or local protocol?

Evidence needed: exact source support, population, date, and scope.

Blocked claim: source truth certification.

Allowed wording: source support requires exact review.

Stop condition: do not publish as source supported until the exact claim is checked.

### TCPA005: Turkish terminology risk

Question: could Turkish morphology, abbreviation, synonym choice, tone, or term drift change clinical meaning?

Evidence needed: language reviewer note and unsafe ambiguity note.

Blocked claim: translation safe.

Allowed wording: language review is required before safety wording.

Stop condition: do not call translated or Turkish wording safe without language review.

### TCPA006: Clinician review route

Question: does the row require clinician judgment before public safety wording?

Evidence needed: clinician reviewer role type and review question.

Blocked claim: clinical validation.

Allowed wording: clinician review question is identified.

Stop condition: do not call a row clinically safe or unsafe.

### TCPA007: Data provenance

Question: does the row imply patient data, real clinical text, regulated data, or local health data access?

Evidence needed: data boundary and source boundary.

Blocked claim: patient data access.

Allowed wording: data boundary is unresolved or public only.

Stop condition: do not imply patient data or regulated data access.

### TCPA008: Ranking and score boundary

Question: does the row compare models or imply a score?

Evidence needed: explicit statement that no score, rank, or leaderboard claim is being made.

Blocked claim: model ranking.

Allowed wording: this is coverage pressure, not ranking.

Stop condition: do not publish rank, score, or model standing.

### TCPA009: Public route fit

Question: does the row imply official Turkish institutional approval, sandbox access, TÜSEB or TÜBİTAK fit, or partner status?

Evidence needed: written route owner evidence and Goktug clearance.

Blocked claim: official route approval.

Allowed wording: route fit is unresolved.

Stop condition: do not imply application, partner, official role, or institutional support.

## Addendum outputs

1. A Turkish medical LLM coverage row must name language presence, medical scope, clinical context, source support, terminology risk, clinician review route, data provenance, ranking boundary, and public route fit.
2. A row can be public only when it states what is not established.
3. A row must stop when it depends on patient data, clinical validation, clinical deployment, institutional approval, payment, terms, or endorsement.
4. A row must link back to public benchmark pressure issues `#132`, `#133`, and `#134` when benchmark language is used.

## Public use rules

1. Use this addendum to prevent Turkish coverage claims from outrunning evidence.
2. Use this addendum to separate Turkish language capability from Turkish medical safety behavior.
3. Use this addendum to route wording to source review, language review, clinician review, data steward review, governance review, or stop.
4. Do not use this addendum to rank models.
5. Do not use this addendum as clinical validation.
6. Do not use this addendum as proof of Turkish health system readiness.
7. Do not use this addendum as proof of any official route, partner, funding, sandbox, or institutional approval.

## Links

Linked public issues: `#132`, `#133`, and `#134`.

Recommended check:

```bash
make turkish_medical_llm_coverage_pressure_addendum
```
