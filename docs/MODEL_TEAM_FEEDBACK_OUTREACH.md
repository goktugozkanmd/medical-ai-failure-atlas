# Model Team Feedback Outreach Queue

Status: draft queue. Do not send externally without G approval.

Source drafts:
- `docs/model_team_feedback/qwen_team_feedback.md`
- `docs/model_team_feedback/deepseek_team_feedback.md`
- `docs/model_team_feedback/glm_zhipuai_team_feedback.md`
- `docs/model_team_feedback/kimi_moonshot_team_feedback.md`

Core message:

> We built a synthetic, clinician-authored medical AI safety benchmark. Your model family appears in the current rule-based snapshot. This is not a ranking and not clinical validation. The useful part is prompt-level failure analysis. If your team wants, I can share the prompt-level JSON and adapt the suite for your QA workflow.

## Send order

1. Qwen: strongest high-sample finding, Qwen 3.7 Max 14/30 unsafe-tier prompts.
2. GLM/ZhipuAI: 28-prompt run, 11/28 unsafe-tier prompts.
3. DeepSeek: consistent source-support score 48.0 across V3.2, V4 Flash, V4 Pro.
4. Kimi/Moonshot: highest unsafe-tier rates, but small prompt counts; phrase cautiously.

## Pre-send checklist

- [ ] G approved the target and channel.
- [ ] The exact prompt-level example is verified against raw model output.
- [ ] No patient data.
- [ ] No clinical validation claim.
- [ ] No model ranking claim.
- [ ] Tone is feedback/collaboration, not accusation.
