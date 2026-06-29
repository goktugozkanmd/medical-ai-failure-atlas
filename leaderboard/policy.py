#!/usr/bin/env python3
from __future__ import annotations

from urllib.parse import urlparse, urlunparse


MAX_MODEL_NAME_LENGTH = 120
MAX_HF_LINK_LENGTH = 240
MAX_NOTES_LENGTH = 1000
MAX_SUBMISSIONS = 100

REQUIRED_SCORE_KEYS = [
    "safety_score",
    "source_support_score",
    "clinical_boundary_score",
]

ALLOWED_STATUS = {"pending review"}

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
    if path_segments[0].lower() in {"datasets", "spaces"}:
        raise ValueError("HuggingFace link must point to a model repo, not a dataset or Space.")
    if len(path_segments) > 2:
        raise ValueError(
            "HuggingFace link must point to a model repo path like "
            "https://huggingface.co/org/model."
        )

    normalized_path = "/" + "/".join(path_segments)
    return urlunparse(("https", "huggingface.co", normalized_path, "", "", ""))


def forbidden_public_claim_phrase(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    lower = value.lower()
    for phrase in FORBIDDEN_PUBLIC_CLAIM_PHRASES:
        if phrase in lower:
            return phrase
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
