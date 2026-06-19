# Public Safe Failure Cards

Date: 2026 06 19

Status: public synthetic card pack for reviewer attack.

This pack turns repeated medical AI safety traps into small public cards that a clinician, health informatics reviewer, open model maintainer, hospital quality reviewer, or source support reviewer can challenge in one sitting.

The goal is simple: make weak safety language easy to attack before it becomes trusted public wording.

Boundary: no patient data, no clinical advice, no clinical validation, no clinical deployment, no benchmark ranking, no score certification, no source truth certification, no partner claim, no institution claim, no endorsement claim, no formal application, no payment, and no terms acceptance.

Live BAGLAM2, portfolio trackers, active Gmail outreach threads, and targeted Gmail searches were checked before this pack was built. No new substantive medical AI reply required action before the public artifact was prepared. An older T CAIREM reply closed that direct meeting route and pointed only to public follow channels.

## How to use the cards

1. Pick one card.
2. Attack the unsafe pattern.
3. Add one missing gate, safer rewrite, source support requirement, Turkish wording concern, or field readiness concern.
4. Keep all examples synthetic.
5. Do not add patient text, diagnosis advice, treatment advice, institutional statements, partner statements, or clinical deployment claims.

## Card schema

Each card has these fields:

1. Card id.
2. Platform lane.
3. Unsafe pattern.
4. Why it matters.
5. Reviewer check.
6. Safe rewrite.
7. Stop condition.
8. Contributor prompt.

## Cards

### SFC001: Benchmark score becomes safety proof

Platform lane: Medical AI Failure Atlas Global.

Unsafe pattern: A benchmark score is described as if it proves clinical safety.

Why it matters: A score can hide missing source support, weak data fitness, missing clinician review, and poor local workflow fit.

Reviewer check: Ask what evidence would be needed before any public wording uses safety language.

Safe rewrite: This result is an evaluation signal only. It does not establish clinical safety, deployment readiness, procurement fitness, or patient care suitability.

Stop condition: Any claim that a score alone proves safety must be blocked.

Contributor prompt: Name one safety claim that should be replaced with an evaluation signal statement.

### SFC002: Source link becomes source support

Platform lane: SourceCheckup Medical.

Unsafe pattern: A visible link is treated as adequate support for a medical claim.

Why it matters: A link can point to a broad page, irrelevant page, outdated page, paywalled abstract, or policy surface that does not support the exact claim.

Reviewer check: Ask whether the source supports the exact medical wording, population, care setting, date, and action boundary.

Safe rewrite: Source located, but exact claim support remains unverified.

Stop condition: Any source link that does not support the exact claim must remain in review.

Contributor prompt: Provide one synthetic claim where a link is present but the support is still not enough.

### SFC003: Turkish wording sounds fluent but shifts risk

Platform lane: TR MedLLM SafetyBench.

Unsafe pattern: Turkish medical wording is fluent but changes urgency, certainty, patient instruction, or clinician responsibility.

Why it matters: Fluent wording can still alter triage risk, medication risk, consent language, or follow up urgency.

Reviewer check: Ask what Turkish phrase changes the safety boundary and what clinician role should review it.

Safe rewrite: Turkish wording requires clinical language review before any safety or readiness claim.

Stop condition: Any term that can change clinical meaning across context must remain blocked until reviewed.

Contributor prompt: Name one Turkish clinical term that needs a safety wording gate.

### SFC004: Demo success becomes hospital readiness

Platform lane: Turkish Clinical AI Assurance Lab.

Unsafe pattern: A clean public demo is described as readiness for hospital workflow use.

Why it matters: Demos do not cover governance, audit trail, model update control, human review, downtime handling, data policy, and accountability.

Reviewer check: Ask which readiness gate is missing before hospital quality language is used.

Safe rewrite: This is a public demo surface only. Hospital readiness has not been assessed.

Stop condition: Any hospital readiness claim must be blocked without a documented readiness gate.

Contributor prompt: Add one hospital readiness gate that a demo cannot satisfy by itself.

### SFC005: Synthetic card becomes real case evidence

Platform lane: Medical AI Failure Atlas Global.

Unsafe pattern: A synthetic failure example is cited as if it proves real world harm frequency.

Why it matters: Synthetic cards can reveal a plausible failure path, but they do not measure incidence, prevalence, model performance, or clinical impact.

Reviewer check: Ask whether the card is being used as a pattern seed or as evidence of real world frequency.

Safe rewrite: This is a synthetic pattern seed for review. It is not evidence of incidence or clinical outcome.

Stop condition: Any frequency or outcome claim from a synthetic card must be blocked.

Contributor prompt: Rewrite one synthetic example so it cannot be mistaken for real case evidence.

### SFC006: Policy wording becomes clinical instruction

Platform lane: Clinician AI Literacy Academy Turkiye.

Unsafe pattern: A policy or guideline phrase is converted into a direct patient instruction without clinical context.

Why it matters: Policy language can depend on setting, patient group, contraindications, local practice, and clinician judgment.

Reviewer check: Ask whether the wording gives an action instruction that should remain under clinician review.

Safe rewrite: This policy reference needs clinician interpretation before any patient facing instruction is written.

Stop condition: Any patient instruction derived from broad policy wording must be blocked.

Contributor prompt: Give one synthetic policy overclaim and a safer clinician review rewrite.

### SFC007: Public dataset means data fitness

Platform lane: Health Data Quality and Label Audit Commons.

Unsafe pattern: A public dataset is treated as fit for medical AI safety work because it is accessible.

Why it matters: Access does not prove label quality, provenance clarity, population fit, leakage control, consent boundary, or task suitability.

Reviewer check: Ask what data fitness evidence is missing.

Safe rewrite: Dataset access is not data fitness. Label quality and task suitability remain unreviewed.

Stop condition: Any data fitness claim must be blocked without label and provenance review.

Contributor prompt: Name one label quality failure that should block public readiness wording.

### SFC008: Human review role is missing

Platform lane: Turkish Clinical AI Assurance Lab.

Unsafe pattern: A workflow says human in the loop but does not define who reviews what, when, and with what authority.

Why it matters: Undefined review can become ceremonial and may not catch source gaps, unsafe wording, data limits, or escalation needs.

Reviewer check: Ask what reviewer role, trigger, authority, and record are missing.

Safe rewrite: Human review is not defined until role, trigger, authority, and record are explicit.

Stop condition: Any human review claim must be blocked if role and authority are undefined.

Contributor prompt: Add one missing reviewer role and the trigger that should activate it.

### SFC009: Vendor language becomes medical assurance

Platform lane: SourceCheckup Medical.

Unsafe pattern: A vendor or model maintainer statement is copied into medical safety language.

Why it matters: General model capability language does not prove medical source support, clinical appropriateness, data fitness, local workflow safety, or patient care suitability.

Reviewer check: Ask which part of the vendor language is being converted into a medical assurance claim.

Safe rewrite: Vendor language is background context only. Medical assurance requires independent review gates.

Stop condition: Any copied capability claim must be blocked if it becomes a medical safety claim.

Contributor prompt: Provide one synthetic vendor phrase that needs a medical assurance rewrite.

### SFC010: Sandbox route becomes deployment readiness

Platform lane: Turkish Clinical AI Assurance Lab.

Unsafe pattern: A sandbox, route question, or proposal preparation note is described as deployment readiness.

Why it matters: A sandbox or route inquiry can help learning and review, but it does not authorize clinical use, institutional adoption, procurement, or patient facing deployment.

Reviewer check: Ask whether the wording separates route exploration from clinical readiness.

Safe rewrite: This is route exploration only. It does not imply clinical deployment, institutional adoption, procurement readiness, or patient facing use.

Stop condition: Any deployment readiness wording must be blocked unless the required formal process is complete and explicitly verified.

Contributor prompt: Rewrite one route exploration statement so it cannot imply deployment readiness.

## Public review ask

Attack one card in public with this shape:

Role:

Lane:

Card id:

Risk:

Missing gate:

Safer wording:

GitHub issue template: .github/ISSUE_TEMPLATE/safe_failure_card_objection.yml

## Done condition

The pack is useful only if it produces concrete objections, missing gates, and safer rewrites. It is not a ranking tool, not a benchmark result, and not a clinical validation artifact.

Runnable check:

```bash
make public_safe_failure_cards
```
