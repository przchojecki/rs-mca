#!/usr/bin/env python3
"""Verify the M2 close-point versus support-wise separation on a tiny RS code."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from typing import Any


def positive_int(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def nonnegative_int(text: str) -> int:
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError("expected a nonnegative integer")
    return value


def eval_poly(coeffs: tuple[int, ...], x_value: int, prime: int) -> int:
    value = 0
    for coeff in reversed(coeffs):
        value = (value * x_value + coeff) % prime
    return value


def codewords(prime: int, dimension: int, domain: list[int]) -> set[tuple[int, ...]]:
    words: set[tuple[int, ...]] = set()
    for coeffs in itertools.product(range(prime), repeat=dimension):
        words.add(tuple(eval_poly(coeffs, x_value, prime) for x_value in domain))
    return words


def restriction(word: tuple[int, ...], support: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(word[index] for index in support)


def restriction_tables(
    words: set[tuple[int, ...]], supports: list[tuple[int, ...]]
) -> list[set[tuple[int, ...]]]:
    tables = []
    for support in supports:
        tables.append({restriction(word, support) for word in words})
    return tables


def scan_supports(
    f: tuple[int, ...],
    g: tuple[int, ...],
    prime: int,
    supports: list[tuple[int, ...]],
    support_codes: list[set[tuple[int, ...]]],
) -> tuple[list[int], list[int], list[tuple[tuple[int, ...], int]]]:
    close_slopes: list[int] = []
    noncontained_slopes: list[int] = []
    witness_pairs: list[tuple[tuple[int, ...], int]] = []

    for slope in range(prime):
        line_word = tuple((fv + slope * gv) % prime for fv, gv in zip(f, g))
        close = False
        noncontained = False
        for support, code_restrictions in zip(supports, support_codes):
            if restriction(line_word, support) not in code_restrictions:
                continue
            close = True
            contained = (
                restriction(f, support) in code_restrictions
                and restriction(g, support) in code_restrictions
            )
            if not contained:
                noncontained = True
                witness_pairs.append((support, slope))
        if close:
            close_slopes.append(slope)
        if noncontained:
            noncontained_slopes.append(slope)

    return close_slopes, noncontained_slopes, witness_pairs


def witness_summary(
    witness_pairs: list[tuple[tuple[int, ...], int]]
) -> dict[str, Any]:
    witness_fibers = Counter(slope for _, slope in witness_pairs)
    witness_supports_by_slope = {
        slope: [
            list(support)
            for support, item_slope in witness_pairs
            if item_slope == slope
        ]
        for slope in sorted(witness_fibers)
    }
    witness_pair_count = len(witness_pairs)
    projected_witness_slopes = sorted(witness_fibers)
    minimum_witness_multiplicity = (
        min(witness_fibers.values()) if witness_fibers else 0
    )
    multiplicity_bound = (
        None
        if minimum_witness_multiplicity == 0
        else witness_pair_count // minimum_witness_multiplicity
    )

    return {
        "witness_pair_count": witness_pair_count,
        "projected_witness_slopes": projected_witness_slopes,
        "witness_support_count_by_slope": dict(sorted(witness_fibers.items())),
        "witness_supports_by_slope": witness_supports_by_slope,
        "minimum_witness_multiplicity": minimum_witness_multiplicity,
        "projection_bound": witness_pair_count,
        "multiplicity_bound": multiplicity_bound,
    }


def compute_report(args: argparse.Namespace) -> dict[str, Any]:
    if args.n >= args.p:
        raise ValueError("use n < p for the default distinct domain 0,...,n-1")
    if args.k > args.n - 2:
        raise ValueError("the spike separation requires k <= n-2")
    if args.spike_index >= args.n:
        raise ValueError("--spike-index must be less than n")

    domain = list(range(args.n))
    agreement = args.n - 1
    exact_supports = list(itertools.combinations(range(args.n), agreement))
    large_supports = [
        support
        for size in range(agreement, args.n + 1)
        for support in itertools.combinations(range(args.n), size)
    ]
    words = codewords(args.p, args.k, domain)
    full_code = words
    exact_support_codes = restriction_tables(words, exact_supports)
    large_support_codes = restriction_tables(words, large_supports)

    spike = [0] * args.n
    spike[args.spike_index] = 1
    h = tuple(spike)
    f = tuple((args.base_slope * value) % args.p for value in h)
    g = h

    close_slopes, exact_noncontained_slopes, exact_witness_pairs = scan_supports(
        f, g, args.p, exact_supports, exact_support_codes
    )
    _, noncontained_slopes, witness_pairs = scan_supports(
        f, g, args.p, large_supports, large_support_codes
    )
    exact_summary = witness_summary(exact_witness_pairs)
    large_summary = witness_summary(witness_pairs)

    line_contained = all(
        tuple((fv + slope * gv) % args.p for fv, gv in zip(f, g)) in full_code
        for slope in range(args.p)
    )
    exceptional_slope = (-args.base_slope) % args.p
    code_line_support_size = args.n - 1
    outside_size = args.n - code_line_support_size
    residual_threshold = max(1, agreement - code_line_support_size)
    common_residual_zero_count = 0
    residual_bound = (
        (outside_size - common_residual_zero_count)
        // (residual_threshold - common_residual_zero_count)
    )

    return {
        "p": args.p,
        "n": args.n,
        "k": args.k,
        "agreement": agreement,
        "delta": f"1/{args.n}",
        "domain": domain,
        "spike_index": args.spike_index,
        "base_slope": args.base_slope,
        "exceptional_slope": exceptional_slope,
        "line_contained_in_code": line_contained,
        "code_line_exception_support_size": code_line_support_size,
        "residual_outside_size": outside_size,
        "residual_threshold": residual_threshold,
        "common_residual_zero_count": common_residual_zero_count,
        "residual_bound": residual_bound,
        "close_point_slope_count": len(close_slopes),
        "supportwise_noncontained_slope_count": len(noncontained_slopes),
        "exact_supportwise_noncontained_slope_count": len(
            exact_noncontained_slopes
        ),
        "supportwise_witness_pair_count": large_summary["witness_pair_count"],
        "exact_supportwise_witness_pair_count": exact_summary[
            "witness_pair_count"
        ],
        "projected_witness_slopes": large_summary["projected_witness_slopes"],
        "exact_projected_witness_slopes": exact_summary[
            "projected_witness_slopes"
        ],
        "witness_support_count_by_slope": large_summary[
            "witness_support_count_by_slope"
        ],
        "exact_witness_support_count_by_slope": exact_summary[
            "witness_support_count_by_slope"
        ],
        "witness_supports_by_slope": large_summary["witness_supports_by_slope"],
        "exact_witness_supports_by_slope": exact_summary[
            "witness_supports_by_slope"
        ],
        "minimum_witness_multiplicity": large_summary[
            "minimum_witness_multiplicity"
        ],
        "exact_minimum_witness_multiplicity": exact_summary[
            "minimum_witness_multiplicity"
        ],
        "projection_bound": large_summary["projection_bound"],
        "exact_projection_bound": exact_summary["projection_bound"],
        "multiplicity_bound": large_summary["multiplicity_bound"],
        "exact_multiplicity_bound": exact_summary["multiplicity_bound"],
        "close_point_slopes": close_slopes,
        "supportwise_noncontained_slopes": noncontained_slopes,
        "exact_supportwise_noncontained_slopes": exact_noncontained_slopes,
        "expected_close_point_slope_count": args.p,
        "expected_supportwise_noncontained_slopes": [exceptional_slope],
        "matches_claim": (
            close_slopes == list(range(args.p))
            and noncontained_slopes == [exceptional_slope]
            and exact_noncontained_slopes == [exceptional_slope]
            and large_summary["projected_witness_slopes"] == [exceptional_slope]
            and exact_summary["projected_witness_slopes"] == [exceptional_slope]
            and large_summary["witness_pair_count"] == args.n
            and exact_summary["witness_pair_count"] == args.n - 1
            and large_summary["multiplicity_bound"] == 1
            and exact_summary["multiplicity_bound"] == 1
            and not line_contained
            and residual_bound == len(noncontained_slopes)
        ),
    }


def print_report(report: dict[str, Any]) -> None:
    print(
        "p={p} n={n} k={k} agreement={agreement} delta={delta}".format(
            **report
        )
    )
    print(f"line contained in code: {report['line_contained_in_code']}")
    print(f"close-point slopes: {report['close_point_slope_count']}")
    print(
        "support-wise noncontained slopes: "
        f"{report['supportwise_noncontained_slope_count']}"
    )
    print(
        "exact-support noncontained slopes: "
        f"{report['exact_supportwise_noncontained_slope_count']}"
    )
    print(f"support-wise witness pairs: {report['supportwise_witness_pair_count']}")
    print(
        "exact-support witness pairs: "
        f"{report['exact_supportwise_witness_pair_count']}"
    )
    print(f"projection bound: {report['projection_bound']}")
    print(f"exact projection bound: {report['exact_projection_bound']}")
    print(f"multiplicity bound: {report['multiplicity_bound']}")
    print(f"exact multiplicity bound: {report['exact_multiplicity_bound']}")
    print(f"residual bound from code-line exception: {report['residual_bound']}")
    print(f"exceptional slope: {report['exceptional_slope']}")
    print(f"matches claim: {report['matches_claim']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify the RS spike-line M2 separation."
    )
    parser.add_argument("--p", type=positive_int, default=17, help="prime field")
    parser.add_argument("--n", type=positive_int, default=8, help="domain size")
    parser.add_argument("--k", type=positive_int, default=3, help="RS dimension")
    parser.add_argument(
        "--spike-index",
        type=nonnegative_int,
        default=0,
        help="coordinate carrying the one-point spike",
    )
    parser.add_argument(
        "--base-slope",
        type=nonnegative_int,
        default=5,
        help="scalar lambda for f=lambda*h, reduced modulo p",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.base_slope %= args.p
    try:
        report = compute_report(args)
    except ValueError as exc:
        parser.error(str(exc))

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
