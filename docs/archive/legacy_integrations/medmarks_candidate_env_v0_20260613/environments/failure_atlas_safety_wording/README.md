# Failure Atlas safety wording environment probe

Status: internal draft only.

This folder is a local proof pack for a possible Medmarks open ended environment. It is not a Medmarks pull request and is not cleared for external posting.

## Task type

Open ended medical safety wording evaluation.

## Data

Source sample:

`../../data/failure_atlas_external_sample_v0_1.jsonl`

The cases are synthetic and contain no patient data.

## Evaluation idea

Generate an answer to each synthetic case, then judge the answer with a rubric focused on:

1. Emergency risk recognition.
2. Unsafe precision avoidance.
3. Missing variable awareness.
4. Triage protocol separation.
5. Safe actionability.

## Smoke command

From the repository root:

```bash
python3 medmarks_candidate_env_v0_20260613/environments/failure_atlas_safety_wording/failure_atlas_safety_wording.py --cases data/failure_atlas_external_sample_v0_1.jsonl --smoke
```

## Boundary

Do not submit this to Medmarks until user approval, final audit, license and citation decisions, and accurate clinician review wording are complete.
