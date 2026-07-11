from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from adapters.lm_eval.medfailbench_safety_layer_metrics import process_results


DATASET_PATH = Path(__file__).with_name("medfailbench_safety_layer_dataset_v0_1.jsonl")

try:
    from inspect_ai import task
    from inspect_ai.scorer import Score, mean, scorer
except ModuleNotFoundError:

    def task(function: Any) -> Any:
        return function

    def scorer(metrics: list[Any], name: str | None = None, **metadata: Any) -> Any:
        def wrapper(function: Any) -> Any:
            return function

        return wrapper

    def mean() -> None:
        return None

    class Score:  # type: ignore[no-redef]
        def __init__(self, **kwargs: Any) -> None:
            self.__dict__.update(kwargs)


def load_records(path: Path = DATASET_PATH) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError("Inspect adapter dataset rows must be JSON objects")
            records.append(record)
    return records


def build_samples(path: Path = DATASET_PATH) -> list[Any]:
    try:
        from inspect_ai.dataset import Sample
    except ModuleNotFoundError as exc:
        raise ImportError("Install inspect-ai to build Inspect samples from this local adapter.") from exc

    samples: list[Any] = []
    for record in load_records(path):
        metadata = dict(record.get("metadata", {}))
        metadata.setdefault("synthetic_only", True)
        metadata.setdefault("contains_patient_data", False)
        samples.append(
            Sample(
                id=record["id"],
                input=record["input"],
                target=record["target"],
                metadata=metadata,
            )
        )
    return samples


@scorer(metrics=[mean()])
def medfailbench_safety_scorer() -> Any:
    async def score(state: Any, target: Any) -> Any:
        metrics = process_results(
            {
                "risk_axis": state.metadata.get("risk_axis", ""),
                "metadata": state.metadata,
            },
            [state.output.completion],
        )
        return Score(
            value=metrics["medfailbench_composite"],
            answer=state.output.completion,
            explanation="Composite local safety layer score.",
            metadata=metrics,
        )

    return score


@task
def medfailbench_safety_layer(path: Path = DATASET_PATH) -> Any:
    try:
        from inspect_ai import Task
        from inspect_ai.solver import generate
    except ModuleNotFoundError as exc:
        raise ImportError("Install inspect-ai to run the MedFailBench local Inspect task wrapper.") from exc

    return Task(
        dataset=build_samples(path),
        solver=generate(),
        scorer=medfailbench_safety_scorer(),
    )


def local_record_count(path: Path = DATASET_PATH) -> int:
    return len(load_records(path))
