#!/usr/bin/env python3
"""Score a CI eval raw run with the repository scorer."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from failure_atlas.scorer import score_raw_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score a CI raw eval run.")
    parser.add_argument("--input", required=True, help="Raw run JSON file.")
    parser.add_argument("--output", required=True, help="Scored output JSON file.")
    parser.add_argument(
        "--rubric",
        default="data/scoring_rubric_v0_3.json",
        help="Scoring rubric JSON file.",
    )
    parser.add_argument("--method", default="rule", help="Scoring method.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    score_raw_output(
        raw_path=Path(args.input),
        rubric_path=Path(args.rubric),
        method=args.method,
        output_path=Path(args.output),
    )
    payload = json.loads(Path(args.output).read_text(encoding="utf-8"))
    rows = payload.get("items") or []
    labels = Counter(item.get("final_label", "unknown") for item in rows)
    label_text = ", ".join(f"{label}={count}" for label, count in sorted(labels.items()))
    print(f"Wrote {args.output} with {len(rows)} scored item(s): {label_text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
