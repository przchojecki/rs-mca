#!/usr/bin/env python3
"""Closed-form L2 accounting for the quotient-core support packet."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from typing import Any


MAX_EXACT_DIGITS = 1000
LOG10_2 = math.log10(2.0)


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


def decimal_digits(value: int) -> int:
    if value == 0:
        return 1
    return int((value.bit_length() - 1) * LOG10_2) + 1


def integer_payload(value: int) -> dict[str, int | str | None]:
    digits = decimal_digits(value)
    return {
        "exact": str(value) if digits <= MAX_EXACT_DIGITS else None,
        "decimal_digits": digits,
        "bits": value.bit_length(),
    }


def fraction_payload(value: Fraction) -> dict[str, Any]:
    try:
        decimal: float | None = float(value)
    except OverflowError:
        decimal = None
    numerator_digits = decimal_digits(value.numerator)
    denominator_digits = decimal_digits(value.denominator)
    exact = None
    if numerator_digits + denominator_digits <= MAX_EXACT_DIGITS:
        exact = str(value)
    return {
        "exact": exact,
        "numerator": integer_payload(value.numerator),
        "denominator": integer_payload(value.denominator),
        "decimal": decimal,
    }


def ceil_div(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


def common_intersection_empty_count(
    universe_size: int, subset_size: int, rows: int
) -> int:
    total = 0
    for forced_common in range(subset_size + 1):
        total += (
            (-1) ** forced_common
            * math.comb(universe_size, forced_common)
            * math.comb(universe_size - forced_common, subset_size - forced_common)
            ** rows
        )
    return total


def quotient_tuple_count_at_threshold(
    quotient_universe_size: int,
    quotient_subset_size: int,
    rows: int,
    common_intersection_threshold: int,
) -> int:
    if common_intersection_threshold <= 0:
        return math.comb(quotient_universe_size, quotient_subset_size) ** rows
    if common_intersection_threshold > quotient_subset_size:
        return 0

    total = 0
    for exact_common in range(common_intersection_threshold, quotient_subset_size + 1):
        remaining_universe = quotient_universe_size - exact_common
        remaining_size = quotient_subset_size - exact_common
        total += math.comb(quotient_universe_size, exact_common) * (
            common_intersection_empty_count(
                remaining_universe,
                remaining_size,
                rows,
            )
        )
    return total


def compute_report(args: argparse.Namespace) -> dict[str, Any]:
    if args.k > args.n:
        raise ValueError("expected k <= n")
    if args.sigma >= args.m:
        raise ValueError("quotient-core construction requires sigma < M")
    if args.n % args.m:
        raise ValueError("M must divide n")
    if args.k % args.m:
        raise ValueError("M must divide k")
    if args.slack_intersection > args.sigma:
        raise ValueError("--slack-intersection cannot exceed sigma")
    if args.agreement is None:
        args.agreement = args.k + args.sigma
    if args.agreement < 0:
        raise ValueError("--agreement must be nonnegative")
    if args.agreement > args.n:
        raise ValueError("--agreement cannot exceed n")

    quotient_order = args.n // args.m
    quotient_dimension = args.k // args.m
    if quotient_dimension > quotient_order - 1:
        raise ValueError("quotient construction requires k/M <= n/M - 1")

    quotient_universe_size = quotient_order - 1
    threshold = ceil_div(args.agreement - args.slack_intersection, args.m)
    base_packet_size = math.comb(quotient_order - 1, quotient_dimension)
    cartesian_packet_size = base_packet_size**args.rows
    interleaved_packet_size = quotient_tuple_count_at_threshold(
        quotient_universe_size,
        quotient_dimension,
        args.rows,
        threshold,
    )

    ratio = (
        None
        if cartesian_packet_size == 0
        else Fraction(interleaved_packet_size, cartesian_packet_size)
    )

    return {
        "n": args.n,
        "k": args.k,
        "sigma": args.sigma,
        "agreement": args.agreement,
        "exact_quotient_core_agreement": args.k + args.sigma,
        "M": args.m,
        "N": quotient_order,
        "ell": quotient_dimension,
        "quotient_universe_size": quotient_universe_size,
        "row_count": args.rows,
        "slack_intersection": args.slack_intersection,
        "common_quotient_intersection_threshold": threshold,
        "base_packet_size": integer_payload(base_packet_size),
        "cartesian_packet_size": integer_payload(cartesian_packet_size),
        "interleaved_packet_size": integer_payload(interleaved_packet_size),
        "interleaved_to_cartesian_ratio": None
        if ratio is None
        else fraction_payload(ratio),
    }


def decimal_text(item: dict[str, Any] | None) -> str:
    if item is None:
        return "undefined"
    decimal = item["decimal"]
    return "overflow" if decimal is None else f"{decimal:.6g}"


def integer_text(item: dict[str, Any]) -> str:
    exact = item["exact"]
    if exact is not None:
        return str(exact)
    return "{digits} decimal digits ({bits} bits)".format(
        digits=item["decimal_digits"],
        bits=item["bits"],
    )


def print_report(report: dict[str, Any]) -> None:
    print(
        "n={n} k={k} sigma={sigma} M={M} N={N} ell={ell} rows={rows}".format(
            n=report["n"],
            k=report["k"],
            sigma=report["sigma"],
            M=report["M"],
            N=report["N"],
            ell=report["ell"],
            rows=report["row_count"],
        )
    )
    print(f"agreement: {report['agreement']}")
    print(f"exact quotient-core agreement: {report['exact_quotient_core_agreement']}")
    print(f"slack intersection: {report['slack_intersection']}")
    print(
        "common quotient-intersection threshold: "
        f"{report['common_quotient_intersection_threshold']}"
    )
    print(
        "base quotient-core packet: "
        + integer_text(report["base_packet_size"])
    )
    print("cartesian packet: " + integer_text(report["cartesian_packet_size"]))
    print(
        "interleaved packet: "
        + integer_text(report["interleaved_packet_size"])
    )
    print(
        "interleaved/cartesian ratio: "
        + decimal_text(report["interleaved_to_cartesian_ratio"])
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute quotient-core packet interleaving counts."
    )
    parser.add_argument("--n", type=positive_int, required=True, help="domain size")
    parser.add_argument("--k", type=positive_int, required=True, help="RS dimension")
    parser.add_argument(
        "--sigma",
        type=positive_int,
        required=True,
        help="quotient-core slack, with agreement k+sigma",
    )
    parser.add_argument(
        "--M",
        dest="m",
        type=positive_int,
        required=True,
        help="quotient fiber size",
    )
    parser.add_argument(
        "--rows",
        type=positive_int,
        default=2,
        help="interleaving row count",
    )
    parser.add_argument(
        "--slack-intersection",
        type=nonnegative_int,
        help="common size of the row slack sets; defaults to sigma",
    )
    parser.add_argument(
        "--agreement",
        type=nonnegative_int,
        help="agreement threshold; defaults to k+sigma",
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
    if args.slack_intersection is None:
        args.slack_intersection = args.sigma

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
