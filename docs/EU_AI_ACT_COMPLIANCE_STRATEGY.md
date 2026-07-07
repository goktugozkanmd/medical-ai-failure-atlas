# MedFailBench — EU AI Act Compliance Positioning Strategy

## Executive Summary

The EU AI Act's high-risk classification for medical AI (SaMD) takes effect **August 2026**.
Manufacturers of AI-enabled medical devices must demonstrate conformity assessment, risk management,
and continuous monitoring. **No standard benchmark exists for clinical safety audit under the AI Act.**

MedFailBench can fill this gap.

---

## 1. The Regulatory Window (Aug 2026 — NOW)

Key deadlines:
- **August 2026**: High-risk AI system obligations apply (Annex III, Article 6)
- Medical devices classified under MDR/IVDR are **automatically high-risk** under the AI Act
- Requirements: risk management system, technical documentation, conformity assessment,
  human oversight, accuracy/robustness/cybersecurity

**What's missing:** A standardised, clinician-written, severity-graded clinical safety benchmark
that manufacturers can point to as part of their conformity assessment.

---

## 2. MedFailBench → Compliance Framework Mapping

| EU AI Act Requirement | MedFailBench Asset |
|---|---|
| Risk management system (Art. 9) | Safety-gate taxonomy (5 severity tiers) |
| Accuracy/robustness (Art. 15) | Worst-case safety metric (unsafe-tier %) |
| Human oversight (Art. 14) | Clinician-authored severity rubrics |
| Continuous monitoring | Scenario-bank + model-run versioning |
| Technical documentation | Zenodo DOI, public leaderboard, open repo |
| Bias/fairness (Art. 10) | TR-EN drift dataset (multilingual safety) |

---

## 3. Differentiation From Competitors

| Benchmark | Focus | EU AI Act Gap |
|---|---|---|
| MedSafetyBench (NeurIPS 2024) | Safety refusal (harmful prompts) | No severity grading, no continuous monitoring |
| HealthBench (OpenAI) | Overall safety+effectiveness | Proprietary, no open audit framework |
| CSEDB (Future Doctor, China) | Dual-track safety+effectiveness | Single-vendor, China regulatory focus |
| **MedFailBench** | **Worst-case safety + clinical severity** | **Directly maps to conformity assessment** |

---

## 4. Immediate Actions (No External Approval Needed)

1. **Rebrand SAFETY_GATE_TAXONOMY.md** as "conformity assessment rubric"
2. **Add EU AI Act article references** to existing rubrics
3. **Create a COMPLIANCE.md** showing the mapping table above
4. **Add "regulatory compliance scenario" category** to scenario bank
5. **Write a whitepaper outline**: "Benchmarking Clinical AI Safety for EU AI Act Conformity"

---

## 5. External Actions (G Approval Required)

- Submit to EU AI Act sandbox / regulatory sandbox programmes
- Contact notified bodies (TÜV SÜD, BSI) for feedback
- Publish in regulatory/medical device journals
- Present at MD&M or MedTech regulatory conferences

---

## 6. Risk Assessment

- **Overclaim risk**: Must not say "certified" or "approved". Say "conformity assessment"
  decision-support tool / "audit framework".
- **EU scope**: Initially position for EU market, then UK MHRA, then Türkiye.
- **Competition**: Established Notified Bodies may develop their own benchmarks.
  But none will have open, clinician-written, severity-graded public data.

---

## Karar

Bu yön en yüksek etkiyi vaat ediyor: Mevcut MedFailBench varlıklarını yeniden konumlandırarak
regülasyon compliance pazarına girmek. Dış onay gerektiren tek adım: whitepaper yayını.
Repo içi dokümantasyon değişiklikleri tamamen C0R3 tarafından yapılabilir.