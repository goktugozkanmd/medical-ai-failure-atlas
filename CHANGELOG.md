# Changelog

## v0.2.1b — 2026-07-02 21:00 (community infra + data section)
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
