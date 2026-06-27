# Repository Structure

Date: 2026 06 27.

This repository now separates public benchmark surfaces from historical process material.

## Core Project Paths

| Path | Role |
| --- | --- |
| `data/` | Synthetic scenario banks, prompt sets, scoring rubrics, and public sample rows. |
| `failure_atlas/public/` | Public failure taxonomy, case intake schema, methodology, and review queue. |
| `leaderboard/` | Preview table, report generator output, and HuggingFace Space app. |
| `rubric/v0.1.0/` | Frozen first rubric documentation. |
| `scripts/` | Validators, runners, report generators, and helper tools. |
| `sourcecheckup/` | Source support review examples, schemas, and demo reports. |
| `tr_medllm_safetybench/` | Turkish medical LLM synthetic risk pack and generated summary. |

## Support Paths

| Path | Role |
| --- | --- |
| `docs/` | Method notes, release cards, governance notes, and project plans. |
| `docs/archive/` | Superseded bundles preserved for traceability. |
| `outputs/` | Generated issue bodies, public action audit notes, and release notes used by legacy validators. |
| `medmarks_candidate_env_v1_20260614/` | Current MedMARKS candidate integration bundle referenced by release validators. |

## Cleanup Completed

The superseded root bundle `medmarks_candidate_env_v0_20260613/` moved to `docs/archive/legacy_integrations/medmarks_candidate_env_v0_20260613/`.

Data files and evaluation result files were not edited.
