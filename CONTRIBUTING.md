# Contributing

MedFailBench welcomes focused contributions from clinicians, evaluation researchers, language reviewers, and open source maintainers.

The project uses synthetic cases only. It is not clinical advice, a clinical validation study, or evidence that a model is safe for clinical use.

## Choose one contribution route

### Report one weak spot

Use [issue 182](https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/182) if you want to flag one unclear claim, missing safety gate, wording problem, or source support concern.

One short response is enough:

```text
Weak spot:
Safer wording or missing gate:
```

A maintainer or controlled seed can test the route, but it is not outside review and is not external validation.

### Propose a synthetic case

Open the [synthetic case issue form](https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/new?template=synthetic_case.yml). The form asks for the clinical domain, care setting, task, expected safety behavior, missing variables, and review question.

Use only invented details. Do not adapt a real patient encounter, note, message, or model transcript.

### Improve code or documentation

Open a focused pull request. Good first contributions include:

1. One validator correction.
2. One adapter or integration fix.
3. One documentation clarification.
4. One Turkish medical language review.
5. One reproducible test for an existing behavior.

The [documentation map](docs/README.md) identifies the current release, method, rubric, and review files.

## Nonnegotiable boundaries

Every contribution must follow these rules:

1. Do not submit patient data or protected health information.
2. Do not include dates, locations, identifiers, rare details, or excerpts derived from a real patient.
3. Do not submit private clinical text or private model output.
4. Mark synthetic material and its provenance clearly.
5. Do not claim clinical validation, deployment readiness, regulatory approval, endorsement, or overall model safety.
6. Do not infer a global model ranking from one case or one run.
7. Do not add external model outputs unless their terms permit redistribution.
8. Keep safety wording conservative and identify missing variables that could change the safe response.

Allowed review wording:

```text
physician authored synthetic draft pending final clinician review
```

Do not use:

```text
clinician validated
safe for clinical use
```

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
```

Run the checks that match your change:

```bash
python3 -m pytest
make validate-public
```

Documentation only changes still need link and formatting checks. State exactly which commands you ran in the pull request.

## Pull request scope

Keep one pull request focused on one problem. Explain:

1. What changed.
2. Why the change is needed.
3. Which public claim or behavior it affects.
4. Which checks were run.
5. What remains unverified.

Use the repository pull request template. A maintainer may request narrower wording, an additional synthetic test, or removal of unsupported claims before merging.

## Review routes

Use the existing issue forms for specialized review:

* [Evidence concern](https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/new?template=evidence_concern.yml)
* [Label audit review](https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/new?template=label_audit_review.yml)
* [Clinician review](https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/new?template=clinician_review.yml)
* [SourceCheckup review](https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/new?template=sourcecheckup_review.yml)

Questions and early ideas can start in [GitHub Discussions](https://github.com/goktugozkanmd/medical-ai-failure-atlas/discussions).

## License

Contribution licensing follows the project notice. Code contributions are provided under Apache License 2.0. Synthetic data, documentation, evaluation cards, and other noncode text are provided under Creative Commons Attribution 4.0 International unless a file states otherwise. See [LICENSE](LICENSE) for the full notice.
