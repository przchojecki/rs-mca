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
from fractions import Fraction
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
        raise argparse.ArgumentTypeError(
            "expected a comma-separated integer list"
        ) from exc
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
        [
            eval_poly([coeff % prime for coeff in coeffs], x_value, prime)
            for x_value in domain
        ]
        for coeffs in coeff_rows
    ]


def normalize_value_rows(
    rows: list[list[int]], domain_size: int, prime: int
) -> list[list[int]]:
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
            f"refusing to enumerate {total} codewords; "
            "raise --max-codewords if intended"
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
    return sum(
        count for mask, count in histogram.items() if mask.bit_count() >= agreement
    )


def count_raw_base_fiber(histogram: Counter[int], agreement: int) -> int:
    return sum(
        count * math.comb(mask.bit_count(), agreement)
        for mask, count in histogram.items()
        if mask.bit_count() >= agreement
    )


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
    return sum(
        count for mask, count in combined.items() if mask.bit_count() >= agreement
    )


def count_raw_simultaneous_fiber(
    histograms: list[Counter[int]], agreement: int, domain_size: int
) -> int:
    combined: Counter[int] = Counter({(1 << domain_size) - 1: 1})
    for histogram in histograms:
        next_combined: Counter[int] = Counter()
        for current_mask, current_count in combined.items():
            for row_mask, row_count in histogram.items():
                next_combined[current_mask & row_mask] += current_count * row_count
        combined = next_combined
    return sum(
        count * math.comb(mask.bit_count(), agreement)
        for mask, count in combined.items()
        if mask.bit_count() >= agreement
    )


def common_intersection_histogram(
    histograms: list[Counter[int]], domain_size: int
) -> Counter[int]:
    combined: Counter[int] = Counter({(1 << domain_size) - 1: 1})
    for histogram in histograms:
        next_combined: Counter[int] = Counter()
        for current_mask, current_count in combined.items():
            for row_mask, row_count in histogram.items():
                next_combined[current_mask & row_mask] += current_count * row_count
        combined = next_combined
    histogram: Counter[int] = Counter()
    for mask, count in combined.items():
        if count:
            histogram[mask.bit_count()] += count
    return histogram


def max_two_row_codegrees(
    histograms: list[Counter[int]], agreement: int
) -> dict[str, int] | None:
    if len(histograms) != 2:
        return None

    left, right = histograms
    left_max = 0
    for left_mask in left:
        compatible = sum(
            count
            for right_mask, count in right.items()
            if (left_mask & right_mask).bit_count() >= agreement
        )
        left_max = max(left_max, compatible)

    right_max = 0
    for right_mask in right:
        compatible = sum(
            count
            for left_mask, count in left.items()
            if (left_mask & right_mask).bit_count() >= agreement
        )
        right_max = max(right_max, compatible)

    return {
        "left_to_right": left_max,
        "right_to_left": right_max,
    }


def support_size_histogram(
    histogram: Counter[int], agreement: int
) -> Counter[int]:
    sizes: Counter[int] = Counter()
    for mask, count in histogram.items():
        support_size = mask.bit_count()
        if support_size >= agreement:
            sizes[support_size] += count
    return sizes


def johnson_neighborhood_size(
    domain_size: int, agreement: int, support_size: int, max_excess: int
) -> int:
    if support_size < agreement:
        return 0
    if support_size > agreement + max_excess:
        raise ValueError("support_size exceeds agreement + max_excess")

    excess = support_size - agreement
    outside_size = domain_size - support_size
    total = 0
    for removed in range(excess + 1):
        max_added = max_excess - excess + removed
        for added in range(min(outside_size, max_added) + 1):
            total += (
                math.comb(support_size, removed)
                * math.comb(outside_size, added)
            )
    return total


def near_exact_johnson_bound(
    histograms: list[Counter[int]],
    agreement: int,
    dimension: int,
    domain_size: int,
) -> dict[str, Any]:
    support_sizes = [
        support_size_histogram(histogram, agreement) for histogram in histograms
    ]
    listed_supports = [sum(histogram.values()) for histogram in support_sizes]

    if any(count == 0 for count in listed_supports):
        return {
            "status": "proved",
            "reason": "some row has no listed supports",
            "max_excess": None,
            "support_size_histograms": [
                dict(sorted(histogram.items())) for histogram in support_sizes
            ],
            "bound": 0,
            "row_bounds": [],
            "neighborhood_sizes": {},
        }

    if agreement < dimension:
        return {
            "status": "not_applicable",
            "reason": "requires agreement >= k for support injectivity",
            "max_excess": None,
            "support_size_histograms": [
                dict(sorted(histogram.items())) for histogram in support_sizes
            ],
            "bound": None,
            "row_bounds": [],
            "neighborhood_sizes": {},
        }

    if any(
        count != 1
        for histogram in histograms
        for mask, count in histogram.items()
        if mask.bit_count() >= agreement
    ):
        return {
            "status": "not_applicable",
            "reason": "listed agreement supports are not injective",
            "max_excess": None,
            "support_size_histograms": [
                dict(sorted(histogram.items())) for histogram in support_sizes
            ],
            "bound": None,
            "row_bounds": [],
            "neighborhood_sizes": {},
        }

    max_excess = max(
        support_size - agreement
        for histogram in support_sizes
        for support_size in histogram
    )
    neighborhood_sizes = {
        support_size: johnson_neighborhood_size(
            domain_size, agreement, support_size, max_excess
        )
        for support_size in range(agreement, agreement + max_excess + 1)
    }
    row_bounds = []
    row_count = len(histograms)
    for histogram in support_sizes:
        row_bounds.append(
            sum(
                count * neighborhood_sizes[support_size] ** (row_count - 1)
                for support_size, count in histogram.items()
            )
        )

    return {
        "status": "proved",
        "reason": "all listed supports have size in [a,a+c]",
        "max_excess": max_excess,
        "support_size_histograms": [
            dict(sorted(histogram.items())) for histogram in support_sizes
        ],
        "bound": min(row_bounds),
        "row_bounds": row_bounds,
        "neighborhood_sizes": dict(sorted(neighborhood_sizes.items())),
    }


def johnson_layer_kernel(
    domain_size: int, agreement: int, anchor_size: int, support_size: int
) -> int:
    if agreement > min(anchor_size, support_size):
        return 0

    outside_anchor = domain_size - anchor_size
    total = 0
    for intersection_size in range(agreement, min(anchor_size, support_size) + 1):
        outside_size = support_size - intersection_size
        if outside_size <= outside_anchor:
            total += (
                math.comb(anchor_size, intersection_size)
                * math.comb(outside_anchor, outside_size)
            )
    return total


def layered_johnson_bound(
    histograms: list[Counter[int]],
    agreement: int,
    dimension: int,
    domain_size: int,
) -> dict[str, Any]:
    support_layers = [
        support_size_histogram(histogram, agreement) for histogram in histograms
    ]
    listed_supports = [sum(histogram.values()) for histogram in support_layers]

    if any(count == 0 for count in listed_supports):
        return {
            "status": "proved",
            "reason": "some row has no listed supports",
            "support_size_histograms": [
                dict(sorted(histogram.items())) for histogram in support_layers
            ],
            "bound": 0,
            "row_bounds": [],
            "kernel_by_anchor_size": {},
        }

    if agreement < dimension:
        return {
            "status": "not_applicable",
            "reason": "requires agreement >= k for support injectivity",
            "support_size_histograms": [
                dict(sorted(histogram.items())) for histogram in support_layers
            ],
            "bound": None,
            "row_bounds": [],
            "kernel_by_anchor_size": {},
        }

    if any(
        count != 1
        for histogram in histograms
        for mask, count in histogram.items()
        if mask.bit_count() >= agreement
    ):
        return {
            "status": "not_applicable",
            "reason": "listed agreement supports are not injective",
            "support_size_histograms": [
                dict(sorted(histogram.items())) for histogram in support_layers
            ],
            "bound": None,
            "row_bounds": [],
            "kernel_by_anchor_size": {},
        }

    all_sizes = sorted(
        {
            support_size
            for histogram in support_layers
            for support_size in histogram
        }
    )
    kernel_by_anchor_size = {
        anchor_size: {
            support_size: johnson_layer_kernel(
                domain_size, agreement, anchor_size, support_size
            )
            for support_size in all_sizes
        }
        for anchor_size in all_sizes
    }

    row_bounds = []
    for anchor_index, anchor_layers in enumerate(support_layers):
        row_total = 0
        for anchor_size, anchor_count in anchor_layers.items():
            completion_bound = 1
            for other_index, other_layers in enumerate(support_layers):
                if other_index == anchor_index:
                    continue
                layer_sum = sum(
                    min(
                        support_count,
                        kernel_by_anchor_size[anchor_size][support_size],
                    )
                    for support_size, support_count in other_layers.items()
                )
                completion_bound *= layer_sum
            row_total += anchor_count * completion_bound
        row_bounds.append(row_total)

    return {
        "status": "proved",
        "reason": "bounded by support-size layer counts",
        "support_size_histograms": [
            dict(sorted(histogram.items())) for histogram in support_layers
        ],
        "bound": min(row_bounds),
        "row_bounds": row_bounds,
        "kernel_by_anchor_size": {
            anchor_size: dict(sorted(kernel.items()))
            for anchor_size, kernel in sorted(kernel_by_anchor_size.items())
        },
    }


def binomial_tail_probability(
    trials: int, success_denominator: int, threshold: int
) -> Fraction:
    total = Fraction(0, 1)
    failure = success_denominator - 1
    denominator = success_denominator**trials
    for hits in range(threshold, trials + 1):
        numerator = math.comb(trials, hits) * failure ** (trials - hits)
        total += Fraction(numerator, denominator)
    return total


def fraction_payload(value: Fraction) -> dict[str, int | str | float | None]:
    try:
        decimal: float | None = float(value)
    except OverflowError:
        decimal = None
    return {
        "exact": str(value),
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": decimal,
    }


def random_received_baseline(
    prime: int, dimension: int, domain_size: int, agreement: int, row_count: int
) -> dict[str, Any]:
    base_tail = binomial_tail_probability(domain_size, prime, agreement)
    direct_tail = binomial_tail_probability(
        domain_size, prime**row_count, agreement
    )
    expected_base = Fraction(prime**dimension, 1) * base_tail
    expected_direct = Fraction(prime ** (dimension * row_count), 1) * direct_tail
    expected_product = expected_base**row_count
    product_to_direct = (
        None if expected_direct == 0 else expected_product / expected_direct
    )

    return {
        "model": "uniform_independent_received_rows",
        "expected_base_list": fraction_payload(expected_base),
        "expected_direct_interleaved_list": fraction_payload(expected_direct),
        "expected_product_bound": fraction_payload(expected_product),
        "expected_product_to_direct_ratio": None
        if product_to_direct is None
        else fraction_payload(product_to_direct),
    }


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
        domain = subgroup_domain(
            args.subgroup_generator % args.p, args.subgroup_order, args.p
        )

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
    base_counts = [
        count_base_list(histogram, args.agreement) for histogram in histograms
    ]
    raw_base_counts = [
        count_raw_base_fiber(histogram, args.agreement) for histogram in histograms
    ]
    product_bound = math.prod(base_counts)
    direct_count = count_interleaved(histograms, args.agreement, len(domain))
    raw_simultaneous_count = count_raw_simultaneous_fiber(
        histograms, args.agreement, len(domain)
    )
    intersection_histogram = common_intersection_histogram(histograms, len(domain))
    two_row_codegrees = max_two_row_codegrees(histograms, args.agreement)
    johnson_bound = near_exact_johnson_bound(
        histograms, args.agreement, args.k, len(domain)
    )
    layered_bound = layered_johnson_bound(
        histograms, args.agreement, args.k, len(domain)
    )
    random_baseline = random_received_baseline(
        args.p, args.k, len(domain), args.agreement, len(received_rows)
    )
    ratio = None if product_bound == 0 else direct_count / product_bound
    raw_to_direct_ratio = (
        None if direct_count == 0 else raw_simultaneous_count / direct_count
    )

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
        "raw_base_fiber_counts": raw_base_counts,
        "trivial_product_bound": product_bound,
        "direct_interleaved_count": direct_count,
        "raw_simultaneous_fiber_count": raw_simultaneous_count,
        "direct_to_product_ratio": ratio,
        "raw_to_direct_ratio": raw_to_direct_ratio,
        "common_intersection_histogram": dict(sorted(intersection_histogram.items())),
        "two_row_max_codegrees": two_row_codegrees,
        "near_exact_johnson_bound": johnson_bound,
        "layered_johnson_bound": layered_bound,
        "random_received_baseline": random_baseline,
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
    print(f"raw base fiber counts: {report['raw_base_fiber_counts']}")
    print(f"trivial product bound: {report['trivial_product_bound']}")
    print(f"direct interleaved count: {report['direct_interleaved_count']}")
    print(f"raw simultaneous fiber count: {report['raw_simultaneous_fiber_count']}")
    ratio = report["direct_to_product_ratio"]
    print("direct/product ratio: " + ("undefined" if ratio is None else f"{ratio:.6g}"))
    raw_ratio = report["raw_to_direct_ratio"]
    print(
        "raw/direct ratio: "
        + ("undefined" if raw_ratio is None else f"{raw_ratio:.6g}")
    )
    print(f"common intersection histogram: {report['common_intersection_histogram']}")
    if report["two_row_max_codegrees"] is not None:
        print(f"two-row max codegrees: {report['two_row_max_codegrees']}")
    johnson_bound = report["near_exact_johnson_bound"]
    print(f"near-exact Johnson status: {johnson_bound['status']}")
    if johnson_bound["bound"] is not None:
        print(f"near-exact Johnson bound: {johnson_bound['bound']}")
    if johnson_bound["max_excess"] is not None:
        print(f"near-exact max excess: {johnson_bound['max_excess']}")
    if johnson_bound["neighborhood_sizes"]:
        print(
            "Johnson neighborhood sizes: "
            f"{johnson_bound['neighborhood_sizes']}"
        )
    layered_bound = report["layered_johnson_bound"]
    print(f"layered Johnson status: {layered_bound['status']}")
    if layered_bound["bound"] is not None:
        print(f"layered Johnson bound: {layered_bound['bound']}")
    if layered_bound["kernel_by_anchor_size"]:
        print(
            "layered Johnson kernels: "
            f"{layered_bound['kernel_by_anchor_size']}"
        )

    def decimal_text(item: dict[str, Any]) -> str:
        decimal = item["decimal"]
        return "overflow" if decimal is None else f"{decimal:.6g}"

    random_baseline = report["random_received_baseline"]
    print(
        "random expected base list: "
        + decimal_text(random_baseline["expected_base_list"])
    )
    print(
        "random expected direct interleaved list: "
        + decimal_text(random_baseline["expected_direct_interleaved_list"])
    )
    print(
        "random expected product bound: "
        + decimal_text(random_baseline["expected_product_bound"])
    )
    product_ratio = random_baseline["expected_product_to_direct_ratio"]
    if product_ratio is not None:
        print(
            "random expected product/direct ratio: "
            + decimal_text(product_ratio)
        )
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
