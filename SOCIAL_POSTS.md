# Social Posts

## LinkedIn — 2026-07-02 MedFailBench live leaderboard

I’ve been building Medical AI Failure Atlas / MedFailBench: a clinician-built open-source benchmark for medical AI safety evaluation.

The point is simple: for medical AI, a wrong answer is not just wrong. The failure mode matters.

A missed urgent escalation is different from an unsupported guideline claim. Remote dosing advice without context is different from vague reassurance after a red flag.

Today I put the leaderboard live on Hugging Face and added a clinical severity distribution view:

- 44 synthetic clinician-reviewed cases
- severity 3: 7 cases
- severity 4: 14 cases
- severity 5: 23 cases
- safety gates for urgent escalation, remote dosing, discharge reassurance, evidence overclaim, and unsafe protocol detail

This is not clinical validation and not a model ranking. It is infrastructure for looking at medical AI failure modes more like a clinician would.

Repo: https://github.com/goktugozkanmd/medical-ai-failure-atlas
Live demo: https://huggingface.co/spaces/goktugozkanmd/medical-ai-failure-atlas

If you work on medical AI evaluation, benchmark design, or clinical safety review, I’d be interested in comparing notes.

## X — short version

I put the Medical AI Failure Atlas / MedFailBench leaderboard live on Hugging Face.

44 synthetic clinician-reviewed cases, now with clinical severity distribution:
severity 3: 7
severity 4: 14
severity 5: 23

Not clinical validation. Not a model ranking. A way to inspect medical AI failure modes by safety boundary.

Repo: https://github.com/goktugozkanmd/medical-ai-failure-atlas
Demo: https://huggingface.co/spaces/goktugozkanmd/medical-ai-failure-atlas
