# Qwen Team Feedback

Status: sent as a follow-up to `QwenLM/Qwen3#1877` on 2026-07-11.

Sent comment: https://github.com/QwenLM/Qwen3/issues/1877#issuecomment-4944990823

## Audited result

- Model route: `qwen/qwen3-max`
- Route label at evaluation time: Qwen3 Max
- Prompt set: 30 synthetic clinician-authored hard cases
- Completed responses: 30/30
- Rule-based safety score after scorer correction: 4.0/5.0
- Safety-gate triggers after correction: 0/30
- Interpretation: no rule-based urgent-escalation, unsafe remote-dosing, or unsafe-reassurance gate was triggered. This is preliminary automated screening, not clinical validation or a safety certification.

## Correction disclosed to the team

The first draft was not sent because the scorer treated negated warnings such as “do not wait until morning” and benign uses of “reassuring” as unsafe discharge advice. Regression tests were added and the 30-case artifact was regenerated before outreach.

## Reproducibility

- Raw outputs: `model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_raw_outputs.json`
- Corrected rule scores: `model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_rule_scores.json`
- Scorer: `failure_atlas/scorer.py`
- Rubric: `data/scoring_rubric_v0_3.json`
- Repository: https://github.com/goktugozkanmd/medical-ai-failure-atlas
- DOI: https://doi.org/10.5281/zenodo.21205535
