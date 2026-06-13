#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


BLOCKED_DIR_NAMES = {
    "__pycache__",
    "raw_outputs",
    "logs",
}

BLOCKED_SUFFIXES = {
    ".pyc",
}

def joined(*parts: str) -> str:
    return "".join(parts)


BLOCKED_TEXT_PATTERNS = [
    joined("/", "Users", "/", "goktugozkan"),
    joined("--dangerously", "-", "skip", "-", "permissions"),
    joined("de", "AI"),
    joined("human", "ized"),
    joined("submit", "_audit"),
    joined("AI", " detector"),
]

REQUIRED_FILES = [
    "README.md",
    "Makefile",
    "DATA_DICTIONARY.md",
    "DATASET_EVALUATION_CARD_V0_1_DRAFT.md",
    "PUBLIC_RELEASE_BOUNDARY_V0_1.md",
    "RELEASE_MANIFEST_V0_1_DRAFT.md",
    "CONTRIBUTING.md",
    "PUBLIC_RELEASE_CANDIDATE_STATUS.md",
    ".gitignore",
    "data/scenario_bank_v1.tsv",
    "data/scenario_bank_v2_hard_addendum.tsv",
    "data/scenario_bank_v3_scale_seed.tsv",
    "data/scenario_taxonomy_v0_2.tsv",
    "data/failure_atlas_external_sample_v0_1.jsonl",
    "data/medhelm_remote_rescue_metric_v0_1.json",
    "data/scoring_rubric_v0_1.json",
    "data/prompt_set_v2_hard_30.tsv",
    "data/prompt_set_v3_scale_30.tsv",
    "docs/clinician_evaluation_rubric.md",
    "docs/MEDHELM_REMOTE_RESCUE_BOUNDARY_METRIC_PACKAGE_DRAFT.md",
    "docs/MEDMARKS_COMPATIBILITY_DRAFT.md",
    "docs/scoring_model_v0_1.md",
    "scripts/validate_external_sample_jsonl.py",
    "scripts/validate_medhelm_metric_json.py",
    "scripts/validate_model_run_json.py",
    "scripts/validate_scoring_rubric_v0_1.py",
    "scripts/validate_public_release.py",
    "scripts/run_prompt_set_openai_compatible_v2.py",
    "scripts/run_prompt_set_hf_transformers_v2.py",
]

STRICT_REQUIRED_FILES = [
    "LICENSE",
    "CITATION.cff",
]


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in {
        "",
        ".cff",
        ".csv",
        ".json",
        ".jsonl",
        ".md",
        ".py",
        ".toml",
        ".tsv",
        ".txt",
        ".yml",
        ".yaml",
    }


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_jsonl(path: Path, errors: list[str]) -> None:
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(errors, f"{path}: line {line_number} invalid JSON: {exc}")
            continue
        if row.get("contains_patient_data") is not False:
            fail(errors, f"{path}: line {line_number} contains_patient_data must be false")
        if row.get("not_for_clinical_use") is not True:
            fail(errors, f"{path}: line {line_number} not_for_clinical_use must be true")


def validate(root: Path, strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not root.exists():
        return [f"Release candidate path does not exist: {root}"], warnings

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).exists():
            fail(errors, f"Missing required public candidate file: {relative_path}")

    if strict:
        for relative_path in STRICT_REQUIRED_FILES:
            if not (root / relative_path).exists():
                fail(errors, f"Strict release blocker: missing {relative_path}")
    else:
        for relative_path in STRICT_REQUIRED_FILES:
            if not (root / relative_path).exists():
                warnings.append(f"Draft blocker remains before public release: missing {relative_path}")

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if path.is_dir() and path.name in BLOCKED_DIR_NAMES:
            fail(errors, f"Blocked directory present: {relative}")
            continue
        if path.is_file() and path.suffix in BLOCKED_SUFFIXES:
            fail(errors, f"Blocked bytecode file present: {relative}")
        if path.is_file() and is_text_file(path):
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in BLOCKED_TEXT_PATTERNS:
                if pattern in text:
                    fail(errors, f"Blocked text pattern {pattern!r} found in {relative}")

    external_sample = root / "data" / "failure_atlas_external_sample_v0_1.jsonl"
    if external_sample.exists():
        validate_jsonl(external_sample, errors)

    medhelm_metric = root / "data" / "medhelm_remote_rescue_metric_v0_1.json"
    if medhelm_metric.exists():
        metric = json.loads(medhelm_metric.read_text(encoding="utf-8"))
        if metric.get("contains_patient_data") is not False:
            fail(errors, "MedHELM metric contains_patient_data must be false")
        if metric.get("not_for_clinical_use") is not True:
            fail(errors, "MedHELM metric not_for_clinical_use must be true")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a sanitized public release candidate tree.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--strict", action="store_true", help="Require final LICENSE and CITATION.cff.")
    args = parser.parse_args()

    errors, warnings = validate(args.root.resolve(), args.strict)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        sys.exit(1)
    print("PASS public release sanitation")
    print(f"Warnings: {len(warnings)}")


if __name__ == "__main__":
    main()
