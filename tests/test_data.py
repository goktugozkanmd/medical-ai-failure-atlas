from __future__ import annotations

from pathlib import Path

import pytest

from failure_atlas.data import SchemaValidationError, load_eval_set, load_prompt_set, load_scoring_rubric


ROOT = Path(__file__).resolve().parents[1]


def test_load_prompt_set_v1() -> None:
    prompts = load_prompt_set(ROOT / "data" / "prompt_set_v1.tsv")
    assert len(prompts) == 10
    assert prompts[0].scenario_id == "M001"
    assert prompts[0].prompt_text


def test_load_scoring_rubric_v0_3() -> None:
    rubric = load_scoring_rubric(ROOT / "data" / "scoring_rubric_v0_3.json")
    assert rubric.schema_version == "scoring_rubric_v0_3"
    assert "unsafe_remote_dosing" in rubric.gate_ids
    assert "clinical_correctness" in rubric.dimension_ids


def test_load_eval_set_jsonl() -> None:
    cases = load_eval_set(ROOT / "data" / "tr_medllm_synthetic_eval_set_v0_3.jsonl")
    assert len(cases) > 5
    assert cases[0].case_id == "TRFAI015"
    assert cases[0].prompt
    assert all(
        "pending clinician review" not in case.raw["synthetic_case_summary"].lower()
        for case in cases
    )


def test_prompt_schema_error(tmp_path: Path) -> None:
    bad = tmp_path / "bad.tsv"
    bad.write_text("scenario_id\tprompt_text\nX001\tPrompt\n", encoding="utf-8")
    with pytest.raises(SchemaValidationError, match="columns must be"):
        load_prompt_set(bad)


def test_approved_eval_set_rejects_stale_review_state(tmp_path: Path) -> None:
    bad = tmp_path / "bad_eval.jsonl"
    bad.write_text(
        (
            '{"case_id":"TRFAI999","turkish_prompt_seed":"Prompt",'
            '"synthetic_case_summary":"pending clinician review despite approved gate",'
            '"release_gate":"approved","final_label":"clinician_reviewed",'
            '"synthetic_only":true,"patient_data_used":false,'
            '"clinical_use_allowed":false}\n'
        ),
        encoding="utf-8",
    )

    with pytest.raises(SchemaValidationError, match="stale review-state phrase"):
        load_eval_set(bad)
