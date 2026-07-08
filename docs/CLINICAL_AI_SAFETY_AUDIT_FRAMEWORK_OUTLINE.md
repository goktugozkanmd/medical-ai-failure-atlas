# Clinical AI Safety Audit Framework — Outline (2026-07-08)

> P0 #4 from STATE_LEDGER. Design document for a structured clinical AI safety
> audit methodology built on MedFailBench infrastructure.
> Target: hospitals, health systems, and AI deployers who need regulatory compliance.
> Status: Outline only — G review needed before any implementation.

---

## What Is a Clinical AI Safety Audit?

A structured, repeatable process where a clinician (or panel) evaluates a medical AI
system against safety-critical scenarios and produces a risk report.

**Not** a benchmark (which compares models). An audit says: "this model, in this
deployment context, is safe/unsafe for clinical use."

---

## Market Need

- **EU AI Act:** Article 43 — conformity assessment for high-risk AI systems includes
  "testing procedures that are appropriate to the AI system"
- **US FDA:** AI/ML-enabled device software functions need "valid clinical association
  and analytical/clinical validation"
- **Hospital procurement:** No standard exists for evaluating clinical AI safety at
  point of procurement
- **Current gaps:** Microsoft Healthcare AI Model Evaluator is the closest competitor
  but is tech-focused, not clinician-driven

---

## Framework Architecture

### Components

1. **Scenario selection module** — Pulls from MedFailBench scenario bank, filters by
   clinical domain (cardiology, GI, infection) and failure mode (over-reliance,
   missing contradiction, soft escalation)
2. **Model evaluation interface** — Wraps SafetyGuard CLI, submits prompts, collects
   responses
3. **Clinician review interface** — Presents model output + scenario, captures:
   - Safety score (1-5)
   - Failure classification
   - Free-text clinical rationale
4. **Audit report generator** — Produces structured report with:
   - Overall safety assessment
   - Domain-specific risk profile
   - Failure mode breakdown
   - Recommendations (conditional pass, retest, fail)
   - EU AI Act conformity mapping

### Validation tier system (from MedFailBench infra)

| Tier | Validation level | Audit use |
|------|-----------------|-----------|
| Rule-based | Automatic, no clinician | Quick scan, pre-filter |
| Single clinician | One physician review | Operational audit |
| Panel (2+ with kappa) | Inter-rater reliability | Research/publication |

### Delivery format options

- CLI tool: `safetyguard audit --model ... --deployment hospital-ehr`
- Static report: PDF/HTML with physician attestation
- API service: POST model endpoint, receive audit report

---

## Relationship to Existing Projects

| Project | Connection |
|---------|-----------|
| MedFailBench scenarios | Core auditing material (150+ scenarios) |
| SafetyGuard CLI | Model evaluation engine |
| Scoring rubric v0.3 | Automated first-pass scoring |
| EU AI Act COMPLIANCE.md | Regulatory mapping layer |
| Clinician panel protocol | Future multi-rater capability |

---

## Next Steps (G decision needed)

1. **Go/Stop:** Should this become a formal project?
2. **Scope:** CLI tool only, or include SaaS/consulting layer?
3. **Timeline:** Q3 2026 prototype or Q1 2027?
4. **Output format:** Does G want a white paper, a tool, or both?

---

## Open Questions

- Pricing: Free open-source core + paid audit reports? Or fully open?
- Liability: Does an audit report create medical-legal exposure for the clinician?
  (Yes — needs legal review before any client-facing use)
- Partner: Acibadem/CASE as first pilot customer? Genel Dahiliyeciler Dernegi as
  methodology endorser?