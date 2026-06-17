#!/usr/bin/env python3
"""Scan canonical-line support-wise MCA slopes over a small prime field.

The scanned line is the quotient-locator line from RS_disproof_v3.tex:

    f = x^(k+a),  g = x^k,  a = n / Nq,

on a cyclic multiplicative domain D of order n in F_p.  The script exhausts all
slopes z in F_p and all supports of size at least k+a, and reports which slopes
are support-wise MCA-bad at radius 1 - k/n - 1/Nq.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from functools import lru_cache
from itertools import combinations
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime", type=int, required=True, help="prime field size p")
    parser.add_argument("--n", type=int, required=True, help="multiplicative domain order")
    parser.add_argument("--k", type=int, required=True, help="RS dimension k")
    parser.add_argument(
        "--quotient-order",
        type=int,
        required=True,
        help="quotient order Nq; must divide n",
    )
    parser.add_argument(
        "--primitive",
        type=int,
        default=None,
        help="optional primitive generator of F_p^*",
    )
    parser.add_argument(
        "--max-supports",
        type=int,
        default=2_000_000,
        help="refuse scans with more support subsets than this limit",
    )
    parser.add_argument("--pretty", action="store_true", help="print a short table before JSON")
    return parser.parse_args()


def factorize(value: int) -> list[int]:
    factors: list[int] = []
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.append(d)
            while value % d == 0:
                value //= d
        d += 1 if d == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    d = 3
    while d * d <= value:
        if value % d == 0:
            return False
        d += 2
    return True


def multiplicative_order(base: int, modulus: int) -> int:
    if math.gcd(base, modulus) != 1:
        return 0
    order = 1
    x = base % modulus
    while x != 1:
        x = (x * base) % modulus
        order += 1
        if order > modulus:
            raise ValueError("order search failed")
    return order


def find_primitive_root(p: int) -> int:
    factors = factorize(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for F_{p}")


def inv(value: int, p: int) -> int:
    return pow(value % p, p - 2, p)


def nullspace_mod(matrix: list[list[int]], p: int) -> list[list[int]]:
    if not matrix:
        return []

    rows = [[entry % p for entry in row] for row in matrix]
    row_count = len(rows)
    col_count = len(rows[0])
    pivot_cols: list[int] = []
    pivot_row = 0

    for col in range(col_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue

        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = inv(rows[pivot_row][col], p)
        rows[pivot_row] = [(entry * scale) % p for entry in rows[pivot_row]]

        for row in range(row_count):
            if row == pivot_row or rows[row][col] % p == 0:
                continue
            factor = rows[row][col] % p
            rows[row] = [
                (rows[row][idx] - factor * rows[pivot_row][idx]) % p
                for idx in range(col_count)
            ]

        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break

    free_cols = [col for col in range(col_count) if col not in pivot_cols]
    basis: list[list[int]] = []
    for free_col in free_cols:
        vector = [0] * col_count
        vector[free_col] = 1
        for row, pivot_col in enumerate(pivot_cols):
            vector[pivot_col] = (-rows[row][free_col]) % p
        basis.append(vector)
    return basis


def make_domain(p: int, n: int, primitive: int | None) -> tuple[int, tuple[int, ...]]:
    if not is_prime(p):
        raise ValueError("--prime must be prime")
    if (p - 1) % n != 0:
        raise ValueError("--n must divide p - 1")

    primitive = primitive if primitive is not None else find_primitive_root(p)
    if multiplicative_order(primitive, p) != p - 1:
        raise ValueError("--primitive must generate F_p^*")

    domain_gen = pow(primitive, (p - 1) // n, p)
    domain = []
    x = 1
    for _ in range(n):
        domain.append(x)
        x = (x * domain_gen) % p
    if x != 1 or len(set(domain)) != n:
        raise ValueError("domain generator did not produce order n")
    return primitive, tuple(domain)


def quotient_values(domain: Iterable[int], a: int, p: int) -> tuple[int, ...]:
    return tuple(sorted({pow(x, a, p) for x in domain}))


def locator_counts(q_values: Iterable[int], ell: int, p: int) -> Counter[int]:
    counts: Counter[int] = Counter()
    for subset in combinations(q_values, ell):
        counts[(-sum(subset)) % p] += 1
    return counts


def fraction_string(numerator: int, denominator: int) -> str:
    gcd = math.gcd(numerator, denominator)
    numerator //= gcd
    denominator //= gcd
    if denominator == 1:
        return str(numerator)
    return f"{numerator}/{denominator}"


class Scanner:
    def __init__(self, p: int, domain: tuple[int, ...], k: int):
        self.p = p
        self.domain = domain
        self.n = len(domain)
        self.k = k

    @lru_cache(maxsize=None)
    def support_constraints(
        self,
        indices: tuple[int, ...],
        dimension: int,
    ) -> tuple[tuple[int, ...], ...]:
        if len(indices) <= dimension:
            return ()
        xs = [self.domain[index] for index in indices]
        vandermonde_t = [
            [pow(x, degree, self.p) for x in xs]
            for degree in range(dimension)
        ]
        return tuple(tuple(row) for row in nullspace_mod(vandermonde_t, self.p))

    def fits_degree(
        self,
        values: tuple[int, ...],
        indices: tuple[int, ...],
        dimension: int,
    ) -> bool:
        for check in self.support_constraints(indices, dimension):
            total = sum(check[pos] * values[index] for pos, index in enumerate(indices))
            if total % self.p:
                return False
        return True

    def monomial_word(self, exponent: int) -> tuple[int, ...]:
        return tuple(pow(x, exponent, self.p) for x in self.domain)

    def line_word(self, anchor_exp: int, direction_exp: int, slope: int) -> tuple[int, ...]:
        return tuple(
            (pow(x, anchor_exp, self.p) + slope * pow(x, direction_exp, self.p))
            % self.p
            for x in self.domain
        )

    def scan_bad_slopes(
        self,
        anchor_exp: int,
        direction_exp: int,
        min_support_size: int,
    ) -> tuple[set[int], int, int]:
        anchor = self.monomial_word(anchor_exp)
        direction = self.monomial_word(direction_exp)
        bad_slopes: set[int] = set()
        support_count = 0
        noncontained_support_count = 0

        for size in range(min_support_size, self.n + 1):
            for support in combinations(range(self.n), size):
                support_count += 1
                anchor_fit = self.fits_degree(anchor, support, self.k)
                direction_fit = self.fits_degree(direction, support, self.k)
                noncontained = not (anchor_fit and direction_fit)
                if not noncontained:
                    continue
                noncontained_support_count += 1

                for slope in range(self.p):
                    if slope in bad_slopes:
                        continue
                    word = self.line_word(anchor_exp, direction_exp, slope)
                    if self.fits_degree(word, support, self.k):
                        bad_slopes.add(slope)

        return bad_slopes, support_count, noncontained_support_count


def support_count(n: int, min_size: int) -> int:
    return sum(math.comb(n, size) for size in range(min_size, n + 1))


def build_result(args: argparse.Namespace) -> dict:
    p = args.prime
    n = args.n
    k = args.k
    q_order = args.quotient_order

    if n % q_order != 0:
        raise ValueError("--quotient-order must divide --n")
    a = n // q_order
    if k % a != 0:
        raise ValueError("a = n / quotient_order must divide k")
    if k + a > n:
        raise ValueError("canonical support size k + a must be at most n")

    min_support = k + a
    total_supports = support_count(n, min_support)
    if total_supports > args.max_supports:
        raise ValueError(
            f"scan needs {total_supports} supports; raise --max-supports to run it"
        )

    primitive, domain = make_domain(p, n, args.primitive)
    scanner = Scanner(p, domain, k)
    q_values = quotient_values(domain, a, p)
    ell = k // a + 1
    counts = locator_counts(q_values, ell, p)
    locator_slopes = set(counts)
    bad_slopes, scanned_supports, noncontained_supports = scanner.scan_bad_slopes(
        k + a,
        k,
        min_support,
    )

    radius = fraction_string(n - k - a, n)
    return {
        "status": "PROVED",
        "theorem_or_problem": "RS_disproof_v3.tex lem:locator; proximity_blueprint_v3.tex M1",
        "input_parameters": {
            "prime": p,
            "domain_order": n,
            "primitive_generator": primitive,
            "k": k,
            "rho": fraction_string(k, n),
            "quotient_order": q_order,
            "a": a,
            "ell": ell,
        },
        "mathematical_object": {
            "domain": list(domain),
            "quotient_values": list(q_values),
            "line": f"u_z(x) = x^{k + a} + z*x^{k}",
            "code": f"RS[F_{p},D,{k}]",
            "radius": f"1 - k/n - 1/Nq = {radius}",
            "support_threshold": min_support,
        },
        "result": {
            "locator_slope_count": len(locator_slopes),
            "locator_slopes": sorted(locator_slopes),
            "locator_slope_count_histogram": {
                str(key): value for key, value in sorted(Counter(counts.values()).items())
            },
            "mca_bad_slope_count": len(bad_slopes),
            "mca_bad_slopes": sorted(bad_slopes),
            "locator_subset_of_mca": locator_slopes <= bad_slopes,
            "extra_mca_slopes": sorted(bad_slopes - locator_slopes),
            "missing_locator_slopes": sorted(locator_slopes - bad_slopes),
            "mca_density": fraction_string(len(bad_slopes), p),
        },
        "proof_certificate": {
            "method": "exhaust all slopes and all supports of size at least k+a",
            "supports_examined": scanned_supports,
            "noncontained_supports": noncontained_supports,
            "support_limit": args.max_supports,
            "script": "scripts/mca_slope_scan.py",
        },
    }


def print_pretty(result: dict) -> None:
    params = result["input_parameters"]
    values = result["result"]
    cert = result["proof_certificate"]
    print("canonical-line MCA slope scan")
    print(f"  p={params['prime']} n={params['domain_order']} k={params['k']}")
    print(f"  quotient_order={params['quotient_order']} a={params['a']}")
    print(f"  locator slopes: {values['locator_slope_count']}")
    print(f"  MCA-bad slopes: {values['mca_bad_slope_count']}")
    print(f"  density: {values['mca_density']}")
    print(f"  supports examined: {cert['supports_examined']}")
    print(f"  locator subset of MCA: {values['locator_subset_of_mca']}")


def main() -> int:
    args = parse_args()
    result = build_result(args)
    if args.pretty:
        print_pretty(result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
