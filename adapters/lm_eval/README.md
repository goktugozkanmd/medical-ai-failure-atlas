# LM Evaluation Harness Local Wrapper

Status: local wrapper. Not submitted upstream.

Files:

1. `medfailbench_safety_layer_v0_1.yaml`
2. `medfailbench_safety_layer_docs_v0_1.jsonl`
3. `medfailbench_safety_layer_metrics.py`

Boundary:

1. Synthetic prompts only.
2. No patient data.
3. No external submission without owner approval.
4. No upstream acceptance claim.
5. No clinical validation claim.

Local smoke:

```bash
python3 scripts/export_adapter_pack_local_wrappers_20260708.py
python3 scripts/validate_adapter_wrappers_20260708.py
```
