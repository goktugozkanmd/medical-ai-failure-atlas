#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "PUBLIC_RELEASE_NOTE_V0_1_20260616.md"

REQUIRED_PHRASES = [
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "19 synthetic intake rows",
    "14 Turkish synthetic risk rows",
    "10 risk axes",
    "10 of 10 Failure Atlas taxonomy pattern IDs represented",
    "6 public review states",
    "Clinician review protocol v0.1",
    "19 clinician review queue rows",
    "4 source review rows",
    "Source claim review queue v0.1",
    "12 source claim review queue rows",
    "10 SourceCheckup v0.2 answer examples",
    "11 SourceCheckup contributor examples",
    "3 red flag source locator contributor examples",
    "Health data quality and label audit card v0.1",
    "Label audit reviewer role table v0.1",
    "make label_audit_role_table",
    "4 label audit reviewer roles",
    "5 label audit escalation gate rows",
    "1 label audit public contributor issue route",
    "5 label audit example intake rows",
    "5 label audit example dashboard rows",
    "5 label audit maintainer triage rows",
    "5 label audit public wording decision rows",
    "Label audit example intake v0.1",
    "Label audit example dashboard v0.1",
    "Label audit maintainer triage board v0.1",
    "Label audit public wording decision log v0.1",
    "make label_audit_examples",
    "make label_audit_dashboard",
    "make label_audit_triage",
    "make label_audit_wording_log",
    "synthetic label audit example intake rows for provenance, label definition, pilot subset, raw output exclusion, and dataset quality proof boundaries",
    "compact label audit example dashboard that summarizes role, audit row, review state, and blocked public claim type",
    "label audit maintainer triage board that turns dashboard rows into maintainer actions and public wording decisions",
    "label audit public wording decision log that records blocked wording and proposed public wording",
    "Label audit public contributor issue guide v0.1",
    "make label_audit_public_issue",
    "public label audit contributor issue route for synthetic data quality and label audit review examples",
    "Label audit reviewer role table that assigns provenance, label definition, pilot subset, and public release boundary review roles",
    "Label audit escalation gate rows for synthetic provenance, label definition lock, pilot inter rater subset, raw output exclusion, and public release boundaries",
    "150 synthetic scenario rows",
    "70 prompt rows",
    "24 pilot inter rater rows",
    "MedHELM and Medmarks boundary notes v0.1",
    "Medical language model assurance card template v0.1",
    "Assurance card template for intended use, risk, source support, human review, and release gate boundaries",
    "SourceCheckup public contributor issue route v0.1",
    "make sourcecheckup_public_issue",
    "public SourceCheckup contributor issue route for synthetic source claim review examples",
    "SourceCheckup source claim example expansion v0.2",
    "make sourcecheckup_expansion_dashboard",
    "generated SourceCheckup expansion dashboard",
    "6 clinician literacy release gate lessons",
    "Clinician literacy release gate lesson map v0.1",
    "make clinician_literacy_map",
    "clinician literacy lesson map that connects Failure Atlas, TR MedLLM, SourceCheckup, assurance gates, and clinician review states",
    "6 assurance release gate examples",
    "Assurance release gate example map v0.1",
    "make assurance_release_gate_map",
    "generated assurance release gate map that connects public examples to assurance card sections and release gate levels",
    "7 SourceCheckup TR MedLLM assurance routes",
    "SourceCheckup TR MedLLM assurance routing map v0.1",
    "make sourcecheckup_tr_medllm_routing",
    "SourceCheckup TR MedLLM assurance routing map that connects 12 source claim queue rows, 14 Turkish synthetic risk rows, and six assurance release gate examples",
    "generated SourceCheckup TR MedLLM assurance routing map that links source surfaces, risk axes, release gate levels, and blocked public wording",
    "2 source review worksheets",
    "Source review worksheets v0.1",
    "make source_review_worksheets",
    "Source review worksheets that turn medication safety and policy wording routes into concrete public review questions",
    "Source review worksheets for medication safety and policy wording without source truth certification or clinical claims",
    "3 red flag warning checklists",
    "4 warning sign reviewer roles",
    "5 escalation gate audit rows",
    "Red flag source locator and warning sign checklist v0.1",
    "make red_flag_warning_checklist",
    "Red flag source locator and warning sign checklist that turns false reassurance, rare danger, and source locator risks into public review steps",
    "Red flag warning checklists for partial negative evidence, symptom fluctuation, and source locator triage claims",
    "Warning sign reviewer role table v0.1",
    "make warning_sign_role_table",
    "Warning sign reviewer role table that assigns clinician, source locator, warning sign wording, and adjudication roles",
    "Escalation gate audit rows for partial negative evidence, symptom fluctuation, source locator triage claims, public wording boundaries, and reviewer disagreement",
    "Red flag source locator contributor examples v0.1",
    "make red_flag_contributor_examples",
    "Red flag source locator contributor examples that turn unsafe red flag wording into SourceCheckup contribution rows",
    "Red flag contributor examples for PMID locator misuse, broad source reassurance, and warning sign placement",
    "Six platform dashboard index v0.1",
    "docs/PLATFORM_DASHBOARD_INDEX_V0_1.md",
    "make platform_dashboard",
    "public dashboard entry point that links the six seed platforms and their runnable checks",
    "TR MedLLM specialty spread dashboard v0.1",
    "make tr_medllm_specialty_dashboard",
    "generated specialty spread dashboard for multilingual medical AI safety benchmark growth",
]

FORBIDDEN_PHRASES = [
    "validated for clinical use",
    "safe for clinical use",
    "approved by",
    "official acceptance",
    "regulatory approval",
    "model is safe",
    "best model",
    "patient data used",
]


def main() -> int:
    errors: list[str] = []
    if not NOTE.exists():
        errors.append(f"Missing release note: {NOTE}")
        text = ""
    else:
        text = NOTE.read_text(encoding="utf-8")
    lower_text = text.lower()

    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")

    if "```bash" not in text:
        errors.append("Release note should include runnable command block")

    if errors:
        print("FAIL public release note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS public release note validation")
    print(f"file={NOTE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
