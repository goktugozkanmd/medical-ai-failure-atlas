# Draft: MedHELM upstream issue / discussion

> Do not post blindly. Use this after one more pass for tone and maintainer-fit.

## Title

Proposal: synthetic clinician safety-gate scenarios for missing variables, escalation wording, and source-support risk

## Body

Hi MedHELM maintainers,

I am a clinician working on an open synthetic medical AI safety benchmark called Medical AI Failure Atlas / MedFailBench:

https://github.com/goktugozkanmd/medical-ai-failure-atlas

I am trying to align it with MedHELM-style clinical workflow evaluation rather than creating another isolated medical QA leaderboard.

The current MedFailBench focus is narrow:

- missing critical variables before clinical advice,
- unsafe escalation wording,
- weak source support,
- overconfident protocol language,
- Turkish clinical wording ambiguity,
- avoiding false validation/deployment/ranking claims.

The data are synthetic and public-safe. No patient records or private clinical text are used.

Would MedHELM prefer this kind of contribution as:

1. a proposed safety-gate scenario suite,
2. a small example scenario PR,
3. a proposed metric / issue for missing-variable and escalation-wording risk,
4. or a separate adapter that exports MedFailBench cases into a MedHELM-compatible scenario format?

I can start with a very small example around high-risk medication/symptom prompts where safe behavior requires asking for missing variables and avoiding overconfident reassurance.

Thanks.

Goktug Ozkan, MD
