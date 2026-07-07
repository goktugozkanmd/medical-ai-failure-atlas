# Reference and Claim Audit: EU AI Act Clinical Safety Whitepaper

Artifact: `docs/BENCHMARKING_CLINICAL_AI_SAFETY_FOR_EU_AI_ACT_CONFORMITY.md`
Date: 2026-07-07
Decision: pass after scope limits. The whitepaper is author-review ready, not legal-review ready, not journal submit-ready, and not regulatory submit-ready.

## Summary

- References checked: 19.
- External source anchors checked: 13.
- Internal repository artifacts checked: 6 groups.
- Bibliographic hallucination found: 0.
- Claim-support blockers found: 0 after conservative wording.
- Required boundary language present: yes.

## Verified references

| # | Source | Verification route | Status | Supports |
| ---: | --- | --- | --- | --- |
| 1 | European Commission AI Act regulatory framework page | Live fetch succeeded | verified | Risk-based approach, high-risk obligations, application timeline, Commission implementation language. |
| 2 | European Commission Navigating the AI Act FAQ | Live fetch succeeded | verified | High-risk examples including medical treatment assessment and medical-device-linked AI systems. |
| 3 | AI Act Service Desk Article 9 | Live fetch succeeded | verified | Risk management system requirements for high-risk AI systems. |
| 4 | AI Act Service Desk Article 10 | Live fetch succeeded | verified | Data governance and dataset quality requirements. |
| 5 | AI Act Service Desk Article 11 | Live fetch succeeded | verified | Technical documentation before market placement or service. |
| 6 | AI Act Service Desk Article 12 | Live fetch succeeded | verified | Record keeping and logging summary. |
| 7 | AI Act Service Desk Article 13 | Live fetch succeeded | verified | Transparency and information to deployers summary. |
| 8 | AI Act Service Desk Article 14 | Live fetch succeeded | verified | Human oversight requirements. |
| 9 | AI Act Service Desk Article 15 | Live fetch succeeded | verified | Accuracy, robustness, cybersecurity, and benchmark methodology encouragement. |
| 10 | AI Act Service Desk Article 43 | Live fetch succeeded | verified | Conformity assessment routes. |
| 11 | AI Act Service Desk Article 57 | Live fetch succeeded | verified | Regulatory sandbox controlled environment, guidance, supervision, and documentation. |
| 12 | MedFailBench Zenodo DOI 10.5281/zenodo.21205535 | Live fetch succeeded | verified | v0.2.1 release, clinician-built synthetic evaluation resource, not clinical advice, not model ranking, not clinically validated decision support. |
| 13 | GitHub repository | Live fetch succeeded | verified | README, live public artifact, public benchmark scope. |
| 14 | `leaderboard/submissions.json` | Local file read | verified | 10 public leaderboard model submissions. |
| 15 | `model_runs/worst_case_safety_report_v0_1.json` | Local file read | verified | 11 worst-case report rows including historical row. |
| 16 | `docs/SAFETY_GATE_TAXONOMY_V0_2.md` | Local file read | verified | Safety gate names and definitions. |
| 17 | Scenario-bank TSV files | Local Python count through terminal | verified | 150 total scenario-bank rows. |
| 18 | Prompt-set TSV files | Local Python count through terminal | verified | 70 total prompt rows. |
| 19 | `COMPLIANCE.md` | Local file read | verified | Existing MedFailBench EU AI Act compliance positioning page. |

## Claim-support audit

| Claim | Support | Fit | Action |
| --- | --- | --- | --- |
| EU AI Act high-risk obligations include risk assessment, dataset quality, logging, documentation, transparency, human oversight, accuracy, robustness, and cybersecurity. | European Commission AI Act page and AI Act FAQ. | direct | keep |
| Article 9 requires a documented risk management system for high-risk AI systems. | AI Act Service Desk Article 9. | direct | keep |
| Article 10 concerns data governance and dataset quality. | AI Act Service Desk Article 10. | direct | keep |
| Article 11 concerns technical documentation. | AI Act Service Desk Article 11. | direct | keep |
| Article 12 concerns record keeping and logging. | AI Act Service Desk Article 12. | direct, summary page | keep with summary-source awareness |
| Article 13 concerns transparency and information to deployers. | AI Act Service Desk Article 13. | direct, summary page | keep with summary-source awareness |
| Article 14 concerns human oversight. | AI Act Service Desk Article 14. | direct | keep |
| Article 15 concerns accuracy, robustness, cybersecurity, and encourages benchmarks and measurement methodologies. | AI Act Service Desk Article 15. | direct | keep |
| Article 43 concerns conformity assessment procedures. | AI Act Service Desk Article 43. | direct | keep |
| Article 57 describes AI regulatory sandboxes as controlled environments for development, testing, validation, guidance, and supervision before market placement or service. | AI Act Service Desk Article 57. | direct | keep |
| Medical treatment assessment and AI systems operating medical devices can fall into high-risk categories under Commission FAQ language. | European Commission Navigating the AI Act FAQ. | direct | keep; avoid saying every medical AI is automatically high-risk |
| MedFailBench v0.2.1 is a clinician-built synthetic evaluation resource and is not clinical advice, not a model ranking, and not clinically validated decision support. | Zenodo DOI page. | direct | keep |
| The repository currently has 150 scenario-bank rows and 70 prompt rows. | Local row-count command over TSV files. | direct | keep |
| The repository currently has 10 public leaderboard model submissions and 11 worst-case report rows. | Local JSON count command. | direct | keep |
| MedFailBench can support broader EU AI Act readiness and conformity-assessment preparation. | Articles 9, 10, 11, 13, 14, 15, 43 plus MedFailBench artifacts. | interpretive, not certification | keep only with boundary language |

## Boundary audit

Required boundary language is present in the whitepaper:

- not legal advice;
- not a regulatory submission;
- not a conformity assessment;
- not CE marking evidence by itself;
- not a medical device claim;
- not clinical validation;
- not clinical deployment guidance;
- not a notified-body audit;
- not a model ranking;
- not an endorsement.

## Problems

None found after drafting. The main risk was overclaiming that MedFailBench itself demonstrates conformity. The final wording says it can provide supporting evidence inside broader readiness or conformity-assessment work.

## Submit decision

Pass after scope limits.

- Repository publication: pass.
- External legal/regulatory use: blocked until legal review.
- Journal submission: blocked until target venue rules, author approval, and formal reference style are prepared.
