# Model Team Feedback Outreach

Status: Qwen and DeepSeek outreach sent on 2026-07-11. GLM was not reopened after its prior decline. Kimi remains withheld because the available runs are too small for model-level feedback.

This packet is structured technical feedback, not a public ranking, clinical validation, deployment recommendation, or safety certification.

## Audit correction

The pre-send audit found that the rule scorer treated negated warnings such as “do not wait until morning” and benign uses of “reassuring” as unsafe discharge advice. A later audit found that the first corrected rerun scored legacy raw files without `prompt_text`, so prompt-dependent escalation checks did not execute. The raw artifacts now include the canonical prompts, promptless scoring fails closed, and both 30-case score files were regenerated.

## Current target state

- Qwen: sent at https://github.com/QwenLM/Qwen3/issues/1877#issuecomment-4944990823. Prompt-linked rescoring produced four lexical `missed_urgent_escalation` alerts. Technical review found explicit escalation or management content in the flagged answers; clinician adjudication is pending.
- DeepSeek: sent at https://github.com/deepseek-ai/DeepSeek-V3/issues/1489. Prompt-linked rescoring produced five `missed_urgent_escalation` alerts and one `unsafe_remote_dosing` alert. H001 and H009 also expose self-referential or truncated output behavior; clinician adjudication is pending.
- GLM/Z.ai: no new outreach. The prior collaboration contact was declined, and the new audit does not justify reopening it.
- Kimi/Moonshot: no external claim yet. Available Kimi runs cover only 5 and 6 prompts, so they are insufficient for model-level feedback.

## Mandatory language

Every external note must state that the prompts are synthetic, the result is rule-based and preliminary, and no clinical validation or safety-certification claim is being made.

## Evidence

- `docs/model_team_feedback/qwen_team_feedback.md`
- `docs/model_team_feedback/deepseek_team_feedback.md`
- `model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_raw_outputs.json`
- `model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_rule_scores.json`
- `model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_raw_outputs.json`
- `model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_rule_scores.json`
- https://github.com/goktugozkanmd/medical-ai-failure-atlas
