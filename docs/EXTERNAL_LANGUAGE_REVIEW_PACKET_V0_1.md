# External Language Review Packet v0.1

Status: public contributor intake guard.

Purpose: give language reviewers a small, testable packet for synthetic Failure Atlas sample rows. The packet keeps translation review separate from clinical validation, model ranking, and patient advice.

## Scope

Use this packet when a contributor reviews whether safety risk survives translation for a public synthetic sample case such as `FA_SAMPLE_001`.

Allowed contribution:

1. A close translation of the source synthetic prompt.
2. A note on whether the safety risk is preserved in the target language.
3. The source failure tags that the reviewer believes are still visible.
4. A wording risk note.
5. A safer rewrite in the target language.

Not allowed:

1. Patient data.
2. Clinical use advice.
3. Model ranking.
4. Clinical validation claims.
5. Official endorsement claims.

## Required JSONL Fields

Each row must include:

```json
{
  "review_id": "FA_SAMPLE_001_LANG_REVIEW_001",
  "source_case_id": "FA_SAMPLE_001",
  "review_language": "zh",
  "review_kind": "close_translation_then_safer_rewrite",
  "reviewer_public_handle": "example-reviewer",
  "reviewer_role": "biomedical language reviewer",
  "translation_text": "Target language close translation.",
  "risk_preservation_note": "Short note about preserved risk.",
  "failure_mechanism_tags_preserved": ["unsafe_remote_dosing"],
  "wording_risk_note": "Short note about unsafe wording risk.",
  "safer_rewrite": "Target language safer rewrite.",
  "contains_patient_data": false,
  "clinical_use_allowed": false,
  "model_ranking_claim": false,
  "clinical_validation_claim": false
}
```

## Local Validation

```bash
python3 scripts/validate_external_language_review_packet_v0_1.py path/to/review.jsonl
```

The validator checks that the source case exists in `data/failure_atlas_external_sample_v0_1.jsonl`, preserved tags match the source case, and public boundary booleans stay false.
