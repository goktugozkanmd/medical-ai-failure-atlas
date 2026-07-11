# SafetyGuard Card Release Gate Smoke

Date: 2026 07 08

Status: local smoke passed.

## What It Checks

1. Starts a local fake OpenAI compatible server.
2. Runs `safetyguard eval` against the fake server.
3. Produces a real Failure Atlas score JSON from the SafetyGuard CLI.
4. Exports the SafetyGuard transparency card JSON and Markdown.
5. Exports the HF evaluation card Markdown.
6. Checks that external action stays blocked and local path leakage is absent.

## Command

```bash
python3 scripts/smoke_safetyguard_card_release_gate_20260708.py
```

## Local Artifacts

Manifest: `docs/safetyguard_card_release_gate_smoke_20260708.json`

Generated smoke outputs:

- `build/safetyguard_card_release_gate_20260708/release-gate-demo-model_scores.json`
- `build/safetyguard_card_release_gate_20260708/safetyguard_transparency_card_v0_1.json`
- `build/safetyguard_card_release_gate_20260708/SAFETYGUARD_TRANSPARENCY_CARD_V0_1.md`
- `build/safetyguard_card_release_gate_20260708/HF_EVALUATION_CARD_MEDFAILBENCH_SAFETY_LAYER_V0_1.md`

## Boundary

No external send, no public publication, no Hugging Face publish, no patient data, no clinical validation claim, no model ranking claim, no official endorsement claim, and no physician selection.
