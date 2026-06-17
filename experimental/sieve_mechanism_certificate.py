#!/usr/bin/env python3
"""Exact certificate for Paper A's N=16 sieve-mechanism record.

This checks the finite computation in `tex/RS_disproof_v3.tex` item V5:

* the characteristic-zero cyclotomic value family for `N=16`, `r=9`
  has exactly 3280 values; and
* for the listed primes `p == 1 mod 16`, the restricted sumset
  `|9^wedge Q_16|` has the stated sizes.

All computations are exact enumeration; there is no sampling.
"""

from __future__ import annotations

import argparse
import itertools
import json
from math import comb
from typing import Iterable


STATUS = "PROVED"
THEOREM_ID = "tex/RS_disproof_v3.tex:app:verify V5, lem:value-family"
OBJECT = "N=16 sieve-mechanism restricted-sum certificate"
N = 16
HALF_N = N // 2
R = 9
PRIME_EXPECTATIONS = {
    1889: 1712,
    3137: 2336,
    7681: 2672,
    12289: 3280,
    40961: 3280,
    65537: 3280,
}


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def primitive_root_mod_prime(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for p={prime}")


def subgroup_order_16(prime: int) -> list[int]:
    if (prime - 1) % N != 0:
        raise ValueError(f"p-1 is not divisible by {N}: p={prime}")
    generator = primitive_root_mod_prime(prime)
    step = pow(generator, (prime - 1) // N, prime)
    subgroup = [pow(step, exponent, prime) for exponent in range(N)]
    if len(set(subgroup)) != N or pow(step, N, prime) != 1:
        raise ValueError(f"failed to construct order-{N} subgroup for p={prime}")
    return subgroup


def admissible_weights() -> list[int]:
    weights = []
    for weight in range(1, HALF_N + 1):
        parity_ok = weight % 2 == R % 2
        padding_ok = (R - weight) // 2 <= HALF_N - weight
        if parity_ok and R >= weight and padding_ok:
            weights.append(weight)
    return weights


def formal_value_vectors() -> set[tuple[int, ...]]:
    vectors: set[tuple[int, ...]] = set()
    for weight in admissible_weights():
        for support in itertools.combinations(range(HALF_N), weight):
            for signs in itertools.product((-1, 1), repeat=weight):
                vector = [0] * HALF_N
                for index, sign in zip(support, signs):
                    vector[index] = sign
                vectors.add(tuple(vector))
    return vectors


def formal_formula_count() -> int:
    return sum(comb(HALF_N, weight) * 2**weight for weight in admissible_weights())


def restricted_sum_count(prime: int) -> int:
    subgroup = subgroup_order_16(prime)
    sums = {
        sum(subgroup[index] for index in subset) % prime
        for subset in itertools.combinations(range(N), R)
    }
    return len(sums)


def reduced_formal_value_count(prime: int) -> int:
    subgroup = subgroup_order_16(prime)
    basis = subgroup[:HALF_N]
    values = {
        sum(coef * basis[index] for index, coef in enumerate(vector)) % prime
        for vector in formal_value_vectors()
    }
    return len(values)


def certificate_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for prime, expected in PRIME_EXPECTATIONS.items():
        restricted_count = restricted_sum_count(prime)
        reduced_formal_count = reduced_formal_value_count(prime)
        rows.append(
            {
                "p": prime,
                "p_mod_16": prime % N,
                "expected_sumset_size": expected,
                "restricted_sumset_size": restricted_count,
                "reduced_formal_value_size": reduced_formal_count,
                "matches_expected": restricted_count == expected,
                "matches_formal_reduction": restricted_count == reduced_formal_count,
            }
        )
    return rows


def payload(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    result_rows = list(rows)
    vectors = formal_value_vectors()
    formula_count = formal_formula_count()
    formal_count = len(vectors)
    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "inputs": {
            "N": N,
            "r": R,
            "admissible_weights": admissible_weights(),
            "primes": list(PRIME_EXPECTATIONS.keys()),
        },
        "result": {
            "formal_formula_count": formula_count,
            "formal_enumeration_count": formal_count,
            "formal_count_expected": 3280,
            "formal_count_ok": formula_count == formal_count == 3280,
            "all_prime_rows_ok": all(
                bool(row["matches_expected"])
                and bool(row["matches_formal_reduction"])
                and row["p_mod_16"] == 1
                for row in result_rows
            ),
            "rows": result_rows,
        },
    }


def print_text(rows: list[dict[str, object]], cert: dict[str, object]) -> None:
    result = cert["result"]
    print(OBJECT)
    print(f"Status: {STATUS}")
    print(f"Theorem/problem ID: {THEOREM_ID}")
    print("Object checked: formal N=16,r=9 values and finite reductions.")
    print()
    print(f"N={N}, r={R}, admissible weights={admissible_weights()}")
    print(
        "formal formula count={formal_formula_count}; "
        "formal enumeration count={formal_enumeration_count}; "
        "expected=3280; ok={formal_count_ok}".format(**result)
    )
    print()
    print("{:>7} {:>6} {:>10} {:>12} {:>12} {:>5}".format(
        "p",
        "p%16",
        "expected",
        "sumset",
        "formal",
        "ok",
    ))
    for row in rows:
        ok = row["matches_expected"] and row["matches_formal_reduction"]
        print("{p:>7} {p_mod_16:>6} {expected_sumset_size:>10} "
              "{restricted_sumset_size:>12} "
              "{reduced_formal_value_size:>12} {ok:>5}".format(
                  **row,
                  ok="yes" if ok else "no",
              ))
    print()
    print(f"All prime rows qualify: {result['all_prime_rows_ok']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. JSON is machine-readable and text is for review.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = certificate_rows()
    cert = payload(rows)
    if args.format == "json":
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print_text(rows, cert)
    result = cert["result"]
    return 0 if result["formal_count_ok"] and result["all_prime_rows_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
