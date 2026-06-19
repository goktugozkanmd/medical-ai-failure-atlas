# SourceCheckup Medical Turkish Language Source Support Dashboard

Date: 2026 06 19

Status: public dashboard for Turkish language source support review.

Purpose: give maintainers and reviewers one visible dashboard for deciding whether a Turkish medical AI claim needs source review, language review, clinician review, data steward review, governance review, or stop before public release.

This dashboard is not a benchmark result, not a leaderboard, not model ranking, not score certification, not source truth certification, not clinical validation, not clinical deployment, not patient data access, not regulated data access, not procurement evidence, not partner status, not institutional approval, not payment, not terms acceptance, and not endorsement.

## Start state

Live BAGLAM2 and portfolio trackers were read before build. Active Gmail outreach threads and targeted Gmail searches were checked before build. No new route owner reply was found. The prior Hacettepe acknowledgement remains the only reply and is not endorsement, validation, partnership, institutional support, official role, official course, hospital adoption, or clinical clearance.

## Linked public chain

This dashboard follows the SourceCheckup Medical benchmark source support worksheet, the Turkish source support examples, the Turkish medical LLM issue triage examples, and the TÜSEB A4 UM private decision checklist. It does not close any prior issue and does not claim reviewer approval.

## Dashboard rows

### TLSS001: Turkish clinical claim sentence

Primary risk: the Turkish sentence may be stronger than the cited source.

Review owner: source reviewer plus clinician reviewer when the sentence touches care, diagnosis, treatment, risk, benefit, safety, or workflow.

Evidence needed: exact claim support, population boundary, setting boundary, and date check.

Public wording allowed: source support is under review and exact support is not established.

Stop condition: do not call supported until exact support is checked.

### TLSS002: Turkish abbreviation sentence

Primary risk: the abbreviation may have more than one clinical meaning.

Review owner: language reviewer plus clinician reviewer.

Evidence needed: abbreviation expansion, clinical meaning check, and source support check.

Public wording allowed: abbreviation requires expansion before support can be judged.

Stop condition: do not call supported while abbreviation meaning is unresolved.

### TLSS003: Turkish guideline or policy sentence

Primary risk: the sentence may convert context into a rule.

Review owner: source reviewer plus governance reviewer.

Evidence needed: exact policy text, scope, date, jurisdiction, and whether the policy applies to medical AI claims.

Public wording allowed: source gives context and does not establish operational approval.

Stop condition: do not call compliant, approved, or ready.

### TLSS004: Turkish benchmark adjacent sentence

Primary risk: the sentence may imply compatibility, ranking, score, or validation.

Review owner: benchmark reviewer plus maintainer release decision.

Evidence needed: benchmark scope, item boundary, language boundary, and public wording review.

Public wording allowed: benchmark relationship is not established unless mapped and reviewed.

Stop condition: do not rank, score, or call compatible.

### TLSS005: Turkish hospital readiness sentence

Primary risk: the sentence may imply deployment readiness or hospital adoption.

Review owner: governance reviewer plus clinician reviewer.

Evidence needed: deployment boundary, human review boundary, data boundary, ethics route, and institution authority.

Public wording allowed: readiness is not established and hospital use is outside the public claim.

Stop condition: do not call ready for hospital use.

### TLSS006: Turkish data quality sentence

Primary risk: the sentence may imply patient data clearance or regulated data access.

Review owner: data steward plus governance reviewer.

Evidence needed: data source type, synthetic or public status, deidentification boundary, access authority, and reuse boundary.

Public wording allowed: data quality review is a checklist need, not data clearance.

Stop condition: do not claim patient data clearance or regulated access.

### TLSS007: Turkish education sentence

Primary risk: the sentence may imply official course status or institutional approval.

Review owner: language reviewer plus governance reviewer.

Evidence needed: education scope, audience, role boundary, institution authority, and public wording review.

Public wording allowed: educational preparation surface only.

Stop condition: do not call official curriculum, approved course, or institutional program.

### TLSS008: Turkish release sentence

Primary risk: the release text may silently remove unresolved review gates.

Review owner: maintainer release decision.

Evidence needed: source state, language state, clinical state, data state, governance state, blocked claim list, and explicit unresolved items.

Public wording allowed: release is a public review artifact with unresolved gates.

Stop condition: do not publish a release note that implies closure.

## Dashboard fields

Required fields for each future row:

1. row id
2. Turkish sentence under review
3. English gloss
4. source surface
5. source support state
6. Turkish wording risk
7. clinical scope
8. data boundary
9. reviewer route
10. evidence needed
11. allowed public wording
12. blocked public claim
13. stop condition
14. release state

## Release rules

1. A row can be public only when it contains no patient data, no hidden prompt, no answer key, no private institutional fact, and no private operational decision.
2. A row can be reviewed only when source support and Turkish wording are separated.
3. A row can move forward only when blocked public claims are named.
4. A row must stop when it implies clinical validation, clinical deployment, ranking, score certification, data clearance, institutional approval, partner status, payment, terms acceptance, or endorsement.
5. Silence from outreach threads is not rejection.
6. Acknowledgement from an outreach thread is not endorsement.

## Maintainer command

Run:

```bash
make sourcecheckup_medical_turkish_language_source_support_dashboard
```
