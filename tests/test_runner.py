from __future__ import annotations

from pathlib import Path
from typing import Any

from failure_atlas.runner import ModelConfig, run_model


class FlakyClient:
    def __init__(self) -> None:
        self.calls = 0

    def complete(self, prompt: str, config: ModelConfig) -> dict[str, Any]:
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("temporary failure")
        return {"choices": [{"message": {"content": f"safe response to {prompt[:8]}"}}]}


def test_runner_saves_raw_output_with_retry(tmp_path: Path) -> None:
    prompts = tmp_path / "prompts.tsv"
    prompts.write_text(
        "scenario_id\tprompt_text\toutput_capture_instruction\n"
        "T001\tPrompt one\tSave exactly\n",
        encoding="utf-8",
    )
    client = FlakyClient()
    config = ModelConfig(
        name="test-model",
        api_endpoint="https://example.test/v1/chat/completions",
        requests_per_minute=0,
        max_retries=1,
        backoff_seconds=0,
    )
    result = run_model(config=config, prompt_path=prompts, output_dir=tmp_path, run_id="run_test", client=client)
    assert result.raw_path.exists()
    assert result.responses[0].attempts == 2
    assert result.responses[0].model_answer.startswith("safe response")
