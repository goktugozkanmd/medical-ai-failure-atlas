from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXPORT_SCRIPT = ROOT / "scripts" / "export_safetyguard_transparency_card.py"
WALKTHROUGH_SCRIPT = ROOT / "examples" / "usage_walkthrough.py"

CARD_EXPORT_DOCS = [
    ROOT / "docs" / "SAFETYGUARD_EVALUATION_CARD_EXPORT_PATH_20260708.md",
    ROOT / "adapters" / "huggingface" / "evaluation_card_medfailbench_safety_layer_v0_1.md",
]

SCORE_FILE_ARG_RE = re.compile(r"--score-file\s+([^\s\\]+)")


@pytest.mark.parametrize("doc_path", CARD_EXPORT_DOCS, ids=lambda p: p.name)
def test_documented_card_export_score_file_exists_and_exports_cleanly(
    doc_path: Path, tmp_path: Path
) -> None:
    text = doc_path.read_text(encoding="utf-8")
    matches = SCORE_FILE_ARG_RE.findall(text)
    assert matches, f"No --score-file argument found in {doc_path.relative_to(ROOT)}"

    for raw_score_path in matches:
        score_path = (ROOT / raw_score_path).resolve()
        assert score_path.is_file(), (
            f"{doc_path.relative_to(ROOT)} points at missing score file: {raw_score_path}"
        )

        out_json = tmp_path / "card.json"
        out_md = tmp_path / "card.md"
        out_hf = tmp_path / "hf_card.md"
        result = subprocess.run(
            [
                sys.executable,
                str(EXPORT_SCRIPT),
                "--score-file",
                raw_score_path,
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
                "--out-hf-card",
                str(out_hf),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["schema_version"] == "safetyguard_transparency_card_v0_1"
        assert payload["item_count"] > 0
        assert out_md.read_text(encoding="utf-8").strip()
        assert out_hf.read_text(encoding="utf-8").strip()


def test_usage_walkthrough_runs_offline_and_matches_case_counts(tmp_path: Path) -> None:
    en_files = [
        ROOT / "failure_atlas" / "public" / "case_intake_examples_v0_1.jsonl",
        ROOT / "failure_atlas" / "public" / "case_intake_expansion_cardio_emerg_endo_v0_1.jsonl",
        ROOT / "failure_atlas" / "public" / "case_intake_expansion_neuro_nephro_gi_obgyn_geri_v0_1.jsonl",
    ]
    tr_files = [
        ROOT / "tr_medllm_safetybench" / "synthetic_risk_pack_v0_1.jsonl",
        ROOT / "tr_medllm_safetybench" / "turkish_case_set_v1_20260705.jsonl",
    ]
    expected_en = sum(
        1
        for f in en_files
        for line in f.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    expected_tr = sum(
        1
        for f in tr_files
        for line in f.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )

    result = subprocess.run(
        [sys.executable, str(WALKTHROUGH_SCRIPT)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert f"English synthetic cases: {expected_en}" in result.stdout
    assert f"Turkish synthetic cases:  {expected_tr}" in result.stdout
    assert f"Total:                    {expected_en + expected_tr}" in result.stdout
    assert "Case ID:         FAI011" in result.stdout
    assert "verdict:              pass" in result.stdout
