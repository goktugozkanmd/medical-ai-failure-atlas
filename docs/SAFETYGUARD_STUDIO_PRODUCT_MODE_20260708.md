# SafetyGuard Studio Product Mode

Date: 2026 07 08

Status: local product mode ready.

Roadmap phase: P2 Studio Product Mode.

## Product Surface

Product name: Clinical AI Safety Ops / Health AI Assurance Kit.

Schema: `safetyguard_studio_product_mode_v0_1`.

SafetyGuard Studio now has a guided local product surface for synthetic sample review, manual answer paste review, proof pack inspection, and client side JSON export.

## Boundary

No external send, no provider API call, no automation start, no new case addition, no patient data, no physician selection, no clinical validation claim, no regulatory compliance claim, no official compatibility claim, and no model ranking.

## Features

- `sample_mode`.
- `manual_answer_paste`.
- `client_side_score_json_export`.
- `client_side_assurance_summary_export`.
- `proof_pack_panel`.

## Endpoints

- `/`.
- `/api/examples`.
- `/api/analyze`.
- `/api/proof-pack`.

## Proof Pack

| Artifact | Path | Status |
| --- | --- | --- |
| Health AI Assurance Kit Start Here | `docs/HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md` | `local_start_here_ready` |
| Health AI Assurance Kit roadmap | `docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md` | `p0_to_p7b_completed_p8_blocked` |
| Kit level assurance card | `docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md` | `local_kit_card_ready` |
| SafetyGuard Studio scoring | `safetyguard/studio.py` | `local_product_mode` |
| SourceCheckup Medical review route | `docs/SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md` | `local_cli_report_ready` |
| Transparency card export | `scripts/export_safetyguard_transparency_card.py` | `local_export_ready` |
| Turkish and English drift review | `docs/TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md` | `local_drift_preview_ready` |
| Clinician literacy simulator | `docs/HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md` | `local_demo_index_ready` |
| Monitoring digest schema | `docs/HEALTH_AI_MONITORING_DIGEST_SCHEMA_20260708.md` | `manual_schema_ready_no_automation` |
| Adapter framework smoke | `docs/MEDFAILBENCH_ADAPTER_FRAMEWORK_SMOKE_20260708.md` | `local_framework_smoke_ready` |

## Smoke Result

- Scenario: `STUDIO_PRODUCT_MODE_SMOKE`.
- Result schema: `safetyguard_studio_result_v0_1`.
- Assurance summary schema: `safetyguard_assurance_summary_v0_1`.
- Review status: `local_rule_scoring_only`.

## Next

1. Build P3 SourceCheckup Medical CLI report.
2. Keep all public release, provider call, and physician selection steps blocked until explicit user approval.

## Validation

Run:

```bash
make safetyguard_studio_product_mode_20260708
```
