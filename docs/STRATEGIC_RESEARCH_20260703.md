# Strategic Research — 2026-07-03

## Decision

Do not spend strategic-research time on congress/deadline scanning.

The best next strategic move is: **turn MedFailBench into a MedHELM-adjacent clinical safety scenario / adapter project**.

Practical framing:

> MedFailBench is not another medical QA leaderboard. It is a clinician severity and safety-gate layer for failure modes that current medical benchmarks under-measure: missing variables, unsafe escalation wording, weak source support, Turkish clinical wording risk, and overclaiming.

## Why this is the move

### 1. MedHELM is the highest-leverage external anchor

Source: https://medhelm.org/

Observed facts:

- MedHELM is open/community-led and Apache 2.0.
- It covers 121 clinical tasks, 22 subcategories, 31 datasets, 5 categories.
- It explicitly says it accepts contribution through new clinical scenarios, refined LLM-jury prompts, bug reports, proposed metrics, and test-suite requests.
- It targets realistic clinical workflows, not just closed-book medical QA.

Fit for G:

- Strongest alignment with clinician-builder positioning.
- Gives MedFailBench a concrete upstream ecosystem target.
- A scenario/adapter contribution is public, technical, and credible.
- This helps OSS AI reputation more than another private artifact.

### 2. HealthBench validates the rubric direction but is not the first action

Source: https://openai.com/index/healthbench/

Observed facts:

- HealthBench uses 5,000 realistic health conversations.
- It was built with 262 physicians across 60 countries.
- It uses physician-created rubrics and realistic multi-turn/multilingual scenarios.

Fit for G:

- Confirms that physician-written rubrics are the right direction.
- But immediate contribution path is unclear.
- Use it as positioning/reference, not as first target.

### 3. LiveMedBench validates the contamination/rubric angle

Source: https://arxiv.org/abs/2602.10367

Observed facts:

- LiveMedBench targets contamination-free medical evaluation.
- It uses continuously updated real-world clinical cases and rubric-based evaluation.
- It reports 2,756 cases, 38 specialties, 16,702 criteria.
- It argues static benchmarks inflate performance due to contamination and temporal misalignment.

Fit for G:

- Supports the argument that MedFailBench should emphasize fresh, scenario-level failure review and rubric criteria.
- But it uses real-world online clinical cases; MedFailBench should stay synthetic/public-safe unless a real-data ethics path opens.

### 4. EVAH / Gates / Wellcome / Novo Nordisk is real but not immediate

Sources:

- https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/02/ai-impact-health
- https://www.povertyactionlab.org/initiative/evidence-ai-health-evah-rfp

Observed facts:

- EVAH Spring 2026 RFP is closed.
- It funds locally led evaluations of AI-enabled clinical decision support tools in primary/community care.
- Funding pathways go up to USD 1M / 3M depending on stage.

Fit for G:

- This is a future grant/collaboration category, not a July 3 action.
- MedFailBench is currently an evaluation artifact, not a deployed CDST evaluation consortium.

### 5. EIT Health Innovation Validation is not fit now

Source: https://eithealth.eu/opportunity/innovation-validation/

Observed facts:

- Call closes May 6, 2026.
- Requires consortium of at least two organizations from different countries.
- A commercializing company must lead.
- Target is late-stage digital/AI medical devices at IML 6 with clinical validation and market launch.

Fit for G:

- Not a fit today. Too commercial/consortium/late-stage.
- Do not spend time here unless a partner brings the consortium.

### 6. HF Open Medical-LLM Leaderboard is useful only as contrast

Source: https://huggingface.co/blog/leaderboard-medicalllm

Observed facts:

- It benchmarks medical QA style tasks: MedQA, MedMCQA, PubMedQA, MMLU medicine/biology.
- It is useful for model comparison but less aligned with clinical safety-gate failures.

Fit for G:

- Good contrast: MedFailBench should not become another MCQ leaderboard.
- Position MedFailBench as safety-gate review, not exam-score ranking.

## Final call

**Primary strategic decision:** build the MedHELM bridge.

Not now:

- Congress scan
- Generic grant scan
- New closed paper idea
- Another standalone benchmark without upstream route

Now:

1. Create a `MEDHELM_BRIDGE_SPEC.md` in the repo.
2. Map MedFailBench safety gates to MedHELM taxonomy categories.
3. Define one small public synthetic scenario candidate:
   - missing critical variable
   - unsafe escalation wording
   - weak source support
   - Turkish clinical wording ambiguity
4. Open/prepare a clean upstream MedHELM issue or discussion after the spec is polished.
5. Turn this into one public post later: “Why medical AI evals need clinician severity gates, not just QA accuracy.”

## 48-hour execution plan

### Block 1 — Repo artifact

Create `docs/MEDHELM_BRIDGE_SPEC.md`:

- MedHELM taxonomy fit
- MedFailBench safety-gate gap
- public synthetic scenario example
- contribution path
- non-claims boundary

### Block 2 — Upstream-ready issue draft

Create `docs/MEDHELM_UPSTREAM_ISSUE_DRAFT.md`:

- short intro
- what we can contribute
- why synthetic clinician-reviewed safety cases are useful
- link MedFailBench
- ask: preferred scenario format / whether a safety-gate suite is welcome

### Block 3 — Visibility

Update `SOCIAL_POSTS.md` with one human, non-hype post:

- “I’m aligning MedFailBench with MedHELM-style clinical workflow evaluation…”
- no grandiose claims
- no institution claims
- invite clinician/eval feedback

### Block 4 — Technical validation

Run:

```bash
make validate-public
python3 scripts/weekly_model_eval.py --dry-run
```

If clean: commit and push.

## One-line answer

The decision is: **MedFailBench should stop acting like an isolated repo and become a MedHELM-compatible clinical safety-gate contribution path.**
