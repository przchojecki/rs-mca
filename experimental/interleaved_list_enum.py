#!/usr/bin/env python3
"""Directly enumerate tiny interleaved Reed-Solomon lists.

For each received row, the script enumerates all degree-<k codewords over F_p,
records the agreement support as a bitmask, and counts interleaved tuples by
intersecting those masks.  This gives an exact tiny-parameter comparison with
the trivial product bound L_mu <= L_1^mu.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
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


def parse_int_list(text: str) -> list[int]:
    try:
        values = [int(part.strip()) for part in text.split(",") if part.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a comma-separated integer list") from exc
    if not values:
        raise argparse.ArgumentTypeError("expected a nonempty integer list")
    return values


def parse_rows(text: str) -> list[list[int]]:
    rows = [parse_int_list(part) for part in text.split(";") if part.strip()]
    if not rows:
        raise argparse.ArgumentTypeError("expected at least one row")
    return rows


def subgroup_domain(generator: int, order: int, prime: int) -> list[int]:
    domain = [pow(generator, index, prime) for index in range(order)]
    if len(set(domain)) != order or pow(generator, order, prime) != 1:
        raise ValueError("subgroup generator does not have the requested order")
    return domain


def eval_poly(coeffs: list[int], x_value: int, prime: int) -> int:
    value = 0
    for coeff in reversed(coeffs):
        value = (value * x_value + coeff) % prime
    return value


def eval_received_polys(
    coeff_rows: list[list[int]], domain: list[int], prime: int
) -> list[list[int]]:
    return [
        [eval_poly([coeff % prime for coeff in coeffs], x_value, prime) for x_value in domain]
        for coeffs in coeff_rows
    ]


def normalize_value_rows(rows: list[list[int]], domain_size: int, prime: int) -> list[list[int]]:
    normalized = []
    for row in rows:
        if len(row) != domain_size:
            raise ValueError("every received value row must have length |domain|")
        normalized.append([value % prime for value in row])
    return normalized


def codeword_count(prime: int, dimension: int) -> int:
    return prime**dimension


def agreement_histograms(
    prime: int,
    dimension: int,
    domain: list[int],
    received_rows: list[list[int]],
    max_codewords: int,
) -> list[Counter[int]]:
    total = codeword_count(prime, dimension)
    if total > max_codewords:
        raise ValueError(
            f"refusing to enumerate {total} codewords; raise --max-codewords if intended"
        )

    histograms = [Counter() for _ in received_rows]
    domain_size = len(domain)
    for coeffs_tuple in itertools.product(range(prime), repeat=dimension):
        coeffs = list(coeffs_tuple)
        values = [eval_poly(coeffs, x_value, prime) for x_value in domain]
        for row_index, received in enumerate(received_rows):
            mask = 0
            for pos in range(domain_size):
                if values[pos] == received[pos]:
                    mask |= 1 << pos
            histograms[row_index][mask] += 1
    return histograms


def count_base_list(histogram: Counter[int], agreement: int) -> int:
    return sum(count for mask, count in histogram.items() if mask.bit_count() >= agreement)


def count_interleaved(
    histograms: list[Counter[int]], agreement: int, domain_size: int
) -> int:
    combined: Counter[int] = Counter({(1 << domain_size) - 1: 1})
    for histogram in histograms:
        next_combined: Counter[int] = Counter()
        for current_mask, current_count in combined.items():
            for row_mask, row_count in histogram.items():
                next_combined[current_mask & row_mask] += current_count * row_count
        combined = next_combined
    return sum(count for mask, count in combined.items() if mask.bit_count() >= agreement)


def top_masks(histogram: Counter[int], limit: int) -> list[dict[str, int]]:
    return [
        {
            "mask": mask,
            "agreement_size": mask.bit_count(),
            "count": count,
        }
        for mask, count in histogram.most_common(limit)
    ]


def compute_report(args: argparse.Namespace) -> dict[str, Any]:
    if args.domain is not None and args.subgroup_generator is not None:
        raise ValueError("use either --domain or --subgroup-generator, not both")
    if args.domain is None and args.subgroup_generator is None:
        raise ValueError("provide --domain or --subgroup-generator/--subgroup-order")
    if args.row_polys is not None and args.row_values is not None:
        raise ValueError("use either --row-polys or --row-values, not both")
    if args.row_polys is None and args.row_values is None:
        raise ValueError("provide --row-polys or --row-values")

    if args.domain is not None:
        domain = [value % args.p for value in args.domain]
    else:
        if args.subgroup_order is None:
            raise ValueError("--subgroup-generator requires --subgroup-order")
        domain = subgroup_domain(args.subgroup_generator % args.p, args.subgroup_order, args.p)

    if len(set(domain)) != len(domain):
        raise ValueError("domain values must be distinct modulo p")
    if args.agreement > len(domain):
        raise ValueError("--agreement cannot exceed |domain|")

    if args.row_polys is not None:
        received_rows = eval_received_polys(args.row_polys, domain, args.p)
        row_source = "polynomial_coefficients"
    else:
        received_rows = normalize_value_rows(args.row_values, len(domain), args.p)
        row_source = "explicit_values"

    histograms = agreement_histograms(
        prime=args.p,
        dimension=args.k,
        domain=domain,
        received_rows=received_rows,
        max_codewords=args.max_codewords,
    )
    base_counts = [count_base_list(histogram, args.agreement) for histogram in histograms]
    product_bound = math.prod(base_counts)
    direct_count = count_interleaved(histograms, args.agreement, len(domain))
    ratio = None if product_bound == 0 else direct_count / product_bound

    return {
        "p": args.p,
        "domain": domain,
        "n": len(domain),
        "k": args.k,
        "agreement": args.agreement,
        "row_count": len(received_rows),
        "row_source": row_source,
        "codeword_count_per_row": codeword_count(args.p, args.k),
        "base_list_counts": base_counts,
        "trivial_product_bound": product_bound,
        "direct_interleaved_count": direct_count,
        "direct_to_product_ratio": ratio,
        "support_mask_counts": [len(histogram) for histogram in histograms],
        "top_masks": [
            top_masks(histogram, args.show_masks) for histogram in histograms
        ]
        if args.show_masks
        else [],
    }


def print_report(report: dict[str, Any]) -> None:
    print(
        "p={p} n={n} k={k} agreement={agreement} rows={rows}".format(
            p=report["p"],
            n=report["n"],
            k=report["k"],
            agreement=report["agreement"],
            rows=report["row_count"],
        )
    )
    print(f"codewords per row: {report['codeword_count_per_row']}")
    print(f"base list counts: {report['base_list_counts']}")
    print(f"trivial product bound: {report['trivial_product_bound']}")
    print(f"direct interleaved count: {report['direct_interleaved_count']}")
    ratio = report["direct_to_product_ratio"]
    print("direct/product ratio: " + ("undefined" if ratio is None else f"{ratio:.6g}"))
    print(f"support masks per row: {report['support_mask_counts']}")

    if report["top_masks"]:
        print()
        for index, masks in enumerate(report["top_masks"], start=1):
            print(f"row {index} top masks")
            for item in masks:
                print(
                    "  mask={mask} agreement={agreement_size} count={count}".format(
                        **item
                    )
                )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Enumerate tiny interleaved RS lists by agreement masks."
    )
    parser.add_argument("--p", type=positive_int, required=True, help="prime field")
    parser.add_argument("--k", type=positive_int, required=True, help="RS dimension")
    parser.add_argument(
        "--agreement",
        type=positive_int,
        required=True,
        help="minimum common agreement columns",
    )
    parser.add_argument(
        "--domain",
        type=parse_int_list,
        help="comma-separated domain values modulo p",
    )
    parser.add_argument(
        "--subgroup-generator",
        type=positive_int,
        help="generator for a multiplicative subgroup domain",
    )
    parser.add_argument(
        "--subgroup-order",
        type=positive_int,
        help="order of the subgroup domain",
    )
    parser.add_argument(
        "--row-polys",
        type=parse_rows,
        help="semicolon-separated rows of low-to-high polynomial coefficients",
    )
    parser.add_argument(
        "--row-values",
        type=parse_rows,
        help="semicolon-separated rows of explicit received values",
    )
    parser.add_argument(
        "--max-codewords",
        type=positive_int,
        default=1_000_000,
        help="safety cap for enumerated codewords p^k",
    )
    parser.add_argument(
        "--show-masks",
        type=nonnegative_int,
        default=0,
        help="show the most common support masks per row",
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
