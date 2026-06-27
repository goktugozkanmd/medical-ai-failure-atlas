# Codex Task: Flagship Project Transformation

## Context
You are working on the medical-ai-failure-atlas repository for Dr. Goktug Ozkan, an internal medicine doctor in Turkey. This is his flagship open-source project. The goal is to make this project visible, usable, and authoritative in the medical AI space.

## Current Problems
1. README is 1387 lines — way too long, nobody will read it. It starts with "outside objection" instructions which makes no sense for a first-time visitor.
2. 10 open issues — most are meta/process issues (objection examples, TUBITAK, TUSEB) that confuse visitors. They should be closed or archived.
3. 0 GitHub stars — the project is invisible.
4. No interactive demo — no HuggingFace Space, no leaderboard people can try.
5. The project has good content (failure atlas, safety cards, evaluation data) but terrible presentation.

## Tasks (Do ALL of these)

### Task 1: Rewrite README.md
Write a NEW README.md that:
- Starts with a one-sentence tagline: "A clinician-built benchmark for medical AI safety evaluation"
- Has a demo GIF or screenshot placeholder at the top
- Explains what this is in 3 sentences a non-expert can understand
- Shows a table of contents
- Has a "Quick Start" section (install + run in 3 commands)
- Has a "What's Inside" section listing the key components
- Has a "Who is this for" section
- Has a "License" section (Apache-2.0 + CC-BY-4.0)
- Has a "Citation" section
- Total length: 200-300 lines MAX. Not 1387.
- Remove all the "outside objection" and "public reviewer call" stuff from the top. Move any useful meta content to docs/ if needed.
- Write in English (this is a global project).

### Task 2: Clean up issues
- Close issues #145, #146, #147, #148, #149, #150, #151, #152, #153, #154 with a comment "Consolidating project focus. See updated README."
- Keep only issues that are actual bugs or feature requests, not process/meta issues.

### Task 3: Prepare HuggingFace leaderboard
- Look at the leaderboard/ directory
- Create a plan (in docs/LEADERBOARD_PLAN.md) for deploying an interactive leaderboard on HuggingFace Spaces
- The leaderboard should let people see how different AI models perform on the medical safety tasks in this repo
- Include what data format is needed, what the Space UI would look like, and what code is needed
- If there's already leaderboard code, clean it up and make it ready to deploy

### Task 4: Consolidate and clean the repo structure
- Remove or archive any files that are not essential to the core project
- Make sure the directory structure is clean and logical
- Ensure data/ directory is well-organized
- Ensure failure_atlas/ directory is well-organized

### Task 5: Check PR status
- Check the status of open PRs to huggingface/lighteval#1272 and UKGovernmentBEIS/inspect_ai#4343
- Note any comments or review requests
- If there are actionable comments, prepare responses

## Rules
- Do NOT create new issues. Only close existing ones.
- Do NOT modify any data files or evaluation results.
- Do NOT change the license.
- Do NOT add AI co-author notes to any commits.
- Write clean, professional English.
- Use git for all changes. Commit with clear messages.
- Do NOT push to remote. Leave changes local for review.

## After completing all tasks
Write a summary of everything you did in docs/CODEX_SUMMARY.md
