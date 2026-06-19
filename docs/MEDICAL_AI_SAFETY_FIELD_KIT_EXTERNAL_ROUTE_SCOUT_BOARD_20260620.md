# Medical AI Safety Field Kit External Route Scout Board

Status: public scout board for choosing where not to post yet.

Date: 2026 06 20

Purpose: turn external distribution into a visible decision process. The board records public issue routes that were checked before any outside comment is made.

Primary link:

https://github.com/v0id-lab/medical-ai-failure-atlas/issues/153

Workbook:

https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_GLOBAL_SAFETY_CLAIM_REVIEW_WORKBOOK_20260620.md

## Decision rule

Post outside this repository only when all conditions are true:

1. The issue or discussion is open.
2. The current thread already asks about medical AI evaluation, benchmark interpretation, source support, safety claim language, or readiness wording.
3. A short resource link would answer the thread rather than redirect it.
4. The comment can avoid institution, partner, validation, deployment, ranking, score, source truth, funding, payment, terms, or application claims.
5. The comment does not tag people or institutions.

If any condition fails, the decision is hold or watch.

## Current route checks

Route: https://github.com/The-AI-Alliance/trust-safety-evals/issues/50

Why checked: The issue asks to add MedHELM to a healthcare risk ranking effort with taxonomy, evaluations, and leaderboards.

Decision: Post

Reason: The workbook directly fits as a claim boundary checklist for avoiding wording where benchmark rank becomes safety proof. The comment must stay short and must not claim AI Alliance review, adoption, partnership, validation, leaderboard effect, clinical readiness, or endorsement.

Route: https://github.com/openai/simple-evals/issues/83

Why checked: HealthBench medical category mapping is active and recent.

Decision: Watch

Reason: The thread asks for category mapping, not safety claim review. A workbook link may distract unless the thread moves to claim wording or use guidance.

Route: https://github.com/openai/simple-evals/issues/109

Why checked: HealthBench uncertainty display affects benchmark interpretation.

Decision: Hold

Reason: The thread is a statistics bug report. A safety claim workbook link would not directly answer the bug.

Route: https://github.com/stanford-crfm/helm/issues/4187

Why checked: MedHELM exact match scoring behavior shows how small wording changes can alter evaluation outcome.

Decision: Watch

Reason: The issue is technical and already has maintainer guidance. Post only if a maintainer asks for broader interpretation or public wording guidance.

Route: https://github.com/mlcommons/endpoints/issues/178

Why checked: HealthBench integration may become a benchmark implementation route.

Decision: Hold

Reason: The issue body is too sparse. A workbook link would be premature.

Route: https://github.com/YLab-Open/BRIDGE/issues/4

Why checked: BRIDGE already has a relevant public route comment from this project.

Decision: Watch

Reason: Do not add another outside comment unless someone replies or asks for a more specific workbook link.

## Best next outside route

Best post candidate: https://github.com/The-AI-Alliance/trust-safety-evals/issues/50

Reason: it is open, public, MedHELM related, and explicitly about taxonomy, evaluations, leaderboards, and healthcare risk ranking.

Best watch candidate: https://github.com/openai/simple-evals/issues/83

Reason: it is recent, public, HealthBench related, and has another user signal. It still needs a topic shift toward safety claim wording, category use limits, or public benchmark interpretation before posting the workbook.

## Safe comment shape if a route becomes ready

```text
Related resource, if useful for claim wording:

The Medical AI Safety Field Kit has a public workbook for checking whether benchmark or readiness wording is becoming too strong:

https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_GLOBAL_SAFETY_CLAIM_REVIEW_WORKBOOK_20260620.md

Boundary: synthetic or public examples only. No patient data, clinical validation, deployment, ranking, score certification, partner claim, institution claim, endorsement, payment, terms, or application claim.
```

## Contributor ladder for issue 153

Level 1 route scout:

Add one exact public issue or discussion URL, why it is relevant, and a post or hold decision.

Level 2 risk mapper:

Explain which safety claim risk the route touches: source support, benchmark interpretation, Turkish wording, hospital readiness wording, governance wording, or no ranking misuse.

Level 3 comment drafter:

Draft a short comment that answers the active thread and includes the workbook only if it helps the thread.

Level 4 maintainer closeout:

After a maintainer checks the route, mark it as post, hold, or watch. Owner comments do not count as external review.

## Current action

One outside comment is cleared after audit:

https://github.com/The-AI-Alliance/trust-safety-evals/issues/50

Public action cleared now: comment on issue 153 with this board.

## Boundary

This board does not claim review, endorsement, partnership, institution approval, clinical validation, clinical deployment, benchmark ranking, score certification, source truth certification, payment, terms acceptance, TBYS action, PRODIS action, or formal application status.
