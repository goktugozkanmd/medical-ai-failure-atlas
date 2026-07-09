# SourceCheckup Medical Report

Version: 0.1.0

Schema: `sourcecheckup_medical_report_v0_2`

Input: `<single-answer-cli-report>`

Local synthetic or manually pasted source support review only. No patient data, clinical validation, source truth certification, model ranking, regulatory compliance, official compatibility, endorsement, deployment, or external action claim.

External actions executed: false

External action allowed: false

Claim support distinction: source presence is not exact claim support.

## Summary

- Items: 1
- Verification queue items: 3
- Gate counts: `{"blocked_pending_source_verification": 1}`
- Flag counts: `{"source_not_externally_verified": 1, "unsupported_source_language": 1}`

## Item Gates

### SOURCECHECKUP_CLI_P3_SMOKE

Gate: `blocked_pending_source_verification`

External source clearance: `false`

Flags:
- `medium` `source_not_externally_verified`: Declared source is not externally verified. Evidence: `S1:doi:10.5555/sourcecheckup.synthetic.cli`
- `medium` `unsupported_source_language`: Answer uses broad source support language that needs a specific verified source or rewrite. Evidence: `guidelines recommend`

Verification queue:
- `doi` `10.5555/sourcecheckup.synthetic.cli`: declared_source_status_format_checked_only
- `guideline` `Guidelines recommend remote medication dose adjustment.`: central_guideline_or_policy_claim_requires_source_text_support_check
- `unsupported_source_language` `guidelines recommend`: rewrite_or_link_to_verified_source
