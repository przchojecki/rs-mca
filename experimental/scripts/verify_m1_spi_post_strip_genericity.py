#!/usr/bin/env python3
"""Verify the support-side strip genericity identities.

The proof note is symbolic.  This script checks the periodic stratum count,
fixed-locus equivalence, intersection formula, and trivial stabilizer of the
aperiodic complement on representative cyclic toy domains.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from itertools import combinations
from math import comb, gcd, lcm
from pathlib import Path
from typing import Any


OUTPUT = Path(
    "experimental/data/certificates/m1-spi-post-strip-genericity/"
    "m1_spi_post_strip_genericity.json"
)


@dataclass(frozen=True)
class Case:
    n: int
    j: int


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def subgroup(n: int, order: int) -> frozenset[int]:
    if n % order:
        raise ValueError("subgroup order must divide n")
    step = n // order
    return frozenset((a * step) % n for a in range(order))


def translate(root_set: frozenset[int], shift: int, n: int) -> frozenset[int]:
    return frozenset((x + shift) % n for x in root_set)


def stable_under(root_set: frozenset[int], n: int, order: int) -> bool:
    return all(translate(root_set, h, n) == root_set for h in subgroup(n, order))


def coset_representatives(n: int, order: int) -> list[int]:
    seen: set[int] = set()
    reps = []
    for x in range(n):
        if x in seen:
            continue
        coset = translate(subgroup(n, order), x, n)
        seen.update(coset)
        reps.append(x)
    return reps


def unions_of_cosets(n: int, order: int, coset_count: int) -> set[frozenset[int]]:
    reps = coset_representatives(n, order)
    out: set[frozenset[int]] = set()
    for chosen in combinations(reps, coset_count):
        union: set[int] = set()
        for rep in chosen:
            union.update(translate(subgroup(n, order), rep, n))
        out.add(frozenset(union))
    return out


def all_root_sets(n: int, j: int) -> list[frozenset[int]]:
    return [frozenset(c) for c in combinations(range(n), j)]


def stabilizer_orders(root_set: frozenset[int], n: int) -> list[int]:
    return [d for d in divisors(n) if stable_under(root_set, n, d)]


def analyze_case(case: Case) -> dict[str, Any]:
    n, j = case.n, case.j
    root_sets = all_root_sets(n, j)
    rows = []
    periodic_by_order: dict[int, set[frozenset[int]]] = {}

    for order in divisors(n):
        fixed = {T for T in root_sets if stable_under(T, n, order)}
        if j % order == 0:
            coset_unions = unions_of_cosets(n, order, j // order)
            expected_count = comb(n // order, j // order)
        else:
            coset_unions = set()
            expected_count = 0
        if fixed != coset_unions:
            raise AssertionError((case, order, "fixed/coset mismatch"))
        if len(fixed) != expected_count:
            raise AssertionError((case, order, "count mismatch", len(fixed), expected_count))
        periodic_by_order[order] = fixed
        rows.append({
            "order": order,
            "count": len(fixed),
            "formula_count": expected_count,
            "nontrivial": order > 1,
        })

    intersection_checks = []
    for m in divisors(n):
        for q in divisors(n):
            generated = lcm(m, q)
            left = periodic_by_order[m] & periodic_by_order[q]
            right = periodic_by_order[generated]
            ok = left == right
            if not ok:
                raise AssertionError((case, m, q, "intersection mismatch"))
            if m > 1 and q > 1 and (m, q) in [(2, 3), (2, 4), (3, 6), (4, 6)]:
                intersection_checks.append({
                    "orders": [m, q],
                    "generated_order": generated,
                    "intersection_count": len(left),
                })

    stripped = set().union(
        *(periodic_by_order[d] for d in divisors(gcd(n, j)) if d > 1)
    ) if gcd(n, j) > 1 else set()
    aperiodic = set(root_sets) - stripped
    bad_aperiodic = [
        sorted(T) for T in aperiodic if max(stabilizer_orders(T, n)) > 1
    ]
    if bad_aperiodic:
        raise AssertionError((case, "aperiodic stabilizer not trivial", bad_aperiodic[:3]))

    stabilizer_histogram: dict[str, int] = {}
    for T in root_sets:
        max_stab = max(stabilizer_orders(T, n))
        stabilizer_histogram[str(max_stab)] = stabilizer_histogram.get(str(max_stab), 0) + 1

    return {
        "n": n,
        "j": j,
        "total_divisors": len(root_sets),
        "periodic_rows": rows,
        "stripped_count": len(stripped),
        "aperiodic_count": len(aperiodic),
        "aperiodic_has_only_trivial_stabilizer": True,
        "stabilizer_order_histogram": dict(sorted(stabilizer_histogram.items(), key=lambda kv: int(kv[0]))),
        "sample_intersection_checks": intersection_checks[:8],
    }


def build_certificate() -> dict[str, Any]:
    cases = [Case(12, 4), Case(16, 8), Case(18, 6), Case(24, 6)]
    case_payloads = [analyze_case(case) for case in cases]
    return {
        "schema": "m1-spi-post-strip-genericity-v1",
        "status": "PROVED_COMBINATORIAL",
        "dag_target": "spi_genericity",
        "theorem": {
            "periodic_stratum_count": "|Per_M(D_j)| = binom(n/M,j/M) if M|j, else 0",
            "intersection": "Per_M(D_j) cap Per_N(D_j) = Per_lcm(M,N)(D_j)",
            "post_strip_genericity": "D_j^aper has no nontrivial subgroup-stabilized locator",
        },
        "cases": case_payloads,
        "non_claims": [
            "does not prove the SPI incidence bound",
            "does not price GAP-1 non-equivariant periodic mass",
            "does not resolve the GAP-2 support-periodic versus line-periodic dictionary",
        ],
    }


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("M1 SPI post-strip genericity")
    print(f"  schema: {cert['schema']}")
    for row in cert["cases"]:
        print(
            f"  n={row['n']} j={row['j']}: total={row['total_divisors']} "
            f"stripped={row['stripped_count']} aperiodic={row['aperiodic_count']} "
            f"trivial_stabilizer={row['aperiodic_has_only_trivial_stabilizer']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")
    if args.check:
        actual = json.loads(args.check.read_text())
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()

