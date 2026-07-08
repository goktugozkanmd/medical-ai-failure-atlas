# Health AI Monitoring Digest Schema

Date: 2026 07 08

Status: manual monitoring digest schema ready.

Roadmap phase: P7 Monitoring Digest.

Product name: Clinical AI Safety Ops / Health AI Assurance Kit.

Schema: `health_ai_monitoring_digest_v0_1`.

## Boundary

Manual only. No external send, no provider API call, no automation start, no paid run, no new case addition, no patient data, no physician selection, no medical advice, no clinical validation claim, no source truth certification claim, no regulatory compliance claim, no official compatibility claim, no institution claim, and no model ranking.

Automation start gate: `owner_must_ask`.

## Schema Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `digest_id` | `true` | Stable row id for a manually reviewed monitoring signal. |
| `date_checked` | `true` | Date when the source was manually checked. |
| `signal_surface` | `true` | Benchmark, model release, governance, source support, language drift, adapter route, repo health, or outreach route. |
| `source_locator` | `true` | Local file path or explicit source pointer used for the row. |
| `observed_change` | `true` | What changed or what needs attention, written as a bounded internal note. |
| `evidence_status` | `true` | local_artifact, official_source_needed, user_approval_needed, blocked, or no_change. |
| `action_meaning` | `true` | What this means for the Health AI Assurance Kit roadmap. |
| `risk_tags` | `true` | Controlled tags such as source_support, language_drift, external_claim, adapter_route, or automation_boundary. |
| `blocked_claims` | `true` | Claims that must not be made from this row. |
| `external_action_gate` | `true` | blocked_without_user_approval for any external post, email, PR, comment, provider run, or institution named claim. |

## Watch Surfaces

| Surface | Local source | Manual question | Allowed action |
| --- | --- | --- | --- |
| `benchmark_and_eval_ecosystem` | `docs/MEDICAL_AI_BENCHMARK_BOUNDARY_INDEX_20260708.md` | Did a benchmark or eval ecosystem signal change the local boundary language? | update internal boundary note |
| `source_support_and_claims` | `docs/SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md` | Did a medical or policy claim need exact source support review? | add internal SourceCheckup review row |
| `turkish_and_non_english_drift` | `docs/TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md` | Did Turkish or English wording drift create a safety review need? | update internal drift note without adding new cases |
| `adapter_and_distribution_routes` | `adapters/README.md` | Did an adapter route need a local wrapper, smoke test, or blocked external packet? | prepare local adapter evidence only |
| `clinician_literacy_and_review` | `docs/HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md` | Did the demo or panel review state need an internal update? | update local demo index or review status only |
| `governance_and_network_routes` | `docs/GLOBAL_NETWORK_EXPANSION_ROADMAP_20260708.md` | Did a governance or network route need a bounded next action? | write a local draft only |
| `repo_health_and_public_claim_hygiene` | `docs/PROJECT_GROWTH_BUILDOUT_INDEX_20260708.md` | Did validators, CI, or public claim hygiene change? | run local QA and update BAGLAM2 |

## Sample Digest Rows

| Id | Surface | Evidence status | Action meaning | External gate |
| --- | --- | --- | --- | --- |
| `HMD001` | `benchmark_and_eval_ecosystem` | `local_index_not_external_claim` | Use benchmark signals as design lenses, not as compatibility or endorsement claims. | `blocked_without_user_approval` |
| `HMD002` | `monitoring_boundary` | `plan_only_automation_not_started` | Keep monitoring as manual digest rows until the owner explicitly asks to start automation. | `blocked_without_user_approval` |
| `HMD003` | `kit_level_evidence` | `local_kit_level_assurance_card_ready` | Use the kit card as the internal anchor for digest interpretation. | `blocked_without_user_approval` |
| `HMD004` | `clinician_literacy_and_review` | `local_clinician_literacy_demo_index_ready` | Route education signals into local demo updates, not external presentation claims. | `blocked_without_user_approval` |
| `HMD005` | `source_support_and_claims` | `local_cli_report_ready` | Any source bearing medical claim should become an internal review row before public wording. | `blocked_without_user_approval` |
| `HMD006` | `turkish_and_non_english_drift` | `local_preview_dashboard_ready` | Language drift signals stay separated by validation tier and do not create new case claims. | `blocked_without_user_approval` |

## Blocked Claims By Row

- `HMD001`: `benchmark_equivalence`, `official_compatibility`, `clinical_validation`, `model_ranking`.
- `HMD002`: `automation_started`, `external_monitoring_active`, `paid_run_allowed`.
- `HMD003`: `clinical_validation`, `source_truth_certification`, `regulatory_compliance`, `model_ranking`.
- `HMD004`: `institution_claim`, `medical_advice`, `clinical_validation`, `physician_selection_by_agent`.
- `HMD005`: `source_truth_certification`, `unsupported_guideline_claim`, `unsupported_policy_claim`.
- `HMD006`: `new_case_validation`, `model_ranking`, `clinical_validation`.

## Source Artifacts

- `monitoring_plan`: `docs/medical_ai_safety_monitoring_bot_plan_20260708.json`.
- `benchmark_boundary_index`: `docs/medical_ai_benchmark_boundary_index_20260708.json`.
- `kit_card`: `docs/health_ai_assurance_kit_card_20260708.json`.
- `clinician_literacy_demo_index`: `docs/health_ai_clinician_literacy_demo_index_20260708.json`.
- `sourcecheckup_cli`: `docs/sourcecheckup_medical_cli_report_20260708.json`.
- `turkish_drift_dashboard`: `docs/turkish_drift_preview_dashboard_20260708.json`.
- `global_network_roadmap`: `docs/GLOBAL_NETWORK_EXPANSION_ROADMAP_20260708.md`.

## Next

1. Connect this schema to the roadmap as P7 completed.
2. Keep P8 external proof route blocked without explicit user approval.
3. Use digest rows only as internal BAGLAM2 style decision support.

## Validation

Run:

```bash
make health_ai_monitoring_digest_schema_20260708
```
