#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "sourcecheckup" / "sourcecheckup_repo_doctor_v0_1.json"

REQUIRED_FILES = [
    "scripts/sourcecheckup_medical.py",
    "sourcecheckup/README.md",
    "sourcecheckup/schemas/sourcecheckup_input_schema_v0_1.json",
    "sourcecheckup/examples/sourcecheckup_seed_answers.jsonl",
    "sourcecheckup/examples/source_surface_examples_v0_2.jsonl",
    "sourcecheckup/examples/sourcecheckup_contribution_examples_v0_2.jsonl",
    "sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl",
    "docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md",
    "docs/sourcecheckup/SOURCECHECKUP_TURKISH_INSTITUTIONAL_WORDING_EXAMPLES_V0_1.md",
    "sourcecheckup/build/source_claim_example_expansion_v0_2.md",
]

JSONL_EXPECTED_COUNTS = {
    "sourcecheckup/examples/sourcecheckup_seed_answers.jsonl": 4,
    "sourcecheckup/examples/source_surface_examples_v0_2.jsonl": 10,
    "sourcecheckup/examples/sourcecheckup_contribution_examples_v0_2.jsonl": 11,
    "sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl": 12,
}

COMMANDS = [
    "make sourcecheckup",
    "make sourcecheckup_v02",
    "make source_claim_queue",
    "make sourcecheckup_expansion_dashboard",
    "make sourcecheckup_turkish_institutional_wording",
]


def count_jsonl(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def main() -> int:
    checks: list[dict[str, object]] = []
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        exists = path.exists()
        checks.append({"path": relative, "exists": exists})
        if not exists:
            errors.append(f"missing {relative}")
    for relative, expected_count in JSONL_EXPECTED_COUNTS.items():
        path = ROOT / relative
        actual_count = count_jsonl(path) if path.exists() else 0
        ok = actual_count == expected_count
        checks.append(
            {
                "path": relative,
                "expected_rows": expected_count,
                "actual_rows": actual_count,
                "ok": ok,
            }
        )
        if not ok:
            errors.append(f"{relative} expected {expected_count} rows and found {actual_count}")

    payload = {
        "version": "sourcecheckup_repo_doctor_v0_1",
        "status": "pass" if not errors else "fail",
        "date": "2026 06 17",
        "required_file_count": len(REQUIRED_FILES),
        "jsonl_count_checks": len(JSONL_EXPECTED_COUNTS),
        "recommended_commands": COMMANDS,
        "contains_patient_data": False,
        "not_for_clinical_use": True,
        "no_external_calls": True,
        "no_model_calls": True,
        "checks": checks,
        "errors": errors,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if errors:
        print("FAIL SourceCheckup repo doctor")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS SourceCheckup repo doctor")
    print(f"output={OUTPUT.relative_to(ROOT)}")
    print(f"required_files={len(REQUIRED_FILES)}")
    print(f"jsonl_count_checks={len(JSONL_EXPECTED_COUNTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
