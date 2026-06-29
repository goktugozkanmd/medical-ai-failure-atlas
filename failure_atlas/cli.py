from __future__ import annotations

import argparse

from failure_atlas.reporter import write_comparison_markdown, write_csv_summary, write_report_bundle
from failure_atlas.runner import ModelConfig, load_model_configs, run_batch
from failure_atlas.scorer import score_raw_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Medical AI Failure Atlas benchmark tools.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a prompt set against one or more models.")
    run_parser.add_argument("--prompt-set", required=True)
    run_parser.add_argument("--model", action="append", help="Model name. Repeat for batch mode.")
    run_parser.add_argument("--model-config", help="JSON file containing one model config object list or a models list.")
    run_parser.add_argument("--endpoint", default="https://api.openai.com/v1/chat/completions")
    run_parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    run_parser.add_argument("--temperature", type=float, default=0.0)
    run_parser.add_argument("--max-tokens", type=int, default=1024)
    run_parser.add_argument("--requests-per-minute", type=float, default=60.0)
    run_parser.add_argument("--timeout-seconds", type=float, default=60.0)
    run_parser.add_argument("--max-retries", type=int, default=3)
    run_parser.add_argument("--backoff-seconds", type=float, default=1.0)
    run_parser.add_argument("--system-prompt")
    run_parser.add_argument("--out-dir", default="outputs/raw")
    run_parser.add_argument("--run-id")
    run_parser.add_argument("--continue-on-error", action="store_true")
    run_parser.set_defaults(func=run_command)

    score_parser = subparsers.add_parser("score", help="Score raw model outputs.")
    score_parser.add_argument("--raw", required=True)
    score_parser.add_argument("--rubric", default="data/scoring_rubric_v0_3.json")
    score_parser.add_argument("--out", required=True)
    score_parser.add_argument("--method", choices=("rule", "judge"), default="rule")
    score_parser.add_argument("--judge-model")
    score_parser.add_argument("--judge-endpoint", default="https://api.openai.com/v1/chat/completions")
    score_parser.add_argument("--judge-api-key-env", default="OPENAI_API_KEY")
    score_parser.add_argument("--judge-temperature", type=float, default=0.0)
    score_parser.add_argument("--judge-max-tokens", type=int, default=1200)
    score_parser.set_defaults(func=score_command)

    report_parser = subparsers.add_parser("report", help="Generate Markdown, JSON, and CSV report files from scores.")
    report_parser.add_argument("--scores", required=True)
    report_parser.add_argument("--out-dir", required=True)
    report_parser.add_argument("--stem")
    report_parser.set_defaults(func=report_command)

    compare_parser = subparsers.add_parser("compare", help="Compare multiple score JSON files.")
    compare_parser.add_argument("--scores", action="append", required=True)
    compare_parser.add_argument("--out-csv", required=True)
    compare_parser.add_argument("--out-md")
    compare_parser.set_defaults(func=compare_command)

    return parser


def run_command(args: argparse.Namespace) -> int:
    configs = _configs_from_args(args)
    results = run_batch(
        configs=configs,
        prompt_path=args.prompt_set,
        output_dir=args.out_dir,
        run_id=args.run_id,
        continue_on_error=args.continue_on_error,
    )
    for result in results:
        print(result.raw_path)
    return 0


def score_command(args: argparse.Namespace) -> int:
    judge_config = None
    if args.method == "judge":
        if not args.judge_model:
            raise SystemExit("--judge-model is required when --method judge is used")
        judge_config = ModelConfig(
            name=args.judge_model,
            api_endpoint=args.judge_endpoint,
            api_key_env=args.judge_api_key_env,
            temperature=args.judge_temperature,
            max_tokens=args.judge_max_tokens,
        )
    score_raw_output(
        raw_path=args.raw,
        rubric_path=args.rubric,
        method=args.method,
        judge_config=judge_config,
        output_path=args.out,
    )
    print(args.out)
    return 0


def report_command(args: argparse.Namespace) -> int:
    from failure_atlas.reporter import load_score_file

    scores = load_score_file(args.scores)
    paths = write_report_bundle(scores=scores, output_dir=args.out_dir, stem=args.stem)
    for path in paths.values():
        print(path)
    return 0


def compare_command(args: argparse.Namespace) -> int:
    write_csv_summary(args.scores, args.out_csv)
    print(args.out_csv)
    if args.out_md:
        write_comparison_markdown(args.scores, args.out_md)
        print(args.out_md)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


def _configs_from_args(args: argparse.Namespace) -> list[ModelConfig]:
    if args.model_config:
        return load_model_configs(args.model_config)
    if not args.model:
        raise SystemExit("Provide --model or --model-config")
    return [
        ModelConfig(
            name=name,
            api_endpoint=args.endpoint,
            api_key_env=args.api_key_env,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            requests_per_minute=args.requests_per_minute,
            timeout_seconds=args.timeout_seconds,
            max_retries=args.max_retries,
            backoff_seconds=args.backoff_seconds,
            system_prompt=args.system_prompt,
        )
        for name in args.model
    ]


if __name__ == "__main__":
    raise SystemExit(main())
