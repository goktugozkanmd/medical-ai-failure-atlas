# MedFailBench MedHELM Benchmark Candidate

Status: local MedHELM configurable benchmark candidate. No external submission or endorsement is implied.

## Files

- `prompts/medfailbench_safety_gate_prompt.txt`
- `datasets/medfailbench_safety_gate.csv`
- `config/medfailbench_safety_gate.yaml`
- `run_medfailbench_safety_gate.conf`

## Source

The CSV is exported from:

- `data/scenario_bank_v1.tsv`
- `data/scenario_bank_v2_hard_addendum.tsv`
- `data/scenario_bank_v3_scale_seed.tsv`

Rows: 150 synthetic scenarios. No patient data.

## Run pattern

Requires `crfm-helm >= 0.5.8`.

```bash
cd medhelm-benchmark
export SUITE_NAME=MEDFAILBENCH-SAFETY-GATE-SMOKE
export RUN_ENTRIES_CONF_PATH=./run_medfailbench_safety_gate.conf
export MAX_EVAL_INSTANCES=5
export OUTPUT_PATH=./benchmark_output

helm-run \
  --conf-paths "$RUN_ENTRIES_CONF_PATH" \
  --max-eval-instances "$MAX_EVAL_INSTANCES" \
  --suite "$SUITE_NAME" \
  --output-path "$OUTPUT_PATH"

helm-summarize \
  --auto-generate-schema \
  --suite "$SUITE_NAME" \
  --output-path "$OUTPUT_PATH"
```

## Boundary

This package is a benchmark candidate only. It is not clinical validation, not a model ranking, not an official MedHELM endorsement, and not for clinical use.
