# China Turkey Collaboration Audit Note

Date: 2026 07 08

Status: internal audit note. G gave explicit send approval after this audit. Send outcome is recorded in `docs/CHINA_TURKEY_COLLAB_SEND_LOG_20260708.md`.

## Files checked

1. `docs/CHINA_TURKEY_CLINICAL_AI_SAFETY_COLLAB_CAMPAIGN_20260708.md`
2. `docs/CHINA_TURKEY_COLLAB_ONE_WAVE_MESSAGES_20260708.md`
3. `docs/CHINA_TURKEY_COLLAB_SOURCE_VERIFICATION_20260708.md`
4. `docs/CHINA_TURKEY_COLLAB_SEND_QUEUE_20260708.md`

## Deterministic audit

Command:

```bash
python3 ~/.agents/skills/academic_submission_audit/scripts/audit_submission.py \
  docs/CHINA_TURKEY_COLLAB_ONE_WAVE_MESSAGES_20260708.md \
  docs/CHINA_TURKEY_COLLAB_SOURCE_VERIFICATION_20260708.md
```

Result: overall ok.

Forbidden process labels: none found.

Hyphen status:

1. Exact one wave message batch has no disallowed hyphen characters.
2. Source verification note has only official URL hyphens.
3. Campaign packet has Markdown table separator hyphens and official URL hyphens. It is internal and not the exact outgoing message batch.

## Reference verification

Command class:

```bash
python3 ~/.agents/skills/academic_reference_verification/scripts/verify_references.py [file]
```

Result:

1. Exact one wave message batch: no formal references found.
2. Source verification note: no formal references found.
3. Send queue: no formal references found.
4. Claim support is manual, recorded in `docs/CHINA_TURKEY_COLLAB_SOURCE_VERIFICATION_20260708.md`.

## Manual claim review

Cleared for draft use:

1. No patient data claim is visible in every outgoing message.
2. No clinical advice claim is made.
3. No deployment claim is made.
4. No partnership, endorsement, or affiliation is claimed before response.
5. The ask is collaboration, joint pilot, shared benchmark, model evaluation report, and possible coauthored paper.

Still required before sending:

1. Freeze the exact channel for each target.
2. Recheck project contribution rules before GitHub issues or comments.
3. Verify direct personal contact routes for named people if used.
4. Get explicit G approval for send.
5. Log target, channel, date, and outcome in BAGLAM2 after send.

## Send clearance

Cleared after explicit G approval.

Send log: `docs/CHINA_TURKEY_COLLAB_SEND_LOG_20260708.md`.
