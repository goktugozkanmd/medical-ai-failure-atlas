#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDHELM = ROOT / "docs" / "MEDHELM_BOUNDARY_NOTE_V0_1.md"
MEDMARKS = ROOT / "docs" / "MEDMARKS_BOUNDARY_NOTE_V0_1.md"

REQUIRED_MEDHELM_PHRASES = [
    "MedHELM official site: https://medhelm.org/",
    "MedHELM GitHub: https://github.com/PacificAI/medhelm",
    "121 clinical tasks",
    "22 subcategories",
    "31 datasets",
    "5 categories",
    "accuracy, calibration, robustness, and writing style",
    "MedHELM oriented boundary note",
    "mapping toward MedHELM style workflow categories",
    "No compatibility claim",
    "No patient data",
    "No model ranking",
    "No clinical validation",
]

REQUIRED_MEDMARKS_PHRASES = [
    "Medmarks GitHub: https://github.com/MedARC-AI/Medmarks",
    "Medmarks technical report: https://arxiv.org/html/2605.01417v1",
    "30 open source benchmarks",
    "benchmark performance is not equivalent to clinical competence",
    "Medmarks style local proof pack",
    "open ended safety wording probe",
    "local dry run planning without endpoint calls",
    "No model endpoint call",
    "No judge endpoint call",
    "No model ranking",
    "No clinical validation",
    "No compatibility claim",
]

REQUIRED_LOCAL_FILES = [
    "data/failure_atlas_external_sample_v0_1.jsonl",
    "data/medhelm_remote_rescue_metric_v0_1.json",
    "medmarks_candidate_env_v1_20260614/VALIDATION_REPORT.md",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/STAGING_MANIFEST.md",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated benchmark",
    "safe for clinical use",
    "deployment ready",
    "official approval",
    "regulatory compliance",
    "sandbox access granted",
    "institutional endorsement",
    "real patient data used",
    "benchmark equivalent",
    "accepted environment",
    "accepted metric",
    "model is safe",
]


def check_file(path: Path, required_phrases: list[str], errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing file: {path.relative_to(ROOT)}")
        return ""
    text = path.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in required_phrases:
        if phrase.lower() not in lower_text:
            errors.append(f"{path.relative_to(ROOT)} missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"{path.relative_to(ROOT)} forbidden phrase present: {phrase}")
    return text


def main() -> int:
    errors: list[str] = []
    medhelm_text = check_file(MEDHELM, REQUIRED_MEDHELM_PHRASES, errors)
    medmarks_text = check_file(MEDMARKS, REQUIRED_MEDMARKS_PHRASES, errors)
    combined_text = f"{medhelm_text}\n{medmarks_text}"

    for relative_path in REQUIRED_LOCAL_FILES:
        if relative_path not in combined_text:
            errors.append(f"Missing local file reference in boundary notes: {relative_path}")
        if not (ROOT / relative_path).exists():
            errors.append(f"Referenced local file does not exist: {relative_path}")

    if errors:
        print("FAIL boundary notes validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS boundary notes validation")
    print(f"medhelm={MEDHELM.relative_to(ROOT)}")
    print(f"medmarks={MEDMARKS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
