#!/usr/bin/env python3
"""Audit a sharper 4p target for M1 depth-two two-coordinate terms."""

from __future__ import annotations

import cmath
import math
from itertools import product
from typing import Dict, List, Tuple


SAMPLES = (
    {"p": 17, "n": 8},
    {"p": 31, "n": 10},
    {"p": 37, "n": 9},
    {"p": 43, "n": 14},
    {"p": 61, "n": 20},
    {"p": 73, "n": 8},
    {"p": 79, "n": 26},
    {"p": 109, "n": 18},
    {"p": 113, "n": 16},
    {"p": 137, "n": 34},
    {"p": 193, "n": 64},
)

GLOBAL_EXPECTED = {
    "p": 109,
    "n": 18,
    "e": 6,
    "h": 12,
    "max_tuple": (0, 5, 5, 3),
    "ratio": 3.3896787506,
}


def prime_factors(value: int) -> List[int]:
    factors: List[int] = []
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


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for p={p}")


def log_table(p: int) -> Dict[int, int]:
    root = primitive_root(p)
    return {pow(root, exponent, p): exponent for exponent in range(p - 1)}


def character_table(p: int, order: int, logs: Dict[int, int]) -> List[List[complex]]:
    table: List[List[complex]] = []
    for exponent in range(order):
        row = [0j]
        for value in range(1, p):
            angle = 2.0 * math.pi * exponent * logs[value] / order
            row.append(cmath.exp(1j * angle))
        table.append(row)
    return table


def shape_a(u: int, v: int, p: int) -> int:
    return (-(u * u + v * v + u * v + u + v + 1)) % p


def sum_for_tuple(
    p: int,
    char_e: List[List[complex]],
    char_h: List[List[complex]],
    exponents: Tuple[int, int, int, int],
    a_values: List[List[int]],
    w_values: List[List[int]],
) -> complex:
    a, b, c, d = exponents
    chi_a = char_e[a]
    chi_b = char_e[b]
    chi_c = char_e[c]
    psi_d = char_h[d]
    total = 0j
    for u in range(p):
        chi_u = chi_a[u]
        if chi_u == 0j:
            continue
        a_row = a_values[u]
        w_row = w_values[u]
        for v in range(p):
            total += chi_u * chi_b[v] * chi_c[w_row[v]] * psi_d[a_row[v]]
    return total


def audit_sample(p: int, n: int) -> Dict[str, object]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p-1")
    e = (p - 1) // n
    h = e * math.gcd(2, n)
    logs = log_table(p)
    char_e = character_table(p, e, logs)
    char_h = character_table(p, h, logs)
    a_values = [[shape_a(u, v, p) for v in range(p)] for u in range(p)]
    w_values = [[(-1 - u - v) % p for v in range(p)] for u in range(p)]
    best_abs = 0.0
    best_tuple = None
    tuple_count = 0

    for exponents in product(range(e), range(e), range(e), range(1, h)):
        if sum(exponent % e != 0 for exponent in exponents[:3]) != 2:
            continue
        tuple_count += 1
        value = sum_for_tuple(
            p,
            char_e,
            char_h,
            exponents,
            a_values,
            w_values,
        )
        magnitude = abs(value)
        if magnitude > best_abs:
            best_abs = magnitude
            best_tuple = exponents

    if best_abs > 4 * p + 1e-8:
        raise AssertionError((p, n, best_abs, best_tuple))
    return {
        "p": p,
        "n": n,
        "e": e,
        "h": h,
        "tuple_count": tuple_count,
        "max_abs": round(best_abs, 10),
        "max_ratio_to_p": round(best_abs / p, 10),
        "max_tuple": best_tuple,
    }


def main() -> None:
    rows = [audit_sample(sample["p"], sample["n"]) for sample in SAMPLES]
    for row in rows:
        print(row)
    best = max(rows, key=lambda row: float(row["max_ratio_to_p"]))
    for key, value in GLOBAL_EXPECTED.items():
        if key == "ratio":
            actual = float(best["max_ratio_to_p"])
        else:
            actual = best[key]
        if actual != value:
            raise AssertionError((key, actual, value))
    print("M1 depth-two two-coordinate sharp-target verifier passed")


if __name__ == "__main__":
    main()
