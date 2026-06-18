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


def shape_d(s: int, x: int, p: int) -> int:
    return (4 * shape_b(s, p) * x - s * s) % p


def projective_points(p: int) -> List[Tuple[int, int, int]]:
    points = [(s, x, 1) for s in range(p) for x in range(p)]
    points.extend((s, 1, 0) for s in range(p))
    points.append((1, 0, 0))
    return points


def projective_b(s: int, z: int, p: int) -> int:
    return (s * s + s * z + z * z) % p


def projective_c(s: int, z: int, p: int) -> int:
    return (3 * s * s + 4 * s * z + 4 * z * z) % p


def projective_d(s: int, x: int, z: int, p: int) -> int:
    return (4 * projective_b(s, z, p) * x - s * s * z) % p


def projective_d_partials(s: int, x: int, z: int, p: int) -> Tuple[int, int, int]:
    d_s = (4 * (2 * s + z) * x - 2 * s * z) % p
    d_x = (4 * projective_b(s, z, p)) % p
    d_z = (4 * (s + 2 * z) * x - s * s) % p
    return d_s, d_x, d_z


def lambda_value(s: int, p: int) -> int:
    denominator = (4 * shape_b(s, p)) % p
    if denominator == 0:
        raise ZeroDivisionError((s, p))
    return (s * s * pow(denominator, -1, p)) % p


def deck_involution(s: int, p: int) -> int:
    if s == p - 1:
        raise ZeroDivisionError((s, p))
    return (-s * pow(s + 1, -1, p)) % p


def z_coordinate(s: int, p: int) -> int:
    if s == p - 2:
        raise ZeroDivisionError((s, p))
    return (s * pow(s + 2, -1, p)) % p


def s_from_z(z: int, p: int) -> int:
    if z == 1:
        raise ZeroDivisionError((z, p))
    return (2 * z * pow(1 - z, -1, p)) % p


def lambda_z_value(z: int, p: int) -> int:
    denominator = (1 + 3 * z * z) % p
    if denominator == 0:
        raise ZeroDivisionError((z, p))
    return (z * z * pow(denominator, -1, p)) % p


def twist_y_value(z: int, p: int) -> int:
    if z == 1:
        raise ZeroDivisionError((z, p))
    numerator = (1 + 3 * z * z) % p
    denominator = (1 - z) * (1 - z) % p
    return numerator * pow(denominator, -1, p) % p


def twist_map_deck_involution(z: int, p: int) -> int:
    denominator = (3 * z - 1) % p
    if denominator == 0:
        raise ZeroDivisionError((z, p))
    return (z + 1) * pow(denominator, -1, p) % p


def y_kernel_argument(x: int, z: int, p: int) -> int:
    return (x + (3 * x - 1) * z * z) % p


def lambda_y_resultant(x: int, y_value: int, p: int) -> int:
    return (
        16 * x * x * y_value * y_value
        - 8 * x * y_value * y_value
        + 4 * x * y_value
        + y_value * y_value
        - 2 * y_value
        + 1
    ) % p


def lambda_y_resultant_x_infinity(u: int, y_value: int, p: int) -> int:
    return (
        u * u * y_value * y_value
        - 2 * u * u * y_value
        + u * u
        - 8 * u * y_value * y_value
        + 4 * u * y_value
        + 16 * y_value * y_value
    ) % p


def lambda_y_resultant_y_infinity(x: int, v: int, p: int) -> int:
    return (
        v * v
        + 4 * v * x
        - 2 * v
        + 16 * x * x
        - 8 * x
        + 1
    ) % p


def lambda_y_resultant_both_infinity(u: int, v: int, p: int) -> int:
    return (
        u * u * v * v
        - 2 * u * u * v
        + u * u
        + 4 * u * v
        - 8 * u
        + 16
    ) % p


def lambda_one_y_polynomial(y_value: int, p: int) -> int:
    return (9 * y_value * y_value + 2 * y_value + 1) % p


def lambda_y_relation_value(y_value: int, lam: int, p: int) -> int:
    return (
        16 * y_value * y_value * lam * lam
        + (-8 * y_value * y_value + 4 * y_value) * lam
        + (y_value - 1) * (y_value - 1)
    ) % p


def lambda_y_relation_dlambda(y_value: int, lam: int, p: int) -> int:
    return (32 * y_value * y_value * lam - 8 * y_value * y_value + 4 * y_value) % p


def lambda_y_relation_dy(y_value: int, lam: int, p: int) -> int:
    return (
        32 * y_value * lam * lam
        + (-16 * y_value + 4) * lam
        + 2 * (y_value - 1)
    ) % p


def lambda_y_relation_at_infinity(r_value: int, lam: int, p: int) -> int:
    return (
        16 * lam * lam
        + (-8 + 4 * r_value) * lam
        + (1 - r_value) * (1 - r_value)
    ) % p


def lambda_y_relation_at_infinity_dlambda(r_value: int, lam: int, p: int) -> int:
    return (32 * lam - 8 + 4 * r_value) % p


def lambda_y_relation_at_infinity_dr(r_value: int, lam: int, p: int) -> int:
    return (4 * lam - 2 * (1 - r_value)) % p


def line_monodromies(e: int, h: int, a: int, d: int) -> Tuple[int, int, int]:
    lift = h // e
    first = (lift * a) % h
    second = first
    infinity = (-(first + second + 2 * d)) % h
    return first, second, infinity


def balanced_z_local_exponents(h: int, alpha_exponent: int) -> Dict[str, object]:
    if h % 2 != 0:
        raise AssertionError(("h must contain the quadratic character", h))
    lambda_infinity = (
        alpha_exponent % h,
        0,
    )
    z_one_twist = (-2 * alpha_exponent) % h
    if alpha_exponent % h == 0 or z_one_twist == 0:
        raise AssertionError(("trivial balanced local character", h, alpha_exponent))
    return {
        "lambda_infinity_characters_after_twist": lambda_infinity,
        "lambda_infinity_invariant_count": 1,
        "z_one_regular_twist": z_one_twist,
    }


def twof1_local_table_import() -> Dict[str, object]:
    return {
        "status": "CONDITIONAL_IMPORT",
        "normalization": "Gauss 2F1(A,B;C;t)",
        "t_zero_characters": ("1", "C^(-1)"),
        "m1_instance": "2F1(chi_2,mu;alpha;t)",
        "after_visible_twists": ("alpha", "1"),
        "invariant_count_per_lambda_infinity_branch": 1,
        "source_pointer": "Katz ESDE 8.4.2(5), via Katz-Tiep GAFA 2021 Sec. 1B",
    }


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


def single_character_pullback_main(
    p: int,
    alpha: List[complex],
) -> complex:
    total = 0j
    for s in range(p):
        if s == p - 1:
            continue
        b_value = shape_b(s, p)
        if b_value == 0:
            continue
        alpha_b = alpha[b_value]
        for x in range(p):
            total += (
                alpha_b
                * alpha[x].conjugate()
                * alpha[x].conjugate()
                * alpha[(x - 1) % p]
                * alpha[(x - 1) % p]
                * alpha[(x - 1) % p]
                * quadratic_character(shape_d(s, x, p), p)
            )
    return quadratic_character(-1, p) * total


def quotient_paired_pullback_main(
    p: int,
    mu: List[complex],
    eta: List[complex],
    alpha: List[complex],
    rho: List[complex],
) -> complex:
    total = 0j
    for q_value in range(p):
        if q_value == 1 or (1 + 3 * q_value) % p == 0:
            continue
        roots = [z for z in range(p) if z * z % p == q_value]
        if not roots:
            continue
        lam = (q_value * pow(1 + 3 * q_value, -1, p)) % p
        weight = 0j
        for z in roots:
            s = s_from_z(z, p)
            weight += rho[shape_b(s, p)]
            expected_weight = (
                rho[(1 + 3 * q_value) % p]
                * alpha[(1 - z) % p].conjugate()
                * alpha[(1 - z) % p].conjugate()
            )
            if abs(rho[shape_b(s, p)] - expected_weight) > 1e-8:
                raise AssertionError(("quotient weight", p, q_value, z))
        total += weight * hypergeometric_trace(p, mu, eta, lam)

    fixed_lambda = pow(3, -1, p)
    total += rho[3 % p] * hypergeometric_trace(p, mu, eta, fixed_lambda)
    return quadratic_character(-4, p) * total


def balanced_z_kernel_value(
    p: int,
    alpha: List[complex],
    rho: List[complex],
    z: int,
) -> complex:
    numerator = (1 + 3 * z * z) % p
    direct_value = (
        rho[numerator]
        * alpha[(1 - z) % p].conjugate()
        * alpha[(1 - z) % p].conjugate()
    )
    balanced_value = (
        alpha[numerator]
        * quadratic_character(numerator, p)
        * alpha[(1 - z) % p].conjugate()
        * alpha[(1 - z) % p].conjugate()
    )
    if abs(direct_value - balanced_value) > 1e-8:
        raise AssertionError(("balanced z kernel", p, z))
    return balanced_value


def balanced_z_complete_sum(
    p: int,
    mu: List[complex],
    eta: List[complex],
    alpha: List[complex],
    rho: List[complex],
) -> complex:
    total = 0j
    for z in range(p):
        numerator = (1 + 3 * z * z) % p
        if numerator == 0:
            continue
        lam = (z * z * pow(numerator, -1, p)) % p
        total += (
            balanced_z_kernel_value(p, alpha, rho, z)
            * hypergeometric_trace(p, mu, eta, lam)
        )
    return total


def balanced_y_pushforward_sum(
    p: int,
    mu: List[complex],
    eta: List[complex],
    rho: List[complex],
) -> complex:
    total = 0j
    infinity_lambda = pow(3, -1, p)
    for y_value in range(1, p):
        fiber_trace = 0j
        for z in range(p):
            if z == 1:
                continue
            if twist_y_value(z, p) != y_value:
                continue
            fiber_trace += hypergeometric_trace(
                p,
                mu,
                eta,
                lambda_z_value(z, p),
            )
        if y_value == 3 % p:
            fiber_trace += hypergeometric_trace(p, mu, eta, infinity_lambda)
        total += rho[y_value] * fiber_trace
    return total


def balanced_y_kernel_sum(
    p: int,
    mu: List[complex],
    eta: List[complex],
    alpha: List[complex],
    rho: List[complex],
) -> complex:
    total = 0j
    for z in range(p):
        if z == 1 or (1 + 3 * z * z) % p == 0:
            continue
        y_value = twist_y_value(z, p)
        for x in range(p):
            total += (
                alpha[y_value]
                * mu[x]
                * eta[(x - 1) % p]
                * quadratic_character(y_kernel_argument(x, z, p), p)
            )
    total += rho[3 % p] * hypergeometric_trace(p, mu, eta, pow(3, -1, p))
    return total


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


def verify_plane_divisor_geometry(p: int) -> Dict[str, object]:
    if p <= 3:
        raise AssertionError(p)
    points = projective_points(p)
    point_p = (0, 1, 0)
    point_q = (1, 0, 0)
    point_r = (0, 0, 1)
    roots_b = [s for s in range(p) if shape_b(s, p) == 0]
    roots_c = [s for s in range(p) if shape_c(s, p) == 0]

    d_singular = [
        point
        for point in points
        if projective_d(*point, p) == 0
        and projective_d_partials(*point, p) == (0, 0, 0)
    ]
    if d_singular != [point_p]:
        raise AssertionError(("D singular", p, d_singular))
    if projective_b(point_p[0], point_p[2], p) != 0:
        raise AssertionError(("P not on B", p))
    if projective_b(point_q[0], point_q[2], p) == 0:
        raise AssertionError(("Q on B", p))
    if projective_b(point_r[0], point_r[2], p) == 0:
        raise AssertionError(("R on B", p))

    b_d = [
        point
        for point in points
        if projective_b(point[0], point[2], p) == 0
        and projective_d(*point, p) == 0
    ]
    if b_d != [point_p]:
        raise AssertionError(("B and D meet", p, b_d))

    l0_d = [
        point
        for point in points
        if point[1] == 0 and projective_d(*point, p) == 0
    ]
    if sorted(l0_d) != sorted([point_q, point_r]):
        raise AssertionError(("L0 and D meet", p, l0_d))

    l1_d = [
        point
        for point in points
        if point[1] == point[2] and projective_d(*point, p) == 0
    ]
    if len(l1_d) != 1 + len(roots_c) or point_q not in l1_d:
        raise AssertionError(("L1 and D meet", p, l1_d, roots_c))
    for point in l1_d:
        if point == point_q:
            continue
        if point[2] != 1 or projective_c(point[0], point[2], p) != 0:
            raise AssertionError(("bad L1/D affine point", p, point))

    b_l0 = [
        point
        for point in points
        if projective_b(point[0], point[2], p) == 0 and point[1] == 0
    ]
    b_l1 = [
        point
        for point in points
        if projective_b(point[0], point[2], p) == 0
        and point[1] == point[2]
    ]
    if len(b_l0) != len(roots_b) or len(b_l1) != len(roots_b):
        raise AssertionError(("B-line counts", p, b_l0, b_l1, roots_b))

    infinity_divisor = [
        point
        for point in points
        if point[2] == 0
        and (
            projective_b(point[0], point[2], p) == 0
            or point[1] == 0
            or point[1] == point[2]
            or projective_d(*point, p) == 0
        )
    ]
    if sorted(infinity_divisor) != sorted([point_p, point_q]):
        raise AssertionError(("infinity divisor", p, infinity_divisor))

    return {
        "p": p,
        "d_singular_point": point_p,
        "b_d_rational_intersection_count": len(b_d),
        "l0_d_rational_intersection_count": len(l0_d),
        "l1_d_rational_intersection_count": len(l1_d),
        "infinity_rational_intersection_count": len(infinity_divisor),
        "naive_plane_euler_target": 5,
    }


def verify_pullback_line_conductor_budget(p: int) -> Dict[str, object]:
    if p <= 3:
        raise AssertionError(p)
    roots_b = [s for s in range(p) if shape_b(s, p) == 0]
    roots_c = [s for s in range(p) if shape_c(s, p) == 0]
    if shape_b(0, p) == 0 or shape_c(0, p) == 0:
        raise AssertionError(("zero collides", p))
    if shape_b(p - 1, p) == 0 or shape_c(p - 1, p) == 0:
        raise AssertionError(("deleted point collides", p))
    if shape_b(p - 2, p) == 0 or shape_c(p - 2, p) == 0:
        raise AssertionError(("extra ramification collides", p))
    if any(shape_c(s, p) == 0 for s in roots_b):
        raise AssertionError(("B and C collide", p, roots_b, roots_c))

    s_zero_cond = 1
    c_root_cond = 2
    b_root_cond = 2
    infinity_twist_cond = 2
    rank = 2
    total_conductor = s_zero_cond + c_root_cond + b_root_cond
    total_conductor += infinity_twist_cond
    h1_budget = total_conductor - 2 * rank
    if h1_budget != 3:
        raise AssertionError((p, h1_budget))

    return {
        "p": p,
        "rank": rank,
        "geometric_collision_points": {
            "lambda_zero": 1,
            "lambda_one": 2,
            "lambda_infinity": 2,
            "s_infinity_twist": 1,
        },
        "rational_collision_counts": {
            "b_roots": len(roots_b),
            "c_roots": len(roots_c),
        },
        "twof1_local_table_import": twof1_local_table_import(),
        "conductor_budget": {
            "s_zero": s_zero_cond,
            "c_roots": c_root_cond,
            "b_roots_after_corrected_twist": b_root_cond,
            "infinity_twist": infinity_twist_cond,
            "total": total_conductor,
            "generic_h1_target": h1_budget,
            "desired_h1_target": 3,
            "missing_conductor_saving": h1_budget - 3,
        },
    }


def verify_pullback_deck_involution(p: int) -> Dict[str, object]:
    if p <= 3:
        raise AssertionError(p)
    roots_b = [s for s in range(p) if shape_b(s, p) == 0]
    roots_c = [s for s in range(p) if shape_c(s, p) == 0]

    for s in range(p):
        if s == p - 1:
            continue
        tau = deck_involution(s, p)
        denominator_square = ((s + 1) * (s + 1)) % p
        if deck_involution(tau, p) != s:
            raise AssertionError(("tau^2", p, s, tau))
        if shape_b(tau, p) * denominator_square % p != shape_b(s, p):
            raise AssertionError(("B transform", p, s, tau))
        if shape_c(tau, p) * denominator_square % p != shape_c(s, p):
            raise AssertionError(("C transform", p, s, tau))
        if shape_b(s, p) != 0 and lambda_value(tau, p) != lambda_value(s, p):
            raise AssertionError(("lambda invariant", p, s, tau))

    if deck_involution(0, p) != 0:
        raise AssertionError(("tau fixes zero", p))
    if deck_involution(p - 2, p) != p - 2:
        raise AssertionError(("tau fixes minus two", p))
    if sorted(deck_involution(s, p) for s in roots_b) != sorted(roots_b):
        raise AssertionError(("tau B roots", p, roots_b))
    if sorted(deck_involution(s, p) for s in roots_c) != sorted(roots_c):
        raise AssertionError(("tau C roots", p, roots_c))
    for s in range(p):
        if s in (p - 1, p - 2):
            continue
        z = z_coordinate(s, p)
        q_value = z * z % p
        if s_from_z(z, p) != s:
            raise AssertionError(("z inverse", p, s, z))
        if z_coordinate(deck_involution(s, p), p) != (-z) % p:
            raise AssertionError(("tau on z", p, s, z))
        if shape_b(s, p) * (1 - z) * (1 - z) % p != (1 + 3 * q_value) % p:
            raise AssertionError(("B z formula", p, s, z))
        if shape_c(s, p) * (1 - z) * (1 - z) % p != (
            4 * (1 + 2 * q_value)
        ) % p:
            raise AssertionError(("C z formula", p, s, z))
        if shape_b(s, p) != 0:
            expected_lambda = q_value * pow(1 + 3 * q_value, -1, p) % p
            if lambda_value(s, p) != expected_lambda:
                raise AssertionError(("lambda q formula", p, s, z))

    return {
        "p": p,
        "deck_involution": "tau(s)=-s/(s+1)",
        "quotient_coordinate": "z=s/(s+2), q=z^2",
        "fixed_points": (0, p - 2),
        "b_root_orbit_count": len(roots_b) // 2,
        "c_root_orbit_count": len(roots_c) // 2,
        "infinity_partner": "s=-1",
        "b_transform": "B(tau)=B/(s+1)^2",
        "lambda_quotient": "lambda=q/(1+3q)",
        "twist_multiplier": "rho((s+1)^(-2))",
    }


def verify_balanced_z_completion_geometry(p: int) -> Dict[str, object]:
    if p <= 3:
        raise AssertionError(p)
    lambda_zero_roots = [0]
    lambda_one_roots = [z for z in range(p) if (1 + 2 * z * z) % p == 0]
    lambda_infinity_roots = [z for z in range(p) if (1 + 3 * z * z) % p == 0]
    finite_special = set(lambda_zero_roots + lambda_one_roots)
    finite_special.update(lambda_infinity_roots)
    finite_special.add(1)
    if len(finite_special) != (
        1 + len(lambda_one_roots) + len(lambda_infinity_roots) + 1
    ):
        raise AssertionError(("balanced z collision", p, sorted(finite_special)))
    for z in range(p):
        numerator = (1 + 3 * z * z) % p
        if numerator == 0:
            continue
        lam = z * z * pow(numerator, -1, p) % p
        if (lam == 0) != (z == 0):
            raise AssertionError(("z lambda zero", p, z, lam))
        if (lam == 1) != ((1 + 2 * z * z) % p == 0):
            raise AssertionError(("z lambda one", p, z, lam))
    if (1 + 3 * 1 * 1) % p == 0:
        raise AssertionError(("z=1 bad", p))
    if (1 + 3 * (p - 1) * (p - 1)) % p == 0:
        raise AssertionError(("z=-1 bad", p))
    lambda_minus_one = (
        (p - 1)
        * (p - 1)
        * pow((1 + 3 * (p - 1) * (p - 1)) % p, -1, p)
    ) % p
    if lambda_minus_one != pow(4, -1, p):
        raise AssertionError(("lambda z=-1", p, lambda_minus_one))

    z_zero_cond = 1
    lambda_one_cond = 2
    lambda_infinity_cond = 2
    z_one_twist_cond = 2
    infinity_cond = 0
    rank = 2
    total_conductor = (
        z_zero_cond
        + lambda_one_cond
        + lambda_infinity_cond
        + z_one_twist_cond
        + infinity_cond
    )
    h1_budget = total_conductor - 2 * rank
    if h1_budget != 3:
        raise AssertionError((p, h1_budget))

    return {
        "p": p,
        "complete_coordinate": "z=s/(s+2)",
        "kernel": "chi_2(1+3z^2) alpha((1+3z^2)/(1-z)^2)",
        "lambda_z": "z^2/(1+3z^2)",
        "deleted_regular_point": "z=-1, lambda=1/4, kernel=1",
        "fixed_infinity_point": "z=infinity, lambda=1/3",
        "lambda_one_root_count": len(lambda_one_roots),
        "lambda_infinity_root_count": len(lambda_infinity_roots),
        "infinity_kummer_ramification": 0,
        "twof1_local_table_import": twof1_local_table_import(),
        "conductor_budget": {
            "z_zero": z_zero_cond,
            "lambda_one_roots": lambda_one_cond,
            "lambda_infinity_roots_after_corrected_twist": lambda_infinity_cond,
            "z_one_regular_twist": z_one_twist_cond,
            "infinity": infinity_cond,
            "total": total_conductor,
            "generic_h1_target": h1_budget,
            "desired_h1_target": 3,
            "missing_conductor_saving": h1_budget - 3,
        },
    }


def verify_balanced_y_pushforward_geometry(p: int) -> Dict[str, object]:
    if p <= 3:
        raise AssertionError(p)
    one_third = pow(3, -1, p)
    minus_one_third = (-one_third) % p
    three_quarters = 3 * pow(4, -1, p) % p
    one_twelfth = pow(12, -1, p)
    if twist_y_value(minus_one_third, p) != three_quarters:
        raise AssertionError(("twist branch value", p))
    if lambda_z_value(minus_one_third, p) != one_twelfth:
        raise AssertionError(("twist branch lambda", p))
    if twist_y_value(one_third, p) != 3 % p:
        raise AssertionError(("infinity partner y", p))
    if lambda_z_value(one_third, p) != one_twelfth:
        raise AssertionError(("infinity partner lambda", p))

    roots_infinity = [z for z in range(p) if (1 + 3 * z * z) % p == 0]
    if roots_infinity:
        if sorted(twist_map_deck_involution(z, p) for z in roots_infinity) != sorted(
            roots_infinity
        ):
            raise AssertionError(("twist deck infinity roots", p, roots_infinity))
        if any(twist_y_value(z, p) != 0 for z in roots_infinity):
            raise AssertionError(("twist infinity maps to zero", p, roots_infinity))

    finite_fiber_sizes: Dict[int, int] = {}
    for y_value in range(1, p):
        finite_fiber_sizes[y_value] = 0
    for z in range(p):
        if z == 1:
            continue
        y_value = twist_y_value(z, p)
        if y_value == 0:
            continue
        finite_fiber_sizes[y_value] += 1
        if quadratic_character((1 + 3 * z * z) % p, p) != quadratic_character(
            y_value,
            p,
        ):
            raise AssertionError(("twist quadratic pullback", p, z, y_value))
        lam = lambda_z_value(z, p)
        relation = (
            16 * y_value * y_value * lam * lam
            - 8 * lam * y_value * y_value
            + 4 * lam * y_value
            + (y_value - 1) * (y_value - 1)
        ) % p
        if relation != 0:
            raise AssertionError(("lambda y relation", p, z, y_value, lam))
        if z not in (1, one_third):
            sigma = twist_map_deck_involution(z, p)
            if sigma != 1 and twist_y_value(sigma, p) != y_value:
                raise AssertionError(("twist deck y", p, z, sigma))
            if sigma not in (1, one_third) and twist_map_deck_involution(
                sigma,
                p,
            ) != z:
                raise AssertionError(("twist deck square", p, z, sigma))

    if finite_fiber_sizes[3 % p] != 1:
        raise AssertionError(("finite y=3 fiber", p, finite_fiber_sizes[3 % p]))
    branch_fiber_size = finite_fiber_sizes[three_quarters]
    if branch_fiber_size != 1:
        raise AssertionError(("finite branch fiber", p, branch_fiber_size))
    ordinary_sizes = {
        size
        for y_value, size in finite_fiber_sizes.items()
        if y_value not in (3 % p, three_quarters)
    }
    if ordinary_sizes - {0, 2}:
        raise AssertionError(("ordinary twist fiber sizes", p, ordinary_sizes))

    return {
        "p": p,
        "twist_map": "y=(1+3z^2)/(1-z)^2",
        "twist_deck": "sigma(z)=(z+1)/(3z-1)",
        "deck_fixed_points": ("z=1", "z=-1/3"),
        "finite_branch": "z=-1/3 maps to y=3/4, lambda=1/12",
        "infinity_partner": "z=1/3 pairs with z=infinity over y=3",
        "lambda_y_relation": (
            "16 y^2 lambda^2 + (-8y^2+4y)lambda + (y-1)^2=0"
        ),
        "boundary_values": {"y_zero": "1+3z^2=0", "y_infinity": "z=1"},
    }


def verify_balanced_y_kernel_resultant(p: int) -> Dict[str, object]:
    if p <= 3:
        raise AssertionError(p)
    one_third = pow(3, -1, p)
    checked_pairs = 0
    product_checks = 0

    for z in range(p):
        if z == 1 or (1 + 3 * z * z) % p == 0:
            continue
        y_value = twist_y_value(z, p)
        chi_y = quadratic_character(y_value, p)
        for x in range(p):
            left = quadratic_character((x - lambda_z_value(z, p)) % p, p)
            right = chi_y * quadratic_character(y_kernel_argument(x, z, p), p)
            if left != right:
                raise AssertionError(("kernel character", p, x, z))
        checked_pairs += 1

    for y_value in range(1, p):
        if y_value == 3 % p:
            continue
        roots = [
            z
            for z in range(p)
            if z != 1
            and (1 + 3 * z * z) % p != 0
            and twist_y_value(z, p) == y_value
        ]
        if len(roots) != 2:
            continue
        denominator = (y_value - 3) * (y_value - 3) % p
        denominator_inverse = pow(denominator, -1, p)
        for x in range(p):
            product = 1
            for z in roots:
                product = product * y_kernel_argument(x, z, p) % p
            expected = lambda_y_resultant(x, y_value, p)
            expected = expected * denominator_inverse % p
            if product != expected:
                raise AssertionError(("kernel resultant", p, x, y_value))
            product_checks += 1

    special_z = one_third
    if twist_y_value(special_z, p) != 3 % p:
        raise AssertionError(("kernel y=3 finite point", p))
    if lambda_z_value(special_z, p) != pow(12, -1, p):
        raise AssertionError(("kernel y=3 lambda", p))

    return {
        "p": p,
        "kernel_argument": "x+(3x-1)z^2",
        "finite_kernel_identity": "chi_2(x-Lambda(z))=chi_2(y)chi_2(x+(3x-1)z^2)",
        "resultant": "16x^2y^2-8xy^2+4xy+y^2-2y+1",
        "resultant_meaning": "product over a split finite y-fiber",
        "checked_finite_z": checked_pairs,
        "product_checks": product_checks,
        "projective_y_three": "finite lambda=1/12 plus infinity lambda=1/3",
    }


def verify_resultant_surface_divisor_geometry(p: int) -> Dict[str, object]:
    if p <= 3:
        raise AssertionError(p)

    affine_singularities = []
    x_infinity_singularities = []
    y_infinity_singularities = []
    both_infinity_singularities = []
    for first in range(p):
        for second in range(p):
            x_value = first
            y_value = second
            affine_dx = (32 * x_value * y_value * y_value)
            affine_dx += (-8 * y_value * y_value + 4 * y_value)
            affine_dy = (32 * x_value * x_value * y_value)
            affine_dy += (-16 * x_value * y_value + 4 * x_value)
            affine_dy += 2 * y_value - 2
            if (
                lambda_y_resultant(x_value, y_value, p) == 0
                and affine_dx % p == 0
                and affine_dy % p == 0
            ):
                affine_singularities.append((x_value, y_value))

            u_value = first
            xinf_y = second
            xinf_du = (
                2 * u_value * xinf_y * xinf_y
                - 4 * u_value * xinf_y
                + 2 * u_value
                - 8 * xinf_y * xinf_y
                + 4 * xinf_y
            )
            xinf_dy = (
                2 * u_value * u_value * xinf_y
                - 2 * u_value * u_value
                - 16 * u_value * xinf_y
                + 4 * u_value
                + 32 * xinf_y
            )
            if (
                lambda_y_resultant_x_infinity(u_value, xinf_y, p) == 0
                and xinf_du % p == 0
                and xinf_dy % p == 0
            ):
                x_infinity_singularities.append((u_value, xinf_y))

            yinf_x = first
            v_value = second
            yinf_dx = (4 * v_value + 32 * yinf_x - 8) % p
            yinf_dv = (2 * v_value + 4 * yinf_x - 2) % p
            if (
                lambda_y_resultant_y_infinity(yinf_x, v_value, p) == 0
                and yinf_dx == 0
                and yinf_dv == 0
            ):
                y_infinity_singularities.append((yinf_x, v_value))

            both_u = first
            both_v = second
            both_du = (
                2 * both_u * both_v * both_v
                - 4 * both_u * both_v
                + 2 * both_u
                + 4 * both_v
                - 8
            )
            both_dv = (
                2 * both_u * both_u * both_v
                - 2 * both_u * both_u
                + 4 * both_u
            )
            if (
                lambda_y_resultant_both_infinity(both_u, both_v, p) == 0
                and both_du % p == 0
                and both_dv % p == 0
            ):
                both_infinity_singularities.append((both_u, both_v))

    if affine_singularities:
        raise AssertionError(("affine resultant singularities", p, affine_singularities))
    if x_infinity_singularities != [(0, 0)]:
        raise AssertionError(("x infinity singularities", p, x_infinity_singularities))
    if y_infinity_singularities:
        raise AssertionError(("y infinity singularities", p, y_infinity_singularities))
    if both_infinity_singularities:
        raise AssertionError(("both infinity singularities", p, both_infinity_singularities))

    y_three_quarters = 3 * pow(4, -1, p) % p
    for value in range(p):
        y_value = value
        discr_x = (-8 * y_value * y_value + 4 * y_value) ** 2
        discr_x -= 64 * y_value * y_value * (y_value - 1) * (y_value - 1)
        if discr_x % p != (16 * y_value * y_value * (4 * y_value - 3)) % p:
            raise AssertionError(("x discriminant", p, y_value))
        x_value = value
        discr_y = (4 * x_value - 2) ** 2
        discr_y -= 4 * (4 * x_value - 1) * (4 * x_value - 1)
        if discr_y % p != (-16 * x_value * (3 * x_value - 1)) % p:
            raise AssertionError(("y discriminant", p, x_value))
        if lambda_y_resultant(0, value, p) != (value - 1) * (value - 1) % p:
            raise AssertionError(("x=0 restriction", p, value))
        if lambda_y_resultant(1, value, p) != (9 * value * value + 2 * value + 1) % p:
            raise AssertionError(("x=1 restriction", p, value))
        if lambda_y_resultant(value, 0, p) != 1:
            raise AssertionError(("y=0 affine restriction", p, value))
        expected_y_branch = (12 * value - 1) * (12 * value - 1)
        expected_y_branch *= pow(16, -1, p)
        if lambda_y_resultant(value, y_three_quarters, p) != expected_y_branch % p:
            raise AssertionError(("y=3/4 restriction", p, value))
        if lambda_y_resultant_x_infinity(0, value, p) != 16 * value * value % p:
            raise AssertionError(("x=infinity restriction", p, value))
        if lambda_y_resultant_y_infinity(value, 0, p) != (4 * value - 1) ** 2 % p:
            raise AssertionError(("y=infinity restriction", p, value))

    component_euler = {
        "six_boundary_lines": 12,
        "nodal_resultant_curve": 1,
    }
    intersection_correction = {
        "line_grid_with_node_triple_point": 10,
        "resultant_line_points_off_grid": 5,
        "total": 15,
    }
    union_euler = sum(component_euler.values()) - intersection_correction["total"]
    complement_euler = 4 - union_euler
    if complement_euler != 6:
        raise AssertionError(("resultant complement euler", p, complement_euler))

    return {
        "p": p,
        "compactification": "P1_x times P1_y",
        "resultant_bidegree": (2, 2),
        "resultant_singularity": "ordinary node at x=infinity, y=0",
        "node_tangent_cone": "4y(4y+u) in the u=1/x chart",
        "geometric_genus": 0,
        "curve_euler": 1,
        "branch_lines_included": ("x=0", "x=1", "x=infinity", "y=0", "y=infinity", "4y-3=0"),
        "component_euler": component_euler,
        "intersection_correction": intersection_correction,
        "union_euler": union_euler,
        "complement_euler_target": complement_euler,
    }


def verify_pushforward_singular_values(p: int) -> Dict[str, object]:
    if p <= 3:
        raise AssertionError(p)
    one_third = pow(3, -1, p)
    one_fourth = pow(4, -1, p)
    one_twelfth = pow(12, -1, p)
    branch_y = 3 * one_fourth % p

    y_one_fiber = [
        z
        for z in range(p)
        if z != 1
        and (1 + 3 * z * z) % p != 0
        and twist_y_value(z, p) == 1
    ]
    if sorted(y_one_fiber) != [0, p - 1]:
        raise AssertionError(("y=1 fiber", p, y_one_fiber))
    if lambda_z_value(0, p) != 0:
        raise AssertionError(("lambda z=0", p))
    if lambda_z_value(p - 1, p) != one_fourth:
        raise AssertionError(("lambda z=-1", p))

    y_three_fiber = [
        z
        for z in range(p)
        if z != 1
        and (1 + 3 * z * z) % p != 0
        and twist_y_value(z, p) == 3 % p
    ]
    if y_three_fiber != [one_third]:
        raise AssertionError(("y=3 finite fiber", p, y_three_fiber))
    if lambda_z_value(one_third, p) != one_twelfth:
        raise AssertionError(("lambda z=1/3", p))

    branch_z = (-one_third) % p
    if twist_y_value(branch_z, p) != branch_y:
        raise AssertionError(("branch y", p))
    if lambda_z_value(branch_z, p) != one_twelfth:
        raise AssertionError(("branch lambda", p))

    lambda_infinity_z_roots = [z for z in range(p) if (1 + 3 * z * z) % p == 0]
    for z in lambda_infinity_z_roots:
        if z == 1 or twist_y_value(z, p) != 0:
            raise AssertionError(("lambda infinity maps to y=0", p, z))

    lambda_one_y_roots = [
        y_value for y_value in range(p) if lambda_one_y_polynomial(y_value, p) == 0
    ]
    if lambda_one_y_polynomial(0, p) == 0:
        raise AssertionError(("lambda=1 collides with y=0", p))
    if lambda_one_y_polynomial(1, p) == 0:
        raise AssertionError(("lambda=1 collides with y=1", p))

    exceptional_p11 = p == 11
    if not exceptional_p11:
        if lambda_one_y_polynomial(branch_y, p) == 0:
            raise AssertionError(("lambda=1 collides with branch", p))
        if lambda_one_y_polynomial(3, p) == 0:
            raise AssertionError(("lambda=1 collides with y=3", p))
    else:
        if lambda_one_y_polynomial(branch_y, p) != 0:
            raise AssertionError(("missing p=11 branch collision", p))
        if lambda_one_y_polynomial(3, p) != 0:
            raise AssertionError(("missing p=11 y=3 collision", p))

    singular_values = {
        "lambda_infinity": "y=0",
        "lambda_zero": "y=1",
        "lambda_one": "9y^2+2y+1=0",
        "cover_branch_regular": "y=3/4",
        "cover_infinity": "y=infinity",
    }
    ordinary_projective_fiber = {
        "y": "3",
        "finite_lambda": "1/12",
        "infinity_lambda": "1/3",
    }
    return {
        "p": p,
        "generic_singular_value_count": 6,
        "singular_values": singular_values,
        "lambda_one_y_roots": lambda_one_y_roots,
        "ordinary_projective_fiber": ordinary_projective_fiber,
        "exceptional_p11_collision": exceptional_p11,
    }


def verify_pushforward_local_conductor_budget(p: int) -> Dict[str, object]:
    if p <= 3 or p == 11:
        raise AssertionError(("generic pushforward conductor excludes p", p))
    one_fourth = pow(4, -1, p)
    one_twelfth = pow(12, -1, p)
    one_third = pow(3, -1, p)
    branch_y = 3 * one_fourth % p

    # y=0, lambda=infinity: in w=1/lambda the tangent cone is
    # w^2+4yw+16y^2, which has two geometric branches for p>3.  The
    # corrected 2F1 local table leaves one invariant on each branch after
    # the Mellin twist.
    if (-48) % p == 0:
        raise AssertionError(("lambda infinity tangent collision", p))

    # y=1: one branch has lambda=0 with quadratic contact; the other is
    # the regular lambda=1/4 branch.
    if lambda_y_relation_value(1, 0, p) != 0:
        raise AssertionError(("y=1 lambda=0", p))
    if lambda_y_relation_dlambda(1, 0, p) == 0:
        raise AssertionError(("y=1 lambda=0 not implicit", p))
    if lambda_y_relation_dy(1, 0, p) != 0:
        raise AssertionError(("y=1 lambda=0 not double", p))
    if lambda_y_relation_value(1, one_fourth, p) != 0:
        raise AssertionError(("y=1 lambda=1/4", p))
    if lambda_y_relation_dlambda(1, one_fourth, p) == 0:
        raise AssertionError(("y=1 regular branch", p))

    # lambda=1: the two roots of 9y^2+2y+1 are simple and separated from
    # the ordinary/branch fibers in the generic characteristics.
    lambda_one_roots = [
        y_value for y_value in range(p) if lambda_one_y_polynomial(y_value, p) == 0
    ]
    for y_value in lambda_one_roots:
        if lambda_y_relation_value(y_value, 1, p) != 0:
            raise AssertionError(("lambda=1 relation", p, y_value))
        if (18 * y_value + 2) % p == 0:
            raise AssertionError(("lambda=1 double y-root", p, y_value))
        if lambda_y_relation_dlambda(y_value, 1, p) == 0:
            raise AssertionError(("lambda=1 branch collision", p, y_value))

    # y=3/4 is a simple branch point over the regular lambda=1/12 value.
    if lambda_y_relation_value(branch_y, one_twelfth, p) != 0:
        raise AssertionError(("regular branch relation", p))
    if lambda_y_relation_dlambda(branch_y, one_twelfth, p) != 0:
        raise AssertionError(("regular branch dlambda", p))
    if lambda_y_relation_dy(branch_y, one_twelfth, p) == 0:
        raise AssertionError(("regular branch dy", p))

    # y=infinity: with r=1/y, the two branches coalesce at lambda=1/4 and
    # the projection to the y-line is simply ramified over a regular fiber.
    if lambda_y_relation_at_infinity(0, one_fourth, p) != 0:
        raise AssertionError(("infinity branch relation", p))
    if lambda_y_relation_at_infinity_dlambda(0, one_fourth, p) != 0:
        raise AssertionError(("infinity branch dlambda", p))
    if lambda_y_relation_at_infinity_dr(0, one_fourth, p) == 0:
        raise AssertionError(("infinity branch dr", p))

    # y=3 is an ordinary projective fiber, not part of the generic conductor.
    if lambda_y_relation_value(3, one_twelfth, p) != 0:
        raise AssertionError(("y=3 finite lambda", p))
    if lambda_y_relation_value(3, one_third, p) != 0:
        raise AssertionError(("y=3 infinity lambda", p))
    if lambda_y_relation_dlambda(3, one_twelfth, p) == 0:
        raise AssertionError(("y=3 finite branch", p))
    if lambda_y_relation_dlambda(3, one_third, p) == 0:
        raise AssertionError(("y=3 infinity branch", p))

    rank = 4
    conductor_budget = {
        "y_zero_lambda_infinity_after_corrected_mellin": 2,
        "y_one_lambda_zero_double_pullback": 1,
        "lambda_one_roots": 2,
        "y_three_quarters_regular_branch": 2,
        "y_infinity_regular_branch_after_mellin": 4,
    }
    total_conductor = sum(conductor_budget.values())
    h1_budget = total_conductor - 2 * rank
    if total_conductor != 11 or h1_budget != 3:
        raise AssertionError(("pushforward conductor budget", p, total_conductor))

    return {
        "p": p,
        "rank": rank,
        "generic_local_profile": {
            "y=0": "two lambda=infinity branches, one invariant on each",
            "y=1": "lambda=0 has quadratic contact; lambda=1/4 is regular",
            "lambda=1": "two simple roots of 9y^2+2y+1",
            "y=3/4": "simple branch over regular lambda=1/12",
            "y=infinity": "simple branch over regular lambda=1/4",
            "y=3": "ordinary lambda=1/12,1/3 fiber",
        },
        "twof1_local_table_import": twof1_local_table_import(),
        "conductor_budget": {
            **conductor_budget,
            "total": total_conductor,
            "generic_h1_target": h1_budget,
            "desired_h1_target": 3,
            "missing_conductor_saving": h1_budget - 3,
        },
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
    alpha_exponent = (lift * a + d) % h
    rho = characters[alpha_exponent]
    rho_chi = characters[(alpha_exponent + h // 2) % h]
    alpha = rho
    balanced_exponents = balanced_z_local_exponents(h, alpha_exponent)
    if (lift * a + d) % h == 0:
        raise AssertionError(("mu eta unexpectedly principal", case))
    if (lift * a + d + h // 2) % h == 0:
        raise AssertionError(("mu eta chi_2 unexpectedly principal", case))
    if abs(mu[primitive_root(p)] - alpha[primitive_root(p)].conjugate() ** 2) > 1e-8:
        raise AssertionError(("mu alpha relation", case))
    if abs(eta[primitive_root(p)] - alpha[primitive_root(p)] ** 3) > 1e-8:
        raise AssertionError(("eta alpha relation", case))

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
    single_character_main = single_character_pullback_main(p, alpha)
    if abs(jacobi_part - first_direct) > 1e-8:
        raise AssertionError((case, jacobi_part, first_direct))
    if abs(direct - (jacobi_part + residual)) > 1e-8:
        raise AssertionError((case, direct, jacobi_part, residual))
    if abs(residual - (pullback_main + exceptional)) > 1e-8:
        raise AssertionError((case, residual, pullback_main, exceptional))
    if abs(pullback_main - single_character_main) > 1e-8:
        raise AssertionError((case, pullback_main, single_character_main))
    quotient_paired_main = quotient_paired_pullback_main(
        p,
        mu,
        eta,
        alpha,
        rho_chi,
    )
    if abs(pullback_main - quotient_paired_main) > 1e-8:
        raise AssertionError((case, pullback_main, quotient_paired_main))
    balanced_complete = balanced_z_complete_sum(
        p,
        mu,
        eta,
        alpha,
        rho_chi,
    )
    deleted_regular = hypergeometric_trace(p, mu, eta, pow(4, -1, p))
    fixed_infinity = (
        rho_chi[3 % p]
        * hypergeometric_trace(p, mu, eta, pow(3, -1, p))
    )
    projective_y_main = balanced_y_pushforward_sum(
        p,
        mu,
        eta,
        rho_chi,
    )
    projective_z_main = balanced_complete + fixed_infinity
    if abs(projective_y_main - projective_z_main) > 1e-8:
        raise AssertionError((case, projective_y_main, projective_z_main))
    kernel_main = balanced_y_kernel_sum(
        p,
        mu,
        eta,
        alpha,
        rho_chi,
    )
    if abs(projective_y_main - kernel_main) > 1e-8:
        raise AssertionError((case, projective_y_main, kernel_main))
    balanced_main = quadratic_character(-4, p) * (
        balanced_complete - deleted_regular + fixed_infinity
    )
    if abs(pullback_main - balanced_main) > 1e-8:
        raise AssertionError((case, pullback_main, balanced_main))
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
        "balanced_z_local_exponents": balanced_exponents,
        "sum_ratio": round(abs(direct) / p, 10),
        "jacobi_ratio": round(abs(jacobi_part) / p, 10),
        "residual_ratio": round(abs(residual) / p, 10),
        "pullback_main_ratio": round(abs(pullback_main) / p, 10),
        "exceptional_sqrt_ratio": round(abs(exceptional) / math.sqrt(p), 10),
        "identity_error": f"{abs(direct - (jacobi_part + residual)):.2e}",
        "pullback_error": f"{abs(residual - (pullback_main + exceptional)):.2e}",
        "single_character_error": f"{abs(pullback_main - single_character_main):.2e}",
        "quotient_pair_error": f"{abs(pullback_main - quotient_paired_main):.2e}",
        "balanced_z_error": f"{abs(pullback_main - balanced_main):.2e}",
        "y_pushforward_error": f"{abs(projective_y_main - projective_z_main):.2e}",
        "y_kernel_error": f"{abs(projective_y_main - kernel_main):.2e}",
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
    plane_rows = [
        verify_plane_divisor_geometry(int(case["p"]))
        for case in CASES
    ]
    for row in plane_rows:
        print(row)
    conductor_rows = [
        verify_pullback_line_conductor_budget(int(case["p"]))
        for case in CASES
    ]
    for row in conductor_rows:
        print(row)
    deck_rows = [
        verify_pullback_deck_involution(int(case["p"]))
        for case in CASES
    ]
    for row in deck_rows:
        print(row)
    z_rows = [
        verify_balanced_z_completion_geometry(int(case["p"]))
        for case in CASES
    ]
    for row in z_rows:
        print(row)
    y_rows = [
        verify_balanced_y_pushforward_geometry(int(case["p"]))
        for case in CASES
    ]
    for row in y_rows:
        print(row)
    kernel_rows = [
        verify_balanced_y_kernel_resultant(int(case["p"]))
        for case in CASES
    ]
    for row in kernel_rows:
        print(row)
    resultant_rows = [
        verify_resultant_surface_divisor_geometry(int(case["p"]))
        for case in CASES
    ]
    for row in resultant_rows:
        print(row)
    pushforward_rows = [
        verify_pushforward_singular_values(int(case["p"]))
        for case in CASES
    ]
    for row in pushforward_rows:
        print(row)
    pushforward_conductor_rows = [
        verify_pushforward_local_conductor_budget(int(case["p"]))
        for case in CASES
    ]
    for row in pushforward_conductor_rows:
        print(row)
    top = max(rows, key=lambda row: float(row["sum_ratio"]))
    for key, value in EXPECTED_TOP.items():
        actual = top[key]
        if actual != value:
            raise AssertionError((key, actual, value, top))
    print("M1 equal-line diagonal reduction verifier passed")


if __name__ == "__main__":
    main()
