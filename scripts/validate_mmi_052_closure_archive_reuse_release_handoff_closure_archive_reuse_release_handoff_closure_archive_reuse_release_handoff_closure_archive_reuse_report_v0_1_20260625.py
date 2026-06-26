#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

sys.dont_write_bytecode = True

from score_mmi_052_closure_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_archive_reuse_release_handoff_closure_archive_reuse_controls_v0_1_20260625 import (
    CROSS_LANGUAGE_CONTROLS,
    OUTPUT_JSON,
    OUTPUT_MARKDOWN,
    REWRITE_CANDIDATES,
    as_json_text,
    build_report,
    load_jsonl,
    render_markdown,
    repo_relative,
    validate_control_rows,
    validate_markdown,
    validate_report,
)


def main() -> int:
    errors: list[str] = []
    for path in (REWRITE_CANDIDATES, CROSS_LANGUAGE_CONTROLS, OUTPUT_JSON, OUTPUT_MARKDOWN):
        if not path.exists():
            errors.append(f"missing required file: {repo_relative(path)}")
    if errors:
        print("FAIL cross language reviewer closeout ledger reconciliation exception replay archive rollup release handoff closure archive reuse release handoff closure archive reuse release handoff closure archive reuse release handoff closure archive reuse report validation")
        for error in errors:
            print(f"- {error}")
        return 1
    try:
        rewrite_candidates = load_jsonl(REWRITE_CANDIDATES)
        controls = load_jsonl(CROSS_LANGUAGE_CONTROLS)
        actual_json = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    except (ValueError, json.JSONDecodeError) as error:
        print(f"FAIL cross language reviewer closeout ledger reconciliation exception replay archive rollup release handoff closure archive reuse release handoff closure archive reuse release handoff closure archive reuse release handoff closure archive reuse report validation: {error}")
        return 1
    expected_report = build_report(controls, rewrite_candidates)
    expected_json_text = as_json_text(expected_report)
    expected_markdown = render_markdown(expected_report)
    actual_markdown = OUTPUT_MARKDOWN.read_text(encoding="utf-8")
    errors.extend(validate_control_rows(controls, rewrite_candidates))
    errors.extend(validate_report(actual_json))
    errors.extend(validate_markdown(actual_markdown))
    if OUTPUT_JSON.read_text(encoding="utf-8") != expected_json_text:
        errors.append(f"stale JSON report: {repo_relative(OUTPUT_JSON)}")
    if actual_markdown != expected_markdown:
        errors.append(f"stale Markdown report: {repo_relative(OUTPUT_MARKDOWN)}")
    if errors:
        print("FAIL cross language reviewer closeout ledger reconciliation exception replay archive rollup release handoff closure archive reuse release handoff closure archive reuse release handoff closure archive reuse release handoff closure archive reuse report validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS cross language reviewer closeout ledger reconciliation exception replay archive rollup release handoff closure archive reuse release handoff closure archive reuse release handoff closure archive reuse release handoff closure archive reuse report validation")
    print(f"json={repo_relative(OUTPUT_JSON)}")
    print(f"markdown={repo_relative(OUTPUT_MARKDOWN)}")
    print(f"controls={actual_json['score_summary']['control_count']}")
    print(f"blocked_controls={actual_json['score_summary']['observed_blocked_controls']}")
    print(f"pass_controls={actual_json['score_summary']['observed_pass_controls']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
