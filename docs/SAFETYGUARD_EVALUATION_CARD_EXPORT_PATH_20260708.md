# SafetyGuard Evaluation Card Export Path

Date: 2026 07 08

Status: local export path.

## What It Does

1. Reads a SafetyGuard score JSON.
2. Builds the transparency card JSON and Markdown.
3. Optionally writes a Hugging Face style evaluation card Markdown file.
4. Keeps public boundary language explicit.

## Command

```bash
python3 scripts/export_safetyguard_transparency_card.py \
  --score-file outputs/demo_scores.json \
  --out-json outputs/safetyguard_transparency_card_v0_1.json \
  --out-md outputs/SAFETYGUARD_TRANSPARENCY_CARD_V0_1.md \
  --out-hf-card outputs/HF_EVALUATION_CARD_MEDFAILBENCH_SAFETY_LAYER_V0_1.md
```

## Local Smoke

```bash
python3 scripts/smoke_safetyguard_card_release_gate_20260708.py
```

The smoke starts a local fake OpenAI compatible server, runs `safetyguard eval`, produces a real score JSON, exports both card formats, and checks that external action remains blocked.

## Boundary

No patient data, no clinical validation claim, no model ranking claim, no registry acceptance claim, and no external publication without owner approval.
