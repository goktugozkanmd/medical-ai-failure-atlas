# SourceCheckup repo run guide v0.1

Status: generated public preview.

Date: 2026 06 17

This guide gives contributors one practical route for running the SourceCheckup Medical surfaces from this repository.

It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not source truth certification, not a model safety claim, not a model ranking, not a benchmark compatibility claim, and not an official endorsement.

## Summary

Run guide rows: 6

Doctor output: `docs/sourcecheckup/sourcecheckup_repo_doctor_v0_1.json`

Guide JSON: `docs/sourcecheckup/sourcecheckup_repo_run_guide_v0_1.json`

Runnable target: `make sourcecheckup_repo_run_guide`

## Recommended path

1. `make sourcecheckup`

Check: seed examples and report generation.

2. `make sourcecheckup_v02`

Check: ten public source surface examples.

3. `make source_claim_queue`

Check: twelve source claim review rows.

4. `make sourcecheckup_expansion_dashboard`

Check: public expansion dashboard and queue surface.

5. `make sourcecheckup_turkish_institutional_wording`

Check: five Turkish institutional wording examples.

6. `make sourcecheckup_repo_run_guide`

Check: required files and row counts.

## Run rows

### SCRUN001: basic source scan

Command: `make sourcecheckup`

Checks: seed examples and report generation

### SCRUN002: expanded example scan

Command: `make sourcecheckup_v02`

Checks: ten public source surface examples

### SCRUN003: review queue check

Command: `make source_claim_queue`

Checks: twelve source claim review rows

### SCRUN004: expansion dashboard check

Command: `make sourcecheckup_expansion_dashboard`

Checks: public expansion dashboard and queue surface

### SCRUN005: institutional wording check

Command: `make sourcecheckup_turkish_institutional_wording`

Checks: five Turkish institutional wording examples

### SCRUN006: repo doctor check

Command: `make sourcecheckup_repo_run_guide`

Checks: required files and row counts

## Boundary checks

1. Patient data is not used.
2. External calls are not required.
3. Model calls are not required.
4. Passing local SourceCheckup does not certify a medical source.
5. Passing local SourceCheckup does not validate clinical use.
6. Passing local SourceCheckup does not create benchmark compatibility.

## Public files

1. Run guide: `docs/sourcecheckup/SOURCECHECKUP_REPO_RUN_GUIDE_V0_1.md`
2. Run guide JSON: `docs/sourcecheckup/sourcecheckup_repo_run_guide_v0_1.json`
3. Doctor JSON: `docs/sourcecheckup/sourcecheckup_repo_doctor_v0_1.json`
4. Generator: `scripts/generate_sourcecheckup_repo_run_guide_v0_1.py`
5. Doctor: `scripts/sourcecheckup_repo_doctor_v0_1.py`
6. Validator: `scripts/validate_sourcecheckup_repo_run_guide_v0_1.py`
7. Runnable target: `make sourcecheckup_repo_run_guide`
