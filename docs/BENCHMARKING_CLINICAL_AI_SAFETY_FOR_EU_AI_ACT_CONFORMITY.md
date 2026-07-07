# Benchmarking Clinical AI Safety for EU AI Act Conformity

Status: public whitepaper v0.1 for MedFailBench v0.2.1.
Date: 2026-07-07.
Scope: synthetic medical AI safety evaluation, conformity-assessment evidence support, and public claim hygiene.

This document is not legal advice, not a regulatory submission, not a conformity assessment, not CE marking evidence by itself, not a medical device claim, not clinical validation, and not clinical deployment guidance.

## Executive summary

The EU AI Act creates strict obligations for high-risk AI systems. Official European Commission material describes high-risk obligations around risk assessment and mitigation, dataset quality, logging, technical documentation, transparency, human oversight, accuracy, robustness, and cybersecurity. The AI Act text also requires risk management systems for high-risk AI systems, technical documentation before market placement or service, human oversight measures, and appropriate accuracy, robustness, and cybersecurity.

Clinical AI evaluation needs a practical evidence layer for these themes. General medical benchmark scores do not show whether a model fails on escalation, missing variables, source support, unsafe reassurance, or operational protocol language. MedFailBench addresses that gap as a clinician-authored, synthetic, rule-based safety benchmark. It does not certify a system. It produces structured evidence that a provider, evaluator, or reviewer can use inside a broader conformity assessment file.

The whitepaper position is narrow:

MedFailBench can serve as an open clinical safety audit layer for EU AI Act readiness work, especially for Article 9 risk management, Article 10 data governance, Article 11 technical documentation, Article 13 transparency, Article 14 human oversight, Article 15 accuracy and robustness, and Article 43 conformity assessment preparation.

## Why clinical AI needs a safety benchmark layer

Clinical AI failures are often not visible in aggregate accuracy. A model can sound fluent and still miss urgent escalation, give unsafe remote dosing advice, reassure a patient with unresolved red flags, or invent source support. These failures map more directly to patient safety review than to a generic task score.

The EU AI Act makes this distinction important. High-risk AI providers must manage risks over the lifecycle, test against defined metrics, document system characteristics, and enable human oversight. A benchmark for clinical AI conformity work should therefore ask four questions:

1. What clinical risk did the output create.
2. How severe is the risk.
3. Which missing variable or source gap caused the risk.
4. What evidence should a human reviewer see before trusting the output.

MedFailBench is built around those questions.

## EU AI Act requirements that need benchmark evidence

| EU AI Act theme | Official requirement signal | MedFailBench evidence role |
| --- | --- | --- |
| Article 9 risk management | High-risk AI systems need a documented, lifecycle risk management system that identifies and mitigates foreseeable risks to health, safety, and fundamental rights. | Safety-gate taxonomy, severity tiers, worst-case unsafe-tier rate, and failure-mode review. |
| Article 10 data governance | Training, validation, and testing datasets need governance around design choices, data origin, labeling, assumptions, suitability, bias, and gaps. | Synthetic-only scenario bank with explicit labels, safety gates, language layer, and no patient data. |
| Article 11 technical documentation | Technical documentation must provide clear information needed by authorities and notified bodies to assess compliance. | Versioned prompt sets, scoring rubric, leaderboard metadata, Zenodo DOI, and public release boundaries. |
| Article 12 record keeping | High-risk systems need logging capabilities that support traceability, post-market monitoring, and risk identification. | Version-controlled model-run metadata and output provenance for research evaluation runs. |
| Article 13 transparency | Deployers need clear information about system characteristics, capabilities, limitations, risks, human oversight, and maintenance. | README boundaries, model failure cards, source-support warnings, and no-deployment language. |
| Article 14 human oversight | Natural persons must be able to oversee, understand limitations, monitor outputs, avoid automation bias, and override or stop use. | Clinician-authored review prompts, reviewer questions, and clinician panel pilot protocol. |
| Article 15 accuracy, robustness, and cybersecurity | High-risk AI systems must achieve appropriate accuracy, robustness, and cybersecurity, and the Commission encourages benchmark and measurement methodology development. | Worst-case safety metric, unsafe-tier rate, repeated prompt-set evaluation, and language-drift probes. |
| Article 43 conformity assessment | Providers must follow the relevant conformity assessment procedure for high-risk systems, including internal control or notified-body routes depending on the system category. | Supporting evidence artifact, not a substitute for formal conformity assessment. |

## MedFailBench artifact base

Current public v0.2.1 artifact base:

- 150 scenario-bank rows across three TSV files.
- 70 prompt rows across three prompt sets.
- 10 public leaderboard model submissions with real, non-simulated eval notes.
- 11 rows in the worst-case safety report, including one historical row not shown in the public 10-model README table.
- A safety-gate taxonomy that names clinical failure modes such as missed urgent escalation, unsafe remote dosing, unsafe discharge reassurance, evidence fabrication or overclaim, unsafe protocol execution detail, and source support gap.
- Zenodo DOI release: 10.5281/zenodo.21205535.

These counts were checked from repository files before this whitepaper was written.

## Method model

MedFailBench treats model evaluation as a clinical safety review task rather than a leaderboard race.

### 1. Synthetic clinical scenario design

The benchmark uses synthetic scenarios only. It does not include patient records, private clinical text, or clinical deployment logs. This makes the benchmark easier to share publicly and easier to inspect without protected health data risk.

### 2. Safety-gate labeling

Each risky output can be assigned to a concrete safety gate. The gate is not a diagnosis. It is the reason a human reviewer must stop and inspect the answer.

Examples:

- `missed_urgent_escalation`: the answer may delay urgent evaluation.
- `unsafe_remote_dosing`: the answer implies medication change without needed variables.
- `unsafe_discharge_reassurance`: the answer reassures despite red flags.
- `evidence_fabrication_or_overclaim`: the answer invents or overstates source support.
- `unsafe_protocol_execution_detail`: the answer turns general guidance into operational protocol language without context.

### 3. Worst-case safety metric

Average scores can hide dangerous outliers. MedFailBench therefore reports the minimum observed safety score and the unsafe-tier rate. This better matches clinical risk review because a single unsafe answer can matter more than a moderate mean score.

### 4. Source-support review

Clinical safety depends on source support as well as tone. MedFailBench includes source-support scoring and SourceCheckup-style claim hygiene so reviewers can separate fluent unsupported claims from supported clinical language.

### 5. Human oversight readiness

The benchmark is designed to feed human review. It does not replace human review. Public materials should continue to say clinician-authored, synthetic, rule-based, and external clinician validation pending unless and until an independent panel result exists.

## Conformity-assessment use cases

MedFailBench can support, but not replace, the following evidence tasks:

1. Pre-market risk review for clinical language failure modes.
2. Regression testing after model, prompt, or system updates.
3. Human-oversight training for clinicians, reviewers, and safety teams.
4. Technical documentation appendices showing evaluation design and release boundaries.
5. Post-market monitoring design for complaint patterns, unsafe claims, and escalation failures.
6. Regulatory sandbox readiness discussions where a team needs a controlled, synthetic test layer before real-world testing.

## What MedFailBench must not claim

MedFailBench must not be described as:

- a certified EU AI Act compliance tool;
- a notified-body audit;
- CE marking evidence by itself;
- clinical validation;
- proof that a model is safe for patient care;
- a model ranking;
- medical advice;
- a partner, regulator, or institutional endorsement.

The safe wording is:

MedFailBench is an open, clinician-authored, synthetic clinical AI safety benchmark that can provide structured evidence for risk-management, transparency, human-oversight, robustness, and documentation discussions under broader EU AI Act readiness work.

## Implementation roadmap

### Near term

1. Keep COMPLIANCE.md linked from the README.
2. Keep this whitepaper linked from README and COMPLIANCE.md.
3. Add a conformity-assessment worksheet that maps each prompt to Article 9, 10, 13, 14, or 15 evidence categories.
4. Add a reviewer-facing risk register template with safety gate, severity, source gap, mitigation, and retest fields.
5. Keep public language conservative until external clinician panel validation is complete.

### Next validation step

The strongest next step is not a larger model leaderboard. The strongest next step is external clinician review:

- two or more independent clinicians;
- at least 20 synthetic cases;
- severity rating and safety-gate agreement;
- disagreement handling;
- inter-rater agreement report;
- updated whitepaper appendix.

## Reference anchors

Primary regulatory sources:

1. European Commission. AI Act regulatory framework page. https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
2. European Commission. Navigating the AI Act FAQ. https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act
3. AI Act Service Desk. Article 9, risk management system. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-9
4. AI Act Service Desk. Article 10, data and data governance. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-10
5. AI Act Service Desk. Article 11, technical documentation. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-11
6. AI Act Service Desk. Article 12, record keeping. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-12
7. AI Act Service Desk. Article 13, transparency and provision of information to deployers. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-13
8. AI Act Service Desk. Article 14, human oversight. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14
9. AI Act Service Desk. Article 15, accuracy, robustness, and cybersecurity. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-15
10. AI Act Service Desk. Article 43, conformity assessment. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-43
11. AI Act Service Desk. Article 57, AI regulatory sandboxes. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-57

MedFailBench sources:

1. Medical AI Failure Atlas repository. https://github.com/goktugozkanmd/medical-ai-failure-atlas
2. MedFailBench Zenodo v0.2.1 DOI. https://doi.org/10.5281/zenodo.21205535
3. `COMPLIANCE.md`
4. `docs/SAFETY_GATE_TAXONOMY_V0_2.md`
5. `leaderboard/submissions.json`
6. `model_runs/worst_case_safety_report_v0_1.json`
7. `data/scenario_bank_v1.tsv`, `data/scenario_bank_v2_hard_addendum.tsv`, `data/scenario_bank_v3_scale_seed.tsv`
8. `data/prompt_set_v1.tsv`, `data/prompt_set_v2_hard_30.tsv`, `data/prompt_set_v3_scale_30.tsv`

## Audit status

Reference and claim-support audit: see `docs/BENCHMARKING_CLINICAL_AI_SAFETY_FOR_EU_AI_ACT_CONFORMITY_AUDIT_20260707.md`.

Current decision: author-review ready. It is not legal review ready and not submit-ready for a journal or regulator.
