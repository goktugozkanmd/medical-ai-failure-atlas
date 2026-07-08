# Model Team Feedback Outreach Queue

Status: draft queue, prepared for G review on 2026-07-08. Do not send externally without target-by-target G approval.

This packet is for respectful model-team feedback, not public accusation, ranking, clinical validation, deployment advice, or a safety certification claim. All figures below are from local repo artifacts and remain rule-based until clinician panel validation exists.

Source drafts:
- `docs/model_team_feedback/qwen_team_feedback.md`
- `docs/model_team_feedback/deepseek_team_feedback.md`
- `docs/model_team_feedback/glm_zhipuai_team_feedback.md`
- `docs/model_team_feedback/kimi_moonshot_team_feedback.md`

Core message:

> We built a synthetic, clinician-authored medical AI safety benchmark. Your model family appears in the current rule-based snapshot. This is not a ranking and not clinical validation. The useful part is prompt-level failure analysis. If your team wants, I can share the prompt-level JSON and adapt the suite for your QA workflow.

## Current evidence anchors

| Team | Current anchor | Source file | Send posture |
|------|----------------|-------------|--------------|
| Qwen / Alibaba | Qwen 3.7 Max: 14/30 unsafe-tier prompts in `worst_case_safety_report_v0_1.json` | `model_runs/worst_case_safety_report_v0_1.json`; `model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_rule_scores.json` | Strongest high-sample feedback, but avoid "worst model" phrasing. |
| GLM / ZhipuAI | GLM-5.2: 11/28 unsafe-tier prompts in `worst_case_safety_report_v0_1.json` | `model_runs/worst_case_safety_report_v0_1.json`; `model_runs/weekly_eval_glm-5.2_20260704_130522.json` | Useful because bilingual and clinical-boundary framing are relevant. |
| DeepSeek | DeepSeek V4 Pro hard30 now locally scored: 30/30 rows, 1 unsafe by current rule scorer | `model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_rule_scores.json` | Phrase as "new 30-prompt local scoring is ready for review"; do not overclaim source-support pattern without examples attached. |
| Kimi / Moonshot | Kimi K2.6 and K2.7 Code have small prompt counts with high unsafe-tier rates | `model_runs/worst_case_safety_report_v0_1.json` | Lower priority until a 30-prompt Kimi run exists; explicitly note sample size. |

## Send order

1. Qwen: strongest high-sample finding, with Qwen 3.7 Max 30-prompt data already public in repo artifacts.
2. GLM/ZhipuAI: 28-prompt run plus Turkish/English safety-drift relevance.
3. DeepSeek: new 30-prompt local scoring exists for DeepSeek V4 Pro; send only after exact examples are selected.
4. Kimi/Moonshot: useful but lower confidence because Kimi runs are still 5-6 prompt snapshots.

## One-paragraph note for first contact

> I am sharing this as structured feedback, not as a public ranking or clinical validation claim. MedFailBench uses synthetic clinician-authored safety prompts to find prompt-level failure modes such as missed urgent escalation, unsafe remote dosing, and false reassurance after partial negative tests. Your model family appears in the current rule-based snapshot, and I can share the exact prompt IDs, raw outputs, and safety-gate labels if your team wants to reproduce or improve against this suite.

## Per-team subject lines

- Qwen: `Prompt-level clinical safety feedback for Qwen models in MedFailBench`
- GLM/ZhipuAI: `GLM-5.2 clinical safety-gate feedback from MedFailBench`
- DeepSeek: `DeepSeek V4 Pro hard30 clinical safety feedback, local scoring ready`
- Kimi/Moonshot: `Kimi clinical safety feedback from a small MedFailBench prompt snapshot`

## Pre-send checklist

- [ ] G approved the target and channel.
- [ ] The exact prompt-level example is verified against raw model output.
- [ ] No patient data.
- [ ] No clinical validation claim.
- [ ] No model ranking claim.
- [ ] Tone is feedback/collaboration, not accusation.
- [ ] Academic submission/outreach audit completed for the exact outgoing text.
- [ ] Reference/source check completed for any DOI, URL, or benchmark claim in the outgoing text.
