# Public platform dashboard index v0.1

Status: public preview.

Date: 2026 06 16

This dashboard is the public entry point for the six seed platforms in the medical AI build portfolio.

It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model safety proof, not a model ranking, not a regulatory claim, not a benchmark compatibility claim, and not an official endorsement.

## Current public coverage

1. 19 synthetic intake rows.
2. 14 Turkish synthetic risk rows.
3. 10 risk axes.
4. 10 of 10 Failure Atlas taxonomy pattern IDs represented.
5. 19 clinician review queue rows.
6. 12 source claim review queue rows.
7. 24 pilot inter rater rows.
8. 150 synthetic scenario rows.
9. 70 prompt rows.
10. 6 clinician literacy release gate lessons.
11. 6 assurance release gate examples.

## Top public entry files

1. [Repository README](../README.md)
2. [TR MedAI Safety Suite preview index](tr%2Dmedai%2Dsafety%2Dsuite/PUBLIC_PREVIEW_INDEX_20260616.md)
3. [TR MedAI Safety Suite release card](tr%2Dmedai%2Dsafety%2Dsuite/PUBLIC_REPO_RELEASE_CARD_20260616.md)
4. [Public infrastructure release note](PUBLIC_RELEASE_NOTE_V0_1_20260616.md)
5. [June roadmap](ROADMAP_2026_06.md)

## Platform map

### 1. TR MedLLM SafetyBench

Current role: Turkish medical language model safety cases for clinical risk, missing context, medication safety, false reassurance, source support, privacy, and communication risk.

Public files:

1. [TR MedLLM synthetic risk pack](../tr_medllm_safetybench/README.md)
2. [TR MedLLM risk rows](../tr_medllm_safetybench/synthetic_risk_pack_v0_1.jsonl)
3. [TR MedLLM specialty spread dashboard](../tr_medllm_safetybench/build/specialty_spread_dashboard_v0_1.md)
4. [Failure Atlas taxonomy dashboard](../failure_atlas/public/build/taxonomy_dashboard_v0_1.md)
5. [Clinician review queue](../failure_atlas/public/build/clinician_review_queue_v0_1.md)

Runnable checks:

```bash
make tr_medllm_pack
make tr_medllm_specialty_spread
make tr_medllm_specialty_dashboard
make taxonomy_dashboard
make clinician_review_queue
```

Track A value: Turkish clinician led evaluation material for national health AI safety, clinician literacy, and assurance review.

Track B value: reusable multilingual safety benchmark seed for global medical AI evaluation without model ranking claims.

Next build: source claim review examples for Turkish rows after maintainer review.

### 2. Medical AI Failure Atlas Global

Current role: public failure mode taxonomy, synthetic case intake workflow, taxonomy dashboard, and clinician review queue.

Public files:

1. [Failure Atlas public index](../failure_atlas/public/INDEX.md)
2. [Failure Atlas methodology](../failure_atlas/public/METHODOLOGY.md)
3. [Case intake checklist](../failure_atlas/public/CASE_INTAKE_CHECKLIST_V0_1.md)
4. [Case intake report](../failure_atlas/public/build/case_intake_report_v0_1.md)
5. [Taxonomy dashboard](../failure_atlas/public/build/taxonomy_dashboard_v0_1.md)
6. [No ranking synthetic report](../leaderboard/build/synthetic_report_v0_1.md)

Runnable checks:

```bash
make case_intake
make taxonomy_dashboard
make clinician_review_queue
make leaderboard_report
```

Track A value: source material for Turkish health AI risk education and assurance gates.

Track B value: global public taxonomy for medical AI failure pattern review and contributor discussion.

Next build: more synthetic failure examples after maintainer review.

### 3. Turkish Clinical AI Assurance Lab

Current role: model card, risk card, data card, source support card, human review card, audit trail, and release gate template.

Public files:

1. [Assurance card template](ASSURANCE_CARD_TEMPLATE_V0_1.md)
2. [Assurance card JSON template](assurance_card_template_v0_1.json)
3. [Assurance governance matrix](tr%2Dmedai%2Dsafety%2Dsuite/ASSURANCE_LAB_TPLC_GOVERNANCE_MATRIX_20260616.md)
4. [MedHELM boundary note](MEDHELM_BOUNDARY_NOTE_V0_1.md)
5. [Medmarks boundary note](MEDMARKS_BOUNDARY_NOTE_V0_1.md)
6. [Assurance release gate example map](ASSURANCE_RELEASE_GATE_EXAMPLE_MAP_V0_1.md)
7. [Assurance release gate example JSON](assurance_release_gate_example_map_v0_1.json)

Runnable checks:

```bash
make assurance_card_template
make assurance_release_gate_map
make boundary_notes
```

Track A value: release gate language for Turkish health AI sandbox readiness discussions without claiming sandbox access.

Track B value: reusable assurance artifact pattern for public medical language model evaluation releases.

Next build: link SourceCheckup dashboard rows back into TR MedLLM specialty and assurance release gates.

### 4. SourceCheckup Medical

Current role: source discipline for medical AI answers, including locator format, source surface, exact claim support, guideline scope, policy jurisdiction, and rewrite routing.

Public files:

1. [SourceCheckup README](../sourcecheckup/README.md)
2. [SourceCheckup workflow example](../sourcecheckup/WORKFLOW_EXAMPLE_20260616.md)
3. [SourceCheckup public demo matrix](sourcecheckup/PUBLIC_DEMO_MATRIX_20260616.md)
4. [Source claim review queue](sourcecheckup/SOURCE_CLAIM_REVIEW_QUEUE_V0_1.md)
5. [SourceCheckup public contributor issue guide](sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md)
6. [SourceCheckup seed report](../sourcecheckup/build/sourcecheckup_seed_report.md)
7. [SourceCheckup v0.2 report](../sourcecheckup/build/source_surface_examples_v0_2_report.md)
8. [SourceCheckup expansion dashboard](../sourcecheckup/build/source_claim_example_expansion_v0_2.md)

Runnable checks:

```bash
make sourcecheckup
make sourcecheckup_v02
make sourcecheckup_contrib_v02
make sourcecheckup_public_issue
make sourcecheckup_expansion_dashboard
make source_claim_queue
```

Track A value: public source support discipline for Turkish medical LLM review examples and clinician AI literacy.

Track B value: open source source quality infrastructure that can grow into source review examples, queues, and contributor workflows.

Next build: link SourceCheckup dashboard rows back into clinician literacy release gates.

### 5. Clinician AI Literacy Academy Turkiye

Current role: practical clinician training surface for safe use, failure recognition, privacy boundaries, source support caution, and AI assisted documentation boundaries.

Public files:

1. [Turkish clinician AI literacy packet](tr%2Dmedai%2Dsafety%2Dsuite/CLINICIAN_AI_LITERACY_30MIN_TR_20260616.md)
2. [Clinician review protocol](CLINICIAN_REVIEW_PROTOCOL_V0_1.md)
3. [Clinician review queue](../failure_atlas/public/build/clinician_review_queue_v0_1.md)
4. [Clinician review states](../failure_atlas/public/clinician_review_states_v0_1.json)
5. [Clinician literacy release gate lesson map](CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md)
6. [Clinician literacy release gate lesson JSON](clinician_literacy_release_gate_lesson_map_v0_1.json)

Runnable checks:

```bash
make clinician_literacy_map
make clinician_review_protocol
make clinician_review_queue
```

Track A value: Turkish clinician literacy material tied to real release gates and synthetic safety cases.

Track B value: clinician review protocol and public review states for global medical AI evaluation workflows.

Next build: connect lesson map outputs into assurance card release gate examples.

### 6. Health Data Quality and Label Audit Commons

Current role: dataset readiness, label quality, provenance, privacy boundary, inter rater review, and release gate checks.

Public files:

1. [Health data quality and label audit card](HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md)
2. [Dataset evaluation card draft](../DATASET_EVALUATION_CARD_V0_1_DRAFT.md)
3. [Data dictionary](../DATA_DICTIONARY.md)
4. [Pilot inter rater review rows](../data/inter_rater_review_subset_v0_1.tsv)
5. [Labeling workflow](../LABELING.md)
6. [Label definition lock](LABEL_DEFINITION_LOCK_V0_1.md)
7. [Labeling package index](LABELING_PACKAGE_INDEX_V0_1.md)

Runnable checks:

```bash
make health_data_quality_card
```

Track A value: data quality and label audit surface for Turkish health AI readiness discussions without patient data use.

Track B value: reusable public checklist for synthetic medical AI dataset release readiness.

Next build: label audit workflow table with reviewer roles and escalation gates.

## Public build order

1. Keep dashboard links and validators green.
2. Link SourceCheckup dashboard rows back into TR MedLLM specialty and assurance release gates.
3. Add lab target packets only after exact target review.

## Visibility rule

Each public update should add at least one runnable check, public issue, generated report, contributor route, review queue, or dashboard surface. Public wording must stay aggressive and useful, but it must not claim patient data use, clinical deployment, clinical validation, model safety proof, model superiority, official status, regulatory approval, sandbox access, or institutional endorsement.
