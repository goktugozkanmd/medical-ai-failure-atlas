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

## LinkedIn — why exam-style medical benchmarks miss clinical failure modes

Most medical AI benchmarks still look too much like exams.

They ask whether a model can name the diagnosis, choose the right option, or summarize a guideline.

That is useful, but it misses the part that worries me as a clinician: a medical AI answer can sound correct and still fail at the safety boundary.

A few examples:

- chest pain with a normal first troponin: does the model keep urgent risk visible?
- severe sudden headache with normal exam: does it avoid false reassurance?
- medication toxicity risk: does it avoid remote dosing or protocol detail?
- evidence claims: does it refuse unsupported citation certainty?
- patient-facing wording: does it avoid language that feels like permission to wait at home?

That is why I am building Medical AI Failure Atlas / MedFailBench.

The goal is not another ranking table. The goal is to label the failure mode clearly enough that clinicians, benchmark builders, and model teams can discuss what actually went wrong.

This week I added:

- a live Hugging Face demo
- model submission flow
- collaborator call
- first real model response preview across 3 models and 5 hard clinical prompts

The early result is exactly the point: the hard part is not only medical knowledge. It is escalation, uncertainty, source support, and safe wording.

Repo: https://github.com/goktugozkanmd/medical-ai-failure-atlas
Demo: https://huggingface.co/spaces/goktugozkanmd/medical-ai-failure-atlas

If you work on medical AI evaluation or clinical safety review, I would value one narrow objection: pick one case, one safety gate, or one wording choice and tell me what is missing.

## X — exam benchmark version

Medical AI benchmarks should not only ask: “did the model know the answer?”

They also need to ask: “what safety boundary failed?”

MedFailBench now has a live demo, model submission flow, collaborator call, and first real model-response preview across 3 models / 5 hard clinical prompts.

Not a ranking. A failure-mode atlas.

---

## LinkedIn / X — 2026-07-05 v0.2.1: DOI, 100 cases, real eval

MedFailBench v0.2.1 is out with a persistent DOI (10.5281/zenodo.21205535), 100 clinician-reviewed synthetic cases across 10 specialty domains, and a CI-integrated weekly pipeline producing real (non-simulated) model responses.

What changed since v0.2.0:
- 44 → 100 synthetic cases (cardiology, emergency, endocrinology, neurology, nephrology, GI/hepatology, OB/women's health, geriatrics/polypharmacy, infectious diseases, source integrity)
- DRY-RUN era is over: Qwen 2.5-7B and Llama 3.1-8B now produce genuine outputs every week via a CI job
- Persistent Zenodo DOI for citation
- arXiv-ready preprint (built automatically on every PR)
- main branch protection — every change goes through PR + required CI checks
- Second clinician reviewer onboarded for inter-rater reliability data

Two real-model preview scores (rule-based, pending clinician panel validation):
- Qwen 2.5-7B: safety 52.0, source support 40.0, clinical boundary 63.2
- Llama 3.1-8B: safety 60.0, source support 56.0, clinical boundary 63.2

Not clinical advice. Not a model ranking. Not clinical validation. A clinician-built infrastructure for inspecting medical AI failure modes.

Cite as: Göktug Özkan. MedFailBench v0.2.1. Zenodo. https://doi.org/10.5281/zenodo.21205535
