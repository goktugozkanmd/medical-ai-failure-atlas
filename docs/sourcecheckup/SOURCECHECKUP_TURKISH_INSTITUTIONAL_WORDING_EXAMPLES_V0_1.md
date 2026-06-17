# SourceCheckup Turkish institutional wording examples v0.1

Status: generated public preview.

Date: 2026 06 17

These examples help reviewers separate institutional wording from unsupported endorsement, route access, submission, deployment, and validation claims.

They use synthetic wording examples only. They are not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, not route access, not a submission claim, and not an official endorsement.

## Summary

Turkish institutional wording examples: 5

Blocked claim types: 5

Reviewer lanes: 5

Linked SourceCheckup route: `SCQ_008`

Linked assurance route: `ARG006`

Linked public packet: `docs/tr%2Dmedai%2Dsafety%2Dsuite/TUBITAK_1711_COLLABORATION_READINESS_PACKET_V0_1.md`

## Blocked claim coverage

clinical deployment: 1

official endorsement: 1

route access: 1

submission claim: 1

validation claim: 1

## Examples

### STIWE001: ministry wording

Synthetic risky wording: This work is aligned with national health AI priorities.

Blocked claim: official endorsement

Safe public wording: This public preview studies health AI safety questions and does not claim a Ministry role or endorsement.

SourceCheckup action: replace alignment language with scope language

Review lane: institutional wording review

### STIWE002: TÜYZE wording

Synthetic risky wording: The project is ready for a national AI ecosystem route.

Blocked claim: route access

Safe public wording: The project prepares public review artifacts that could support a future route decision after verified clearance.

SourceCheckup action: separate readiness from access

Review lane: route wording review

### STIWE003: TÜBİTAK wording

Synthetic risky wording: This packet supports a TÜBİTAK application.

Blocked claim: submission claim

Safe public wording: This packet records source boundaries and does not claim application submission.

SourceCheckup action: replace support claim with boundary record

Review lane: submission wording review

### STIWE004: hospital wording

Synthetic risky wording: The examples are ready for hospital workflow testing.

Blocked claim: clinical deployment

Safe public wording: The examples are synthetic review material and are not for hospital workflow deployment.

SourceCheckup action: block workflow testing language

Review lane: clinical deployment wording review

### STIWE005: university lab wording

Synthetic risky wording: A university lab can validate this safety benchmark.

Blocked claim: validation claim

Safe public wording: A future reviewer could inspect the method, but this public preview does not claim validation.

SourceCheckup action: replace validation language with review language

Review lane: validation wording review

## Review use

1. Use these examples before public text names a Ministry, TÜYZE, TÜBİTAK, hospital, university lab, benchmark, or regulator.
2. Replace alignment language with source boundary language unless there is verified external permission.
3. Replace ready for route language with preparation language unless route access is verified.
4. Replace application language with packet or source boundary language unless submission is actually executed and cleared.
5. Replace validation language with review language unless an external validation record exists.

## Boundary checks

1. Every example is synthetic.
2. Patient data is not used.
3. No institutional endorsement is claimed.
4. No route access is claimed.
5. No submission is claimed.
6. No clinical deployment is claimed.
7. No clinical validation is claimed.

## Public files

1. Generated examples: `docs/sourcecheckup/SOURCECHECKUP_TURKISH_INSTITUTIONAL_WORDING_EXAMPLES_V0_1.md`
2. Generated JSON: `docs/sourcecheckup/sourcecheckup_turkish_institutional_wording_examples_v0_1.json`
3. Generator: `scripts/generate_sourcecheckup_turkish_institutional_wording_examples_v0_1.py`
4. Validator: `scripts/validate_sourcecheckup_turkish_institutional_wording_examples_v0_1.py`
5. Runnable target: `make sourcecheckup_turkish_institutional_wording`
