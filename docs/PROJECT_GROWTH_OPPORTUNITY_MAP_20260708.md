# Project Growth Opportunity Map

Date checked: 2026 07 08

Status: internal strategy note for MedFailBench growth planning. Not an external release, not a collaboration claim, not a regulatory claim, not a clinical validation claim, and not a physician selection plan.

Owner boundary: G selects physicians and external reviewers. This note does not select, rank, or contact physicians.

## Core Decision

MedFailBench should not try to become another broad medical benchmark.

The strongest growth path is to become the clinical safety, failure, source support, and transparency layer that can sit beside broad benchmark systems.

Short positioning:

> MedFailBench is the failure layer for medical AI evaluation: worst answer review, escalation language, missing clinical variables, source support, Turkish clinical wording risk, and claim hygiene.

## Source Signals

### Broad benchmark space is crowded

OpenAI HealthBench is a broad health evaluation with 5,000 realistic health conversations, 262 physicians across 60 countries, physician written rubrics, multilingual multi turn cases, and 48,562 rubric criteria.

Implication: MedFailBench should not compete as a generic conversation benchmark. The better lane is high acuity failure behavior, source support, and worst case safety reporting.

### MedHELM is the best upstream adjacent ecosystem

MedHELM presents itself as an open, community led medical evaluation project with 121 clinical tasks, 31 datasets, local first evaluation, a leaderboard, and explicit contribution paths for new clinical scenarios, new metrics, test suite requests, and GitHub issues.

Implication: the highest leverage external route is a MedHELM adjacent safety suite, not an isolated private benchmark.

### Inspect Evals is a realistic distribution route

Inspect Evals states that from 8 May 2026 community contributions move through the register folder, with submission via GitHub issue, arXiv URL, and source code link. It supports Python based eval distribution and many model providers.

Implication: MedFailBench needs a small Inspect compatible evaluation implementation, not only documentation.

### Hugging Face remains useful for visibility

Hugging Face documents leaderboards and evaluations as first class Hub artifacts for machine learning models, including LLMs and chatbots.

Implication: a small public Space or evaluation card that runs SafetyGuard on sample synthetic cases can grow visibility without clinical claims.

### Governance and transparency demand is increasing

The European Commission AI Act page describes transparency rules, GPAI obligations, high risk timelines, sandbox access, and critical sector testing support. ONC HTI 1 describes transparency requirements for AI and predictive algorithms in certified health IT. CHAI describes Model Card metadata expressed through the HL7 AI Transparency on FHIR implementation guide. NIST maintains AI risk management guidance. FDA draft guidance describes lifecycle and marketing submission documentation expectations for AI enabled device software functions. WHO guidance addresses large multi modal models in health.

Implication: MedFailBench should package outputs as evidence, transparency, and risk management artifacts. It should not claim compliance, approval, certification, device status, or official endorsement.

## Best Growth Tracks

### 1. SafetyGuard Studio

Goal: make SafetyGuard usable by non repo users.

Build:

1. Minimal web UI or Hugging Face Space for uploading model answers or pasting a response.
2. One click output: worst case report, missing variable flags, escalation wording flags, source support flags, and model card ready summary.
3. Demo mode with synthetic sample only.

Why it grows the project:

It turns the repo from a benchmark artifact into a usable safety tool.

First success metric:

One external maintainer or model team can run it without asking for setup help.

### 2. MedFailBench Adapter Pack

Goal: make MedFailBench run where evaluators already work.

Build:

1. Inspect Evals register ready implementation.
2. LM Evaluation Harness task wrapper.
3. MedHELM adjacent scenario and metric packet.
4. Hugging Face evaluation card with clear boundary language.

Why it grows the project:

It moves MedFailBench into existing eval ecosystems rather than asking everyone to adopt a new workflow.

First success metric:

One accepted upstream issue, PR, registry listing, or maintainer discussion.

### 3. SourceCheckup Medical

Goal: turn source support into a standalone project line.

Build:

1. Input: model answer plus optional sources.
2. Output: supported, unsupported, source needed, or overclaimed.
3. Medical specific warning set: guideline claim, drug dose claim, diagnostic certainty claim, institution claim, regulatory claim, endorsement claim.
4. Turkish and English examples.

Why it grows the project:

Most medical AI demos fail through confident unsupported claims, not only wrong facts. This gives MedFailBench a sharper and reusable product.

First success metric:

Twenty public synthetic examples and a runnable CLI report.

### 4. Turkish Clinical SafetyBench

Goal: own the Turkish clinical wording and safety drift lane.

Build:

1. Bilingual paired prompts.
2. Turkish ambiguity tags.
3. Escalation wording drift checks.
4. Source support and guideline claim checks.

Boundary:

No new cases are added without G approval. No patient data. No clinical validation claim.

Why it grows the project:

HealthBench and MedHELM are broad. Turkish clinical safety drift is a narrower, more defensible lane for a clinician builder in Turkiye.

First success metric:

A small approved public preview with explicit validation tier labeling.

### 5. AI Transparency Card Exporter

Goal: turn each evaluation run into a transparent evidence artifact.

Build:

1. JSON and Markdown export from SafetyGuard outputs.
2. Fields aligned to common transparency concepts: intended use, data boundary, model version, evaluation date, prompt set, safety failures, source support limitations, human review status.
3. CHAI and HL7 AI Transparency on FHIR inspired mapping note, with no affiliation or compliance claim.

Why it grows the project:

Hospitals, model teams, and researchers increasingly need documentation, not only scores.

First success metric:

Every run produces a clean assurance card without manual writing.

### 6. Medical AI Benchmark Boundary Index

Goal: become the place that explains what each medical benchmark proves and does not prove.

Build:

1. Index of HealthBench, MedHELM, BRIDGE, LiveMedBench, Open Medical LLM Leaderboard, and MedFailBench.
2. Fields: task type, data boundary, language coverage, scoring style, open contribution route, and what not to claim.
3. Monthly refresh note.

Why it grows the project:

It makes MedFailBench a field navigation project, not only a dataset.

First success metric:

One concise public table that others can cite for benchmark selection.

### 7. Clinical AI Literacy Simulator

Goal: use failure cases as training material.

Build:

1. Twenty minute synthetic case module.
2. Before and after answer comparison.
3. Red flag checklist.
4. Instructor notes without institution claims.

Why it grows the project:

It turns safety failures into education. This can support CASE style demos without requiring patient data or clinical deployment.

First success metric:

A local module that can be shown in a short meeting.

### 8. Medical AI Safety Monitoring Bot

Goal: track public medical AI benchmark, governance, and model evaluation changes.

Build:

1. Source watcher over official benchmark pages, GitHub issues, model release notes, and regulator pages.
2. Daily internal digest.
3. No external posts without G approval.

Why it grows the project:

The field moves fast. A watcher turns the project into a living observatory.

First success metric:

Three verified route changes captured in BAGLAM2 or a repo note without manual search.

## Priority Order

1. SafetyGuard Studio plus Adapter Pack.
2. SourceCheckup Medical.
3. Turkish Clinical SafetyBench.
4. AI Transparency Card Exporter.
5. Benchmark Boundary Index.
6. Clinical AI Literacy Simulator.
7. Safety Monitoring Bot.

Reason:

The first two create immediate usability and external visibility. The third creates a distinctive Turkiye lane. The fourth converts results into governance ready evidence. The others support field positioning.

## Thirty Day Build Plan

### Week 1

1. Publish this internal growth map.
2. Add SafetyGuard demo mode to a local or Space ready UI.
3. Create adapter skeleton for Inspect Evals and LM Evaluation Harness.

### Week 2

1. Build SourceCheckup Medical CLI report.
2. Create 10 to 20 source support examples from synthetic material only.
3. Prepare a small upstream route issue draft.

### Week 3

1. Build transparency card exporter from SafetyGuard outputs.
2. Create one run level evidence card.
3. Add governance mapping note with explicit non claim boundaries.

### Week 4

1. Prepare a benchmark boundary index.
2. Prepare one public demo page.
3. Decide which external issue, PR, or discussion is worth asking G to approve.

## Do Not Do Now

1. Do not create another broad HealthBench style benchmark.
2. Do not use patient data.
3. Do not claim clinical validation.
4. Do not claim regulatory compliance.
5. Do not rank physicians or select reviewers.
6. Do not start paid model runs without approval.
7. Do not start automation loops unless G asks.
8. Do not send external posts, email, comments, or PRs without G approval.

## Next Concrete Task

Build the SafetyGuard Studio plus Adapter Pack foundation:

1. Add a small local web UI for SafetyGuard dry run output.
2. Add an Inspect Evals adapter skeleton.
3. Add a clear README section that says this is a failure layer, not clinical validation.
4. Run the public validator.
