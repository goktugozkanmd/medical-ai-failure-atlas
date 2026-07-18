# OpenCompass Candidate Export

Status: local candidate. Not submitted upstream.

Purpose: keep the 44 case Turkish MedFailBench evidence set in a shape that can be turned into an OpenCompass dataset contribution after maintainer review.

Files:

1. `medfailbench_safety_layer_docs_v0_1.jsonl`
2. `medfailbench_safety_layer_manifest_v0_1.json`

Boundary:

1. Synthetic prompts only.
2. No patient data.
3. No external submission without owner approval.
4. No upstream acceptance claim.
5. No clinical validation claim.
6. No model score or leaderboard claim.

Local smoke:

```bash
python3 scripts/export_opencompass_adapter_candidate_v0_1.py
python3 scripts/validate_opencompass_adapter_candidate_v0_1.py
```
