# Health AI Assurance Feedback Triage Board

Date: 2026 07 08

Status: public feedback triage board ready.

Roadmap phase: P10 feedback triage board.

Public anchor: https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231

## Purpose

This board gives maintainers a public way to classify Health AI Assurance Kit feedback after intake. It turns each issue into a narrow next action while preserving the project boundary: synthetic or public information only, no clinical advice, no clinical validation claim, no model ranking, no source truth certification, no regulatory compliance claim, no official compatibility claim, and no institution support claim.

## Inputs

| Route | Source |
| --- | --- |
| `kit_feedback` | `.github/ISSUE_TEMPLATE/health_ai_assurance_feedback.yml` |
| `source_support_review` | `.github/ISSUE_TEMPLATE/sourcecheckup_review.yml` |
| `synthetic_failure_case` | `.github/ISSUE_TEMPLATE/synthetic_failure_case.yml` |
| `evidence_concern` | `.github/ISSUE_TEMPLATE/evidence_concern.yml` |

## Triage States

| State | Maintainer meaning |
| --- | --- |
| `needs_route` | The issue belongs in a different public route before review can continue. |
| `needs_rewrite` | The issue has useful intent but includes wording that can overstate safety, validation, ranking, source truth, or clinical use. |
| `accepted_for_docs` | The issue can become a documentation fix after maintainer review. |
| `accepted_for_queue` | The issue can enter a source review queue, evidence queue, or synthetic intake queue after maintainer review. |
| `closed_boundary` | The issue asks for blocked material or blocked claims. |
| `needs_owner_review` | The issue affects project positioning and needs owner review before a public change. |

## Board Rows

| Row id | Route | Reviewer concern | Triage state | Next action | Allowed output |
| --- | --- | --- | --- | --- | --- |
| `P10R001` | `unknown_or_mixed` | The issue mixes kit wording, source support, synthetic case input, or evidence concern. | `needs_route` | Ask the reviewer to reopen through one selected template. | Routed GitHub issue. |
| `P10R002` | `kit_feedback` | A Health AI Assurance Kit sentence is confusing or too broad. | `accepted_for_docs` | Open a small documentation PR with the exact sentence and safer replacement. | Documentation fix. |
| `P10R003` | `source_support_review` or `synthetic_failure_case` | A source support question or synthetic failure case proposal fits the public boundary. | `accepted_for_queue` | Move the item into the matching queue after maintainer review. | Queue entry or reviewed PR. |
| `P10R004` | `kit_feedback` | The wording can sound like clinical advice, clinical validation, model ranking, or source truth certification. | `needs_rewrite` | Request a narrower wording before accepting the issue. | Rewritten issue text. |
| `P10R005` | any route | The issue includes patient data, private clinical text, raw clinical notes, or private model output. | `closed_boundary` | Close the issue and ask for synthetic or public information only. | Boundary closure note. |
| `P10R006` | any route | The issue asks for provider API runs, new cases without review, agent selected physicians, regulatory compliance, official compatibility, institution support, partnership, payment, or terms acceptance claims. | `closed_boundary` or `needs_owner_review` | Close blocked requests. Send positioning questions to owner review. | Boundary closure note or owner review note. |

## Review Columns

Use these fields when maintainers copy a row into a project board or release note:

| Column | Value format |
| --- | --- |
| Route | One selected intake route. |
| Intake id | GitHub issue number or pull request number. |
| Reviewer concern | One sentence that names the concern. |
| Public artifact | File path or issue URL. |
| Blocked claim risk | yes or no. |
| Maintainer state | One triage state from this board. |
| Next action | One maintainer action. |
| Allowed output | Documentation fix, queue entry, rewritten issue text, boundary closure note, or owner review note. |

## Boundary Lock

Maintainers must not convert feedback into patient data use, private clinical text use, raw clinical note use, private model output use, provider API runs, new case addition without review, physician selection by the agent, clinical validation claims, model ranking claims, source truth certification claims, regulatory compliance claims, official compatibility claims, institution support claims, partnership claims, payment claims, or terms acceptance claims.

## Related Artifacts

| Artifact | Path |
| --- | --- |
| Feedback intake | `docs/HEALTH_AI_ASSURANCE_FEEDBACK_INTAKE_20260708.md` |
| Feedback intake manifest | `docs/health_ai_assurance_feedback_intake_20260708.json` |
| Start Here proof pack | `docs/HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md` |
| Health AI Assurance Kit roadmap | `docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md` |
| Kit level assurance card | `docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md` |
| Project growth buildout index | `docs/PROJECT_GROWTH_BUILDOUT_INDEX_20260708.md` |
