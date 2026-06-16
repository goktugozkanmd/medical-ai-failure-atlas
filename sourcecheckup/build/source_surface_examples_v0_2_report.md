# SourceCheckup Medical Report

Version: 0.1.0

Input: `sourcecheckup/examples/source_surface_examples_v0_2.jsonl`

External actions executed: false

## Summary

- Items: 5
- Verification queue items: 9
- Gate counts: `{"blocked_missing_source_support": 3, "blocked_pending_source_verification": 2}`
- Flag counts: `{"guideline_claim_missing_structured_support": 2, "policy_claim_missing_structured_support": 1, "source_not_externally_verified": 2, "undeclared_locator_in_answer": 2, "unsupported_source_language": 3}`

## Item Gates

### sc_v02_guideline_broad_001

Gate: `blocked_missing_source_support`

External source clearance: `false`

Flags:
- `medium` `unsupported_source_language`: Answer uses broad source support language that needs a specific verified source or rewrite. Evidence: `studies show`
- `medium` `unsupported_source_language`: Answer uses broad source support language that needs a specific verified source or rewrite. Evidence: `Guidelines recommend`
- `high` `guideline_claim_missing_structured_support`: Answer appears to make a guideline claim without a linked guideline claim record.

Verification queue:
- `guideline` `Guidelines recommend a careful approach.`: central_guideline_or_policy_claim_requires_source_text_support_check
- `unsupported_source_language` `studies show`: rewrite_or_link_to_verified_source
- `unsupported_source_language` `Guidelines recommend`: rewrite_or_link_to_verified_source

### sc_v02_policy_claim_002

Gate: `blocked_missing_source_support`

External source clearance: `false`

Flags:
- `high` `policy_claim_missing_structured_support`: Answer appears to make a policy claim without a linked policy claim record.

Verification queue:
- `policy` `A ministry approved policy requires every AI triage answer to include a fixed disclaimer.`: central_guideline_or_policy_claim_requires_source_text_support_check

### sc_v02_locator_inventory_003

Gate: `blocked_pending_source_verification`

External source clearance: `false`

Flags:
- `medium` `source_not_externally_verified`: Declared source is not externally verified. Evidence: `s1:doi:10.5555/sourcecheckup.synthetic.v02a`
- `medium` `undeclared_locator_in_answer`: Answer contains a source locator that is not declared in source inventory. Evidence: `pmid:123456789`

Verification queue:
- `doi` `10.5555/sourcecheckup.synthetic.v02a`: declared_source_status_not_checked
- `pmid` `123456789`: undeclared_locator_found_in_answer

### sc_v02_url_missing_inventory_004

Gate: `blocked_missing_source_support`

External source clearance: `false`

Flags:
- `medium` `undeclared_locator_in_answer`: Answer contains a source locator that is not declared in source inventory. Evidence: `url:https://example.org/synthetic/source_a`
- `medium` `unsupported_source_language`: Answer uses broad source support language that needs a specific verified source or rewrite. Evidence: `official sources support`
- `high` `guideline_claim_missing_structured_support`: Answer appears to make a guideline claim without a linked guideline claim record.

Verification queue:
- `url` `https://example.org/synthetic/source_a`: undeclared_locator_found_in_answer
- `unsupported_source_language` `official sources support`: rewrite_or_link_to_verified_source

### sc_v02_complete_inventory_005

Gate: `blocked_pending_source_verification`

External source clearance: `false`

Flags:
- `medium` `source_not_externally_verified`: Declared source is not externally verified. Evidence: `s1:url:https://example.org/synthetic/source_b`

Verification queue:
- `url` `https://example.org/synthetic/source_b`: declared_source_status_not_checked
