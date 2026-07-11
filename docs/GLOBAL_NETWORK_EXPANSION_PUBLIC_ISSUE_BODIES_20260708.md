# Global Network Expansion Public Issue Bodies

Date: 2026 07 08

Status: public issue text prepared for the MedFailBench repository.

## issue_inspect_evals_adapter

Goal

Create a small MedFailBench adapter that can be reviewed by people who work with Inspect Evals.

Scope

1. Use synthetic MedFailBench prompts only.
2. Keep the first task small.
3. Return a simple safety score summary from existing SafetyGuard or Failure Atlas scoring code.
4. Document the prompt set, scorer, output fields, and human review state.

Starting files

1. `adapters/inspect_evals/register/medfailbench_safety_layer_v0_1.json`
2. `docs/MEDFAILBENCH_ADAPTER_PACK_FOUNDATION_20260708.md`
3. `safetyguard/cli.py`

Expected contribution

1. A minimal local task wrapper.
2. A smoke run that does not call a paid endpoint by default.
3. A short note listing what still blocks any outside submission.

Boundaries

No patient data. No clinical advice. No clinical validation claim. No model ranking claim. No official compatibility or endorsement claim.

## issue_lm_eval_task

Goal

Create a small LM Evaluation Harness style task for Turkish clinical source support and safety boundary checking.

Scope

1. Use synthetic Turkish clinical prompts only.
2. Start with a tiny task that can be reviewed by maintainers and clinicians.
3. Keep scoring transparent and reproducible.
4. Separate source support, urgent escalation, missing variables, and unsafe precision.

Starting files

1. `adapters/lm_eval/medfailbench_safety_layer_v0_1.yaml`
2. `docs/SOURCECHECKUP_MEDICAL_PRODUCT_PACKET_20260708.md`
3. `tr_medllm_safetybench/`

Expected contribution

1. A task folder shape proposal.
2. Ten synthetic example rows.
3. A local smoke command.
4. A short boundary note for what the task does and does not prove.

Boundaries

No patient data. No clinical advice. No clinical validation claim. No model ranking claim. No official compatibility or endorsement claim.

## issue_transparency_card_mapping

Goal

Map SafetyGuard run outputs into a transparent evidence card that a reviewer can read without running the full repo.

Scope

1. Include model name, date, prompt set, scoring method, worst case safety, unsafe rate, source support gaps, and human review state.
2. Export Markdown and JSON.
3. Keep the card descriptive.
4. Avoid compliance, certification, deployment, or endorsement wording.

Starting files

1. `scripts/export_safetyguard_transparency_card.py`
2. `docs/SAFETYGUARD_TRANSPARENCY_CARD_EXPORTER_20260708.md`
3. `docs/MEDFAILBENCH_SAFETY_ASSURANCE_CARD_V0_1.md`

Expected contribution

1. One improved card field map.
2. One demo card from a dry run.
3. One validator check for required fields.

Boundaries

No patient data. No clinical advice. No clinical validation claim. No model ranking claim. No official compatibility or endorsement claim.

## issue_informatics_route_note

Goal

Identify the best route for a synthetic clinical AI safety review discussion in health informatics communities.

Scope

1. Compare OHDSI, AMIA, and similar health informatics routes.
2. Focus on synthetic safety cases, source support, missing variables, and escalation wording.
3. Propose one bounded contribution that a community member could review.
4. Keep the recommendation evidence based and modest.

Starting files

1. `docs/GLOBAL_NETWORK_EXPANSION_ROADMAP_20260708.md`
2. `docs/GLOBAL_NETWORK_EXPANSION_SOURCE_VERIFICATION_20260708.md`
3. `docs/MEDICAL_AI_BENCHMARK_BOUNDARY_INDEX_20260708.md`

Expected contribution

1. A one page route note.
2. A short list of route owners or public forums, if verified.
3. A first contribution package that uses synthetic examples only.

Boundaries

No patient data. No clinical advice. No membership claim. No invitation claim. No acceptance claim. No endorsement claim.

## issue_china_model_team_run_notes

Goal

Create a clean model team run note format for Chinese and global model teams that may want to test MedFailBench synthetic safety prompts.

Scope

1. Keep the ask to one small synthetic prompt pack.
2. Record model name, date, endpoint or local setup, prompt set, scorer version, and limitations.
3. Make the output useful for Qwen, DeepSeek, Kimi, GLM, Hunyuan, InternLM, MiniMax, and other model teams.
4. Avoid comparative ranking language.

Starting files

1. `docs/CHINA_TURKEY_CLINICAL_AI_SAFETY_COLLAB_CAMPAIGN_20260708.md`
2. `docs/CHINA_TURKEY_COLLAB_SEND_LOG_20260708.md`
3. `docs/CHINESE_FRONTIER_SAFETY_REPORT.md`

Expected contribution

1. A reusable run note template.
2. One synthetic example run note.
3. Clear rules for what a model team can add or challenge.

Boundaries

No patient data. No clinical advice. No clinical validation claim. No model ranking claim. No official compatibility or endorsement claim.

## issue_language_review

Goal

Open a small collaboration route for Turkish, Chinese, and English clinical safety wording review.

Scope

1. Review whether a translated case preserves the same safety risk.
2. Flag unsafe reassurance, missing urgent escalation, unsafe dosing precision, and weak source support.
3. Keep review comments tied to one synthetic case at a time.
4. Prefer concrete wording edits over broad opinions.

Starting files

1. `docs/TR_EN_DRIFT_GLM_PROBE_V0_1.md`
2. `docs/TURKISH_CLINICAL_SAFETYBENCH_PACKAGING_GATE_20260708.md`
3. `data/failure_atlas_external_sample_v0_1.jsonl`

Expected contribution

1. One reviewed synthetic case.
2. One wording risk note.
3. One proposed safer version in the target language.

Boundaries

No patient data. No clinical advice. No clinical validation claim. No model ranking claim. No official compatibility or endorsement claim.
