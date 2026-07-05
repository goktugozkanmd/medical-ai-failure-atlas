#!/usr/bin/env python3
"""Model provider submission CLI (closes #201).

Lets a model provider submit a HuggingFace model link, run the MedFailBench
rule-based eval against the v2_hard_30 prompt set, and append the result to
leaderboard/submissions.json with status 'pending review'.

This is the synchronous, local variant of the submission API. It uses the
same HF router + User-Agent + rule-based scorer as the weekly-eval CI job.
A queued / asynchronous version can wrap this later.

Usage:
    # Evaluate a model already configured in weekly_model_eval.py
    python scripts/submit_and_eval.py --model qwen-2.5-7b-instruct

    # Evaluate an arbitrary HF router model id (one-off)
    python scripts/submit_and_eval.py --hf-id meta-llama/Llama-3.1-8B-Instruct \\
        --display-name "Llama 3.1 8B"

Requires HF_TOKEN in the environment.

Output:
    - model_runs/weekly_eval_<slug>_<timestamp>.json (raw eval)
    - leaderboard/submissions.json (a new row appended)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBMISSIONS = ROOT / "leaderboard" / "submissions.json"
WEEKLY_EVAL = ROOT / "scripts" / "weekly_model_eval.py"
MODEL_RUNS = ROOT / "model_runs"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def hf_link_reachable(link: str, timeout: int = 15) -> tuple[bool, str]:
    """Return (reachable, http_status_string). Uses urllib to avoid deps."""
    import urllib.request, urllib.error
    try:
        req = urllib.request.Request(link, method="GET",
            headers={"User-Agent": "MedFailBench-submission/0.1"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return True, str(r.status)
    except urllib.error.HTTPError as e:
        # 200/302/403 still mean the page exists; 404 means gone
        return e.code in (200, 302, 401, 403), str(e.code)
    except Exception as e:
        return False, f"ERR:{type(e).__name__}"


def parse_eval_summary(path: Path) -> dict:
    """Pull the mean scores out of a weekly_eval_*.json file."""
    data = json.loads(path.read_text(encoding="utf-8"))
    results = data.get("prompt_results", [])
    if not results:
        raise SystemExit(f"No prompt_results in {path}")
    n = len(results)
    def mean(key):
        return sum(r["scores"].get(key, 0) for r in results) / n
    to100 = lambda v: round(v / 5 * 100, 1)
    return {
        "safety_score": to100(mean("safety")),
        "source_support_score": to100(mean("source_transparency")),
        "clinical_boundary_score": to100(mean("mean")),
        "prompt_count": n,
    }


def append_submission(store_path: Path, submission: dict) -> None:
    store = json.loads(store_path.read_text(encoding="utf-8"))
    submissions = store.get("submissions", [])
    submissions.insert(0, submission)
    store["submissions"] = submissions
    store["last_updated"] = submission["submitted_at"]
    store_path.write_text(json.dumps(store, indent=2), encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", help="Model key from weekly_model_eval.py CONFIGURED_MODELS")
    p.add_argument("--hf-id", help="One-off HF router model id (e.g. meta-llama/Llama-3.1-8B-Instruct)")
    p.add_argument("--display-name", help="Display name for one-off model")
    p.add_argument("--notes", default="Real auto-eval via scripts/submit_and_eval.py.")
    args = p.parse_args()

    if args.model and args.hf_id:
        p.error("Pass either --model or --hf-id, not both.")
    if not args.model and not args.hf_id:
        p.error("Required: --model <key> or --hf-id <hf-router-id>")

    if not Path.home().joinpath(".huggingface").exists() and "HF_TOKEN" not in __import__("os").environ:
        print("WARNING: HF_TOKEN not set; eval may fail with HTTP 401/403.", file=sys.stderr)

    # Step 1: run the eval (reuses weekly_model_eval.py)
    cmd = [sys.executable, str(WEEKLY_EVAL)]
    display_name = args.display_name or args.model
    hf_link = ""
    if args.model:
        cmd += ["--model", args.model]
        # Best-effort HF link for known configs
        try:
            sys.path.insert(0, str(ROOT / "scripts"))
            import weekly_model_eval as wme
            cfg = wme.CONFIGURED_MODELS.get(args.model, {})
            mid = cfg.get("model_id") or args.model
            if cfg.get("provider") == "huggingface" and mid:
                hf_link = f"https://huggingface.co/{mid}"
                display_name = display_name or mid.split("/")[-1]
        except Exception:
            pass
    else:
        # one-off: register temporarily via env injection isn't supported by the script,
        # so we evaluate via a small inline call
        print(f"One-off eval for {args.hf_id} not yet supported by this CLI; "
              f"please add the model to weekly_model_eval.py CONFIGURED_MODELS first.",
              file=sys.stderr)
        return 1

    print(f"Running eval: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(ROOT))
    if proc.returncode != 0:
        print(f"Eval failed (exit {proc.returncode}).", file=sys.stderr)
        return proc.returncode

    # Step 2: find the just-written eval file (weekly_model_eval.py writes
    # weekly_eval_<model_key>_<timestamp>.json — model_key keeps dots, so we
    # match by prefix and timestamp rather than slugified name)
    prefix = f"weekly_eval_{args.model}_"
    candidates = sorted(MODEL_RUNS.glob(f"{prefix}*.json"),
                        key=lambda p: p.stat().st_mtime)
    if not candidates:
        # fallback: match by leading chars of the model key
        loose = args.model.replace(".", "?")  # regex-ish not needed, just try
        candidates = sorted(MODEL_RUNS.glob(f"weekly_eval_{loose}_*.json"),
                            key=lambda p: p.stat().st_mtime)
    if not candidates:
        print(f"Could not find eval output file with prefix '{prefix}'.", file=sys.stderr)
        return 1
    eval_file = candidates[-1]
    print(f"Eval output: {eval_file.relative_to(ROOT)}")

    # Step 3: parse scores
    scores = parse_eval_summary(eval_file)

    # Step 4: HF link reachability (best-effort)
    reachable, status = (True, "200")
    if hf_link:
        reachable, status = hf_link_reachable(hf_link)

    # Step 5: build submission row (matches leaderboard/policy.py schema)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sub_id = hashlib.sha1(f"{args.model}-{eval_file.stem}".encode()).hexdigest()[:32]
    submission = {
        "id": sub_id,
        "model_name": display_name,
        "huggingface_link": hf_link,
        "benchmark_scores": {
            "safety_score": scores["safety_score"],
            "source_support_score": scores["source_support_score"],
            "clinical_boundary_score": scores["clinical_boundary_score"],
        },
        "notes": args.notes,
        "status": "pending review",
        "submitted_at": now,
        "first_submitted_at": now,
        "huggingface_reachable": reachable,
        "huggingface_status": status,
    }

    # Step 6: append to store
    if not SUBMISSIONS.exists():
        SUBMISSIONS.write_text(json.dumps({"last_updated": now, "submissions": []}, indent=2), encoding="utf-8")
    append_submission(SUBMISSIONS, submission)

    print("\n=== Submission added ===")
    print(json.dumps(submission, indent=2))
    print(f"\nStore: {SUBMISSIONS.relative_to(ROOT)}")
    print("Status: pending review. Clinician review is required before any public claim.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
