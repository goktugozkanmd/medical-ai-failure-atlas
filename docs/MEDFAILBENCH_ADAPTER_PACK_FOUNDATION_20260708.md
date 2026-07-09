# MedFailBench Adapter Pack Foundation

Date: 2026 07 08

Status: local foundation. Not submitted externally.

Purpose: create a small, inspectable adapter foundation for moving MedFailBench into existing evaluation ecosystems.

## Adapter Targets

| Target | Local artifact | Current state |
| --- | --- | --- |
| Inspect Evals register | `adapters/inspect_evals/register/medfailbench_safety_layer_v0_1.json` | local wrapper package |
| Inspect Evals task | `adapters/inspect_evals/medfailbench_safety_layer_v0_1.py` | dependency gated local wrapper |
| LM Evaluation Harness | `adapters/lm_eval/medfailbench_safety_layer_v0_1.yaml` | local wrapper package |
| LM Evaluation Harness metrics | `adapters/lm_eval/medfailbench_safety_layer_metrics.py` | local metric smoke |
| Framework smoke | `scripts/smoke_adapter_frameworks_20260708.py` | local isolated smoke passed |
| Hugging Face evaluation card | `adapters/huggingface/evaluation_card_medfailbench_safety_layer_v0_1.md` | local draft |
| MedHELM adjacent packet | `docs/MEDHELM_THREE_CASE_UPSTREAM_PACKET_V0_1.md` | local draft |

## Boundary

1. This is not an accepted adapter.
2. This is not an official compatibility claim.
3. This is not clinical validation.
4. This is not a model ranking.
5. This is not a regulatory claim.
6. This does not use patient data.
7. External submission remains blocked until fresh audit and owner approval.

## Next Engineering Work

1. Add a full Inspect run smoke after model selection.
2. Add a SafetyGuard score export path that writes evaluation card fields.
3. Use the transparency card exporter for every demo run.
4. Keep external submission blocked until owner approval and fresh audit.
