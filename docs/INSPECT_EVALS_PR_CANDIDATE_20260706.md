# Inspect Evals Upstream PR Candidate — 2026-07-06

**Status:** local-only candidate; no upstream PR opened without G approval
**Upstream:** `UKGovernmentBEIS/inspect_evals`
**Local clone:** `~/Documents/Codex/upstream-inspect/inspect_evals`
**Local branch:** `goktug/docs-typo-cleanup`
**Local commit:** `dae1538`

## Live upstream check

- Repository reachable: `https://github.com/UKGovernmentBEIS/inspect_evals`
- Viewer permission: read-only.
- Search found no open PR by `goktugozkanmd` or `drozkan2` against `UKGovernmentBEIS/inspect_evals`.
- No external issue, comment, PR, or push was made.

## Candidate change

Small documentation/metadata typo cleanup:

1. `pyproject.toml`
   - `fallabck` → `fallback`
2. `BEST_PRACTICES.md`
   - `seperate an inlined computation` → `separate an inlined computation`

## Local verification

Ran in the upstream clone:

```bash
python3 - <<'PY'
from pathlib import Path
assert 'fallabck' not in Path('pyproject.toml').read_text()
assert 'seperate an inlined' not in Path('BEST_PRACTICES.md').read_text()
print('typo checks pass')
PY
git diff --check
```

Result:

```text
typo checks pass
```

`git diff --check` produced no whitespace errors.

## PR body draft

```markdown
# This PR contains

## Description

Fixes two small typos in documentation/config comments:

- `fallabck` → `fallback` in `pyproject.toml`
- `seperate` → `separate` in `BEST_PRACTICES.md`

No eval behavior, runtime code, task metadata, assets, or contributor workflow semantics are changed.

## Checklist

- [x] Does this change affect existing eval(s)? No.
- [x] Is this change consequential to users? No.
- [x] Does this change affect how future contributors write or submit evaluations? No.
```

## Next action

If G approves public upstream action, push the local branch to G's fork and open a **draft** PR using the upstream template. Do not open it without approval.
