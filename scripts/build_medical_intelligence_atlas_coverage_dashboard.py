#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_NAME_TOKEN = "medical_intelligence_atlas_coverage"
DASHBOARD_NAME_TOKEN = "medical_intelligence_atlas_coverage_dashboard"
DEFAULT_OUTPUT = ROOT / "docs" / f"{DASHBOARD_NAME_TOKEN}.md"
SUPPORTED_SUFFIXES = {".json", ".jsonl", ".csv", ".tsv"}

ROW_KEYS = ("coverage", "coverage_rows", "coverage_items", "rows", "nodes")
STATUS_DONE_VALUES = {"covered", "complete", "done", "pass", "passed", "ready"}
STATUS_OPEN_MARKERS = {"blocked", "gap", "missing", "needs", "partial"}
OPEN_GAP_OPEN_MARKERS = {
    "blocked",
    "missing",
    "needs",
    "not_yet_represented",
    "unresolved",
}

EXTERNAL_URL_RE = re.compile(r"https?://|www\.", re.IGNORECASE)
FORBIDDEN_TEXT_RE = re.compile(
    "|".join(
        re.escape(phrase)
        for phrase in [
            "patient data used",
            "real patient data",
            "clinical validation complete",
            "clinically validated",
            "clinical deployment ready",
            "deployment ready",
            "diagnosis provided",
            "treatment recommendation provided",
        ]
    ),
    re.IGNORECASE,
)
SENSITIVE_FIELD_NAMES = {
    "date_of_birth",
    "dob",
    "medical_record_number",
    "mrn",
    "patient_id",
    "patient_name",
    "tc_kimlik",
}


class DashboardError(Exception):
    pass


def repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def find_data_file() -> Path:
    data_dir = ROOT / "data"
    if not data_dir.exists():
        raise DashboardError("FAIL missing data directory: data")

    candidates = sorted(
        path
        for path in data_dir.rglob("*")
        if path.is_file()
        and DATA_NAME_TOKEN in path.name.lower()
        and path.suffix.lower() in SUPPORTED_SUFFIXES
    )
    if not candidates:
        suffixes = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise DashboardError(
            "FAIL missing coverage data file: expected one file under data/ "
            f"with name containing '{DATA_NAME_TOKEN}' and suffix {suffixes}"
        )
    if len(candidates) > 1:
        joined = ", ".join(repo_relative(path) for path in candidates)
        raise DashboardError(
            "FAIL multiple coverage data files found; pass --data explicitly: "
            f"{joined}"
        )
    return candidates[0]


def validate_data_path(path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.exists():
        raise DashboardError(f"FAIL missing data file: {path}")
    if DATA_NAME_TOKEN not in resolved.name.lower():
        raise DashboardError(
            "FAIL data file name must contain "
            f"'{DATA_NAME_TOKEN}': {repo_relative(resolved)}"
        )
    if resolved.suffix.lower() not in SUPPORTED_SUFFIXES:
        suffixes = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise DashboardError(
            f"FAIL unsupported data suffix for {repo_relative(resolved)}; "
            f"expected one of {suffixes}"
        )
    return resolved


def load_json(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {}, require_records(payload, path)
    if not isinstance(payload, dict):
        raise DashboardError("FAIL JSON data must be an object or an array of objects")

    for key in ROW_KEYS:
        rows = payload.get(key)
        if rows is not None:
            metadata = {name: value for name, value in payload.items() if name != key}
            return metadata, require_records(rows, path)

    expected = ", ".join(ROW_KEYS)
    raise DashboardError(
        "FAIL JSON object must contain one coverage row key: " f"{expected}"
    )


def load_jsonl(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise DashboardError(
                f"FAIL invalid JSONL at line {line_number}: {exc.msg}"
            ) from exc
        if not isinstance(row, dict):
            raise DashboardError(f"FAIL JSONL line {line_number} is not an object")
        rows.append(row)
    return {}, require_records(rows, path)


def load_delimited(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        if not reader.fieldnames:
            raise DashboardError(f"FAIL missing header row: {repo_relative(path)}")
        rows = [dict(row) for row in reader]
    return {}, require_records(rows, path)


def load_data(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return load_json(path)
    if suffix == ".jsonl":
        return load_jsonl(path)
    if suffix in {".csv", ".tsv"}:
        return load_delimited(path)
    raise DashboardError(f"FAIL unsupported data suffix: {suffix}")


def require_records(rows: Any, path: Path) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        raise DashboardError(f"FAIL coverage rows must be an array: {repo_relative(path)}")
    if not rows:
        raise DashboardError(f"FAIL coverage data has no rows: {repo_relative(path)}")
    bad_indexes = [index for index, row in enumerate(rows, 1) if not isinstance(row, dict)]
    if bad_indexes:
        joined = ", ".join(str(index) for index in bad_indexes[:5])
        raise DashboardError(f"FAIL coverage rows must be objects; bad rows: {joined}")
    return rows


def walk_values(value: Any, prefix: str = "root") -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            findings.extend(walk_values(item, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value, 1):
            findings.extend(walk_values(item, f"{prefix}[{index}]"))
    elif value is not None:
        findings.append((prefix, str(value)))
    return findings


def validate_content(metadata: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    errors: list[str] = []
    payload = {"metadata": metadata, "rows": rows}
    for location, value in walk_values(payload):
        if EXTERNAL_URL_RE.search(value):
            errors.append(f"external URL at {location}")
        if FORBIDDEN_TEXT_RE.search(value):
            errors.append(f"forbidden claim text at {location}")

    for row_index, row in enumerate(rows, 1):
        for key in row:
            normalized = normalize_key(key)
            if normalized in SENSITIVE_FIELD_NAMES:
                errors.append(f"sensitive field '{key}' in row {row_index}")

    if errors:
        print("FAIL coverage data boundary check")
        for error in errors:
            print(f"- {error}")
        raise DashboardError("FAIL coverage data boundary check failed")


def normalize_key(key: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", key.strip().lower())
    return normalized.strip("_")


def find_field(rows: list[dict[str, Any]], candidates: tuple[str, ...]) -> str | None:
    by_normalized: dict[str, str] = {}
    for row in rows:
        for key in row:
            by_normalized.setdefault(normalize_key(key), key)
    for candidate in candidates:
        found = by_normalized.get(candidate)
        if found:
            return found
    return None


def ordered_columns(rows: list[dict[str, Any]]) -> list[str]:
    preferred_candidates = [
        ("layer", "domain", "area"),
        ("node_id", "node", "id", "target_id"),
        ("artifact", "target", "build_target"),
        ("coverage_status", "status", "state"),
        ("evidence", "evidence_file", "source_file", "artifact_path"),
        ("validator", "validation", "check"),
        ("blocker", "gap", "missing", "next_action", "open_gap"),
    ]
    columns: list[str] = []
    for candidates in preferred_candidates:
        field = find_field(rows, candidates)
        if field and field not in columns:
            columns.append(field)

    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    return columns


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=True, sort_keys=True)
    else:
        text = str(value)
    return text.replace("\n", " ").replace("|", "\\|").strip()


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(cell(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(value) for value in row) + " |")
    return lines


def counter_rows(counter: Counter[str]) -> list[list[Any]]:
    return [[key, counter[key]] for key in sorted(counter)]


def status_is_covered(status: str) -> bool:
    normalized = normalize_key(status)
    if normalized in STATUS_DONE_VALUES:
        return True
    if normalized.endswith("_coverage"):
        return not any(marker in normalized for marker in STATUS_OPEN_MARKERS)
    return False


def open_gap_is_unresolved(value: str) -> bool:
    normalized = normalize_key(value)
    if not normalized:
        return False
    if any(marker in normalized for marker in OPEN_GAP_OPEN_MARKERS):
        return True
    if "represented_by" in normalized:
        return False
    return True


def render_dashboard(
    data_path: Path, metadata: dict[str, Any], rows: list[dict[str, Any]]
) -> str:
    layer_field = find_field(rows, ("layer", "domain", "area"))
    status_field = find_field(rows, ("coverage_status", "status", "state"))
    node_field = find_field(rows, ("node_id", "node", "id", "target_id"))
    blocker_field = find_field(rows, ("blocker", "gap", "missing", "next_action", "open_gap"))
    blocker_field_name = normalize_key(blocker_field or "")

    lines = [
        "# Medical Intelligence Atlas Coverage Dashboard",
        "",
        f"Source data: `{repo_relative(data_path)}`",
        "",
        f"Rows: {len(rows)}",
        "",
        "Boundary: this dashboard uses the source coverage data only and does not assert clinical readiness.",
        "",
    ]

    metadata_rows = [
        [key, value]
        for key, value in sorted(metadata.items())
        if isinstance(value, (str, int, float, bool)) or value is None
    ]
    if metadata_rows:
        lines.extend(["## Metadata", "", *markdown_table(["Field", "Value"], metadata_rows), ""])

    if status_field:
        status_counts = Counter(cell(row.get(status_field)) or "unspecified" for row in rows)
        lines.extend(
            ["## Status Summary", "", *markdown_table(["Status", "Rows"], counter_rows(status_counts)), ""]
        )
    else:
        lines.extend(["## Status Summary", "", "No status field was found in the source data.", ""])

    if layer_field and status_field:
        grouped: dict[str, Counter[str]] = defaultdict(Counter)
        statuses = sorted({cell(row.get(status_field)) or "unspecified" for row in rows})
        for row in rows:
            layer = cell(row.get(layer_field)) or "unspecified"
            status = cell(row.get(status_field)) or "unspecified"
            grouped[layer][status] += 1
        layer_rows = [
            [layer, sum(grouped[layer].values()), *(grouped[layer][status] for status in statuses)]
            for layer in sorted(grouped)
        ]
        lines.extend(
            [
                "## Layer Coverage",
                "",
                *markdown_table(["Layer", "Rows", *statuses], layer_rows),
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Layer Coverage",
                "",
                "Layer and status fields were not both found in the source data.",
                "",
            ]
        )

    if status_field or blocker_field:
        open_rows = []
        for row in rows:
            status = cell(row.get(status_field)) if status_field else ""
            blocker = cell(row.get(blocker_field)) if blocker_field else ""
            is_done = status_is_covered(status)
            blocker_open = bool(blocker)
            if blocker_field_name == "open_gap":
                blocker_open = open_gap_is_unresolved(blocker)
            if blocker_open or (status and not is_done):
                open_rows.append(
                    [
                        row.get(layer_field, "") if layer_field else "",
                        row.get(node_field, "") if node_field else "",
                        status,
                        blocker,
                    ]
                )
        lines.extend(["## Open Gaps", ""])
        if open_rows:
            lines.extend(markdown_table(["Layer", "Node", "Status", "Blocker"], open_rows))
        else:
            lines.append("No open gaps were found in the source data.")
        lines.append("")

    columns = ordered_columns(rows)
    lines.extend(
        [
            "## Coverage Rows",
            "",
            *markdown_table(columns, [[row.get(column, "") for column in columns] for row in rows]),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--data", type=Path)
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    try:
        data_path = validate_data_path(args.data) if args.data else find_data_file()
        metadata, rows = load_data(data_path)
        validate_content(metadata, rows)
        expected = render_dashboard(data_path, metadata, rows)

        if args.stdout:
            print(expected)
            return 0

        if args.check:
            if not DEFAULT_OUTPUT.exists():
                print(f"FAIL missing dashboard: {repo_relative(DEFAULT_OUTPUT)}")
                return 1
            if DEFAULT_OUTPUT.read_text(encoding="utf-8") != expected:
                print(f"FAIL stale dashboard: {repo_relative(DEFAULT_OUTPUT)}")
                return 1
            print("PASS Medical Intelligence Atlas coverage dashboard is current")
            print(f"data={repo_relative(data_path)}")
            print(f"dashboard={repo_relative(DEFAULT_OUTPUT)}")
            return 0

        DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_OUTPUT.write_text(expected, encoding="utf-8")
        print(f"Wrote {repo_relative(DEFAULT_OUTPUT)}")
        return 0
    except DashboardError as exc:
        if str(exc):
            print(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
