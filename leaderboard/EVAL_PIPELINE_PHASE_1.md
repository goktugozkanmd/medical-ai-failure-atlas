# MedFailBench Eval CI Pipeline — Phase 1 Implementation

> Reference: `docs/CORE_TRACK_AUTOMATION_DATA_PIPELINE_20260708.md` (design)
> This file: implementation record. G greenlight received on 2026-07-08.

---

## What Phase 1 Delivers

A scheduled GitHub Actions workflow that:
1. Reads model registry from `config/models.yaml`
2. Runs each registered model through the MedFailBench prompt set
3. Scores raw output using the rule-based scorer
4. Optionally commits scored results back to the repo after a manual real run
5. Uploads raw and scored results as GitHub Actions artifacts

Default scheduled runs stay in dry-run mode, so no provider/API credits are spent automatically. Real eval runs require explicit `workflow_dispatch` with `dry_run=false` plus the matching repo secret (`OPENROUTER_API_KEY`, `OPENAI_API_KEY`, or `HF_TOKEN`).

---

## Implementation Status

- [x] `.github/workflows/eval-pipeline.yml` created.
- [x] `scripts/ci_eval_runner.py` created.
- [x] `scripts/ci_score_runner.py` created.
- [x] Dry-run path tested locally without API calls.
- [x] Scoring path tested locally against an existing raw run.
- [x] New pytest coverage passed locally: `tests/test_ci_eval_pipeline.py`.
- [x] GitHub push completed after adding `workflow` scope.
- [x] GitHub workflow_dispatch dry-run passed: run `28929095888`.

## Files Created

### 1. `.github/workflows/eval-pipeline.yml` — Main workflow

Workflow inputs:
- `model_id`: optional single model id from `config/models.yaml`.
- `dry_run`: default true, validates without provider/API calls.
- `prompt_limit`: default 5 prompts per model.
- `commit_results`: commits scored outputs only after a manual real run.

Scheduled runs use the `schedules.weekly` list in `config/models.yaml` and execute dry-run by default. A scheduled real run requires repo variable `EVAL_PIPELINE_ENABLE_SCHEDULE=true`.

### 2. `scripts/ci_eval_runner.py` — Python script for automated eval

Purpose: Accept model ID, provider, and prompt file; call the model API; save raw JSON output compatible with `failure_atlas/scorer.py`.

Key design:
- Accepts `--model`, `--provider`, `--model-name`, `--prompts`, `--output-dir`
- Provider routing: `hf` → HuggingFace Inference API, `openrouter` → OpenRouter API
- Dry-run mode: `--dry-run` prints what would be called without making API calls
- Output: `raw_{model_id}.json` with prompt, response, model_id, timestamp

### 3. `scripts/ci_score_runner.py` — Python script for automated scoring

Purpose: Read raw JSON, apply rule-based rubric, output scored JSON.

- Accepts `--input`, `--output`, `--rubric`
- Uses existing `failure_atlas/scorer.py` scoring logic
- Output: `scored_{model_id}.json` with scores per prompt

---

## Implementation Order

```
Step 1: Create config/models.yaml                        ← DONE (this run)
Step 2: Write scripts/ci_eval_runner.py                  ← DONE
Step 3: Write scripts/ci_score_runner.py                 ← DONE
Step 4: Create .github/workflows/eval-pipeline.yml        ← DONE
Step 5: Test with dry-run                                ← DONE
Step 6: Enable weekly dry-run schedule                   ← DONE
```

---

## Blockers

| Blocker | Type | Resolution |
|---------|------|------------|
| `OPENROUTER_API_KEY` secret | Configuration | Needed only for OpenRouter real runs |
| `OPENAI_API_KEY` secret | Configuration | Needed only for OpenAI real runs |
| `HF_TOKEN` secret | Configuration | Needed only for Hugging Face real runs |
| GitHub Actions readback | Verification | Dry-run passed on GitHub; real provider run still needs secrets and spend approval |

---

## Success Criteria

- [x] `config/models.yaml` exists and validates
- [x] `scripts/ci_eval_runner.py --dry-run` prints planned calls without errors
- [ ] Full run on 1 model produces `leaderboard/results/raw_*.json` and `scored_*.json`
- [ ] Scored results match manual eval format (append-compatible)
- [x] GitHub Actions workflow runs green on `workflow_dispatch` dry-run
- [ ] Weekly schedule triggers correctly

---

## G Onayı Gerekenler

1. Provider secrets for real runs, if not already present in GitHub repo settings.
2. First real eval run target model and prompt limit.
3. Whether scored results should be committed back automatically after real runs.
