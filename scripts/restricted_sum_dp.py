#!/usr/bin/env python3
"""Exact restricted-sum verifier over prime fields.

This AUDIT helper computes

    r^wedge A = {a_1 + ... + a_r : a_i in A distinct}

over F_p by dynamic programming.  It is intended for Paper A finite-claim
checks and for P2 certificate-scanner infrastructure.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class RestrictedSumReport:
    object: str
    status: str
    theorem_problem_id: str
    p: int
    r: int
    element_count: int
    element_values_sample: list[int]
    subgroup_order: int | None
    subgroup_generator: int | None
    restricted_sum_size: int
    field_size: int
    full_coverage: bool
    zero_in_sumset: bool
    dsh_lower_bound: int
    dsh_certifies_full_coverage: bool
    missing_count: int
    sample_limit: int
    missing_values_sample: list[int]
    sum_values_sample: list[int]
    bad_slope_values_sample: list[int]
    proof_certificate: str
    notes: list[str]


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


def parse_elements(text: str) -> list[int]:
    if not text.strip():
        raise argparse.ArgumentTypeError("element list must not be empty")
    out = []
    for part in text.split(","):
        item = part.strip()
        if not item:
            continue
        try:
            out.append(int(item, 0))
        except ValueError as exc:
            raise argparse.ArgumentTypeError(f"not an integer: {item}") from exc
    if not out:
        raise argparse.ArgumentTypeError("element list must not be empty")
    return out


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def prime_factors(n: int) -> list[int]:
    factors: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def primitive_root(p: int) -> int:
    if p == 2:
        return 1
    factors = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root found for p={p}")


def subgroup_elements(p: int, order: int, generator: int | None) -> tuple[list[int], int]:
    if (p - 1) % order != 0:
        raise ValueError("--subgroup-order must divide p-1")
    if generator is None:
        root = primitive_root(p)
        gen = pow(root, (p - 1) // order, p)
    else:
        gen = generator % p
        if gen == 0:
            raise ValueError("--generator must be nonzero modulo p")
        if pow(gen, order, p) != 1:
            raise ValueError("--generator does not have order dividing --subgroup-order")
        for q in prime_factors(order):
            if pow(gen, order // q, p) == 1:
                raise ValueError("--generator has order smaller than --subgroup-order")

    elems = [pow(gen, i, p) for i in range(order)]
    if len(set(elems)) != order:
        raise ValueError("constructed subgroup has repeated elements")
    return sorted(elems), gen


def normalize_elements(elements: list[int], p: int) -> list[int]:
    normalized = sorted({x % p for x in elements})
    if len(normalized) != len(elements):
        raise ValueError("elements must be distinct modulo p")
    return normalized


def restricted_sums(elements: list[int], r: int, p: int) -> set[int]:
    if r < 0 or r > len(elements):
        raise ValueError("require 0 <= r <= number of elements")
    by_size: list[set[int]] = [set() for _ in range(r + 1)]
    by_size[0].add(0)
    for index, x in enumerate(elements, start=1):
        upper = min(r, index)
        for size in range(upper, 0, -1):
            by_size[size].update((value + x) % p for value in by_size[size - 1])
    return by_size[r]


def dsh_lower_bound(p: int, m: int, r: int) -> int:
    if not (1 <= r <= m):
        return 0
    return min(p, r * (m - r) + 1)


def build_report(args: argparse.Namespace) -> RestrictedSumReport:
    p = args.p
    r = args.r
    if not is_prime(p):
        raise ValueError("--p must be prime")

    if args.elements is None and args.subgroup_order is None:
        raise ValueError("provide either --elements or --subgroup-order")
    if args.elements is not None and args.subgroup_order is not None:
        raise ValueError("provide only one of --elements or --subgroup-order")

    subgroup_order = None
    subgroup_generator = None
    if args.elements is not None:
        elements = normalize_elements(args.elements, p)
    else:
        subgroup_order = args.subgroup_order
        elements, subgroup_generator = subgroup_elements(p, subgroup_order, args.generator)

    if r > len(elements):
        raise ValueError("--r must be at most the number of elements")

    sums = restricted_sums(elements, r, p)
    missing = sorted(set(range(p)) - sums)
    sum_values = sorted(sums)
    bad_slopes = sorted((-value) % p for value in sums)
    dsh = dsh_lower_bound(p, len(elements), r)
    max_values = args.max_values

    notes = [
        "AUDIT helper; exact finite DP only, no MCA/list theorem upgrade.",
        "Bad-slope samples are the negated restricted sums used by the locator identity.",
    ]
    if subgroup_order is not None:
        notes.append("Subgroup mode constructs the unique subgroup of the requested order.")
    if dsh == p:
        notes.append("The imported DSH bound alone certifies full field coverage.")
    elif len(sums) == p:
        notes.append("Full coverage was verified by DP, beyond what DSH certifies here.")

    return RestrictedSumReport(
        object="restricted_sum_dp",
        status="AUDIT",
        theorem_problem_id="Paper A lem:dsh / A1 finite-claim audit / P2 scanner",
        p=p,
        r=r,
        element_count=len(elements),
        element_values_sample=elements[:max_values],
        subgroup_order=subgroup_order,
        subgroup_generator=subgroup_generator,
        restricted_sum_size=len(sums),
        field_size=p,
        full_coverage=len(sums) == p,
        zero_in_sumset=0 in sums,
        dsh_lower_bound=dsh,
        dsh_certifies_full_coverage=dsh == p,
        missing_count=len(missing),
        sample_limit=max_values,
        missing_values_sample=missing[:max_values],
        sum_values_sample=sum_values[:max_values],
        bad_slope_values_sample=bad_slopes[:max_values],
        proof_certificate=(
            "DP invariant: after processing a prefix of A, state[j] is exactly "
            "the set of sums of j distinct processed elements. Descending j "
            "updates use each new element at most once."
        ),
        notes=notes,
    )


def print_text(report: RestrictedSumReport) -> None:
    rows: list[tuple[str, Any]] = [
        ("object", report.object),
        ("status", report.status),
        ("theorem/problem", report.theorem_problem_id),
        ("p", report.p),
        ("r", report.r),
        ("element_count", report.element_count),
        ("element_values_sample", report.element_values_sample),
        ("subgroup_order", report.subgroup_order),
        ("subgroup_generator", report.subgroup_generator),
        ("restricted_sum_size", report.restricted_sum_size),
        ("field_size", report.field_size),
        ("full_coverage", report.full_coverage),
        ("zero_in_sumset", report.zero_in_sumset),
        ("dsh_lower_bound", report.dsh_lower_bound),
        ("dsh_certifies_full_coverage", report.dsh_certifies_full_coverage),
        ("missing_count", report.missing_count),
        ("sample_limit", report.sample_limit),
        ("missing_values_sample", report.missing_values_sample),
        ("sum_values_sample", report.sum_values_sample),
        ("bad_slope_values_sample", report.bad_slope_values_sample),
        ("certificate", report.proof_certificate),
    ]
    width = max(len(key) for key, _ in rows)
    print("Restricted-sum DP certificate (AUDIT)")
    for key, value in rows:
        print(f"{key:<{width}} : {value}")
    print("notes:")
    for note in report.notes:
        print(f"  - {note}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute exact restricted sums r^wedge A over F_p."
    )
    parser.add_argument("--p", required=True, type=positive_int, help="prime field size")
    parser.add_argument("--r", required=True, type=nonnegative_int, help="restricted sum size")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--elements",
        type=parse_elements,
        help="comma-separated field elements, e.g. 1,2,4,8",
    )
    source.add_argument(
        "--subgroup-order",
        type=positive_int,
        help="construct the multiplicative subgroup of this order",
    )
    parser.add_argument(
        "--generator",
        type=positive_int,
        default=None,
        help="optional generator for --subgroup-order",
    )
    parser.add_argument(
        "--max-values",
        type=positive_int,
        default=20,
        help="maximum number of residues included in each sample",
    )
    parser.add_argument(
        "--expect-full",
        action="store_true",
        help="exit with status 1 unless the computed sumset is all of F_p",
    )
    parser.add_argument(
        "--expect-size",
        type=positive_int,
        default=None,
        help="exit with status 1 unless the computed sumset has this size",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(sys.argv[1:] if argv is None else argv)
        report = build_report(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(asdict(report), indent=2, sort_keys=True))
    else:
        print_text(report)

    if args.expect_full and not report.full_coverage:
        return 1
    if args.expect_size is not None and report.restricted_sum_size != args.expect_size:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
