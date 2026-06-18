#!/usr/bin/env python3
"""Verify the M1 quadratic one-coordinate depth-two lemma."""

from __future__ import annotations

import cmath
import math
from typing import Dict, List, Tuple


SAMPLES = (
    {"p": 17, "n": 8},
    {"p": 31, "n": 10},
    {"p": 37, "n": 9},
    {"p": 43, "n": 14},
    {"p": 61, "n": 20},
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


def legendre(value: int, p: int) -> int:
    residue = pow(value % p, (p - 1) // 2, p)
    if residue == p - 1:
        return -1
    return residue


def shape_a(u: int, v: int, p: int) -> int:
    return (-(u * u + v * v + u * v + u + v + 1)) % p


def coordinates(u: int, v: int, p: int) -> Tuple[int, int, int]:
    return u % p, v % p, (-1 - u - v) % p


def delta(value: int, p: int) -> int:
    return (-3 * value * value - 2 * value - 3) % p


def delta_roots(p: int) -> List[int]:
    return [value for value in range(p) if delta(value, p) == 0]


def full_sum(p: int, char: List[complex], active: int) -> complex:
    total = 0j
    for u in range(p):
        for v in range(p):
            triple = coordinates(u, v, p)
            total += char[triple[active]] * legendre(shape_a(u, v, p), p)
    return total


def open_sum(p: int, char: List[complex], active: int) -> complex:
    total = 0j
    for u in range(p):
        for v in range(p):
            triple = coordinates(u, v, p)
            if any(value == 0 for value in triple):
                continue
            total += char[triple[active]] * legendre(shape_a(u, v, p), p)
    return total


def expected_full_sum(p: int, char: List[complex]) -> complex:
    root_sum = sum(char[root] for root in delta_roots(p))
    return p * legendre(-1, p) * root_sum


def audit_sample(p: int, n: int) -> Dict[str, object]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p-1")
    e = (p - 1) // n
    logs = log_table(p)
    chars = character_table(p, e, logs)
    max_full = 0.0
    max_correction = 0.0
    max_open = 0.0
    worst_tuple = None

    for exponent in range(1, e):
        char = chars[exponent]
        expected = expected_full_sum(p, char)
        for active in range(3):
            full = full_sum(p, char, active)
            opened = open_sum(p, char, active)
            correction = full - opened
            if abs(full - expected) > 1e-8:
                raise AssertionError((p, n, exponent, active, full, expected))
            if abs(full) > 2 * p + 1e-8:
                raise AssertionError((p, n, exponent, active, "full", full))
            if abs(correction) > (2 * p - 1) + 1e-8:
                raise AssertionError((p, n, exponent, active, correction))
            if abs(opened) > 4 * p + 1e-8:
                raise AssertionError((p, n, exponent, active, opened))
            if abs(opened) > max_open:
                worst_tuple = (exponent, active)
            max_full = max(max_full, abs(full))
            max_correction = max(max_correction, abs(correction))
            max_open = max(max_open, abs(opened))

    return {
        "p": p,
        "n": n,
        "e": e,
        "delta_roots": delta_roots(p),
        "max_full_ratio_to_p": round(max_full / p, 10),
        "max_correction_ratio_to_p": round(max_correction / p, 10),
        "max_open_ratio_to_p": round(max_open / p, 10),
        "max_open_tuple": worst_tuple,
    }


def main() -> None:
    rows = [audit_sample(sample["p"], sample["n"]) for sample in SAMPLES]
    for row in rows:
        print(row)
    print("M1 depth-two quadratic one-coordinate verifier passed")


if __name__ == "__main__":
    main()
