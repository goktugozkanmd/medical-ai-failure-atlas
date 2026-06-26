#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "medical_intelligence_atlas_v0_1_20260625.json"
BUILDER = ROOT / "scripts" / "build_medical_intelligence_atlas_v0_1_20260625.py"
MARKDOWN = ROOT / "docs" / "MEDICAL_INTELLIGENCE_ATLAS_V0_1_20260625.md"

EXPECTED_LAYERS = {
    "Clinical State Language",
    "Clinical Trajectory Engine",
    "Medical Reasoning Verifier",
    "Agentic Medicine Sandbox",
    "Multilingual Medical Intelligence",
    "Medical Intelligence Atlas",
}

FORBIDDEN_PHRASES = [
    "patient data used",
    "clinical validation complete",
    "clinical deployment ready",
    "diagnosis provided",
    "treatment recommendation provided",
    "model superiority proven",
    "partner confirmed",
    "institutional support confirmed",
    "payment completed",
    "terms accepted",
]


def main() -> int:
    errors: list[str] = []

    if not CONFIG.exists():
        errors.append(f"Missing config: {CONFIG.relative_to(ROOT)}")
        data = {}
    else:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))

    check = subprocess.run(
        [sys.executable, str(BUILDER), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if check.returncode != 0:
        errors.append(check.stdout.strip())

    nodes = data.get("nodes", [])
    if len(nodes) != 88:
        errors.append("Expected eighty eight atlas nodes")

    layers = {node.get("layer") for node in nodes}
    if layers != EXPECTED_LAYERS:
        errors.append(f"Layer set mismatch: {sorted(layers)}")

    seen_ids: set[str] = set()
    for node in nodes:
        node_id = node.get("id")
        if node_id in seen_ids:
            errors.append(f"Duplicate node id: {node_id}")
        seen_ids.add(str(node_id))
        for field in ["artifact", "input", "output", "validator", "risk_gate", "next_build"]:
            if not node.get(field):
                errors.append(f"{node_id}: missing {field}")

    if len(data.get("relationships", [])) != 5:
        errors.append("Expected five relationships")
    if len(data.get("release_states", [])) != 3:
        errors.append("Expected three release states")

    text = ""
    if not MARKDOWN.exists():
        errors.append(f"Missing markdown: {MARKDOWN.relative_to(ROOT)}")
    else:
        text = MARKDOWN.read_text(encoding="utf-8")

    lower = text.lower()
    for phrase in [
        "Medical Intelligence Atlas v0.1",
        "Build Nodes",
        "Clinical State Language",
        "Clinical Trajectory Engine",
        "Medical Reasoning Verifier",
        "Agentic Medicine Sandbox",
        "Multilingual Medical Intelligence",
        "release cannot outrun validators",
        "make medical_intelligence_atlas",
    ]:
        if phrase.lower() not in lower:
            errors.append(f"Missing required phrase: {phrase}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower:
            errors.append(f"Forbidden phrase: {phrase}")

    if errors:
        print("FAIL Medical Intelligence Atlas validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Medical Intelligence Atlas validation")
    print(f"config={CONFIG.relative_to(ROOT)}")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"nodes={len(nodes)}")
    print(f"relationships={len(data['relationships'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
