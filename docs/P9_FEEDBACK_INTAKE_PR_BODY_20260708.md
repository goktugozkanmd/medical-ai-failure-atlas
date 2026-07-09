## Summary

This PR adds the P9 feedback intake route for the Health AI Assurance Kit.

It adds a public intake guide, a JSON manifest, a GitHub issue template, a validator, a pytest check, and a README link. The route helps reviewers choose between kit feedback, SourceCheckup review, synthetic failure case intake, and evidence concern reporting.

## Scope

1. Add the Health AI Assurance feedback intake guide.
2. Add a matching machine readable manifest.
3. Add a Health AI Assurance Kit feedback issue template.
4. Add validator and pytest coverage.
5. Link the intake from the README Health AI Assurance line.

## Boundaries

1. No patient data.
2. No private clinical text.
3. No provider API run.
4. No new case addition.
5. No physician selection.
6. No medical advice.
7. No clinical validation claim.
8. No model ranking claim.
9. No source truth certification claim.
10. No regulatory compliance claim.
11. No official compatibility or institution support claim.

## Checks

1. Feedback intake validator passes.
2. README local link test passes.
3. Targeted pytest passes.
4. Academic submission audit passes on outward facing P9 text.
5. Reference script finds 0 extracted references in the outward facing P9 text.
6. Public release sanitation passes.
