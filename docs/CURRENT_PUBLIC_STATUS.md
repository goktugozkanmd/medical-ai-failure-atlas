# MedFailBench Current Public Status

**Snapshot:** 26 July 2026
**Source commit:** `0f6cc5f6ee7e9da140f3c50903e77477fdbe6241`

This file separates the current public benchmark evidence from component releases, hosted previews, working notes, and historical artifacts.

## Public benchmark release

The current archived benchmark software and data release is MedFailBench `v0.2.1`.

* [GitHub release v0.2.1](https://github.com/goktugozkanmd/medical-ai-failure-atlas/releases/tag/v0.2.1)
* [Zenodo software record](https://doi.org/10.5281/zenodo.21205535)

SafetyGuard `v0.1.0` is a later component release in the same repository. It does not replace the MedFailBench benchmark version.

## Public core evidence set

The current core file is `data/tr_medllm_synthetic_eval_set_v0_3.jsonl`.

At the source commit above it contains:

* 44 synthetic cases with 44 unique case identifiers.
* 21 clinical domain labels.
* 44 records marked `clinician_reviewed`.
* 44 records marked `approved` for the release gate.
* 40 populated safety gate fields and 4 null safety gate fields.
* No patient data.

The file SHA256 is `23f69c913b6ff38ccde23e526b4b0f72785ccfc3fa76478c980a879a499ef331`.

These counts describe this file only. They must not be combined with broader scenario banks, prompt sets, adapter exports, or generated records as one benchmark size claim.

## Availability

The GitHub repository and Zenodo record are public. At this snapshot the [Hugging Face Space](https://huggingface.co/spaces/goktugozkanmd/medical-ai-failure-atlas) runtime reports `RUNTIME_ERROR`. The hosted Space is not used here as release evidence or described as a live demo.

Local tools and validation commands remain available from the repository README.

## Repository verification

At this snapshot:

* `uv run pytest -q` completed with 237 passing tests.
* `make PYTHON=python3 validate-public` completed successfully.

These checks cover repository behavior and public artifact contracts. They are not clinical validation.

## Preprint status

The public [arXiv record 2607.15166](https://arxiv.org/abs/2607.15166) has a version one integrity mismatch: its abstract metadata reports 44 cases, while its public PDF and source package contain an older 100 case manuscript. Until a corrected arXiv version is public, the preprint is not the source for the benchmark size or model result claims.

## Evidence boundaries

The current public release is:

* Synthetic and patient data free.
* Clinician authored and internally reviewed.
* Not independently validated by a clinician panel.
* Not a clinical validation study.
* Not evidence of overall model safety, clinical deployment readiness, regulatory approval, or endorsement.

The four null safety gate fields remain an explicit review gap. They must not be filled by assumption.

## Update rule

Update this file whenever the benchmark release, source commit, public core file, hosted availability, preprint version, or validation boundary changes. Every numerical claim must be reproduced from the named source file before publication.
