# Leaderboard Preview

This folder contains the synthetic no ranking leaderboard preview for Medical AI Failure Atlas.

The preview is not clinical advice, not a clinical validation table, not a model ranking, and not a model safety claim.

## Files

| File | Purpose |
| --- | --- |
| `synthetic_report_template_v0_1.tsv` | Current preview rows. |
| `app.py` | Gradio app for local use or HuggingFace Spaces. |
| `requirements.txt` | App dependency file. |
| `SPACE_README.md` | Metadata and copy instructions for the Space repository. |
| `build/synthetic_report_v0_1.md` | Generated Markdown report. |

## Validate

```bash
make leaderboard
```

## Generate Report

```bash
make leaderboard_report
```

## Run the App

```bash
python3 -m pip install -r leaderboard/requirements.txt
python3 leaderboard/app.py
```

## Deployment Plan

See `docs/LEADERBOARD_PLAN.md`.
