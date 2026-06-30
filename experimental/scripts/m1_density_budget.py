#!/usr/bin/env python3
"""Exact evaluator for the M1 sparse-certificate density budget.

This is an AUDIT helper for the local M1 sparse-certificate chain in
``experimental/notes/m1/m1_same_slope_root_slice_lemma.md``.  It evaluates the
integer ceiling

    R_Z(a0,L) = ceil(R_dens(a0,L)) - 1

from (RKSQINTBUDGET), using exact rational arithmetic.  If an endpoint
footprint cap S is supplied, it also uses the optimal compatible far-factor

    L_S = floor((S+1)/(2D)).

The script does not prove the missing global row-basis/core-image density
bound.  It tells a finite checker what support budget that hypothetical bound
would close, and what near-star template ledger remains.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction
from typing import Any


def positive_int(text: str) -> int:
    try:
        value = int(text, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not an integer: {text}") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return value


def nonnegative_int(text: str) -> int:
    try:
        value = int(text, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not an integer: {text}") from exc
    if value < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return value


def even_positive_int(text: str) -> int:
    value = positive_int(text)
    if value % 2:
        raise argparse.ArgumentTypeError("must be even")
    return value


def rational(text: str) -> Fraction:
    try:
        value = Fraction(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not a rational number: {text}") from exc
    return value


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def fraction_record(value: Fraction) -> dict[str, Any]:
    try:
        decimal = float(value)
    except OverflowError:
        decimal = None
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": decimal,
        "text": str(value),
    }


def template_bound(q: int, footprint_cap: int, e: int) -> int:
    h = e // 2
    return sum(
        math.comb(q + 1, footprint_size)
        * (1 << (h * math.comb(footprint_size, 2)))
        for footprint_size in range(footprint_cap + 1)
    )


def compute_report(args: argparse.Namespace) -> dict[str, Any]:
    q = args.q
    d_cap = args.D
    a0 = args.a0
    if not (Fraction(0) <= a0 <= Fraction(1)):
        raise ValueError("--a0 must satisfy 0 <= a0 <= 1")

    if args.L is not None:
        far_factor = args.L
        if far_factor < 2:
            raise ValueError("--L must be at least 2")
        footprint_cap = min(q + 1, max(0, 2 * far_factor * d_cap - 1))
        footprint_source = "from_L"
    else:
        if args.S < 4 * d_cap - 1:
            raise ValueError("--S must be at least 4D-1")
        far_factor = (args.S + 1) // (2 * d_cap)
        if far_factor < 2:
            raise ValueError("derived L_S must be at least 2")
        footprint_cap = min(q + 1, args.S)
        footprint_source = "from_S"

    selected_denominator = (q - 3) * far_factor + 2
    if selected_denominator <= 0:
        raise ValueError("require q-3+2/L > 0")

    r_sel = (
        a0
        * a0
        * (q - 1)
        * (q - 1)
        * far_factor
        / selected_denominator
    )
    r_miss = (
        Fraction(q + 1)
        - Fraction(far_factor, far_factor - 1) * (1 - a0) * (q - 1)
    )
    r_dens = max(r_sel, r_miss)
    r_z = ceil_fraction(r_dens) - 1

    report: dict[str, Any] = {
        "object": "m1_sparse_certificate_density_budget",
        "status": "AUDIT",
        "theorem_problem_id": (
            "M1 / RKSQALPHA0 / RKSQBUDGET / RKSQINTBUDGET / RKSQTRADE"
        ),
        "q": q,
        "D": d_cap,
        "a0": fraction_record(a0),
        "L": far_factor,
        "footprint_cap": footprint_cap,
        "footprint_source": footprint_source,
        "R_sel": fraction_record(r_sel),
        "R_miss": fraction_record(r_miss),
        "R_dens": fraction_record(r_dens),
        "R_Z": r_z,
        "proof_certificate": (
            "Exact Fraction arithmetic. R_Z=ceil(max(R_sel,R_miss))-1, so "
            "an integer R satisfies R<R_dens iff R<=R_Z."
        ),
        "notes": [
            "This script assumes a separate theorem proves alpha_ap >= a0.",
            "Closed budgets leave the endpoint-star, D-small, large-support, "
            "or near-star template branches from the M1 local theorem.",
        ],
    }

    if args.R is not None:
        report["queried_R"] = args.R
        report["queried_R_closes_far_sparse_branch"] = args.R <= r_z

    if args.e is not None:
        exact_template_bound = None
        omitted_reason = None
        if footprint_cap <= args.template_exact_limit:
            exact_template_bound = template_bound(q, footprint_cap, args.e)
        else:
            omitted_reason = (
                "footprint_cap exceeds --template-exact-limit; rerun with a "
                "larger limit if this exact integer is needed"
            )
        report["e"] = args.e
        report["template_bound"] = {
            "formula": (
                "sum_{s=0}^{footprint_cap} binom(q+1,s) "
                "2^((e/2) binom(s,2))"
            ),
            "exact": exact_template_bound,
            "omitted_reason": omitted_reason,
            "template_exact_limit": args.template_exact_limit,
        }

    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q", type=positive_int, required=True)
    parser.add_argument("--D", type=positive_int, required=True)
    parser.add_argument("--a0", type=rational, required=True)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--L", type=positive_int)
    selector.add_argument("--S", type=nonnegative_int)
    parser.add_argument("--R", type=nonnegative_int)
    parser.add_argument("--e", type=even_positive_int)
    parser.add_argument("--template-exact-limit", type=nonnegative_int, default=64)
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = compute_report(args)
    except ValueError as exc:
        parser.error(str(exc))
    json.dump(report, sys.stdout, indent=2 if args.pretty else None, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
