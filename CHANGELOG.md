# Changelog

## v0.2.1e — 2026-07-03 02:00 (weekly eval script + release issue + arXiv doc update)

- Created `scripts/weekly_model_eval.py`: reusable weekly model response evaluation script (reads 5 hard prompts from TSV, calls configured model APIs, runs rule-based scoring, writes timestamped report). Handles all 3 models (DeepSeek Flash, Qwen 7B, Llama 70B) and includes `--dry-run` mode. Addresses issue #185.
- Created GitHub issue #186: v0.2.1 release plan meta-tracker (DOI, arXiv, weekly eval, 100 cases, second reviewer, community growth milestones).
- Updated `docs/ARXIV_SUBMIT_PREP_20260703.md` with current status: figure exists, AI disclosure section present, LaTeX source arXiv-compatible.
- Updated CHANGELOG.
- HF Space still RUNNING (200 OK).

## v0.2.1d — 2026-07-03 01:00 (preprint figure + AI disclosure + eval protocol)

- Added severity distribution figure (bar chart PDF) to preprint: 44 cases weighted toward high severity (52% level 5).
- Added AI-Assisted Writing Disclosure section per arXiv requirements.
- Expanded Methods: Real Model Response Evaluation protocol described (5 prompts, 5 dimensions, automated scoring pass).
- Updated arXiv prep checklist with figure, LaTeX build, and .bbl upload steps.
- Created `scripts/generate_severity_figure.py` for reproducible figure generation.
- Created `scripts/verify_refs.py` for reference verification workflow.
- Preprint main.tex: 285 → ~305 lines. All URLs 200 OK.

## v0.2.1c — 2026-07-02 23:00 (preprint Discussion expanded + Future Work)
- Expanded Discussion with cross-model comparison (7B to 70B consistency).
- Added "Future Work" subsection: DOI, weekly eval automation, second reviewer,
  case expansion to 100, submission API.
- Expanded "Relation to Other Benchmarks" with specific contrast to MMLU,
  HealthBench, MedHELM, GPT-4/Med-PaLM 2 evaluations.
- Strengthened Conclusion with community-invitation framing.
- Created GitHub issues #184 (Zenodo DOI) and #185 (weekly eval automation).
- main.tex: 229 -> 258 lines. All URLs 200 OK.

## v0.2.1b — 2026-07-02 22:00 (reference audit + arXiv ID fixes)
- Reference hallucination audit: 4/13 arXiv IDs verified wrong via Crossref/arXiv API.
  Fixed: wornow2025healthbench (was SoundStorm), nori2023gpt4medical (was neutrino physics),
  tsai2025trmmmu (was axion physics). Removed unverifiable arXiv ID from pal2024medhelm.
- Updated preprint citation keys and references.bib. All 13 references now point to
  real, verified arXiv IDs or journal DOIs.
- CHANGELOG, roadmap, and BAGLAM2 updated.
- Added GitHub Discussions welcome post (#183), synthetic case template,
  CONTRIBUTING.md onboarding flow, and issue #182 progress comment.
- Created `docs/templates/SYNTHETIC_CASE_TEMPLATE.md`.
- Added Data and Code Availability section to preprint.
- HF Space, GitHub, Discussions all live.
- Expanded preprint skeleton: main.tex now includes real model evaluation table,
  13 total references, expanded Introduction, Results, Discussion sections.
- Added `docs/MEDFAILBENCH_V0_2_1_ROADMAP.md` with DOI, Discussions,
  contributor onboarding, weekly eval automation, and arXiv submit plan.
- Enabled GitHub Discussions for community contributions.
- Added 7 new references to `preprint/references.bib` (Med-PaLM 2, GPT-4 NEJM,
  npj Digital Medicine safety, MedEval, Turkish NLP eval and survey).
- Public boundaries remain unchanged.

## v0.2.0 flagship layer — 2026-07-02
- Added clinical severity rubric v0.2: `docs/CLINICAL_SEVERITY_RUBRIC_V0_2.md`.
- Added safety gate taxonomy v0.2: `docs/SAFETY_GATE_TAXONOMY_V0_2.md`.
- Added rubric package: `rubric/v0.2.0/`.
- Added deploy-ready HuggingFace Space sync workflow: `.github/workflows/hf-sync.yml`.
- Added preprint skeleton: `preprint/`.
- Added demo screenshot and GitHub social preview assets.
- Updated README and citation metadata for the flagship layer.
- Public boundaries remain unchanged: no patient data, no clinical advice, no model ranking, no endorsement, no clinical validation.


## v0.3 — 2026-06-23 (synthetic draft review package)
- Draft scoring rubric v0.3: `data/scoring_rubric_v0_3.json`
- Merged synthetic Turkish eval set, 44 cases (TRFAI015–TRFAI058): `data/tr_medllm_synthetic_eval_set_v0_3.jsonl`
- Scoring rubric v0.3 worked examples: `docs/SCORING_RUBRIC_V0_3_WALKTHROUGH.md`
- Coverage matrix: `docs/TR_MEDLLM_SYNTHETIC_EVAL_SET_COVERAGE_MATRIX_V0_3.md`

All v0.3 materials are clinician-led synthetic draft artifacts clinician-reviewed (Göktuğ Özkan, MD, 2026-06-23). No patient data, no clinical advice, no clinical validation, no model ranking, no endorsement.
