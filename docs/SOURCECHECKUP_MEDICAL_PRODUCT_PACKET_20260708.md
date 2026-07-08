# SourceCheckup Medical Product Packet

Date: 2026 07 08

Status: local product packet. Not externally released.

Purpose: turn existing SourceCheckup Medical work into a clearer product surface for medical AI answer source support review.

## Product Shape

Input:

1. Model answer.
2. Optional declared sources.
3. Optional declared claims.

Output:

1. Supported.
2. Unsupported.
3. Source needed.
4. Overclaimed.
5. Hold for external source support review.

## Local Route

```bash
make sourcecheckup
make sourcecheckup_medical_source_claim_walkthrough
```

## Product Rules

1. Locator format is not claim support.
2. A real URL, DOI, or PMID is not enough unless the source supports the exact claim.
3. Guideline, policy, drug dose, diagnostic certainty, institution, regulatory, and endorsement claims require explicit source support.
4. External wording is blocked until source support and audit state are refreshed.

## Growth Work

1. Add a paste based CLI mode.
2. Add twenty synthetic examples.
3. Add Turkish and English source support examples.
4. Connect SourceCheckup output to SafetyGuard transparency cards.

## Boundary

No patient data, no guideline truth certification, no clinical validation, no regulatory compliance claim, no official endorsement claim.

