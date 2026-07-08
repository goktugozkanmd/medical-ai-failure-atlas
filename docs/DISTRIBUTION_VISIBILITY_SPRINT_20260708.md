# Distribution Visibility Sprint Packet (2026-07-08)

Status: prepared, not submitted.

This file turns the distribution checklist into a short execution packet. No external submission, pull request, issue, comment, email, or form was sent in this run.

## Live check summary

| Target | Live check result | Action now |
|--------|-------------------|------------|
| AISafetyBenchExplorer | arXiv page exists for `2604.12875`; catalogue is framed as a structured AI safety benchmark catalogue. | Prepare a concise benchmark entry and look for author contact or project repository before sending. |
| Epoch AI Benchmarking Hub | Epoch says it includes internally evaluated results and reputable external sources; benchmark pages expose a feedback form. | Prepare feedback-form text, do not submit without final approval. |
| BenchLM | Live site reports a benchmark/model directory surface with 278 models and 253 benchmarks as of its July 2026 page. | Prepare listing request text, channel still needs verification. |
| Papers With Code | GitHub org and data/client repos exist, but public maintenance surface appears limited. | Treat as lower-confidence; first action is contact or data-repo review, not automated client submission. |
| Awesome medical AI lists | Three candidate GitHub repositories are live and not archived. | Prepare PR snippets; actual PRs not opened in this run. |

## Benchmark entry text

Use this as the base for directories or feedback forms:

```text
Name: Medical AI Failure Atlas / MedFailBench
Category: Medical AI safety; clinical safety failure-mode evaluation
Repository: https://github.com/goktugozkanmd/medical-ai-failure-atlas
Persistent release: https://doi.org/10.5281/zenodo.21205535
Short description: Synthetic, clinician-authored medical AI safety benchmark focused on prompt-level failure modes such as missed urgent escalation, unsafe remote dosing, false reassurance after partial negative tests, and source-support gaps. It reports rule-based safety-gate results and keeps public validation tiers separate.
Data boundary: No patient data. Synthetic cases only. No clinical validation or deployment claim.
Current public snapshot: 150 scenario-bank rows, 70 prompts, and 10 public leaderboard models, with clinician panel validation still pending.
```

## First target order

1. AISafetyBenchExplorer: best fit because the project is explicitly an AI safety benchmark catalogue.
2. Epoch AI: good fit for external benchmark-source awareness, but likely requires a concise evidence-backed feedback submission.
3. Awesome medical AI lists: low friction GitHub PR route; easiest if each repo has a benchmarks section.
4. BenchLM: potentially useful, but submission route needs confirmation.
5. Papers With Code: do not rely on old API/client until current submission path is verified.

## Awesome list PR snippet

```markdown
- [Medical AI Failure Atlas / MedFailBench](https://github.com/goktugozkanmd/medical-ai-failure-atlas) - Synthetic, clinician-authored medical AI safety benchmark focused on clinical failure modes, safety-gate scoring, and Turkish/English safety-drift examples. No patient data.
```

Candidate repositories checked live:

| Repository | Status | Suggested section |
|------------|--------|-------------------|
| `curatedhealth/awesome-ai4med` | Live, not archived | Benchmarks or datasets |
| `medtorch/awesome-healthcare-ai` | Live, not archived | Datasets, benchmarks, or evaluation |
| `openmedlab/Awesome-Medical-Dataset` | Live, not archived | Evaluation benchmarks |

## Approval gate

Before any external action:

- Re-read the target repo contribution rules or submission form.
- Confirm exact text and target channel with G.
- Run the academic submission audit on the outgoing text.
- Keep the language as a benchmark discovery request, not a superiority claim.

## Sources checked

- AISafetyBenchExplorer arXiv page: https://arxiv.org/abs/2604.12875
- Epoch AI Benchmarking Hub about/data pages: https://epoch.ai/benchmarks/about and https://epoch.ai/benchmarks/use-this-data
- BenchLM live directory page: https://benchlm.ai/
- Papers With Code GitHub org: https://github.com/paperswithcode
- GitHub repo metadata via `gh repo view` for the three awesome-list candidates.
