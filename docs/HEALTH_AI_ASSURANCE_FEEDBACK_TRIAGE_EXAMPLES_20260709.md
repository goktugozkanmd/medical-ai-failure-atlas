# Health AI Assurance Feedback Triage Examples

Date: 2026 07 09

Status: public feedback triage examples ready.

Roadmap phase: P11 feedback triage examples.

Public anchor: https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231

## Purpose

These examples show how maintainers can turn public Health AI Assurance Kit feedback into narrow decision records after intake and triage. They are synthetic issue examples for maintainer routing. They are not patient data, not private clinical text, not raw model output, not clinical advice, not a clinical validation claim, not a model ranking claim, not source truth certification, not a regulatory compliance claim, not an official compatibility claim, and not institution support.

## Source chain

1. Feedback intake: `docs/HEALTH_AI_ASSURANCE_FEEDBACK_INTAKE_20260708.md`.
2. Feedback intake manifest: `docs/health_ai_assurance_feedback_intake_20260708.json`.
3. Feedback triage board: `docs/HEALTH_AI_ASSURANCE_FEEDBACK_TRIAGE_BOARD_20260708.md`.
4. Feedback triage board manifest: `docs/health_ai_assurance_feedback_triage_board_20260708.json`.
5. Public proof route anchor: issue `#231`.

## Decision examples

| Example id | Incoming route | Example feedback | Triage state | Decision | Maintainer action | Allowed output |
| --- | --- | --- | --- | --- | --- | --- |
| `P11E001` | `kit_feedback` | Reviewer says the Start Here packet is useful but one boundary sentence is too broad. | `accepted_for_docs` | Documentation fix. | Open a small PR with the exact sentence, safer replacement, and changed file path. | `documentation_fix` |
| `P11E002` | `source_support_review` | Reviewer flags a DOI, PMID, guideline phrase, or URL that may not support the claim sentence. | `accepted_for_queue` | Source review queue. | Add the claim sentence, locator, support state, and uncertainty state to a reviewed source queue. | `source_review_queue_entry` |
| `P11E003` | `synthetic_failure_case` | Reviewer proposes a synthetic failure case without patient data or private model output. | `accepted_for_queue` | Synthetic case queue. | Move the proposal into synthetic intake only after maintainer review and boundary check. | `synthetic_case_queue_entry` |
| `P11E004` | `kit_feedback` | Reviewer wording says the kit proves clinical safety, validates a model, ranks models, or certifies sources. | `needs_rewrite` | Rewrite before acceptance. | Ask for narrower wording that names the documentation concern without validation, ranking, or certification language. | `rewritten_issue_text` |
| `P11E005` | any route | Reviewer includes patient data, private clinical text, raw clinical notes, or private model output. | `closed_boundary` | Boundary close. | Close the issue and request synthetic or public information only. | `boundary_closure_note` |
| `P11E006` | any route | Reviewer asks for provider API runs, physician selection by the agent, regulatory clearance, official compatibility, institution support, partnership, payment, or terms acceptance. | `needs_owner_review` | Owner review. | Close blocked requests and send any positioning question to owner review before public wording changes. | `owner_review_note` |

## Maintainer reply shapes

### Documentation fix

Use when the feedback is narrow and public.

Reply shape: Thanks. This is accepted as a documentation wording fix. We will move the exact sentence and safer replacement into a small reviewed PR.

### Source review queue

Use when the feedback points to a source support gap.

Reply shape: Thanks. This belongs in the source support queue. Please keep the claim sentence, source locator, and uncertainty state explicit. This does not certify source truth.

### Synthetic case queue

Use when the feedback proposes a synthetic case that fits the public boundary.

Reply shape: Thanks. This can enter synthetic intake after maintainer review. Please keep it synthetic and avoid patient data, private model output, and answer keys.

### Rewrite before acceptance

Use when the feedback has useful intent but unsafe claim wording.

Reply shape: Thanks. The concern may be useful, but the wording needs to be narrower before acceptance. Please remove clinical validation, ranking, source certification, deployment, or endorsement language.

### Boundary close

Use when the feedback includes blocked material.

Reply shape: Closing for boundary reasons. Please do not include patient data, private clinical text, raw clinical notes, or private model output. A synthetic or public version can be reopened through the right template.

### Owner review

Use when the feedback affects project positioning or asks for blocked operational commitments.

Reply shape: This needs owner review before any public change. The project cannot claim provider runs, physician selection, regulatory clearance, official compatibility, institution support, partnership, payment, or terms acceptance from this issue.

## Boundary lock

Maintainers must keep all examples synthetic or public. Do not convert any feedback into patient data use, private clinical text use, raw clinical note use, private model output use, provider API runs, new case addition without review, physician selection by the agent, clinical validation claims, model ranking claims, source truth certification claims, regulatory compliance claims, official compatibility claims, institution support claims, partnership claims, payment claims, terms acceptance claims, or endorsement claims.

## Public use

1. Use these rows as example decision records, not as real reviewer decisions.
2. Choose one incoming route and one triage state for each issue.
3. Preserve the exact issue link and artifact path before opening a PR.
4. Keep documentation fixes, source queue entries, synthetic case queue entries, rewrites, boundary closures, and owner review notes separate.
5. Run `python scripts/validate_health_ai_assurance_feedback_triage_examples_20260709.py` before release.
