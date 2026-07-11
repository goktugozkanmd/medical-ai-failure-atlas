# SafetyGuard Transparency Card Exporter

Date: 2026 07 08

Status: local exporter implemented.

Purpose: convert a SafetyGuard or Failure Atlas score JSON into a bounded transparency card.

## Command

```bash
python3 scripts/export_safetyguard_transparency_card.py --score-file path/to/model_scores.json
```

## Output

1. JSON transparency card.
2. Markdown transparency card.
3. Worst case item list.
4. Safety gate counts.
5. Boundary flags.

## Boundary

The card is not clinical advice, clinical validation, model ranking, regulatory compliance, certification, or official endorsement.
