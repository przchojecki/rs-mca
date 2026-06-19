#!/usr/bin/env python3
"""Verify the M1 depth-two line-conic resonance reduction."""

from __future__ import annotations

import cmath
import math
from typing import Dict, Iterable, List, Tuple


EXHAUSTIVE_PRIMES = (17, 31)
MOMENT_PRIMES = (5, 7, 11, 17, 31)
FILTER_ORDERS = tuple(range(2, 41))
ADMISSIBLE_OPEN_AUDIT_PRIMES = (17, 31, 43)
ADMISSIBLE_TRANSFER_CONSTANTS = (1, 2, 4, 9)
RATIO_SURFACE_CASES = (
    (17, 8),
    (17, 16),
    (31, 6),
    (31, 10),
    (43, 6),
    (43, 14),
)
TARGETED_CASES = (
    (37, 2, 5),
    (37, 7, 11),
    (43, 3, 8),
    (43, 12, 5),
    (61, 5, 17),
    (61, 19, 7),
    (61, 30, 23),
    (73, 8, 32),
    (97, 49, 59),
    (109, 105, 19),
    (109, 105, 92),
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


def least_nonsquare(p: int) -> int:
    for value in range(2, p):
        if legendre(value, p) == -1:
            return value
    raise ValueError((p, "no nonsquare"))


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


def transformed_inner(p: int, y: int, nu: List[complex]) -> complex:
    total = 0j
    for v in range(p):
        total += nu[v] * legendre(q_y_v(y, v, p), p)
    return total


def jacobi_sum(p: int, alpha: List[complex], beta: List[complex]) -> complex:
    total = 0j
    for t in range(p):
        total += alpha[t] * beta[(1 - t) % p]
    return total


def hypergeometric_fiber_trace(
    p: int,
    parameter: int,
    nu: List[complex],
) -> complex:
    total = 0j
    for x in range(p):
        total += nu[x] * legendre((x - 1) * (x - parameter), p)
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


def verify_singular_fiber_values(p: int, table: List[List[complex]]) -> None:
    quadratic_exponent = (p - 1) // 2
    quadratic_character = table[quadratic_exponent]
    singular_values = {0, (-1) % p, 2 % p, 3 % p}
    for y in singular_values:
        if y == (-1) % p:
            for nu_exponent in range(1, p - 1):
                actual = transformed_inner(p, y, table[nu_exponent])
                assert_close((p, nu_exponent, "G(-1)"), actual, 0j)
        elif y == 2 % p:
            for nu_exponent in range(1, p - 1):
                nu = table[nu_exponent]
                expected = -legendre(-3, p) * nu[(-1) % p]
                actual = transformed_inner(p, y, nu)
                assert_close((p, nu_exponent, "G(2)"), actual, expected)
        elif y == 3 % p:
            minus_eight_over_three = (-8 * pow(3, -1, p)) % p
            for nu_exponent in range(1, p - 1):
                nu = table[nu_exponent]
                alpha = table[(nu_exponent + quadratic_exponent) % (p - 1)]
                expected = (
                    legendre(3, p)
                    * nu[minus_eight_over_three]
                    * jacobi_sum(p, alpha, quadratic_character)
                )
                actual = transformed_inner(p, y, nu)
                assert_close((p, nu_exponent, "G(3)"), actual, expected)
                if nu_exponent == quadratic_exponent:
                    if abs(actual) > 1 + TOLERANCE:
                        raise AssertionError((p, nu_exponent, "G(3)-quadratic"))
                elif abs(actual) > math.sqrt(p) + TOLERANCE:
                    raise AssertionError((p, nu_exponent, "G(3)-jacobi-bound"))
        else:
            for eta_exponent in range(1, p - 1):
                eta = table[eta_exponent]
                if eta[0] != 0j:
                    raise AssertionError((p, eta_exponent, "eta(0)"))


def square_root_mod(value: int, p: int) -> int:
    value %= p
    for candidate in range(p):
        if candidate * candidate % p == value:
            return candidate
    raise ValueError((p, value, "not a square"))


def verify_split_hypergeometric_pullback(
    p: int,
    table: List[List[complex]],
) -> int:
    checked = 0
    inverse_three = pow(3, -1, p)
    singular_values = {(-1) % p, 2 % p, 3 % p}
    for y in range(p):
        if y in singular_values:
            continue
        discriminant_root_square = (y - 2) * (y + 1)
        if legendre(discriminant_root_square, p) != 1:
            continue
        z = square_root_mod(discriminant_root_square, p)
        root_plus = (-(y + 1 + 2 * z) * inverse_three) % p
        root_minus = (-(y + 1 - 2 * z) * inverse_three) % p
        if root_plus == 0 or root_minus == 0 or root_plus == root_minus:
            raise AssertionError((p, y, z, root_plus, root_minus))
        parameter = root_minus * pow(root_plus, -1, p) % p
        if parameter in {0, 1}:
            raise AssertionError((p, y, z, parameter))
        for nu_exponent in range(1, p - 1):
            nu = table[nu_exponent]
            expected = (
                legendre(-3, p)
                * nu[root_plus]
                * hypergeometric_fiber_trace(p, parameter, nu)
            )
            actual = transformed_inner(p, y, nu)
            assert_close(
                (p, y, z, nu_exponent, "split_hypergeometric"),
                actual,
                expected,
            )
            checked += 1
    return checked


def verify_lambda_map_ledger(p: int) -> int:
    checked = 0
    for parameter in range(p):
        denominator = (3 * parameter * parameter + 10 * parameter + 3) % p
        numerator = (9 * parameter * parameter + 14 * parameter + 9) % p
        if denominator == 0:
            continue
        y = numerator * pow(denominator, -1, p) % p
        z = (
            6
            * (1 - parameter * parameter)
            * pow(denominator, -1, p)
        ) % p
        root_plus = (-8 * (1 + parameter) * pow(denominator, -1, p)) % p
        root_minus = (parameter * root_plus) % p
        if z * z % p != (y - 2) * (y + 1) % p:
            raise AssertionError((p, parameter, "double_cover", y, z))
        if q_y_v(y, root_plus, p) != 0 or q_y_v(y, root_minus, p) != 0:
            raise AssertionError((p, parameter, "root", y, root_plus, root_minus))
        if parameter not in {(-1) % p, 0} and root_plus == 0:
            raise AssertionError((p, parameter, "root_plus_zero"))
        if root_plus != 0:
            recovered = root_minus * pow(root_plus, -1, p) % p
            if recovered != parameter:
                raise AssertionError((p, parameter, recovered))

        expected_y_minus_two = (
            3
            * (parameter - 1)
            * (parameter - 1)
            * pow(denominator, -1, p)
        ) % p
        expected_y_plus_one = (
            12
            * (parameter + 1)
            * (parameter + 1)
            * pow(denominator, -1, p)
        ) % p
        expected_y_minus_three = (
            -16 * parameter * pow(denominator, -1, p)
        ) % p
        if (y - 2) % p != expected_y_minus_two:
            raise AssertionError((p, parameter, "y-2"))
        if (y + 1) % p != expected_y_plus_one:
            raise AssertionError((p, parameter, "y+1"))
        if (y - 3) % p != expected_y_minus_three:
            raise AssertionError((p, parameter, "y-3"))

        finite_singular = (
            parameter in {0, 1, (-1) % p}
            or denominator == 0
            or numerator == 0
        )
        y_singular = y in {0, (-1) % p, 2 % p, 3 % p}
        if y_singular and not finite_singular:
            raise AssertionError((p, parameter, "unexpected singular y", y))
        checked += 1

    # The two finite poles of y(lambda) are lambda=-3 and lambda=-1/3.
    if (3 * (-3) * (-3) + 10 * (-3) + 3) % p != 0:
        raise AssertionError((p, "lambda=-3 pole"))
    minus_inverse_three = (-pow(3, -1, p)) % p
    if (
        3 * minus_inverse_three * minus_inverse_three
        + 10 * minus_inverse_three
        + 3
    ) % p != 0:
        raise AssertionError((p, "lambda=-1/3 pole"))
    return checked


def lambda_denominator(parameter: int, p: int) -> int:
    return (3 * parameter * parameter + 10 * parameter + 3) % p


def lambda_outer_numerator(parameter: int, p: int) -> int:
    return (9 * parameter * parameter + 14 * parameter + 9) % p


def verify_lambda_twist_divisor(p: int) -> Tuple[int, int]:
    finite_standard = {0, 1 % p, (-1) % p, (-3) % p, (-pow(3, -1, p)) % p}
    outer_roots = {
        parameter
        for parameter in range(p)
        if lambda_outer_numerator(parameter, p) == 0
    }
    expected_outer_root_count = 1 + legendre(-2, p)
    if len(outer_roots) != expected_outer_root_count:
        raise AssertionError((p, outer_roots, expected_outer_root_count))
    if finite_standard & outer_roots:
        raise AssertionError((p, "outer collision", finite_standard & outer_roots))

    pole_roots = {
        parameter for parameter in range(p) if lambda_denominator(parameter, p) == 0
    }
    expected_poles = {(-3) % p, (-pow(3, -1, p)) % p}
    if pole_roots != expected_poles:
        raise AssertionError((p, pole_roots, expected_poles))

    for parameter in range(p):
        denominator = lambda_denominator(parameter, p)
        numerator = lambda_outer_numerator(parameter, p)
        root_numerator = (-8 * (1 + parameter)) % p
        in_support = (
            parameter in {0, 1 % p, (-1) % p}
            or parameter in pole_roots
            or parameter in outer_roots
        )
        if not in_support:
            if denominator == 0 or numerator == 0 or root_numerator == 0:
                raise AssertionError((p, parameter, "unexpected twist support"))
        if parameter == (-1) % p and root_numerator != 0:
            raise AssertionError((p, parameter, "missing r_plus zero"))
        if parameter in pole_roots and (numerator == 0 or root_numerator == 0):
            raise AssertionError((p, parameter, "pole collision"))

    # The derivative of y(lambda) vanishes only at lambda=+-1.
    for parameter in range(p):
        derivative_numerator = 48 * (parameter - 1) * (parameter + 1)
        if derivative_numerator % p == 0 and parameter not in {1 % p, (-1) % p}:
            raise AssertionError((p, parameter, "unexpected branch"))
    finite_support_count = len({0, 1 % p, (-1) % p} | pole_roots | outer_roots)
    # Infinity is the remaining support point: r_+(lambda) has a zero there.
    return finite_support_count, finite_support_count + 1


def lambda_pullback_sum(
    p: int,
    eta: List[complex],
    nu: List[complex],
) -> complex:
    total = 0j
    for parameter in range(p):
        denominator = lambda_denominator(parameter, p)
        if denominator == 0:
            continue
        y = lambda_outer_numerator(parameter, p) * pow(denominator, -1, p) % p
        root_plus = (-8 * (1 + parameter) * pow(denominator, -1, p)) % p
        total += (
            eta[(-y) % p]
            * legendre(-3, p)
            * nu[root_plus]
            * hypergeometric_fiber_trace(p, parameter, nu)
        )
    return total


def quadratic_twisted_core(
    p: int,
    eta: List[complex],
    nu: List[complex],
) -> complex:
    total = 0j
    for y in range(p):
        total += (
            legendre((y - 2) * (y + 1), p)
            * eta[(-y) % p]
            * transformed_inner(p, y, nu)
        )
    return total


def split_projected_core(
    p: int,
    eta: List[complex],
    nu: List[complex],
) -> complex:
    return (
        transformed_core(p, eta, nu)
        + quadratic_twisted_core(p, eta, nu)
        - eta[(-3) % p] * transformed_inner(p, 3 % p, nu)
    )


def nonsplit_projected_core(
    p: int,
    eta: List[complex],
    nu: List[complex],
) -> complex:
    return transformed_core(p, eta, nu) - quadratic_twisted_core(p, eta, nu)


def projection_singular_contributions(
    p: int,
    eta: List[complex],
    nu: List[complex],
) -> Tuple[complex, complex, complex, complex]:
    split_projection = 0j
    nonsplit_projection = 0j
    for y in {0, (-1) % p, 2 % p, 3 % p}:
        base = eta[(-y) % p] * transformed_inner(p, y, nu)
        discriminant_sign = legendre((y - 2) * (y + 1), p)
        split_projection += (1 + discriminant_sign) * base
        nonsplit_projection += (1 - discriminant_sign) * base
    split_projection -= eta[(-3) % p] * transformed_inner(p, 3 % p, nu)

    split_expected = (
        eta[(-2) % p] * transformed_inner(p, 2 % p, nu)
        + eta[(-3) % p] * transformed_inner(p, 3 % p, nu)
    )
    nonsplit_expected = eta[(-2) % p] * transformed_inner(p, 2 % p, nu)
    return (
        split_projection,
        nonsplit_projection,
        split_expected,
        nonsplit_expected,
    )


def twisted_discriminant_y(p: int, t: int, delta: int) -> int:
    denominator = (t * t - delta) % p
    if denominator == 0:
        raise AssertionError((p, t, delta, "twist_denominator"))
    numerator = (2 * t * t + delta) % p
    return numerator * pow(denominator, -1, p) % p


def verify_twisted_discriminant_map(p: int) -> Tuple[int, int]:
    delta = least_nonsquare(p)
    checked = 0
    nonsplit_values = set()
    for t in range(p):
        denominator = (t * t - delta) % p
        if denominator == 0:
            raise AssertionError((p, t, delta, "finite_twist_pole"))
        y = twisted_discriminant_y(p, t, delta)
        inverse_denominator = pow(denominator, -1, p)

        expected_y_minus_two = 3 * delta * inverse_denominator % p
        expected_y_plus_one = 3 * t * t * inverse_denominator % p
        expected_y_minus_three = (4 * delta - t * t) * inverse_denominator % p
        if (y - 2) % p != expected_y_minus_two:
            raise AssertionError((p, t, delta, "twist_y_minus_two"))
        if (y + 1) % p != expected_y_plus_one:
            raise AssertionError((p, t, delta, "twist_y_plus_one"))
        if (y - 3) % p != expected_y_minus_three:
            raise AssertionError((p, t, delta, "twist_y_minus_three"))

        discriminant = (y - 2) * (y + 1) % p
        expected_discriminant = (
            9
            * delta
            * t
            * t
            * pow(denominator * denominator % p, -1, p)
        ) % p
        if discriminant != expected_discriminant:
            raise AssertionError((p, t, delta, "twist_discriminant"))
        if t == 0:
            if y != (-1) % p:
                raise AssertionError((p, t, y, "twist_zero_branch"))
        elif legendre(discriminant, p) != -1:
            raise AssertionError((p, t, y, discriminant, "not_nonsplit"))
        else:
            nonsplit_values.add(y)
        checked += 1

    expected_nonsplit_values = {
        y
        for y in range(p)
        if legendre((y - 2) * (y + 1), p) == -1
    }
    if nonsplit_values != expected_nonsplit_values:
        raise AssertionError(
            (p, delta, "nonsplit_value_set", nonsplit_values, expected_nonsplit_values)
        )
    for y in expected_nonsplit_values:
        roots = [t for t in range(p) if twisted_discriminant_y(p, t, delta) == y]
        if len(roots) != 2 or (roots[0] + roots[1]) % p != 0:
            raise AssertionError((p, delta, y, roots, "nonsplit_preimages"))

    # These are geometric support pairs but have no F_p-points for nonsquare delta.
    for value, label in ((delta, "twist_infinity_poles"), (4 * delta, "twist_y3")):
        if any(t * t % p == value % p for t in range(p)):
            raise AssertionError((p, delta, value, label))
    return checked, len(nonsplit_values)


def twisted_discriminant_nonsplit_sum(
    p: int,
    eta: List[complex],
    nu: List[complex],
) -> complex:
    delta = least_nonsquare(p)
    total = eta[(-2) % p] * transformed_inner(p, 2 % p, nu)
    for t in range(p):
        y = twisted_discriminant_y(p, t, delta)
        total += eta[(-y) % p] * transformed_inner(p, y, nu)
    return total


def twisted_line_kernel_trace(
    p: int,
    t: int,
    delta: int,
    nu: List[complex],
) -> complex:
    total = 0j
    for x in range(p):
        total += nu[(x - t) % p] * legendre(x * x - 4 * delta, p)
    return total


def verify_twisted_line_fiber_trace(
    p: int,
    table: List[List[complex]],
) -> int:
    delta = least_nonsquare(p)
    checked = 0
    for t in range(p):
        denominator = (t * t - delta) % p
        if denominator == 0:
            raise AssertionError((p, t, delta, "twisted_line_denominator"))
        y = twisted_discriminant_y(p, t, delta)
        for nu_exponent in range(1, p - 1):
            nu = table[nu_exponent]
            expected = (
                legendre(-3, p)
                * nu[t * pow(denominator, -1, p) % p]
                * twisted_line_kernel_trace(p, t, delta, nu)
            )
            actual = transformed_inner(p, y, nu)
            assert_close(
                (p, t, nu_exponent, "twisted_line_fiber_trace"),
                actual,
                expected,
            )
            checked += 1
    return checked


def twisted_line_nonsplit_sum(
    p: int,
    eta: List[complex],
    nu: List[complex],
) -> complex:
    delta = least_nonsquare(p)
    total = eta[(-2) % p] * transformed_inner(p, 2 % p, nu)
    for t in range(p):
        denominator = (t * t - delta) % p
        y = twisted_discriminant_y(p, t, delta)
        total += (
            eta[(-y) % p]
            * legendre(-3, p)
            * nu[t * pow(denominator, -1, p) % p]
            * twisted_line_kernel_trace(p, t, delta, nu)
        )
    return total


def verify_twisted_line_twist_divisor(p: int) -> Tuple[int, int, int, int]:
    delta = least_nonsquare(p)
    inverse_two = pow(2, -1, p)
    outer_zero_roots = {0}
    outer_pole_roots = {t for t in range(p) if (t * t - delta) % p == 0}
    outer_mellin_roots = {
        t for t in range(p) if (2 * t * t + delta) % p == 0
    }
    trace_collision_roots = {
        t for t in range(p) if (t * t - 4 * delta) % p == 0
    }

    if outer_pole_roots:
        raise AssertionError((p, delta, "unexpected_rational_denominator_root"))
    if trace_collision_roots:
        raise AssertionError((p, delta, "unexpected_rational_collision_root"))
    expected_mellin_root_count = 1 + legendre(-delta * inverse_two, p)
    if len(outer_mellin_roots) != expected_mellin_root_count:
        raise AssertionError(
            (p, delta, outer_mellin_roots, expected_mellin_root_count)
        )
    if outer_zero_roots & outer_mellin_roots:
        raise AssertionError((p, delta, "zero_outer_collision"))

    # Geometric disjointness of t=0, t^2=delta, t^2=-delta/2, and t^2=4delta.
    if delta % p == 0:
        raise AssertionError((p, delta, "zero_delta"))
    if (delta + delta * inverse_two) % p == 0:
        raise AssertionError((p, delta, "pole_mellin_collision"))
    if (delta - 4 * delta) % p == 0:
        raise AssertionError((p, delta, "pole_trace_collision"))
    if ((-delta * inverse_two) - 4 * delta) % p == 0:
        raise AssertionError((p, delta, "mellin_trace_collision"))

    # The outer twist is unramified at the K(t) collision pair.
    for value in (4 * delta % p,):
        if value == 0 or value == delta % p or (2 * value + delta) % p == 0:
            raise AssertionError((p, delta, value, "trace_collision_outer_twist"))

    geometric_outer_points = 1 + 2 + 2 + 1  # t=0, D=0, N=0, infinity.
    geometric_trace_points = 2              # t^2=4delta.
    rational_outer_points = (
        len(outer_zero_roots) + len(outer_pole_roots) + len(outer_mellin_roots) + 1
    )
    return (
        rational_outer_points,
        geometric_outer_points,
        len(trace_collision_roots),
        geometric_trace_points,
    )


def verify_twisted_line_deck_symmetry(
    p: int,
    table: List[List[complex]],
) -> Tuple[int, float, float, float]:
    delta = least_nonsquare(p)
    checked = 0
    max_kernel_difference = 0.0
    max_summand_difference = 0.0
    max_kernel_ratio = 0.0
    kernel_values: Dict[int, List[complex]] = {}
    for nu_exponent in range(1, p - 1):
        nu = table[nu_exponent]
        kernel_values[nu_exponent] = [
            twisted_line_kernel_trace(p, t, delta, nu) for t in range(p)
        ]
        for t in range(p):
            actual_kernel = kernel_values[nu_exponent][(-t) % p]
            expected_kernel = nu[(-1) % p] * kernel_values[nu_exponent][t]
            assert_close(
                (p, t, nu_exponent, "twisted_line_kernel_deck"),
                actual_kernel,
                expected_kernel,
            )
            max_kernel_difference = max(
                max_kernel_difference,
                abs(actual_kernel - expected_kernel),
            )
            kernel_ratio = abs(kernel_values[nu_exponent][t])
            max_kernel_ratio = max(max_kernel_ratio, kernel_ratio / math.sqrt(p))
            if kernel_ratio > 2 * math.sqrt(p) + TOLERANCE:
                raise AssertionError((p, t, nu_exponent, "kernel_2sqrt"))
            checked += 1

    for eta_exponent in range(1, p - 1):
        eta = table[eta_exponent]
        for nu_exponent in range(1, p - 1):
            nu = table[nu_exponent]
            for t in range(p):
                minus_t = (-t) % p
                denominator = (t * t - delta) % p
                y = twisted_discriminant_y(p, t, delta)
                actual_summand = (
                    eta[(-y) % p]
                    * nu[minus_t * pow(denominator, -1, p) % p]
                    * kernel_values[nu_exponent][minus_t]
                )
                expected_summand = (
                    eta[(-y) % p]
                    * nu[t * pow(denominator, -1, p) % p]
                    * kernel_values[nu_exponent][t]
                )
                assert_close(
                    (p, t, eta_exponent, nu_exponent, "twisted_line_deck"),
                    actual_summand,
                    expected_summand,
                )
                max_summand_difference = max(
                    max_summand_difference,
                    abs(actual_summand - expected_summand),
                )
    return (
        checked,
        max_kernel_difference,
        max_summand_difference,
        max_kernel_ratio,
    )


def quotient_line_kernel_trace(
    p: int,
    s_value: int,
    delta: int,
    nu: List[complex],
) -> complex:
    total = 0j
    for r_value in range(p):
        total += nu[(r_value - 1) % p] * legendre(
            s_value * r_value * r_value - 4 * delta,
            p,
        )
    return total


def verify_quotient_line_kernel_trace(
    p: int,
    table: List[List[complex]],
) -> Tuple[int, float]:
    delta = least_nonsquare(p)
    checked = 0
    max_difference = 0.0
    for nu_exponent in range(1, p - 1):
        nu = table[nu_exponent]
        for t in range(1, p):
            s_value = t * t % p
            actual = twisted_line_kernel_trace(p, t, delta, nu)
            expected = nu[t] * quotient_line_kernel_trace(
                p,
                s_value,
                delta,
                nu,
            )
            assert_close(
                (p, t, nu_exponent, "quotient_line_kernel_trace"),
                actual,
                expected,
            )
            max_difference = max(max_difference, abs(actual - expected))
            checked += 1
    return checked, max_difference


def quotient_line_nonsplit_sum(
    p: int,
    eta: List[complex],
    nu: List[complex],
) -> complex:
    delta = least_nonsquare(p)
    total = eta[(-2) % p] * transformed_inner(p, 2 % p, nu)
    for s_value in range(p):
        if s_value == delta:
            continue
        projector_weight = 1 + legendre(s_value, p)
        if projector_weight == 0:
            continue
        denominator = (s_value - delta) % p
        y = (2 * s_value + delta) * pow(denominator, -1, p) % p
        total += (
            legendre(-3, p)
            * projector_weight
            * eta[(-y) % p]
            * nu[s_value * pow(denominator, -1, p) % p]
            * quotient_line_kernel_trace(p, s_value, delta, nu)
        )
    return total


def verify_quotient_line_support(p: int) -> Tuple[int, int]:
    delta = least_nonsquare(p)
    support_points = {
        0,
        delta % p,
        (-delta * pow(2, -1, p)) % p,
        (4 * delta) % p,
    }
    if len(support_points) != 4:
        raise AssertionError((p, delta, support_points, "quotient_support_collision"))
    rational_finite_points = len(support_points)
    geometric_projective_points = rational_finite_points + 1
    return rational_finite_points, geometric_projective_points


def verify_quotient_line_kernel_moments(
    p: int,
    table: List[List[complex]],
) -> Tuple[int, float, float]:
    delta = least_nonsquare(p)
    checked = 0
    max_zero_value = 0.0
    max_second_moment_error = 0.0
    for nu_exponent in range(1, p - 1):
        nu = table[nu_exponent]
        values = [
            quotient_line_kernel_trace(p, s_value, delta, nu)
            for s_value in range(p)
        ]
        zero_value = abs(values[0])
        second_moment = sum(abs(value) ** 2 for value in values)
        nu_minus_one_value = nu[(-1) % p]
        if abs(nu_minus_one_value.imag) > TOLERANCE:
            raise AssertionError((p, nu_exponent, "nu_minus_one_not_real"))
        nu_minus_one = int(round(nu_minus_one_value.real))
        if nu_minus_one not in {-1, 1}:
            raise AssertionError((p, nu_exponent, "nu_minus_one_not_sign"))
        expected_second_moment = p * p - 2 * p - 1 - p * nu_minus_one
        max_zero_value = max(max_zero_value, zero_value)
        max_second_moment_error = max(
            max_second_moment_error,
            abs(second_moment - expected_second_moment),
        )
        if zero_value > TOLERANCE:
            raise AssertionError((p, nu_exponent, "quotient_kernel_zero"))
        if abs(second_moment - expected_second_moment) > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "quotient_kernel_second_moment",
                    second_moment,
                    expected_second_moment,
                )
            )
        checked += 1
    return checked, max_zero_value, max_second_moment_error


def verify_quotient_line_mellin_spectrum(
    p: int,
    table: List[List[complex]],
) -> Tuple[int, float, float]:
    delta = least_nonsquare(p)
    c_value = 4 * delta % p
    quadratic = table[(p - 1) // 2]
    chi_minus_c = legendre(-c_value, p)
    checked = 0
    max_formula_error = 0.0
    max_mellin_ratio = 0.0
    for nu_exponent in range(1, p - 1):
        nu = table[nu_exponent]
        kernel_values = [
            quotient_line_kernel_trace(p, s_value, delta, nu)
            for s_value in range(p)
        ]
        for theta_exponent, theta in enumerate(table):
            theta_inverse_square = table[(-2 * theta_exponent) % (p - 1)]
            actual = sum(
                theta[s_value] * kernel_values[s_value]
                for s_value in range(p)
            )
            expected = (
                chi_minus_c
                * nu[(-1) % p]
                * theta[c_value]
                * jacobi_sum(p, theta, quadratic)
                * jacobi_sum(p, theta_inverse_square, nu)
            )
            if theta_exponent == 0:
                expected += chi_minus_c * nu[(-1) % p] * (p - 1)
            error = abs(actual - expected)
            max_formula_error = max(max_formula_error, error)
            max_mellin_ratio = max(max_mellin_ratio, abs(actual) / p)
            if error > TOLERANCE:
                raise AssertionError(
                    (
                        p,
                        nu_exponent,
                        theta_exponent,
                        "quotient_mellin_formula",
                        actual,
                        expected,
                    )
                )
            if abs(actual) > p + TOLERANCE:
                raise AssertionError(
                    (p, nu_exponent, theta_exponent, "quotient_mellin_bound")
                )
            checked += 1
    return checked, max_formula_error, max_mellin_ratio


def verify_quotient_line_mellin_magnitudes(
    p: int,
    table: List[List[complex]],
) -> Tuple[int, float, int, int, int]:
    delta = least_nonsquare(p)
    order = p - 1
    quadratic_exponent = order // 2
    checked = 0
    max_magnitude_error = 0.0
    total_p_size = 0
    total_sqrt_size = 0
    total_unit_size = 0
    for nu_exponent in range(1, order):
        nu = table[nu_exponent]
        kernel_values = [
            quotient_line_kernel_trace(p, s_value, delta, nu)
            for s_value in range(p)
        ]
        p_size = 0
        sqrt_size = 0
        unit_size = 0
        for theta_exponent, theta in enumerate(table):
            actual = sum(
                theta[s_value] * kernel_values[s_value]
                for s_value in range(p)
            )
            if theta_exponent == 0:
                expected_magnitude = float(p)
                p_size += 1
            elif theta_exponent == quadratic_exponent:
                expected_magnitude = 1.0
                unit_size += 1
            elif (2 * theta_exponent - nu_exponent) % order == 0:
                expected_magnitude = math.sqrt(p)
                sqrt_size += 1
            else:
                expected_magnitude = float(p)
                p_size += 1
            magnitude_error = abs(abs(actual) - expected_magnitude)
            max_magnitude_error = max(max_magnitude_error, magnitude_error)
            if magnitude_error > TOLERANCE:
                raise AssertionError(
                    (
                        p,
                        nu_exponent,
                        theta_exponent,
                        "quotient_mellin_magnitude",
                        abs(actual),
                        expected_magnitude,
                    )
                )
            checked += 1
        expected_sqrt_size = 2 if nu_exponent % 2 == 0 else 0
        expected_p_size = p - 4 if nu_exponent % 2 == 0 else p - 2
        if (p_size, sqrt_size, unit_size) != (
            expected_p_size,
            expected_sqrt_size,
            1,
        ):
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "quotient_mellin_magnitude_counts",
                    (p_size, sqrt_size, unit_size),
                    (expected_p_size, expected_sqrt_size, 1),
                )
            )
        total_p_size += p_size
        total_sqrt_size += sqrt_size
        total_unit_size += unit_size
    return checked, max_magnitude_error, total_p_size, total_sqrt_size, total_unit_size


def quotient_line_outer_twist_value(
    p: int,
    s_value: int,
    delta: int,
    eta: List[complex],
    nu: List[complex],
) -> complex:
    if s_value == delta:
        return 0j
    projector_weight = 1 + legendre(s_value, p)
    if projector_weight == 0:
        return 0j
    denominator = (s_value - delta) % p
    y = (2 * s_value + delta) * pow(denominator, -1, p) % p
    return (
        projector_weight
        * eta[(-y) % p]
        * nu[s_value * pow(denominator, -1, p) % p]
    )


def quotient_line_outer_kummer_piece(
    p: int,
    delta: int,
    alpha: List[complex],
    beta: List[complex],
    gamma: List[complex],
) -> complex:
    total = 0j
    for s_value in range(p):
        total += (
            alpha[s_value]
            * beta[(2 * s_value + delta) % p]
            * gamma[(s_value - delta) % p]
        )
    return total


def quotient_line_outer_standard_piece(
    p: int,
    alpha: List[complex],
    beta: List[complex],
    gamma: List[complex],
) -> complex:
    total = 0j
    for z_value in range(p):
        total += (
            alpha[z_value]
            * beta[(1 - z_value) % p]
            * gamma[(z_value + 2) % p]
        )
    return total


def quotient_line_outer_square_filtered_piece(
    p: int,
    alpha: List[complex],
    beta: List[complex],
    gamma: List[complex],
) -> complex:
    total = 0j
    square_class = legendre(-2, p)
    for z_value in range(p):
        total += (
            alpha[z_value]
            * (1 - square_class * legendre(z_value, p))
            * beta[(1 - z_value) % p]
            * gamma[(z_value + 2) % p]
        )
    return total


def quotient_line_kernel_square_filtered_jacobi(
    p: int,
    theta: List[complex],
    quadratic: List[complex],
) -> complex:
    total = 0j
    for x_value in range(p):
        total += (
            theta[x_value]
            * (1 - legendre(x_value, p))
            * quadratic[(1 - x_value) % p]
        )
    return total


def quotient_line_paired_diagonal_sum(
    p: int,
    eta: List[complex],
    nu: List[complex],
    gamma: List[complex],
) -> complex:
    total = 0j
    inverse_eight = pow(8, -1, p)
    square_class = legendre(-2, p)
    for z_value in range(1, p):
        outer_weight = (
            nu[z_value]
            * (1 - square_class * legendre(z_value, p))
            * eta[(1 - z_value) % p]
            * gamma[(z_value + 2) % p]
        )
        if abs(outer_weight) == 0:
            continue
        for y_value in range(1, p):
            x_value = (-z_value * y_value * y_value * inverse_eight) % p
            kernel_weight = (
                (1 - legendre(x_value, p))
                * legendre(1 - x_value, p)
            )
            if kernel_weight == 0:
                continue
            total += outer_weight * nu[(1 - y_value) % p] * kernel_weight
    return total


def quotient_line_paired_collapsed_diagonal_sum(
    p: int,
    eta: List[complex],
    nu: List[complex],
    gamma: List[complex],
) -> complex:
    total = 0j
    inverse_eight = pow(8, -1, p)
    square_class = legendre(-2, p)
    for z_value in range(1, p):
        outer_weight = (
            nu[z_value]
            * (1 - square_class * legendre(z_value, p))
            * eta[(1 - z_value) % p]
            * gamma[(z_value + 2) % p]
        )
        if abs(outer_weight) == 0:
            continue
        for y_value in range(1, p):
            kernel_value = legendre(
                1 + z_value * y_value * y_value * inverse_eight,
                p,
            )
            total += 2 * outer_weight * nu[(1 - y_value) % p] * kernel_value
    return total


def quotient_line_collapsed_rank_two_transform(
    p: int,
    eta: List[complex],
    nu: List[complex],
    gamma: List[complex],
) -> complex:
    total = 0j
    square_class = legendre(-2, p)
    for z_value in range(p):
        outer_weight = (
            nu[z_value]
            * (1 - square_class * legendre(z_value, p))
            * eta[(1 - z_value) % p]
            * gamma[(z_value + 2) % p]
        )
        if abs(outer_weight) == 0:
            continue
        total += outer_weight * (
            quotient_line_collapsed_inner_trace(p, z_value, nu) + 1
        )
    return total


def is_line_conic_admissible_pair(
    order: int,
    eta_exponent: int,
    nu_exponent: int,
) -> bool:
    a_exponent = (-eta_exponent) % order
    b_exponent = nu_exponent % order
    return (
        a_exponent != 0
        and b_exponent != 0
        and b_exponent != a_exponent
        and b_exponent != (-a_exponent) % order
        and b_exponent != (2 * a_exponent) % order
        and (2 * b_exponent - a_exponent) % order != 0
    )


def verify_quotient_line_collapsed_four_p_obstruction() -> Tuple[
    int, int, int, float, float
]:
    p = 97
    eta_exponent = 13
    nu_exponent = 91
    order = p - 1
    table = character_table(p, log_table(p))
    eta = table[eta_exponent]
    nu = table[nu_exponent]
    gamma = table[(-eta_exponent - nu_exponent) % order]
    rank_two_transform = quotient_line_collapsed_rank_two_transform(
        p,
        eta,
        nu,
        gamma,
    )
    rank_one_transform = quotient_line_outer_square_filtered_piece(
        p,
        nu,
        eta,
        gamma,
    )
    h_transform = rank_two_transform - rank_one_transform
    rank_two_ratio = abs(rank_two_transform) / p
    h_ratio = abs(h_transform) / p
    quadratic_exponent = order // 2
    if eta_exponent in {0, quadratic_exponent}:
        raise AssertionError((p, eta_exponent, "eta_not_generic"))
    if nu_exponent in {0, quadratic_exponent}:
        raise AssertionError((p, nu_exponent, "nu_not_generic"))
    if (2 * eta_exponent - nu_exponent) % order == 0:
        raise AssertionError((p, eta_exponent, nu_exponent, "sqrt_row"))
    if not is_line_conic_admissible_pair(order, eta_exponent, nu_exponent):
        raise AssertionError((p, eta_exponent, nu_exponent, "not_admissible"))
    if rank_two_ratio <= 4.0 + TOLERANCE:
        raise AssertionError((p, eta_exponent, nu_exponent, rank_two_ratio))
    if h_ratio <= 4.0 + TOLERANCE:
        raise AssertionError((p, eta_exponent, nu_exponent, h_ratio))
    return (
        p,
        eta_exponent,
        nu_exponent,
        round(rank_two_ratio, 10),
        round(h_ratio, 10),
    )


def quotient_line_collapsed_mobius_kernel(
    p: int,
    r_value: int,
    nu: List[complex],
) -> complex:
    if r_value == (-1) % p:
        return 0j
    denominator = (r_value + 1) % p
    z_value = (1 - 2 * r_value) * pow(denominator, -1, p) % p
    nu_argument = (1 - 2 * r_value) * pow(3, -1, p) % p
    return (
        nu[nu_argument]
        * (1 - legendre(-2, p) * legendre(z_value, p))
        * (quotient_line_collapsed_inner_trace(p, z_value, nu) + 1)
    )


def quotient_line_collapsed_mobius_transform(
    p: int,
    eta: List[complex],
    nu: List[complex],
) -> complex:
    total = 0j
    for r_value in range(1, p):
        if r_value == (-1) % p:
            continue
        total += eta[r_value] * quotient_line_collapsed_mobius_kernel(
            p,
            r_value,
            nu,
        )
    return total


def collapsed_quadratic_l_energy_formula(
    p: int,
    nu_exponent: int,
    table: List[List[complex]],
) -> Tuple[complex, float]:
    order = p - 1
    quadratic_exponent = order // 2
    quadratic = table[quadratic_exponent]
    b_one = -legendre(-1, p)
    if nu_exponent % 2 == 1:
        return legendre(8, p) * p * b_one, float(p)

    alpha_exponent = nu_exponent // 2
    alpha = table[alpha_exponent]
    alpha_inverse = table[(-alpha_exponent) % order]
    alpha_quadratic = table[(alpha_exponent + quadratic_exponent) % order]
    alpha_inverse_quadratic = table[
        (-alpha_exponent + quadratic_exponent) % order
    ]
    t_transform = legendre(-1, p) * (
        jacobi_sum(p, alpha, quadratic)
        * jacobi_sum(p, alpha_inverse_quadratic, quadratic)
        + jacobi_sum(p, alpha_quadratic, quadratic)
        * jacobi_sum(p, alpha_inverse, quadratic)
    )
    return legendre(8, p) * (p * b_one - t_transform), 3.0 * p


def verify_quotient_line_collapsed_mobius_energy(
    p: int,
    table: List[List[complex]],
) -> Tuple[
    int,
    int,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    int,
    int,
    float,
]:
    order = p - 1
    expected_active = (p - 1) // 2
    if legendre(-2, p) == -1:
        expected_active -= 1
    checked = 0
    max_parseval_error = 0.0
    max_energy_ratio = 0.0
    max_pointwise_ratio = 0.0
    max_rms_ratio = 0.0
    max_full_energy_error = 0.0
    max_sharp_energy_ratio = 0.0
    max_sharp_bound_rms_ratio = 0.0
    max_quadratic_energy_error = 0.0
    max_quadratic_energy_ratio = 0.0
    max_selected_energy_ratio = 0.0
    max_selected_bound_rms_ratio = 0.0
    max_four_p_count = 0
    max_admissible_four_p_count = 0
    max_transform_ratio = 0.0
    for nu_exponent in range(1, order):
        nu = table[nu_exponent]
        active_count = 0
        energy = 0.0
        kernels: List[Tuple[int, complex]] = []
        for r_value in range(1, p):
            if r_value == (-1) % p:
                continue
            denominator = (r_value + 1) % p
            z_value = (1 - 2 * r_value) * pow(denominator, -1, p) % p
            nu_argument = (1 - 2 * r_value) * pow(3, -1, p) % p
            active = (
                nu_argument != 0
                and 1 - legendre(-2, p) * legendre(z_value, p) != 0
            )
            if active:
                active_count += 1
            kernel = quotient_line_collapsed_mobius_kernel(p, r_value, nu)
            kernels.append((r_value, kernel))
            energy += abs(kernel) ** 2
            max_pointwise_ratio = max(
                max_pointwise_ratio,
                abs(kernel) / (4 * math.sqrt(p)),
            )
            if abs(kernel) > 4 * math.sqrt(p) + TOLERANCE:
                raise AssertionError(
                    (
                        p,
                        nu_exponent,
                        r_value,
                        "collapsed_mobius_kernel_4sqrt",
                        kernel,
                    )
                )
        if active_count != expected_active:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_mobius_active_count",
                    active_count,
                    expected_active,
                )
            )
        full_l_energy = sum(
            abs(quotient_line_collapsed_inner_trace(p, z_value, nu) + 1) ** 2
            for z_value in range(1, p)
        )
        nu_minus_one_value = nu[(-1) % p]
        if abs(nu_minus_one_value.imag) > TOLERANCE:
            raise AssertionError((p, nu_exponent, "mobius_nu_minus_one_not_real"))
        nu_minus_one = int(round(nu_minus_one_value.real))
        expected_full_l_energy = p * p - 2 * p - 1 - p * nu_minus_one
        full_energy_error = abs(full_l_energy - expected_full_l_energy)
        max_full_energy_error = max(max_full_energy_error, full_energy_error)
        if full_energy_error > 100 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_mobius_full_l_energy",
                    full_l_energy,
                    expected_full_l_energy,
                )
            )
        quadratic_l_energy = sum(
            legendre(z_value, p)
            * abs(quotient_line_collapsed_inner_trace(p, z_value, nu) + 1) ** 2
            for z_value in range(1, p)
        )
        expected_quadratic_l_energy, quadratic_energy_bound = (
            collapsed_quadratic_l_energy_formula(p, nu_exponent, table)
        )
        quadratic_energy_error = abs(
            quadratic_l_energy - expected_quadratic_l_energy
        )
        max_quadratic_energy_error = max(
            max_quadratic_energy_error,
            quadratic_energy_error,
        )
        max_quadratic_energy_ratio = max(
            max_quadratic_energy_ratio,
            abs(quadratic_l_energy) / quadratic_energy_bound,
        )
        if quadratic_energy_error > 100 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_mobius_quadratic_l_energy",
                    quadratic_l_energy,
                    expected_quadratic_l_energy,
                )
            )
        energy_bound = 16 * p * expected_active
        max_energy_ratio = max(max_energy_ratio, energy / energy_bound)
        if energy > energy_bound + 100 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_mobius_energy_bound",
                    energy,
                    energy_bound,
                )
            )
        sharp_energy_bound = 4 * expected_full_l_energy
        max_sharp_energy_ratio = max(
            max_sharp_energy_ratio,
            energy / sharp_energy_bound,
        )
        max_sharp_bound_rms_ratio = max(
            max_sharp_bound_rms_ratio,
            math.sqrt(sharp_energy_bound) / p,
        )
        if energy > sharp_energy_bound + 100 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_mobius_sharp_energy_bound",
                    energy,
                    sharp_energy_bound,
                )
            )
        selected_energy_bound = 2 * p * p - 2
        max_selected_energy_ratio = max(
            max_selected_energy_ratio,
            energy / selected_energy_bound,
        )
        max_selected_bound_rms_ratio = max(
            max_selected_bound_rms_ratio,
            math.sqrt(selected_energy_bound) / p,
        )
        if energy > selected_energy_bound + 100 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_mobius_selected_energy_bound",
                    energy,
                    selected_energy_bound,
                )
            )
        max_rms_ratio = max(max_rms_ratio, math.sqrt(energy) / p)
        parseval_sum = 0.0
        four_p_count = 0
        admissible_four_p_count = 0
        four_p_count_bound = (order * (p * p - 1)) // (8 * p * p)
        for eta_exponent, eta in enumerate(table):
            transform = sum(
                eta[r_value] * kernel
                for r_value, kernel in kernels
            )
            parseval_sum += abs(transform) ** 2
            max_transform_ratio = max(max_transform_ratio, abs(transform) / p)
            if abs(transform) >= 4 * p - TOLERANCE:
                four_p_count += 1
                if is_line_conic_admissible_pair(
                    order,
                    eta_exponent,
                    nu_exponent,
                ):
                    admissible_four_p_count += 1
        max_four_p_count = max(max_four_p_count, four_p_count)
        max_admissible_four_p_count = max(
            max_admissible_four_p_count,
            admissible_four_p_count,
        )
        if four_p_count > four_p_count_bound:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_mobius_four_p_sparsity",
                    four_p_count,
                    four_p_count_bound,
                )
            )
        if admissible_four_p_count > four_p_count_bound:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_mobius_admissible_four_p_sparsity",
                    admissible_four_p_count,
                    four_p_count_bound,
                )
            )
        parseval_error = abs(parseval_sum - order * energy)
        max_parseval_error = max(max_parseval_error, parseval_error)
        if parseval_error > 100 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_mobius_parseval",
                    parseval_sum,
                    order * energy,
                )
            )
        checked += order
    return (
        checked,
        expected_active,
        max_parseval_error,
        max_energy_ratio,
        max_pointwise_ratio,
        max_rms_ratio,
        max_full_energy_error,
        max_sharp_energy_ratio,
        max_sharp_bound_rms_ratio,
        max_quadratic_energy_error,
        max_quadratic_energy_ratio,
        max_selected_energy_ratio,
        max_selected_bound_rms_ratio,
        max_four_p_count,
        max_admissible_four_p_count,
        max_transform_ratio,
    )


def quotient_line_collapsed_inner_trace(
    p: int,
    z_value: int,
    nu: List[complex],
) -> complex:
    total = 0j
    inverse_eight = pow(8, -1, p)
    for y_value in range(1, p):
        total += nu[(1 - y_value) % p] * legendre(
            1 + z_value * y_value * y_value * inverse_eight,
            p,
        )
    return total


def verify_quotient_line_collapsed_inner_spectrum(
    p: int,
    table: List[List[complex]],
) -> Tuple[int, float, float, float, float, float, float, int, int, int]:
    order = p - 1
    quadratic_exponent = order // 2
    quadratic = table[quadratic_exponent]
    checked = 0
    max_formula_error = 0.0
    max_magnitude_error = 0.0
    max_moment_error = 0.0
    max_special_error = 0.0
    max_special_ratio = 0.0
    max_regular_full_ratio = 0.0
    total_p_size = 0
    total_sqrt_size = 0
    total_unit_size = 0
    for nu_exponent in range(1, order):
        nu = table[nu_exponent]
        inner_values = [
            quotient_line_collapsed_inner_trace(p, z_value, nu)
            for z_value in range(p)
        ]
        if abs(inner_values[0] + 1) > TOLERANCE:
            raise AssertionError(
                (p, nu_exponent, "collapsed_inner_zero", inner_values[0])
            )
        special_value = inner_values[(-8) % p]
        expected_special_value = (
            nu[2 % p]
            * jacobi_sum(
                p,
                table[(nu_exponent + quadratic_exponent) % order],
                quadratic,
            )
            - 1
        )
        special_error = abs(special_value - expected_special_value)
        max_special_error = max(max_special_error, special_error)
        max_special_ratio = max(
            max_special_ratio,
            abs(special_value) / (math.sqrt(p) + 1),
        )
        if special_error > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_inner_minus_eight",
                    special_value,
                    expected_special_value,
                )
            )
        for z_value in range(1, p):
            if z_value == (-8) % p:
                continue
            regular_full_trace = inner_values[z_value] + 1
            max_regular_full_ratio = max(
                max_regular_full_ratio,
                abs(regular_full_trace) / (2 * math.sqrt(p)),
            )
            if abs(regular_full_trace) > 2 * math.sqrt(p) + TOLERANCE:
                raise AssertionError(
                    (
                        p,
                        nu_exponent,
                        z_value,
                        "collapsed_inner_regular_bound",
                        regular_full_trace,
                    )
                )
        second_moment = sum(abs(inner_values[z_value]) ** 2 for z_value in range(1, p))
        nu_minus_one_value = nu[(-1) % p]
        if abs(nu_minus_one_value.imag) > TOLERANCE:
            raise AssertionError((p, nu_exponent, "inner_nu_minus_one_not_real"))
        nu_minus_one = int(round(nu_minus_one_value.real))
        expected_second_moment = p * p - 3 * p - 2 - p * nu_minus_one
        moment_error = abs(second_moment - expected_second_moment)
        max_moment_error = max(max_moment_error, moment_error)
        if moment_error > 100 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_inner_second_moment",
                    second_moment,
                    expected_second_moment,
                )
            )
        p_size = 0
        sqrt_size = 0
        unit_size = 0
        for rho_exponent, rho in enumerate(table):
            actual = sum(
                rho[z_value] * inner_values[z_value]
                for z_value in range(1, p)
            )
            expected = (
                rho[(-8) % p]
                * jacobi_sum(p, rho, quadratic)
                * jacobi_sum(p, table[(-2 * rho_exponent) % order], nu)
            )
            formula_error = abs(actual - expected)
            max_formula_error = max(max_formula_error, formula_error)
            if formula_error > TOLERANCE:
                raise AssertionError(
                    (
                        p,
                        nu_exponent,
                        rho_exponent,
                        "collapsed_inner_mellin_formula",
                        actual,
                        expected,
                    )
                )
            if rho_exponent in {0, quadratic_exponent}:
                expected_magnitude = 1.0
                unit_size += 1
            elif (2 * rho_exponent - nu_exponent) % order == 0:
                expected_magnitude = math.sqrt(p)
                sqrt_size += 1
            else:
                expected_magnitude = float(p)
                p_size += 1
            magnitude_error = abs(abs(actual) - expected_magnitude)
            max_magnitude_error = max(max_magnitude_error, magnitude_error)
            if magnitude_error > TOLERANCE:
                raise AssertionError(
                    (
                        p,
                        nu_exponent,
                        rho_exponent,
                        "collapsed_inner_mellin_magnitude",
                        abs(actual),
                        expected_magnitude,
                    )
                )
            checked += 1
        expected_sqrt_size = 2 if nu_exponent % 2 == 0 else 0
        expected_p_size = p - 5 if nu_exponent % 2 == 0 else p - 3
        if (p_size, sqrt_size, unit_size) != (
            expected_p_size,
            expected_sqrt_size,
            2,
        ):
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    "collapsed_inner_magnitude_counts",
                    (p_size, sqrt_size, unit_size),
                    (expected_p_size, expected_sqrt_size, 2),
                )
            )
        total_p_size += p_size
        total_sqrt_size += sqrt_size
        total_unit_size += unit_size
    return (
        checked,
        max_formula_error,
        max_magnitude_error,
        max_moment_error,
        max_special_error,
        max_special_ratio,
        max_regular_full_ratio,
        total_p_size,
        total_sqrt_size,
        total_unit_size,
    )


def verify_quotient_line_spectral_normal_form(
    p: int,
    eta_exponent: int,
    nu_exponent: int,
    table: List[List[complex]],
) -> Tuple[
    int,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    int,
    float,
    float,
    int,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    float,
    int,
]:
    delta = least_nonsquare(p)
    order = p - 1
    eta = table[eta_exponent]
    nu = table[nu_exponent]
    quadratic_exponent = order // 2
    quadratic = table[quadratic_exponent]
    c_value = 4 * delta % p
    chi_minus_c = legendre(-c_value, p)
    gamma = table[(-eta_exponent - nu_exponent) % order]
    outer_values = [
        quotient_line_outer_twist_value(p, s_value, delta, eta, nu)
        for s_value in range(p)
    ]
    kernel_values = [
        quotient_line_kernel_trace(p, s_value, delta, nu)
        for s_value in range(p)
    ]
    direct_pairing = sum(
        outer_values[s_value] * kernel_values[s_value]
        for s_value in range(p)
    )
    spectral_pairing = 0j
    exceptional_pairing = 0j
    exceptional_count = 0
    generic_phase_sum = 0j
    generic_count = 0
    max_generic_phase_error = 0.0
    checked = 0
    max_outer_decomposition_error = 0.0
    max_outer_standard_error = 0.0
    max_outer_quadratic_shift_error = 0.0
    max_kernel_pair_phase_error = 0.0
    max_delta_free_pair_error = 0.0
    max_pair_jacobi_product_error = 0.0
    max_outer_square_filter_error = 0.0
    max_kernel_square_filter_error = 0.0
    max_algebraic_pair_orbit_error = 0.0
    max_pair_diagonal_error = 0.0
    max_generic_diagonal_error = 0.0
    max_collapsed_diagonal_error = 0.0
    max_collapsed_singular_error = 0.0
    max_collapsed_rank_one_error = 0.0
    max_collapsed_rank_one_piece_ratio = 0.0
    max_collapsed_rank_one_ratio = 0.0
    max_collapsed_rank_two_split_error = 0.0
    max_collapsed_rank_two_mobius_error = 0.0
    max_collapsed_mobius_deleted_error = 0.0
    max_collapsed_rank_two_ratio = 0.0
    max_collapsed_h_ratio = 0.0
    max_paired_phase_ratio = 0.0
    paired_generic_count = 0
    max_outer_piece_ratio = 0.0
    max_outer_ratio = 0.0
    outer_energy = 0.0
    kernel_energy = 0.0
    outer_inverse_mellins: List[complex] = []
    kernel_mellins: List[complex] = []
    generic_flags: List[bool] = []
    for theta_exponent, theta in enumerate(table):
        outer_mellin = sum(
            theta[s_value] * outer_values[s_value]
            for s_value in range(p)
        )
        alpha_plain = table[(theta_exponent + nu_exponent) % order]
        alpha_quadratic = table[
            (theta_exponent + nu_exponent + quadratic_exponent) % order
        ]
        plain_piece = quotient_line_outer_kummer_piece(
            p, delta, alpha_plain, eta, gamma
        )
        quadratic_piece = quotient_line_outer_kummer_piece(
            p, delta, alpha_quadratic, eta, gamma
        )
        inv_two = pow(2, -1, p)
        scale_point = (-delta * inv_two) % p
        for alpha, piece in (
            (alpha_plain, plain_piece),
            (alpha_quadratic, quadratic_piece),
        ):
            expected_piece = (
                alpha[scale_point]
                * eta[delta % p]
                * gamma[scale_point]
                * quotient_line_outer_standard_piece(p, alpha, eta, gamma)
            )
            standard_error = abs(piece - expected_piece)
            max_outer_standard_error = max(
                max_outer_standard_error,
                standard_error,
            )
            if standard_error > TOLERANCE:
                raise AssertionError(
                    (
                        p,
                        eta_exponent,
                        nu_exponent,
                        theta_exponent,
                        "outer_standard_form",
                        piece,
                        expected_piece,
                    )
                )
        max_outer_piece_ratio = max(
            max_outer_piece_ratio,
            abs(plain_piece) / math.sqrt(p),
            abs(quadratic_piece) / math.sqrt(p),
        )
        if (
            abs(plain_piece) > 2 * math.sqrt(p) + TOLERANCE
            or abs(quadratic_piece) > 2 * math.sqrt(p) + TOLERANCE
        ):
            raise AssertionError(
                (
                    p,
                    eta_exponent,
                    nu_exponent,
                    theta_exponent,
                    "outer_kummer_piece_2sqrt",
                )
            )
        expected_outer_mellin = eta[(-1) % p] * (
            plain_piece + quadratic_piece
        )
        outer_error = abs(outer_mellin - expected_outer_mellin)
        max_outer_decomposition_error = max(
            max_outer_decomposition_error,
            outer_error,
        )
        if outer_error > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    eta_exponent,
                    nu_exponent,
                    theta_exponent,
                    "outer_mellin_decomposition",
                )
            )
        if abs(outer_mellin) > 4 * math.sqrt(p) + TOLERANCE:
            raise AssertionError(
                (
                    p,
                    eta_exponent,
                    nu_exponent,
                    theta_exponent,
                    "outer_mellin_4sqrt",
                )
            )
        max_outer_ratio = max(max_outer_ratio, abs(outer_mellin) / math.sqrt(p))
        inverse_theta = table[(-theta_exponent) % order]
        outer_inverse_mellin = sum(
            inverse_theta[s_value] * outer_values[s_value]
            for s_value in range(p)
        )
        kernel_mellin = sum(
            theta[s_value] * kernel_values[s_value]
            for s_value in range(p)
        )
        outer_inverse_mellins.append(outer_inverse_mellin)
        kernel_mellins.append(kernel_mellin)
        is_exceptional = (
            theta_exponent == 0
            or theta_exponent == quadratic_exponent
            or (2 * theta_exponent - nu_exponent) % order == 0
        )
        generic_flags.append(not is_exceptional)
        if is_exceptional:
            exceptional_pairing += outer_inverse_mellin * kernel_mellin
            exceptional_count += 1
        else:
            generic_phase = kernel_mellin / p
            generic_phase_error = abs(abs(generic_phase) - 1)
            max_generic_phase_error = max(
                max_generic_phase_error,
                generic_phase_error,
            )
            if generic_phase_error > TOLERANCE:
                raise AssertionError(
                    (
                        p,
                        eta_exponent,
                        nu_exponent,
                        theta_exponent,
                        "generic_kernel_phase",
                        abs(generic_phase),
                    )
                )
            generic_phase_sum += outer_inverse_mellin * generic_phase
            generic_count += 1
        outer_energy += abs(outer_mellin) ** 2
        kernel_energy += abs(kernel_mellin) ** 2
        spectral_pairing += outer_inverse_mellin * kernel_mellin
        checked += 1
    nu_minus_one_value = nu[(-1) % p]
    if abs(nu_minus_one_value.imag) > TOLERANCE:
        raise AssertionError((p, nu_exponent, "spectral_nu_minus_one_not_real"))
    nu_minus_one = int(round(nu_minus_one_value.real))
    if nu_minus_one not in {-1, 1}:
        raise AssertionError((p, nu_exponent, "spectral_nu_minus_one_not_sign"))
    expected_exceptional_count = 4 if nu_minus_one == 1 else 2
    if exceptional_count != expected_exceptional_count:
        raise AssertionError(
            (
                p,
                nu_exponent,
                "exceptional_theta_count",
                exceptional_count,
                expected_exceptional_count,
            )
        )
    expected_generic_count = order - expected_exceptional_count
    if generic_count != expected_generic_count:
        raise AssertionError(
            (
                p,
                nu_exponent,
                "generic_theta_count",
                generic_count,
                expected_generic_count,
            )
        )
    exceptional_contribution = exceptional_pairing / order
    exceptional_bound = (
        4
        * math.sqrt(p)
        * (p + 1 + (2 * math.sqrt(p) if nu_minus_one == 1 else 0))
        / order
    )
    if abs(exceptional_contribution) > exceptional_bound + TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "exceptional_spectral_bound",
                exceptional_contribution,
                exceptional_bound,
            )
        )
    expected_outer_energy = 2 * (p - 1) * (p - 2 + legendre(-2, p))
    expected_kernel_energy = (p - 1) * (
        p * p - 2 * p - 1 - p * nu_minus_one
    )
    outer_energy_error = abs(outer_energy - expected_outer_energy)
    kernel_energy_error = abs(kernel_energy - expected_kernel_energy)
    if outer_energy_error > TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "outer_spectral_energy",
                outer_energy,
                expected_outer_energy,
            )
        )
    if kernel_energy_error > 100 * TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "kernel_spectral_energy",
                kernel_energy,
                expected_kernel_energy,
            )
        )
    reconstructed_pairing = spectral_pairing / order
    generic_pairing = p * generic_phase_sum / order
    paired_generic_phase_sum = 0j
    scale_point = (-delta * pow(2, -1, p)) % p
    pair_constant = -legendre(-1, p) * eta[2 % p] * nu[(-1) % p]
    for theta_exponent, theta in enumerate(table):
        partner_exponent = (theta_exponent + quadratic_exponent) % order
        if theta_exponent > partner_exponent:
            continue
        if not generic_flags[theta_exponent]:
            continue
        if not generic_flags[partner_exponent]:
            raise AssertionError(
                (p, nu_exponent, theta_exponent, "generic_pair_stability")
            )
        outer_shift_error = abs(
            outer_inverse_mellins[theta_exponent]
            - outer_inverse_mellins[partner_exponent]
        )
        max_outer_quadratic_shift_error = max(
            max_outer_quadratic_shift_error,
            outer_shift_error,
        )
        if outer_shift_error > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    eta_exponent,
                    nu_exponent,
                    theta_exponent,
                    "outer_quadratic_shift",
                    outer_inverse_mellins[theta_exponent],
                    outer_inverse_mellins[partner_exponent],
                )
            )
        paired_phase = (
            kernel_mellins[theta_exponent]
            + kernel_mellins[partner_exponent]
        ) / p
        theta_inverse_square = table[(-2 * theta_exponent) % order]
        theta_chi = table[partner_exponent]
        first_jacobi = jacobi_sum(p, theta, quadratic)
        shifted_jacobi = jacobi_sum(p, theta_chi, quadratic)
        square_jacobi = jacobi_sum(p, theta_inverse_square, nu)
        filtered_jacobi = quotient_line_kernel_square_filtered_jacobi(
            p,
            theta,
            quadratic,
        )
        kernel_filter_error = abs(
            filtered_jacobi - (first_jacobi - shifted_jacobi)
        )
        max_kernel_square_filter_error = max(
            max_kernel_square_filter_error,
            kernel_filter_error,
        )
        if kernel_filter_error > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    theta_exponent,
                    "kernel_square_class_filter",
                    filtered_jacobi,
                    first_jacobi - shifted_jacobi,
                )
            )
        expected_paired_phase = (
            chi_minus_c
            * nu[(-1) % p]
            * theta[c_value]
            * square_jacobi
            * (first_jacobi + quadratic[c_value] * shifted_jacobi)
            / p
        )
        pair_phase_error = abs(paired_phase - expected_paired_phase)
        max_kernel_pair_phase_error = max(
            max_kernel_pair_phase_error,
            pair_phase_error,
        )
        if pair_phase_error > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    theta_exponent,
                    "paired_kernel_phase_formula",
                    paired_phase,
                    expected_paired_phase,
                )
            )
        jacobi_product_error = abs(
            first_jacobi * shifted_jacobi - legendre(-1, p) * p
        )
        max_pair_jacobi_product_error = max(
            max_pair_jacobi_product_error,
            jacobi_product_error,
        )
        if jacobi_product_error > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    theta_exponent,
                    "quadratic_jacobi_pair_product",
                    first_jacobi * shifted_jacobi,
                    legendre(-1, p) * p,
                )
            )
        alpha_plain = table[(-theta_exponent + nu_exponent) % order]
        alpha_quadratic = table[
            (-theta_exponent + nu_exponent + quadratic_exponent) % order
        ]
        standard_plain = quotient_line_outer_standard_piece(
            p,
            alpha_plain,
            eta,
            gamma,
        )
        standard_quadratic = quotient_line_outer_standard_piece(
            p,
            alpha_quadratic,
            eta,
            gamma,
        )
        filtered_outer = quotient_line_outer_square_filtered_piece(
            p,
            alpha_plain,
            eta,
            gamma,
        )
        outer_filter_error = abs(
            filtered_outer
            - (standard_plain - legendre(-2, p) * standard_quadratic)
        )
        max_outer_square_filter_error = max(
            max_outer_square_filter_error,
            outer_filter_error,
        )
        if outer_filter_error > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    eta_exponent,
                    nu_exponent,
                    theta_exponent,
                    "outer_square_class_filter",
                    filtered_outer,
                    standard_plain - legendre(-2, p) * standard_quadratic,
                )
            )
        expected_outer_inverse = (
            eta[2 % p]
            * theta[scale_point].conjugate()
            * filtered_outer
        )
        outer_delta_free_error = abs(
            outer_inverse_mellins[theta_exponent]
            - expected_outer_inverse
        )
        if outer_delta_free_error > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    eta_exponent,
                    nu_exponent,
                    theta_exponent,
                    "outer_delta_free_form",
                    outer_inverse_mellins[theta_exponent],
                    expected_outer_inverse,
                )
            )
        expected_pair_term = (
            pair_constant
            * theta[(-8) % p]
            * filtered_outer
            * square_jacobi
            * filtered_jacobi
            / p
        )
        pair_term = outer_inverse_mellins[theta_exponent] * paired_phase
        delta_free_error = abs(pair_term - expected_pair_term)
        max_delta_free_pair_error = max(
            max_delta_free_pair_error,
            delta_free_error,
        )
        if delta_free_error > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    eta_exponent,
                    nu_exponent,
                    theta_exponent,
                    "delta_free_pair_term",
                    pair_term,
                    expected_pair_term,
                )
            )
        max_paired_phase_ratio = max(max_paired_phase_ratio, abs(paired_phase))
        if abs(paired_phase) > 2 + TOLERANCE:
            raise AssertionError(
                (
                    p,
                    nu_exponent,
                    theta_exponent,
                    "paired_kernel_phase_bound",
                    abs(paired_phase),
                )
            )
        paired_generic_phase_sum += pair_term
        paired_generic_count += 1
    algebraic_pair_terms: List[complex] = []
    algebraic_pair_sum = 0j
    exceptional_algebraic_pair_sum = 0j
    for theta_exponent, theta in enumerate(table):
        alpha_plain = table[(-theta_exponent + nu_exponent) % order]
        filtered_outer = quotient_line_outer_square_filtered_piece(
            p,
            alpha_plain,
            eta,
            gamma,
        )
        square_jacobi = jacobi_sum(
            p,
            table[(-2 * theta_exponent) % order],
            nu,
        )
        filtered_jacobi = quotient_line_kernel_square_filtered_jacobi(
            p,
            theta,
            quadratic,
        )
        algebraic_pair_term = (
            pair_constant
            * theta[(-8) % p]
            * filtered_outer
            * square_jacobi
            * filtered_jacobi
            / p
        )
        algebraic_pair_terms.append(algebraic_pair_term)
        algebraic_pair_sum += algebraic_pair_term
        if not generic_flags[theta_exponent]:
            exceptional_algebraic_pair_sum += algebraic_pair_term
    for theta_exponent, algebraic_pair_term in enumerate(algebraic_pair_terms):
        partner_exponent = (theta_exponent + quadratic_exponent) % order
        orbit_error = abs(
            algebraic_pair_term - algebraic_pair_terms[partner_exponent]
        )
        max_algebraic_pair_orbit_error = max(
            max_algebraic_pair_orbit_error,
            orbit_error,
        )
        if orbit_error > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    eta_exponent,
                    nu_exponent,
                    theta_exponent,
                    "algebraic_pair_orbit",
                    algebraic_pair_term,
                    algebraic_pair_terms[partner_exponent],
                )
            )
    diagonal_pair_sum = (
        pair_constant
        * (p - 1)
        * quotient_line_paired_diagonal_sum(p, eta, nu, gamma)
        / p
    )
    collapsed_h_transform = (
        quotient_line_paired_collapsed_diagonal_sum(p, eta, nu, gamma) / 2
    )
    collapsed_diagonal_pair_sum = (
        pair_constant * (p - 1) * 2 * collapsed_h_transform / p
    )
    collapsed_diagonal_error = abs(
        diagonal_pair_sum - collapsed_diagonal_pair_sum
    )
    max_collapsed_diagonal_error = max(
        max_collapsed_diagonal_error,
        collapsed_diagonal_error,
    )
    if collapsed_diagonal_error > 100 * TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "collapsed_diagonal_expansion",
                diagonal_pair_sum,
                collapsed_diagonal_pair_sum,
            )
        )
    for singular_z in (0, 1, (-2) % p, (-8) % p):
        singular_value = (
            nu[singular_z]
            * (1 - legendre(-2, p) * legendre(singular_z, p))
            * eta[(1 - singular_z) % p]
            * gamma[(singular_z + 2) % p]
            * quotient_line_collapsed_inner_trace(p, singular_z, nu)
        )
        max_collapsed_singular_error = max(
            max_collapsed_singular_error,
            abs(singular_value),
        )
        if abs(singular_value) > TOLERANCE:
            raise AssertionError(
                (
                    p,
                    eta_exponent,
                    nu_exponent,
                    singular_z,
                    "collapsed_singular_zero",
                    singular_value,
                )
            )
    rank_one_plain = quotient_line_outer_standard_piece(p, nu, eta, gamma)
    rank_one_quadratic = quotient_line_outer_standard_piece(
        p,
        table[(nu_exponent + quadratic_exponent) % order],
        eta,
        gamma,
    )
    rank_one_correction = quotient_line_outer_square_filtered_piece(
        p,
        nu,
        eta,
        gamma,
    )
    expected_rank_one_correction = (
        rank_one_plain - legendre(-2, p) * rank_one_quadratic
    )
    rank_one_error = abs(rank_one_correction - expected_rank_one_correction)
    max_collapsed_rank_one_error = max(
        max_collapsed_rank_one_error,
        rank_one_error,
    )
    if rank_one_error > TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "collapsed_rank_one_filter",
                rank_one_correction,
                expected_rank_one_correction,
            )
        )
    max_collapsed_rank_one_piece_ratio = max(
        max_collapsed_rank_one_piece_ratio,
        abs(rank_one_plain) / math.sqrt(p),
        abs(rank_one_quadratic) / math.sqrt(p),
    )
    if (
        abs(rank_one_plain) > 2 * math.sqrt(p) + TOLERANCE
        or abs(rank_one_quadratic) > 2 * math.sqrt(p) + TOLERANCE
    ):
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "collapsed_rank_one_piece_2sqrt",
            )
        )
    max_collapsed_rank_one_ratio = max(
        max_collapsed_rank_one_ratio,
        abs(rank_one_correction) / math.sqrt(p),
    )
    if abs(rank_one_correction) > 4 * math.sqrt(p) + TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "collapsed_rank_one_4sqrt",
                rank_one_correction,
            )
        )
    rank_two_transform = quotient_line_collapsed_rank_two_transform(
        p,
        eta,
        nu,
        gamma,
    )
    rank_two_split_error = abs(
        rank_two_transform - collapsed_h_transform - rank_one_correction
    )
    max_collapsed_rank_two_split_error = max(
        max_collapsed_rank_two_split_error,
        rank_two_split_error,
    )
    if rank_two_split_error > 100 * TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "collapsed_rank_two_split",
                rank_two_transform,
                collapsed_h_transform + rank_one_correction,
            )
        )
    mobius_transform = quotient_line_collapsed_mobius_transform(p, eta, nu)
    mobius_error = abs(rank_two_transform - mobius_transform)
    max_collapsed_rank_two_mobius_error = max(
        max_collapsed_rank_two_mobius_error,
        mobius_error,
    )
    if mobius_error > 100 * TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "collapsed_rank_two_mobius",
                rank_two_transform,
                mobius_transform,
            )
        )
    inverse_two = pow(2, -1, p)
    deleted_error = max(
        abs(quotient_line_collapsed_mobius_kernel(p, inverse_two, nu)),
        abs(
            quotient_line_collapsed_mobius_kernel(
                p,
                (-3 * inverse_two) % p,
                nu,
            )
        ),
    )
    max_collapsed_mobius_deleted_error = max(
        max_collapsed_mobius_deleted_error,
        deleted_error,
    )
    if deleted_error > TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "collapsed_mobius_deleted_points",
                deleted_error,
            )
        )
    max_collapsed_rank_two_ratio = max(
        max_collapsed_rank_two_ratio,
        abs(rank_two_transform) / p,
    )
    max_collapsed_h_ratio = max(
        max_collapsed_h_ratio,
        abs(collapsed_h_transform) / p,
    )
    pair_diagonal_error = abs(algebraic_pair_sum - diagonal_pair_sum)
    max_pair_diagonal_error = max(
        max_pair_diagonal_error,
        pair_diagonal_error,
    )
    if pair_diagonal_error > 100 * TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "paired_diagonal_expansion",
                algebraic_pair_sum,
                diagonal_pair_sum,
            )
        )
    generic_from_diagonal = (
        diagonal_pair_sum - exceptional_algebraic_pair_sum
    ) / 2
    generic_diagonal_error = abs(generic_from_diagonal - generic_phase_sum)
    max_generic_diagonal_error = max(
        max_generic_diagonal_error,
        generic_diagonal_error,
    )
    if generic_diagonal_error > 100 * TOLERANCE:
        raise AssertionError(
            (
                p,
                eta_exponent,
                nu_exponent,
                "generic_diagonal_expansion",
                generic_from_diagonal,
                generic_phase_sum,
            )
        )
    assert_close(
        (p, eta_exponent, nu_exponent, "paired_generic_phase_reconstruction"),
        paired_generic_phase_sum,
        generic_phase_sum,
    )
    assert_close(
        (p, eta_exponent, nu_exponent, "generic_phase_reconstruction"),
        exceptional_contribution + generic_pairing,
        reconstructed_pairing,
    )
    assert_close(
        (p, eta_exponent, nu_exponent, "quotient_spectral_pairing"),
        reconstructed_pairing,
        direct_pairing,
    )
    spectral_nonsplit = (
        eta[(-2) % p] * transformed_inner(p, 2 % p, nu)
        + legendre(-3, p) * reconstructed_pairing
    )
    assert_close(
        (p, eta_exponent, nu_exponent, "quotient_spectral_nonsplit"),
        spectral_nonsplit,
        quotient_line_nonsplit_sum(p, eta, nu),
    )
    return (
        checked,
        max_outer_decomposition_error,
        max_outer_standard_error,
        abs(reconstructed_pairing - direct_pairing),
        max_outer_piece_ratio,
        max_outer_ratio,
        max(outer_energy_error, kernel_energy_error),
        math.sqrt(expected_outer_energy * expected_kernel_energy) / ((p - 1) * p),
        abs(exceptional_contribution) / math.sqrt(p),
        exceptional_count,
        max_generic_phase_error,
        abs(generic_phase_sum) / p,
        generic_count,
        max_outer_quadratic_shift_error,
        max_kernel_pair_phase_error,
        max_delta_free_pair_error,
        max_pair_jacobi_product_error,
        max_outer_square_filter_error,
        max_kernel_square_filter_error,
        max_algebraic_pair_orbit_error,
        max_pair_diagonal_error,
        max_generic_diagonal_error,
        max_collapsed_diagonal_error,
        max_collapsed_singular_error,
        max_collapsed_rank_one_error,
        max_collapsed_rank_one_piece_ratio,
        max_collapsed_rank_one_ratio,
        max_collapsed_rank_two_split_error,
        max_collapsed_rank_two_mobius_error,
        max_collapsed_mobius_deleted_error,
        max_collapsed_rank_two_ratio,
        max_collapsed_h_ratio,
        max_paired_phase_ratio,
        paired_generic_count,
    )


def verify_twisted_line_kernel_moments(
    p: int,
    table: List[List[complex]],
) -> Tuple[int, float, float]:
    delta = least_nonsquare(p)
    checked = 0
    max_first_moment = 0.0
    max_second_moment_error = 0.0
    for nu_exponent in range(1, p - 1):
        nu = table[nu_exponent]
        values = [twisted_line_kernel_trace(p, t, delta, nu) for t in range(p)]
        first_moment = sum(values)
        second_moment = sum(abs(value) ** 2 for value in values)
        max_first_moment = max(max_first_moment, abs(first_moment))
        max_second_moment_error = max(
            max_second_moment_error,
            abs(second_moment - (p * p - 1)),
        )
        if abs(first_moment) > TOLERANCE:
            raise AssertionError((p, nu_exponent, "kernel_first_moment"))
        if abs(second_moment - (p * p - 1)) > TOLERANCE:
            raise AssertionError(
                (p, nu_exponent, "kernel_second_moment", second_moment)
            )
        checked += 1
    return checked, max_first_moment, max_second_moment_error


def core_collision_formula(p: int) -> int:
    return (
        2 * p * p
        - 8 * p
        + 13
        - legendre(-3, p) * p
        + 9 * legendre(-3, p)
        + legendre(-2, p)
    )


def line_support_formula(p: int) -> int:
    return p - 3 - legendre(-3, p)


def open_support_size_formula(p: int) -> int:
    return p * p - 4 * p + 6 + 4 * legendre(-3, p)


def support_size_formula(p: int) -> int:
    return p * p - 3 * p + 3 + 3 * legendre(-3, p)


def open_core_collision_formula(p: int) -> int:
    return core_collision_formula(p) - 3 * (p - 3 - legendre(-3, p))


def x_marginal_size_formula(p: int, x_value: int) -> int:
    x_value %= p
    if x_value == 0:
        return 0
    chi_minus_three = legendre(-3, p)
    if x_value == 1:
        return (1 + chi_minus_three) * (p - 2)
    if x_value == (-2) % p:
        return 1 + (1 + chi_minus_three) * (p - 3)
    return (
        p
        - 2
        - 2 * chi_minus_three
        - legendre((x_value - 1) * (x_value + 3), p)
    )


def x_marginal_second_formula(p: int) -> int:
    chi_minus_three = legendre(-3, p)
    return (
        p**3
        - 3 * p * p
        + 5 * p
        - 19
        + (6 * p - 16) * chi_minus_three
    )


def open_x_marginal_second_formula(p: int) -> int:
    chi_minus_three = legendre(-3, p)
    return (
        p**3
        - 5 * p * p
        + 17 * p
        - 50
        + (10 * p - 36) * chi_minus_three
    )


def open_x_marginal_size_formula(p: int, x_value: int) -> int:
    x_value %= p
    if x_value == 0:
        return 0
    chi_minus_three = legendre(-3, p)
    if x_value == 1:
        return (1 + chi_minus_three) * (p - 2)
    if x_value == (-2) % p:
        return 1 + (1 + chi_minus_three) * (p - 4)
    return (
        p
        - 3
        - 2 * chi_minus_three
        - 2 * legendre((x_value - 1) * (x_value + 3), p)
    )


def v_marginal_size_formula(p: int, v: int) -> int:
    if v % p == 0:
        return 0
    delta = -3 * v * v - 2 * v - 3
    return p - 2 - legendre(delta, p) + int(shape_b(v, p) == 0)


def open_v_marginal_size_formula(p: int, v: int) -> int:
    if v % p == 0:
        return 0
    delta = -3 * v * v - 2 * v - 3
    return (
        p
        - 3
        - legendre(delta, p)
        + 2 * int(shape_b(v, p) == 0)
        + int(v % p == (-1) % p)
    )


def v_marginal_second_formula(p: int) -> int:
    chi_minus_three = legendre(-3, p)
    chi_minus_two = legendre(-2, p)
    return (
        p**3
        - 5 * p * p
        + 11 * p
        - 11
        + (6 * p - 13) * chi_minus_three
        - chi_minus_two
    )


def open_v_marginal_second_formula(p: int) -> int:
    chi_minus_three = legendre(-3, p)
    chi_minus_two = legendre(-2, p)
    chi_minus_one = legendre(-1, p)
    return (
        p**3
        - 7 * p * p
        + 22 * p
        - 28
        + (8 * p - 24) * chi_minus_three
        - chi_minus_two
        - 2 * chi_minus_one
    )


def nonprincipal_core_moment_formula(p: int) -> int:
    chi_minus_three = legendre(-3, p)
    chi_minus_two = legendre(-2, p)
    direct_formula = (
        p**4
        - 8 * p**3
        + 22 * p * p
        - 6 * p
        + 1
        + (-p**3 + 5 * p * p + 4 * p - 2) * chi_minus_three
        + (p * p - p) * chi_minus_two
    )
    orthogonality_formula = (
        (p - 1) * (p - 1) * core_collision_formula(p)
        - (p - 1) * x_marginal_second_formula(p)
        - (p - 1) * v_marginal_second_formula(p)
        + support_size_formula(p) * support_size_formula(p)
    )
    if direct_formula != orthogonality_formula:
        raise AssertionError((p, direct_formula, orthogonality_formula))
    return direct_formula


def nonprincipal_open_moment_formula(p: int) -> int:
    chi_minus_three = legendre(-3, p)
    chi_minus_two = legendre(-2, p)
    chi_minus_one = legendre(-1, p)
    direct_formula = (
        p**4
        - 9 * p**3
        + 23 * p * p
        + 14 * p
        - 4
        + (-p**3 + 4 * p * p + 21 * p) * chi_minus_three
        + (p * p - p) * chi_minus_two
        + (2 * p - 2) * chi_minus_one
    )
    orthogonality_formula = (
        (p - 1) * (p - 1) * open_core_collision_formula(p)
        - (p - 1) * open_x_marginal_second_formula(p)
        - (p - 1) * open_v_marginal_second_formula(p)
        + open_support_size_formula(p) * open_support_size_formula(p)
    )
    if direct_formula != orthogonality_formula:
        raise AssertionError((p, direct_formula, orthogonality_formula))
    return direct_formula


def nonprincipal_line_moment_formula(p: int) -> int:
    chi_minus_three = legendre(-3, p)
    return (
        p**3
        - 7 * p * p
        + 14 * p
        - 3
        + (-p * p + 3 * p + 2) * chi_minus_three
    )


def nonprincipal_core_line_cross_formula(p: int) -> int:
    chi_minus_three = legendre(-3, p)
    chi_minus_one = legendre(-1, p)
    return (
        p**3
        - 4 * p * p
        - 3 * p
        + 1
        - 7 * p * chi_minus_three
        + (1 - p) * chi_minus_one
    )


def split_projector_weight(p: int, y: int) -> int:
    chi_discriminant = legendre((y - 2) * (y + 1), p)
    return 1 + chi_discriminant - int(y % p == 3 % p)


def nonsplit_projector_weight(p: int, y: int) -> int:
    chi_discriminant = legendre((y - 2) * (y + 1), p)
    return 1 - chi_discriminant


def projector_v_support_count(p: int, y: int) -> int:
    return sum(1 for v in range(1, p) if q_y_v(y, v, p) != 0)


def projector_v_support_formula(p: int, y: int) -> int:
    chi_discriminant = legendre((y - 2) * (y + 1), p)
    zero_root_correction = int(y % p == (-1) % p) + int(y % p == 3 % p)
    return p - 2 - chi_discriminant + zero_root_correction


def projector_collision_sums(p: int) -> Tuple[int, int, int]:
    split_sum = 0
    nonsplit_sum = 0
    cross_sum = 0
    for y in range(1, p):
        direct_support = projector_v_support_count(p, y)
        expected_support = projector_v_support_formula(p, y)
        if direct_support != expected_support:
            raise AssertionError((p, y, direct_support, expected_support))
        split_weight = split_projector_weight(p, y)
        nonsplit_weight = nonsplit_projector_weight(p, y)
        split_sum += split_weight * split_weight * direct_support
        nonsplit_sum += nonsplit_weight * nonsplit_weight * direct_support
        cross_sum += split_weight * nonsplit_weight * direct_support
    return split_sum, nonsplit_sum, cross_sum


def projector_collision_formulas(p: int) -> Tuple[int, int, int]:
    chi_minus_two = legendre(-2, p)
    split_sum = 2 * p * p - 15 * p + 31 - 2 * (p - 3) * chi_minus_two
    nonsplit_sum = 2 * p * p - 4 * p + 1 + 2 * (p - 1) * chi_minus_two
    cross_sum = 2 * p - 3
    return split_sum, nonsplit_sum, cross_sum


def principal_eta_row_formula(p: int, nu: List[complex]) -> complex:
    delta_sum = sum(
        nu[v] * legendre(-3 * v * v - 2 * v - 3, p) for v in range(p)
    )
    collision_sum = sum(nu[v] for v in range(p) if shape_b(v, p) == 0)
    return -delta_sum + collision_sum


def principal_nu_row_formula(p: int, eta: List[complex]) -> complex:
    conic_sum = sum(
        eta[x] * legendre((x - 1) * (x + 3), p) for x in range(p)
    )
    exceptional = legendre(-3, p) * p * (eta[1] + eta[(-2) % p])
    return -conic_sum + exceptional


def verify_principal_rows(p: int) -> None:
    logs = log_table(p)
    table = character_table(p, logs)
    principal = table[0]
    for nu_exponent in range(1, p - 1):
        actual = direct_core(p, principal, table[nu_exponent], principal)
        expected = principal_eta_row_formula(p, table[nu_exponent])
        assert_close((p, nu_exponent, "eta_principal_row"), actual, expected)
    for eta_exponent in range(1, p - 1):
        eta = table[eta_exponent]
        eta_inv = table[(-eta_exponent) % (p - 1)]
        actual = direct_core(p, eta_inv, principal, eta)
        expected = principal_nu_row_formula(p, eta)
        assert_close((p, eta_exponent, "nu_principal_row"), actual, expected)
    principal_principal = direct_core(p, principal, principal, principal)
    assert_close(
        (p, "principal_principal_row"),
        principal_principal,
        complex(support_size_formula(p), 0),
    )


def admissible_filter_formula(e: int) -> int:
    return (
        (e - 1) * (e - 5)
        + (3 if e % 2 == 0 else 0)
        + 2 * (math.gcd(e, 3) - 1)
    )


def direct_admissible_filter_count(e: int) -> int:
    count = 0
    for a in range(1, e):
        eta_exponent = (-a) % e
        if eta_exponent == 0:
            raise AssertionError((e, a, "eta principal"))
        for b in range(1, e):
            line_exponents = (a % e, b % e, (a - b) % e)
            if any(exponent == 0 for exponent in line_exponents):
                continue
            has_equal_pair = len(set(line_exponents)) != 3
            has_reciprocal_pair = any(
                (line_exponents[i] + line_exponents[j]) % e == 0
                for i in range(3)
                for j in range(i + 1, 3)
            )
            direct_filter = (
                b % e != a % e
                and b % e != (-a) % e
                and b % e != (2 * a) % e
                and (2 * b) % e != a % e
            )
            if direct_filter != (not has_equal_pair and not has_reciprocal_pair):
                raise AssertionError((e, a, b, line_exponents, direct_filter))
            other_resonances = (
                (b - a) % e == 0
                or ((a - b) - a) % e == 0
            )
            if direct_filter and other_resonances:
                raise AssertionError((e, a, b, "extra resonance"))
            count += int(direct_filter)
    return count


def verify_admissible_twist_nontriviality() -> List[Tuple[int, int]]:
    checked: List[Tuple[int, int]] = []
    for e in FILTER_ORDERS:
        count = 0
        for a in range(1, e):
            eta_exponent = (-a) % e
            for b in range(1, e):
                direct_filter = (
                    b % e != a % e
                    and b % e != (-a) % e
                    and b % e != (2 * a) % e
                    and (2 * b) % e != a % e
                )
                if not direct_filter:
                    continue
                nu_exponent = b % e
                eta_nu_exponent = (b - a) % e
                if eta_exponent == 0 or nu_exponent == 0 or eta_nu_exponent == 0:
                    raise AssertionError(
                        (
                            e,
                            a,
                            b,
                            eta_exponent,
                            nu_exponent,
                            eta_nu_exponent,
                        )
                    )
                count += 1
        expected_count = admissible_filter_formula(e)
        if count != expected_count:
            raise AssertionError((e, count, expected_count))
        checked.append((e, count))
    return checked


def verify_admissible_filter_counts() -> List[Tuple[int, int]]:
    checked: List[Tuple[int, int]] = []
    for e in FILTER_ORDERS:
        direct_count = direct_admissible_filter_count(e)
        expected_count = admissible_filter_formula(e)
        if direct_count != expected_count:
            raise AssertionError((e, direct_count, expected_count))
        checked.append((e, expected_count))
    return checked


def direct_core_collision_count(p: int) -> int:
    total = 0
    for v in range(1, p):
        values: Dict[int, int] = {}
        for u in range(1, p):
            a_value = shape_a(u, v, p)
            if a_value == 0:
                continue
            key = a_value * pow(u, -1, p) % p
            values[key] = values.get(key, 0) + 1
        total += sum(count * count for count in values.values())
    return total


def direct_line_support_count(p: int) -> int:
    count = 0
    for u in range(p):
        v = (-1 - u) % p
        if u == 0 or v == 0 or shape_a(u, v, p) == 0:
            continue
        count += 1
    return count


def direct_support_marginal_counts(p: int) -> Tuple[int, int, int]:
    x_counts: Dict[int, int] = {}
    v_counts: Dict[int, int] = {}
    for u in range(1, p):
        inverse_u = pow(u, -1, p)
        for v in range(1, p):
            a_value = shape_a(u, v, p)
            if a_value == 0:
                continue
            x_value = a_value * inverse_u % p
            x_counts[x_value] = x_counts.get(x_value, 0) + 1
            v_counts[v] = v_counts.get(v, 0) + 1
    for x_value in range(1, p):
        actual = x_counts.get(x_value, 0)
        expected = x_marginal_size_formula(p, x_value)
        if actual != expected:
            raise AssertionError((p, "x_marginal", x_value, actual, expected))
    for v in range(1, p):
        actual = v_counts.get(v, 0)
        expected = v_marginal_size_formula(p, v)
        if actual != expected:
            raise AssertionError((p, "v_marginal", v, actual, expected))
    support_count = sum(x_counts.values())
    x_second = sum(count * count for count in x_counts.values())
    v_second = sum(count * count for count in v_counts.values())
    return support_count, x_second, v_second


def direct_open_support_marginal_counts(p: int) -> Tuple[int, int, int, int]:
    x_counts: Dict[int, int] = {}
    v_counts: Dict[int, int] = {}
    xv_counts: Dict[Tuple[int, int], int] = {}
    for u in range(1, p):
        inverse_u = pow(u, -1, p)
        for v in range(1, p):
            if (-1 - u - v) % p == 0:
                continue
            a_value = shape_a(u, v, p)
            if a_value == 0:
                continue
            x_value = a_value * inverse_u % p
            x_counts[x_value] = x_counts.get(x_value, 0) + 1
            v_counts[v] = v_counts.get(v, 0) + 1
            xv_counts[(x_value, v)] = xv_counts.get((x_value, v), 0) + 1
    for x_value in range(1, p):
        actual = x_counts.get(x_value, 0)
        expected = open_x_marginal_size_formula(p, x_value)
        if actual != expected:
            raise AssertionError(
                (p, "open_x_marginal", x_value, actual, expected)
            )
    for v in range(1, p):
        actual = v_counts.get(v, 0)
        expected = open_v_marginal_size_formula(p, v)
        if actual != expected:
            raise AssertionError((p, "open_v_marginal", v, actual, expected))
    support_count = sum(x_counts.values())
    collision_count = sum(count * count for count in xv_counts.values())
    x_second = sum(count * count for count in x_counts.values())
    v_second = sum(count * count for count in v_counts.values())
    return support_count, collision_count, x_second, v_second


def direct_full_character_moments(
    p: int,
) -> Tuple[int, int, int, int, int, int]:
    logs = log_table(p)
    table = character_table(p, logs)
    core_moment = 0.0
    nonprincipal_core_moment = 0.0
    nonprincipal_open_moment = 0.0
    nonprincipal_line_moment = 0.0
    nonprincipal_core_line_cross = 0j
    line_moment = 0.0
    for eta_exponent in range(p - 1):
        eta = table[eta_exponent]
        eta_inv = table[(-eta_exponent) % (p - 1)]
        for nu_exponent in range(p - 1):
            nu = table[nu_exponent]
            core_sum = direct_core(p, eta_inv, nu, eta)
            core_value = abs(core_sum) ** 2
            core_moment += core_value
            line_value = line_correction(p, eta_inv, nu, eta)
            if eta_exponent != 0 and nu_exponent != 0:
                nonprincipal_core_moment += core_value
                nonprincipal_open_moment += (
                    abs(direct_open(p, eta_inv, nu, eta)) ** 2
                )
                nonprincipal_line_moment += abs(line_value) ** 2
                nonprincipal_core_line_cross += core_sum * line_value.conjugate()
            line_moment += abs(line_value) ** 2
    if abs(nonprincipal_core_line_cross.imag) > 100 * TOLERANCE:
        raise AssertionError((p, "nonprincipal_cross_imag"))
    return (
        round(core_moment),
        round(line_moment),
        round(nonprincipal_core_moment),
        round(nonprincipal_open_moment),
        round(nonprincipal_line_moment),
        round(nonprincipal_core_line_cross.real),
    )


def direct_full_character_projector_moments(p: int) -> Tuple[int, int, int]:
    logs = log_table(p)
    table = character_table(p, logs)
    split_moment = 0.0
    nonsplit_moment = 0.0
    cross_moment = 0j
    for eta_exponent in range(p - 1):
        eta = table[eta_exponent]
        for nu_exponent in range(p - 1):
            nu = table[nu_exponent]
            split_value = split_projected_core(p, eta, nu)
            nonsplit_value = nonsplit_projected_core(p, eta, nu)
            split_moment += abs(split_value) ** 2
            nonsplit_moment += abs(nonsplit_value) ** 2
            cross_moment += nonsplit_value * split_value.conjugate()
    if abs(cross_moment.imag) > 100 * TOLERANCE:
        raise AssertionError((p, "projector_cross_imag", cross_moment))
    return round(split_moment), round(nonsplit_moment), round(cross_moment.real)


def verify_admissible_open_moment_audit() -> List[
    Tuple[int, int, float, float, float, Tuple[int, int], float]
]:
    checked: List[
        Tuple[int, int, float, float, float, Tuple[int, int], float]
    ] = []
    for p in ADMISSIBLE_OPEN_AUDIT_PRIMES:
        table = character_table(p, log_table(p))
        order = p - 1
        total = 0.0
        l1_total = 0.0
        count = 0
        max_ratio = 0.0
        max_label = (0, 0)
        for eta_exponent in range(1, order):
            eta = table[eta_exponent]
            eta_inv = table[(-eta_exponent) % order]
            for nu_exponent in range(1, order):
                if not is_line_conic_admissible_pair(
                    order,
                    eta_exponent,
                    nu_exponent,
                ):
                    continue
                nu = table[nu_exponent]
                value = direct_open(p, eta_inv, nu, eta)
                total += abs(value) ** 2
                l1_total += abs(value)
                count += 1
                ratio = abs(value) / p
                if ratio > max_ratio:
                    max_ratio = ratio
                    max_label = (eta_exponent, nu_exponent)
        expected_count = admissible_filter_formula(order)
        if count != expected_count:
            raise AssertionError((p, count, expected_count))
        inherited_bound = nonprincipal_open_moment_formula(p)
        if total > inherited_bound + 100 * TOLERANCE:
            raise AssertionError((p, total, inherited_bound))
        cauchy_l1_bound = math.sqrt(count * inherited_bound)
        if l1_total > cauchy_l1_bound + 100 * TOLERANCE:
            raise AssertionError((p, l1_total, cauchy_l1_bound))
        checked.append(
            (
                p,
                count,
                round(math.sqrt(total / count) / p, 10),
                round(l1_total / (count * p), 10),
                round(max_ratio, 10),
                max_label,
                round(math.sqrt(inherited_bound / count) / p, 10),
            )
        )
    return checked


def verify_admissible_suborder_transfer_thresholds() -> List[
    Tuple[int, int, Tuple[Tuple[int, int], ...]]
]:
    checked: List[Tuple[int, int, Tuple[Tuple[int, int], ...]]] = []
    for p in ADMISSIBLE_OPEN_AUDIT_PRIMES:
        order = p - 1
        moment_bound = nonprincipal_open_moment_formula(p)
        thresholds: List[Tuple[int, int]] = []
        for constant in ADMISSIBLE_TRANSFER_CONSTANTS:
            possible_orders = [
                suborder
                for suborder in range(2, order + 1)
                if order % suborder == 0
                and admissible_filter_formula(suborder) > 0
                and moment_bound
                <= constant * constant * p * p
                * admissible_filter_formula(suborder)
            ]
            thresholds.append(
                (constant, min(possible_orders) if possible_orders else 0)
            )
        full_order_bound = thresholds[-1][1]
        if full_order_bound == 0:
            raise AssertionError((p, thresholds))
        checked.append(
            (
                p,
                admissible_filter_formula(order),
                tuple(thresholds),
            )
        )
    return checked


def verify_admissible_suborder_moment_audit() -> List[
    Tuple[int, int, int, float, float, float, float]
]:
    checked: List[Tuple[int, int, int, float, float, float, float]] = []
    for p in ADMISSIBLE_OPEN_AUDIT_PRIMES:
        table = character_table(p, log_table(p))
        order = p - 1
        inherited_bound = nonprincipal_open_moment_formula(p)
        for suborder in range(2, order + 1):
            if order % suborder != 0:
                continue
            expected_count = admissible_filter_formula(suborder)
            if expected_count == 0:
                continue
            lift = order // suborder
            total = 0.0
            l1_total = 0.0
            count = 0
            max_ratio = 0.0
            for eta_subexponent in range(1, suborder):
                eta_exponent = lift * eta_subexponent
                eta = table[eta_exponent]
                eta_inv = table[(-eta_exponent) % order]
                for nu_subexponent in range(1, suborder):
                    if not is_line_conic_admissible_pair(
                        suborder,
                        eta_subexponent,
                        nu_subexponent,
                    ):
                        continue
                    nu_exponent = lift * nu_subexponent
                    value = direct_open(p, eta_inv, table[nu_exponent], eta)
                    value_abs = abs(value)
                    total += value_abs * value_abs
                    l1_total += value_abs
                    count += 1
                    max_ratio = max(max_ratio, value_abs / p)
            if count != expected_count:
                raise AssertionError((p, suborder, count, expected_count))
            if l1_total > math.sqrt(count * inherited_bound) + 100 * TOLERANCE:
                raise AssertionError((p, suborder, l1_total, inherited_bound))
            checked.append(
                (
                    p,
                    suborder,
                    count,
                    round(math.sqrt(total / count) / p, 10),
                    round(l1_total / (count * p), 10),
                    round(max_ratio, 10),
                    round(math.sqrt(inherited_bound / count) / p, 10),
                )
            )
    return checked


def open_suborder_coset_moment(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> Tuple[int, int, int, int, int]:
    joint_counts: Dict[Tuple[int, int], int] = {}
    x_counts: Dict[int, int] = {}
    v_counts: Dict[int, int] = {}
    support_count = 0
    for u in range(1, p):
        inverse_u = pow(u, -1, p)
        for v in range(1, p):
            if (-1 - u - v) % p == 0:
                continue
            a_value = shape_a(u, v, p)
            if a_value == 0:
                continue
            x_class = logs[a_value * inverse_u % p] % suborder
            v_class = logs[v] % suborder
            joint_counts[(x_class, v_class)] = (
                joint_counts.get((x_class, v_class), 0) + 1
            )
            x_counts[x_class] = x_counts.get(x_class, 0) + 1
            v_counts[v_class] = v_counts.get(v_class, 0) + 1
            support_count += 1
    joint_energy = sum(count * count for count in joint_counts.values())
    x_energy = sum(count * count for count in x_counts.values())
    v_energy = sum(count * count for count in v_counts.values())
    moment = (
        suborder * suborder * joint_energy
        - suborder * (x_energy + v_energy)
        + support_count * support_count
    )
    return support_count, joint_energy, x_energy, v_energy, moment


def is_open_support_point(p: int, u: int, v: int) -> bool:
    return (
        u % p != 0
        and v % p != 0
        and (-1 - u - v) % p != 0
        and shape_a(u, v, p) != 0
    )


def ratio_surface_joint_energy(p: int, suborder: int) -> int:
    logs = log_table(p)
    kernel = [value for value in range(1, p) if logs[value] % suborder == 0]
    total = 0
    for alpha in kernel:
        for beta in kernel:
            for ratio in range(1, p):
                for u in range(1, p):
                    ratio_u = ratio * u % p
                    for v in range(1, p):
                        beta_v = beta * v % p
                        equation = (
                            ratio * (ratio - alpha) * u * u
                            + ratio
                            * ((beta - alpha) * v + (1 - alpha))
                            * u
                            + shape_b(beta_v, p)
                            - alpha * ratio * shape_b(v, p)
                        ) % p
                        if equation != 0:
                            continue
                        if not is_open_support_point(p, u, v):
                            continue
                        if not is_open_support_point(p, ratio_u, beta_v):
                            continue
                        total += 1
    return total


def verify_ratio_surface_joint_energy() -> List[Tuple[int, int, int]]:
    checked: List[Tuple[int, int, int]] = []
    for p, suborder in RATIO_SURFACE_CASES:
        logs = log_table(p)
        _, joint_energy, _, _, _ = open_suborder_coset_moment(p, suborder, logs)
        surface_energy = ratio_surface_joint_energy(p, suborder)
        if surface_energy != joint_energy:
            raise AssertionError((p, suborder, surface_energy, joint_energy))
        checked.append((p, suborder, joint_energy))
    return checked


def ratio_surface_conic_coefficients(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> Tuple[int, int, int, int, int, int]:
    return (
        ratio * (ratio - alpha) % p,
        ratio * (beta - alpha) % p,
        (beta * beta - alpha * ratio) % p,
        ratio * (1 - alpha) % p,
        (beta - alpha * ratio) % p,
        (1 - alpha * ratio) % p,
    )


def ratio_surface_delta(p: int, alpha: int, beta: int, ratio: int) -> int:
    a = alpha
    b = beta
    r = ratio
    return (
        -2 * a * a * a * r * r
        + 3 * a * a * b * b * r
        - a * a * b * r * r
        - a * a * b * r
        + 3 * a * a * r * r * r
        - a * a * r * r
        + 3 * a * a * r
        - 3 * a * b * b * r * r
        + a * b * b * r
        - 3 * a * b * b
        + a * b * r * r
        + a * b * r
        - 3 * a * r * r
        + 2 * b * b * r
    ) % p


def ratio_surface_delta_cubic_coefficients(
    p: int,
    alpha: int,
    beta: int,
) -> Tuple[int, int, int, int]:
    a = alpha
    b = beta
    return (
        3 * a * a % p,
        a * (-2 * a * a - a * b - a - 3 * b * b + b - 3) % p,
        (
            3 * a * a * b * b
            - a * a * b
            + 3 * a * a
            + a * b * b
            + a * b
            + 2 * b * b
        )
        % p,
        -3 * a * b * b % p,
    )


def ratio_surface_doubled_projective_determinant(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> int:
    uu, uv, vv, u_linear, v_linear, constant = (
        ratio_surface_conic_coefficients(p, alpha, beta, ratio)
    )
    return (
        (2 * uu) * ((2 * vv) * (2 * constant) - v_linear * v_linear)
        - uv * (uv * (2 * constant) - v_linear * u_linear)
        + u_linear * (uv * v_linear - (2 * vv) * u_linear)
    ) % p


def verify_ratio_surface_degeneracy() -> List[
    Tuple[int, int, int, int, int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int, int, int, int, int]] = []
    for p, suborder in RATIO_SURFACE_CASES:
        logs = log_table(p)
        kernel = [value for value in range(1, p) if logs[value] % suborder == 0]
        parameter_count = 0
        degenerate_count = 0
        zero_conic_count = 0
        for alpha in kernel:
            for beta in kernel:
                cubic_coefficients = ratio_surface_delta_cubic_coefficients(
                    p,
                    alpha,
                    beta,
                )
                if cubic_coefficients[0] == 0:
                    raise AssertionError((p, suborder, alpha, beta, "zero-leading"))
                for ratio in range(1, p):
                    parameter_count += 1
                    cubic_value = (
                        cubic_coefficients[0] * ratio * ratio * ratio
                        + cubic_coefficients[1] * ratio * ratio
                        + cubic_coefficients[2] * ratio
                        + cubic_coefficients[3]
                    ) % p
                    delta_value = ratio_surface_delta(p, alpha, beta, ratio)
                    if cubic_value != delta_value:
                        raise AssertionError(
                            (
                                p,
                                suborder,
                                alpha,
                                beta,
                                ratio,
                                cubic_value,
                                delta_value,
                            )
                        )
                    coefficients = ratio_surface_conic_coefficients(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    if all(coefficient == 0 for coefficient in coefficients):
                        zero_conic_count += 1
                        if (alpha, beta, ratio) != (1, 1, 1):
                            raise AssertionError(
                                (p, suborder, alpha, beta, ratio, "zero-conic")
                            )
                    determinant = ratio_surface_doubled_projective_determinant(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    expected = (
                        2 * ratio * ratio_surface_delta(p, alpha, beta, ratio)
                    ) % p
                    if determinant != expected:
                        raise AssertionError(
                            (p, suborder, alpha, beta, ratio, determinant, expected)
                        )
                    if determinant == 0:
                        degenerate_count += 1
        degenerate_bound = 3 * len(kernel) * len(kernel)
        if zero_conic_count != 1:
            raise AssertionError((p, suborder, zero_conic_count))
        if degenerate_count > degenerate_bound:
            raise AssertionError((p, suborder, degenerate_count, degenerate_bound))
        support_count, joint_energy, _, _, _ = open_suborder_coset_moment(
            p,
            suborder,
            logs,
        )
        conic_bound = (
            support_count
            + (parameter_count - degenerate_count) * (p + 1)
            + (degenerate_count - 1) * (2 * p + 1)
        )
        uniform_bound = (
            support_count
            + (parameter_count - 1) * (p + 1)
            + (degenerate_bound - 1) * p
        )
        if joint_energy > conic_bound:
            raise AssertionError((p, suborder, joint_energy, conic_bound))
        if conic_bound > uniform_bound:
            raise AssertionError((p, suborder, conic_bound, uniform_bound))
        checked.append(
            (
                p,
                suborder,
                parameter_count,
                degenerate_count,
                zero_conic_count,
                degenerate_bound,
                joint_energy,
                conic_bound,
                uniform_bound,
            )
        )
    return checked


def direct_suborder_nonprincipal_open_moment(
    p: int,
    suborder: int,
    table: List[List[complex]],
) -> int:
    order = p - 1
    lift = order // suborder
    total = 0.0
    for eta_subexponent in range(1, suborder):
        eta_exponent = lift * eta_subexponent
        eta = table[eta_exponent]
        eta_inv = table[(-eta_exponent) % order]
        for nu_subexponent in range(1, suborder):
            nu_exponent = lift * nu_subexponent
            total += abs(direct_open(p, eta_inv, table[nu_exponent], eta)) ** 2
    return round(total)


def verify_suborder_parseval_open_moments() -> List[
    Tuple[int, int, int, int, float, float, float, float]
]:
    checked: List[Tuple[int, int, int, int, float, float, float, float]] = []
    for p in ADMISSIBLE_OPEN_AUDIT_PRIMES:
        logs = log_table(p)
        table = character_table(p, logs)
        order = p - 1
        full_moment_bound = nonprincipal_open_moment_formula(p)
        for suborder in range(2, order + 1):
            if order % suborder != 0:
                continue
            admissible_count = admissible_filter_formula(suborder)
            if admissible_count == 0:
                continue
            (
                support_count,
                joint_energy,
                x_energy,
                v_energy,
                moment,
            ) = open_suborder_coset_moment(p, suborder, logs)
            expected_support = open_support_size_formula(p)
            if support_count != expected_support:
                raise AssertionError((p, suborder, support_count, expected_support))
            direct_moment = direct_suborder_nonprincipal_open_moment(
                p,
                suborder,
                table,
            )
            if moment != direct_moment:
                raise AssertionError((p, suborder, moment, direct_moment))
            if moment > full_moment_bound:
                raise AssertionError((p, suborder, moment, full_moment_bound))
            all_nonprincipal_count = (suborder - 1) * (suborder - 1)
            checked.append(
                (
                    p,
                    suborder,
                    admissible_count,
                    moment,
                    round(math.sqrt(moment) / (suborder * p), 10),
                    round(math.sqrt(moment / all_nonprincipal_count) / p, 10),
                    round(math.sqrt(moment / admissible_count) / p, 10),
                    round(math.sqrt(full_moment_bound / admissible_count) / p, 10),
                )
            )
            if joint_energy <= 0 or x_energy <= 0 or v_energy <= 0:
                raise AssertionError((p, suborder, joint_energy, x_energy, v_energy))
    return checked


def verify_second_moments() -> List[
    Tuple[int, int, int, int, int, int, int, int, int, int, int]
]:
    checked: List[
        Tuple[int, int, int, int, int, int, int, int, int, int, int]
    ] = []
    for p in MOMENT_PRIMES:
        collision_count = direct_core_collision_count(p)
        expected_collision_count = core_collision_formula(p)
        if collision_count != expected_collision_count:
            raise AssertionError((p, collision_count, expected_collision_count))
        projector_sums = projector_collision_sums(p)
        expected_projector_sums = projector_collision_formulas(p)
        if projector_sums != expected_projector_sums:
            raise AssertionError((p, projector_sums, expected_projector_sums))
        line_support_count = direct_line_support_count(p)
        expected_line_support_count = line_support_formula(p)
        if line_support_count != expected_line_support_count:
            raise AssertionError((p, line_support_count, expected_line_support_count))
        support_count, x_second, v_second = direct_support_marginal_counts(p)
        expected_support_count = support_size_formula(p)
        if support_count != expected_support_count:
            raise AssertionError((p, support_count, expected_support_count))
        expected_x_second = x_marginal_second_formula(p)
        expected_v_second = v_marginal_second_formula(p)
        if x_second != expected_x_second:
            raise AssertionError((p, "x_second", x_second, expected_x_second))
        if v_second != expected_v_second:
            raise AssertionError((p, "v_second", v_second, expected_v_second))
        (
            open_support_count,
            open_collision_count,
            open_x_second,
            open_v_second,
        ) = direct_open_support_marginal_counts(p)
        expected_open_support_count = open_support_size_formula(p)
        expected_open_collision_count = open_core_collision_formula(p)
        expected_open_x_second = open_x_marginal_second_formula(p)
        expected_open_v_second = open_v_marginal_second_formula(p)
        if open_support_count != expected_open_support_count:
            raise AssertionError(
                (p, "open_support", open_support_count, expected_open_support_count)
            )
        if open_collision_count != expected_open_collision_count:
            raise AssertionError(
                (
                    p,
                    "open_collision",
                    open_collision_count,
                    expected_open_collision_count,
                )
            )
        if open_x_second != expected_open_x_second:
            raise AssertionError(
                (p, "open_x_second", open_x_second, expected_open_x_second)
            )
        if open_v_second != expected_open_v_second:
            raise AssertionError(
                (p, "open_v_second", open_v_second, expected_open_v_second)
            )
        (
            core_moment,
            line_moment,
            nonprincipal_moment,
            nonprincipal_open_moment,
            nonprincipal_line_moment,
            nonprincipal_core_line_cross,
        ) = direct_full_character_moments(p)
        expected_core_moment = (p - 1) * (p - 1) * expected_collision_count
        expected_line_moment = (p - 1) * (p - 1) * expected_line_support_count
        expected_nonprincipal_moment = nonprincipal_core_moment_formula(p)
        expected_nonprincipal_open_moment = nonprincipal_open_moment_formula(p)
        expected_nonprincipal_line_moment = nonprincipal_line_moment_formula(p)
        expected_nonprincipal_cross = nonprincipal_core_line_cross_formula(p)
        if core_moment != expected_core_moment:
            raise AssertionError((p, core_moment, expected_core_moment))
        if line_moment != expected_line_moment:
            raise AssertionError((p, line_moment, expected_line_moment))
        if nonprincipal_moment != expected_nonprincipal_moment:
            raise AssertionError(
                (p, nonprincipal_moment, expected_nonprincipal_moment)
            )
        if nonprincipal_open_moment != expected_nonprincipal_open_moment:
            raise AssertionError(
                (
                    p,
                    nonprincipal_open_moment,
                    expected_nonprincipal_open_moment,
                )
            )
        if nonprincipal_line_moment != expected_nonprincipal_line_moment:
            raise AssertionError(
                (
                    p,
                    nonprincipal_line_moment,
                    expected_nonprincipal_line_moment,
                )
            )
        if nonprincipal_core_line_cross != expected_nonprincipal_cross:
            raise AssertionError(
                (
                    p,
                    nonprincipal_core_line_cross,
                    expected_nonprincipal_cross,
                )
            )
        (
            split_projector_moment,
            nonsplit_projector_moment,
            projector_cross_moment,
        ) = direct_full_character_projector_moments(p)
        expected_split_moment = (p - 1) * (p - 1) * expected_projector_sums[0]
        expected_nonsplit_moment = (p - 1) * (p - 1) * expected_projector_sums[1]
        expected_projector_cross = (p - 1) * (p - 1) * expected_projector_sums[2]
        if split_projector_moment != expected_split_moment:
            raise AssertionError(
                (p, split_projector_moment, expected_split_moment)
            )
        if nonsplit_projector_moment != expected_nonsplit_moment:
            raise AssertionError(
                (p, nonsplit_projector_moment, expected_nonsplit_moment)
            )
        if projector_cross_moment != expected_projector_cross:
            raise AssertionError(
                (p, projector_cross_moment, expected_projector_cross)
            )
        verify_principal_rows(p)
        checked.append(
            (
                p,
                expected_collision_count,
                expected_line_support_count,
                expected_nonprincipal_moment,
                expected_open_collision_count,
                expected_nonprincipal_open_moment,
                expected_nonprincipal_line_moment,
                expected_nonprincipal_cross,
                expected_projector_sums[0],
                expected_projector_sums[1],
                expected_projector_sums[2],
            )
        )
    return checked


def main() -> None:
    tables: Dict[int, List[List[complex]]] = {}
    checked_cases = 0
    checked_fibers = 0
    checked_open_decompositions = 0
    max_difference = 0.0
    max_pullback_difference = 0.0
    max_twisted_difference = 0.0
    max_twisted_line_difference = 0.0
    max_quotient_line_difference = 0.0
    max_quotient_spectral_difference = 0.0
    max_outer_mellin_decomposition_error = 0.0
    max_outer_standard_error = 0.0
    max_outer_quadratic_shift_error = 0.0
    max_kernel_pair_phase_error = 0.0
    max_delta_free_pair_error = 0.0
    max_pair_jacobi_product_error = 0.0
    max_outer_square_filter_error = 0.0
    max_kernel_square_filter_error = 0.0
    max_algebraic_pair_orbit_error = 0.0
    max_pair_diagonal_error = 0.0
    max_generic_diagonal_error = 0.0
    max_collapsed_diagonal_error = 0.0
    max_collapsed_singular_error = 0.0
    max_collapsed_rank_one_error = 0.0
    max_collapsed_rank_one_piece_ratio = 0.0
    max_collapsed_rank_one_ratio = 0.0
    max_collapsed_rank_two_split_error = 0.0
    max_collapsed_rank_two_mobius_error = 0.0
    max_collapsed_mobius_deleted_error = 0.0
    max_collapsed_rank_two_ratio = 0.0
    max_collapsed_h_ratio = 0.0
    max_paired_phase_ratio = 0.0
    max_outer_mellin_piece_ratio = 0.0
    max_outer_mellin_ratio = 0.0
    max_spectral_energy_error = 0.0
    max_spectral_cauchy_ratio = 0.0
    max_exceptional_spectral_ratio = 0.0
    max_generic_phase_error = 0.0
    max_generic_phase_sum_ratio = 0.0
    exceptional_theta_checked = 0
    generic_theta_checked = 0
    paired_generic_theta_checked = 0
    max_core_ratio = 0.0
    max_open_ratio = 0.0
    max_line_ratio = 0.0
    max_split_projection_ratio = 0.0
    max_nonsplit_projection_ratio = 0.0
    max_nonsplit_singular_ratio = 0.0
    max_core_label: Tuple[object, ...] = ()
    max_open_label: Tuple[object, ...] = ()
    max_line_label: Tuple[object, ...] = ()
    max_split_projection_label: Tuple[object, ...] = ()
    max_nonsplit_projection_label: Tuple[object, ...] = ()
    max_nonsplit_singular_label: Tuple[object, ...] = ()
    max_collapsed_rank_two_label: Tuple[object, ...] = ()
    max_collapsed_h_label: Tuple[object, ...] = ()
    singular_checked: List[int] = []
    lambda_map_checked = 0
    lambda_twist_checked: List[Tuple[int, int, int]] = []
    twisted_discriminant_checked: List[Tuple[int, int, int]] = []
    twisted_line_twist_checked: List[Tuple[int, int, int, int, int]] = []
    twisted_line_deck_checked: List[Tuple[int, int, float, float, float]] = []
    quotient_line_checked: List[Tuple[int, int, float, int, int]] = []
    quotient_line_kernel_moment_checked: List[Tuple[int, int, float, float]] = []
    quotient_line_mellin_checked: List[Tuple[int, int, float, float]] = []
    quotient_line_mellin_magnitude_checked: List[
        Tuple[int, int, float, int, int, int]
    ] = []
    collapsed_inner_spectrum_checked: List[
        Tuple[int, int, float, float, float, float, float, float, int, int, int]
    ] = []
    collapsed_mobius_energy_checked: List[
        Tuple[
            int,
            int,
            int,
            float,
            float,
            float,
            float,
            float,
            float,
            float,
            float,
            float,
            float,
            float,
            int,
            int,
            float,
        ]
    ] = []
    twisted_line_kernel_moment_checked: List[Tuple[int, int, float, float]] = []
    twisted_line_fiber_checked = 0
    quotient_spectral_checked = 0
    split_hypergeometric_checked = 0
    filter_checked = verify_admissible_filter_counts()
    twist_nontrivial_checked = verify_admissible_twist_nontriviality()
    moment_checked = verify_second_moments()
    admissible_open_moment_checked = verify_admissible_open_moment_audit()
    admissible_transfer_thresholds_checked = (
        verify_admissible_suborder_transfer_thresholds()
    )
    admissible_suborder_moment_checked = (
        verify_admissible_suborder_moment_audit()
    )
    suborder_parseval_moment_checked = verify_suborder_parseval_open_moments()
    ratio_surface_joint_energy_checked = verify_ratio_surface_joint_energy()
    ratio_surface_degeneracy_checked = verify_ratio_surface_degeneracy()
    collapsed_four_p_obstruction_checked = (
        verify_quotient_line_collapsed_four_p_obstruction()
    )
    for p, eta_exponent, nu_exponent in case_iterator():
        if p not in tables:
            logs = log_table(p)
            tables[p] = character_table(p, logs)
            verify_discriminant_values(p)
            verify_singular_fiber_values(p, tables[p])
            lambda_map_checked += verify_lambda_map_ledger(p)
            finite_twist_count, projective_twist_count = verify_lambda_twist_divisor(p)
            lambda_twist_checked.append((p, finite_twist_count, projective_twist_count))
            twist_map_count, nonsplit_value_count = verify_twisted_discriminant_map(p)
            twisted_discriminant_checked.append(
                (p, twist_map_count, nonsplit_value_count)
            )
            (
                rational_outer_points,
                geometric_outer_points,
                rational_trace_points,
                geometric_trace_points,
            ) = verify_twisted_line_twist_divisor(p)
            twisted_line_twist_checked.append(
                (
                    p,
                    rational_outer_points,
                    geometric_outer_points,
                    rational_trace_points,
                    geometric_trace_points,
                )
            )
            (
                deck_count,
                max_kernel_deck,
                max_summand_deck,
                max_kernel_ratio,
            ) = verify_twisted_line_deck_symmetry(p, tables[p])
            twisted_line_deck_checked.append(
                (
                    p,
                    deck_count,
                    round(max_kernel_deck, 12),
                    round(max_summand_deck, 12),
                    round(max_kernel_ratio, 10),
                )
            )
            quotient_kernel_count, quotient_kernel_difference = (
                verify_quotient_line_kernel_trace(p, tables[p])
            )
            quotient_finite_points, quotient_projective_points = (
                verify_quotient_line_support(p)
            )
            quotient_line_checked.append(
                (
                    p,
                    quotient_kernel_count,
                    round(quotient_kernel_difference, 12),
                    quotient_finite_points,
                    quotient_projective_points,
                )
            )
            (
                quotient_moment_count,
                max_quotient_zero,
                max_quotient_second_error,
            ) = verify_quotient_line_kernel_moments(p, tables[p])
            quotient_line_kernel_moment_checked.append(
                (
                    p,
                    quotient_moment_count,
                    round(max_quotient_zero, 12),
                    round(max_quotient_second_error, 12),
                )
            )
            (
                quotient_mellin_count,
                max_quotient_mellin_error,
                max_quotient_mellin_ratio,
            ) = verify_quotient_line_mellin_spectrum(p, tables[p])
            quotient_line_mellin_checked.append(
                (
                    p,
                    quotient_mellin_count,
                    round(max_quotient_mellin_error, 12),
                    round(max_quotient_mellin_ratio, 10),
                )
            )
            (
                quotient_magnitude_count,
                max_quotient_magnitude_error,
                p_size_count,
                sqrt_size_count,
                unit_size_count,
            ) = verify_quotient_line_mellin_magnitudes(p, tables[p])
            quotient_line_mellin_magnitude_checked.append(
                (
                    p,
                    quotient_magnitude_count,
                    round(max_quotient_magnitude_error, 12),
                    p_size_count,
                    sqrt_size_count,
                    unit_size_count,
                )
            )
            (
                collapsed_inner_count,
                max_collapsed_inner_error,
                max_collapsed_inner_magnitude_error,
                max_collapsed_inner_moment_error,
                max_collapsed_inner_special_error,
                max_collapsed_inner_special_ratio,
                max_collapsed_inner_regular_ratio,
                inner_p_size_count,
                inner_sqrt_size_count,
                inner_unit_size_count,
            ) = verify_quotient_line_collapsed_inner_spectrum(p, tables[p])
            collapsed_inner_spectrum_checked.append(
                (
                    p,
                    collapsed_inner_count,
                    round(max_collapsed_inner_error, 12),
                    round(max_collapsed_inner_magnitude_error, 12),
                    round(max_collapsed_inner_moment_error, 12),
                    round(max_collapsed_inner_special_error, 12),
                    round(max_collapsed_inner_special_ratio, 10),
                    round(max_collapsed_inner_regular_ratio, 10),
                    inner_p_size_count,
                    inner_sqrt_size_count,
                    inner_unit_size_count,
                )
            )
            (
                mobius_energy_count,
                mobius_active_count,
                max_mobius_parseval_error,
                max_mobius_energy_ratio,
                max_mobius_pointwise_ratio,
                max_mobius_rms_ratio,
                max_mobius_full_energy_error,
                max_mobius_sharp_energy_ratio,
                max_mobius_sharp_bound_rms_ratio,
                max_mobius_quadratic_energy_error,
                max_mobius_quadratic_energy_ratio,
                max_mobius_selected_energy_ratio,
                max_mobius_selected_bound_rms_ratio,
                max_mobius_four_p_count,
                max_mobius_admissible_four_p_count,
                max_mobius_transform_ratio,
            ) = verify_quotient_line_collapsed_mobius_energy(p, tables[p])
            collapsed_mobius_energy_checked.append(
                (
                    p,
                    mobius_energy_count,
                    mobius_active_count,
                    round(max_mobius_parseval_error, 9),
                    round(max_mobius_energy_ratio, 10),
                    round(max_mobius_pointwise_ratio, 10),
                    round(max_mobius_rms_ratio, 10),
                    round(max_mobius_full_energy_error, 9),
                    round(max_mobius_sharp_energy_ratio, 10),
                    round(max_mobius_sharp_bound_rms_ratio, 10),
                    round(max_mobius_quadratic_energy_error, 9),
                    round(max_mobius_quadratic_energy_ratio, 10),
                    round(max_mobius_selected_energy_ratio, 10),
                    round(max_mobius_selected_bound_rms_ratio, 10),
                    max_mobius_four_p_count,
                    max_mobius_admissible_four_p_count,
                    round(max_mobius_transform_ratio, 10),
                )
            )
            (
                kernel_moment_count,
                max_kernel_first_moment,
                max_kernel_second_error,
            ) = verify_twisted_line_kernel_moments(p, tables[p])
            twisted_line_kernel_moment_checked.append(
                (
                    p,
                    kernel_moment_count,
                    round(max_kernel_first_moment, 12),
                    round(max_kernel_second_error, 12),
                )
            )
            twisted_line_fiber_checked += verify_twisted_line_fiber_trace(
                p,
                tables[p],
            )
            split_hypergeometric_checked += verify_split_hypergeometric_pullback(
                p,
                tables[p],
            )
            singular_checked.append(p)
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
        pulled_back = lambda_pullback_sum(p, eta, nu)
        twisted_core = quadratic_twisted_core(p, eta, nu)
        pullback_expected = (
            transformed
            + twisted_core
            - eta[(-3) % p] * transformed_inner(p, 3 % p, nu)
        )
        split_projection = split_projected_core(p, eta, nu)
        nonsplit_projection = nonsplit_projected_core(p, eta, nu)
        twisted_nonsplit = twisted_discriminant_nonsplit_sum(p, eta, nu)
        twisted_line_nonsplit = twisted_line_nonsplit_sum(p, eta, nu)
        quotient_line_nonsplit = quotient_line_nonsplit_sum(p, eta, nu)
        (
            spectral_theta_count,
            outer_decomposition_error,
            outer_standard_error,
            quotient_spectral_difference,
            outer_mellin_piece_ratio,
            outer_mellin_ratio,
            spectral_energy_error,
            spectral_cauchy_ratio,
            exceptional_spectral_ratio,
            exceptional_theta_count,
            generic_phase_error,
            generic_phase_sum_ratio,
            generic_theta_count,
            outer_quadratic_shift_error,
            kernel_pair_phase_error,
            delta_free_pair_error,
            pair_jacobi_product_error,
            outer_square_filter_error,
            kernel_square_filter_error,
            algebraic_pair_orbit_error,
            pair_diagonal_error,
            generic_diagonal_error,
            collapsed_diagonal_error,
            collapsed_singular_error,
            collapsed_rank_one_error,
            collapsed_rank_one_piece_ratio,
            collapsed_rank_one_ratio,
            collapsed_rank_two_split_error,
            collapsed_rank_two_mobius_error,
            collapsed_mobius_deleted_error,
            collapsed_rank_two_ratio,
            collapsed_h_ratio,
            paired_phase_ratio,
            paired_generic_count,
        ) = verify_quotient_line_spectral_normal_form(
            p,
            eta_exponent,
            nu_exponent,
            table,
        )
        quotient_spectral_checked += spectral_theta_count
        exceptional_theta_checked += exceptional_theta_count
        generic_theta_checked += generic_theta_count
        paired_generic_theta_checked += paired_generic_count
        assert_close(
            (p, eta_exponent, nu_exponent, "lambda_pullback_descent"),
            pulled_back,
            pullback_expected,
        )
        assert_close(
            (p, eta_exponent, nu_exponent, "split_projector"),
            pulled_back,
            split_projection,
        )
        assert_close(
            (p, eta_exponent, nu_exponent, "twisted_discriminant_nonsplit"),
            twisted_nonsplit,
            nonsplit_projection,
        )
        assert_close(
            (p, eta_exponent, nu_exponent, "twisted_line_nonsplit"),
            twisted_line_nonsplit,
            nonsplit_projection,
        )
        assert_close(
            (p, eta_exponent, nu_exponent, "quotient_line_nonsplit"),
            quotient_line_nonsplit,
            nonsplit_projection,
        )
        g_at_three = transformed_inner(p, 3 % p, nu)
        reconstructed_core = (
            split_projection
            + nonsplit_projection
            + eta[(-3) % p] * g_at_three
        ) / 2
        reconstructed_twist = (
            split_projection
            - nonsplit_projection
            + eta[(-3) % p] * g_at_three
        ) / 2
        assert_close(
            (p, eta_exponent, nu_exponent, "projector_core_reconstruction"),
            reconstructed_core,
            transformed,
        )
        assert_close(
            (p, eta_exponent, nu_exponent, "projector_twist_reconstruction"),
            reconstructed_twist,
            twisted_core,
        )
        (
            singular_split,
            singular_nonsplit,
            expected_singular_split,
            expected_singular_nonsplit,
        ) = projection_singular_contributions(p, eta, nu)
        assert_close(
            (p, eta_exponent, nu_exponent, "split_singular_projection"),
            singular_split,
            expected_singular_split,
        )
        assert_close(
            (p, eta_exponent, nu_exponent, "nonsplit_singular_projection"),
            singular_nonsplit,
            expected_singular_nonsplit,
        )
        if abs(singular_split) > 1 + math.sqrt(p) + TOLERANCE:
            raise AssertionError(
                (p, eta_exponent, nu_exponent, "split_singular_bound")
            )
        if abs(singular_nonsplit) > 1 + TOLERANCE:
            raise AssertionError(
                (p, eta_exponent, nu_exponent, "nonsplit_singular_bound")
            )
        max_pullback_difference = max(
            max_pullback_difference,
            abs(pulled_back - pullback_expected),
        )
        max_twisted_difference = max(
            max_twisted_difference,
            abs(twisted_nonsplit - nonsplit_projection),
        )
        max_twisted_line_difference = max(
            max_twisted_line_difference,
            abs(twisted_line_nonsplit - nonsplit_projection),
        )
        max_quotient_line_difference = max(
            max_quotient_line_difference,
            abs(quotient_line_nonsplit - nonsplit_projection),
        )
        max_quotient_spectral_difference = max(
            max_quotient_spectral_difference,
            quotient_spectral_difference,
        )
        max_outer_mellin_decomposition_error = max(
            max_outer_mellin_decomposition_error,
            outer_decomposition_error,
        )
        max_outer_standard_error = max(
            max_outer_standard_error,
            outer_standard_error,
        )
        max_outer_quadratic_shift_error = max(
            max_outer_quadratic_shift_error,
            outer_quadratic_shift_error,
        )
        max_kernel_pair_phase_error = max(
            max_kernel_pair_phase_error,
            kernel_pair_phase_error,
        )
        max_delta_free_pair_error = max(
            max_delta_free_pair_error,
            delta_free_pair_error,
        )
        max_pair_jacobi_product_error = max(
            max_pair_jacobi_product_error,
            pair_jacobi_product_error,
        )
        max_outer_square_filter_error = max(
            max_outer_square_filter_error,
            outer_square_filter_error,
        )
        max_kernel_square_filter_error = max(
            max_kernel_square_filter_error,
            kernel_square_filter_error,
        )
        max_algebraic_pair_orbit_error = max(
            max_algebraic_pair_orbit_error,
            algebraic_pair_orbit_error,
        )
        max_pair_diagonal_error = max(
            max_pair_diagonal_error,
            pair_diagonal_error,
        )
        max_generic_diagonal_error = max(
            max_generic_diagonal_error,
            generic_diagonal_error,
        )
        max_collapsed_diagonal_error = max(
            max_collapsed_diagonal_error,
            collapsed_diagonal_error,
        )
        max_collapsed_singular_error = max(
            max_collapsed_singular_error,
            collapsed_singular_error,
        )
        max_collapsed_rank_one_error = max(
            max_collapsed_rank_one_error,
            collapsed_rank_one_error,
        )
        max_collapsed_rank_one_piece_ratio = max(
            max_collapsed_rank_one_piece_ratio,
            collapsed_rank_one_piece_ratio,
        )
        max_collapsed_rank_one_ratio = max(
            max_collapsed_rank_one_ratio,
            collapsed_rank_one_ratio,
        )
        max_collapsed_rank_two_split_error = max(
            max_collapsed_rank_two_split_error,
            collapsed_rank_two_split_error,
        )
        max_collapsed_rank_two_mobius_error = max(
            max_collapsed_rank_two_mobius_error,
            collapsed_rank_two_mobius_error,
        )
        max_collapsed_mobius_deleted_error = max(
            max_collapsed_mobius_deleted_error,
            collapsed_mobius_deleted_error,
        )
        if collapsed_rank_two_ratio > max_collapsed_rank_two_ratio:
            max_collapsed_rank_two_ratio = collapsed_rank_two_ratio
            max_collapsed_rank_two_label = (p, eta_exponent, nu_exponent)
        if collapsed_h_ratio > max_collapsed_h_ratio:
            max_collapsed_h_ratio = collapsed_h_ratio
            max_collapsed_h_label = (p, eta_exponent, nu_exponent)
        max_paired_phase_ratio = max(
            max_paired_phase_ratio,
            paired_phase_ratio,
        )
        max_outer_mellin_ratio = max(
            max_outer_mellin_ratio,
            outer_mellin_ratio,
        )
        max_outer_mellin_piece_ratio = max(
            max_outer_mellin_piece_ratio,
            outer_mellin_piece_ratio,
        )
        max_spectral_energy_error = max(
            max_spectral_energy_error,
            spectral_energy_error,
        )
        max_spectral_cauchy_ratio = max(
            max_spectral_cauchy_ratio,
            spectral_cauchy_ratio,
        )
        max_exceptional_spectral_ratio = max(
            max_exceptional_spectral_ratio,
            exceptional_spectral_ratio,
        )
        max_generic_phase_error = max(
            max_generic_phase_error,
            generic_phase_error,
        )
        max_generic_phase_sum_ratio = max(
            max_generic_phase_sum_ratio,
            generic_phase_sum_ratio,
        )
        split_projection_ratio = abs(split_projection) / p
        nonsplit_projection_ratio = abs(nonsplit_projection) / p
        nonsplit_singular_ratio = abs(singular_nonsplit)
        if split_projection_ratio > max_split_projection_ratio:
            max_split_projection_ratio = split_projection_ratio
            max_split_projection_label = (p, eta_exponent, nu_exponent)
        if nonsplit_projection_ratio > max_nonsplit_projection_ratio:
            max_nonsplit_projection_ratio = nonsplit_projection_ratio
            max_nonsplit_projection_label = (p, eta_exponent, nu_exponent)
        if nonsplit_singular_ratio > max_nonsplit_singular_ratio:
            max_nonsplit_singular_ratio = nonsplit_singular_ratio
            max_nonsplit_singular_label = (p, eta_exponent, nu_exponent)
        core_ratio = abs(direct) / p
        if core_ratio > max_core_ratio:
            max_core_ratio = core_ratio
            max_core_label = (p, eta_exponent, nu_exponent)
        if abs(direct) > 4 * p + TOLERANCE:
            raise AssertionError((p, eta_exponent, nu_exponent, "core_4p"))
        direct_open_sum = direct_open(p, eta_inv, nu, eta)
        correction = line_correction(p, eta_inv, nu, eta)
        corrected_core = direct - correction
        assert_close(
            (p, eta_exponent, nu_exponent, "open"),
            direct_open_sum,
            corrected_core,
        )
        max_difference = max(max_difference, abs(direct_open_sum - corrected_core))
        open_ratio = abs(direct_open_sum) / p
        line_ratio = abs(correction) / math.sqrt(p)
        if open_ratio > max_open_ratio:
            max_open_ratio = open_ratio
            max_open_label = (p, eta_exponent, nu_exponent)
        if line_ratio > max_line_ratio:
            max_line_ratio = line_ratio
            max_line_label = (p, eta_exponent, nu_exponent)
        if abs(direct_open_sum) > 4 * p + TOLERANCE:
            raise AssertionError((p, eta_exponent, nu_exponent, "open_4p"))
        if abs(correction) > 3 * math.sqrt(p) + TOLERANCE:
            raise AssertionError((p, eta_exponent, nu_exponent, "line_3sqrt"))
        checked_open_decompositions += 1
        checked_cases += 1
    print(
        "verify_m1_depth_two_line_conic_resonance_reduction: PASS",
        f"cases={checked_cases}",
        f"fibers={checked_fibers}",
        f"open_decompositions={checked_open_decompositions}",
        f"max_difference={max_difference:.3e}",
        f"max_pullback_difference={max_pullback_difference:.3e}",
        f"max_twisted_difference={max_twisted_difference:.3e}",
        f"max_twisted_line_difference={max_twisted_line_difference:.3e}",
        f"max_quotient_line_difference={max_quotient_line_difference:.3e}",
        f"max_quotient_spectral_difference="
        f"{max_quotient_spectral_difference:.3e}",
        f"max_outer_mellin_decomposition_error="
        f"{max_outer_mellin_decomposition_error:.3e}",
        f"max_outer_standard_error={max_outer_standard_error:.3e}",
        f"max_outer_quadratic_shift_error="
        f"{max_outer_quadratic_shift_error:.3e}",
        f"max_kernel_pair_phase_error={max_kernel_pair_phase_error:.3e}",
        f"max_delta_free_pair_error={max_delta_free_pair_error:.3e}",
        f"max_pair_jacobi_product_error="
        f"{max_pair_jacobi_product_error:.3e}",
        f"max_outer_square_filter_error={max_outer_square_filter_error:.3e}",
        f"max_kernel_square_filter_error="
        f"{max_kernel_square_filter_error:.3e}",
        f"max_algebraic_pair_orbit_error="
        f"{max_algebraic_pair_orbit_error:.3e}",
        f"max_pair_diagonal_error={max_pair_diagonal_error:.3e}",
        f"max_generic_diagonal_error={max_generic_diagonal_error:.3e}",
        f"max_collapsed_diagonal_error="
        f"{max_collapsed_diagonal_error:.3e}",
        f"max_collapsed_singular_error="
        f"{max_collapsed_singular_error:.3e}",
        f"max_collapsed_rank_one_error="
        f"{max_collapsed_rank_one_error:.3e}",
        f"max_collapsed_rank_one_piece_ratio="
        f"{max_collapsed_rank_one_piece_ratio:.10f}",
        f"max_collapsed_rank_one_ratio="
        f"{max_collapsed_rank_one_ratio:.10f}",
        f"max_collapsed_rank_two_split_error="
        f"{max_collapsed_rank_two_split_error:.3e}",
        f"max_collapsed_rank_two_mobius_error="
        f"{max_collapsed_rank_two_mobius_error:.3e}",
        f"max_collapsed_mobius_deleted_error="
        f"{max_collapsed_mobius_deleted_error:.3e}",
        f"max_collapsed_rank_two_ratio="
        f"{max_collapsed_rank_two_ratio:.10f}@"
        f"{max_collapsed_rank_two_label}",
        f"max_collapsed_h_ratio={max_collapsed_h_ratio:.10f}@"
        f"{max_collapsed_h_label}",
        f"max_paired_phase_ratio={max_paired_phase_ratio:.10f}",
        f"max_outer_mellin_piece_ratio={max_outer_mellin_piece_ratio:.10f}",
        f"max_outer_mellin_ratio={max_outer_mellin_ratio:.10f}",
        f"max_spectral_energy_error={max_spectral_energy_error:.3e}",
        f"max_spectral_cauchy_ratio={max_spectral_cauchy_ratio:.10f}",
        f"max_exceptional_spectral_ratio="
        f"{max_exceptional_spectral_ratio:.10f}",
        f"max_generic_phase_error={max_generic_phase_error:.3e}",
        f"max_generic_phase_sum_ratio={max_generic_phase_sum_ratio:.10f}",
        f"max_core_ratio={max_core_ratio:.10f}@{max_core_label}",
        f"max_open_ratio={max_open_ratio:.10f}@{max_open_label}",
        f"max_line_ratio={max_line_ratio:.10f}@{max_line_label}",
        f"max_split_projection_ratio={max_split_projection_ratio:.10f}@"
        f"{max_split_projection_label}",
        f"max_nonsplit_projection_ratio={max_nonsplit_projection_ratio:.10f}@"
        f"{max_nonsplit_projection_label}",
        f"max_nonsplit_singular={max_nonsplit_singular_ratio:.10f}@"
        f"{max_nonsplit_singular_label}",
        f"singular_checked={singular_checked}",
        f"lambda_map_checked={lambda_map_checked}",
        f"lambda_twist_checked={lambda_twist_checked}",
        f"twisted_discriminant_checked={twisted_discriminant_checked}",
        f"twisted_line_twist_checked={twisted_line_twist_checked}",
        f"twisted_line_deck_checked={twisted_line_deck_checked}",
        f"quotient_line_checked={quotient_line_checked}",
        f"quotient_line_kernel_moment_checked="
        f"{quotient_line_kernel_moment_checked}",
        f"quotient_line_mellin_checked={quotient_line_mellin_checked}",
        f"quotient_line_mellin_magnitude_checked="
        f"{quotient_line_mellin_magnitude_checked}",
        f"collapsed_inner_spectrum_checked="
        f"{collapsed_inner_spectrum_checked}",
        f"collapsed_mobius_energy_checked="
        f"{collapsed_mobius_energy_checked}",
        f"quotient_spectral_checked={quotient_spectral_checked}",
        f"exceptional_theta_checked={exceptional_theta_checked}",
        f"generic_theta_checked={generic_theta_checked}",
        f"paired_generic_theta_checked={paired_generic_theta_checked}",
        f"twisted_line_kernel_moment_checked="
        f"{twisted_line_kernel_moment_checked}",
        f"twisted_line_fiber_checked={twisted_line_fiber_checked}",
        f"split_hypergeometric_checked={split_hypergeometric_checked}",
        f"filter_checked={filter_checked[0]}..{filter_checked[-1]}",
        f"twist_nontrivial_checked={twist_nontrivial_checked[0]}.."
        f"{twist_nontrivial_checked[-1]}",
        f"moment_checked={moment_checked}",
        f"admissible_open_moment_checked={admissible_open_moment_checked}",
        f"admissible_transfer_thresholds_checked="
        f"{admissible_transfer_thresholds_checked}",
        f"admissible_suborder_moment_checked="
        f"{admissible_suborder_moment_checked}",
        f"suborder_parseval_moment_checked={suborder_parseval_moment_checked}",
        f"ratio_surface_joint_energy_checked="
        f"{ratio_surface_joint_energy_checked}",
        f"ratio_surface_degeneracy_checked="
        f"{ratio_surface_degeneracy_checked}",
        f"collapsed_four_p_obstruction_checked="
        f"{collapsed_four_p_obstruction_checked}",
    )


if __name__ == "__main__":
    main()
