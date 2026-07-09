# SafetyGuard Card Release Gate CI Artifact

Date: 2026 07 08

Status: workflow dry run artifact job wired.

## What Changed

The Eval Pipeline workflow now has a `safetyguard-card-release-gate` job. It runs only when the resolved workflow mode is dry run.

## Job Behavior

1. Checks out the repository.
2. Installs the local package.
3. Runs `scripts/smoke_safetyguard_card_release_gate_20260708.py`.
4. Uploads the manifest and generated local smoke outputs as a GitHub Actions artifact.

## Artifact

Artifact name: `safetyguard-card-release-gate`

Included paths:

- `docs/safetyguard_card_release_gate_smoke_20260708.json`
- `build/safetyguard_card_release_gate_20260708/`

## Boundary

No provider API call, no paid run, no Hugging Face publish, no external submission, no patient data, no physician selection, no clinical validation claim, no model ranking claim, and no official endorsement claim.
