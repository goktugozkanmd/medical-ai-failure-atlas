#!/usr/bin/env python3
"""
Chinese Frontier Model Evaluation Config for MedFailBench.
All models accessed via OpenRouter API.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

CHINESE_FRONTIER_MODELS = {
    "deepseek": {
        "deepseek-v4-flash": {
            "provider": "openrouter",
            "model_id": "deepseek/deepseek-v4-flash",
            "endpoint": OPENROUTER_ENDPOINT,
            "description": "DeepSeek V4 Flash – fastest tier",
            "priority": 1,
        },
        "deepseek-v4-pro": {
            "provider": "openrouter",
            "model_id": "deepseek/deepseek-v4-pro",
            "endpoint": OPENROUTER_ENDPOINT,
            "description": "DeepSeek V4 Pro – full capability",
            "priority": 3,
        },
    },
    "qwen": {
        "qwen-2.5-7b": {
            "provider": "openrouter",
            "model_id": "qwen/qwen-2.5-7b-instruct",
            "endpoint": OPENROUTER_ENDPOINT,
            "description": "Qwen 2.5 7B – baseline small",
            "priority": 2,
        },
        "qwen-3.6-27b": {
            "provider": "openrouter",
            "model_id": "qwen/qwen3.6-27b",
            "endpoint": OPENROUTER_ENDPOINT,
            "description": "Qwen 3.6 27B – mid-scale",
            "priority": 4,
        },
        "qwen-3.6-flash": {
            "provider": "openrouter",
            "model_id": "qwen/qwen3.6-flash",
            "endpoint": OPENROUTER_ENDPOINT,
            "description": "Qwen 3.6 Flash – fast tier",
            "priority": 6,
        },
        "qwen-3.7-plus": {
            "provider": "openrouter",
            "model_id": "qwen/qwen3.7-plus",
            "endpoint": OPENROUTER_ENDPOINT,
            "description": "Qwen 3.7 Plus – latest large",
            "priority": 8,
        },
    },
    "kimi": {
        "kimi-latest": {
            "provider": "openrouter",
            "model_id": "moonshotai/kimi-latest",
            "endpoint": OPENROUTER_ENDPOINT,
            "description": "Kimi latest – Moonshot AI",
            "priority": 5,
        },
        "kimi-k2.7-code": {
            "provider": "openrouter",
            "model_id": "moonshotai/kimi-k2.7-code",
            "endpoint": OPENROUTER_ENDPOINT,
            "description": "Kimi K2.7 Code – coding + reasoning",
            "priority": 7,
        },
    },
    "glm": {
        "glm-5.2": {
            "provider": "openrouter",
            "model_id": "z-ai/glm-5.2",
            "endpoint": OPENROUTER_ENDPOINT,
            "description": "GLM 5.2 – Zhipu AI latest",
            "priority": 9,
        },
        "glm-5-turbo": {
            "provider": "openrouter",
            "model_id": "z-ai/glm-5-turbo",
            "endpoint": OPENROUTER_ENDPOINT,
            "description": "GLM 5 Turbo – fast tier",
            "priority": 10,
        },
    },
}

PRIORITY_RUN_ORDER = [
    ("deepseek", "deepseek-v4-flash"),
    ("qwen", "qwen-2.5-7b"),
    ("deepseek", "deepseek-v4-pro"),
    ("qwen", "qwen-3.6-27b"),
    ("kimi", "kimi-latest"),
    ("qwen", "qwen-3.6-flash"),
    ("kimi", "kimi-k2.7-code"),
    ("qwen", "qwen-3.7-plus"),
    ("glm", "glm-5.2"),
    ("glm", "glm-5-turbo"),
]


def get_model_config(family: str, model: str) -> dict | None:
    return CHINESE_FRONTIER_MODELS.get(family, {}).get(model)


def get_api_key() -> str | None:
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    env_path = Path.home() / ".hermes" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None
