# EU AI Act Health AI Sandbox Readiness Crosswalk

Date: 2026 06 19

Status: public readiness crosswalk for medical AI safety infrastructure.

Purpose: translate live EU AI Act implementation signals into a practical readiness map for health AI assurance work. This is built for Türkiye health AI safety infrastructure, Medical AI Failure Atlas, SourceCheckup Medical, clinician AI literacy, and data quality work that may need to speak clearly about sandbox readiness.

This crosswalk is not legal advice, not an EU sandbox application, not a regulatory submission, not a conformity assessment, not a CE marking claim, not a medical device claim, not clinical validation, not clinical deployment, not patient data use, not a partner claim, not an official role claim, not an endorsement claim, not payment, and not terms acceptance.

## Live source anchors

1. The European Commission AI Act page states that AI literacy obligations entered into application on 2 February 2025, obligations for general purpose AI models became applicable on 2 August 2025, and the AI Act is generally applicable on 2 August 2026 with exceptions.

Source: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

Readiness meaning: public medical AI work should already document AI literacy, role boundaries, and governance language before any sandbox or institutional route.

2. The European Commission AI Act page states that rules for systems used in certain high risk areas will apply from 2 December 2027, and rules for systems integrated into products will apply from 2 August 2028 under the simplification timeline described on that page.

Source: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

Readiness meaning: the project should separate general readiness work from product route, medical device route, and high risk system route.

3. The European Commission AI Act question page describes mandatory high risk system themes such as risk management, data quality, documentation and traceability, transparency, human oversight, accuracy, robustness, quality management, monitoring, incident response, and cooperation with authorities.

Source: https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act

Readiness meaning: the public readiness package should mirror these themes as evidence categories, without claiming compliance.

4. The same question page gives medical treatment assessment as an example of a high risk use case and separately notes that AI systems operating medical devices can be high risk when tied to product legislation.

Source: https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act

Readiness meaning: health AI safety work must preserve a hard boundary between educational or evaluation infrastructure and medical treatment decision systems.

5. The European Commission AI Act Service Desk page for Article 57 says AI regulatory sandboxes provide a controlled environment for developing and testing innovative AI systems before market release, with legal certainty, innovation support, regulatory compliance, guidance, and supervision.

Source: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-57

Readiness meaning: sandbox readiness should be framed as a supervised evidence and documentation route, not as permission to deploy.

## Crosswalk

1. Intended use

Public artifact question: Is the artifact limited to evaluation, assurance, education, or claim hygiene.

Evidence to prepare: scope paragraph, blocked use paragraph, user role list.

Blocked claim: clinical deployment.

2. AI literacy

Public artifact question: Are clinician and builder roles explained before model output use.

Evidence to prepare: literacy module, role checklist, review worksheet.

Blocked claim: autonomous clinical use.

3. Risk management

Public artifact question: Are failure modes, harms, and escalation paths listed before scores.

Evidence to prepare: failure atlas rows, escalation table, release gate.

Blocked claim: safety certification.

4. Data quality

Public artifact question: Are source, label, representativeness, leakage, and missingness checks visible.

Evidence to prepare: data quality card, label audit row, dataset boundary note.

Blocked claim: patient data clearance.

5. Documentation

Public artifact question: Is every public claim tied to source support and audit state.

Evidence to prepare: SourceCheckup output, manual source support, audit note.

Blocked claim: verified compliance.

6. Transparency

Public artifact question: Can an external reviewer see what is and is not claimed.

Evidence to prepare: README link, issue body, release note, boundary section.

Blocked claim: endorsement.

7. Human oversight

Public artifact question: Is clinician review treated as a gate rather than decoration.

Evidence to prepare: clinician review protocol, reviewer role table.

Blocked claim: clinical validation.

8. Robustness

Public artifact question: Are failure cases, uncertainty, and abstention language present.

Evidence to prepare: synthetic risk pack, warning sign checklist.

Blocked claim: performance guarantee.

9. Data and operational boundary

Public artifact question: Are secrets, private data, and operational systems excluded.

Evidence to prepare: no secrets statement, no private operational data statement.

Blocked claim: production readiness.

10. Monitoring

Public artifact question: Is post release public review possible without patient data.

Evidence to prepare: public issue template, contributor guide, triage board.

Blocked claim: real world monitoring claim.

11. Incident handling

Public artifact question: Is there a route for unsafe claims, broken sources, or misuse reports.

Evidence to prepare: public issue label, maintainer handoff, correction log.

Blocked claim: clinical incident management.

12. Sandbox route

Public artifact question: Is any sandbox language below access, application, and approval.

Evidence to prepare: route gate, source checked eligibility memo.

Blocked claim: sandbox access.

## Türkiye health AI safety use

1. Use this crosswalk as a public readiness companion for Turkish medical AI evaluation and clinician AI literacy work.
2. Pair it with the Türkiye Health AI Safety Handoff Index when a route owner asks what to inspect first.
3. Pair it with SourceCheckup Medical when source support and public claim hygiene are the immediate question.
4. Pair it with clinician review protocol when human oversight is the immediate question.
5. Pair it with health data quality and label audit work when data fitness is the immediate question.
6. Do not use it as legal advice, compliance proof, ethics approval, regulatory access, clinical validation, or clinical deployment evidence.

## Immediate public action queue

1. Convert each crosswalk row into a one page reviewer worksheet.
2. Add benchmark compatibility notes for MedHELM, HealthBench, and BRIDGE using this same no ranking evidence structure.
3. Add a TÜSEB A4 UM eligibility proof checklist that separates public readiness work from formal application authority.
4. Add a TEKNOFEST team facing safety reminder before 29 June 2026 if a public report checklist is still useful.

## Runnable check

```bash
make eu_ai_act_health_ai_sandbox_readiness_crosswalk
```
