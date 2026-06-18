#!/usr/bin/env python3
"""Verify the M1 depth-two line-conic resonance reduction."""

from __future__ import annotations

import cmath
import math
from typing import Dict, Iterable, List, Tuple


EXHAUSTIVE_PRIMES = (17, 31)
TARGETED_CASES = (
    (37, 2, 5),
    (37, 7, 11),
    (43, 3, 8),
    (43, 12, 5),
    (61, 5, 17),
    (61, 19, 7),
)
TOLERANCE = 1e-7


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


def character_table(p: int, logs: Dict[int, int]) -> List[List[complex]]:
    order = p - 1
    table: List[List[complex]] = []
    for exponent in range(order):
        row = [0j]
        for value in range(1, p):
            angle = 2.0 * math.pi * exponent * logs[value] / order
            row.append(cmath.exp(1j * angle))
        table.append(row)
    return table


def legendre(value: int, p: int) -> int:
    value %= p
    if value == 0:
        return 0
    return 1 if pow(value, (p - 1) // 2, p) == 1 else -1


def shape_a(u: int, v: int, p: int) -> int:
    return (-(u * u + v * v + u * v + u + v + 1)) % p


def shape_b(v: int, p: int) -> int:
    return (v * v + v + 1) % p


def q_y_v(y: int, v: int, p: int) -> int:
    return (y * y - 2 * (v + 1) * y - 3 * v * v - 2 * v - 3) % p


def direct_core(
    p: int,
    eta_inv: List[complex],
    nu: List[complex],
    eta: List[complex],
) -> complex:
    total = 0j
    for u in range(p):
        for v in range(p):
            total += eta_inv[u] * nu[v] * eta[shape_a(u, v, p)]
    return total


def direct_open(
    p: int,
    eta_inv: List[complex],
    nu: List[complex],
    eta: List[complex],
) -> complex:
    total = 0j
    for u in range(p):
        for v in range(p):
            if (-1 - u - v) % p == 0:
                continue
            total += eta_inv[u] * nu[v] * eta[shape_a(u, v, p)]
    return total


def line_correction(
    p: int,
    eta_inv: List[complex],
    nu: List[complex],
    eta: List[complex],
) -> complex:
    total = 0j
    for u in range(p):
        v = (-1 - u) % p
        total += eta_inv[u] * nu[v] * eta[shape_a(u, v, p)]
    return total


def fiber_transform(
    p: int,
    v: int,
    eta: List[complex],
) -> complex:
    total = 0j
    b_value = shape_b(v, p)
    for x in range(p):
        total += legendre(x * x - 4 * b_value, p) * eta[(-x - v - 1) % p]
    return total


def direct_resonant_fiber(
    p: int,
    v: int,
    eta_inv: List[complex],
    eta: List[complex],
) -> complex:
    total = 0j
    for u in range(p):
        total += eta_inv[u] * eta[shape_a(u, v, p)]
    return total


def transformed_core(
    p: int,
    eta: List[complex],
    nu: List[complex],
) -> complex:
    total = 0j
    for y in range(p):
        inner = 0j
        for v in range(p):
            inner += nu[v] * legendre(q_y_v(y, v, p), p)
        total += eta[(-y) % p] * inner
    return total


def assert_close(label: Tuple[object, ...], actual: complex, expected: complex) -> None:
    if abs(actual - expected) > TOLERANCE:
        raise AssertionError((label, actual, expected, abs(actual - expected)))


def case_iterator() -> Iterable[Tuple[int, int, int]]:
    for p in EXHAUSTIVE_PRIMES:
        for eta_exponent in range(1, p - 1):
            for nu_exponent in range(1, p - 1):
                yield p, eta_exponent, nu_exponent
    yield from TARGETED_CASES


def verify_discriminant_values(p: int) -> None:
    for y in range(p):
        a = -3 % p
        b = (-2 * (y + 1)) % p
        c = (y * y - 2 * y - 3) % p
        discriminant = (b * b - 4 * a * c) % p
        expected = (16 * (y - 2) * (y + 1)) % p
        if discriminant != expected:
            raise AssertionError((p, y, discriminant, expected))
        q_at_zero = q_y_v(y, 0, p)
        expected_zero = ((y - 3) * (y + 1)) % p
        if q_at_zero != expected_zero:
            raise AssertionError((p, y, q_at_zero, expected_zero))


def main() -> None:
    tables: Dict[int, List[List[complex]]] = {}
    checked_cases = 0
    checked_fibers = 0
    checked_open_decompositions = 0
    max_difference = 0.0
    for p, eta_exponent, nu_exponent in case_iterator():
        if p not in tables:
            logs = log_table(p)
            tables[p] = character_table(p, logs)
            verify_discriminant_values(p)
        table = tables[p]
        eta = table[eta_exponent]
        eta_inv = table[(-eta_exponent) % (p - 1)]
        nu = table[nu_exponent]
        for v in range(p):
            direct = direct_resonant_fiber(p, v, eta_inv, eta)
            transformed = fiber_transform(p, v, eta)
            assert_close((p, eta_exponent, v, "fiber"), direct, transformed)
            max_difference = max(max_difference, abs(direct - transformed))
            checked_fibers += 1
        direct = direct_core(p, eta_inv, nu, eta)
        transformed = transformed_core(p, eta, nu)
        assert_close((p, eta_exponent, nu_exponent, "core"), direct, transformed)
        max_difference = max(max_difference, abs(direct - transformed))
        direct_open_sum = direct_open(p, eta_inv, nu, eta)
        corrected_core = direct - line_correction(p, eta_inv, nu, eta)
        assert_close(
            (p, eta_exponent, nu_exponent, "open"),
            direct_open_sum,
            corrected_core,
        )
        max_difference = max(max_difference, abs(direct_open_sum - corrected_core))
        checked_open_decompositions += 1
        checked_cases += 1
    print(
        "verify_m1_depth_two_line_conic_resonance_reduction: PASS",
        f"cases={checked_cases}",
        f"fibers={checked_fibers}",
        f"open_decompositions={checked_open_decompositions}",
        f"max_difference={max_difference:.3e}",
    )


if __name__ == "__main__":
    main()
