# Health AI Assurance Feedback Intake

Date: 2026 07 08

Status: public feedback intake ready.

Roadmap phase: P9 external feedback intake.

Public anchor: https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/231

## Purpose

This intake gives outside reviewers one safe way to comment on the Health AI Assurance Kit without turning feedback into clinical validation, model ranking, endpoint claims, institution claims, or source truth certification.

Use this file when you want to review the Start Here proof pack, roadmap, kit card, SourceCheckup surface, Turkish drift preview, clinician literacy demo, monitoring digest, adapter smoke note, or local leaderboard preview.

## Boundary

Use synthetic or public information only. Do not include patient data, private clinical text, raw clinical notes, private model outputs, deployment results, clinical advice, clinical validation claims, model ranking claims, source truth certification claims, regulatory compliance claims, official compatibility claims, institution support claims, partnership claims, payment claims, or terms acceptance claims.

## Route Selector

| Route | Use when | File |
| --- | --- | --- |
| `kit_feedback` | You reviewed a Health AI Assurance Kit artifact and want to flag wording, missing context, usability, or boundary risk. | `.github/ISSUE_TEMPLATE/health_ai_assurance_feedback.yml` |
| `source_support_review` | You found a source locator, guideline phrase, policy phrase, DOI, PMID, or URL that needs exact claim support review. | `.github/ISSUE_TEMPLATE/sourcecheckup_review.yml` |
| `synthetic_failure_case` | You want to propose a synthetic medical AI failure case without patient data or raw private output. | `.github/ISSUE_TEMPLATE/synthetic_failure_case.yml` |
| `evidence_concern` | You want to report a reproducible concern about model behavior, documentation, release quality, or evaluation design. | `.github/ISSUE_TEMPLATE/evidence_concern.yml` |

## Small Tasks

| Task id | Reviewer action | Accepted output |
| --- | --- | --- |
| `P9T001` | Read the Start Here proof pack and identify one confusing boundary sentence. | GitHub issue using `kit_feedback`. |
| `P9T002` | Read SourceCheckup Medical wording and identify one claim that needs source support review. | GitHub issue using `source_support_review`. |
| `P9T003` | Read Turkish drift preview and identify one sentence that could overstate language coverage. | GitHub issue using `kit_feedback`. |
| `P9T004` | Read clinician literacy demo and identify one place that could sound like medical advice. | GitHub issue using `kit_feedback`. |
| `P9T005` | Propose one synthetic failure case that fits the existing boundaries. | GitHub issue using `synthetic_failure_case`. |

## Maintainer Triage States

| State | Meaning |
| --- | --- |
| `needs_route` | The issue should move to SourceCheckup, synthetic failure case, evidence concern, or kit feedback. |
| `needs_rewrite` | The issue has useful intent but includes unsafe wording, private data risk, or overclaiming. |
| `accepted_for_docs` | The issue can become a documentation fix after maintainer review. |
| `accepted_for_queue` | The issue can enter a source review queue or synthetic intake queue after maintainer review. |
| `closed_boundary` | The issue asks for patient data use, clinical advice, deployment claims, validation claims, ranking, endorsement, official compatibility, or institution support. |

## Do Not Ask For

1. Patient data.
2. Real clinical notes.
3. Private model output.
4. Provider API runs.
5. New case addition without maintainer review.
6. Physician selection by the agent.
7. Clinical validation.
8. Model ranking.
9. Source truth certification.
10. Regulatory compliance.
11. Official compatibility.
12. Institution support.

## Maintainer Use

1. Keep issue #231 open as the public proof route anchor.
2. Route incoming comments through one of the four templates above.
3. Close or rewrite comments that make blocked claims.
4. Move accepted feedback into a separate PR only after review.

## Related Artifacts

| Artifact | Path |
| --- | --- |
| Start Here proof pack | `docs/HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md` |
| Health AI Assurance Kit roadmap | `docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md` |
| Kit level assurance card | `docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md` |
| Project growth buildout index | `docs/PROJECT_GROWTH_BUILDOUT_INDEX_20260708.md` |
| SourceCheckup Medical product packet | `docs/SOURCECHECKUP_MEDICAL_PRODUCT_PACKET_20260708.md` |
| Turkish drift preview dashboard | `docs/TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md` |
