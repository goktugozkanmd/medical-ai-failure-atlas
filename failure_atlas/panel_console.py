from __future__ import annotations

import argparse
import csv
import io
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from failure_atlas.panel_review import (
    DEFAULT_PANEL_CASES_PATH,
    DEFAULT_RATING_TEMPLATE_PATH,
    DEFAULT_REVIEW_STORE_PATH,
    PanelCase,
    cohen_kappa,
    load_panel_cases,
    load_rating_template,
    load_reviews,
    progress_summary,
    reviewer_codes,
    upsert_review,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local MedFailBench clinician review console.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--cases", default=str(DEFAULT_PANEL_CASES_PATH))
    parser.add_argument("--template", default=str(DEFAULT_RATING_TEMPLATE_PATH))
    parser.add_argument("--store", default=str(DEFAULT_REVIEW_STORE_PATH))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run_console(
        host=args.host,
        port=args.port,
        cases_path=Path(args.cases),
        template_path=Path(args.template),
        store_path=Path(args.store),
    )
    return 0


def run_console(*, host: str, port: int, cases_path: Path, template_path: Path, store_path: Path) -> None:
    cases = load_panel_cases(cases_path)
    template_rows = load_rating_template(template_path)
    handler = make_handler(cases=cases, template_rows=template_rows, store_path=store_path)
    server = ThreadingHTTPServer((host, port), handler)
    print(f"Clinician review console: http://{host}:{port}")
    print(f"Review store: {store_path}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping clinician review console")
    finally:
        server.server_close()


def make_handler(
    *,
    cases: list[PanelCase],
    template_rows: list[dict[str, str]],
    store_path: Path,
) -> type[BaseHTTPRequestHandler]:
    reviewers = reviewer_codes(template_rows)

    class ClinicianReviewHandler(BaseHTTPRequestHandler):
        server_version = "MedFailBenchClinicianReview/0.1"

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path == "/":
                self._send_html(render_index(default_reviewer=_query_reviewer(parsed.query, reviewers)))
                return
            if parsed.path == "/api/cases":
                self._send_json([case.to_dict() for case in cases])
                return
            if parsed.path == "/api/reviewers":
                self._send_json({"reviewers": reviewers})
                return
            if parsed.path == "/api/reviews":
                self._send_json({"records": load_reviews(store_path)})
                return
            if parsed.path == "/api/summary":
                records = load_reviews(store_path)
                self._send_json(
                    {
                        "progress": progress_summary(cases, template_rows, records),
                        "severity_kappa": cohen_kappa(records),
                    }
                )
                return
            if parsed.path == "/api/export.json":
                records = load_reviews(store_path)
                self._send_json(
                    {
                        "schema_version": "clinician_review_console_export_v0_1",
                        "progress": progress_summary(cases, template_rows, records),
                        "severity_kappa": cohen_kappa(records),
                        "records": records,
                    },
                    headers={"Content-Disposition": "attachment; filename=clinician_reviews.json"},
                )
                return
            if parsed.path == "/api/export.csv":
                self._send_csv(load_reviews(store_path))
                return
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path != "/api/reviews":
                self.send_error(HTTPStatus.NOT_FOUND, "Not found")
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("Request body must be a JSON object")
                record = upsert_review(payload, cases=cases, template_rows=template_rows, path=store_path)
            except (json.JSONDecodeError, ValueError) as exc:
                self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return
            self._send_json({"record": record, "summary": progress_summary(cases, template_rows, load_reviews(store_path))})

        def log_message(self, format: str, *args: object) -> None:
            print(f"{self.address_string()} - {format % args}")

        def _send_html(self, html: str) -> None:
            body = html.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_json(
            self,
            payload: object,
            *,
            status: HTTPStatus = HTTPStatus.OK,
            headers: dict[str, str] | None = None,
        ) -> None:
            body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            for key, value in (headers or {}).items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(body)

        def _send_csv(self, records: list[dict[str, object]]) -> None:
            fieldnames = [
                "panel_case_id",
                "reviewer_code",
                "language",
                "clinical_domain",
                "severity_1_to_5",
                "likely_harm_if_copied",
                "missing_safety_gate",
                "failure_tags",
                "confidence",
                "free_text_note",
                "should_this_case_stay_in_benchmark",
                "possible_patient_data_flag",
                "updated_at_utc",
            ]
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=fieldnames)
            writer.writeheader()
            for row in records:
                writer.writerow({field: row.get(field, "") for field in fieldnames})
            body = buffer.getvalue().encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=clinician_reviews.csv")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return ClinicianReviewHandler


def _query_reviewer(query: str, reviewers: list[str]) -> str:
    requested = parse_qs(query).get("reviewer", [""])[0]
    return requested if requested in reviewers else (reviewers[0] if reviewers else "")


def render_index(*, default_reviewer: str) -> str:
    default_reviewer_json = json.dumps(default_reviewer)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MedFailBench Clinician Review</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7f8;
      --panel: #ffffff;
      --ink: #172026;
      --muted: #66727f;
      --line: #d8dee4;
      --accent: #0f766e;
      --accent-dark: #115e59;
      --danger: #b42318;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
      letter-spacing: 0;
    }}
    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 14px 22px;
      border-bottom: 1px solid var(--line);
      background: #ffffff;
    }}
    h1 {{
      margin: 0;
      font-size: 18px;
      font-weight: 680;
    }}
    .topbar {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}
    main {{
      display: grid;
      grid-template-columns: minmax(220px, 300px) 1fr;
      min-height: calc(100vh - 58px);
    }}
    aside {{
      border-right: 1px solid var(--line);
      background: #fbfcfd;
      overflow-y: auto;
      padding: 14px;
    }}
    section {{
      padding: 20px;
      overflow: auto;
    }}
    label {{
      display: block;
      font-size: 12px;
      font-weight: 650;
      color: var(--muted);
      margin-bottom: 6px;
    }}
    select, input, textarea {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 9px 10px;
      font: inherit;
      background: #ffffff;
      color: var(--ink);
    }}
    textarea {{
      min-height: 84px;
      resize: vertical;
    }}
    button, .button {{
      border: 1px solid var(--accent);
      background: var(--accent);
      color: #ffffff;
      border-radius: 6px;
      padding: 9px 12px;
      font: inherit;
      font-weight: 650;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 38px;
    }}
    button:hover, .button:hover {{ background: var(--accent-dark); }}
    .ghost {{
      background: #ffffff;
      color: var(--accent);
    }}
    .ghost:hover {{
      background: #edf7f5;
      color: var(--accent-dark);
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(120px, 1fr));
      gap: 10px;
      margin-bottom: 18px;
    }}
    .metric {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      min-height: 74px;
    }}
    .metric strong {{
      display: block;
      font-size: 22px;
      line-height: 1.2;
    }}
    .metric span {{
      color: var(--muted);
      font-size: 12px;
    }}
    .case-list {{
      display: grid;
      gap: 8px;
    }}
    .case-button {{
      width: 100%;
      text-align: left;
      background: #ffffff;
      color: var(--ink);
      border: 1px solid var(--line);
      justify-content: flex-start;
      min-height: 48px;
    }}
    .case-button.active {{
      border-color: var(--accent);
      background: #eaf7f5;
    }}
    .case-button.complete::after {{
      content: "Done";
      margin-left: auto;
      font-size: 11px;
      color: var(--accent-dark);
    }}
    .layout {{
      display: grid;
      grid-template-columns: minmax(260px, 0.95fr) minmax(360px, 1.2fr);
      gap: 18px;
      align-items: start;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }}
    .panel h2 {{
      margin: 0 0 12px;
      font-size: 17px;
    }}
    .case-meta {{
      display: grid;
      gap: 10px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }}
    .case-meta b {{ color: var(--ink); }}
    .form-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(180px, 1fr));
      gap: 14px;
    }}
    .form-grid .wide {{ grid-column: 1 / -1; }}
    .status {{
      min-height: 22px;
      margin-top: 12px;
      font-size: 14px;
      color: var(--muted);
    }}
    .status.error {{ color: var(--danger); }}
    .actions {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 14px;
    }}
    @media (max-width: 900px) {{
      main, .layout {{ grid-template-columns: 1fr; }}
      aside {{ border-right: 0; border-bottom: 1px solid var(--line); max-height: 280px; }}
      .summary {{ grid-template-columns: repeat(2, minmax(120px, 1fr)); }}
    }}
    @media (max-width: 560px) {{
      header {{ align-items: flex-start; flex-direction: column; }}
      section {{ padding: 14px; }}
      .form-grid, .summary {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>MedFailBench Clinician Review</h1>
    <div class="topbar">
      <div>
        <label for="reviewer">Reviewer</label>
        <select id="reviewer"></select>
      </div>
      <a class="button ghost" href="/api/export.csv">CSV</a>
      <a class="button ghost" href="/api/export.json">JSON</a>
    </div>
  </header>
  <main>
    <aside>
      <div class="case-list" id="caseList"></div>
    </aside>
    <section>
      <div class="summary">
        <div class="metric"><strong id="completedMetric">0</strong><span>completed assignments</span></div>
        <div class="metric"><strong id="caseMetric">0</strong><span>synthetic cases</span></div>
        <div class="metric"><strong id="kappaMetric">NA</strong><span>R01 and R02 severity kappa</span></div>
        <div class="metric"><strong id="sharedMetric">0</strong><span>paired cases</span></div>
      </div>
      <div class="layout">
        <div class="panel">
          <h2 id="caseTitle">Select a case</h2>
          <div class="case-meta" id="caseMeta"></div>
        </div>
        <form class="panel" id="reviewForm">
          <h2>Review</h2>
          <div class="form-grid">
            <div>
              <label for="severity">Severity 1 to 5</label>
              <select id="severity" name="severity_1_to_5" required>
                <option value=""></option>
                <option value="1">1 minimal</option>
                <option value="2">2 low</option>
                <option value="3">3 moderate</option>
                <option value="4">4 high</option>
                <option value="5">5 severe</option>
              </select>
            </div>
            <div>
              <label for="confidence">Confidence 1 to 5</label>
              <select id="confidence" name="confidence" required>
                <option value=""></option>
                <option value="1">1 low</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5 high</option>
              </select>
            </div>
            <div>
              <label for="harm">Likely harm if copied</label>
              <select id="harm" name="likely_harm_if_copied" required>
                <option value=""></option>
                <option value="yes">yes</option>
                <option value="no">no</option>
                <option value="unclear">unclear</option>
              </select>
            </div>
            <div>
              <label for="stay">Keep in benchmark</label>
              <select id="stay" name="should_this_case_stay_in_benchmark" required>
                <option value=""></option>
                <option value="yes">yes</option>
                <option value="revise">revise</option>
                <option value="no">no</option>
              </select>
            </div>
            <div class="wide">
              <label for="gate">Missing safety gate</label>
              <input id="gate" name="missing_safety_gate" placeholder="Example: missed_urgent_escalation">
            </div>
            <div class="wide">
              <label for="tags">Failure tags</label>
              <input id="tags" name="failure_tags" placeholder="Comma separated tags">
            </div>
            <div>
              <label for="patientData">Possible patient data flag</label>
              <select id="patientData" name="possible_patient_data_flag">
                <option value="no">no</option>
                <option value="possible">possible</option>
                <option value="yes">yes</option>
              </select>
            </div>
            <div>
              <label for="language">Language</label>
              <input id="language" name="language">
            </div>
            <div class="wide">
              <label for="note">Free text note</label>
              <textarea id="note" name="free_text_note"></textarea>
            </div>
          </div>
          <div class="actions">
            <button type="submit">Save Review</button>
            <button type="button" class="ghost" id="nextButton">Next Case</button>
          </div>
          <div class="status" id="status"></div>
        </form>
      </div>
    </section>
  </main>
  <script>
    const defaultReviewer = {default_reviewer_json};
    let cases = [];
    let reviewers = [];
    let reviews = [];
    let selectedCaseId = "";

    const reviewerEl = document.getElementById("reviewer");
    const caseListEl = document.getElementById("caseList");
    const formEl = document.getElementById("reviewForm");
    const statusEl = document.getElementById("status");

    function reviewKey(row) {{
      return `${{row.panel_case_id}}::${{row.reviewer_code}}`;
    }}

    function selectedReviewer() {{
      return reviewerEl.value || defaultReviewer;
    }}

    function existingReview(caseId, reviewerCode) {{
      return reviews.find(row => row.panel_case_id === caseId && row.reviewer_code === reviewerCode);
    }}

    async function loadAll() {{
      const [caseResp, reviewerResp, reviewResp, summaryResp] = await Promise.all([
        fetch("/api/cases"),
        fetch("/api/reviewers"),
        fetch("/api/reviews"),
        fetch("/api/summary")
      ]);
      cases = await caseResp.json();
      reviewers = (await reviewerResp.json()).reviewers;
      reviews = (await reviewResp.json()).records;
      renderReviewers();
      selectedCaseId = selectedCaseId || (cases[0] && cases[0].panel_case_id) || "";
      renderCases();
      renderSelectedCase();
      renderSummary(await summaryResp.json());
    }}

    function renderReviewers() {{
      reviewerEl.innerHTML = reviewers.map(code => `<option value="${{code}}">${{code}}</option>`).join("");
      reviewerEl.value = reviewers.includes(defaultReviewer) ? defaultReviewer : reviewers[0];
    }}

    function renderCases() {{
      const reviewer = selectedReviewer();
      caseListEl.innerHTML = cases.map(item => {{
        const complete = existingReview(item.panel_case_id, reviewer) ? " complete" : "";
        const active = item.panel_case_id === selectedCaseId ? " active" : "";
        return `<button type="button" class="case-button${{complete}}${{active}}" data-case="${{item.panel_case_id}}">
          <span>${{item.panel_case_id}}<br><small>${{item.domain}}</small></span>
        </button>`;
      }}).join("");
      for (const button of caseListEl.querySelectorAll("button")) {{
        button.addEventListener("click", () => {{
          selectedCaseId = button.dataset.case;
          renderCases();
          renderSelectedCase();
        }});
      }}
    }}

    function renderSelectedCase() {{
      const item = cases.find(row => row.panel_case_id === selectedCaseId);
      if (!item) return;
      document.getElementById("caseTitle").textContent = `${{item.panel_case_id}} · ${{item.theme}}`;
      document.getElementById("caseMeta").innerHTML = `
        <div><b>Domain:</b> ${{item.domain}}</div>
        <div><b>Setting:</b> ${{item.setting}}</div>
        <div><b>Summary:</b> ${{item.synthetic_patient_summary}}</div>
        <div><b>Task:</b> ${{item.task_for_model}}</div>
        <div><b>Safety focus:</b> ${{item.expected_safety_focus}}</div>
        <div><b>Data status:</b> ${{item.patient_data_status}}</div>
      `;
      formEl.reset();
      document.getElementById("language").value = item.language;
      document.getElementById("patientData").value = "no";
      const existing = existingReview(selectedCaseId, selectedReviewer());
      if (existing) {{
        for (const field of new FormData(formEl).keys()) {{
          const element = formEl.elements[field];
          if (element && existing[field] !== undefined) element.value = existing[field];
        }}
      }}
      setStatus(existing ? `Loaded saved review from ${{existing.updated_at_utc}}` : "");
    }}

    function renderSummary(payload) {{
      const progress = payload.progress || {{}};
      const kappa = payload.severity_kappa || {{}};
      document.getElementById("completedMetric").textContent = `${{progress.completed_count || 0}}/${{progress.assignment_count || 0}}`;
      document.getElementById("caseMetric").textContent = progress.case_count || 0;
      document.getElementById("kappaMetric").textContent = kappa.kappa === null || kappa.kappa === undefined ? "NA" : kappa.kappa;
      document.getElementById("sharedMetric").textContent = kappa.n || 0;
    }}

    function setStatus(message, isError=false) {{
      statusEl.textContent = message;
      statusEl.classList.toggle("error", isError);
    }}

    formEl.addEventListener("submit", async event => {{
      event.preventDefault();
      const data = Object.fromEntries(new FormData(formEl).entries());
      data.panel_case_id = selectedCaseId;
      data.reviewer_code = selectedReviewer();
      const response = await fetch("/api/reviews", {{
        method: "POST",
        headers: {{"Content-Type": "application/json"}},
        body: JSON.stringify(data)
      }});
      const payload = await response.json();
      if (!response.ok) {{
        setStatus(payload.error || "Save failed", true);
        return;
      }}
      reviews = reviews.filter(row => reviewKey(row) !== reviewKey(payload.record));
      reviews.push(payload.record);
      renderCases();
      const summaryResp = await fetch("/api/summary");
      renderSummary(await summaryResp.json());
      setStatus(`Saved ${{payload.record.panel_case_id}} for ${{payload.record.reviewer_code}}`);
    }});

    document.getElementById("nextButton").addEventListener("click", () => {{
      const index = cases.findIndex(row => row.panel_case_id === selectedCaseId);
      selectedCaseId = cases[(index + 1) % cases.length].panel_case_id;
      renderCases();
      renderSelectedCase();
    }});

    reviewerEl.addEventListener("change", () => {{
      renderCases();
      renderSelectedCase();
    }});

    loadAll().catch(error => setStatus(error.message, true));
  </script>
</body>
</html>"""


if __name__ == "__main__":
    raise SystemExit(main())
