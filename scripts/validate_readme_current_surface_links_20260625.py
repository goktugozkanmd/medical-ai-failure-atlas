#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

SECTION_TITLE = "2026 06 25 public route and report hygiene surfaces"

REQUIRED_LINKS = {
    "docs/HEALTH_AI_ASSURANCE_OPPORTUNITY_RADAR_20260625.md",
    "docs/TEKNOFEST_HEALTH_AI_REPORT_CLAIM_HYGIENE_CHECKLIST_20260625.md",
    "docs/AI_ALLIANCE_MEDHELM_FOLLOW_UP_PREP_20260625.md",
    "docs/PUBLIC_GITHUB_ROUTE_WATCHLIST_20260625.md",
    "docs/PUBLIC_VISIBILITY_CLAIM_GATE_20260625.md",
    "docs/PUBLIC_REVIEW_OPERATING_SYSTEM_20260625.md",
    "docs/REPO_ACCELERATION_NORTH_STAR_20260625.md",
    "docs/CLINICIAN_SEVERITY_LAYER_SEED_ROWS_20260625.md",
    "docs/MEDICAL_AI_FIELD_COMMAND_PLAN_20260625.md",
    "docs/TURKISH_INTERNAL_MEDICINE_SAFETY_EVAL_V0_1_20260625.md",
    "docs/CLINICAL_INTELLIGENCE_STACK_MANIFESTO_20260625.md",
    "docs/CLINICAL_STATE_LANGUAGE_V0_1_20260625.md",
    "docs/CLINICAL_TRAJECTORY_ENGINE_V0_1_20260625.md",
    "docs/MEDICAL_REASONING_VERIFIER_V0_1_20260625.md",
    "docs/AGENTIC_MEDICINE_SANDBOX_V0_1_20260625.md",
    "docs/CLINICAL_INTELLIGENCE_STACK_GLOBAL_TARGET_MAP_20260625.md",
    "scripts/validate_clinical_state_language_v0_1.py",
    "data/clinical_trajectory_engine_transition_fixtures_v0_1_20260625.jsonl",
    "scripts/score_medical_reasoning_verifier_v0_1.py",
    "data/agentic_medicine_sandbox_event_fixtures_v0_1_20260625.jsonl",
    "docs/MEDICAL_INTELLIGENCE_ATLAS_V0_1_20260625.md",
    "docs/medical_intelligence_atlas_coverage_dashboard.md",
    "data/medical_intelligence_atlas_release_gate_v0_1_20260625.json",
    "docs/MULTILINGUAL_MEDICAL_INTELLIGENCE_SOURCE_CHECK_V0_1_20260625.md",
    "data/multilingual_medical_intelligence_paired_state_examples_v0_1_20260625.jsonl",
    "data/multilingual_medical_intelligence_source_check_index_v0_1_20260625.json",
    "scripts/validate_multilingual_medical_intelligence_paired_state_examples_v0_1_20260625.py",
    "docs/MULTILINGUAL_MEDICAL_INTELLIGENCE_PUBLIC_WORDING_BANK_V0_1_20260625.md",
    "data/multilingual_medical_intelligence_public_wording_index_v0_1_20260625.json",
    "scripts/validate_multilingual_medical_intelligence_public_wording_bank_v0_1_20260625.py",
}

REQUIRED_PHRASES = [
    "Current public navigation for the latest medical AI intelligence work",
    "without application, partner, device, clinical validation, or compliance claims",
    "ten gate checklist for safer project report language",
    "keeps acknowledgement separate from endorsement",
    "The AI Alliance issue 50",
    "lighteval pull request 1272",
    "inspect ai pull request 4343",
    "Before using any route state in public text",
    "make public_github_route_preflight",
    "live GitHub route state",
    "public post, comment, outreach, and reply text gate",
    "from turning into endorsement, acceptance, validation, or deployment claims",
    "generated public review flow",
    "one artifact per loop",
    "generated repo direction system",
    "clinician severity layer",
    "source support layer",
    "claim hygiene layer",
    "Turkish clinical context layer",
    "open source eval bridge",
    "72 hour queue",
    "ten generated seed rows",
    "clinical severity",
    "missing variable",
    "source support gap",
    "safe rewrite",
    "reviewer state",
    "Medical AI Field Command Plan",
    "source checked field plan",
    "FDA, WHO, IMDRF, HealthBench, MedGemma, MedHELM, AgentClinic",
    "TÜYZE, KDS, NeyimVar, TÜBİTAK, and TEKNOFEST",
    "internal medicine safety evaluation lane",
    "Turkish Internal Medicine Safety Eval v0.1",
    "generated 30 row synthetic Turkish internal medicine safety eval path",
    "v0.3 synthetic case set",
    "escalation, medication safety, laboratory interpretation, source support, and safe Turkish wording gates",
    "make internal_medicine_ai_safety_strategy",
    "Clinical Intelligence Stack Manifesto",
    "medical AI needs a clinical intelligence stack",
    "source anchors, stack layers, boundaries, and the first build command",
    "Clinical State Language v0.1",
    "patient state, timeline, missing data, hypotheses, evidence, action boundary",
    "Clinical Trajectory Engine v0.1",
    "twenty synthetic trajectory seed rows across clinical domains",
    "Medical Reasoning Verifier v0.1",
    "state completeness, timeline tracking, missing variable discipline",
    "Agentic Medicine Sandbox v0.1",
    "patient, clinician, test, source support, consultant, and follow up agents",
    "make clinical_intelligence_stack",
    "Clinical Intelligence Stack Global Target Map",
    "source anchored distribution map for reasoning model teams",
    "health benchmark builders, health foundation model developers",
    "Türkiye health AI decision ecosystem, and national technology circles",
    "make clinical_intelligence_stack_global_target_map",
    "Clinical State Language validator",
    "dependency free validator and normalizer",
    "canonical fixture output",
    "Clinical Trajectory Engine transition fixtures",
    "five synthetic trajectories with fifteen states and ten explicit transitions",
    "red flag, and action boundary checks",
    "Medical Reasoning Verifier scorer",
    "deterministic scorer for seven synthetic examples",
    "state completeness, timeline tracking, missing variable discipline",
    "uncertainty handling, action sequencing, source support, and forbidden claim avoidance",
    "Agentic Medicine Sandbox event fixtures",
    "three synthetic event flow scenarios",
    "patient simulator, clinician reasoner, test result emitter, source support checker, consultant simulator, and follow up monitor agents",
    "Medical Intelligence Atlas v0.1",
    "machine readable repo construction map",
    "build nodes, validators, risk gates, release states, and exact next builds",
    "Medical Intelligence Atlas Coverage Dashboard",
    "maps twelve atlas nodes to local runtime artifacts",
    "validators, coverage focus, and open gap state",
    "Medical Intelligence Atlas Release Gate",
    "release gate for six Clinical Intelligence Stack layers",
    "synthetic boundary flags, source check state, and exact next action",
    "Multilingual Medical Intelligence Source Check",
    "paired Turkish English synthetic state check",
    "language ambiguity, missing data preservation, action boundary preservation",
    "source support preservation",
    "Multilingual Medical Intelligence paired state examples",
    "six paired Turkish English synthetic state rows",
    "emergency, medication safety, chronic disease, pregnancy, laboratory interpretation, and follow up contexts",
    "Multilingual Medical Intelligence source check index",
    "repo local synthetic pair evidence, boundary flags, ready status, and exact next action",
    "Multilingual Medical Intelligence paired state validator",
    "six pairs, twelve states, boundary flags, cross language checks",
    "private identifier absence, and forbidden claim absence",
    "Multilingual Medical Intelligence Public Wording Bank",
    "eight synthetic Turkish English public wording rows",
    "plain clinical language, missing data, source support, and action boundaries",
    "without diagnosis or treatment instruction",
    "Multilingual Medical Intelligence public wording index",
    "source pair coverage, boundary flags, validation command, ready status, and next build",
    "Multilingual Medical Intelligence public wording validator",
    "all six paired source state examples",
    "ASCII Turkish wording, private identifier absence, URL absence, forbidden claim absence, and patient facing instruction absence",
    "make medical_intelligence_atlas",
    "make multilingual_medical_intelligence_source_check",
    "make multilingual_medical_intelligence_public_wording_bank",
    "multilingual paired state source checks, public wording bank checks, and exact next action state",
    "public navigation and claim hygiene materials only",
    "not submissions, applications, merge decisions",
]

FORBIDDEN_SECTION_PHRASES = [
    "application submitted",
    "partner confirmed",
    "official role granted",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used",
    "benchmark compatible",
    "score certified",
    "fda authorized",
    "eu compliant",
    "chai certified",
    "medhelm partner",
    "healthbench partner",
    "bridge partner",
    "teknofest finalist",
    "terms accepted",
    "payment completed",
    "accepted contribution",
    "merged contribution",
    "endorsement confirmed",
]


def extract_section(text: str, title: str) -> str:
    pattern = rf"^## {re.escape(title)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    return match.group(0) if match else ""


def main() -> int:
    errors: list[str] = []
    if not README.exists():
        errors.append("Missing README.md")
        section = ""
    else:
        text = README.read_text(encoding="utf-8")
        section = extract_section(text, SECTION_TITLE)

    if not section:
        errors.append(f"README missing section: {SECTION_TITLE}")

    lower_section = section.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_section:
            errors.append(f"Section missing required phrase: {phrase}")

    for link in REQUIRED_LINKS:
        if link not in section:
            errors.append(f"Section missing required link: {link}")
        if not (ROOT / link).exists():
            errors.append(f"Linked file missing: {link}")

    for phrase in FORBIDDEN_SECTION_PHRASES:
        if phrase in lower_section:
            errors.append(f"Section contains forbidden phrase: {phrase}")

    if errors:
        print("FAIL README current surface links validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS README current surface links validation")
    print(f"section={SECTION_TITLE}")
    print(f"links={len(REQUIRED_LINKS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
