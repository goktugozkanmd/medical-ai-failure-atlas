# COMPLIANCE.md — MedFailBench as EU AI Act Clinical Safety Audit Framework

> **Purpose:** This document maps MedFailBench assets to EU AI Act conformity assessment
> requirements for high-risk medical AI systems (SaMD).
> **Status:** Exploratory — not a certified compliance tool.

---

## EU AI Act Landscape (August 2026)

The EU AI Act classifies medical devices under MDR/IVDR as **high-risk AI systems** (Annex III, Art. 6).
Manufacturers must demonstrate:

- Conformity assessment (Art. 43, Annex VII)
- Risk management system (Art. 9)
- Data governance (Art. 10)
- Transparency (Art. 13)
- Human oversight (Art. 14)
- Accuracy, robustness, cybersecurity (Art. 15)

**Problem:** No standard clinical safety benchmark exists for Article 15 (accuracy/robustness)
or Article 9 (risk management) demonstration.

---

## Asset → Requirement Mapping

| EU AI Act Art. | Requirement | MedFailBench Asset |
|---|---|---|
| 9 | Risk management system | Safety-gate taxonomy (5 clinical severity tiers) |
| 9 | Risk identification | Worst-case safety metric (% unsafe-tier) |
| 9 | Risk mitigation testing | Scenario bank (150+ clinical failure scenarios) |
| 10 | Bias monitoring | TR-EN clinical safety drift dataset (50 paired cases) |
| 13 | Transparency | Open-source repo, Zenodo DOI, public leaderboard |
| 14 | Human oversight | Clinician-authored severity rubrics |
| 15 | Accuracy | Model-run results (10 models, rule-based scoring) |
| 15 | Robustness | Repeated eval runs, version-controlled prompt sets |

---

## Current Limitations

1. **Not a notified-body audit.** This is a public research benchmark, not a CE-marking tool.
2. **Single-physician methodology.** Clinician-authored, not multiple independent raters (kappa pending).
3. **Limited model coverage.** 10 models, all public API — not manufacturer-specific testing.
4. **No continuous monitoring pipeline.** Manual eval runs, not automated CI/CD.

---

## Future Direction

- Add EU AI Act compliance scenarios (manufacturer-use-case specific)
- Expand to UK MHRA / FDA alignment
- Create a "conformity assessment rubric" version of the scoring framework
- Publish a whitepaper: "Benchmarking Clinical AI Safety for EU AI Act Conformity"

---

## References

- [EU AI Act High-Risk Classification Guidelines (May 2026)](https://meddeviceguide.com/blog/eu-ai-act-high-risk-classification-guidelines-medical-device-guide)
- [EU AI Act for Medical Devices: SaMD Compliance Deadlines](https://mdxcro.com/eu-ai-act-medical-devices-samd/)
- [AI Act & AI-Enabled Medical Devices: Regulatory Status 2026](https://www.dqsglobal.com/en/explore/blog/ai-act-ai-enabled-medical-devices)
- [EU AI Act Omnibus — What 2026 Rules Mean for Medical Device Manufacturers](https://patientguard.com/the-ai-act-omnibus-explained-what-the-2026-eu-rules-mean-for-medical-device-and-ivd-manufacturers/)