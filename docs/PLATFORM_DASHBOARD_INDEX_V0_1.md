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
7. 11 SourceCheckup contributor examples.
8. 24 pilot inter rater rows.
9. 150 synthetic scenario rows.
10. 70 prompt rows.
11. 6 clinician literacy release gate lessons.
12. 6 assurance release gate examples.
13. 7 SourceCheckup TR MedLLM assurance routes.
14. 2 source review worksheets.
15. 3 red flag warning checklists.
16. 4 warning sign reviewer roles.
17. 5 escalation gate audit rows.
18. 4 label audit reviewer roles.
19. 5 label audit escalation gate rows.
20. 1 label audit public contributor issue route.
21. 5 label audit example intake rows.
22. 5 label audit example dashboard rows.
23. 5 label audit maintainer triage rows.
24. 5 label audit public wording decision rows.
25. 5 label audit release gate rows.
26. 5 label audit release gate outcome rows.
27. 7 label audit release note packet rows.
28. 3 red flag source locator contributor examples.

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
6. [SourceCheckup TR MedLLM assurance routing map](SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md)

Runnable checks:

```bash
make tr_medllm_pack
make tr_medllm_specialty_spread
make tr_medllm_specialty_dashboard
make sourcecheckup_tr_medllm_routing
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
8. [SourceCheckup TR MedLLM assurance routing map](SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md)
9. [SourceCheckup TR MedLLM assurance routing JSON](sourcecheckup_tr_medllm_assurance_routing_map_v0_1.json)
10. [Source review worksheets](SOURCE_REVIEW_WORKSHEETS_V0_1.md)
11. [Source review worksheets JSON](source_review_worksheets_v0_1.json)
12. [Red flag source locator and warning sign checklist](RED_FLAG_WARNING_CHECKLIST_V0_1.md)
13. [Red flag source locator and warning sign checklist JSON](red_flag_warning_checklist_v0_1.json)
14. [Warning sign reviewer role table](WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md)
15. [Warning sign reviewer role table JSON](warning_sign_reviewer_role_table_v0_1.json)

Runnable checks:

```bash
make assurance_card_template
make assurance_release_gate_map
make sourcecheckup_tr_medllm_routing
make source_review_worksheets
make red_flag_warning_checklist
make warning_sign_role_table
make boundary_notes
```

Track A value: release gate language for Turkish health AI sandbox readiness discussions without claiming sandbox access.

Track B value: reusable assurance artifact pattern for public medical language model evaluation releases.

Next build: add label audit reviewer role table and escalation gate rows.

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
9. [SourceCheckup TR MedLLM assurance routing map](../docs/SOURCECHECKUP_TR_MEDLLM_ASSURANCE_ROUTING_MAP_V0_1.md)
10. [Source review worksheets](../docs/SOURCE_REVIEW_WORKSHEETS_V0_1.md)
11. [Red flag source locator and warning sign checklist](../docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md)
12. [Red flag source locator contributor examples](sourcecheckup/RED_FLAG_SOURCE_LOCATOR_CONTRIBUTOR_EXAMPLES_V0_1.md)
13. [Warning sign reviewer role table](../docs/WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md)

Runnable checks:

```bash
make sourcecheckup
make sourcecheckup_v02
make sourcecheckup_contrib_v02
make sourcecheckup_public_issue
make sourcecheckup_expansion_dashboard
make sourcecheckup_tr_medllm_routing
make source_review_worksheets
make red_flag_warning_checklist
make red_flag_contributor_examples
make warning_sign_role_table
make source_claim_queue
```

Track A value: public source support discipline for Turkish medical LLM review examples and clinician AI literacy.

Track B value: open source source quality infrastructure that can grow into source review examples, queues, and contributor workflows.

Next build: add issue ready source locator example packets after maintainer wording review.

### 5. Clinician AI Literacy Academy Turkiye

Current role: practical clinician training surface for safe use, failure recognition, privacy boundaries, source support caution, and AI assisted documentation boundaries.

Public files:

1. [Turkish clinician AI literacy packet](tr%2Dmedai%2Dsafety%2Dsuite/CLINICIAN_AI_LITERACY_30MIN_TR_20260616.md)
2. [Clinician review protocol](CLINICIAN_REVIEW_PROTOCOL_V0_1.md)
3. [Clinician review queue](../failure_atlas/public/build/clinician_review_queue_v0_1.md)
4. [Clinician review states](../failure_atlas/public/clinician_review_states_v0_1.json)
5. [Clinician literacy release gate lesson map](CLINICIAN_LITERACY_RELEASE_GATE_LESSON_MAP_V0_1.md)
6. [Clinician literacy release gate lesson JSON](clinician_literacy_release_gate_lesson_map_v0_1.json)
7. [Warning sign reviewer role table](WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md)

Runnable checks:

```bash
make clinician_literacy_map
make clinician_review_protocol
make clinician_review_queue
make warning_sign_role_table
```

Track A value: Turkish clinician literacy material tied to real release gates and synthetic safety cases.

Track B value: clinician review protocol and public review states for global medical AI evaluation workflows.

Next build: connect lesson map outputs into assurance card release gate examples.

### 6. Health Data Quality and Label Audit Commons

Current role: dataset readiness, label quality, provenance, privacy boundary, inter rater review, and release gate checks.

Public files:

1. [Health data quality and label audit card](HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md)
2. [Label audit reviewer role table](LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md)
3. [Label audit reviewer role table JSON](label_audit_reviewer_role_table_v0_1.json)
4. [Label audit public contributor issue guide](label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md)
5. [Label audit example intake rows](label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md)
6. [Label audit example intake JSON](label_audit/label_audit_example_intake_v0_1.json)
7. [Label audit example dashboard](label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md)
8. [Label audit example dashboard JSON](label_audit/label_audit_example_dashboard_v0_1.json)
9. [Label audit maintainer triage board](label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md)
10. [Label audit maintainer triage JSON](label_audit/label_audit_maintainer_triage_board_v0_1.json)
11. [Label audit public wording decision log](label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md)
12. [Label audit public wording decision JSON](label_audit/label_audit_public_wording_decision_log_v0_1.json)
13. [Label audit release gate checklist](label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md)
14. [Label audit release gate JSON](label_audit/label_audit_release_gate_checklist_v0_1.json)
15. [Label audit release gate outcome dashboard](label_audit/LABEL_AUDIT_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md)
16. [Label audit release gate outcome JSON](label_audit/label_audit_release_gate_outcome_dashboard_v0_1.json)
17. [Label audit release note packet](label_audit/LABEL_AUDIT_RELEASE_NOTE_PACKET_V0_1.md)
18. [Label audit release note packet JSON](label_audit/label_audit_release_note_packet_v0_1.json)
19. [Label audit GitHub issue template](../.github/ISSUE_TEMPLATE/label_audit_review.yml)
20. [Dataset evaluation card draft](../DATASET_EVALUATION_CARD_V0_1_DRAFT.md)
21. [Data dictionary](../DATA_DICTIONARY.md)
22. [Pilot inter rater review rows](../data/inter_rater_review_subset_v0_1.tsv)
23. [Labeling workflow](../LABELING.md)
24. [Label definition lock](LABEL_DEFINITION_LOCK_V0_1.md)
25. [Labeling package index](LABELING_PACKAGE_INDEX_V0_1.md)

Runnable checks:

```bash
make health_data_quality_card
make label_audit_role_table
make label_audit_public_issue
make label_audit_examples
make label_audit_dashboard
make label_audit_triage
make label_audit_wording_log
make label_audit_release_gates
make label_audit_outcome_dashboard
make label_audit_release_packet
```

Track A value: data quality and label audit surface for Turkish health AI readiness discussions without patient data use.

Track B value: reusable public checklist for synthetic medical AI dataset release readiness.

Next build: add a label audit public changelog after maintainer review.

## Public build order

1. Keep dashboard links and validators green.
2. Add a label audit release gate checklist after maintainer wording review.
3. Add lab target packets only after exact target review.

## Visibility rule

Each public update should add at least one runnable check, public issue, generated report, contributor route, review queue, or dashboard surface. Public wording must stay aggressive and useful, but it must not claim patient data use, clinical deployment, clinical validation, model safety proof, model superiority, official status, regulatory approval, sandbox access, or institutional endorsement.
