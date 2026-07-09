# Codex Summary

Date: 2026 06 27.

## Completed Tasks

### 1. README rewrite

Replaced the long root `README.md` with a 167 line global project front door.

The new README includes:

1. The required tagline: "A clinician-built benchmark for medical AI safety evaluation."
2. A top demo screenshot placeholder at `docs/assets/demo-placeholder.svg`.
3. A short plain English project explanation.
4. Table of contents.
5. Three command quick start.
6. What this evaluates.
7. What is inside.
8. Repository structure.
9. Example workflows.
10. Who this is for.
11. Safety boundaries.
12. Roadmap.
13. License section with Apache-2.0 and CC-BY-4.0.
14. Citation section.

Removed the old outside objection and public reviewer call material from the README front door.

### 2. GitHub issue cleanup

Closed issues `#145` through `#154` in `goktugozkanmd/medical-ai-failure-atlas`.

Each issue was closed with the requested comment:

`Consolidating project focus. See updated README.`

After closure, `gh issue list --state open` returned an empty list.

### 3. HuggingFace leaderboard preparation

Added:

1. `docs/LEADERBOARD_PLAN.md`
2. `leaderboard/app.py`
3. `leaderboard/requirements.txt`
4. `leaderboard/SPACE_README.md`

Updated `leaderboard/README.md`.

The new Gradio app reads the existing synthetic TSV preview, shows a no ranking safety boundary, exposes filters for SourceCheckup gate, clinician review state, release gate, and search, then displays a result table and counts.

Official HuggingFace documentation checked for the plan:

1. https://huggingface.co/docs/hub/spaces-overview
2. https://huggingface.co/docs/hub/spaces-sdks-gradio
3. https://huggingface.co/docs/hub/spaces-dependencies
4. https://huggingface.co/docs/hub/spaces-config-reference

### 4. Repository structure cleanup

Added:

1. `docs/REPOSITORY_STRUCTURE.md`
2. `docs/archive/README.md`
3. `data/README.md`
4. `failure_atlas/README.md`

Moved the superseded root bundle:

`medmarks_candidate_env_v0_20260613/` to `docs/archive/legacy_integrations/medmarks_candidate_env_v0_20260613/`

Left `medmarks_candidate_env_v1_20260614/` in place because validators and boundary notes still reference it.

No files under `data/` were edited. No evaluation result files were edited.

Updated `release/PUBLIC_RELEASE_BOUNDARY_V0_1.md` to point at the archived MedMARKS v0 path.

### 5. External PR status checks

Recorded status in `docs/EXTERNAL_PR_STATUS_20260627.md`.

`huggingface/lighteval#1272`

1. State: open.
2. Review decision: review required.
3. Comments: none returned by `gh pr view`.
4. Reviews: none returned by `gh pr view`.
5. Checks: no checks reported on branch `a67-issue-745-language-script`.
6. Actionable response needed: no.

`UKGovernmentBEIS/inspect_ai#4343`

1. State: open.
2. Review decision: review required.
3. Comments: none returned by `gh pr view`.
4. Reviews: none returned by `gh pr view`.
5. Checks: passing, with workflow skipped jobs for release or slow tests.
6. Actionable response needed: no.

## Validator Updates

Updated `scripts/validate_public_release.py` so it accepts the new concise README format while retaining legacy checks for the old README path.

Updated `scripts/validate_medical_ai_safety_field_kit_one_objection_gateway_20260620.py` so it accepts the concise README safety boundary instead of requiring outside review wording in the root README.

Updated `docs/PUBLIC_SAFE_FAILURE_CARDS_20260619.md` to keep the Safe Failure Card issue template route visible outside the root README.

## Verification

Passed:

1. `make leaderboard_report`
2. `python3 scripts/validate_leaderboard_template_v0_1.py`
3. `PYTHONPYCACHEPREFIX=/tmp/medical_ai_failure_atlas_pycache python3 -m py_compile leaderboard/app.py`
4. Direct Python syntax compile for `leaderboard/app.py`
5. `leaderboard/app.py` helper load and filter check
6. `python3 scripts/validate_public_release.py --root .`
7. `python3 scripts/validate_medical_ai_safety_field_kit_one_objection_gateway_20260620.py`
8. `python3 scripts/validate_safe_failure_card_issue_template_20260619.py`
9. `make validate-public`

Public text review result:

1. `overall_ok: True`
2. No forbidden visible process labels found in the new outward facing Markdown files.
3. Hyphen contexts were reported by the script, but the current audit skill does not block on hyphen count.

Reference verification script result:

1. `README.md`: no formal references extracted.
2. `docs/LEADERBOARD_PLAN.md`: no formal references extracted.
3. `docs/EXTERNAL_PR_STATUS_20260627.md`: no formal references extracted.
4. Official source claims were checked manually through GitHub CLI and official HuggingFace documentation.

## Git Status

Could not create a local commit because the sandbox can read `.git` but cannot write the Git index.

The exact failure from `git add` was:

```text
fatal: Unable to create '.git/index.lock': Operation not permitted
```

No push was attempted.
