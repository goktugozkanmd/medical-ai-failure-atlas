# Docs Directory Cleanup Assessment

**Status:** Draft recommendation | **Date:** 2026-07-07 12:45 TRT

## Problem

`docs/` contains ~320 files. Many are:
- Single-use planning documents from June 18–19
- JSON duplicates of .md files
- `reviewer_question_maintainer_*` archive files (25+ near-identical filenames)
- Files referencing stale targets (Hacettepe, TUBITAK 1711, KTU, TEKNOFEST, etc.)

## Size estimate

```
$ find docs/ -type f | wc -l
~320 files
$ du -sh docs/
~15 MB
```

## Categorization

| Category | Count | Action |
|----------|-------|--------|
| Active docs (referenced in README/STATE_LEDGER) | ~15 | Keep |
| Template / JSON model files | ~80 | Archive to `docs/archive/` |
| Single-use outreach plans (June 18-19 batch) | ~50 | Archive |
| Reviewer question maintainer archive (June 19) | ~25 | Archive or delete |
| Stale TUBITAK/TUSEB/TEKNOFEST plans | ~20 | Archive |
| Model failure cards (active) | ~10 | Keep |
| `model_team_feedback/` | ~4 | Keep (contains approval drafts) |
| `sourcecheckup/` | ~10 | Keep (validation trail) |
| `weekly_failure_of_the_week/` | ~? | Keep (draft series) |
| `archive/` (already archived) | ~? | Leave as-is |

## Recommended Cleanup

### Phase 1: No-brainer moves (G approval not needed for file moves)

Move stale single-use files to `docs/archive/june2026/`:

```
docs/archive/june2026/acibadem_*
docs/archive/june2026/hacettepe_*
docs/archive/june2026/hospital_*
docs/archive/june2026/tubitak_1711_*
docs/archive/june2026/tuseb_a4_um_*
docs/archive/june2026/tuyze_*
docs/archive/june2026/teknofest_*
docs/archive/june2026/ktu_*
docs/archive/june2026/deu_digital_medicine_*
docs/archive/june2026/turkiye_health_ai_*
docs/archive/june2026/turkiye_clinical_ai_*
docs/archive/june2026/turkiye_no_ranking_*
docs/archive/june2026/global_benchmark_*
docs/archive/june2026/global_health_ai_*
docs/archive/june2026/medical_ai_post_0900_*
docs/archive/june2026/goktug_field_action_*
docs/archive/june2026/route_owner_acknowledgement_*
docs/archive/june2026/benchmark_language_reviewer_*
docs/archive/june2026/benchmark_style_reviewer_*
docs/archive/june2026/chai_governance_*
docs/archive/june2026/current_medical_ai_intelligence_*
docs/archive/june2026/eu_ai_act_health_ai_*
docs/archive/june2026/field_impact_opportunity_*
docs/archive/june2026/healthbench_medhelm_*
docs/archive/june2026/medhelm_healthbench_*
docs/archive/june2026/medical_ai_safety_field_kit_*
docs/archive/june2026/named_outreach_decision_*
docs/archive/june2026/no_ranking_benchmark_*
docs/archive/june2026/red_flag_warning_*
docs/archive/june2026/source_review_worksheets_*
docs/archive/june2026/sourcecheckup_medhelm_*
docs/archive/june2026/turkiye_ai_ethics_*
docs/archive/june2026/turkiye_health_data_*
docs/archive/june2026/clinician_literacy_*
docs/archive/june2026/clinician_ai_literacy_*
docs/archive/june2026/hospital_ai_governance_*
docs/archive/june2026/hospital_ai_literacy_*
docs/archive/june2026/tr_clinical_ai_assurance_*
```

### Phase 2: JSON duplicates

Most `.json` files in docs/ are exact copies of `.md` file content. 
Move all `.json` files to `docs/archive/june2026/json-duplicates/`.

### Phase 3: Reviewer question maintainer archive (needs G decision)

The `reviewer_question_maintainer_*_v0_1.json` and `.md` files (25 files) 
are an over-engineered archive trail. Two options:
- Delete (clean break)
- Move to `docs/archive/maintainer-review-log/`

## Expected Result After Cleanup

| Before | After | 
|--------|-------|
| ~320 files | ~40–50 files |
| ~15 MB | ~3–5 MB |
| Hard to navigate | Clean, active docs only |

## Pitfall Warning

- **Do not delete** files referenced by README, STATE_LEDGER, or any active CI path
- **Do not delete** template files under `docs/templates/`
- **Do not delete** files under `docs/model_failure_cards/` or `docs/model_team_feedback/`
- **Do not delete** files under `docs/weekly_failure_of_the_week/`
- **Do not delete** `docs/sourcecheckup/` — these contain validation evidence

## Immediate Action

None until G confirms cleanup direction.

This document exists so the information is durable and can be actioned later.