# MedFailBench Automation & Data Pipeline — Core Track (2026-07-08)

> Core track improvement for the Medical AI Failure Atlas.
> Focus: making the eval loop automated, continuous, and product-like.
> Written without external approval — design for G review.

---

## Problem: Why MedFailBench Needs an Automation Layer

MedFailBench has a solid foundation:
- 150 scenario-bank rows, 70 prompts, 10 models evaluated
- 2 Inspect Evals PRs merged upstream
- DOI, HF Space, CI green

But the eval loop is **manual and batch-oriented**:
1. G writes new prompts → manual JSONL entry
2. C0R3 writes Python scripts → manual model API calls
3. Scores computed locally → manual leaderboard update
4. Failure cards drafted by hand → manual HF Space deploy

This doesn't scale. A project that tracks 10 models today needs to track 50 in 3 months. Without automation, the data pipeline becomes a bottleneck.

---

## Solution: 3-Phase Automation Architecture

### Phase 1: CI Pipeline for Scheduled Eval Runs

A GitHub Actions workflow that:
- Runs weekly (Mon 00:00 UTC) or on-demand via `workflow_dispatch`
- Iterates over registered models in `config/models.yaml`
- Calls each model's API with the MedFailBench prompt set
- Scores raw output using rule-based scorer
- Appends results to `leaderboard/results/`

**Key design decisions:**
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Runner | GitHub Actions (ubuntu-latest) | Free, already has CI, Python 3.12 available |
| Model config | YAML file in repo | Extensible, version-controlled |
| API calls | OpenAI-compatible endpoint | All current models use this |
| Scoring | Existing rule-based scorer | Works, just needs pip packaging |
| Output | JSONL with metadata | Append-only, easy to validate |
| HF sync | Separate workflow (manual trigger) | Avoids accidental public push |

**Cost:**
- GH Actions: 2,000 min/month free (more than enough for 10-20 models × 70 prompts)
- API credits: OpenRouter or direct provider keys (G manages)
- Storage: <100MB for output files (years of data)

**Blockers:**
- Python 3.9 local environment vs pyproject 3.10+ — GH Actions runner has 3.12, so this only blocks local dev, not CI
- `safetyguard` package needs `pip install -e .` compatibility verified
- HF_TOKEN needs to be added as GH Actions secret

### Phase 2: Automated Leaderboard Update + Failure Card Generation

After Phase 1 feeds raw eval data into the repo:
- Auto-generate markdown failure cards from worst-case outputs
- Auto-update HF Space leaderboard table
- Auto-detect regression (model gets worse on safety over time)

**Pipeline:**
```
Model API → raw output → score → worst-case filter → card template → HF sync
                                    ↓
                              leaderboard update → commit
```

### Phase 3: Continuous Model Pool Expansion

- Monitor HF model hub for new medical-capable models
- Auto-add to eval list based on clinic-relevant criteria
- Track model version changes and re-eval on major updates

---

## Next Actions for G

No external approval needed for anything here — this is a repo-internal design doc.

1. **Fix Python version:** Upgrade machine to Python 3.12+ or use a venv
2. **Verify SafetyGuard CLI:** `cd repo && python3 -m venv .venv && source .venv/bin/activate && pip install -e . && safetyguard --help`
3. **Choose first Phase 1 model:** Pick 2-3 models for pilot eval run in CI
4. **Add HF_TOKEN to GH secrets** (if not already present)
5. **Review this doc and greenlight Phase 1 implementation**

---

## Automation Roadmap

| Phase | What | When | Depends on |
|-------|------|------|------------|
| 0 | Python 3.12+ env + SafetyGuard verifiable | This week | Machine setup |
| 1 | CI eval workflow for 2-3 models | Next week | Phase 0 |
| 1b | Auto-score + leaderboard commit | Week after | Phase 1 |
| 2 | Failure card auto-generation | TBD | Phase 1b |
| 2b | Automated model pool expansion | TBD | Phase 2 |
| 3 | Competitor monitoring integration | TBD | Phase 2b |