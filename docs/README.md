# MedFailBench Documentation Map

This page identifies the current public entry points for MedFailBench. Files not listed here may be working records, generated artifacts, historical notes, or supporting material. They do not replace the release manifest, method, rubric, or citation metadata below.

## Start here

* [Current public status](CURRENT_PUBLIC_STATUS.md)
* [Project overview and quick start](../README.md)
* [Public artifact integrity manifest](release/PUBLIC_ARTIFACT_MANIFEST_V0_1.json)
* [Changelog](../CHANGELOG.md)
* [Citation metadata](../CITATION.cff)
* [Apache License 2.0](../LICENSE)
* [License scope and attribution notice](../NOTICE)

## Method and review boundaries

* [Public methodology](../failure_atlas/public/METHODOLOGY.md)
* [Clinical severity rubric](CLINICAL_SEVERITY_RUBRIC_V0_2.md)
* [Safety gate taxonomy](SAFETY_GATE_TAXONOMY_V0_2.md)
* [Clinician panel protocol](CLINICIAN_PANEL_PROTOCOL_V0_1.md)

These files describe synthetic evaluation and review procedures. They do not establish clinical validation, model safety, deployment readiness, regulatory approval, or endorsement.

## Data and integrations

* [Data guide](../data/README.md)
* [Adapter overview](../adapters/README.md)
* [Inspect Evals adapter](../adapters/inspect_evals/README.md)
* [LM Evaluation Harness adapter](../adapters/lm_eval/README.md)
* [OpenCompass adapter](../adapters/opencompass/README.md)

## Contribute or review

* [Contribution guide](../CONTRIBUTING.md)
* [Synthetic case issue form](https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/new?template=synthetic_case.yml)
* [Evidence concern issue form](https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/new?template=evidence_concern.yml)
* [Clinician review issue form](https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/new?template=clinician_review.yml)
* [GitHub Discussions](https://github.com/goktugozkanmd/medical-ai-failure-atlas/discussions)

## Status rule

When two files appear to conflict, use this order:

1. Current public status and integrity manifest.
2. Current method, rubric, and taxonomy.
3. Current README and citation metadata.
4. Dated development notes and generated artifacts.

Open an [evidence concern](https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/new?template=evidence_concern.yml) if a public claim conflicts with the higher priority source.

## Historical and working material

The `docs/` directory contains dated research notes, outreach records, generated dashboards, and older release preparation files. A file name, validator pass, or historical release record does not by itself establish a current benchmark claim. Use the current public status and the supporting source file before repeating a number, availability statement, or validation claim.
