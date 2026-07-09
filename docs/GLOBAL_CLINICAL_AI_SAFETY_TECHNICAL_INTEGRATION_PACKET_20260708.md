# Global Clinical AI Safety Technical Integration Packet

Date: 2026 07 08

Status: external outreach packet. Not sent until audit is complete.

## Purpose

This packet turns MedFailBench from a standalone repository into a collaboration object for existing medical AI benchmark and evaluation frameworks.

The ask is technical and concrete:

1. Add a small MedFailBench safety task.
2. Add a runner or adapter.
3. Compare clinical safety boundary scoring with existing medical benchmark scores.
4. Produce a shared report or paper if the integration is substantial.

## Target set

### Medmarks

Repo:

https://github.com/MedARC-AI/medmarks

Fit:

Medmarks is an open source LLM benchmark suite for medical tasks with runnable environments and evaluation configs.

Collaboration ask:

Explore a MedFailBench safety environment or small verified task subset focused on clinical safety boundary failures.

### MedHELM

Repo:

https://github.com/PacificAI/medhelm

Public benchmark page:

https://medhelm.org/

Fit:

MedHELM is a multi institutional medical LLM evaluation effort with a broad clinical task taxonomy.

Collaboration ask:

Explore whether MedFailBench can serve as a synthetic safety boundary companion task for medical LLM evaluation.

### MedPerf

Repo:

https://github.com/mlcommons/medperf

Fit:

MedPerf is an open benchmarking platform for medical AI using federated evaluation.

Collaboration ask:

Discuss whether synthetic safety boundary evaluation can become a lightweight non patient data companion benchmark.

### AgentClinic

Repo:

https://github.com/SamuelSchmidgall/AgentClinic

Fit:

AgentClinic evaluates clinical agents in simulated clinical environments across specialties and languages.

Collaboration ask:

Explore a safety boundary layer for sequential clinical agent behavior, especially escalation, uncertainty, and unsafe advice.

### MedAgentBench

Repo:

https://github.com/stanfordmlgroup/MedAgentBench

Fit:

MedAgentBench provides a virtual EHR environment for benchmarking medical LLM agents.

Collaboration ask:

Explore a clinical safety gate layer for medical agent actions and outputs in simulated EHR tasks.

## Shared message body

Hello [Team],

I am a physician from Turkey building MedFailBench, an open source clinical AI safety benchmark based on synthetic clinician authored cases.

Project:

https://github.com/goktugozkanmd/medical-ai-failure-atlas

I am looking for technical collaboration with medical AI benchmark and evaluation teams. The goal is to add a small clinical safety boundary evaluation layer that can complement existing medical benchmark scores.

MedFailBench focuses on cases where a model response may sound clinically fluent but crosses a safety boundary: missed urgent escalation, unsafe remote advice, unsupported certainty, weak source support, or unsafe safety net wording.

No patient data is involved. This is not clinical advice, not clinical validation, and not a deployment claim.

Would your team be open to discussing a small adapter, task integration, or shared pilot?

Best,
Goktug Ozkan

## Target specific opening lines

Medmarks:

Medmarks looks like a strong technical fit because it already organizes runnable medical LLM benchmark environments and evaluation configs.

MedHELM:

MedHELM looks like a strong conceptual fit because it evaluates medical LLMs across a broad clinical task taxonomy.

MedPerf:

MedPerf looks relevant because federated medical AI evaluation needs safety oriented companion tasks that do not require moving patient data.

AgentClinic:

AgentClinic looks highly relevant because sequential clinical agent behavior can fail at escalation, uncertainty, or unsafe advice even when a final answer looks plausible.

MedAgentBench:

MedAgentBench looks highly relevant because simulated EHR agents need safety gates around actions, advice, and output wording.

## Do not claim

Do not claim partnership.

Do not claim endorsement.

Do not claim clinical validation.

Do not claim deployment readiness.

Do not claim patient data use.
