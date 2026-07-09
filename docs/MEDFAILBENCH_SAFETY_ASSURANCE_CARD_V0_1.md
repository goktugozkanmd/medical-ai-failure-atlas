# MedFailBench Safety Assurance Card v0.1

Status: local build. Not externally released.

Date: 2026 07 08

Artifact: Medical AI Failure Atlas and MedFailBench safety gate work.

Release gate level: L1 local build.

This card records what the current repository can safely claim, what it cannot claim, and what must be checked before any external message, issue, pull request, submission, or outreach packet uses the project.

It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not official endorsement.

## Intended Use

1. Keep MedFailBench framed as a synthetic clinician safety evaluation artifact.
2. Make current evidence visible before any public wording is drafted.
3. Separate local engineering evidence from clinical, regulatory, or institutional claims.
4. Give contributors a simple gate before outreach to benchmark maintainers, clinicians, academic venues, or governance groups.

## Non Use Boundary

1. Do not use this card for clinical care.
2. Do not use this card as a claim that any model has proven safety.
3. Do not use this card as a claim that any benchmark result is clinically valid.
4. Do not use this card as a claim of NIST, CHAI, FDA, WHO, MedHELM, or HealthBench endorsement.
5. Do not use this card as a medical device submission artifact.
6. Do not post, email, upload, or package this card externally before a fresh audit and owner approval.

## Current Evidence State

1. `data/failure_atlas_external_sample_v0_1.jsonl` exists as a three row public sample.
2. `data/medhelm_remote_rescue_metric_v0_1.json` exists as a synthetic metric draft.
3. `data/panel_pilot/clinician_panel_pilot_cases_v0_1.tsv` has fifteen synthetic panel cases.
4. `data/panel_pilot/clinician_panel_rating_sheet_v0_1.tsv` has thirty reviewer assignments.
5. `docs/MEDHELM_THREE_CASE_UPSTREAM_PACKET_V0_1.md` exists as a draft only upstream discussion packet.
6. `failure_atlas/panel_console.py` and `failure_atlas/panel_review.py` support local clinician review capture.

## Evidence Gaps

1. No clinician review results are recorded in this card.
2. No model endpoint run is part of this card.
3. No raw model output is released by this card.
4. No inter reviewer agreement is reported by this card.
5. No external maintainer has accepted or endorsed this card.
6. No patient data review route is opened by this card.

## Privacy And Data Boundary

1. contains_patient_data: false.
2. identifiers_present: false.
3. synthetic_examples_only: true.
4. patient_data_route: blocked.
5. real_world_deployment_route: blocked.
6. privacy_release_decision: local only.

Any future route using real patient text, screenshots, portal data, copied clinical notes, or identifiable examples must stop before writing the data into this repository.

## Source Lenses

These are orientation anchors only. They are not compliance claims.

1. NIST AI RMF lens: risk management and trustworthiness language should stay explicit across design, use, and evaluation.
2. CHAI Applied Model Card lens: a health AI artifact should make use case, workflow, technical context, safety, fairness, transparency, privacy, and security boundaries visible.
3. FDA lifecycle draft lens: if a future product route appears, lifecycle risk management and marketing submission documentation are a different evidence lane from this local benchmark card.
4. FDA PCCP lens: any planned model or metric change needs a change log, validation plan, and impact assessment before external claims.
5. WHO LMM lens: large model health use needs ethics and governance boundaries, especially where a general purpose system can affect health communication.

Source verification file:

`docs/MEDFAILBENCH_SAFETY_ASSURANCE_CARD_SOURCE_VERIFICATION_20260708.md`

## Risk Register

| Risk | Current status | Required control |
| --- | --- | --- |
| False reassurance | Active benchmark theme | Clinician review and red flag wording checks |
| Unsafe remote dosing | Active benchmark theme | Block dosing calculation examples from public advice wording |
| Missed urgent escalation | Active benchmark theme | Require escalation gate labels in cases |
| Fabricated source support | Active benchmark theme | Source claim queue and reference verification before outreach |
| Benchmark misuse | Active public risk | No ranking language and no model safety claim |
| Patient data leakage | Blocked route | Synthetic only gate and reviewer flag |
| Institutional overclaim | Active public risk | No endorsement wording unless official written evidence exists |

## Human Review State

1. Reviewer roster: local reviewer codes only.
2. Completed reviews: none recorded in this card.
3. Adjudication state: not started.
4. Kappa or agreement state: not available.
5. Public wording clearance: not cleared.

## Release Gate

Current level: L1 local build.

L1 means the local files exist and validate. External use is not allowed by default.

Conditions to move to L2:

1. At least one clinician review pass is recorded.
2. Possible patient data flags are reviewed.
3. High severity cases are checked for wording and source support.
4. Open disagreements are logged.

Conditions to move to L3:

1. Public wording is audited.
2. Source claims are refreshed from official pages.
3. Any academic or formal submission text has a visible audit record.
4. Exact target and exact action are known.
5. Owner approval is recorded.

L5 clinical deployment is blocked in this automation.

## Public Wording Allowed

Use wording like:

1. MedFailBench is a synthetic safety evaluation workbench.
2. The current card is a local assurance record.
3. The current examples are not patient data.
4. The current evidence does not establish clinical validation.
5. The current evidence does not rank models.
6. The current evidence does not show official endorsement.

## Public Wording Blocked

Do not claim:

1. clinical validation.
2. model safety.
3. model ranking.
4. deployment readiness.
5. regulatory approval.
6. official endorsement.
7. benchmark compatibility.
8. patient data use.

## Audit Trail

1. Markdown card: `docs/MEDFAILBENCH_SAFETY_ASSURANCE_CARD_V0_1.md`
2. JSON card: `docs/medfailbench_safety_assurance_card_v0_1.json`
3. Source verification note: `docs/MEDFAILBENCH_SAFETY_ASSURANCE_CARD_SOURCE_VERIFICATION_20260708.md`
4. Validator: `scripts/validate_medfailbench_safety_assurance_card_v0_1.py`
5. Runnable target: `make medfailbench_safety_assurance_card`
6. External action status: blocked until fresh audit, source refresh, and owner approval.
