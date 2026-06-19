# SourceCheckup Medical Benchmark Source Support Worksheet

Date: 2026 06 19

Status: public worksheet for benchmark adjacent source support review.

Purpose: convert BRIDGE, MedHELM, and HealthBench pressure into a SourceCheckup Medical worksheet that separates claim, source, support state, uncertainty, reviewer role, allowed public wording, blocked public claim, escalation route, and stop condition.

This worksheet is not a BRIDGE collaboration claim, not a MedHELM collaboration claim, not an OpenAI or HealthBench collaboration claim, not a benchmark result, not a leaderboard, not model ranking, not score certification, not source truth certification, not clinical validation, not clinical deployment, not patient data access, not regulated data access, not procurement evidence, not partner status, not institutional approval, not payment, not terms acceptance, and not endorsement.

## Start state

Live BAGLAM2 and portfolio trackers were read before build. Active Gmail outreach threads and targeted Gmail searches were checked before build. No new route owner reply was found. The prior Hacettepe acknowledgement remains the only reply and is not endorsement, validation, partnership, institutional support, official role, official course, hospital adoption, or clinical clearance.

## Source pressure

### Source 1: BRIDGE

Source: https://www.nature.com/articles/s41551-026-01719-2

Checked signal: the article published on 17 June 2026 describes BRIDGE as a multilingual benchmark with 87 tasks from 59 real world clinical data sources across 9 languages, 8 task types, and 14 clinical specialties. It also points to open data, leaderboard access, and evaluation code surfaces.

Worksheet pressure: any public source support row should separate source existence from claim support, data access boundary, and public wording decision.

### Source 2: MedHELM

Source: https://medhelm.org/

Checked signal: MedHELM describes an open community led benchmark for medical tasks with 121 clinical tasks, 22 subcategories, 31 datasets, and 5 categories. It reports multiple evaluation dimensions across clinical workflows.

Worksheet pressure: a source support row should name workflow context and reviewer role before public safety wording is used.

### Source 3: HealthBench

Source: https://openai.com/index/healthbench/

Checked signal: HealthBench is described as a benchmark with 5000 realistic health conversations, physician written rubrics, 262 physicians from 60 countries, multilingual and multi turn scenarios, and detailed rubric criteria.

Worksheet pressure: a source support row should distinguish rubric awareness from benchmark compatibility, score report, source truth certification, clinical validation, or clinical deployment.

## Worksheet fields

### Field 1: claim id

Allowed value: stable public identifier.

Evidence needed: identifier only.

Blocked claim: hidden benchmark item or patient case identity.

### Field 2: claim sentence

Allowed value: one public sentence that needs source support review.

Evidence needed: exact sentence under review.

Blocked claim: clinical advice, score proof, ranking, validation, or deployment readiness.

### Field 3: source surface

Allowed value: public URL, public document, public policy page, public article, public benchmark page, or withheld source boundary.

Evidence needed: source type and URL when public.

Blocked claim: source truth certification.

### Field 4: support state

Allowed value: supports exact claim, supports weaker claim, supports context only, does not support, source unavailable, or review pending.

Evidence needed: short support note.

Blocked claim: source support complete when only citation presence exists.

### Field 5: uncertainty state

Allowed value: no major uncertainty, wording uncertainty, scope uncertainty, data boundary uncertainty, reviewer uncertainty, or stop release.

Evidence needed: uncertainty note.

Blocked claim: certainty when scope is unresolved.

### Field 6: reviewer role

Allowed value: clinician reviewer, source reviewer, language reviewer, data steward, governance reviewer, or maintainer.

Evidence needed: named role type, not a person unless permission exists.

Blocked claim: clinician endorsement.

### Field 7: evidence needed

Allowed value: public source support, source absence, scope check, data boundary, reviewer question, label provenance, missingness note, leakage note, or allowed wording.

Evidence needed: checklist items.

Blocked claim: evidence complete with missing source or role.

### Field 8: allowed public wording

Allowed value: cautious public wording that states what the source supports and what remains unresolved.

Evidence needed: support state and uncertainty state.

Blocked claim: benchmark compatibility, source truth certification, clinical validation, clinical deployment, ranking, score certification, procurement evidence, partner, payment, terms, or endorsement.

### Field 9: blocked public claim

Allowed value: exact claim type that must not be published.

Evidence needed: blocked wording note.

Blocked claim: silent release while blocked wording remains.

### Field 10: escalation route

Allowed value: source review, clinician review, language review, data steward review, governance review, maintainer review, owner clearance, or stop.

Evidence needed: route label and reason.

Blocked claim: release readiness without route.

### Field 11: stop condition

Allowed value: do not publish, do not rank, do not submit, do not contact maintainer, do not call ready, or do not reuse until evidence is supplied.

Evidence needed: stop reason.

Blocked claim: public readiness without stop rule.

## Example worksheet rows

### SCSW001: Source existence is not claim support

Claim sentence: this answer cites a guideline.

Source surface: public guideline URL or public citation.

Support state: review pending.

Uncertainty state: scope uncertainty.

Reviewer role: source reviewer.

Evidence needed: exact claim support, population, setting, and date.

Allowed public wording: citation presence is recorded and exact claim support is not yet established.

Blocked public claim: source truth certification.

Escalation route: source review.

Stop condition: do not publish as supported until exact claim support is checked.

### SCSW002: Benchmark page is context only

Claim sentence: this row is benchmark adjacent.

Source surface: BRIDGE, MedHELM, or HealthBench public page.

Support state: supports context only.

Uncertainty state: wording uncertainty.

Reviewer role: governance reviewer.

Evidence needed: source boundary and allowed wording.

Allowed public wording: this row is informed by public benchmark pressure and is not a benchmark result.

Blocked public claim: benchmark compatibility.

Escalation route: maintainer review.

Stop condition: do not publish as a benchmark result or score report.

### SCSW003: Clinical safety wording needs reviewer role

Claim sentence: this output may require clinician review before public wording.

Source surface: public safety note or public benchmark rubric description.

Support state: supports weaker claim.

Uncertainty state: reviewer uncertainty.

Reviewer role: clinician reviewer.

Evidence needed: reviewer question and stop condition.

Allowed public wording: this row identifies a clinician review question.

Blocked public claim: clinical validation.

Escalation route: clinician review.

Stop condition: do not publish as clinically safe or unsafe.

### SCSW004: Real clinical text pressure does not grant data access

Claim sentence: real clinical text benchmarks increase data boundary pressure.

Source surface: BRIDGE public article.

Support state: supports context only.

Uncertainty state: data boundary uncertainty.

Reviewer role: data steward.

Evidence needed: data access boundary and public source state.

Allowed public wording: this row records a data boundary review need.

Blocked public claim: patient data access.

Escalation route: data steward review.

Stop condition: do not imply regulated data access.

### SCSW005: Rubric awareness is not score reporting

Claim sentence: rubric discipline can improve review wording.

Source surface: HealthBench public page.

Support state: supports context only.

Uncertainty state: wording uncertainty.

Reviewer role: maintainer.

Evidence needed: allowed wording and blocked score language.

Allowed public wording: this worksheet borrows rubric discipline without using benchmark content.

Blocked public claim: score certification.

Escalation route: maintainer review.

Stop condition: do not publish as HealthBench compatibility or score report.

### SCSW006: Workflow context is not deployment readiness

Claim sentence: workflow context should be named before safety language.

Source surface: MedHELM public page.

Support state: supports context only.

Uncertainty state: scope uncertainty.

Reviewer role: governance reviewer.

Evidence needed: workflow label and reviewer question.

Allowed public wording: workflow context is recorded before public safety wording.

Blocked public claim: clinical deployment.

Escalation route: governance review.

Stop condition: do not call deployment ready.

## Public use rules

1. Treat source existence and source support as separate states.
2. Treat benchmark public pages as context unless a formal benchmark result is actually present and cleared.
3. Do not copy benchmark examples, answer keys, hidden prompts, protected examples, private clinical text, or patient data.
4. Do not rank models.
5. Do not describe a score as clinical safety.
6. Do not describe leaderboard standing as procurement evidence.
7. Do not describe source support as source truth certification.
8. Do not publish if support state, uncertainty state, reviewer role, allowed wording, blocked claim, escalation route, or stop condition is missing.
9. Link benchmark adjacent SourceCheckup work back to issues #132 and #133.

## Immediate next actions

1. Convert this worksheet into SourceCheckup issue template fields.
2. Add Turkish medical LLM coverage pressure addendum for language, abbreviation, specialty, document type, and care stage.
3. Add clinician reviewer handoff protocol for benchmark adjacent SourceCheckup rows.
4. Add health data label audit card for benchmark adjacent reports.

## Runnable check

```bash
make sourcecheckup_medical_benchmark_source_support_worksheet
```
