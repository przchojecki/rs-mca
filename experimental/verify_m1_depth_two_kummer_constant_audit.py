#!/usr/bin/env python3
"""Audit finite M1 depth-two Kummer constants by direct summation.

Proof status: AUDIT / EXPERIMENTAL.

This script exhausts every character tuple in representative small
prime/subgroup cases and checks the exact sums against the degree-stratified
constants used by the slack-two depth-two Kummer ledger.
"""

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
)

BOUND_LABELS = {
    "jacobi": "p + 6 ceil(sqrt(p))",
    "conic_only": "p + 6 ceil(sqrt(p))",
    "quadratic_one_coordinate": "4p",
    "one_coordinate_kummer": "4p",
    "two_coordinate_kummer": "9p",
    "three_coordinate_kummer": "16p",
}

ObstructionCheck = Tuple[str, int, int, str, Tuple[int, int, int, int], int, float]

OBSTRUCTION_CHECKS: Tuple[ObstructionCheck, ...] = (
    (
        "three-coordinate-not-4p",
        37,
        9,
        "three_coordinate_kummer",
        (2, 2, 2, 2),
        4,
        5.0,
    ),
)


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


def ceil_sqrt(value: int) -> int:
    root = math.isqrt(value)
    if root * root < value:
        root += 1
    return root


def category_bound(kind: str, p: int) -> int:
    if kind == "jacobi":
        return p + 6 * ceil_sqrt(p)
    if kind == "conic_only":
        return p + 6 * ceil_sqrt(p)
    if kind in {"quadratic_one_coordinate", "one_coordinate_kummer"}:
        return 4 * p
    if kind == "two_coordinate_kummer":
        return 9 * p
    if kind == "three_coordinate_kummer":
        return 16 * p
    raise ValueError(kind)


def category(e: int, h: int, a: int, b: int, c: int, d: int) -> str:
    active_coordinates = sum(exponent % e != 0 for exponent in (a, b, c))
    conic_active = d % h != 0
    if not conic_active:
        if active_coordinates == 0:
            return "principal"
        return "jacobi"
    if active_coordinates == 0:
        return "conic_only"
    if active_coordinates == 1 and h % 2 == 0 and d % h == h // 2:
        return "quadratic_one_coordinate"
    if active_coordinates == 1:
        return "one_coordinate_kummer"
    if active_coordinates == 2:
        return "two_coordinate_kummer"
    return "three_coordinate_kummer"


def sum_for_tuple(
    p: int,
    char_e: List[List[complex]],
    char_h: List[List[complex]],
    exponents: Tuple[int, int, int, int],
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
        for v in range(p):
            w = (-1 - u - v) % p
            value = (
                chi_u
                * chi_b[v]
                * chi_c[w]
                * psi_d[shape_a(u, v, p)]
            )
            total += value
    return total


def empty_category_record(label: str) -> Dict[str, object]:
    return {
        "count": 0,
        "bound": label,
        "max_abs": 0.0,
        "max_tuple": None,
        "max_ratio_to_p": 0.0,
    }


def audit_sample(p: int, n: int) -> Dict[str, object]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p-1")
    e = (p - 1) // n
    h = e * math.gcd(2, n)
    logs = log_table(p)
    char_e = character_table(p, e, logs)
    char_h = character_table(p, h, logs)
    categories = {
        name: empty_category_record(label)
        for name, label in BOUND_LABELS.items()
    }

    for exponents in product(range(e), range(e), range(e), range(h)):
        kind = category(e, h, *exponents)
        if kind == "principal":
            continue
        value = sum_for_tuple(p, char_e, char_h, exponents)
        magnitude = abs(value)
        record = categories[kind]
        record["count"] = int(record["count"]) + 1
        if magnitude > float(record["max_abs"]):
            record["max_abs"] = magnitude
            record["max_tuple"] = exponents
            record["max_ratio_to_p"] = magnitude / p

    for kind, record in categories.items():
        count = int(record["count"])
        if count == 0:
            continue
        bound = category_bound(kind, p)
        if float(record["max_abs"]) > bound + 1e-8:
            raise AssertionError((p, n, kind, record, bound))

    rounded_categories = {}
    for kind, record in categories.items():
        rounded_categories[kind] = {
            **record,
            "max_abs": round(float(record["max_abs"]), 10),
            "max_ratio_to_p": round(float(record["max_ratio_to_p"]), 10),
        }

    return {
        "p": p,
        "n": n,
        "e": e,
        "h": h,
        "tuple_count": e**3 * h - 1,
        "categories": rounded_categories,
    }


def audit_obstruction(check: ObstructionCheck) -> Dict[str, object]:
    (
        name,
        p,
        n,
        expected_kind,
        exponents,
        strict_multiplier,
        expected_ratio,
    ) = check
    e = (p - 1) // n
    h = e * math.gcd(2, n)
    kind = category(e, h, *exponents)
    if kind != expected_kind:
        raise AssertionError((name, "category", kind, expected_kind))
    logs = log_table(p)
    char_e = character_table(p, e, logs)
    char_h = character_table(p, h, logs)
    magnitude = abs(sum_for_tuple(p, char_e, char_h, exponents))
    if magnitude <= strict_multiplier * p + 1e-8:
        raise AssertionError((name, "not an obstruction", magnitude))
    ratio = magnitude / p
    if not math.isclose(ratio, expected_ratio, rel_tol=0.0, abs_tol=1e-8):
        raise AssertionError((name, "ratio", ratio, expected_ratio))
    return {
        "name": name,
        "p": p,
        "n": n,
        "category": kind,
        "tuple": exponents,
        "max_abs": round(magnitude, 10),
        "ratio_to_p": round(ratio, 10),
        "exceeds": f"{strict_multiplier}p",
    }


def main() -> None:
    rows = [audit_sample(sample["p"], sample["n"]) for sample in SAMPLES]
    for row in rows:
        print(row)
    for check in OBSTRUCTION_CHECKS:
        print(audit_obstruction(check))
    print("M1 depth-two Kummer constant audit passed")


if __name__ == "__main__":
    main()
