# SourceCheckup Medical CLI Report

Date: 2026 07 08

Status: local CLI report ready.

Roadmap phase: P3 SourceCheckup Medical CLI.

## Product Surface

This adds a runnable single answer CLI report for medical AI source support review.

Command: `python3 scripts/sourcecheckup_medical.py report`.

Report schema: `sourcecheckup_medical_report_v0_2`.

The report separates source presence from exact claim support. A locator, URL, DOI, PMID, guideline phrase, or policy phrase does not clear a medical claim by itself.

## Boundary

No external send, no provider API call, no automation start, no new case addition, no patient data, no physician selection, no clinical validation claim, no source truth certification claim, no regulatory compliance claim, no official compatibility claim, and no model ranking.

## Features

- `single_answer_cli_report`.
- `manual_answer_or_answer_file_input`.
- `optional_declared_sources_json`.
- `optional_declared_claims_json`.
- `source_presence_vs_exact_claim_support_boundary`.
- `markdown_and_json_output`.

## Sample Smoke

- Answer id: `SOURCECHECKUP_CLI_P3_SMOKE`.
- External use gate: `blocked_pending_source_verification`.
- Source claims present: `true`.
- Declared sources: 1.
- Declared claims: 1.
- Verification queue count: 3.

## Outputs

- JSON report: `sourcecheckup/build/sourcecheckup_medical_cli_report_20260708.json`.
- Markdown report: `sourcecheckup/build/sourcecheckup_medical_cli_report_20260708.md`.

## Next

1. Connect this report output to the kit level assurance card.
2. Keep public source support claims blocked until exact source support is checked.

## Validation

Run:

```bash
make sourcecheckup_medical_cli_report_20260708
```
