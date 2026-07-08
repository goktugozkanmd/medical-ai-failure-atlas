# Health AI Assurance Kit Roadmap

Date: 2026 07 08

Status: canonical big project roadmap.

Project name: Clinical AI Safety Ops / Health AI Assurance Kit.

## Direction

A clinician built safety ops layer that helps inspect worst answers, missed escalation, missing clinical variables, source support, Turkish and English drift, transparency, and public claim hygiene before teams make claims about a medical AI system.

Strategic decision: do not build another broad medical benchmark. Build the safety, assurance, source support, Turkish drift, transparency, clinician literacy, and monitoring layer around existing evaluation ecosystems.

## Boundary

No external send, no provider API call, no automation start, no new case addition, no patient data, no physician selection, no clinical validation claim, no regulatory compliance claim, no official compatibility claim, and no model ranking.

## Product Lanes

| Lane | Purpose | Current artifacts | Next build |
| --- | --- | --- | --- |
| Safety Gap Layer | Inspect worst answers, missed escalation, unsafe reassurance, missing clinical variables, and source support gaps. | `safetyguard/studio.py`, `docs/SAFETYGUARD_STUDIO_PRODUCT_MODE_20260708.md`, `docs/MODEL_RUN_NORMALIZATION_PLAN_20260708.md`, `docs/MODEL_RUN_PROMOTION_GATE_20260708.md`, `docs/LOCAL_LEADERBOARD_DRAFT_PREVIEW_20260708.md`, `docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md` | `clinician_literacy_demo_index` |
| Adapter Distribution Layer | Make the safety layer runnable where evaluators already work. | `adapters/README.md`, `docs/MEDFAILBENCH_LOCAL_ADAPTER_WRAPPERS_20260708.md`, `docs/MEDFAILBENCH_ADAPTER_FRAMEWORK_SMOKE_20260708.md` | `upstream_ready_packet_without_external_submit` |
| SourceCheckup Medical Layer | Separate source presence from exact medical claim support. | `docs/SOURCECHECKUP_MEDICAL_PRODUCT_PACKET_20260708.md`, `docs/SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md`, `docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md`, `docs/sourcecheckup/SOURCECHECKUP_REPO_RUN_GUIDE_V0_1.md`, `sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl` | `included_in_kit_level_card` |
| Turkish and Non English Drift Layer | Track Turkish clinical wording risk, meaning loss, escalation drift, and source support drift. | `docs/TURKISH_CLINICAL_SAFETYBENCH_PACKAGING_GATE_20260708.md`, `docs/TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md`, `docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md`, `data/tr_en_drift_glm_probe_v0_1.tsv`, `data/tr_medllm_synthetic_eval_set_v0_3.jsonl` | `included_in_kit_level_card` |
| Transparency and Assurance Card Layer | Convert evaluation runs into readable evidence cards with limits, prompt set, model version, and review status. | `scripts/export_safetyguard_transparency_card.py`, `docs/SAFETYGUARD_EVALUATION_CARD_EXPORT_PATH_20260708.md`, `docs/SAFETYGUARD_CARD_RELEASE_NOTE_DRAFT_20260708.md`, `docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md`, `docs/HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md` | `start_here_proof_pack_completed` |
| Clinician Literacy Simulator | Turn synthetic failure cases into a short training and demo workflow. | `docs/CLINICAL_AI_LITERACY_SIMULATOR_MODULE_20260708.md`, `docs/HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md`, `docs/HEALTH_AI_SAFETY_OPS_DEMO_FLOW_20260708.md`, `failure_atlas/panel_console.py` | `monitoring_digest_schema` |
| Medical AI Safety Monitoring Layer | Track benchmark, governance, model release, and issue route changes for internal decision support. | `docs/MEDICAL_AI_SAFETY_MONITORING_BOT_PLAN_20260708.md`, `docs/HEALTH_AI_MONITORING_DIGEST_SCHEMA_20260708.md`, `docs/MEDICAL_AI_BENCHMARK_BOUNDARY_INDEX_20260708.md`, `docs/GLOBAL_NETWORK_EXPANSION_ROADMAP_20260708.md` | `p8_external_proof_route_issue_opened` |

## Build Phases

| Phase | Name | Status | Build |
| --- | --- | --- | --- |
| P0 | Product Spine | `completed` | Create a canonical roadmap, lane manifest, and local validation target for the full Health AI Assurance Kit. |
| P1 | Safety Evidence Spine | `completed` | Create local leaderboard draft preview from promoted 30 prompt score files without changing the public leaderboard. |
| P2 | Studio Product Mode | `completed` | Turn SafetyGuard Studio from local scorer into a guided product surface with sample mode, answer paste, and export links. |
| P3 | SourceCheckup Medical CLI | `completed` | Produce a runnable medical claim support report from synthetic answers and optional source locators. |
| P4 | Turkish Drift Preview | `completed` | Create a small Turkish and English drift dashboard with explicit validation tier labeling. |
| P5 | Kit Level Assurance Card | `completed` | Generate one kit level assurance card that links safety gaps, source support, transparency, Turkish drift, and human review status. |
| P6 | Clinician Literacy Demo | `completed` | Package the 20 minute synthetic demo into a reusable local lesson index. |
| P7 | Monitoring Digest | `completed` | Create a manual digest schema before any automation loop is allowed. |
| P7B | Start Here Proof Pack | `completed` | Create one local entry point that maps the roadmap, kit card, product surfaces, language drift, source support, demo, monitoring, and blocked gates. |
| P8 | External Proof Route | `first_public_issue_opened` | Open the first public proof route issue after explicit user approval, with further external actions kept behind separate review. |

## Current Build Focus

Current focus: `p8_external_proof_route_issue_opened`.

Next build step: `p8_followups_need_separate_review`.

## Proof Pack

- SafetyGuard Studio local scoring
- SourceCheckup Medical claim support review
- Transparency card generated from a run
- Turkish and English drift review
- Clinician literacy demo material
- Monitoring digest route
- Start Here proof pack index

## Validation

Run:

```bash
make health_ai_assurance_kit_roadmap_20260708
```
