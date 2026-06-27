# Public release boundary v0.1

Status: public release boundary.

Date: 2026 06 13

## Purpose

This file separates material that can plausibly become public v0.1 from material that must remain internal until review and legal or platform checks are complete.

## Public candidate

These files are eligible for the public v0.1 release after sanitation:

1. `README.md` after public wording cleanup.
2. `DATA_DICTIONARY.md` after public wording cleanup.
3. `Makefile`
4. `data/scenario_bank_v1.tsv`
5. `data/scenario_bank_v2_hard_addendum.tsv`
6. `data/scenario_bank_v3_scale_seed.tsv`
7. `data/scenario_taxonomy_v0_2.tsv`
8. `data/failure_atlas_external_sample_v0_1.jsonl`
9. `data/medhelm_remote_rescue_metric_v0_1.json`
10. `data/scoring_rubric_v0_1.json`
11. `data/inter_rater_review_subset_v0_1.tsv`
12. `data/prompt_set_v1.tsv`
13. `data/prompt_set_v2_hard_30.tsv`
14. `data/prompt_set_v3_scale_30.tsv`
15. `docs/clinician_evaluation_rubric.md`
16. `docs/scoring_model_v0_1.md`
17. `docs/failure_atlas_entry_001_insulin_sick_day_wording_draft.md` after clinician wording status is corrected.
18. `docs/failure_atlas_entry_002_protocol_overprecision_draft.md` after clinician wording status is corrected.
19. `docs/failure_atlas_entry_003_remote_rescue_protocols_draft.md` after clinician wording status is corrected.
20. `docs/MEDHELM_CROSSWALK_DRAFT.md` after external text audit.
21. `docs/MEDHELM_REMOTE_RESCUE_BOUNDARY_METRIC_PACKAGE_DRAFT.md` after external text audit.
22. `docs/MEDMARKS_COMPATIBILITY_DRAFT.md` after external text audit.
23. `docs/LABEL_DEFINITION_LOCK_V0_1.md`
24. `docs/CLINICIAN_REVIEW_DISAGREEMENT_PROTOCOL_V0_1.md`
25. `docs/INTER_RATER_REVIEW_SUBSET_PLAN_V0_1.md`
26. `docs/LABELING_PACKAGE_INDEX_V0_1.md`
27. `rubric/v0.1.0/README.md`
28. `rubric/v0.1.0/CHANGELOG.md`
29. `docs/archive/legacy_integrations/medmarks_candidate_env_v0_20260613/` as a superseded integration proof pack.
30. `scripts/validate_external_sample_jsonl.py`
31. `scripts/validate_medhelm_metric_json.py`
32. `scripts/validate_model_run_json.py`
33. `scripts/validate_public_release.py`
34. `scripts/validate_scoring_rubric_v0_1.py`
35. `scripts/benchmark_runner.py`
36. `scripts/run_prompt_set_openai_compatible_v2.py`
37. `scripts/run_prompt_set_hf_transformers_v2.py`
38. `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`
39. `scripts/validate_health_data_quality_card_v0_1.py`
40. `docs/MEDHELM_BOUNDARY_NOTE_V0_1.md`
41. `docs/MEDMARKS_BOUNDARY_NOTE_V0_1.md`
42. `scripts/validate_boundary_notes_v0_1.py`
43. `docs/ASSURANCE_CARD_TEMPLATE_V0_1.md`
44. `docs/assurance_card_template_v0_1.json`
45. `scripts/validate_assurance_card_template_v0_1.py`

## Internal only

These should not ship in public v0.1 without separate review:

1. `docs/OPEN_SOURCE_CONTRIBUTION_DRAFTS_20260613.md`
2. `model_runs_hard30_20260613/raw_outputs/`
3. `model_runs_v3_scale30_20260613/raw_outputs/`
4. `model_runs_hard30_20260613/logs/`
5. `model_runs_v3_scale30_20260613/logs/`
6. Any script with absolute local machine paths.
7. Any file containing shell permission bypass flags.
8. Any outreach draft, email draft, or external issue draft before final audit.
9. `review_forms/` while reviewer facing files contain raw model answer text.

## Completed before public v0.1

1. Code license selected.
2. Data and text license selected.
3. `LICENSE` added.
4. `CITATION.cff` added.
5. `CONTRIBUTING.md` added.
6. No patient data policy included.
7. Local validation instructions included.
8. Absolute local paths excluded from public scripts.
9. Raw model outputs excluded because platform terms are not cleared.
10. Public examples use `python3` or `make`.
11. Public wording audit completed with official identifier exceptions.
12. Explicit user approval received for the initial GitHub publication.
13. Later public GitHub updates still require separate user approval.

## Allowed claim language

Allowed:

`physician authored synthetic draft pending final clinician review`

Allowed:

`internal development signal`

Not allowed yet:

`clinician validated`

Not allowed yet:

`model X is unsafe`

Not allowed yet:

`MedHELM compatible`

Use instead:

`MedHELM oriented draft`

Not allowed yet:

`Medmarks compatible`

Use instead:

`Medmarks style local proof pack`
