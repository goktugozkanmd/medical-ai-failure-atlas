# MedFailBench Eval CI Pipeline — Phase 1 Implementation

> Reference: `docs/CORE_TRACK_AUTOMATION_DATA_PIPELINE_20260708.md` (design)
> This file: implementation-ready plan, ready for G to greenlight.

---

## What Phase 1 Delivers

A scheduled GitHub Actions workflow that:
1. Reads model registry from `config/models.yaml`
2. Runs each registered model through the MedFailBench prompt set
3. Scores raw output using the rule-based scorer
4. Commits scored results back to the repo
5. Generates a summary report

No external API credits needed for models already running (HF-backed models: Qwen 2.5-7B, Llama 3.1-8B). OpenRouter models need `OPENROUTER_API_KEY` secret.

---

## Files to Create

### 1. `.github/workflows/eval-pipeline.yml` — Main workflow

```yaml
name: Eval Pipeline

on:
  schedule:
    - cron: "0 5 * * 1"  # Monday 05:00 UTC
  workflow_dispatch:
    inputs:
      model_id:
        description: 'Specific model to eval (leave empty for all weekly)'
        required: false
        type: string
      dry_run:
        description: 'Dry run (validate only, no API calls)'
        required: false
        type: boolean
        default: false

permissions:
  contents: write  # Need write to commit results

jobs:
  # Job 1: Resolve which models to run
  resolve-models:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.resolve.outputs.matrix }}
      report_exists: ${{ steps.resolve.outputs.report_exists }}
    steps:
      - uses: actions/checkout@v4
      - id: resolve
        run: |
          python3 <<'PY'
          import json, yaml, os, sys
          
          with open('config/models.yaml') as f:
              config = yaml.safe_load(f)
          
          model_id = os.environ.get('INPUT_MODEL_ID', '')
          dry_run = os.environ.get('INPUT_DRY_RUN', 'false') == 'true'
          
          if model_id:
              # Single model specified
              models = [m for m in config['models'] if m['id'] == model_id]
          else:
              # Weekly schedule
              weekly_ids = config['schedules']['weekly']
              models = [m for m in config['models'] if m['id'] in weekly_ids and m['active']]
          
          matrix = json.dumps({'model': [m['id'] for m in models], 'include': [
              {'model': m['id'], 'provider': m['provider'], 'model_name': m['model']}
              for m in models
          ]})
          print(f'matrix={matrix}')
          print(f'report_exists={os.path.exists("leaderboard/results/")}')
          
          PY
        env:
          INPUT_MODEL_ID: ${{ github.event.inputs.model_id || '' }}
          INPUT_DRY_RUN: ${{ github.event.inputs.dry_run || 'false' }}

  # Job 2: Evaluate each model (parallel matrix)
  eval:
    needs: resolve-models
    if: ${{ needs.resolve-models.outputs.matrix != '{"model":[],"include":[]}' }}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix: ${{ fromJson(needs.resolve-models.outputs.matrix) }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          python -m pip install -e .
          python -m pip install pyyaml
      - name: Run eval
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          python scripts/ci_eval_runner.py \
            --model ${{ matrix.model }} \
            --provider ${{ matrix.provider }} \
            --model-name "${{ matrix.model_name }}" \
            --prompts leaderboard/medfailbench_prompts_v0_2.jsonl \
            --output-dir leaderboard/results/
      - name: Score results
        run: |
          python scripts/ci_score_runner.py \
            --input leaderboard/results/raw_${{ matrix.model }}.jsonl \
            --output leaderboard/results/scored_${{ matrix.model }}.json \
            --rubric failure_atlas/rubric.json

  # Job 3: Commit results back
  commit:
    needs: [resolve-models, eval]
    if: ${{ always() && needs.resolve-models.result != 'skipped' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Configure git
        run: |
          git config user.name "C0R3 Bot"
          git config user.email "bot@c0r3.dev"
      - name: Commit eval results
        run: |
          git add leaderboard/results/
          git diff --cached --quiet || \
            git commit -m "chore: automated eval results $(date +%Y-%m-%d)"
          git push
```

### 2. `scripts/ci_eval_runner.py` — Python script for automated eval

Purpose: Accept model ID, provider, and prompt file; call the model API; save raw JSONL output.

Key design:
- Accepts `--model`, `--provider`, `--model-name`, `--prompts`, `--output-dir`
- Provider routing: `hf` → HuggingFace Inference API, `openrouter` → OpenRouter API
- Dry-run mode: `--dry-run` prints what would be called without making API calls
- Output: `raw_{model_id}.jsonl` with prompt, response, model_id, timestamp

### 3. `scripts/ci_score_runner.py` — Python script for automated scoring

Purpose: Read raw JSONL, apply rule-based rubric, output scored JSON.

- Accepts `--input`, `--output`, `--rubric`
- Uses existing `failure_atlas/scorer.py` scoring logic
- Output: `scored_{model_id}.json` with scores per prompt

---

## Implementation Order

```
Step 1: Create config/models.yaml                        ← DONE (this run)
Step 2: Write scripts/ci_eval_runner.py                  ← needs G greenlight
Step 3: Write scripts/ci_score_runner.py                 ← needs G greenlight
Step 4: Create .github/workflows/eval-pipeline.yml        ← needs G greenlight
Step 5: Test with dry-run on 1 model                     ← needs G greenlight
Step 6: Enable weekly schedule                           ← needs G greenlight
```

---

## Blockers

| Blocker | Type | Resolution |
|---------|------|------------|
| `OPENROUTER_API_KEY` secret | Configuration | G adds to GH repo secrets |
| `HF_TOKEN` secret | Configuration | Check if already set |
| Python 3.12 compatibility | Verification | Test run on GH Actions |
| `failure_atlas/scorer.py` standalone | Dependency | Check if it runs without other modules |

---

## Success Criteria

- [ ] `config/models.yaml` exists and validates
- [ ] `scripts/ci_eval_runner.py --dry-run` prints planned calls without errors
- [ ] Full run on 1 model produces `leaderboard/results/raw_*.jsonl` and `scored_*.json`
- [ ] Scored results match manual eval format (append-compatible)
- [ ] GitHub Actions workflow runs green on `workflow_dispatch`
- [ ] Weekly schedule triggers correctly

---

## G Onayı Gerekenler

1. Phase 1 implementation: scripts + workflow YAML
2. `OPENROUTER_API_KEY` addition to GH secrets
3. Whether to start with dry-run mode or full eval