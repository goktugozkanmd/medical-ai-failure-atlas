# Secondary Lens: Distribution & Visibility (2026-07-08)

> Deep growth dual-loop. Secondary lens rotates every run.
> This lens: where MedFailBench should be listed/discovered, and what product/visibility gaps exist.

---

## Key Findings

### F1: Benchmark Aggregators Are Priority Discovery Targets

AISafetyBenchExplorer (arXiv 2604.12875) catalogues 195 AI safety benchmarks from 2018–2026. BenchLM tracks 278 models and 253 benchmarks on its July 2026 page. Current web checks did not surface MedFailBench in AISafetyBenchExplorer, BenchLM, PapersWithCode, or the Open Medical LLM Leaderboard page.

This is the single biggest distribution gap. Submission routes differ by site and must be verified before any outward action. No listing request should be sent without G approving the exact text and target.

| Aggregator | Submission Method | Effort | Impact |
|------------|------------------|--------|--------|
| AISafetyBenchExplorer | Author contact or project repository to verify | Low | High (safety-focused audience) |
| PapersWithCode | Current contact or data route to verify | Medium | High (canonical benchmark DB) |
| BenchLM | Unknown — needs investigation | Low | Medium |
| Epoch AI DB | Feedback form visible | Low | Medium (research/journalist audience) |

Sources:
- https://arxiv.org/abs/2604.12875 (AISafetyBenchExplorer)
- https://paperswithcode.com/ (PapersWithCode)
- https://benchlm.ai/ (BenchLM)
- https://epoch.ai/benchmarks (Epoch AI)

---

### F2: Awesome Lists Are the Second-Biggest Distribution Channel

GitHub "awesome" lists can drive organic discovery. MedFailBench fits in at least 3 candidate repositories checked live:

1. `curatedhealth/awesome-ai4med` — medical LLMs, multimodal systems, datasets, and benchmarks
2. `medtorch/awesome-healthcare-ai` — open source healthcare tools
3. `openmedlab/Awesome-Medical-Dataset` — medical dataset resources with evaluation benchmark coverage

PR routes should be verified per repository before opening anything. Current checks did not find a MedFailBench listing in these candidate surfaces.

Sources:
- https://github.com/curatedhealth/awesome-ai4med
- https://github.com/medtorch/awesome-healthcare-ai
- https://deepwiki.com/openmedlab/Awesome-Medical-Dataset/3.1-evaluation-benchmarks

---

### F3: HF Open Medical-LLM Leaderboard — Natural Cross-Listing Opportunity

The HuggingFace Open Medical-LLM Leaderboard evaluates medical LLMs. MedFailBench is already on HF Spaces. A cross-reference between the two would bring mutual visibility.

**Specific action:** Check if the Open Medical-LLM Leaderboard accepts external benchmark results. If yes, prepare a MedFailBench safety companion request for G approval.

Source: https://huggingface.co/blog/leaderboard-medicalllm

---

### F4: MLCommons MedPerf — Federated Medical AI Benchmarking

MedPerf (MLCommons) is an open federated evaluation platform for medical AI. MedFailBench synthetic vignettes may fit a MedPerf style package, but the exact packaging and submission route still needs validation.

**Caveat:** Requires understanding of MedPerf's MLCube packaging standard. Higher effort than other channels.

Source: https://github.com/mlcommons/medperf
Source: https://docs.medperf.org/

---

### F5: MedFailBench GitHub Topics Are Comprehensive — Already Done

Repo has 20 topics including `ai-safety`, `medical-ai-safety`, `medfailbench`, `patient-safety`, `clinician-review`, `turkish-medical-ai`. This is the only distribution channel that's already fully exploited.

Verified via `gh repo view --json repositoryTopics`: ✅

---

## New Project Idea: MedAI Safety Benchmark Index

**Problem:** Medical AI safety benchmarks are fragmented. CSEDB, MedSafetyBench, HealthBench, ClinBench, MedFailBench — there's no single directory comparing them. Researchers can't easily find which benchmark covers which safety dimension.

**Solution:** A lightweight GitHub repository or page that indexes all medical AI safety/eval benchmarks, maps each to:
- Safety dimensions covered (worst-case, source support, bilingual drift, etc.)
- Model coverage (which models evaluated)
- Methodology (clinician-authored, synthetic, real-world)
- Accessibility (open-source, API-required, commercial)
- Regulatory position (EU AI Act, MDR alignment)

**How it helps MedFailBench:**
- Positions MedFailBench at the center of the ecosystem
- Drives organic discovery from people searching for "medical AI safety benchmarks"
- Provides a clear competitive landscape (shows gaps MedFailBench fills)
- C0R3 can maintain with monthly updates

**MVP (week 1):** A single `INDEX.md` in the MedFailBench docs folder listing 8-10 benchmarks with comparison table. No separate repo needed initially. Can live as `docs/MEDAI_SAFETY_BENCHMARK_INDEX.md`.

**Phase 2 (week 2-3):** Expand to standalone GitHub repo with README comparison, add "How to get listed" for new benchmarks, open for community PRs.

**Kovalanir mi?** Evet — low effort (single markdown file), high visibility, positions MedFailBench as hub.

---

## Distribution Gap Summary

| Channel | Status | Priority | G Approval? |
|---------|--------|----------|-------------|
| AISafetyBenchExplorer | Not found in current checks | P0 | Yes |
| PapersWithCode | Not found in current checks | P0 | Yes |
| Awesome medical AI lists | Not found in current checks | P1 | Yes |
| BenchLM | Not found in current checks | P1 | Yes |
| Epoch AI DB | Not found in current checks | P1 | Yes |
| HF Open Medical-LLM LB | Not found in current checks | P1 | Yes |
| MLCommons MedPerf | ❌ Not listed | P2 | Maybe |
| GitHub Topics | ✅ Done | — | — |
| HF Space | ✅ Live | — | — |
| GitHub repo | ✅ Live | — | — |
| Zenodo DOI | ✅ Live | — | — |

---

## Immediate Actions (Prepared, Not Sent)

1. AISafetyBenchExplorer — find author contact or project repository, then prepare the MedFailBench entry for approval
2. PapersWithCode — verify the current contact or data route before any client/API action
3. Awesome lists — prepare PR text for `awesome-ai4med` and `awesome-healthcare-ai`, then ask G before opening PRs
4. Create `docs/MEDAI_SAFETY_BENCHMARK_INDEX.md` — comparison table with competitive landscape

## Actions Requiring G Decision

5. HF Open Medical-LLM Leaderboard cross-listing
6. MLCommons MedPerf packaging feasibility
7. ClinBench.com commercial platform listing
