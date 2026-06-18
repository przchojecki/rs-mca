#!/usr/bin/env python3
"""Verify the M1 nonquadratic one-coordinate depth-two lemma."""

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


def inv(value: int, p: int) -> int:
    return pow(value % p, p - 2, p)


def shape_a(u: int, v: int, p: int) -> int:
    return (-(u * u + v * v + u * v + u + v + 1)) % p


def coordinates(u: int, v: int, p: int) -> Tuple[int, int, int]:
    return u % p, v % p, (-1 - u - v) % p


def delta(value: int, p: int) -> int:
    return (-3 * value * value - 2 * value - 3) % p


def legendre(value: int, p: int) -> int:
    residue = pow(value % p, (p - 1) // 2, p)
    if residue == p - 1:
        return -1
    return residue


def jacobi_eta_quadratic(p: int, eta: List[complex]) -> complex:
    return sum(eta[t] * legendre(1 - t, p) for t in range(p))


def inner_sum(
    p: int,
    eta: List[complex],
    active: int,
    fixed_value: int,
) -> complex:
    total = 0j
    if active == 0:
        for v in range(p):
            total += eta[shape_a(fixed_value, v, p)]
    elif active == 1:
        for u in range(p):
            total += eta[shape_a(u, fixed_value, p)]
    else:
        for u in range(p):
            v = (-1 - u - fixed_value) % p
            total += eta[shape_a(u, v, p)]
    return total


def expected_inner_sum(p: int, eta: List[complex], fixed_value: int) -> complex:
    return (
        eta[inv(4, p)]
        * jacobi_eta_quadratic(p, eta)
        * eta[delta(fixed_value, p)]
        * legendre(delta(fixed_value, p), p)
    )


def discriminant_sum(p: int, mu: List[complex], eta: List[complex]) -> complex:
    return sum(
        mu[u] * legendre(delta(u, p), p) * eta[delta(u, p)]
        for u in range(p)
    )


def expected_full_sum(p: int, mu: List[complex], eta: List[complex]) -> complex:
    return eta[inv(4, p)] * jacobi_eta_quadratic(p, eta) * discriminant_sum(
        p,
        mu,
        eta,
    )


def full_sum(
    p: int,
    mu: List[complex],
    eta: List[complex],
    active: int,
) -> complex:
    total = 0j
    for u in range(p):
        for v in range(p):
            triple = coordinates(u, v, p)
            total += mu[triple[active]] * eta[shape_a(u, v, p)]
    return total


def open_sum(
    p: int,
    mu: List[complex],
    eta: List[complex],
    active: int,
) -> complex:
    total = 0j
    for u in range(p):
        for v in range(p):
            triple = coordinates(u, v, p)
            if any(value == 0 for value in triple):
                continue
            total += mu[triple[active]] * eta[shape_a(u, v, p)]
    return total


def is_quadratic_exponent(order: int, exponent: int) -> bool:
    return order % 2 == 0 and exponent % order == order // 2


def audit_sample(p: int, n: int) -> Dict[str, object]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p-1")
    e = (p - 1) // n
    h = e * math.gcd(2, n)
    logs = log_table(p)
    char_e = character_table(p, e, logs)
    char_h = character_table(p, h, logs)
    sqrt_p = math.sqrt(p)
    max_jacobi_ratio = 0.0
    max_disc_ratio = 0.0
    max_full_ratio = 0.0
    max_open_ratio = 0.0
    checked = 0

    for coordinate_exponent in range(1, e):
        mu = char_e[coordinate_exponent]
        for conic_exponent in range(1, h):
            if is_quadratic_exponent(h, conic_exponent):
                continue
            eta = char_h[conic_exponent]
            jacobi = jacobi_eta_quadratic(p, eta)
            disc = discriminant_sum(p, mu, eta)
            predicted = expected_full_sum(p, mu, eta)
            if abs(jacobi) > sqrt_p + 1e-8:
                raise AssertionError((p, n, conic_exponent, "jacobi", jacobi))
            if abs(disc) > 2 * sqrt_p + 1e-8:
                raise AssertionError((p, n, coordinate_exponent, disc))
            for fixed_value in range(p):
                expected_inner = expected_inner_sum(p, eta, fixed_value)
                for active in range(3):
                    actual_inner = inner_sum(p, eta, active, fixed_value)
                    if abs(actual_inner - expected_inner) > 1e-8:
                        raise AssertionError(
                            (p, n, conic_exponent, active, fixed_value)
                        )
            for active in range(3):
                full = full_sum(p, mu, eta, active)
                opened = open_sum(p, mu, eta, active)
                correction = full - opened
                if abs(full - predicted) > 1e-8:
                    raise AssertionError(
                        (p, n, coordinate_exponent, conic_exponent, active)
                    )
                if abs(full) > 2 * p + 1e-8:
                    raise AssertionError((p, n, "full", full))
                if abs(correction) > (2 * p - 1) + 1e-8:
                    raise AssertionError((p, n, "correction", correction))
                if abs(opened) > 4 * p + 1e-8:
                    raise AssertionError((p, n, "open", opened))
                max_full_ratio = max(max_full_ratio, abs(full) / p)
                max_open_ratio = max(max_open_ratio, abs(opened) / p)
                checked += 1
            max_jacobi_ratio = max(max_jacobi_ratio, abs(jacobi) / sqrt_p)
            max_disc_ratio = max(max_disc_ratio, abs(disc) / sqrt_p)

    return {
        "p": p,
        "n": n,
        "e": e,
        "h": h,
        "checked": checked,
        "jacobi_over_sqrt_p": round(max_jacobi_ratio, 10),
        "disc_over_sqrt_p": round(max_disc_ratio, 10),
        "full_over_p": round(max_full_ratio, 10),
        "open_over_p": round(max_open_ratio, 10),
    }


def main() -> None:
    rows = [audit_sample(sample["p"], sample["n"]) for sample in SAMPLES]
    for row in rows:
        print(row)
    print("M1 depth-two nonquadratic one-coordinate verifier passed")


if __name__ == "__main__":
    main()
