# Medical Intelligence Atlas Coverage Dashboard

Source data: `data/medical_intelligence_atlas_coverage_matrix_v0_1_20260625.json`

Rows: 12

Boundary: this dashboard uses the source coverage data only and does not assert clinical readiness.

## Metadata

| Field | Value |
| --- | --- |
| date | 2026 06 25 |
| matrix_id | medical_intelligence_atlas_coverage_matrix_v0_1_20260625 |
| scope | Medical Intelligence Atlas nodes mapped to existing local stack runtime artifacts |
| source_policy | repo artifact references only |
| status | machine readable repo coverage fixture |

## Status Summary

| Status | Rows |
| --- | --- |
| direct fixture coverage | 12 |

## Layer Coverage

| Layer | Rows | direct fixture coverage |
| --- | --- | --- |
| Agentic Medicine Sandbox | 2 | 2 |
| Clinical State Language | 2 | 2 |
| Clinical Trajectory Engine | 2 | 2 |
| Medical Intelligence Atlas | 2 | 2 |
| Medical Reasoning Verifier | 2 | 2 |
| Multilingual Medical Intelligence | 2 | 2 |

## Open Gaps

No open gaps were found in the source data.

## Coverage Rows

| layer | node_id | coverage_status | node_artifact | stack_runtime_artifact_ids | coverage_focus | local_validation_refs |
| --- | --- | --- | --- | --- | --- | --- |
| Clinical State Language | mia_csl_001 | direct fixture coverage | clinical state record validator | ["csl_schema", "csl_fixture_normalized", "state_language_doc"] | ["required clinical state fields", "normalized synthetic state rows", "missing data and source support fields"] | ["scripts/validate_clinical_state_language_v0_1.py"] |
| Clinical State Language | mia_csl_002 | direct fixture coverage | state transition contract | ["csl_schema", "cte_transition_fixtures", "trajectory_engine_doc"] | ["ordered synthetic states", "risk state change", "prior signal preservation"] | ["scripts/validate_clinical_trajectory_engine_transitions_v0_1.py"] |
| Clinical Trajectory Engine | mia_cte_001 | direct fixture coverage | trajectory row runner | ["cte_seed_set", "stack_config", "trajectory_engine_doc"] | ["twenty synthetic trajectory seed rows", "state count and turn order", "clinical use false boundary"] | ["scripts/validate_clinical_intelligence_stack_20260625.py"] |
| Clinical Trajectory Engine | mia_cte_002 | direct fixture coverage | missing variable pressure test | ["cte_transition_fixtures", "csl_fixture_normalized"] | ["missing variable lists", "transition level missing data pressure", "empty missing data rejection"] | ["scripts/validate_clinical_trajectory_engine_transitions_v0_1.py", "scripts/validate_clinical_state_language_v0_1.py"] |
| Medical Reasoning Verifier | mia_mrv_001 | direct fixture coverage | reasoning trace scorer | ["mrv_examples", "reasoning_verifier_doc"] | ["state completeness", "timeline tracking", "uncertainty handling", "source support", "forbidden claim avoidance"] | ["scripts/score_medical_reasoning_verifier_v0_1.py"] |
| Medical Reasoning Verifier | mia_mrv_002 | direct fixture coverage | source support gate | ["mrv_examples", "stack_config"] | ["source support dimension", "claim support left unresolved unless evidence exists", "public claim boundary"] | ["scripts/score_medical_reasoning_verifier_v0_1.py"] |
| Agentic Medicine Sandbox | mia_ams_001 | direct fixture coverage | agent event protocol | ["ams_event_fixtures", "sandbox_doc"] | ["six agent role sequence", "event payload shape", "safe next agent routing"] | ["scripts/validate_agentic_medicine_sandbox_event_fixtures_v0_1_20260625.py"] |
| Agentic Medicine Sandbox | mia_ams_002 | direct fixture coverage | tool use boundary map | ["ams_event_fixtures", "sandbox_doc"] | ["blocked patient specific action", "source support release gate", "clinical use false boundary"] | ["scripts/validate_agentic_medicine_sandbox_event_fixtures_v0_1_20260625.py"] |
| Multilingual Medical Intelligence | mia_mmi_001 | direct fixture coverage | language context lock | ["csl_fixture_normalized", "mmi_eval_rows", "mmi_paired_state_examples", "mmi_source_check_index", "stack_manifesto"] | ["language context field", "paired Turkish English synthetic state rows", "translation must not add certainty", "missing data and source support preservation"] | ["scripts/validate_multilingual_medical_intelligence_paired_state_examples_v0_1_20260625.py", "scripts/validate_clinical_state_language_v0_1.py", "scripts/validate_clinical_intelligence_stack_20260625.py"] |
| Multilingual Medical Intelligence | mia_mmi_002 | direct fixture coverage | plain clinical language gate | ["mmi_paired_state_examples", "mmi_source_check_index", "mmi_source_check_doc", "stack_manifesto"] | ["plain public wording boundary", "diagnosis and treatment instruction avoidance", "education separated from care", "action boundary preservation across Turkish and English"] | ["scripts/validate_multilingual_medical_intelligence_paired_state_examples_v0_1_20260625.py"] |
| Medical Intelligence Atlas | mia_atlas_001 | direct fixture coverage | node registry | ["atlas_registry", "stack_config", "atlas_markdown"] | ["twelve atlas nodes", "input output validator risk gate and next build fields", "stack layer alignment"] | ["scripts/validate_medical_intelligence_atlas_v0_1_20260625.py", "scripts/validate_clinical_intelligence_stack_20260625.py"] |
| Medical Intelligence Atlas | mia_atlas_002 | direct fixture coverage | release readiness map | ["atlas_registry", "atlas_markdown", "stack_config"] | ["ready blocked and needs source check release states", "validator bounded release status", "machine readable coverage matrix"] | ["scripts/validate_medical_intelligence_atlas_v0_1_20260625.py"] |
