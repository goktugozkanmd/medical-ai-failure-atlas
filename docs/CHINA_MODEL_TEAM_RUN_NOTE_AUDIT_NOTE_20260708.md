# China Model Team Run Note Audit Note

Date: 2026 07 08

Status: internal audit note before Hunyuan, InternLM, and MiniMax outreach.

## Files checked

1. `docs/CHINA_MODEL_TEAM_RUN_NOTE_WAVE_20260708.md`
2. `docs/CHINA_MODEL_TEAM_RUN_NOTE_SOURCE_VERIFICATION_20260708.md`

## Required checks before sending

1. Run deterministic submission audit on both files.
2. Run reference extraction on the source verification note.
3. Manually verify that the messages do not claim collaboration, acceptance, endorsement, clinical validation, deployment, ranking, official compatibility, or patient data use.
4. Confirm that each message asks for one bounded action only.

## Deterministic audit result

Command:

```bash
python3 ~/.agents/skills/academic_submission_audit/scripts/audit_submission.py docs/CHINA_MODEL_TEAM_RUN_NOTE_WAVE_20260708.md docs/CHINA_MODEL_TEAM_RUN_NOTE_SOURCE_VERIFICATION_20260708.md docs/CHINA_MODEL_TEAM_RUN_NOTE_AUDIT_NOTE_20260708.md
```

Result: overall ok.

Forbidden process labels: none found.

Hyphen status:

1. Message wave: hyphens only in official URLs.
2. Source verification: hyphens only in official URLs.
3. Audit note: zero hyphens.

## Reference extraction result

Command:

```bash
python3 ~/.agents/skills/academic_reference_verification/scripts/verify_references.py docs/CHINA_MODEL_TEAM_RUN_NOTE_SOURCE_VERIFICATION_20260708.md
```

Result:

1. No formal reference list items were found.
2. Manual source verification is recorded in `docs/CHINA_MODEL_TEAM_RUN_NOTE_SOURCE_VERIFICATION_20260708.md`.
3. Claim support was checked manually for route facts only.

## Manual claim review

Cleared message principles:

1. Synthetic cases only.
2. No patient data.
3. No clinical advice.
4. No clinical validation claim.
5. No deployment claim.
6. No model ranking claim.
7. No official compatibility claim.
8. No endorsement, membership, submission, invitation, or partnership claim.

## Current send plan

Allowed routes after audit:

1. Public GitHub issue to the Hunyuan A13B repository.
2. Public GitHub issue to `InternLM/InternLM`.
3. Public GitHub issue to the MiniMax M1 repository.
4. Email to `hunyuan_opensource@tencent.com`.
5. Email to `internlm@pjlab.org.cn`.
6. Email to `model@minimax.io`.

Optional MiniMax fallback after a bounce:

1. Email to `model@minimaxi.com`.

## Open lock

No CHAI, OHDSI, AMIA, or other governance community message is cleared by this audit.

## Send result

Send outcome is recorded in `docs/CHINA_MODEL_TEAM_RUN_NOTE_SEND_LOG_20260708.md`.
