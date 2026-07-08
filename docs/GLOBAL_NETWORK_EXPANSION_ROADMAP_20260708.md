# Global Network Expansion Roadmap

Date: 2026 07 08

Status: internal operating plan. No external collaboration, acceptance, endorsement, clinical validation, deployment, or regulatory claim is made here.

## Core decision

The next useful move is not another broad outreach note.

MedFailBench needs visible tasks that let outside people contribute in one hour, one day, or one pull request. A model team, benchmark maintainer, informatics researcher, or clinician should see a concrete task instead of a general request for feedback.

## Best next channels

### 1. Evaluation infrastructure

Targets:

1. Inspect Evals
2. LM Evaluation Harness
3. Medmarks
4. MedPerf

Why:

These projects already sit where model evaluators work. MedFailBench should enter through small adapters, not through a new standalone workflow.

First artifact:

1. Inspect Evals adapter issue in the MedFailBench repo.
2. LM Evaluation Harness task issue in the MedFailBench repo.
3. Medmarks and MedPerf follow up only after the local adapter is cleaner.

Status:

Local adapter foundations already exist. Public starter issues are the next step.

### 2. Standards and governance

Targets:

1. CHAI
2. HL7 AI Transparency on FHIR

Why:

MedFailBench can turn model run outputs into a clear safety and transparency card. That is a better collaboration hook than a leaderboard claim.

First artifact:

One public task for mapping SafetyGuard output fields to an AI transparency card.

Status:

Do not claim CHAI membership, HL7 publication status, certification, or compliance. Treat these as source informed design lenses only.

### 3. Informatics and evidence communities

Targets:

1. OHDSI Generative AI and Foundational Models workgroup
2. AMIA working groups and AI task force route

Why:

These communities understand evidence generation, EHR context, and clinical informatics. MedFailBench can offer a small synthetic safety review package, not patient data and not a clinical deployment claim.

First artifact:

One public task that asks contributors to propose the best OHDSI or AMIA route for synthetic clinical AI safety review.

Status:

No submission, membership, speaker slot, partnership, or acceptance claim is made.

### 4. China model and open source teams

Targets:

1. Hunyuan
2. InternLM and OpenCompass
3. MiniMax
4. Baidu Research or Paddle ecosystem
5. Existing live routes: Qwen, DeepSeek, Kimi, GLM

Why:

The first China wave already reached Qwen, DeepSeek, Kimi, GLM, OpenCompass, CMB, HuatuoGPT, General Medical AI, GMAI MMBench, LiveMedBench, OpenMEDLab, and Awesome AI4Med. The next wave should not repeat the same message. It should ask model teams to run one synthetic safety prompt pack or review one bilingual failure mode.

First artifact:

One public task for Chinese model team run notes and one public task for Turkish and Chinese clinical wording review.

Status:

Do not send the next third party wave until the public tasks are live and the user explicitly asks to send.

## Public starter issues to open now

1. Inspect Evals adapter for MedFailBench safety layer.
2. LM Evaluation Harness task for Turkish clinical source support.
3. AI transparency card mapping for SafetyGuard outputs.
4. OHDSI or AMIA route note for synthetic medical AI safety review.
5. Chinese model team run notes for synthetic safety prompts.
6. Turkish and Chinese clinical safety wording review.

## Follow up wave after the issues are live

Priority:

1. Hunyuan open source email or issue.
2. InternLM route through GitHub issue or verified email.
3. MiniMax route through GitHub issue or contact page.
4. Baidu Research route only after a better model team contact is verified.
5. CHAI, OHDSI, AMIA only after a focused public packet exists.

The message should ask for one bounded action:

1. Run a small synthetic prompt set.
2. Review one safety gate.
3. Review one language pair.
4. Comment on one adapter path.

## Boundaries

1. Synthetic cases only.
2. No patient data.
3. No clinical advice.
4. No clinical validation claim.
5. No model ranking claim.
6. No official compatibility claim.
7. No endorsement, partnership, membership, or submission claim.

## Success criteria for this week

1. Six public collaboration issues open in the MedFailBench repo.
2. Labels make the tasks easy to find.
3. BAGLAM2 records the new network infrastructure.
4. Next third party wave has a clear target and a clear ask.
