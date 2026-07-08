# Local Leaderboard Draft Preview

Date: 2026 07 08

Status: local draft preview only. The public leaderboard file was not changed.

## Boundary

No external send, no provider API call, no public leaderboard write, no new case addition, no patient data, no physician selection, no clinical validation claim, no official compatibility claim, and no model ranking.

## Scope

- Models in preview: 2.
- Public rows closed by existing local artifacts: 27.
- Provider generation rows used: 0.
- Source leaderboard SHA256: `6848859365e29736c00f808bf0ee3fd998686c5f983772600250a6cae1a801a8`.

## Draft Rows

| Model | Current public rows | Draft rows | Local rows closing gap | Draft safety | Draft source support | Draft clinical boundary | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| DeepSeek V4 Pro | 5 | 30 | 25 | 74.0 | 82.7 | 81.0 | local_preview_only_not_written_to_public_leaderboard |
| GLM-5.2 | 28 | 30 | 2 | 72.0 | 82.7 | 87.0 | local_preview_only_not_written_to_public_leaderboard |

## Next

1. Review score derivation and row wording.
2. If the user later approves, create a separate public leaderboard update patch.
3. Keep remaining provider generation rows blocked until explicit approval.

## Validation

Run:

```bash
make local_leaderboard_draft_preview_20260708
```
