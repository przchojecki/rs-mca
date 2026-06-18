#!/usr/bin/env python3
"""Verify the M1 depth-two reciprocal two-coordinate lemma."""

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


def coordinates(u: int, v: int, p: int) -> Tuple[int, int, int]:
    return u % p, v % p, (-1 - u - v) % p


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
    mu_inv: List[complex],
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
                * mu_inv[triple[active_pair[1]]]
                * eta[shape_a(u, v, p)]
            )
    return total


def direct_line(
    p: int,
    active_pair: Tuple[int, int],
    mu: List[complex],
    mu_inv: List[complex],
    eta: List[complex],
) -> complex:
    total = 0j
    for first_value in range(p):
        u, v, triple_w = line_triple(active_pair, first_value, p)
        triple = (u, v, triple_w)
        total += (
            mu[triple[active_pair[0]]]
            * mu_inv[triple[active_pair[1]]]
            * eta[shape_a(u, v, p)]
        )
    return total


def direct_open(
    p: int,
    active_pair: Tuple[int, int],
    mu: List[complex],
    mu_inv: List[complex],
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
                * mu_inv[triple[active_pair[1]]]
                * eta[shape_a(u, v, p)]
            )
    return total


def jacobi_sum(
    p: int,
    first: List[complex],
    second: List[complex],
) -> complex:
    return sum(first[value] * second[(1 - value) % p] for value in range(p))


def ratio_a(t: int, p: int) -> int:
    return (t * t + t + 1) % p


def ratio_delta(t: int, p: int) -> int:
    return (-3 * t * t - 2 * t - 3) % p


def expected_core_nonquadratic(
    p: int,
    mu_inv: List[complex],
    eta: List[complex],
    eta_inv: List[complex],
    quadratic: List[complex],
) -> complex:
    jacobi = jacobi_sum(p, eta, quadratic)
    ratio_sum = 0j
    for t in range(p):
        delta = ratio_delta(t, p)
        ratio_sum += (
            mu_inv[t]
            * eta[delta]
            * eta_inv[ratio_a(t, p)]
            * legendre(delta, p)
        )
    return eta[pow(4, -1, p)] * jacobi * ratio_sum


def expected_core_quadratic(p: int, mu_inv: List[complex]) -> complex:
    smooth = 0j
    exceptional = 0j
    for t in range(p):
        value = mu_inv[t] * legendre(-ratio_a(t, p), p)
        smooth += value
        if ratio_delta(t, p) == 0:
            exceptional += value
    return -smooth + p * exceptional


def common_exponent(e: int, h: int, exponent: int) -> int:
    return (h // e) * exponent


def infinity_exponent(e: int, h: int, a: int, b: int, d: int) -> int:
    return (-(common_exponent(e, h, a) + common_exponent(e, h, b) + 2 * d)) % h


def reciprocal_chart_exponents(
    e: int,
    h: int,
    a: int,
    b: int,
    d: int,
) -> List[int]:
    first = common_exponent(e, h, a)
    second = common_exponent(e, h, b)
    infinity = infinity_exponent(e, h, a, b, d)
    chart_exponents: List[int] = []
    if (first + infinity) % h == 0:
        chart_exponents.append(a)
    if (second + infinity) % h == 0:
        chart_exponents.append(b)
    return chart_exponents


def equal_pair_chart_exponents(
    e: int,
    h: int,
    a: int,
    b: int,
    d: int,
) -> List[int]:
    first = common_exponent(e, h, a)
    second = common_exponent(e, h, b)
    infinity = infinity_exponent(e, h, a, b, d)
    chart_exponents: List[int] = []
    if first == infinity:
        chart_exponents.append(a)
    if second == infinity:
        chart_exponents.append(b)
    return chart_exponents


def expected_reciprocal_core(
    p: int,
    mu_inv: List[complex],
    eta: List[complex],
    eta_inv: List[complex],
    quadratic: List[complex],
    eta_is_quadratic: bool,
) -> complex:
    if eta_is_quadratic:
        return expected_core_quadratic(p, mu_inv)
    return expected_core_nonquadratic(p, mu_inv, eta, eta_inv, quadratic)


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
    nonquadratic_checked = 0
    quadratic_checked = 0
    projective_checked = 0
    projective_equal_checked = 0
    max_core_ratio = 0.0
    max_open_ratio = 0.0
    max_line_ratio = 0.0
    max_identity_error = 0.0

    for active_pair in active_pairs:
        if active_pair[0] == active_pair[1]:
            continue
        for mu_exponent in range(1, e):
            mu = char_e[mu_exponent]
            mu_inv = char_e[(-mu_exponent) % e]
            for eta_exponent in range(1, h):
                eta = char_h[eta_exponent]
                eta_inv = char_h[(-eta_exponent) % h]
                core = direct_core(p, active_pair, mu, mu_inv, eta)
                line = direct_line(p, active_pair, mu, mu_inv, eta)
                opened = direct_open(p, active_pair, mu, mu_inv, eta)
                max_identity_error = max(
                    max_identity_error,
                    abs(opened - (core - line)),
                )
                if abs(opened - (core - line)) > 1e-8:
                    raise AssertionError(
                        (p, n, active_pair, mu_exponent, eta_exponent)
                    )
                if abs(line) > 3 * math.sqrt(p) + 1e-8:
                    raise AssertionError(
                        (p, n, active_pair, mu_exponent, eta_exponent, "line")
                    )

                if h % 2 == 0 and eta_exponent == h // 2:
                    expected = expected_core_quadratic(p, mu_inv)
                    if abs(core - expected) > 1e-8:
                        raise AssertionError(
                            (
                                p,
                                n,
                                active_pair,
                                mu_exponent,
                                eta_exponent,
                                core,
                                expected,
                            )
                        )
                    if abs(core) > 2 * p + 2 * math.sqrt(p) + 1e-8:
                        raise AssertionError(
                            (p, n, active_pair, mu_exponent, "quadratic bound")
                        )
                    quadratic_checked += 1
                else:
                    expected = expected_core_nonquadratic(
                        p,
                        mu_inv,
                        eta,
                        eta_inv,
                        quadratic,
                    )
                    if abs(core - expected) > 1e-8:
                        raise AssertionError(
                            (
                                p,
                                n,
                                active_pair,
                                mu_exponent,
                                eta_exponent,
                                core,
                                expected,
                            )
                        )
                    if abs(core) > 4 * p + 1e-8:
                        raise AssertionError(
                            (
                                p,
                                n,
                                active_pair,
                                mu_exponent,
                                eta_exponent,
                                "nonquadratic bound",
                            )
                        )
                    nonquadratic_checked += 1

                checked += 1
                max_core_ratio = max(max_core_ratio, abs(core) / p)
                max_open_ratio = max(max_open_ratio, abs(opened) / p)
                max_line_ratio = max(max_line_ratio, abs(line) / math.sqrt(p))

        for first_exponent in range(1, e):
            first_char = char_e[first_exponent]
            for second_exponent in range(1, e):
                second_char = char_e[second_exponent]
                for eta_exponent in range(1, h):
                    eta = char_h[eta_exponent]
                    eta_inv = char_h[(-eta_exponent) % h]
                    eta_is_quadratic = h % 2 == 0 and eta_exponent == h // 2
                    for chart_exponent in reciprocal_chart_exponents(
                        e,
                        h,
                        first_exponent,
                        second_exponent,
                        eta_exponent,
                    ):
                        chart_char = char_e[chart_exponent]
                        chart_inv = char_e[(-chart_exponent) % e]
                        core = direct_core(
                            p,
                            active_pair,
                            first_char,
                            second_char,
                            eta,
                        )
                        chart_core = direct_core(
                            p,
                            (0, 1),
                            chart_char,
                            chart_inv,
                            eta,
                        )
                        line = direct_line(
                            p,
                            active_pair,
                            first_char,
                            second_char,
                            eta,
                        )
                        opened = direct_open(
                            p,
                            active_pair,
                            first_char,
                            second_char,
                            eta,
                        )
                        expected = expected_reciprocal_core(
                            p,
                            chart_inv,
                            eta,
                            eta_inv,
                            quadratic,
                            eta_is_quadratic,
                        )
                        max_identity_error = max(
                            max_identity_error,
                            abs(core - chart_core),
                            abs(chart_core - expected),
                            abs(opened - (core - line)),
                        )
                        if abs(core - chart_core) > 1e-8:
                            raise AssertionError(
                                (
                                    p,
                                    n,
                                    active_pair,
                                    first_exponent,
                                    second_exponent,
                                    eta_exponent,
                                    chart_exponent,
                                    core,
                                    chart_core,
                                )
                            )
                        if abs(chart_core - expected) > 1e-8:
                            raise AssertionError(
                                (
                                    p,
                                    n,
                                    active_pair,
                                    first_exponent,
                                    second_exponent,
                                    eta_exponent,
                                    chart_exponent,
                                    chart_core,
                                    expected,
                                )
                            )
                        if abs(opened - (core - line)) > 1e-8:
                            raise AssertionError(
                                (
                                    p,
                                    n,
                                    active_pair,
                                    first_exponent,
                                    second_exponent,
                                    eta_exponent,
                                    opened,
                                    core,
                                    line,
                                )
                            )
                        if abs(line) > 3 * math.sqrt(p) + 1e-8:
                            raise AssertionError(
                                (
                                    p,
                                    n,
                                    active_pair,
                                    first_exponent,
                                    second_exponent,
                                    eta_exponent,
                                    "line",
                                )
                            )
                        if eta_is_quadratic:
                            if abs(core) > 2 * p + 2 * math.sqrt(p) + 1e-8:
                                raise AssertionError(
                                    (
                                        p,
                                        n,
                                        active_pair,
                                        first_exponent,
                                        second_exponent,
                                        eta_exponent,
                                        "quadratic bound",
                                    )
                                )
                        elif abs(core) > 4 * p + 1e-8:
                            raise AssertionError(
                                (
                                    p,
                                    n,
                                    active_pair,
                                    first_exponent,
                                    second_exponent,
                                    eta_exponent,
                                    "nonquadratic bound",
                                )
                            )
                        projective_checked += 1
                        max_core_ratio = max(max_core_ratio, abs(core) / p)
                        max_open_ratio = max(max_open_ratio, abs(opened) / p)
                        max_line_ratio = max(
                            max_line_ratio,
                            abs(line) / math.sqrt(p),
                        )

                    for chart_exponent in equal_pair_chart_exponents(
                        e,
                        h,
                        first_exponent,
                        second_exponent,
                        eta_exponent,
                    ):
                        chart_char = char_e[chart_exponent]
                        core = direct_core(
                            p,
                            active_pair,
                            first_char,
                            second_char,
                            eta,
                        )
                        opened = direct_open(
                            p,
                            active_pair,
                            first_char,
                            second_char,
                            eta,
                        )
                        chart_core = direct_core(
                            p,
                            (0, 1),
                            chart_char,
                            chart_char,
                            eta,
                        )
                        chart_open = direct_open(
                            p,
                            (0, 1),
                            chart_char,
                            chart_char,
                            eta,
                        )
                        max_identity_error = max(
                            max_identity_error,
                            abs(core - chart_core),
                            abs(opened - chart_open),
                        )
                        if abs(core - chart_core) > 1e-8:
                            raise AssertionError(
                                (
                                    p,
                                    n,
                                    active_pair,
                                    first_exponent,
                                    second_exponent,
                                    eta_exponent,
                                    chart_exponent,
                                    core,
                                    chart_core,
                                )
                            )
                        if abs(opened - chart_open) > 1e-8:
                            raise AssertionError(
                                (
                                    p,
                                    n,
                                    active_pair,
                                    first_exponent,
                                    second_exponent,
                                    eta_exponent,
                                    chart_exponent,
                                    opened,
                                    chart_open,
                                )
                            )
                        projective_equal_checked += 1
                        max_core_ratio = max(max_core_ratio, abs(core) / p)
                        max_open_ratio = max(max_open_ratio, abs(opened) / p)

    return {
        "p": p,
        "n": n,
        "e": e,
        "h": h,
        "checked": checked,
        "projective_checked": projective_checked,
        "projective_equal_checked": projective_equal_checked,
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
    print("M1 depth-two reciprocal two-coordinate verifier passed")


if __name__ == "__main__":
    main()
