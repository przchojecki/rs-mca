#!/usr/bin/env python3
"""Verify the M1 depth-two infinity-unramified two-coordinate lemma."""

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
    {"p": 109, "n": 18},
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
    value %= p
    if value == 0:
        return 0
    return 1 if pow(value, (p - 1) // 2, p) == 1 else -1


def shape_a(u: int, v: int, p: int) -> int:
    return (-(u * u + v * v + u * v + u + v + 1)) % p


def triple_from_active(
    active_pair: Tuple[int, int],
    first_value: int,
    second_value: int,
    p: int,
) -> Tuple[int, int, int]:
    triple = [0, 0, 0]
    first_index, second_index = active_pair
    inactive_index = next(index for index in range(3) if index not in active_pair)
    triple[first_index] = first_value % p
    triple[second_index] = second_value % p
    triple[inactive_index] = (-1 - first_value - second_value) % p
    return triple[0], triple[1], triple[2]


def line_triple(
    active_pair: Tuple[int, int],
    first_value: int,
    p: int,
) -> Tuple[int, int, int]:
    second_value = (-1 - first_value) % p
    triple = [0, 0, 0]
    first_index, second_index = active_pair
    inactive_index = next(index for index in range(3) if index not in active_pair)
    triple[first_index] = first_value % p
    triple[second_index] = second_value
    triple[inactive_index] = 0
    return triple[0], triple[1], triple[2]


def direct_core(
    p: int,
    active_pair: Tuple[int, int],
    mu: List[complex],
    nu: List[complex],
    eta: List[complex],
) -> complex:
    total = 0j
    for first_value in range(p):
        for second_value in range(p):
            u, v, triple_w = triple_from_active(
                active_pair,
                first_value,
                second_value,
                p,
            )
            triple = (u, v, triple_w)
            total += (
                mu[triple[active_pair[0]]]
                * nu[triple[active_pair[1]]]
                * eta[shape_a(u, v, p)]
            )
    return total


def direct_line(
    p: int,
    active_pair: Tuple[int, int],
    mu: List[complex],
    nu: List[complex],
    eta: List[complex],
) -> complex:
    total = 0j
    for first_value in range(p):
        u, v, triple_w = line_triple(active_pair, first_value, p)
        triple = (u, v, triple_w)
        total += (
            mu[triple[active_pair[0]]]
            * nu[triple[active_pair[1]]]
            * eta[shape_a(u, v, p)]
        )
    return total


def direct_open(
    p: int,
    active_pair: Tuple[int, int],
    mu: List[complex],
    nu: List[complex],
    eta: List[complex],
) -> complex:
    inactive_index = next(index for index in range(3) if index not in active_pair)
    total = 0j
    for first_value in range(p):
        for second_value in range(p):
            u, v, triple_w = triple_from_active(
                active_pair,
                first_value,
                second_value,
                p,
            )
            triple = (u, v, triple_w)
            if triple[inactive_index] == 0:
                continue
            total += (
                mu[triple[active_pair[0]]]
                * nu[triple[active_pair[1]]]
                * eta[shape_a(u, v, p)]
            )
    return total


def jacobi_sum(
    p: int,
    first: List[complex],
    second: List[complex],
) -> complex:
    return sum(first[value] * second[(1 - value) % p] for value in range(p))


def ratio_b(t: int, p: int) -> int:
    return (t * t + t + 1) % p


def ratio_delta(t: int, p: int) -> int:
    return (-3 * t * t - 2 * t - 3) % p


def expected_core(
    p: int,
    mu: List[complex],
    eta: List[complex],
    quadratic: List[complex],
    eta_is_quadratic: bool,
) -> complex:
    missing = 0j
    for t in range(p):
        missing += mu[t] * eta[(-ratio_b(t, p)) % p]

    if eta_is_quadratic:
        full = 0j
        sign = legendre(-1, p)
        for t in range(p):
            full += mu[t] * (-sign)
            if ratio_delta(t, p) == 0:
                full += mu[t] * p * sign
        return full - missing

    jacobi = jacobi_sum(p, eta, quadratic)
    full_ratio_sum = 0j
    for t in range(p):
        delta = ratio_delta(t, p)
        full_ratio_sum += mu[t] * eta[delta] * legendre(delta, p)
    return eta[pow(4, -1, p)] * jacobi * full_ratio_sum - missing


def infinity_unramified_b_values(e: int, h: int, a: int, d: int) -> List[int]:
    multiplier = h // e
    return [
        b
        for b in range(1, e)
        if (multiplier * (a + b) + 2 * d) % h == 0
    ]


def audit_sample(p: int, n: int) -> Dict[str, object]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p-1")
    e = (p - 1) // n
    h = e * math.gcd(2, n)
    logs = log_table(p)
    char_e = character_table(p, e, logs)
    char_h = character_table(p, h, logs)
    quadratic = [complex(legendre(value, p)) for value in range(p)]
    active_pairs = tuple(product(range(3), repeat=2))

    checked = 0
    quadratic_checked = 0
    nonquadratic_checked = 0
    max_core_ratio = 0.0
    max_open_ratio = 0.0
    max_line_ratio = 0.0
    max_identity_error = 0.0

    for active_pair in active_pairs:
        if active_pair[0] == active_pair[1]:
            continue
        for mu_exponent in range(1, e):
            mu = char_e[mu_exponent]
            for eta_exponent in range(1, h):
                eta = char_h[eta_exponent]
                eta_is_quadratic = (2 * eta_exponent) % h == 0
                for nu_exponent in infinity_unramified_b_values(
                    e,
                    h,
                    mu_exponent,
                    eta_exponent,
                ):
                    nu = char_e[nu_exponent]
                    core = direct_core(p, active_pair, mu, nu, eta)
                    line = direct_line(p, active_pair, mu, nu, eta)
                    opened = direct_open(p, active_pair, mu, nu, eta)
                    expected = expected_core(
                        p,
                        mu,
                        eta,
                        quadratic,
                        eta_is_quadratic,
                    )
                    max_identity_error = max(
                        max_identity_error,
                        abs(core - expected),
                        abs(opened - (core - line)),
                    )
                    if abs(core - expected) > 1e-8:
                        raise AssertionError(
                            (p, n, active_pair, mu_exponent, nu_exponent,
                             eta_exponent, core, expected)
                        )
                    if abs(opened - (core - line)) > 1e-8:
                        raise AssertionError(
                            (p, n, active_pair, mu_exponent, nu_exponent,
                             eta_exponent, opened, core, line)
                        )
                    if abs(core) > 2 * p + 2 * math.sqrt(p) + 1e-8:
                        raise AssertionError(
                            (p, n, "core", active_pair, mu_exponent,
                             nu_exponent, eta_exponent, abs(core))
                        )
                    if abs(line) > 3 * math.sqrt(p) + 1e-8:
                        raise AssertionError(
                            (p, n, "line", active_pair, mu_exponent,
                             nu_exponent, eta_exponent, abs(line))
                        )
                    if abs(opened) > 2 * p + 5 * math.sqrt(p) + 1e-8:
                        raise AssertionError(
                            (p, n, "open", active_pair, mu_exponent,
                             nu_exponent, eta_exponent, abs(opened))
                        )
                    checked += 1
                    quadratic_checked += int(eta_is_quadratic)
                    nonquadratic_checked += int(not eta_is_quadratic)
                    max_core_ratio = max(max_core_ratio, abs(core) / p)
                    max_open_ratio = max(max_open_ratio, abs(opened) / p)
                    max_line_ratio = max(max_line_ratio, abs(line) / math.sqrt(p))

    return {
        "p": p,
        "n": n,
        "e": e,
        "h": h,
        "checked": checked,
        "quadratic_checked": quadratic_checked,
        "nonquadratic_checked": nonquadratic_checked,
        "max_core_ratio_to_p": round(max_core_ratio, 10),
        "max_open_ratio_to_p": round(max_open_ratio, 10),
        "max_line_ratio_to_sqrt_p": round(max_line_ratio, 10),
        "max_identity_error": f"{max_identity_error:.2e}",
    }


def main() -> None:
    rows = [audit_sample(sample["p"], sample["n"]) for sample in SAMPLES]
    for row in rows:
        print(row)
    print("M1 depth-two infinity-unramified two-coordinate verifier passed")


if __name__ == "__main__":
    main()
