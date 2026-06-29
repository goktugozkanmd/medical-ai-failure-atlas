from __future__ import annotations

import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol
from urllib import error, request

from failure_atlas.data import PathLike, PromptItem, load_prompt_set


class ModelClient(Protocol):
    def complete(self, prompt: str, config: ModelConfig) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class ModelConfig:
    name: str
    api_endpoint: str
    api_key_env: str = "OPENAI_API_KEY"
    temperature: float = 0.0
    max_tokens: int = 1024
    requests_per_minute: float = 60.0
    timeout_seconds: float = 60.0
    max_retries: int = 3
    backoff_seconds: float = 1.0
    system_prompt: str | None = None
    extra_headers: dict[str, str] = field(default_factory=dict)
    extra_body: dict[str, Any] = field(default_factory=dict)

    def api_key(self) -> str:
        value = os.getenv(self.api_key_env)
        if not value:
            raise RuntimeError(f"Missing API key: environment variable {self.api_key_env} is not set")
        return value

    def safe_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["api_key_env"] = self.api_key_env
        return value


@dataclass(frozen=True)
class RawResponseRecord:
    scenario_id: str
    prompt_text: str
    output_capture_instruction: str
    model_answer: str
    raw_response: dict[str, Any] | None
    latency_seconds: float
    attempts: int
    status: str
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BenchmarkRunResult:
    run_id: str
    model_name: str
    raw_path: Path
    responses: list[RawResponseRecord]


class RateLimiter:
    def __init__(self, requests_per_minute: float) -> None:
        self.interval = 0.0 if requests_per_minute <= 0 else 60.0 / requests_per_minute
        self.next_allowed = 0.0

    def wait(self) -> None:
        if self.interval <= 0:
            return
        now = time.monotonic()
        if now < self.next_allowed:
            time.sleep(self.next_allowed - now)
        self.next_allowed = time.monotonic() + self.interval


class OpenAICompatibleClient:
    def complete(self, prompt: str, config: ModelConfig) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": config.name,
            "messages": _messages(prompt, config.system_prompt),
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
        }
        payload.update(config.extra_body)
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {config.api_key()}",
            "Content-Type": "application/json",
            **config.extra_headers,
        }
        api_request = request.Request(config.api_endpoint, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(api_request, timeout=config.timeout_seconds) as response:
                data = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"API request failed with HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"API request failed: {exc.reason}") from exc
        parsed = json.loads(data)
        if not isinstance(parsed, dict):
            raise RuntimeError("API response must be a JSON object")
        return parsed


def run_model(
    config: ModelConfig,
    prompt_path: PathLike,
    output_dir: PathLike = Path("outputs/raw"),
    run_id: str | None = None,
    client: ModelClient | None = None,
    continue_on_error: bool = False,
) -> BenchmarkRunResult:
    prompts = load_prompt_set(prompt_path)
    active_client = client or OpenAICompatibleClient()
    active_run_id = run_id or _default_run_id()
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    limiter = RateLimiter(config.requests_per_minute)
    responses: list[RawResponseRecord] = []
    for index, prompt in enumerate(prompts, start=1):
        _log(f"[{config.name}] {index}/{len(prompts)} {prompt.scenario_id}")
        limiter.wait()
        try:
            record = _call_prompt(active_client, config, prompt)
        except Exception as exc:
            if not continue_on_error:
                raise
            record = RawResponseRecord(
                scenario_id=prompt.scenario_id,
                prompt_text=prompt.prompt_text,
                output_capture_instruction=prompt.output_capture_instruction,
                model_answer="",
                raw_response=None,
                latency_seconds=0.0,
                attempts=max(config.max_retries + 1, 1),
                status="error",
                error=str(exc),
            )
        responses.append(record)
    raw_path = target_dir / f"{active_run_id}_{slugify(config.name)}.json"
    _write_raw_run(raw_path, active_run_id, config, prompt_path, responses)
    _log(f"[{config.name}] saved {raw_path}")
    return BenchmarkRunResult(
        run_id=active_run_id,
        model_name=config.name,
        raw_path=raw_path,
        responses=responses,
    )


def run_batch(
    configs: list[ModelConfig],
    prompt_path: PathLike,
    output_dir: PathLike = Path("outputs/raw"),
    run_id: str | None = None,
    continue_on_error: bool = False,
) -> list[BenchmarkRunResult]:
    active_run_id = run_id or _default_run_id()
    results: list[BenchmarkRunResult] = []
    for config in configs:
        results.append(
            run_model(
                config=config,
                prompt_path=prompt_path,
                output_dir=output_dir,
                run_id=active_run_id,
                continue_on_error=continue_on_error,
            )
        )
    return results


def load_model_configs(path: PathLike) -> list[ModelConfig]:
    target = Path(path)
    with target.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict) and isinstance(data.get("models"), list):
        items = data["models"]
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError(f"{target} must be a JSON list or an object with a models list")
    configs: list[ModelConfig] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"{target} model entry {index} must be an object")
        configs.append(ModelConfig(**item))
    return configs


def extract_answer(payload: dict[str, Any]) -> str:
    direct = payload.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct
    choices = payload.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict):
                content = message.get("content")
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    return "".join(_content_part_text(part) for part in content).strip()
            text = first.get("text")
            if isinstance(text, str):
                return text
    raise RuntimeError("API response does not contain choices[0].message.content, choices[0].text, or output_text")


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    slug = re.sub(r"_+", "_", slug).strip("._")
    return slug or "model"


def _messages(prompt: str, system_prompt: str | None) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages


def _content_part_text(part: object) -> str:
    if isinstance(part, dict) and isinstance(part.get("text"), str):
        return part["text"]
    if isinstance(part, str):
        return part
    return ""


def _call_prompt(client: ModelClient, config: ModelConfig, prompt: PromptItem) -> RawResponseRecord:
    errors: list[str] = []
    start = time.monotonic()
    total_attempts = max(config.max_retries + 1, 1)
    for attempt in range(1, total_attempts + 1):
        try:
            raw_response = client.complete(prompt.prompt_text, config)
            answer = extract_answer(raw_response)
            return RawResponseRecord(
                scenario_id=prompt.scenario_id,
                prompt_text=prompt.prompt_text,
                output_capture_instruction=prompt.output_capture_instruction,
                model_answer=answer,
                raw_response=raw_response,
                latency_seconds=round(time.monotonic() - start, 6),
                attempts=attempt,
                status="ok",
            )
        except Exception as exc:
            errors.append(str(exc))
            if attempt >= total_attempts:
                raise RuntimeError(f"API failed after {attempt} attempts: {errors[-1]}") from exc
            delay = config.backoff_seconds * (2 ** (attempt - 1))
            _log(f"[{config.name}] retry {attempt}/{config.max_retries} after error: {errors[-1]}")
            time.sleep(delay)
    raise RuntimeError("unreachable retry state")


def _write_raw_run(
    path: Path,
    run_id: str,
    config: ModelConfig,
    prompt_path: PathLike,
    responses: list[RawResponseRecord],
) -> None:
    payload = {
        "schema_version": "failure_atlas_raw_run_v0_1",
        "run_id": run_id,
        "model_name": config.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "prompt_set": str(prompt_path),
        "config": config.safe_dict(),
        "responses": [record.to_dict() for record in responses],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _default_run_id() -> str:
    return datetime.now(timezone.utc).strftime("run_%Y%m%dT%H%M%SZ")


def _log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)
