#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


BLOCKED_DIR_NAMES = {
    "__pycache__",
    "raw_outputs",
    "logs",
    "results",
    "review_forms",
}

BLOCKED_SUFFIXES = {
    ".pyc",
}

VCS_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
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
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
    "docs/MEDHELM_BOUNDARY_NOTE_V0_1.md",
    "docs/MEDMARKS_BOUNDARY_NOTE_V0_1.md",
    "docs/ASSURANCE_CARD_TEMPLATE_V0_1.md",
    "docs/assurance_card_template_v0_1.json",
    ".gitignore",
    "data/scenario_bank_v1.tsv",
    "data/scenario_bank_v2_hard_addendum.tsv",
    "data/scenario_bank_v3_scale_seed.tsv",
    "data/scenario_taxonomy_v0_2.tsv",
    "data/failure_atlas_external_sample_v0_1.jsonl",
    "data/medhelm_remote_rescue_metric_v0_1.json",
    "data/scoring_rubric_v0_1.json",
    "data/inter_rater_review_subset_v0_1.tsv",
    "data/prompt_set_v1.tsv",
    "data/prompt_set_v2_hard_30.tsv",
    "data/prompt_set_v3_scale_30.tsv",
    "docs/clinician_evaluation_rubric.md",
    "docs/MEDHELM_REMOTE_RESCUE_BOUNDARY_METRIC_PACKAGE_DRAFT.md",
    "docs/MEDMARKS_COMPATIBILITY_DRAFT.md",
    "docs/scoring_model_v0_1.md",
    "failure_atlas/public/INDEX.md",
    "failure_atlas/public/METHODOLOGY.md",
    "scripts/validate_external_sample_jsonl.py",
    "scripts/validate_medhelm_metric_json.py",
    "scripts/validate_model_run_json.py",
    "scripts/validate_scoring_rubric_v0_1.py",
    "scripts/validate_failure_atlas_public_summary_v0_1.py",
    "scripts/validate_health_data_quality_card_v0_1.py",
    "scripts/validate_boundary_notes_v0_1.py",
    "scripts/validate_assurance_card_template_v0_1.py",
    "scripts/validate_public_release.py",
    "scripts/run_prompt_set_openai_compatible_v2.py",
    "scripts/run_prompt_set_hf_transformers_v2.py",
    "medmarks_candidate_env_v1_20260614/VALIDATION_REPORT.md",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/STAGING_MANIFEST.md",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/configs/failure_atlas_safety_wording_30case_smoke.toml",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/failure_atlas_safety_wording.py",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/judge_prompts.py",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/pyproject.toml",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/data/failure_atlas_medmarks_30_case_seed_v0_1.jsonl",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/docs/MEDMARKS_FAILURE_PROBE_SET_DATASHEET_V0_1.md",
    "medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/environments/failure_atlas_safety_wording/docs/MEDMARKS_FAILURE_PROBE_TAXONOMY_V0_1.md",
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


def count_tsv_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle, delimiter="\t"))


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
        if relative.parts and relative.parts[0] in VCS_DIR_NAMES:
            continue
        if relative.parts and relative.parts[0] == "review_forms":
            fail(errors, f"Internal review form path present in public candidate: {relative}")
            continue
        if relative.parts and relative.parts[0] == "results":
            fail(errors, f"Internal result path present in public candidate: {relative}")
            continue
        if len(relative.parts) >= 2 and relative.parts[0] == "docs" and path.name.startswith("HEALTHBENCH_"):
            fail(errors, f"Internal HealthBench workflow doc present in public candidate: {relative}")
            continue
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

    readme = root / "README.md"
    readme_text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    if readme.exists():
        if "failure_atlas/public/INDEX.md" not in readme_text:
            fail(errors, "README must link to failure_atlas/public/INDEX.md")
        if "failure_atlas/public/METHODOLOGY.md" not in readme_text:
            fail(errors, "README must link to failure_atlas/public/METHODOLOGY.md")
        if "Raw model outputs and logs are not included" not in readme_text:
            fail(errors, "README must state that raw model outputs and logs are not included")

    prompt_files = [
        root / "data" / "prompt_set_v1.tsv",
        root / "data" / "prompt_set_v2_hard_30.tsv",
        root / "data" / "prompt_set_v3_scale_30.tsv",
    ]
    if all(path.exists() for path in prompt_files):
        prompt_rows = sum(count_tsv_rows(path) for path in prompt_files)
        if prompt_rows != 70:
            fail(errors, f"Public prompt set count must be 70 rows, found {prompt_rows}")
        if readme.exists() and "70 row prompt set" not in readme_text:
            fail(errors, "README must describe the public prompt set count as 70 rows")

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
