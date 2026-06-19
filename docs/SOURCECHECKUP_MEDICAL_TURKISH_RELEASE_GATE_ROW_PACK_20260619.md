# SourceCheckup Medical Turkish Release Gate Row Pack

Date: 2026 06 19

Status: public row pack for Turkish release gate review.

Purpose: turn the Turkish language source support dashboard into reusable release gate rows that maintainers can copy before publishing Turkish medical AI safety notes.

This row pack is not a benchmark result, not a leaderboard, not model ranking, not score certification, not source truth certification, not clinical validation, not clinical deployment, not patient data access, not regulated data access, not procurement evidence, not partner status, not institutional approval, not payment, not terms acceptance, and not endorsement.

## Start state

Live BAGLAM2 and portfolio trackers were read before build. Active Gmail outreach threads and targeted Gmail searches were checked before build. The only inbound reply remains the Hacettepe health informatics acknowledgement that the material will be reviewed. That acknowledgement is not endorsement, validation, partnership, institutional support, official role, official course, hospital adoption, or clinical clearance.

## How to use this row pack

Each row is a release gate. A row can move toward public release only when the required evidence fields are filled and blocked claims are removed.

Required action for every row:

1. copy the row type
2. paste the Turkish sentence under review
3. write a plain English gloss
4. name the source surface without adding private material
5. choose a source support state
6. write the Turkish wording risk
7. define the clinical scope
8. define the data boundary
9. assign the reviewer route
10. name evidence still needed
11. write allowed public wording
12. write blocked public claims
13. decide the release state

Allowed release states:

1. blocked before public release
2. public as unresolved review artifact
3. public as source support request
4. public after source support checked
5. public after wording risk removed

Do not use this pack to declare a source true, declare a model safe, rank a model, certify a score, approve a clinical workflow, clear patient data, or claim institutional approval.

## Row pack

### RGR001: Turkish clinical claim row

Use when a Turkish sentence touches diagnosis, treatment, prognosis, risk, benefit, safety, triage, or workflow.

Minimum evidence fields:

1. exact source sentence
2. patient group boundary
3. setting boundary
4. care action boundary
5. clinical reviewer route
6. release state

Blocked public claims:

1. clinically validated
2. ready for care
3. safe for patient use
4. source proves clinical safety

Allowed public wording:

The claim is under source and clinical wording review.

### RGR002: Turkish abbreviation row

Use when a Turkish sentence includes an abbreviation with possible multiple meanings.

Minimum evidence fields:

1. abbreviation expansion
2. medical meaning check
3. context sentence
4. language reviewer route
5. clinician reviewer route
6. release state

Blocked public claims:

1. meaning is obvious
2. source support is clear
3. no clinician check needed

Allowed public wording:

The abbreviation needs expansion before source support can be judged.

### RGR003: Turkish guideline or policy row

Use when a Turkish sentence refers to a guideline, policy, regulation, governance note, institutional rule, or public authority surface.

Minimum evidence fields:

1. exact policy text
2. date checked
3. jurisdiction
4. scope boundary
5. governance reviewer route
6. release state

Blocked public claims:

1. compliant
2. approved
3. legally ready
4. official route confirmed

Allowed public wording:

The source gives context and does not establish operational approval.

### RGR004: Turkish benchmark adjacent row

Use when a Turkish sentence mentions benchmark, evaluation, comparison, leaderboard, score, coverage, compatibility, or model quality.

Minimum evidence fields:

1. benchmark surface
2. language boundary
3. item boundary
4. score boundary
5. benchmark reviewer route
6. release state

Blocked public claims:

1. model ranking
2. score certification
3. benchmark compatibility confirmed
4. best model

Allowed public wording:

Benchmark relationship is not established unless mapped and reviewed.

### RGR005: Turkish hospital readiness row

Use when a Turkish sentence could imply hospital use, adoption, procurement, clinical deployment, or workflow readiness.

Minimum evidence fields:

1. deployment boundary
2. human review boundary
3. institution authority boundary
4. ethics route boundary
5. governance reviewer route
6. release state

Blocked public claims:

1. hospital ready
2. adopted by hospital
3. procurement ready
4. ready for clinical deployment

Allowed public wording:

Hospital readiness is not established by this public artifact.

### RGR006: Turkish data quality row

Use when a Turkish sentence touches dataset quality, label quality, data access, public data, synthetic data, deidentification, or reuse.

Minimum evidence fields:

1. data type
2. data source category
3. access authority boundary
4. reuse boundary
5. data steward route
6. release state

Blocked public claims:

1. patient data cleared
2. regulated data access approved
3. labels validated
4. dataset safe for clinical use

Allowed public wording:

Data quality review is a checklist need and is not data clearance.

### RGR007: Turkish education row

Use when a Turkish sentence could imply course status, curriculum status, institutional approval, training approval, or official education role.

Minimum evidence fields:

1. education scope
2. audience boundary
3. role boundary
4. institution authority boundary
5. language reviewer route
6. release state

Blocked public claims:

1. official curriculum
2. approved course
3. institutional program
4. faculty endorsed

Allowed public wording:

This is an educational preparation surface only.

### RGR008: Turkish release note row

Use before a public release note, issue body, issue comment, roadmap note, or repository announcement.

Minimum evidence fields:

1. source state
2. language state
3. clinical state
4. data state
5. governance state
6. unresolved item list
7. release state

Blocked public claims:

1. all gates closed
2. reviewer approved
3. public release means validation
4. acknowledgement means endorsement

Allowed public wording:

The release is a public review artifact with unresolved gates named.

## Maintainer command

Run:

```bash
make sourcecheckup_medical_turkish_release_gate_row_pack
```
