# MedFailBench Distribution & Visibility Checklist

> Secondary lens: distribution_visibility (2026-07-08)
> Purpose: Where to list MedFailBench for organic discovery, and how.
> Execution packet: `docs/DISTRIBUTION_VISIBILITY_SPRINT_20260708.md`

---

## Priority Matrix

| Platform | Impact | Effort | G Approval? | Do Status |
|----------|--------|--------|-------------|-----------|
| AISafetyBenchExplorer (arXiv) | High | Low | G final text approval | PACKET READY |
| GitHub Topics | Medium | Low | No | DONE (20 topics) |
| HF Open Medical-LLM Leaderboard | High | Low | Maybe | NOT DONE |
| MLCommons MedPerf | Medium | Medium | Maybe | NOT DONE |
| BenchLM aggregator | Medium | Low | G final text approval | PACKET READY |
| Awesome medical AI lists | Medium | Low | G final text approval | PR SNIPPET READY |
| ClinBench.com | Medium | Low | Maybe | NOT DONE |
| PapersWithCode | High | Medium | G final text approval | CHANNEL UNCERTAIN |
| Epoch AI benchmark DB | Medium | Low | G final text approval | PACKET READY |

---

## Channel Details

### 1. AISafetyBenchExplorer (arXiv 2604.12875) — HIGH PRIORITY

**What:** A structured catalog of 195 AI safety benchmarks (2018–2026). Academic audience, LLM safety community.

**How to get listed:** The paper lists all 195 benchmarks in a supplemental CSV. The authors likely accept contributions via GitHub issues or email. The arXiv paper page (2604.12875) has contact information.

**Action:**
```
1. Go to https://arxiv.org/abs/2604.12875
2. Find GitHub repo or contact email for AISafetyBenchExplorer
3. Submit MedFailBench entry with:
   - Name: Medical AI Failure Atlas (MedFailBench)
   - Category: Medical AI Safety / Clinical Safety
   - Metrics: Rule-based safety scoring (0-100), worst-case tier analysis
   - Domains: Clinical vignettes, Turkish/EN bilingual safety drift
   - Citation: Ozkan 2026, Zenodo DOI 10.5281/zenodo.21205535
```

**Status:** PACKET READY — no submission made. See `docs/DISTRIBUTION_VISIBILITY_SPRINT_20260708.md`.

---

### 2. PapersWithCode — HIGH PRIORITY

**What:** The canonical ML benchmark tracking platform. Academic and industry audience.

**How to get listed:**
- Option A: Create dataset entry for MedFailBench prompts → easy, no review
- Option B: Create benchmark task ("Medical AI Safety Gate") → needs paper link
- Option C: Submit results table (10 models already evaluated) → shows leaderboard

**API approach:**
```python
# paperswithcode-client can create dataset entries
pip install paperswithcode-client
python -c "
from paperswithcode import PapersWithCodeClient
client = PapersWithCodeClient()
# Create dataset
client.dataset_create('medfailbench', 
    description='Clinician-authored medical AI safety benchmark')
# Add results for each model
"
```

**Status:** CHANNEL UNCERTAIN — current live check shows GitHub org/data surfaces, but no automated submission was attempted. Treat as contact/data-route verification first.

---

### 3. HF Open Medical-LLM Leaderboard

**What:** HuggingFace's medical LLM evaluation leaderboard. High visibility in the HF ecosystem.

**How to get listed:** Not confirmed. The public page documents medical model evaluation and model submission, but a MedFailBench benchmark cross-listing route still needs verification.

**Action:**
1. Check if Open Medical-LLM Leaderboard accepts external benchmark submissions
2. If yes, prepare a MedFailBench companion benchmark request for G approval
3. Add any cross-reference to MedFailBench README only after a listing is actually accepted

**Status:** CHANNEL UNCERTAIN — public page checked, no submission attempted

---

### 4. GitHub Topics — LOW EFFORT, DONE

**What:** GitHub repo topics that appear in search and topic pages.

**Current topics (20):** ai-benchmark, ai-safety, clinical-nlp, evaluation-framework, failure-analysis, healthcare-ai, language-model-evaluation, llm-safety, medical-ai, patient-safety, clinician-review, medical-language-models, llm-evaluation, source-verification, failure-atlas, medical-ai-safety, turkish-medical-ai, medical-llm, huggingface-spaces, medfailbench

**Status:** DONE ✅ — already comprehensive

---

### 5. Awesome Medical AI Lists — MEDIUM PRIORITY

**What:** Community-curated GitHub repos listing medical AI resources.

**Target lists:**
- `curatedhealth/awesome-ai4med`: Covers medical LLMs, datasets, benchmarks ✓
- `medtorch/awesome-healthcare-ai`: Open source healthcare tools ✓
- `openmedlab/Awesome-Medical-Dataset`: Evaluation benchmarks section ✓

**Action:** For each list, prepare a PR snippet adding MedFailBench to the benchmarks section. Open PRs only after target rules and G approval are confirmed.

**Links:**
- https://github.com/curatedhealth/awesome-ai4med
- https://github.com/medtorch/awesome-healthcare-ai
- https://deepwiki.com/openmedlab/Awesome-Medical-Dataset/3.1-evaluation-benchmarks

**Status:** PR SNIPPET READY — candidate repositories live-checked; no PR opened.

---

### 6. MLCommons MedPerf — MEDIUM PRIORITY

**What:** MLCommons open benchmarking platform for medical AI using federated evaluation. If MedFailBench scenarios were uploaded as a MedPerf dataset, it would gain visibility in the MLCommons community.

**Action:**
1. Review MedPerf dataset submission docs: https://docs.medperf.org/
2. Check if synthetic clinical vignettes qualify as a MedPerf benchmark dataset
3. Create MedPerf-compatible dataset packaging
4. Submit via `medperf dataset submit`

**Status:** NOT STARTED — needs G approval for MedPerf community engagement

---

### 7. BenchLM Aggregator — MEDIUM PRIORITY

**What:** Tracks 278 models across 253 benchmarks. Medical AI safety category exists.

**Action:** Check https://benchlm.ai/ for submission form or contact. Submit MedFailBench entry.

**Status:** PACKET READY — submission channel still needs final live confirmation.

---

### 8. Epoch AI Benchmark Database

**What:** Tracks model performance across benchmarks. Used by researchers and journalists.

**Action:** Submit MedFailBench results at https://epoch.ai/benchmarks

**Status:** PACKET READY — use feedback form text from `docs/DISTRIBUTION_VISIBILITY_SPRINT_20260708.md`; no form submitted.

---

### 9. ClinBench.com — LOW PRIORITY (needs G call)

**What:** New medical AI benchmark comparison platform. Commercial. Could list MedFailBench for cross-platform visibility.

**Risk:** Commercial platform may have terms that conflict with MedFailBench's open positioning.

**Action:** G to decide if ClinBench listing is desirable.

**Status:** DEFER — needs G decision

---

## Weekly Distribution Maintenance

Once initial listings are done, maintain with a monthly check:

```bash
# Quick check script (run monthly via cron)
python3 -c "
import urllib.request, json

# Check GitHub stars
req = urllib.request.Request(
    'https://api.github.com/repos/goktugozkanmd/medical-ai-failure-atlas',
    headers={'User-Agent': 'C0R3', 'Accept': 'application/vnd.github.v3+json'})
data = json.loads(urllib.request.urlopen(req, timeout=15).read())
stars = data.get('stargazers_count', 0)
forks = data.get('forks_count', 0)
print(f'GitHub Stars: {stars}, Forks: {forks}')

# Check HF Space visits (via HF API)
# TODO: Add HF Space analytics API call when available
"
```

---

## Current Distribution Scorecard (2026-07-08)

| Channel | Status | Date |
|---------|--------|------|
| GitHub repo | ✅ Live | Jul 2026 |
| GitHub Topics | ✅ 20 topics | Jul 2026 |
| HF Space | ✅ Live | Jul 2026 |
| Zenodo DOI | ✅ 10.5281/zenodo.21205535 | Jul 2026 |
| arXiv preprint | ❌ Endorsement blocked | — |
| AISafetyBenchExplorer | 🟡 Packet ready, not submitted | 2026-07-08 |
| PapersWithCode | 🟡 Channel uncertain, not submitted | 2026-07-08 |
| Awesome medical AI lists | 🟡 PR snippet ready, not submitted | 2026-07-08 |
| BenchLM | 🟡 Packet ready, not submitted | 2026-07-08 |
| Epoch AI | 🟡 Packet ready, not submitted | 2026-07-08 |
| Open Medical-LLM Leaderboard | ❌ Not submitted | — |
| MedPerf (MLCommons) | ❌ Not submitted | — |
| ClinBench.com | ❌ Deferred | — |

---

## Next 7-Day Sprint

| Day | Channel | Action | Time |
|-----|---------|--------|------|
| Day 1 | AISafetyBenchExplorer | Confirm author/repo channel + submit approved entry | 30 min |
| Day 2 | Awesome-ai4med | Open approved PR adding MedFailBench | 20 min |
| Day 3 | Epoch AI | Submit approved feedback-form entry | 15 min |
| Day 4 | BenchLM | Confirm channel + submit approved benchmark entry | 15 min |
| Day 5 | PapersWithCode | Verify current submission/contact route before any action | 30 min |
| Day 6 | Open Medical-LLM Leaderboard | Check submission process | 20 min |
| Day 7 | Build summary | Log all submissions, verify visibility | 15 min |

---

## Metric Goals

| Metric | Current | 30-day target | 90-day target |
|--------|---------|---------------|---------------|
| GitHub stars | ~? | +50% | 3x |
| HF Space visitors | ? | Trackable | Weekly trend up |
| Benchmark aggregators listed | 0 | 3 | 6 |
| Awesome list appearances | 0 | 2 | 5 |
| PubMed/Crossref citations | ? | Trackable | 5+ |
| Upstream PR merges | 2 | 3 | 5 |
