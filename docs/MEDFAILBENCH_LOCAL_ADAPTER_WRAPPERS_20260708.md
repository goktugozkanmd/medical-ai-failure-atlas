# MedFailBench Local Adapter Wrappers

Date: 2026 07 08

Status: local wrapper package. No external submission.

## What Changed

1. Inspect Evals now has a dependency gated local task file and a JSONL dataset export.
2. LM Evaluation Harness now has a concrete YAML task draft, JSONL docs export, and local metric function.
3. A deterministic export script writes both local datasets from the existing synthetic MedFailBench prompt file.
4. A validator checks wrapper files, JSONL rows, metric output, manifest flags, and claim boundaries.
5. A framework smoke script can verify Inspect AI and LM Evaluation Harness in an isolated environment.

## Boundary

1. No patient data.
2. No clinical validation claim.
3. No registry acceptance claim.
4. No model ranking claim.
5. No external submission without owner approval.

## Local Commands

```bash
python3 scripts/export_adapter_pack_local_wrappers_20260708.py
python3 scripts/validate_adapter_wrappers_20260708.py
python3 scripts/smoke_adapter_frameworks_20260708.py --skip-missing
```
