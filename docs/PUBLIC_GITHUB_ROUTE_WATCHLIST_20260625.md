# Public GitHub Route Watchlist

Date: 2026 06 25

Status: local public route watchlist for medical AI and open source AI contribution surfaces. It records public GitHub state only. It does not claim maintainer support, review completion, merge, acceptance, endorsement, partnership, clinical validation, clinical deployment, benchmark result, model ranking, score certification, payment, terms acceptance, patient data use, or institutional approval.

## Live checks used

Checked after reading BAGLAM2, Gmail, the LinkedIn tracker, the local repository branch, and public GitHub surfaces.

1. The AI Alliance trust safety evals issue 50.
2. Hugging Face lighteval pull request 1272.
3. UK Government inspect ai pull request 4343.
4. Medical AI Failure Atlas issue 154.

No public write action was taken during this check.

## Watch rows

### Route 1. The AI Alliance issue 50

Public URL: https://github.com/The-AI-Alliance/trust-safety-evals/issues/50

Live state: open.

Latest useful public signal: Dean Wampler acknowledged the comment and said he would try to follow up tomorrow.

Current action: wait. Do not add a visibility comment.

Allowed next action: if the maintainer asks for a smaller contribution, offer one docs oriented claim boundary checklist using public or synthetic examples only.

Blocked claim: AI Alliance review, adoption, partnership, endorsement, MedHELM compatibility, benchmark result, clinical validation, clinical deployment.

### Route 2. Hugging Face lighteval pull request 1272

Public URL: https://github.com/huggingface/lighteval/pull/1272

Live state: open.

Live review state: review required.

Live merge state: blocked.

Latest useful public signal: no comments or reviews found in the live pull request metadata.

Current action: wait for maintainer review.

Allowed next action: respond only if a maintainer comments or requests changes. Do not ask for review again.

Blocked claim: merge status beyond the live pull request state, acceptance status, maintainer approval, release inclusion.

### Route 3. UK Government inspect ai pull request 4343

Public URL: https://github.com/UKGovernmentBEIS/inspect_ai/pull/4343

Live state: open.

Live review state: review required.

Live merge state: behind.

Latest useful public signal: no comments or reviews found in the live pull request metadata.

Current action: wait for maintainer review.

Allowed next action: respond only if a maintainer comments, requests changes, or asks for a branch refresh. Do not push a branch refresh without explicit user approval.

Blocked claim: merge status beyond the live pull request state, acceptance status, maintainer approval, release inclusion.

### Route 4. Medical AI Failure Atlas issue 154

Public URL: https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/154

Live state: open.

Latest useful public signal: no outside comment found in the live issue list.

Current action: keep it as the single outside objection intake point.

Allowed next action: link it from future posts only when the post asks for one concrete objection.

Blocked claim: external review, outside validation, public endorsement, clinical validation, clinical deployment.

## Current routing decision

The right next move is still build and wait:

1. Do not push a new public GitHub comment today.
2. Do not ask for review again on open upstream pull requests.
3. Keep LinkedIn visibility separate from GitHub maintainer pressure.
4. Use issue 154 only when asking for a narrow outside objection.
5. Recheck all public routes before any future public claim.

## Runnable check

```bash
make public_github_route_watchlist
make public_github_route_live_check
```
