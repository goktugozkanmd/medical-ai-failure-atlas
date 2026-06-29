from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


from typing import Union
PathLike = Union[str, Path]

PROMPT_COLUMNS = ("scenario_id", "prompt_text", "output_capture_instruction")
SCENARIO_BANK_COLUMNS = (
    "scenario_id",
    "theme",
    "domain",
    "setting",
    "patient_summary",
    "task_for_model",
    "expected_safety_focus",
    "development_feedback_signal",
    "suggested_prompt_style",
)
TAXONOMY_COLUMNS = ("axis_id", "axis_type", "name", "description", "target_count")


class FailureAtlasDataError(ValueError):
    pass


class MissingDataFileError(FileNotFoundError):
    pass


class SchemaValidationError(FailureAtlasDataError):
    pass


@dataclass(frozen=True)
class PromptItem:
    scenario_id: str
    prompt_text: str
    output_capture_instruction: str
    metadata: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, str]:
        row = dict(self.metadata)
        row.update(
            {
                "scenario_id": self.scenario_id,
                "prompt_text": self.prompt_text,
                "output_capture_instruction": self.output_capture_instruction,
            }
        )
        return row


@dataclass(frozen=True)
class ScenarioRecord:
    scenario_id: str
    fields: dict[str, str]

    def to_dict(self) -> dict[str, str]:
        row = dict(self.fields)
        row["scenario_id"] = self.scenario_id
        return row


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    prompt: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class ScoringRubric:
    schema_version: str
    title: str
    safety_gates: list[dict[str, Any]]
    graded_dimensions: list[dict[str, Any]]
    decision_rules: list[dict[str, Any]]
    final_labels: list[str]
    raw: dict[str, Any]

    @property
    def gate_ids(self) -> list[str]:
        return [str(gate["gate_id"]) for gate in self.safety_gates]

    @property
    def dimension_ids(self) -> list[str]:
        return [str(dimension["dimension_id"]) for dimension in self.graded_dimensions]


def ensure_file(path: PathLike) -> Path:
    target = Path(path)
    if not target.exists():
        raise MissingDataFileError(f"Missing data file: {target}")
    if not target.is_file():
        raise MissingDataFileError(f"Expected a file but found a directory: {target}")
    return target


def load_tsv_rows(path: PathLike, required_columns: tuple[str, ...] | None = None) -> list[dict[str, str]]:
    target = ensure_file(path)
    with target.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = tuple(reader.fieldnames or ())
        if not fieldnames:
            raise SchemaValidationError(f"{target} has no header row")
        if required_columns is not None:
            _require_exact_columns(target, fieldnames, required_columns)
        rows = [dict(row) for row in reader]
    if not rows:
        raise SchemaValidationError(f"{target} has no data rows")
    for index, row in enumerate(rows, start=2):
        for key, value in row.items():
            if value is None:
                raise SchemaValidationError(f"{target}:{index} has a missing value under {key}")
    return rows


def load_jsonl_rows(path: PathLike) -> list[dict[str, Any]]:
    target = ensure_file(path)
    rows: list[dict[str, Any]] = []
    with target.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SchemaValidationError(f"{target}:{line_number} is not valid JSON: {exc.msg}") from exc
            if not isinstance(value, dict):
                raise SchemaValidationError(f"{target}:{line_number} must be a JSON object")
            rows.append(value)
    if not rows:
        raise SchemaValidationError(f"{target} has no JSONL rows")
    return rows


def load_prompt_set(path: PathLike) -> list[PromptItem]:
    target = ensure_file(path)
    rows = load_tsv_rows(target, PROMPT_COLUMNS)
    _require_unique(rows, "scenario_id", target)
    prompts: list[PromptItem] = []
    for index, row in enumerate(rows, start=2):
        scenario_id = _required_text(row, "scenario_id", target, index)
        prompt_text = _required_text(row, "prompt_text", target, index)
        output_capture_instruction = _required_text(row, "output_capture_instruction", target, index)
        metadata = {key: value for key, value in row.items() if key not in PROMPT_COLUMNS}
        prompts.append(
            PromptItem(
                scenario_id=scenario_id,
                prompt_text=prompt_text,
                output_capture_instruction=output_capture_instruction,
                metadata=metadata,
            )
        )
    return prompts


def load_scenario_bank(path: PathLike, prompt_ids: set[str] | None = None) -> list[ScenarioRecord]:
    target = ensure_file(path)
    rows = load_tsv_rows(target, SCENARIO_BANK_COLUMNS)
    _require_unique(rows, "scenario_id", target)
    records: list[ScenarioRecord] = []
    for index, row in enumerate(rows, start=2):
        scenario_id = _required_text(row, "scenario_id", target, index)
        for column in SCENARIO_BANK_COLUMNS:
            _required_text(row, column, target, index)
        records.append(ScenarioRecord(scenario_id=scenario_id, fields=dict(row)))
    if prompt_ids is not None:
        scenario_ids = {record.scenario_id for record in records}
        missing = sorted(prompt_ids - scenario_ids)
        if missing:
            raise SchemaValidationError(f"{target} is missing prompt scenario IDs: {missing[:10]}")
    return records


def load_taxonomy(path: PathLike) -> list[dict[str, str]]:
    target = ensure_file(path)
    rows = load_tsv_rows(target, TAXONOMY_COLUMNS)
    _require_unique(rows, "axis_id", target)
    return rows


def load_eval_set(path: PathLike) -> list[EvalCase]:
    target = ensure_file(path)
    rows = load_jsonl_rows(target)
    cases: list[EvalCase] = []
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        case_id = _first_text(row, ("case_id", "scenario_id", "id"), target, index)
        prompt = _first_text(row, ("prompt", "prompt_text", "turkish_prompt_seed"), target, index)
        if case_id in seen:
            raise SchemaValidationError(f"{target}:{index} duplicates case_id {case_id}")
        seen.add(case_id)
        for key in ("synthetic_only", "patient_data_used", "clinical_use_allowed", "contains_patient_data", "not_for_clinical_use"):
            if key in row and not isinstance(row[key], bool):
                raise SchemaValidationError(f"{target}:{index} field {key} must be boolean")
        if row.get("patient_data_used") is True or row.get("contains_patient_data") is True:
            raise SchemaValidationError(f"{target}:{index} contains patient data but eval sets must be synthetic or public")
        cases.append(EvalCase(case_id=case_id, prompt=prompt, raw=dict(row)))
    return cases


def load_scoring_rubric(path: PathLike) -> ScoringRubric:
    target = ensure_file(path)
    with target.open(encoding="utf-8") as handle:
        try:
            raw = json.load(handle)
        except json.JSONDecodeError as exc:
            raise SchemaValidationError(f"{target} is not valid JSON: {exc.msg}") from exc
    if not isinstance(raw, dict):
        raise SchemaValidationError(f"{target} must contain a JSON object")
    schema_version = _required_json_text(raw, "schema_version", target)
    title = str(raw.get("title", schema_version))
    safety_gates = _required_json_list(raw, "safety_gates", target)
    graded_dimensions = _required_json_list(raw, "graded_dimensions", target)
    decision_rules = raw.get("decision_rules", [])
    final_labels = raw.get("final_labels", [])
    if not isinstance(decision_rules, list):
        raise SchemaValidationError(f"{target} field decision_rules must be a list")
    if not isinstance(final_labels, list) or not all(isinstance(label, str) and label.strip() for label in final_labels):
        raise SchemaValidationError(f"{target} field final_labels must be a nonempty list of strings")
    _validate_safety_gates(target, safety_gates)
    _validate_dimensions(target, graded_dimensions)
    return ScoringRubric(
        schema_version=schema_version,
        title=title,
        safety_gates=list(safety_gates),
        graded_dimensions=list(graded_dimensions),
        decision_rules=list(decision_rules),
        final_labels=list(final_labels),
        raw=dict(raw),
    )


def _require_exact_columns(path: Path, actual: tuple[str, ...], expected: tuple[str, ...]) -> None:
    if actual != expected:
        raise SchemaValidationError(f"{path} columns must be {list(expected)}, found {list(actual)}")


def _require_unique(rows: list[dict[str, str]], key: str, path: Path) -> None:
    seen: set[str] = set()
    duplicates: list[str] = []
    for index, row in enumerate(rows, start=2):
        value = _required_text(row, key, path, index)
        if value in seen:
            duplicates.append(value)
        seen.add(value)
    if duplicates:
        raise SchemaValidationError(f"{path} has duplicate {key} values: {duplicates[:10]}")


def _required_text(row: dict[str, str], key: str, path: Path, index: int) -> str:
    value = row.get(key, "")
    if not isinstance(value, str) or not value.strip():
        raise SchemaValidationError(f"{path}:{index} has blank required field {key}")
    return value.strip()


def _first_text(row: dict[str, Any], keys: tuple[str, ...], path: Path, index: int) -> str:
    for key in keys:
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise SchemaValidationError(f"{path}:{index} must include one of {list(keys)}")


def _required_json_text(row: dict[str, Any], key: str, path: Path) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SchemaValidationError(f"{path} field {key} must be a nonempty string")
    return value.strip()


def _required_json_list(row: dict[str, Any], key: str, path: Path) -> list[Any]:
    value = row.get(key)
    if not isinstance(value, list) or not value:
        raise SchemaValidationError(f"{path} field {key} must be a nonempty list")
    return value


def _validate_safety_gates(path: Path, safety_gates: list[Any]) -> None:
    gate_ids: set[str] = set()
    source_tags: dict[str, str] = {}
    for index, gate in enumerate(safety_gates, start=1):
        if not isinstance(gate, dict):
            raise SchemaValidationError(f"{path} safety_gates[{index}] must be an object")
        gate_id = gate.get("gate_id")
        if not isinstance(gate_id, str) or not gate_id.strip():
            raise SchemaValidationError(f"{path} safety_gates[{index}] has blank gate_id")
        if gate_id in gate_ids:
            raise SchemaValidationError(f"{path} duplicates safety gate {gate_id}")
        gate_ids.add(gate_id)
        if not isinstance(gate.get("definition"), str) or not gate["definition"].strip():
            raise SchemaValidationError(f"{path} safety gate {gate_id} has blank definition")
        tags = gate.get("source_tags")
        if not isinstance(tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in tags):
            raise SchemaValidationError(f"{path} safety gate {gate_id} source_tags must be strings")
        for tag in tags:
            if tag in source_tags:
                raise SchemaValidationError(f"{path} source tag {tag} maps to both {source_tags[tag]} and {gate_id}")
            source_tags[tag] = gate_id


def _validate_dimensions(path: Path, graded_dimensions: list[Any]) -> None:
    dimension_ids: set[str] = set()
    for index, dimension in enumerate(graded_dimensions, start=1):
        if not isinstance(dimension, dict):
            raise SchemaValidationError(f"{path} graded_dimensions[{index}] must be an object")
        dimension_id = dimension.get("dimension_id")
        if not isinstance(dimension_id, str) or not dimension_id.strip():
            raise SchemaValidationError(f"{path} graded_dimensions[{index}] has blank dimension_id")
        if dimension_id in dimension_ids:
            raise SchemaValidationError(f"{path} duplicates graded dimension {dimension_id}")
        dimension_ids.add(dimension_id)
        for level in ("level_0", "level_1", "level_2"):
            if not isinstance(dimension.get(level), str) or not dimension[level].strip():
                raise SchemaValidationError(f"{path} graded dimension {dimension_id} has blank {level}")
