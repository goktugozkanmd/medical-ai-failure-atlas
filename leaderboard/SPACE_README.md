---
title: Medical AI Failure Atlas Leaderboard
colorFrom: green
colorTo: yellow
sdk: gradio
app_file: app.py
pinned: false
short_description: Synthetic medical AI safety evaluation preview
---

# Medical AI Failure Atlas Leaderboard

This Space shows synthetic preview rows, contributor supplied model submissions, a worst-case safety view, model failure cards, and a narrow collaborator call from Medical AI Failure Atlas.

It does not provide clinical advice, clinical validation, source truth certification, partner claims, institution claims, or endorsement claims. Submitted scores are pending review and rows are ordered by latest submission time, not by score.

The submission form accepts HuggingFace model repository links only. Spaces, datasets, and file paths are rejected.
Model names and notes must not include contact details, long numeric identifiers, patient data, clinical validation claims, or ranking claims.
Credential-like strings are rejected in model names, notes, and repository links.

Submitted rows are written to the JSON store available to the running app. Enable persistent Space storage, or export the JSON store before rebuilds, if public submissions need to survive runtime restarts.

## Model submission and collaborator call

Use the app form for HuggingFace model repository links only. Use GitHub issues for collaboration: one synthetic case, one safety gate objection, one label audit note, or one wording fix.

Do not submit patient data, private clinical text, clinical advice, validation claims, ranking claims, score certification, source truth certification, partner claims, institution claims, or endorsement claims.

## Direct Repository Deployment

The repository root includes the files HuggingFace Spaces expects:

1. `app.py`
2. `requirements.txt`
3. `leaderboard/policy.py`
4. `leaderboard/synthetic_report_template_v0_1.tsv`
5. `leaderboard/submissions.json`
6. `model_runs/worst_case_safety_report_v0_1.json`
7. `docs/model_failure_cards/`

Enable persistent Space storage before treating submitted rows as durable.

## Copy Deployment

If only the leaderboard files are copied into a Space root, copy:

1. `leaderboard/app.py` as `app.py`.
2. `leaderboard/policy.py` as `policy.py`.
3. `leaderboard/requirements.txt` as `requirements.txt`.
4. `leaderboard/synthetic_report_template_v0_1.tsv` as `synthetic_report_template_v0_1.tsv`.
5. `leaderboard/submissions.json` as `submissions.json`.
6. `model_runs/worst_case_safety_report_v0_1.json` as `worst_case_safety_report_v0_1.json`.
7. `docs/model_failure_cards/` as `model_failure_cards/`.
8. This file as `README.md`.

Set `FAILURE_ATLAS_LEADERBOARD_TSV=synthetic_report_template_v0_1.tsv`, `FAILURE_ATLAS_SUBMISSIONS_JSON=submissions.json`, `FAILURE_ATLAS_WORST_CASE_JSON=worst_case_safety_report_v0_1.json`, and `FAILURE_ATLAS_FAILURE_CARDS_DIR=model_failure_cards` if the TSV, JSON, and failure-card files are copied to the Space root.

## Public identity note

Deploy this Space only under a professional account or organization. Do not deploy under a non-professional personal handle.
