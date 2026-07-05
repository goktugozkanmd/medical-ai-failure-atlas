#!/usr/bin/env python3
"""Inter-rater reliability (Cohen's kappa + weighted kappa) for MedFailBench.

Reads two reviewer TSV files joined on case id and computes agreement on the
severity rating. Standard library only — no numpy/scipy dependency.

Usage:
    python scripts/interrater_kappa.py \\
        --reviewer1 data/inter_rater_review_subset_v0_1.tsv \\
        --reviewer2 data/inter_rater_reviewer2_form_v0_1.tsv \\
        --r1-col severity_r1 \\
        --r2-col r2_severity_1_to_5
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable


def load_column(path: Path, key_col: str, value_col: str) -> dict[str, str]:
    """Load {case_key: value} from a TSV. Skips rows with empty value."""
    out: dict[str, str] = {}
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if key_col not in reader.fieldnames:
            raise SystemExit(f"{path}: column {key_col!r} not found. Have: {reader.fieldnames}")
        if value_col not in reader.fieldnames:
            raise SystemExit(f"{path}: column {value_col!r} not found. Have: {reader.fieldnames}")
        for row in reader:
            key = (row.get(key_col) or "").strip()
            val = (row.get(value_col) or "").strip()
            if key and val:
                out[key] = val
    return out


def cohen_kappa(pairs: list[tuple[int, int]]) -> tuple[float, float]:
    """Return (unweighted Cohen's kappa, percent observed agreement)."""
    if not pairs:
        raise SystemExit("No overlapping rated cases — both files must share keys.")
    n = len(pairs)
    cats = sorted({a for a, _ in pairs} | {b for _, b in pairs})
    idx = {c: i for i, c in enumerate(cats)}
    k = len(cats)

    # Observed agreement
    agree = sum(1 for a, b in pairs if a == b)
    p_o = agree / n

    # Marginal counts
    r1_counts = [0] * k
    r2_counts = [0] * k
    for a, b in pairs:
        r1_counts[idx[a]] += 1
        r2_counts[idx[b]] += 1

    # Expected agreement by chance
    p_e = sum((r1_counts[i] / n) * (r2_counts[i] / n) for i in range(k))

    if p_e == 1.0:
        return 1.0, p_o
    kappa = (p_o - p_e) / (1 - p_e)
    return kappa, p_o


def weighted_kappa(pairs: list[tuple[int, int]]) -> float:
    """Quadratic weighted Cohen's kappa.

    Uses v_ij = (i-j)^2 disagreement weights. The weighted observed and
    expected agreement are computed from the marginal sums of the
    confusion matrix, following the standard Cohen (1968) definition.
    """
    if not pairs:
        raise SystemExit("No pairs.")
    n = len(pairs)
    cats = sorted({a for a, _ in pairs} | {b for _, b in pairs})
    if len(cats) < 2:
        return 1.0
    idx = {c: i for i, c in enumerate(cats)}
    k = len(cats)

    # Observed confusion matrix (counts)
    obs = [[0] * k for _ in range(k)]
    for a, b in pairs:
        obs[idx[a]][idx[b]] += 1

    # Marginals (as counts; converted to probabilities below)
    r1_marg = [sum(obs[i]) for i in range(k)]
    r2_marg = [sum(obs[i][j] for i in range(k)) for j in range(k)]

    # Quadratic weights: v_ij = (i-j)^2 (0 on diagonal, larger off-diagonal)
    num = 0.0
    den = 0.0
    for i in range(k):
        for j in range(k):
            v = (i - j) ** 2
            p_obs = obs[i][j] / n
            p_exp = (r1_marg[i] / n) * (r2_marg[j] / n)
            num += v * p_obs
            den += v * p_exp
    if den == 0:
        return 1.0
    return 1.0 - num / den


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--reviewer1", type=Path, required=True, help="Reviewer 1 TSV")
    p.add_argument("--reviewer2", type=Path, required=True, help="Reviewer 2 TSV")
    p.add_argument("--key", default="subset_id", help="Join key column name")
    p.add_argument("--r1-col", required=True, help="Severity column in reviewer 1 file")
    p.add_argument("--r2-col", required=True, help="Severity column in reviewer 2 file")
    args = p.parse_args()

    r1 = load_column(args.reviewer1, args.key, args.r1_col)
    r2 = load_column(args.reviewer2, args.key, args.r2_col)

    common = sorted(set(r1) & set(r2))
    only1 = sorted(set(r1) - set(r2))
    only2 = sorted(set(r2) - set(r1))
    print(f"Reviewer 1 rated: {len(r1)} cases")
    print(f"Reviewer 2 rated: {len(r2)} cases")
    print(f"Common (rated by both): {len(common)}")
    if only1:
        print(f"Only in reviewer 1 ({len(only1)}): {only1[:5]}")
    if only2:
        print(f"Only in reviewer 2 ({len(only2)}): {only2[:5]}")
    print()

    pairs: list[tuple[int, int]] = []
    parse_errors: list[str] = []
    for key in common:
        try:
            a = int(str(r1[key]).strip())
            b = int(str(r2[key]).strip())
            pairs.append((a, b))
        except ValueError:
            parse_errors.append(f"{key}: r1={r1[key]!r} r2={r2[key]!r} not integers")
    if parse_errors:
        print(f"Skipping {len(parse_errors)} rows with non-integer ratings:")
        for e in parse_errors[:5]:
            print(f"  {e}")
        print()
    if not pairs:
        print("No valid integer pairs to compute kappa. Reviewer 2 form may be empty.")
        return 1

    kappa, p_o = cohen_kappa(pairs)
    wk = weighted_kappa(pairs)

    print("=== Inter-rater reliability (severity) ===")
    print(f"Pairs used: {len(pairs)}")
    print(f"Observed agreement (exact): {p_o * 100:.1f}%")
    print(f"Cohen's kappa (unweighted): {kappa:.3f}")
    print(f"Cohen's kappa (quadratic weighted): {wk:.3f}")
    print()
    print("Interpretation (Landis-Koch):")
    if kappa < 0:
        print("  <0.00   poor")
    elif kappa < 0.20:
        print("  0.00-0.20 slight")
    elif kappa < 0.40:
        print("  0.21-0.40 fair")
    elif kappa < 0.60:
        print("  0.41-0.60 moderate")
    elif kappa < 0.80:
        print("  0.61-0.80 substantial")
    else:
        print("  0.81-1.00 almost perfect")
    return 0


if __name__ == "__main__":
    sys.exit(main())
