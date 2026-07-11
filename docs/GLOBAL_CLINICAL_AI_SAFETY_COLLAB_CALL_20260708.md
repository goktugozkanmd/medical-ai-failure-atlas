# Global Clinical AI Safety Collaboration Call

Date: 2026 07 08

Status: public call text. Prepared for the MedFailBench repository.

## Why this exists

MedFailBench is a clinician built open source benchmark for testing where medical AI outputs cross safety boundaries.

Most medical AI benchmarks ask whether a model knows the answer. MedFailBench asks a different question: what clinical safety boundary failed?

The current focus is synthetic clinical cases only. No patient data is used.

## Collaboration goal

We want to build a global clinical AI safety collaboration around multilingual medical LLM evaluation.

The intended outputs are:

1. A shared synthetic clinical safety case set across Turkish, English, Chinese, and other languages.
2. A reproducible model evaluation report across frontier, open, and medical models.
3. A safety gate taxonomy that can be reused by benchmark and model teams.
4. Technical adapters for medical AI evaluation frameworks.
5. A coauthored paper or technical report if the collaboration produces enough shared work.

## What collaborators can do

Clinical contributors:

1. Add synthetic clinical safety cases.
2. Review whether a safety gate is clinically meaningful.
3. Improve wording for urgent escalation, uncertainty, medication risk, source support, and safety net advice.

Benchmark contributors:

1. Help map MedFailBench into existing medical AI benchmark frameworks.
2. Review scoring fields and failure categories.
3. Help compare safety boundary evaluation against exam style performance.

Model and platform contributors:

1. Run models through the synthetic case set.
2. Add reproducible model outputs.
3. Help define a fair reporting format that does not claim clinical validation.

Language contributors:

1. Add Turkish, Chinese, English, and other language variants.
2. Review whether translated cases preserve the same clinical safety risk.
3. Identify wording patterns that are unsafe in one language but less visible in another.

## Coauthor path

Coauthorship is not promised for a single comment. It is reserved for meaningful intellectual or technical contribution.

Examples of meaningful contribution:

1. A reviewed set of synthetic clinical cases.
2. A substantial safety taxonomy improvement.
3. A benchmark adapter or reproducible evaluation workflow.
4. A clinician review protocol contribution.
5. A language review that materially changes the benchmark.
6. A model evaluation contribution with reproducible outputs and interpretation.

## Boundaries

This project does not provide clinical advice.

This project does not use patient data.

This project does not claim clinical validation.

This project does not claim that benchmark performance proves clinical competence.

This project does not rank models for clinical deployment.

## Current repo

Project repo:

https://github.com/goktugozkanmd/medical-ai-failure-atlas

## First useful contribution

Open an issue with one of the following:

1. One synthetic clinical safety case.
2. One critique of a safety gate.
3. One benchmark integration suggestion.
4. One language review of a Turkish, English, or Chinese case.
5. One model output that shows a safety boundary failure.

## Short version

If you work on medical AI, LLM evaluation, clinical safety, multilingual benchmarks, or medical model deployment risk, this project is looking for collaborators who want to build a shared open benchmark rather than only discuss AI safety in general terms.
