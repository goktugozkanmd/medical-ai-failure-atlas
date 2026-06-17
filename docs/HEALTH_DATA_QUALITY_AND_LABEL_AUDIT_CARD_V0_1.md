# Health data quality and label audit card v0.1

Date: 2026 06 16

Status: public preview.

This card summarizes the synthetic data quality and label audit boundary for the Medical AI Failure Atlas public repository.

It is a synthetic dataset release readiness checklist. It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, and not an institutional or national program endorsement.

## Dataset surfaces

Current public source files:

1. `data/scenario_bank_v1.tsv`
2. `data/scenario_bank_v2_hard_addendum.tsv`
3. `data/scenario_bank_v3_scale_seed.tsv`
4. `data/prompt_set_v1.tsv`
5. `data/prompt_set_v2_hard_30.tsv`
6. `data/prompt_set_v3_scale_30.tsv`
7. `data/inter_rater_review_subset_v0_1.tsv`
8. `data/scoring_rubric_v0_1.json`
9. `docs/LABEL_DEFINITION_LOCK_V0_1.md`
10. `LABELING.md`
11. `sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl`

## Current counts

1. 150 synthetic scenario rows.
2. 70 prompt rows.
3. 24 pilot inter rater rows.
4. 14 Turkish synthetic risk rows.
5. 12 source claim review queue rows.

The 24 pilot inter rater rows are for protocol testing only. They are not a powered agreement study and they do not establish clinical validation.

## Provenance

1. Data provenance: synthetic only.
2. Patient data: absent.
3. Direct identifiers: absent.
4. Real clinical records: absent.
5. Raw model outputs: excluded from the public release.
6. Output redistribution terms: not cleared for raw output publication.

## Label method

Current public review wording:

`single physician authored synthetic draft pending additional clinician review`

Current label version:

`v0.1.0`

Current label lock:

`docs/LABEL_DEFINITION_LOCK_V0_1.md`

Current rubric:

`data/scoring_rubric_v0_1.json`

The label audit checks whether the label definitions, safety gates, pilot subset, and public wording are internally consistent. It does not prove that the labels are correct for real clinical use.

## Quality checks

This card tracks:

1. Synthetic provenance.
2. Patient data absence.
3. Identifier absence.
4. Scenario count.
5. Prompt count.
6. Pilot inter rater subset count.
7. Label version.
8. Label lock file.
9. Reviewer status.
10. Raw output exclusion.
11. SourceCheckup routing.
12. Public release gate.

## Known limitations

1. Scenario banks are synthetic and may not cover real workflow diversity.
2. The pilot inter rater subset is for protocol testing only.
3. Additional clinician review is still pending.
4. No agreement statistic is reported here.
5. Raw model outputs are not public.
6. This card does not evaluate any model.
7. This card does not approve any dataset for clinical deployment.

## SourceCheckup routing

Rows that make source, guideline, policy, or broad evidence claims should be routed to:

`sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl`

SourceCheckup routing is a review queue. It does not turn a citation, PMID, DOI, URL, guideline phrase, or policy phrase into evidence.

## Release gate

Current release gate:

`public_preview_allowed_synthetic_only`

Allowed public use:

1. Repository inspection.
2. Synthetic evaluation design discussion.
3. Contributor review of source claim and label audit structure.
4. Clinician review workflow design.

Not allowed public use:

1. Patient care.
2. Clinical deployment.
3. Clinical validation claims.
4. Model ranking.
5. Claims that one model is better than another.
6. Claims of formal approval.
7. Claims of sandbox access.
8. Claims of institutional backing.

## Label audit reviewer role table

Use `docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md` when a public dataset surface needs provenance review, label definition review, pilot subset framing review, raw output exclusion review, or public release boundary review.

The table defines four public reviewer roles:

1. Synthetic provenance reviewer.
2. Label definition reviewer.
3. Pilot subset reviewer.
4. Public release boundary reviewer.

Run:

```bash
make label_audit_role_table
```

The linked escalation gate audit rows keep synthetic provenance, label definition lock, pilot inter rater subset, raw output exclusion, and public release boundary checks visible before stronger public wording.

## Label audit public contributor route

Contributors may open a public synthetic label audit issue with:

`.github/ISSUE_TEMPLATE/label_audit_review.yml`

Guide:

`docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md`

The route accepts synthetic examples for provenance, label definition lock, pilot subset framing, raw output exclusion, and public release boundary review. It does not allow patient data, raw model outputs, clinical advice, clinical validation claims, dataset quality proof, or outward use without maintainer review.

Run:

```bash
make label_audit_public_issue
```

## Label audit example intake rows

Current public example intake rows:

`docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md`

Machine readable source:

`docs/label_audit/label_audit_example_intake_v0_1.json`

The file contains 5 synthetic label audit examples for synthetic provenance, label definition lock, pilot subset framing, raw output exclusion, and dataset quality proof boundary review. These examples are intake rows only. They do not prove dataset quality, clinical readiness, clinical validation, model safety, or formal approval.

Run:

```bash
make label_audit_examples
```

## Label audit example dashboard

Current public dashboard:

`docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md`

Machine readable dashboard source:

`docs/label_audit/label_audit_example_dashboard_v0_1.json`

The dashboard summarizes 5 intake rows by reviewer role, audit row, review state, and blocked public claim type. Blocked public claim types represented: 5.

Run:

```bash
make label_audit_dashboard
```

## Label audit maintainer triage board

Current public triage board:

`docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md`

Machine readable triage source:

`docs/label_audit/label_audit_maintainer_triage_board_v0_1.json`

Maintainer triage rows: 5.

The board turns dashboard rows into maintainer actions, owner roles, triage status values, and next public wording decisions. It does not approve dataset quality, clinical readiness, clinical validation, model safety, or formal approval.

Run:

```bash
make label_audit_triage
```

## Label audit public wording decision log

Current public wording decision log:

`docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md`

Machine readable decision source:

`docs/label_audit/label_audit_public_wording_decision_log_v0_1.json`

Public wording decision rows: 5.

The log records blocked wording, proposed public wording, reviewer role, decision status, maintainer action, and next public surface for each triage row. It does not approve dataset quality, clinical readiness, clinical validation, model safety, or formal approval.

Run:

```bash
make label_audit_wording_log
```

## Label audit release gate checklist

Current release gate checklist:

`docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md`

Machine readable release gate source:

`docs/label_audit/label_audit_release_gate_checklist_v0_1.json`

Release gate rows: 5.

The checklist converts wording decisions into required pass or block states for synthetic provenance, label definition review, pilot subset scope, raw output release, and dataset quality proof boundaries. It does not approve dataset quality, clinical readiness, clinical validation, model safety, or formal approval.

Run:

```bash
make label_audit_release_gates
```

## Label audit release gate outcome dashboard

Current release gate outcome dashboard:

`docs/label_audit/LABEL_AUDIT_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md`

Machine readable outcome source:

`docs/label_audit/label_audit_release_gate_outcome_dashboard_v0_1.json`

Outcome rows: 5.

The dashboard summarizes pass and block outcomes across label audit release gate rows. It does not approve dataset quality, clinical readiness, clinical validation, model safety, or formal approval.

Run:

```bash
make label_audit_outcome_dashboard
```

## Label audit release note packet

Current release note packet:

`docs/label_audit/LABEL_AUDIT_RELEASE_NOTE_PACKET_V0_1.md`

Machine readable packet source:

`docs/label_audit/label_audit_release_note_packet_v0_1.json`

Packet surface rows: 7.

The packet gives one public release note surface for the contributor route, intake rows, dashboard, triage board, wording log, release gate checklist, and outcome dashboard. It does not approve dataset quality, clinical readiness, clinical validation, model safety, or formal approval.

Run:

```bash
make label_audit_release_packet
```

## Maintenance owner

Maintainer: Dr. Goktug Ozkan, Internal Medicine Specialist.

Maintenance action:

Update this card whenever public scenario counts, prompt counts, label version, review status, or raw output release boundary changes.
