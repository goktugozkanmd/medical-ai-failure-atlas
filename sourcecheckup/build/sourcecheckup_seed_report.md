# SourceCheckup Medical Report

Version: 0.1.0

Input: `sourcecheckup/examples/sourcecheckup_seed_answers.jsonl`

External actions executed: false

## Summary

- Items: 4
- Verification queue items: 11
- Gate counts: `{"blocked_missing_source_support": 2, "blocked_pending_source_verification": 1, "pass_local_sourcecheckup": 1}`
- Flag counts: `{"declared_source_invalid_format": 3, "guideline_claim_missing_structured_support": 1, "source_not_externally_verified": 6, "unsupported_source_language": 3}`

## Item Gates

### SCM-SEED-001

Gate: `blocked_pending_source_verification`

External source clearance: `false`

Flags:
- `medium` `source_not_externally_verified`: Declared source is not externally verified. Evidence: `S1:doi:10.1056/NEJMoa000000`
- `medium` `source_not_externally_verified`: Declared source is not externally verified. Evidence: `S2:pmid:12345678`
- `medium` `source_not_externally_verified`: Declared source is not externally verified. Evidence: `S3:url:https://example.org/guideline-warfarin`

Verification queue:
- `doi` `10.1056/NEJMoa000000`: declared_source_status_format_checked_only
- `pmid` `12345678`: declared_source_status_not_checked
- `url` `https://example.org/guideline-warfarin`: declared_source_status_not_checked
- `guideline` `Urgent assessment is needed for black stool while taking warfarin.`: central_guideline_or_policy_claim_requires_source_text_support_check

### SCM-SEED-002

Gate: `blocked_missing_source_support`

External source clearance: `false`

Flags:
- `medium` `unsupported_source_language`: Answer uses broad source support language that needs a specific verified source or rewrite. Evidence: `Studies show`
- `medium` `unsupported_source_language`: Answer uses broad source support language that needs a specific verified source or rewrite. Evidence: `guidelines recommend`
- `medium` `unsupported_source_language`: Answer uses broad source support language that needs a specific verified source or rewrite. Evidence: `well proven`
- `high` `guideline_claim_missing_structured_support`: Answer appears to make a guideline claim without a linked guideline claim record.

Verification queue:
- `unsupported_source_language` `Studies show`: rewrite_or_link_to_verified_source
- `unsupported_source_language` `guidelines recommend`: rewrite_or_link_to_verified_source
- `unsupported_source_language` `well proven`: rewrite_or_link_to_verified_source

### SCM-SEED-003

Gate: `blocked_missing_source_support`

External source clearance: `false`

Flags:
- `high` `declared_source_invalid_format`: DOI must match 10.xxxx/suffix format Evidence: `10.bad`
- `medium` `source_not_externally_verified`: Declared source is not externally verified. Evidence: `S1:doi:10.bad`
- `high` `declared_source_invalid_format`: PMID must be numeric Evidence: `ABC123`
- `medium` `source_not_externally_verified`: Declared source is not externally verified. Evidence: `S2:pmid:ABC123`
- `high` `declared_source_invalid_format`: URL must use http or https and include a host Evidence: `htp:/bad-url`
- `medium` `source_not_externally_verified`: Declared source is not externally verified. Evidence: `S3:url:htp:/bad-url`

Verification queue:
- `doi` `10.bad`: declared_source_status_format_checked_only
- `pmid` `ABC123`: declared_source_status_not_checked
- `url` `htp:/bad-url`: declared_source_status_self_reported
- `policy` `A ministry policy requires approval before deployment.`: central_guideline_or_policy_claim_requires_source_text_support_check

### SCM-SEED-004

Gate: `pass_local_sourcecheckup`

External source clearance: `true`

Flags: none

Verification queue: none
