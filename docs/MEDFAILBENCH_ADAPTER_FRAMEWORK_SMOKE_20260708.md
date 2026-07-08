# MedFailBench Adapter Framework Smoke

Date: 2026 07 08

Status: local smoke passed in an isolated Python 3.11 environment.

## Result

1. Inspect AI import and task build passed.
2. Inspect AI local scorer smoke passed with composite score 1.0 on a safe answer.
3. LM Evaluation Harness task validation passed.
4. LM Evaluation Harness dummy run passed on one synthetic item.

## Versions

1. Inspect AI: 0.3.244.
2. LM Evaluation Harness: 0.4.12.
3. Datasets: 5.0.0.

## Boundary

1. No patient data.
2. No external submission.
3. No model ranking.
4. No clinical validation claim.
5. No registry acceptance claim.

## Reproduce

```bash
python3.11 -m venv /tmp/medfailbench_adapter_smoke_20260708
/tmp/medfailbench_adapter_smoke_20260708/bin/python -m pip install inspect-ai lm_eval datasets
/tmp/medfailbench_adapter_smoke_20260708/bin/python scripts/smoke_adapter_frameworks_20260708.py --write-result docs/medfailbench_adapter_framework_smoke_20260708.json
```
