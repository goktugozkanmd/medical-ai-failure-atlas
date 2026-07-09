# COMPLIANCE.md — MedFailBench as EU AI Act Clinical Safety Audit Framework

> **Purpose:** This document maps MedFailBench assets to EU AI Act conformity assessment
> requirements for high-risk medical AI systems (SaMD).
> **Status:** Exploratory — not a certified compliance tool.

---

## EU AI Act Landscape

The EU AI Act treats some health-related AI systems as high-risk. The European Commission FAQ gives medical treatment assessment as a high-risk example and notes that AI systems operating medical devices can be high-risk when tied to product legislation and third-party conformity assessment.

High-risk system readiness evidence should cover:

- Conformity assessment (Art. 43, Annex VII)
- Risk management system (Art. 9)
- Data governance (Art. 10)
- Technical documentation (Art. 11)
- Record keeping and traceability (Art. 12)
- Transparency and deployer information (Art. 13)
- Human oversight (Art. 14)
- Accuracy, robustness, cybersecurity (Art. 15)

**Problem:** No standard open clinical safety benchmark exists for Article 15 robustness evidence or Article 9 risk management evidence in medical language models.

---

## Asset → Requirement Mapping

| EU AI Act Art. | Requirement | MedFailBench Asset |
|---|---|---|
| 9 | Risk management system | Safety-gate taxonomy (5 clinical severity tiers) |
| 9 | Risk identification | Worst-case safety metric (% unsafe-tier) |
| 9 | Risk mitigation testing | Scenario bank (150+ clinical failure scenarios) |
| 10 | Data governance and bias monitoring | Synthetic scenario-bank labels and TR-EN clinical safety drift dataset |
| 11 | Technical documentation | Versioned prompt sets, release manifest, Zenodo DOI, public repo |
| 12 | Record keeping and traceability | Model-run metadata and version-controlled output provenance |
| 13 | Transparency | Open-source repo, boundary language, public leaderboard |
| 14 | Human oversight | Clinician-authored severity rubrics and clinician panel pilot protocol |
| 15 | Accuracy | Model-run results (10 models, rule-based scoring) |
| 15 | Robustness | Repeated eval runs, worst-case safety view, version-controlled prompt sets |

---

## Current Limitations

1. **Not legal advice or a notified-body audit.** This is a public research benchmark, not a CE-marking tool.
2. **Single-physician methodology.** Clinician-authored, not yet multiple independent raters (kappa pending).
3. **Limited model coverage.** 10 public leaderboard models, all rule-based scoring; not manufacturer-specific testing.
4. **No certified continuous monitoring pipeline.** Eval runs are versioned research artifacts, not a regulated production monitoring system.

---

## Future Direction

- Add EU AI Act compliance scenarios (manufacturer-use-case specific)
- Expand to UK MHRA / FDA alignment
- Create a "conformity assessment rubric" version of the scoring framework
- Whitepaper v0.1: ["Benchmarking Clinical AI Safety for EU AI Act Conformity"](../BENCHMARKING_CLINICAL_AI_SAFETY_FOR_EU_AI_ACT_CONFORMITY.md)

---

## References

Primary official sources:

- [European Commission AI Act regulatory framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [European Commission Navigating the AI Act FAQ](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act)
- [AI Act Service Desk: Article 9, risk management system](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-9)
- [AI Act Service Desk: Article 10, data and data governance](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-10)
- [AI Act Service Desk: Article 11, technical documentation](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-11)
- [AI Act Service Desk: Article 12, record keeping](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-12)
- [AI Act Service Desk: Article 13, transparency](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-13)
- [AI Act Service Desk: Article 14, human oversight](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14)
- [AI Act Service Desk: Article 15, accuracy, robustness, cybersecurity](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-15)
- [AI Act Service Desk: Article 43, conformity assessment](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-43)
- [AI Act Service Desk: Article 57, regulatory sandboxes](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-57)

Secondary commentary retained for context:

- [EU AI Act High-Risk Classification Guidelines (May 2026)](https://meddeviceguide.com/blog/eu-ai-act-high-risk-classification-guidelines-medical-device-guide)
- [EU AI Act for Medical Devices: SaMD Compliance Deadlines](https://mdxcro.com/eu-ai-act-medical-devices-samd/)
- [AI Act & AI-Enabled Medical Devices: Regulatory Status 2026](https://www.dqsglobal.com/en/explore/blog/ai-act-ai-enabled-medical-devices)
- [EU AI Act Omnibus — What 2026 Rules Mean for Medical Device Manufacturers](https://patientguard.com/the-ai-act-omnibus-explained-what-the-2026-eu-rules-mean-for-medical-device-and-ivd-manufacturers/)