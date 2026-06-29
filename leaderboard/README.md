# Leaderboard Preview

This folder contains the synthetic no ranking leaderboard preview for Medical AI Failure Atlas.

The preview is not clinical advice, not a clinical validation table, not a model ranking, and not a model safety claim.

Contributor submitted rows are pending review and are ordered by latest submission time, not by score.
The submission form accepts HuggingFace model repository links only; Spaces, datasets, and file paths are rejected.

## Files

| File | Purpose |
| --- | --- |
| `synthetic_report_template_v0_1.tsv` | Current preview rows. |
| `app.py` | Gradio app module for local use or HuggingFace Spaces. |
| `submissions.json` | JSON store for submitted model rows. |
| `requirements.txt` | App dependency file. |
| `SPACE_README.md` | Metadata and copy instructions for the Space repository. |
| `build/synthetic_report_v0_1.md` | Generated Markdown report. |
| `../app.py` | Root Spaces entrypoint that imports the leaderboard app. |
| `../requirements.txt` | Root Spaces dependency file. |

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

From the repository root, the HuggingFace Spaces entrypoint also works:

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

## Deployment Plan

See `docs/LEADERBOARD_PLAN.md`.
