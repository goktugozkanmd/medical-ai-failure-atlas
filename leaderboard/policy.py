#!/usr/bin/env python3
from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse


MAX_MODEL_NAME_LENGTH = 120
MAX_HF_LINK_LENGTH = 240
MAX_NOTES_LENGTH = 1000
MAX_SUBMISSIONS = 100
SUBMISSION_ID_PATTERN = re.compile(r"^[a-f0-9]{32}$")
HF_REACHABILITY_STATUS_PATTERN = re.compile(r"^[23]\d{2}$")

ALLOWED_SUBMISSION_KEYS = {
    "id",
    "model_name",
    "huggingface_link",
    "benchmark_scores",
    "notes",
    "status",
    "submitted_at",
    "first_submitted_at",
    "huggingface_reachable",
    "huggingface_status",
}

REQUIRED_SCORE_KEYS = [
    "safety_score",
    "source_support_score",
    "clinical_boundary_score",
]

ALLOWED_STATUS = {"pending review"}

RESERVED_HF_PATH_PREFIXES = {
    "api",
    "collections",
    "datasets",
    "docs",
    "join",
    "login",
    "models",
    "new",
    "organizations",
    "pricing",
    "settings",
    "spaces",
}

FORBIDDEN_PUBLIC_CLAIM_PHRASES = [
    "clinical advice",
    "clinical validation",
    "clinically validated",
    "safe for clinical use",
    "approved for clinical use",
    "regulatory approved",
    "best model",
    "model ranking",
    "source truth certification",
    "patient data",
]

PRIVATE_DATA_PATTERNS = [
    (re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE), "email address"),
    (re.compile(r"\b(?:\+?\d[\s().-]*){10,}\b"), "phone or long numeric identifier"),
    (
        re.compile(r"\b(?:github_pat|ghp|gho|ghu|ghs|ghr|hf)_[A-Za-z0-9_]{20,}\b"),
        "credential-like token",
    ),
    (re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"), "credential-like token"),
    (re.compile(r"\bbearer\s+[A-Za-z0-9._~+/=-]{16,}\b", re.IGNORECASE), "credential-like token"),
    (
        re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
        "credential-like token",
    ),
    (
        re.compile(
            r"\b(?:api[_\s-]?key|access[_\s-]?token|secret|password)"
            r"\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}",
            re.IGNORECASE,
        ),
        "credential-like token",
    ),
]


def is_valid_submission_id(value: object) -> bool:
    return isinstance(value, str) and bool(SUBMISSION_ID_PATTERN.fullmatch(value))


def normalize_huggingface_model_url(link: str | None) -> str:
    candidate = (link or "").strip()
    if not candidate:
        raise ValueError("HuggingFace link is required.")
    if len(candidate) > MAX_HF_LINK_LENGTH:
        raise ValueError(f"HuggingFace link must be {MAX_HF_LINK_LENGTH} characters or fewer.")
    if "://" not in candidate:
        candidate = f"https://{candidate}"

    parsed = urlparse(candidate)
    host = parsed.netloc.lower()
    if parsed.scheme != "https" or host not in {"huggingface.co", "www.huggingface.co"}:
        raise ValueError("HuggingFace link must start with https://huggingface.co/.")

    path_segments = [segment for segment in parsed.path.split("/") if segment]
    if not path_segments:
        raise ValueError("HuggingFace link must include a model path.")
    if path_segments[0].lower() in RESERVED_HF_PATH_PREFIXES:
        raise ValueError("HuggingFace link must point to a model repo, not a site page, dataset, or Space.")
    if len(path_segments) > 2:
        raise ValueError(
            "HuggingFace link must point to a model repo path like "
            "https://huggingface.co/org/model."
        )

    normalized_path = "/" + "/".join(path_segments)
    normalized = urlunparse(("https", "huggingface.co", normalized_path, "", "", ""))
    if len(normalized) > MAX_HF_LINK_LENGTH:
        raise ValueError(f"HuggingFace link must be {MAX_HF_LINK_LENGTH} characters or fewer.")
    return normalized


def forbidden_public_claim_phrase(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    lower = value.lower()
    for phrase in FORBIDDEN_PUBLIC_CLAIM_PHRASES:
        if phrase in lower:
            return phrase
    return None


def forbidden_private_data_pattern(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    for pattern, label in PRIVATE_DATA_PATTERNS:
        if pattern.search(value):
            return label
    return None


def coerce_score(value: object, label: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a number.")
    try:
        score = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a number.") from exc
    if not 0 <= score <= 100:
        raise ValueError(f"{label} must be between 0 and 100.")
    return round(score, 2)
