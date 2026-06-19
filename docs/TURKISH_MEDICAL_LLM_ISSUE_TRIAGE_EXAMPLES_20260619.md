# Turkish Medical LLM Issue Triage Examples

Date: 2026 06 19

Status: public triage examples for Turkish medical LLM issue routing.

Purpose: turn the reviewer issue template into concrete example rows that maintainers can use before a Turkish medical LLM related issue is accepted for public review.

This package is not a Turkish medical benchmark, not a benchmark result, not a leaderboard, not model ranking, not score certification, not source truth certification, not clinical validation, not clinical deployment, not patient data access, not regulated data access, not institutional approval, not partner status, not a formal application, not payment, not terms acceptance, and not endorsement.

## Start state

Live BAGLAM2 and portfolio trackers were read before build. Active Gmail outreach threads and targeted Gmail searches were checked before build. No new route owner reply was found. The prior Hacettepe acknowledgement remains the only reply and is not endorsement, validation, partnership, institutional support, official role, official course, hospital adoption, or clinical clearance.

## Linked public issue chain

1. Issue `#132`: Global Benchmark Pressure Response.
2. Issue `#133`: Failure Atlas Real Clinical Text Pressure Template.
3. Issue `#134`: SourceCheckup Medical Benchmark Source Support Worksheet.
4. Issue `#135`: Turkish Medical LLM Coverage Pressure Addendum.
5. Issue `#136`: Turkish Medical LLM Coverage Reviewer Intake Rows.
6. Issue `#137`: Turkish Medical LLM Reviewer Issue Template.

## Example 1

Example id: TMT001.

Issue title: Turkish language only claim needs medical coverage review.

Linked issues: `#132`, `#135`, and `#137`.

Issue intent: language review plus medical scope review.

Turkish language state: Turkish text is present, but this does not prove Turkish medical coverage.

Medical scope: unresolved.

Clinical context: maintainer and clinician reviewer.

Source support: no medical safety source supplied.

Turkish terminology risk: low until medical scope is claimed.

Clinician review question: is there any medical task in the row, or is it only a language claim?

Data boundary: public only or synthetic safety text only.

Ranking boundary: no ranking.

Public route fit: no official route claim.

Release decision: hold for medical scope rewrite.

Stop rule: stop if Turkish language presence is reused as medical readiness.

## Example 2

Example id: TMT002.

Issue title: Translated patient education snippet needs language and clinician review.

Linked issues: `#133`, `#135`, `#136`, and `#137`.

Issue intent: language review plus clinician review.

Turkish language state: translated Turkish.

Medical scope: patient education wording.

Clinical context: patient education review, not clinical advice release.

Source support: source sentence required before acceptance.

Turkish terminology risk: medium because tone, suffix, and local terminology may change medical meaning.

Clinician review question: could the wording cause delay in care or unsafe self management?

Data boundary: public only or synthetic safety text only.

Ranking boundary: no ranking.

Public route fit: no official route claim.

Release decision: route to language review and clinician review.

Stop rule: stop if the row uses patient data or copies benchmark items.

## Example 3

Example id: TMT003.

Issue title: Medication safety statement needs source support before public release.

Linked issues: `#132`, `#134`, `#136`, and `#137`.

Issue intent: source review plus clinician review.

Turkish language state: Turkish medical wording present.

Medical scope: medication safety.

Clinical context: clinician reviewer and source reviewer.

Source support: exact public source, claim sentence, support state, and uncertainty state required.

Turkish terminology risk: high if dose, frequency, contraindication, warning sign, or drug class wording appears.

Clinician review question: does the public source support the safety wording without overstating certainty?

Data boundary: public only or synthetic safety text only.

Ranking boundary: no ranking.

Public route fit: no official route claim.

Release decision: hold until source support is explicit.

Stop rule: stop if source existence is treated as source support.

## Example 4

Example id: TMT004.

Issue title: Turkish abbreviation ambiguity needs language and clinician routing.

Linked issues: `#135`, `#136`, and `#137`.

Issue intent: language review plus clinician review.

Turkish language state: Turkish abbreviation or local shorthand present.

Medical scope: unresolved until abbreviation meaning is fixed.

Clinical context: clinician reviewer and language reviewer.

Source support: source may be needed if abbreviation maps to a medical claim.

Turkish terminology risk: high because abbreviation ambiguity can change the medical task.

Clinician review question: which meaning is clinically intended, and what risk follows if readers choose the wrong meaning?

Data boundary: public only or synthetic safety text only.

Ranking boundary: no ranking.

Public route fit: no official route claim.

Release decision: route to language review before public acceptance.

Stop rule: stop if the meaning is unresolved.

## Example 5

Example id: TMT005.

Issue title: Benchmark adjacent claim needs no ranking boundary review.

Linked issues: `#132`, `#134`, and `#137`.

Issue intent: governance review plus source review.

Turkish language state: may be Turkish, translated Turkish, or only a claim about Turkish coverage.

Medical scope: benchmark adjacent summary.

Clinical context: maintainer and governance reviewer.

Source support: source URL, claim sentence, support state, and uncertainty state required.

Turkish terminology risk: depends on the claim sentence.

Clinician review question: is the claim about clinical usefulness, benchmark coverage, or only public documentation?

Data boundary: no benchmark item copying, no answer keys, no hidden prompts.

Ranking boundary: no ranking, no score, no leaderboard standing, no model standing.

Public route fit: no official route claim.

Release decision: rewrite if any ranking language appears.

Stop rule: stop if the issue asks for rank, score, model standing, or score certification.

## Example 6

Example id: TMT006.

Issue title: Public route fit question needs governance boundary review.

Linked issues: `#137`.

Issue intent: governance review.

Turkish language state: public route question may use Turkish or English.

Medical scope: non patient data medical AI safety preparation.

Clinical context: maintainer and governance reviewer.

Source support: written source needed for any official route, funding, institution, or programme claim.

Turkish terminology risk: low unless medical scope is added.

Clinician review question: no clinical claim should be reviewed until a clinical context exists.

Data boundary: no patient data and no regulated data.

Ranking boundary: no ranking.

Public route fit: unresolved unless written evidence exists.

Release decision: hold if any official route claim is unsupported.

Stop rule: stop if the issue implies official approval, partner status, application submission, payment, terms acceptance, or endorsement.

## Maintainer use

1. Use these examples as routing examples, not benchmark examples.
2. Accept a row only when issue intent, linked context, Turkish language state, medical scope, clinical context, source support, terminology risk, clinician review question, data boundary, ranking boundary, public route fit, and release decision are explicit.
3. Route unresolved language to language review.
4. Route unresolved medical judgment to clinician review.
5. Route unresolved sources to source review.
6. Route unresolved data boundary to data steward review.
7. Route unresolved public route or ranking boundary to governance review.
8. Stop if any blocked claim appears.

## Recommended check

```bash
make turkish_medical_llm_issue_triage_examples
```
