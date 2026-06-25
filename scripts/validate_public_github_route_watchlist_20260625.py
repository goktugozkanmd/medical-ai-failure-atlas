#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "PUBLIC_GITHUB_ROUTE_WATCHLIST_20260625.md"
DATA = ROOT / "docs" / "public_github_route_watchlist_20260625.json"

REQUIRED_DOC_PHRASES = [
    "Public GitHub Route Watchlist",
    "It records public GitHub state only.",
    "No public write action was taken during this check.",
    "The AI Alliance issue 50",
    "wait. Do not add a visibility comment.",
    "Hugging Face lighteval pull request 1272",
    "Live review state: review required.",
    "Live merge state: blocked.",
    "UK Government inspect ai pull request 4343",
    "Live merge state: behind.",
    "no comments or reviews found in the live pull request metadata.",
    "Medical AI Failure Atlas issue 154",
    "no outside comment found in the live issue list.",
    "The right next move is still build and wait",
    "Do not push a new public GitHub comment today.",
    "make public_github_route_watchlist",
    "make public_github_route_live_check",
]

REQUIRED_URLS = {
    "https://github.com/The-AI-Alliance/trust-safety-evals/issues/50",
    "https://github.com/huggingface/lighteval/pull/1272",
    "https://github.com/UKGovernmentBEIS/inspect_ai/pull/4343",
    "https://github.com/goktugozkanmd/medical-ai-failure-atlas/issues/154",
}

FORBIDDEN_PHRASES = [
    "maintainer support confirmed",
    "review complete",
    "merged contribution",
    "accepted contribution",
    "endorsement confirmed",
    "partner confirmed",
    "clinical validation complete",
    "clinical deployment ready",
    "benchmark result confirmed",
    "model ranking confirmed",
    "score certification complete",
    "payment completed",
    "terms accepted",
    "patient data used",
]

REQUIRED_FLAGS = {
    "public_write_action_taken": False,
    "contains_patient_data": False,
    "contains_private_email_text": False,
    "claims_maintainer_support": False,
    "claims_review_completion": False,
    "claims_merge": False,
    "claims_acceptance": False,
    "claims_endorsement": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_benchmark_result": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
}

EXPECTED_ROUTE_IDS = {
    "ai_alliance_issue_50",
    "lighteval_pr_1272",
    "inspect_ai_pr_4343",
    "failure_atlas_issue_154",
}

EXPECTED_MERGE_STATES = {
    "lighteval_pr_1272": "blocked",
    "inspect_ai_pr_4343": "behind",
}


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"Missing doc: {DOC.relative_to(ROOT)}")
    if not DATA.exists():
        errors.append(f"Missing data: {DATA.relative_to(ROOT)}")

    text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    lower_text = text.lower()
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Doc contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append("Doc contains non URL hyphen character")
    urls = {match.rstrip(".,)") for match in re.findall(r"https?://\S+", text)}
    if urls != REQUIRED_URLS:
        errors.append("Doc URL set mismatch")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key in [
        "checked_after_reading_baglam2",
        "checked_gmail_before_build",
        "checked_linkedin_tracker_before_build",
        "checked_local_repository_before_build",
        "checked_public_github_before_build",
    ]:
        if payload.get(key) is not True:
            errors.append(f"Expected {key} to be true")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    routes = payload.get("routes", [])
    if len(routes) != 4:
        errors.append("Expected four watch routes")
    route_ids = {route.get("id") for route in routes}
    if route_ids != EXPECTED_ROUTE_IDS:
        errors.append("Route id set mismatch")
    route_urls = {route.get("url") for route in routes}
    if route_urls != REQUIRED_URLS:
        errors.append("Route URL set mismatch")
    for route in routes:
        if route.get("live_state") != "open":
            errors.append(f"Route {route.get('id')} expected open state")
        if not route.get("current_action"):
            errors.append(f"Route {route.get('id')} missing current action")
        if not route.get("allowed_next_action"):
            errors.append(f"Route {route.get('id')} missing allowed next action")
        if not route.get("blocked_claims"):
            errors.append(f"Route {route.get('id')} missing blocked claims")
        expected_merge_state = EXPECTED_MERGE_STATES.get(route.get("id"))
        if expected_merge_state and route.get("merge_state") != expected_merge_state:
            errors.append(
                f"Route {route.get('id')} expected merge state {expected_merge_state}"
            )

    if len(payload.get("routing_decision", [])) != 5:
        errors.append("Expected five routing decisions")

    if errors:
        print("FAIL public GitHub route watchlist validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS public GitHub route watchlist validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"routes={len(routes)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
