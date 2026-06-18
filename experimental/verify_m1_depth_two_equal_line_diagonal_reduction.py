#!/usr/bin/env python3
"""Verify the M1 equal-line diagonal symmetric-coordinate reduction."""

from __future__ import annotations

import cmath
import math
from typing import Dict, List, Tuple


CASES = (
    {"p": 89, "n": 8, "a": 1, "d": 8},
    {"p": 181, "n": 20, "a": 5, "d": 12},
    {"p": 421, "n": 20, "a": 5, "d": 6},
    {"p": 461, "n": 20, "a": 18, "d": 15},
)

EXPECTED_TOP = {
    "p": 421,
    "n": 20,
    "a": 5,
    "d": 6,
    "sum_ratio": 3.9771715522,
    "jacobi_ratio": 1.0485702499,
    "residual_ratio": 2.9290031282,
    "pullback_main_ratio": 2.9043632895,
    "exceptional_sqrt_ratio": 1.0,
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


def quadratic_character(value: int, p: int) -> int:
    value %= p
    if value == 0:
        return 0
    return 1 if pow(value, (p - 1) // 2, p) == 1 else -1


def shape_a(u: int, v: int, p: int) -> int:
    return (-(u * u + v * v + u * v + u + v + 1)) % p


def shape_b(s: int, p: int) -> int:
    return (s * s + s + 1) % p


def shape_c(s: int, p: int) -> int:
    return (3 * s * s + 4 * s + 4) % p


def lambda_value(s: int, p: int) -> int:
    denominator = (4 * shape_b(s, p)) % p
    if denominator == 0:
        raise ZeroDivisionError((s, p))
    return (s * s * pow(denominator, -1, p)) % p


def line_monodromies(e: int, h: int, a: int, d: int) -> Tuple[int, int, int]:
    lift = h // e
    first = (lift * a) % h
    second = first
    infinity = (-(first + second + 2 * d)) % h
    return first, second, infinity


def direct_open_sum(
    p: int,
    mu: List[complex],
    eta: List[complex],
) -> complex:
    total = 0j
    for u in range(p):
        mu_u = mu[u]
        if mu_u == 0j:
            continue
        for v in range(p):
            w = (-1 - u - v) % p
            if w == 0:
                continue
            total += mu_u * mu[v] * eta[shape_a(u, v, p)]
    return total


def jacobi_minus(mu: List[complex], eta: List[complex]) -> complex:
    return sum(mu[t] * eta[(t - 1) % len(mu)] for t in range(len(mu)))


def diagonal_reduction_parts(
    p: int,
    mu: List[complex],
    eta: List[complex],
    rho: List[complex],
) -> Tuple[complex, complex, complex]:
    jacobi_factor = jacobi_minus(mu, eta)
    base_sum = sum(
        rho[shape_b(s, p)]
        for s in range(p)
        if s != p - 1
    )
    jacobi_part = jacobi_factor * base_sum
    first_direct = 0j
    residual = 0j
    for s in range(p):
        if s == p - 1:
            continue
        b_value = shape_b(s, p)
        for t in range(p):
            summand = mu[t] * eta[(t - b_value) % p]
            first_direct += summand
            residual += quadratic_character(s * s - 4 * t, p) * summand
    return jacobi_part, first_direct, residual


def hypergeometric_trace(
    p: int,
    mu: List[complex],
    eta: List[complex],
    lam: int,
) -> complex:
    return sum(
        mu[x] * eta[(x - 1) % p] * quadratic_character(x - lam, p)
        for x in range(p)
    )


def residual_pullback_parts(
    p: int,
    mu: List[complex],
    eta: List[complex],
    rho: List[complex],
) -> Tuple[complex, complex]:
    pullback_main = 0j
    exceptional = 0j
    for s in range(p):
        if s == p - 1:
            continue
        b_value = shape_b(s, p)
        if b_value == 0:
            exceptional += sum(
                quadratic_character(s * s - 4 * t, p)
                * mu[t]
                * eta[t]
                for t in range(p)
            )
            continue
        lam = (s * s * pow(4 * b_value, -1, p)) % p
        pullback_main += (
            quadratic_character(-4, p)
            * rho[b_value]
            * hypergeometric_trace(p, mu, eta, lam)
        )
    return pullback_main, exceptional


def verify_pullback_branch_geometry(p: int) -> Dict[str, object]:
    if p <= 3:
        raise AssertionError(p)
    roots_b = [s for s in range(p) if shape_b(s, p) == 0]
    roots_c = [s for s in range(p) if shape_c(s, p) == 0]
    if any(shape_c(s, p) == 0 for s in roots_b):
        raise AssertionError(("B and C meet", p, roots_b, roots_c))
    if shape_b(0, p) != 1 or shape_c(0, p) != 4 % p:
        raise AssertionError(("bad zero fiber", p))
    if shape_b(p - 1, p) != 1 or shape_c(p - 1, p) != 3 % p:
        raise AssertionError(("bad deleted point", p))
    if shape_b(p - 2, p) != 3 % p or shape_c(p - 2, p) != 8 % p:
        raise AssertionError(("bad second critical point", p))
    if lambda_value(p - 1, p) != pow(4, -1, p):
        raise AssertionError(("lambda(-1)", p, lambda_value(p - 1, p)))
    if lambda_value(p - 2, p) != pow(3, -1, p):
        raise AssertionError(("lambda(-2)", p, lambda_value(p - 2, p)))
    for s in range(p):
        if shape_b(s, p) == 0:
            continue
        lam = lambda_value(s, p)
        if (lam == 0) != (s == 0):
            raise AssertionError(("lambda zero", p, s, lam))
        if (lam == 1) != (shape_c(s, p) == 0):
            raise AssertionError(("lambda one", p, s, lam))
    return {
        "p": p,
        "b_root_count": len(roots_b),
        "c_root_count": len(roots_c),
        "lambda_minus_one": pow(4, -1, p),
        "lambda_minus_two": pow(3, -1, p),
    }


def audit_case(case: Dict[str, int]) -> Dict[str, object]:
    p = int(case["p"])
    n = int(case["n"])
    a = int(case["a"])
    d = int(case["d"])
    if (p - 1) % n != 0:
        raise AssertionError(case)
    e = (p - 1) // n
    h = e * math.gcd(2, n)
    lift = h // e
    monodromies = line_monodromies(e, h, a, d)
    if len(set(monodromies)) != 1:
        raise AssertionError((case, monodromies))
    if (3 * monodromies[0] + 2 * d) % h != 0:
        raise AssertionError((case, monodromies))

    logs = log_table(p)
    characters = character_table(p, h, logs)
    mu = characters[(lift * a) % h]
    eta = characters[d % h]
    rho = characters[(lift * a + d) % h]
    rho_chi = characters[(lift * a + d + h // 2) % h]
    if (lift * a + d) % h == 0:
        raise AssertionError(("mu eta unexpectedly principal", case))
    if (lift * a + d + h // 2) % h == 0:
        raise AssertionError(("mu eta chi_2 unexpectedly principal", case))

    direct = direct_open_sum(p, mu, eta)
    jacobi_part, first_direct, residual = diagonal_reduction_parts(
        p,
        mu,
        eta,
        rho,
    )
    pullback_main, exceptional = residual_pullback_parts(
        p,
        mu,
        eta,
        rho_chi,
    )
    if abs(jacobi_part - first_direct) > 1e-8:
        raise AssertionError((case, jacobi_part, first_direct))
    if abs(direct - (jacobi_part + residual)) > 1e-8:
        raise AssertionError((case, direct, jacobi_part, residual))
    if abs(residual - (pullback_main + exceptional)) > 1e-8:
        raise AssertionError((case, residual, pullback_main, exceptional))
    if abs(exceptional) > 2 * math.sqrt(p) + 1e-8:
        raise AssertionError((case, exceptional))
    jacobi_bound = p + math.sqrt(p)
    if abs(jacobi_part) > jacobi_bound + 1e-8:
        raise AssertionError((case, abs(jacobi_part), jacobi_bound))

    return {
        "p": p,
        "n": n,
        "e": e,
        "h": h,
        "a": a,
        "d": d,
        "line_monodromies": monodromies,
        "sum_ratio": round(abs(direct) / p, 10),
        "jacobi_ratio": round(abs(jacobi_part) / p, 10),
        "residual_ratio": round(abs(residual) / p, 10),
        "pullback_main_ratio": round(abs(pullback_main) / p, 10),
        "exceptional_sqrt_ratio": round(abs(exceptional) / math.sqrt(p), 10),
        "identity_error": f"{abs(direct - (jacobi_part + residual)):.2e}",
        "pullback_error": f"{abs(residual - (pullback_main + exceptional)):.2e}",
    }


def main() -> None:
    rows = [audit_case(case) for case in CASES]
    for row in rows:
        print(row)
    branch_rows = [
        verify_pullback_branch_geometry(int(case["p"]))
        for case in CASES
    ]
    for row in branch_rows:
        print(row)
    top = max(rows, key=lambda row: float(row["sum_ratio"]))
    for key, value in EXPECTED_TOP.items():
        actual = top[key]
        if actual != value:
            raise AssertionError((key, actual, value, top))
    print("M1 equal-line diagonal reduction verifier passed")


if __name__ == "__main__":
    main()
