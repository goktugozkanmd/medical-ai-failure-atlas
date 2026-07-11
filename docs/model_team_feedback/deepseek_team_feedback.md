# DeepSeek Team Feedback

Status: sent as first-contact outreach on 2026-07-11.

Sent issue: https://github.com/deepseek-ai/DeepSeek-V3/issues/1489

## Audited result

- Model route: `deepseek/deepseek-v4-pro`
- Route label at evaluation time: DeepSeek V4 Pro
- Prompt set: 30 synthetic clinician-authored hard cases
- Completed responses: 30/30
- Rule-based safety score after scorer correction: 4.0/5.0
- Safety-gate triggers after correction: 0/30
- Interpretation: no rule-based urgent-escalation, unsafe remote-dosing, or unsafe-reassurance gate was triggered. This is preliminary automated screening, not clinical validation or a safety certification.

## Correction disclosed to the team

The first draft’s 1/30 unsafe count was not sent. The flag came from a lexical false positive: the answer said not to wait until morning. Regression tests were added and the 30-case artifact was regenerated before outreach.

## Reproducibility

- Raw outputs: `model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_raw_outputs.json`
- Corrected rule scores: `model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_rule_scores.json`
- Scorer: `failure_atlas/scorer.py`
- Rubric: `data/scoring_rubric_v0_3.json`
- Repository: https://github.com/goktugozkanmd/medical-ai-failure-atlas
- DOI: https://doi.org/10.5281/zenodo.21205535
