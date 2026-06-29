# HuggingFace Spaces Leaderboard Plan

Status: deployment ready preview plan.

Date: 2026 06 27.

## Goal

Deploy an interactive HuggingFace Space that lets visitors inspect how model runs perform on Medical AI Failure Atlas safety tasks.

The leaderboard should foreground safety gates, review states, and synthetic evidence status. It should not rank models or imply clinical validation.

## Current Repo State

The current leaderboard folder contains:

1. `leaderboard/synthetic_report_template_v0_1.tsv`, the preview result table.
2. `scripts/validate_leaderboard_template_v0_1.py`, the schema and safety boundary validator.
3. `scripts/validate_leaderboard_submissions_v0_1.py`, the pending submission store validator.
4. `scripts/generate_leaderboard_report_v0_1.py`, the Markdown report generator.
5. `leaderboard/app.py`, a Gradio app with synthetic preview and pending review submission tabs.
6. `leaderboard/policy.py`, the shared submission policy used by both the app and validator.
7. `leaderboard/requirements.txt`, the Python dependency file for the app.
8. `leaderboard/SPACE_README.md`, the Space metadata and copy instructions.
9. `leaderboard/submissions.json`, the JSON store for contributor supplied rows.
10. `app.py`, the repository root Space entrypoint.
11. `requirements.txt`, the repository root Space dependency file.

HuggingFace Spaces supports Gradio apps, repository based deployment, `app.py`, `requirements.txt`, and README YAML configuration. Official docs checked:

1. https://huggingface.co/docs/hub/spaces-overview
2. https://huggingface.co/docs/hub/spaces-sdks-gradio
3. https://huggingface.co/docs/hub/spaces-dependencies
4. https://huggingface.co/docs/hub/spaces-config-reference

## Data Format

The preview app reads a tab separated file for synthetic result rows. The current minimum columns are:

| Column | Required | Meaning |
| --- | --- | --- |
| `run_id` | yes | Unique result row identifier. |
| `model_label` | yes | Public model label or anonymized label. |
| `scenario_set` | yes | Scenario pack or prompt set used. |
| `synthetic_only` | yes | Must be `true` for public preview rows. |
| `patient_data_used` | yes | Must be `false`. |
| `clinical_use_allowed` | yes | Must be `false`. |
| `sourcecheckup_gate` | yes | Source support gate state. |
| `failure_atlas_pattern` | yes | Main failure pattern. |
| `clinician_review_state` | yes | Clinician review status. |
| `release_gate` | yes | Public release status for the row. |
| `public_summary` | yes | Short public explanation. |

The next result schema should add these columns before the first public model run:

| Column | Purpose |
| --- | --- |
| `model_provider` | Organization or platform label when public. |
| `model_version` | Exact model revision or release date when public. |
| `scenario_count` | Number of synthetic scenarios in the run. |
| `pass_count` | Count of rows passing the named release gate. |
| `needs_review_count` | Count of rows requiring source or clinician review. |
| `high_risk_count` | Count of high priority safety failures. |
| `eval_date_utc` | Run date in UTC. |
| `repo_commit` | Commit hash for the prompt set and rubric. |
| `runner` | Script or evaluation harness used. |
| `result_file_sha256` | Hash for the raw result artifact kept outside the public table when needed. |

Contributor submitted rows are stored separately in `leaderboard/submissions.json`. They remain pending review, are ordered by latest submission time, and must use HuggingFace model repository links rather than Spaces, datasets, or nested file paths.

## Space UI

The first Space contains:

1. A boundary note above the table.
2. A Submitted Runs tab with pending review contributor rows.
3. A model submission form with HuggingFace model repo link validation.
4. A Synthetic Preview tab with dropdown filters for SourceCheckup gate, clinician review state, and release gate.
5. A search box for model label, scenario set, and failure pattern.
6. A table with visible synthetic result rows.
7. A summary block with counts by safety gate and review state.

The next version should add:

1. A chart of gate counts by model label.
2. A detail panel for each run.
3. Links to scenario set documentation.
4. A download button for the public TSV.
5. A validator status badge from the latest public check.

## Deployment Steps

1. Create a new HuggingFace Space and choose Gradio as the SDK.
2. Deploy the repository root directly, or copy `leaderboard/SPACE_README.md` to the Space root as `README.md`.
3. For copy deployment, copy `leaderboard/app.py` as `app.py`.
4. For copy deployment, copy `leaderboard/policy.py` as `policy.py`.
5. For copy deployment, copy `leaderboard/requirements.txt` as `requirements.txt`.
6. Copy `leaderboard/synthetic_report_template_v0_1.tsv` and `leaderboard/submissions.json`.
7. Set `FAILURE_ATLAS_LEADERBOARD_TSV=synthetic_report_template_v0_1.tsv` and `FAILURE_ATLAS_SUBMISSIONS_JSON=submissions.json` if the files are copied to the Space root.
8. Confirm the Space builds on CPU Basic.
9. Add the Space URL to the repo README after the first successful build.

## Code Needed

Already added:

1. `leaderboard/app.py` for the interactive preview.
2. `leaderboard/policy.py` for shared submission safety rules.
3. `leaderboard/requirements.txt` for Gradio.
4. `leaderboard/SPACE_README.md` for Space metadata.
5. Root `app.py` and `requirements.txt` for direct repository deployment.
6. `leaderboard/submissions.json` for pending review contributor rows.
7. `scripts/validate_leaderboard_submissions_v0_1.py` for submission store safety checks.

Still needed for a full public leaderboard:

1. A `leaderboard/results_v0_1.tsv` file generated from approved model runs.
2. A validator for the expanded result schema.
3. A conversion script from benchmark runner output into the public TSV.
4. A checksum manifest for hidden raw run artifacts.
5. A public policy for model naming, anonymization, and correction requests.

## Safety Rules for the Space

1. Use synthetic scenarios only.
2. Keep patient data columns out of the public table.
3. Do not sort the table as a model ranking.
4. Do not label any model as safe, best, approved, certified, or clinically validated.
5. Show review gates and unresolved review states.
6. Keep model claims tied to the exact scenario set, rubric version, and commit.

## Acceptance Checklist

1. `make leaderboard_report` passes.
2. `python3 scripts/validate_leaderboard_submissions_v0_1.py` passes.
3. `PYTHONPYCACHEPREFIX=/tmp/medical_ai_failure_atlas_pycache python3 -m py_compile leaderboard/app.py leaderboard/policy.py` passes.
4. The Space loads the TSV without editing data files.
5. Filters work for all current gate values.
6. The boundary note is visible before the table.
7. The README links to the Space only after a live Space URL exists.
