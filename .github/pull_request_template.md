## Summary

Describe the single problem this pull request addresses and the smallest public behavior or claim that changes.

## Contribution type

* [ ] Validator or test
* [ ] Adapter or integration
* [ ] Synthetic data or rubric
* [ ] Documentation
* [ ] Turkish medical language review

## Safety and data boundary

* [ ] This contribution contains no patient data, protected health information, private clinical text, or private model output.
* [ ] Any case material is fully synthetic and its provenance is stated.
* [ ] The change does not claim clinical validation, deployment readiness, regulatory approval, endorsement, or overall model safety.
* [ ] External model output is included only when redistribution is permitted.

## Evidence

List the files, issue, source, or reproducible behavior that supports this change.

## Verification

List the exact commands you ran and their results. If a check was not run, explain why.

```text
python3 -m pytest
make validate-public
```

## Remaining uncertainty

State what this pull request does not prove or what still needs review.
