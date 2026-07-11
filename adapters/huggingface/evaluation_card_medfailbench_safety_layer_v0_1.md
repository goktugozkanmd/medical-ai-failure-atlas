# MedFailBench Safety Layer Evaluation Card v0.1

Status: local draft. Not published to Hugging Face as an evaluation card.

## Intended Use

Run synthetic MedFailBench safety prompts through SafetyGuard and publish a clearly bounded evidence card.

## Not Intended Use

1. No clinical advice.
2. No clinical validation.
3. No model ranking.
4. No patient data claim.
5. No official benchmark acceptance claim.
6. No regulatory compliance claim.

## Required Public Fields

1. Prompt set path and version.
2. Model name and date.
3. Scoring method.
4. Worst case safety rows.
5. Unsafe rate.
6. Source support gap count.
7. Human review state.
8. External audit state.

## Local Command

```bash
safetyguard eval --model demo-model --dry-run --limit 5
python3 scripts/export_safetyguard_transparency_card.py \
  --score-file outputs/demo_scores.json \
  --out-json outputs/safetyguard_transparency_card_v0_1.json \
  --out-md outputs/SAFETYGUARD_TRANSPARENCY_CARD_V0_1.md \
  --out-hf-card outputs/HF_EVALUATION_CARD_MEDFAILBENCH_SAFETY_LAYER_V0_1.md
```
