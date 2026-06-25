# Multilingual Medical Intelligence Public Wording Bank v0.1

Date: 2026 06 25

Status: public repo documentation

## Purpose

The Multilingual Medical Intelligence public wording fixture bank gives maintainers synthetic Turkish and English examples for public language review.

Maintainers use the bank to check whether public wording keeps education separate from care, preserves uncertainty, and carries the same meaning across languages.

The bank uses synthetic cases only. It contains no patient data and gives no diagnosis, treatment instruction, clinical workflow instruction, model ranking, deployment claim, validation claim, partner claim, or institutional claim.

## Schema

Each row describes one public wording item and one expected local review result.

```text
row_id
fixture_version
atlas_layer
atlas_node_id
source_state_pair_id
language_pair
clinical_domain
scenario_stub
public_wording_en
public_wording_tr_ascii
plain_clinical_language_checks
missing_data_to_preserve
source_support_to_preserve
unsafe_rewrite_to_avoid
review_gate
release_boundary
```

## Field Notes

`row_id`: stable row id.

`fixture_version`: expected value `v0_1_20260625`.

`atlas_layer`: expected value `Multilingual Medical Intelligence`.

`atlas_node_id`: expected value `mia_mmi_002`.

`source_state_pair_id`: paired state row used as the local source boundary.

`language_pair`: expected value `Turkish English`.

`clinical_domain`: short synthetic topic label.

`scenario_stub`: brief synthetic situation for local fixture review.

`public_wording_en`: English text for public review.

`public_wording_tr_ascii`: Turkish ASCII text for public review.

`plain_clinical_language_checks`: row level plain language checks.

`missing_data_to_preserve`: facts the wording must leave absent if the input does not contain them.

`source_support_to_preserve`: source support limits that must remain visible.

`unsafe_rewrite_to_avoid`: example of wording that the gate should block.

`review_gate`: status and local blocker flags.

`release_boundary`: synthetic scope and blocked use flags.

## Current Bank

The v0.1 bank contains eight rows.

It covers emergency symptom wording, medication safety wording, chronic monitoring wording, pregnancy symptom wording, laboratory result wording, follow up result wording, source support excerpt wording, and multilingual translation wording.

Every row maps to one of the six paired Turkish English state examples. The validator requires all six source pairs to be represented.

## Checks

1. Language meaning: Turkish and English wording describe the same synthetic situation.
2. Certainty preservation: wording does not add diagnosis, severity, timing, dose, result, or outcome.
3. Missing data preservation: absent facts stay absent.
4. Care boundary: wording stays in general education and does not instruct a reader to act on a condition.
5. Public claim boundary: wording avoids clinical validation, clinical deployment, model superiority, partner, institutional, fee, deadline, publisher, source, web link, and bibliographic identifier claims.
6. Atlas fit: each row maps to `mia_mmi_002` and can feed the plain clinical language gate.

## Release Boundary

This v0.1 bank supports repository quality review for synthetic public wording. It does not clear text for patient care, clinical validation, clinical deployment, model comparison, institutional use, or external publication.

A row can move into a repo preview set when it has synthetic scope, explicit language pair, source pair linkage, no patient data, no diagnosis or treatment instruction, no unsupported public clinical claim, and a recorded review status.

Rows that contain source claims, formal title claims, partner claims, or clinical performance claims remain blocked until maintainers remove the claim or add a separate verified source record.

## Atlas Connection

Atlas node: `mia_mmi_002`.

The Medical Intelligence Atlas names a public wording fixture bank as the next build for the plain clinical language gate.

This bank gives that atlas node a small row schema, source pair linkage, review boundary, and check list. It connects Multilingual Medical Intelligence with Clinical State Language, Medical Reasoning Verifier, and release readiness review without adding clinical use claims.

## Validation Command

`make multilingual_medical_intelligence_public_wording_bank`
