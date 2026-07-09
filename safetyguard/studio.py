from __future__ import annotations

import argparse
import json
import webbrowser
from datetime import datetime, timezone
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from failure_atlas.data import load_prompt_set, load_scoring_rubric
from failure_atlas.scorer import FailureAtlasScorer, RawModelOutput


PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_PROMPTS = PACKAGE_ROOT / "data" / "medfailbench_prompts_v0_2.tsv"
DEFAULT_RUBRIC = PACKAGE_ROOT / "data" / "scoring_rubric_v0_3.json"

PROOF_PACK_ARTIFACTS = [
    {
        "id": "health_ai_start_here",
        "label": "Health AI Assurance Kit Start Here",
        "path": "docs/HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md",
        "status": "local_start_here_ready",
    },
    {
        "id": "health_ai_roadmap",
        "label": "Health AI Assurance Kit roadmap",
        "path": "docs/HEALTH_AI_ASSURANCE_KIT_ROADMAP_20260708.md",
        "status": "p0_to_p7b_completed_p8_blocked",
    },
    {
        "id": "kit_assurance_card",
        "label": "Kit level assurance card",
        "path": "docs/HEALTH_AI_ASSURANCE_KIT_CARD_20260708.md",
        "status": "local_kit_card_ready",
    },
    {
        "id": "safetyguard_studio",
        "label": "SafetyGuard Studio scoring",
        "path": "safetyguard/studio.py",
        "status": "local_product_mode",
    },
    {
        "id": "sourcecheckup_medical",
        "label": "SourceCheckup Medical review route",
        "path": "docs/SOURCECHECKUP_MEDICAL_CLI_REPORT_20260708.md",
        "status": "local_cli_report_ready",
    },
    {
        "id": "transparency_card",
        "label": "Transparency card export",
        "path": "scripts/export_safetyguard_transparency_card.py",
        "status": "local_export_ready",
    },
    {
        "id": "turkish_drift",
        "label": "Turkish and English drift review",
        "path": "docs/TURKISH_DRIFT_PREVIEW_DASHBOARD_20260708.md",
        "status": "local_drift_preview_ready",
    },
    {
        "id": "clinician_literacy",
        "label": "Clinician literacy simulator",
        "path": "docs/HEALTH_AI_CLINICIAN_LITERACY_DEMO_INDEX_20260708.md",
        "status": "local_demo_index_ready",
    },
    {
        "id": "monitoring_digest_schema",
        "label": "Monitoring digest schema",
        "path": "docs/HEALTH_AI_MONITORING_DIGEST_SCHEMA_20260708.md",
        "status": "manual_schema_ready_no_automation",
    },
    {
        "id": "adapter_framework_smoke",
        "label": "Adapter framework smoke",
        "path": "docs/MEDFAILBENCH_ADAPTER_FRAMEWORK_SMOKE_20260708.md",
        "status": "local_framework_smoke_ready",
    },
]


def product_mode_manifest() -> dict[str, Any]:
    return {
        "schema_version": "safetyguard_studio_product_mode_v0_1",
        "product_name": "Clinical AI Safety Ops / Health AI Assurance Kit",
        "surface": "SafetyGuard Studio product mode",
        "boundary": "Local synthetic or manually pasted review only. No patient data, clinical validation, model ranking, regulatory compliance, official compatibility, or deployment claim.",
        "external_action_allowed": False,
        "provider_api_call_allowed": False,
        "new_cases_added": False,
        "proof_pack": PROOF_PACK_ARTIFACTS,
        "export_types": [
            {
                "id": "score_json",
                "label": "Score JSON",
                "description": "Machine readable local rule scoring result.",
            },
            {
                "id": "assurance_summary_json",
                "label": "Assurance summary JSON",
                "description": "Short local evidence summary with explicit boundary fields.",
            },
        ],
        "input_modes": ["sample_mode", "manual_answer_paste"],
    }


def analyze_answer(
    *,
    prompt: str,
    answer: str,
    scenario_id: str = "STUDIO_MANUAL",
    model_name: str = "manual-answer",
    rubric_path: str | Path = DEFAULT_RUBRIC,
) -> dict[str, Any]:
    rubric = load_scoring_rubric(rubric_path)
    scorer = FailureAtlasScorer(rubric=rubric)
    output = RawModelOutput(
        model_name=model_name.strip() or "manual-answer",
        scenario_id=scenario_id.strip() or "STUDIO_MANUAL",
        prompt_text=prompt,
        model_answer=answer,
        raw={
            "source": "safetyguard_studio_manual_input",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    scores = scorer.score_outputs(model_name=output.model_name, outputs=[output], method="rule")
    score_item = scores["items"][0]
    result = {
        "schema_version": "safetyguard_studio_result_v0_1",
        "generated_at": scores["scored_at"],
        "boundary": "Synthetic or manually pasted review only. Not clinical advice, clinical validation, ranking, certification, or deployment evidence.",
        "product_mode_schema_version": "safetyguard_studio_product_mode_v0_1",
        "model_name": output.model_name,
        "scenario_id": output.scenario_id,
        "score_item": score_item,
        "aggregates": scores["aggregates"],
    }
    result["export_bundle"] = build_export_bundle(result)
    return result


def build_export_bundle(result: dict[str, Any]) -> dict[str, Any]:
    scenario_id = safe_filename_part(str(result.get("scenario_id", "STUDIO_MANUAL")))
    generated = str(result.get("generated_at", "")).replace(":", "").replace("+", "Z")
    stem = f"safetyguard_studio_{scenario_id}_{generated or 'local'}"
    summary = {
        "schema_version": "safetyguard_assurance_summary_v0_1",
        "generated_at": result.get("generated_at"),
        "model_name": result.get("model_name"),
        "scenario_id": result.get("scenario_id"),
        "final_label": result.get("score_item", {}).get("final_label"),
        "scores": result.get("score_item", {}).get("scores", {}),
        "safety_gates": result.get("score_item", {}).get("safety_gates", {}),
        "review_status": "local_rule_scoring_only",
        "synthetic_or_manual_input_only": True,
        "contains_patient_data": False,
        "external_action_allowed": False,
        "clinical_validation_claim": False,
        "model_ranking_claim": False,
        "boundary": result.get("boundary"),
    }
    return {
        "score_json_filename": f"{stem}_score.json",
        "assurance_summary_filename": f"{stem}_assurance_summary.json",
        "assurance_summary": summary,
        "download_links_are_client_side": True,
    }


def safe_filename_part(value: str) -> str:
    cleaned = "".join(character.lower() if character.isalnum() else "_" for character in value.strip())
    cleaned = "_".join(part for part in cleaned.split("_") if part)
    return cleaned[:80] or "studio_manual"


def load_examples(prompt_set: str | Path = DEFAULT_PROMPTS, limit: int = 12) -> list[dict[str, str]]:
    prompts = load_prompt_set(prompt_set)
    return [
        {
            "scenario_id": prompt.scenario_id,
            "prompt_text": prompt.prompt_text,
            "output_capture_instruction": prompt.output_capture_instruction,
        }
        for prompt in prompts[:limit]
    ]


def make_handler(
    *,
    prompt_set: str | Path = DEFAULT_PROMPTS,
    rubric_path: str | Path = DEFAULT_RUBRIC,
) -> type[BaseHTTPRequestHandler]:
    prompt_source = Path(prompt_set)
    rubric_source = Path(rubric_path)

    class SafetyGuardStudioHandler(BaseHTTPRequestHandler):
        server_version = "SafetyGuardStudio/0.1"

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path == "/":
                self._send_text(build_html(), content_type="text/html; charset=utf-8")
                return
            if parsed.path == "/api/examples":
                self._send_json({"examples": load_examples(prompt_source)})
                return
            if parsed.path == "/api/proof-pack":
                self._send_json(product_mode_manifest())
                return
            self._send_json({"error": "not_found"}, status=HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path != "/api/analyze":
                self._send_json({"error": "not_found"}, status=HTTPStatus.NOT_FOUND)
                return
            try:
                payload = self._read_json()
                result = analyze_answer(
                    prompt=str(payload.get("prompt", "")),
                    answer=str(payload.get("answer", "")),
                    scenario_id=str(payload.get("scenario_id", "STUDIO_MANUAL")),
                    model_name=str(payload.get("model_name", "manual-answer")),
                    rubric_path=rubric_source,
                )
            except Exception as exc:
                self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return
            self._send_json(result)

        def log_message(self, format: str, *args: object) -> None:
            return

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 1_000_000:
                raise ValueError("Request body is too large.")
            raw = self.rfile.read(length).decode("utf-8")
            if not raw.strip():
                return {}
            payload = json.loads(raw)
            if not isinstance(payload, dict):
                raise ValueError("Request body must be a JSON object.")
            return payload

        def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
            body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(int(status))
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_text(self, value: str, *, content_type: str, status: HTTPStatus = HTTPStatus.OK) -> None:
            body = value.encode("utf-8")
            self.send_response(int(status))
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return SafetyGuardStudioHandler


def build_html() -> str:
    title = "SafetyGuard Studio"
    escaped_title = escape(title)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escaped_title}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f4;
      --panel: #ffffff;
      --ink: #202124;
      --muted: #5f6368;
      --line: #d7d9d3;
      --accent: #1f6f78;
      --danger: #9f2f25;
      --ok: #237344;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    header {{
      border-bottom: 1px solid var(--line);
      background: var(--panel);
      padding: 16px 24px;
    }}
    h1 {{ font-size: 20px; margin: 0; font-weight: 700; }}
    main {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 360px;
      gap: 16px;
      padding: 16px;
      max-width: 1220px;
      margin: 0 auto;
    }}
    section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }}
    h2 {{ margin: 0 0 12px; font-size: 15px; }}
    label {{ display: block; color: var(--muted); font-weight: 650; margin: 12px 0 6px; }}
    input, select, textarea {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px;
      font: inherit;
      background: #fff;
      color: var(--ink);
    }}
    textarea {{ min-height: 150px; resize: vertical; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
    .actions {{ display: flex; gap: 8px; align-items: center; margin-top: 12px; }}
    .modebar {{ display: flex; gap: 8px; flex-wrap: wrap; margin: 4px 0 10px; }}
    button {{
      border: 1px solid var(--accent);
      background: var(--accent);
      color: #fff;
      border-radius: 6px;
      padding: 10px 12px;
      font-weight: 700;
      cursor: pointer;
    }}
    .mode-btn.active {{ box-shadow: 0 0 0 2px rgba(31, 111, 120, 0.18); }}
    button.secondary {{ background: #fff; color: var(--accent); }}
    a.download {{
      display: inline-block;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 9px 10px;
      margin: 4px 4px 4px 0;
      color: var(--accent);
      text-decoration: none;
      font-weight: 700;
      background: #fff;
    }}
    a.download.disabled {{
      color: var(--muted);
      pointer-events: none;
      opacity: .62;
    }}
    .score-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }}
    .metric {{ border: 1px solid var(--line); border-radius: 6px; padding: 10px; }}
    .metric strong {{ display: block; font-size: 22px; }}
    .label {{ font-weight: 800; margin: 10px 0; }}
    .unsafe {{ color: var(--danger); }}
    .usable {{ color: var(--ok); }}
    pre {{
      white-space: pre-wrap;
      word-break: break-word;
      background: #f1f3f1;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px;
      max-height: 320px;
      overflow: auto;
    }}
    .muted {{ color: var(--muted); }}
    .proof-list {{ margin: 0; padding-left: 18px; }}
    .proof-list li {{ margin: 6px 0; }}
    .tag {{ color: var(--muted); font-size: 12px; }}
    @media (max-width: 860px) {{
      main {{ grid-template-columns: 1fr; padding: 10px; }}
      .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{escaped_title}</h1>
    <div class="muted">Local synthetic safety review. No patient data. No clinical validation claim.</div>
  </header>
  <main>
    <section>
      <h2>Review Input</h2>
      <div class="modebar" role="group" aria-label="Input mode">
        <button class="secondary mode-btn active" id="sampleModeBtn" type="button">Sample mode</button>
        <button class="secondary mode-btn" id="manualModeBtn" type="button">Manual answer</button>
      </div>
      <div class="grid">
        <div>
          <label for="modelName">Model or run label</label>
          <input id="modelName" value="manual-answer">
        </div>
        <div>
          <label for="scenarioId">Scenario ID</label>
          <input id="scenarioId" value="STUDIO_MANUAL">
        </div>
      </div>
      <label for="exampleSelect">Synthetic example</label>
      <select id="exampleSelect"><option value="">Manual input</option></select>
      <label for="prompt">Prompt</label>
      <textarea id="prompt"></textarea>
      <label for="answer">Model answer</label>
      <textarea id="answer"></textarea>
      <div class="actions">
        <button id="analyzeBtn">Analyze</button>
        <button class="secondary" id="clearBtn" type="button">Clear</button>
      </div>
    </section>
    <section>
      <h2>Proof Pack</h2>
      <div class="muted">Health AI Assurance Kit Start Here: docs/HEALTH_AI_ASSURANCE_KIT_START_HERE_20260708.md</div>
      <div id="proofBoundary" class="muted">Loading product mode.</div>
      <ul id="proofPack" class="proof-list"></ul>
      <h2>Exports</h2>
      <div>
        <a id="scoreDownload" class="download disabled" href="#" aria-disabled="true">Score JSON</a>
        <a id="summaryDownload" class="download disabled" href="#" aria-disabled="true">Assurance summary</a>
      </div>
      <h2>Result</h2>
      <div id="status" class="muted">Waiting for input.</div>
      <div id="label" class="label"></div>
      <div id="metrics" class="score-grid"></div>
      <h2>Reasons</h2>
      <pre id="reasons"></pre>
      <h2>JSON</h2>
      <pre id="jsonOut"></pre>
    </section>
  </main>
  <script>
    const exampleSelect = document.getElementById('exampleSelect');
    const promptBox = document.getElementById('prompt');
    const answerBox = document.getElementById('answer');
    const scenarioBox = document.getElementById('scenarioId');
    const modelBox = document.getElementById('modelName');
    const statusBox = document.getElementById('status');
    const labelBox = document.getElementById('label');
    const metricsBox = document.getElementById('metrics');
    const reasonsBox = document.getElementById('reasons');
    const jsonOut = document.getElementById('jsonOut');
    const proofPack = document.getElementById('proofPack');
    const proofBoundary = document.getElementById('proofBoundary');
    const scoreDownload = document.getElementById('scoreDownload');
    const summaryDownload = document.getElementById('summaryDownload');
    const sampleModeBtn = document.getElementById('sampleModeBtn');
    const manualModeBtn = document.getElementById('manualModeBtn');
    let examples = [];
    let currentMode = 'sample_mode';

    async function loadExamples() {{
      const response = await fetch('/api/examples');
      const payload = await response.json();
      examples = payload.examples || [];
      examples.forEach((item, index) => {{
        const option = document.createElement('option');
        option.value = String(index);
        option.textContent = item.scenario_id + ' - ' + item.prompt_text.slice(0, 64);
        exampleSelect.appendChild(option);
      }});
    }}

    async function loadProofPack() {{
      const response = await fetch('/api/proof-pack');
      const payload = await response.json();
      proofBoundary.textContent = payload.boundary || '';
      proofPack.innerHTML = '';
      (payload.proof_pack || []).forEach((item) => {{
        const li = document.createElement('li');
        li.innerHTML = '<strong>' + item.label + '</strong><div class="tag">' + item.status + ' - ' + item.path + '</div>';
        proofPack.appendChild(li);
      }});
    }}

    function setMode(mode) {{
      currentMode = mode;
      sampleModeBtn.classList.toggle('active', mode === 'sample_mode');
      manualModeBtn.classList.toggle('active', mode === 'manual_answer_paste');
      if (mode === 'manual_answer_paste') {{
        exampleSelect.value = '';
        scenarioBox.value = 'STUDIO_MANUAL';
        promptBox.focus();
      }} else {{
        exampleSelect.focus();
      }}
    }}

    function setDownload(anchor, filename, content) {{
      const blob = new Blob([content], {{type: 'application/json'}});
      if (anchor.dataset.url) URL.revokeObjectURL(anchor.dataset.url);
      const url = URL.createObjectURL(blob);
      anchor.href = url;
      anchor.download = filename;
      anchor.dataset.url = url;
      anchor.classList.remove('disabled');
      anchor.setAttribute('aria-disabled', 'false');
    }}

    function clearDownloads() {{
      [scoreDownload, summaryDownload].forEach((anchor) => {{
        if (anchor.dataset.url) URL.revokeObjectURL(anchor.dataset.url);
        anchor.removeAttribute('download');
        anchor.href = '#';
        anchor.dataset.url = '';
        anchor.classList.add('disabled');
        anchor.setAttribute('aria-disabled', 'true');
      }});
    }}

    exampleSelect.addEventListener('change', () => {{
      const item = examples[Number(exampleSelect.value)];
      if (!item) return;
      setMode('sample_mode');
      scenarioBox.value = item.scenario_id;
      promptBox.value = item.prompt_text;
      answerBox.value = '';
    }});

    sampleModeBtn.addEventListener('click', () => setMode('sample_mode'));
    manualModeBtn.addEventListener('click', () => setMode('manual_answer_paste'));

    document.getElementById('clearBtn').addEventListener('click', () => {{
      promptBox.value = '';
      answerBox.value = '';
      scenarioBox.value = 'STUDIO_MANUAL';
      labelBox.textContent = '';
      metricsBox.innerHTML = '';
      reasonsBox.textContent = '';
      jsonOut.textContent = '';
      clearDownloads();
      statusBox.textContent = 'Waiting for input.';
    }});

    document.getElementById('analyzeBtn').addEventListener('click', async () => {{
      statusBox.textContent = 'Analyzing...';
      const response = await fetch('/api/analyze', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{
          model_name: modelBox.value,
          scenario_id: scenarioBox.value,
          prompt: promptBox.value,
          answer: answerBox.value
        }})
      }});
      const payload = await response.json();
      if (!response.ok) {{
        statusBox.textContent = payload.error || 'Request failed.';
        return;
      }}
      const item = payload.score_item || {{}};
      const scores = item.scores || {{}};
      statusBox.textContent = payload.boundary || '';
      labelBox.textContent = item.final_label || '';
      labelBox.className = 'label ' + ((item.final_label || '').includes('unsafe') ? 'unsafe' : 'usable');
      metricsBox.innerHTML = '';
      Object.keys(scores).forEach((key) => {{
        const cell = document.createElement('div');
        cell.className = 'metric';
        cell.innerHTML = '<span class="muted">' + key + '</span><strong>' + scores[key] + '</strong>';
        metricsBox.appendChild(cell);
      }});
      reasonsBox.textContent = (item.reasons || []).join('\\n');
      jsonOut.textContent = JSON.stringify(payload, null, 2);
      const bundle = payload.export_bundle || {{}};
      setDownload(scoreDownload, bundle.score_json_filename || 'safetyguard_studio_score.json', JSON.stringify(payload, null, 2));
      setDownload(summaryDownload, bundle.assurance_summary_filename || 'safetyguard_assurance_summary.json', JSON.stringify(bundle.assurance_summary || {{}}, null, 2));
    }});

    loadExamples().catch((error) => {{
      statusBox.textContent = error.message;
    }});
    loadProofPack().catch((error) => {{
      proofBoundary.textContent = error.message;
    }});
  </script>
</body>
</html>
"""


def serve(
    *,
    host: str = "127.0.0.1",
    port: int = 8766,
    prompt_set: str | Path = DEFAULT_PROMPTS,
    rubric_path: str | Path = DEFAULT_RUBRIC,
    open_browser: bool = False,
) -> None:
    handler = make_handler(prompt_set=prompt_set, rubric_path=rubric_path)
    server = ThreadingHTTPServer((host, port), handler)
    url = f"http://{host}:{server.server_port}/"
    print(f"SafetyGuard Studio running at {url}")
    print("Boundary: local synthetic review only. No patient data or clinical validation claim.")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping SafetyGuard Studio.")
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local SafetyGuard Studio web UI.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--prompt-set", default=str(DEFAULT_PROMPTS))
    parser.add_argument("--rubric", default=str(DEFAULT_RUBRIC))
    parser.add_argument("--open", action="store_true", help="Open the UI in the default browser")
    args = parser.parse_args(argv)
    serve(
        host=args.host,
        port=args.port,
        prompt_set=args.prompt_set,
        rubric_path=args.rubric,
        open_browser=args.open,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
