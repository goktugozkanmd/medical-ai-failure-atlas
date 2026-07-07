# Clinical AI Deployment Safety Audit Framework

**Side project proposal** — 2026-07-08

---

## Problem

Hospitals deploying clinical AI have no standard way to audit safety before go-live. Current practice:
- Internal ad-hoc testing with no repeatable methodology
- No standardized safety gate taxonomy applied to workflow-level AI
- Governance frameworks exist (EHRSource 2026, Wolters Kluwer 2026) but lack a benchmark component
- EU AI Act Article 9 (risk management) and Article 15 (robustness) require evidence — no open standard exists
- Turkey AI regulation (Bills 2/2234, 2/3358) creates legal obligation without compliance tools

## Solution

A structured audit framework that extends MedFailBench's safety-gate taxonomy from model-level to workflow-level evaluation. Output is an actionable **Clinical AI Safety Audit Report** that deployment teams can use for regulatory compliance and clinical governance.

## Components

| Component | What | MedFailBench Link |
|-----------|------|-------------------|
| Safety Gate Matrix | 5-gate taxonomy applied to workflow stages | Direct extension |
| Pre-deployment Test Suite | MedFailBench prompts + workflow-specific scenarios | Core data |
| Alert Quality Index | Measures over/under-alert ratio per model per workflow | False-reassurance gate |
| Governance Checklist | EU AI Act Art. 9-15 + Turkey regulation mapping | COMPLIANCE.md |
| Audit Report Template | Standardized output for regulatory review | New artifact |

## Target Users

1. Hospital AI/CIO teams deploying clinical LLMs (Turkey, then global)
2. Clinical AI vendors needing pre-deployment safety evidence
3. Regulatory bodies (CBDDO/Turkey, notified bodies/EU) needing standard evaluation methodology
4. Academic medical centers running clinical AI pilots

## Why G / MedFailBench

- Already has the safety-gate taxonomy — no one else does
- Already has COMPLIANCE.md mapping EU AI Act requirements
- Already has 10-model results showing worst-case safety
- G is a clinician — can speak the language of hospital safety committees
- Turkey AI regulation creates a first-mover advantage

## What Needs to Happen

| Step | Effort | Dependency |
|------|--------|------------|
| 1. Write methodology white paper | 1 day | — |
| 2. Create governance checklist from COMPLIANCE.md | 1 day | — |
| 3. Build audit report template (DOCX) | 1 day | — |
| 4. Pilot with 1 hospital (Acibadem/CASE?) | 2 weeks | G time + institutional relationship |
| 5. Publish methodology + template as open source | 1 day | G approval |
| 6. Write up as case study / blog post | 1 day | After pilot |

## This Run's Artifact

**Decision note + side project proposal** (this file). Next concrete step: methodology white paper outline + governance checklist.

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Overclaim: "certified compliance tool" | Always frame as "decision-support tool for internal audit" |
| Requires institutional partner for pilot | Acibadem/CASE is natural first partner — already have meeting pipeline |
| Scope creep into legal/compliance advisory | Stay in technical evaluation lane; include "consult your legal team" disclaimers |
| Turkey regulation still evolving | Monitor Bills 2/2234 debate; framework is modular by design |

## Go/No-Go

**Decision: Proceed to white paper outline.** Requires G confirmation to commit further time. This is a natural product extension of MedFailBench — not a distraction.