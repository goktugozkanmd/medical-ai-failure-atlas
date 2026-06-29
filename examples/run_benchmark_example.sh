#!/usr/bin/env bash
set -euo pipefail

python -m failure_atlas.cli run \
  --prompt-set data/prompt_set_v1.tsv \
  --model gpt-4.1-mini \
  --endpoint https://api.openai.com/v1/chat/completions \
  --api-key-env OPENAI_API_KEY \
  --requests-per-minute 30 \
  --out-dir outputs/raw
