#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "label_audit" / "PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md"
TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "label_audit_review.yml"

REQUIRED_GUIDE_PHRASES = [
    "Label audit public contributor issue guide",
    "synthetic data quality and label audit review examples",
    "not proof of dataset quality",
    "not clinical advice",
    "not patient data",
    "not raw model output release",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not an institutional or national program endorsement",
    ".github/ISSUE_TEMPLATE/label_audit_review.yml",
    "Audit surface",
    "Synthetic audit example",
    "Suggested reviewer role",
    "Exact boundary to review",
    "Proposed public action",
    "Required checks",
    "docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md",
    "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
    "DATASET_EVALUATION_CARD_V0_1_DRAFT.md",
    "DATA_DICTIONARY.md",
    "docs/LABEL_DEFINITION_LOCK_V0_1.md",
    "docs/LABELING_PACKAGE_INDEX_V0_1.md",
    "synthetic_provenance",
    "patient_data_absence",
    "label_lock_match",
    "pilot_subset_framing",
    "raw_output_exclusion",
    "public_release_boundary",
    "dataset_quality_proof_boundary",
    "No dataset quality proof",
    "Label audit example intake rows",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    "5 synthetic label audit examples",
]

REQUIRED_TEMPLATE_PHRASES = [
    "Label audit review",
    "labels: [\"label audit\", \"data quality\"]",
    "synthetic examples only",
    "does not verify dataset quality",
    "audit_surface",
    "synthetic_audit_example",
    "reviewer_role",
    "exact_boundary_to_review",
    "proposed_public_action",
    "required_checks",
    "Synthetic provenance reviewer",
    "Label definition reviewer",
    "Pilot subset reviewer",
    "Public release boundary reviewer",
    "This is synthetic and contains no patient data.",
    "This does not include raw model outputs or private benchmark content.",
    "This does not claim dataset quality is proven.",
    "No external action has been executed.",
    "Outward use is not allowed without maintainer review.",
    "This is not clinical advice and not a clinical validation claim.",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "official approval",
    "official acceptance",
    "sandbox access granted",
    "institutional endorsement",
    "real patient data used",
    "model is safe",
    "best model",
    "proves data quality",
]


def check_text(path: Path, required_phrases: list[str], errors: list[str]) -> str:
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
    guide_text = check_text(GUIDE, REQUIRED_GUIDE_PHRASES, errors)
    template_text = check_text(TEMPLATE, REQUIRED_TEMPLATE_PHRASES, errors)

    for relative_path in [
        ".github/ISSUE_TEMPLATE/label_audit_review.yml",
        "docs/LABEL_AUDIT_REVIEWER_ROLE_TABLE_V0_1.md",
        "docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md",
        "DATASET_EVALUATION_CARD_V0_1_DRAFT.md",
        "DATA_DICTIONARY.md",
        "docs/LABEL_DEFINITION_LOCK_V0_1.md",
        "docs/LABELING_PACKAGE_INDEX_V0_1.md",
        "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    ]:
        if relative_path not in guide_text and relative_path not in template_text:
            errors.append(f"Missing public route reference: {relative_path}")
        if not (ROOT / relative_path).exists():
            errors.append(f"Referenced file does not exist: {relative_path}")

    if errors:
        print("FAIL label audit public contributor issue validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit public contributor issue validation")
    print(f"guide={GUIDE.relative_to(ROOT)}")
    print(f"template={TEMPLATE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
