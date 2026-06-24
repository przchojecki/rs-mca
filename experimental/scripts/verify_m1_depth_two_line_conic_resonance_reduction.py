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
LOWER_CHART_PRIMES = (5, 7, 11, 17, 31, 43)
PUSHFORWARD_TRACE_CASES = (
    (17, 1, 3),
    (17, 5, 7),
    (31, 2, 5),
    (31, 6, 11),
    (43, 3, 10),
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


def quotient_conic_joint_energy_bound(p: int, suborder: int) -> int:
    kernel_size = (p - 1) // suborder
    parameter_count = kernel_size * kernel_size * (p - 1)
    degenerate_bound = 3 * kernel_size * kernel_size
    support_count = open_support_size_formula(p)
    return (
        support_count
        + (parameter_count - 1) * (p + 1)
        + (degenerate_bound - 1) * p
    )


def quotient_conic_centered_moment_bound(p: int, suborder: int) -> int:
    support_count = open_support_size_formula(p)
    return (
        suborder
        * suborder
        * quotient_conic_joint_energy_bound(p, suborder)
        - support_count
        * support_count
    )


def quotient_centering_weight(p: int, suborder: int, logs: Dict[int, int], value: int) -> int:
    if value % p == 0:
        raise ValueError((p, suborder, "zero-weight"))
    return suborder * int(logs[value % p] % suborder == 0) - 1


def weighted_ratio_surface_centered_moment(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> int:
    support: List[Tuple[int, int, int]] = []
    for u in range(1, p):
        inverse_u = pow(u, -1, p)
        for v in range(1, p):
            if not is_open_support_point(p, u, v):
                continue
            support.append((u, v, shape_a(u, v, p) * inverse_u % p))
    total = 0
    for u, v, x_value in support:
        inverse_u = pow(u, -1, p)
        inverse_v = pow(v, -1, p)
        inverse_x = pow(x_value, -1, p)
        for target_u, target_v, target_x in support:
            alpha = target_x * inverse_x % p
            beta = target_v * inverse_v % p
            ratio = target_u * inverse_u % p
            equation = (
                ratio * (ratio - alpha) * u * u
                + ratio * ((beta - alpha) * v + (1 - alpha)) * u
                + shape_b(beta * v % p, p)
                - alpha * ratio * shape_b(v, p)
            ) % p
            if equation != 0:
                raise AssertionError(
                    (p, suborder, alpha, beta, ratio, u, v, equation)
                )
            total += (
                quotient_centering_weight(p, suborder, logs, alpha)
                * quotient_centering_weight(p, suborder, logs, beta)
            )
    return total


def ratio_surface_projective_point_count(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> int:
    uu, uv, vv, u_linear, v_linear, constant = (
        ratio_surface_conic_coefficients(p, alpha, beta, ratio)
    )
    affine_count = 0
    for u in range(p):
        for v in range(p):
            value = (
                uu * u * u
                + uv * u * v
                + vv * v * v
                + u_linear * u
                + v_linear * v
                + constant
            ) % p
            if value == 0:
                affine_count += 1
    infinity_count = int(vv == 0)
    for slope in range(p):
        value = (uu + uv * slope + vv * slope * slope) % p
        if value == 0:
            infinity_count += 1
    return affine_count + infinity_count


def ratio_surface_affine_value(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
    u: int,
    v: int,
) -> int:
    uu, uv, vv, u_linear, v_linear, constant = (
        ratio_surface_conic_coefficients(p, alpha, beta, ratio)
    )
    return (
        uu * u * u
        + uv * u * v
        + vv * v * v
        + u_linear * u
        + v_linear * v
        + constant
    ) % p


def ratio_surface_infinity_count(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> int:
    uu, uv, vv, _, _, _ = ratio_surface_conic_coefficients(
        p,
        alpha,
        beta,
        ratio,
    )
    count = int(vv == 0)
    for slope in range(p):
        if (uu + uv * slope + vv * slope * slope) % p == 0:
            count += 1
    return count


BOUNDARY_LABELS = (
    "infinity",
    "u0",
    "v0",
    "source_line",
    "target_line",
    "source_a0",
    "target_a0",
)


def shape_a_zero_points(p: int) -> List[Tuple[int, int]]:
    return [
        (u, v)
        for u in range(p)
        for v in range(p)
        if shape_a(u, v, p) == 0
    ]


def ratio_surface_boundary_label(
    p: int,
    beta: int,
    ratio: int,
    u: int,
    v: int,
) -> str:
    if u % p == 0:
        return "u0"
    if v % p == 0:
        return "v0"
    if (-1 - u - v) % p == 0:
        return "source_line"
    if (-1 - ratio * u - beta * v) % p == 0:
        return "target_line"
    if shape_a(u, v, p) == 0:
        return "source_a0"
    if shape_a(ratio * u % p, beta * v % p, p) == 0:
        return "target_a0"
    return ""


def add_boundary_candidate(
    totals: Dict[str, int],
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
    weight: int,
    expected_label: str,
    u: int,
    v: int,
) -> None:
    if ratio_surface_affine_value(p, alpha, beta, ratio, u, v) != 0:
        return
    label = ratio_surface_boundary_label(p, beta, ratio, u, v)
    if label == expected_label:
        totals[label] += weight


def weighted_boundary_partition_sum(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> Tuple[int, ...]:
    totals = {label: 0 for label in BOUNDARY_LABELS}
    source_a_points = shape_a_zero_points(p)
    for alpha in range(1, p):
        alpha_weight = quotient_centering_weight(p, suborder, logs, alpha)
        for beta in range(1, p):
            inverse_beta = pow(beta, -1, p)
            weight = alpha_weight * quotient_centering_weight(
                p,
                suborder,
                logs,
                beta,
            )
            for ratio in range(1, p):
                inverse_ratio = pow(ratio, -1, p)
                totals["infinity"] += weight * ratio_surface_infinity_count(
                    p,
                    alpha,
                    beta,
                    ratio,
                )
                for v in range(p):
                    add_boundary_candidate(
                        totals,
                        p,
                        alpha,
                        beta,
                        ratio,
                        weight,
                        "u0",
                        0,
                        v,
                    )
                for u in range(p):
                    add_boundary_candidate(
                        totals,
                        p,
                        alpha,
                        beta,
                        ratio,
                        weight,
                        "v0",
                        u,
                        0,
                    )
                    add_boundary_candidate(
                        totals,
                        p,
                        alpha,
                        beta,
                        ratio,
                        weight,
                        "source_line",
                        u,
                        (-1 - u) % p,
                    )
                    add_boundary_candidate(
                        totals,
                        p,
                        alpha,
                        beta,
                        ratio,
                        weight,
                        "target_line",
                        u,
                        (-1 - ratio * u) * inverse_beta % p,
                    )
                for u, v in source_a_points:
                    add_boundary_candidate(
                        totals,
                        p,
                        alpha,
                        beta,
                        ratio,
                        weight,
                        "source_a0",
                        u,
                        v,
                    )
                    add_boundary_candidate(
                        totals,
                        p,
                        alpha,
                        beta,
                        ratio,
                        weight,
                        "target_a0",
                        u * inverse_ratio % p,
                        v * inverse_beta % p,
                    )
    return tuple(totals[label] for label in BOUNDARY_LABELS)


def add_solved_alpha_weight(
    p: int,
    suborder: int,
    logs: Dict[int, int],
    beta: int,
    numerator: int,
    denominator: int,
) -> int:
    numerator %= p
    denominator %= p
    if denominator == 0:
        return 0
    alpha = numerator * pow(denominator, -1, p) % p
    if alpha == 0:
        return 0
    return (
        quotient_centering_weight(p, suborder, logs, alpha)
        * quotient_centering_weight(p, suborder, logs, beta)
    )


def weighted_infinity_formula_sum(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> int:
    total = 0
    for beta in range(1, p):
        beta_weight = quotient_centering_weight(p, suborder, logs, beta)
        for ratio in range(1, p):
            for slope in range(p):
                numerator = (
                    ratio * ratio
                    + ratio * beta * slope
                    + beta * beta * slope * slope
                )
                denominator = ratio * shape_b(slope, p)
                total += add_solved_alpha_weight(
                    p,
                    suborder,
                    logs,
                    beta,
                    numerator,
                    denominator,
                )
            alpha = beta * beta * pow(ratio, -1, p) % p
            total += (
                quotient_centering_weight(p, suborder, logs, alpha)
                * beta_weight
            )
    return total


def quotient_weight_autocorrelation(
    p: int,
    suborder: int,
    logs: Dict[int, int],
    value: int,
) -> int:
    value %= p
    if value == 0:
        return 0
    direct = 0
    for y in range(1, p):
        direct += quotient_centering_weight(
            p,
            suborder,
            logs,
            value * y % p,
        ) * quotient_centering_weight(p, suborder, logs, y)
    expected = (p - 1) * quotient_centering_weight(p, suborder, logs, value)
    if direct != expected:
        raise AssertionError((p, suborder, value, direct, expected))
    return expected


def weighted_infinity_autocorrelation_sum(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> int:
    total = 0
    point_at_infinity = 0
    for t in range(1, p):
        point_at_infinity += quotient_weight_autocorrelation(
            p,
            suborder,
            logs,
            t,
        )
        for slope in range(p):
            denominator = t * shape_b(slope, p) % p
            if denominator == 0:
                continue
            numerator = (
                1
                + t * slope
                + t * t * slope * slope
            ) % p
            if numerator == 0:
                continue
            value = numerator * pow(denominator, -1, p) % p
            total += quotient_weight_autocorrelation(
                p,
                suborder,
                logs,
                value,
            )
    if point_at_infinity != 0:
        raise AssertionError((p, suborder, point_at_infinity))
    return total


def infinity_shape_ratio(p: int, value: int) -> int:
    return shape_b(value, p) * pow(value, -1, p) % p


def weighted_infinity_fiber_energy_sum(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> int:
    counts = {value: 0 for value in range(1, p)}
    for source in range(1, p):
        if shape_b(source, p) == 0:
            continue
        counts[infinity_shape_ratio(p, source)] += 1

    for value, count in counts.items():
        discriminant = value * value - 2 * value - 3
        expected = 1 + legendre(discriminant, p)
        if count != expected:
            raise AssertionError((p, suborder, value, count, expected))

    fiber_energy = 0
    centered_energy = 0
    constant_part = 0
    linear_part = 0
    for left in range(1, p):
        left_twist = legendre(left * left - 2 * left - 3, p)
        for right in range(1, p):
            right_twist = legendre(right * right - 2 * right - 3, p)
            weight = quotient_centering_weight(
                p,
                suborder,
                logs,
                left * pow(right, -1, p),
            )
            fiber_energy += counts[left] * counts[right] * weight
            centered_energy += left_twist * right_twist * weight
            constant_part += weight
            linear_part += left_twist * weight
    if constant_part != 0 or linear_part != 0:
        raise AssertionError((p, suborder, constant_part, linear_part))
    if fiber_energy != centered_energy:
        raise AssertionError((p, suborder, fiber_energy, centered_energy))
    return (p - 1) * fiber_energy


def weighted_infinity_spectral_audit(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> Tuple[int, float]:
    total = 0.0
    max_ratio = 0.0
    root = cmath.exp(2j * math.pi / suborder)
    for exponent in range(1, suborder):
        character_sum = 0j
        for value in range(1, p):
            twist = legendre(value * value - 2 * value - 3, p)
            if twist == 0:
                continue
            character_sum += twist * root ** (exponent * logs[value])
        total += abs(character_sum) ** 2
        max_ratio = max(max_ratio, abs(character_sum) / math.sqrt(p))
    energy = weighted_infinity_fiber_energy_sum(p, suborder, logs) // (p - 1)
    if abs(total - energy) > 1000 * TOLERANCE:
        raise AssertionError((p, suborder, total, energy))
    if max_ratio > 2 + 1000 * TOLERANCE:
        raise AssertionError((p, suborder, max_ratio))
    return round(total), round(max_ratio, 10)


def weighted_source_line_formula_sum(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> int:
    total = 0
    for beta in range(1, p):
        for ratio in range(1, p):
            for u in range(1, p):
                v = (-1 - u) % p
                if v == 0:
                    continue
                numerator = (
                    ratio * ratio * u * u
                    + ratio * (beta * v + 1) * u
                    + shape_b(beta * v % p, p)
                )
                denominator = ratio * shape_b(u, p)
                total += add_solved_alpha_weight(
                    p,
                    suborder,
                    logs,
                    beta,
                    numerator,
                    denominator,
                )
    return total


def weighted_source_line_split_formula_sums(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> Tuple[int, int]:
    exclusive = 0
    overlap = 0
    for beta in range(1, p):
        for ratio in range(1, p):
            for u in range(1, p):
                v = (-1 - u) % p
                if v == 0:
                    continue
                numerator = (
                    ratio * ratio * u * u
                    + ratio * (beta * v + 1) * u
                    + shape_b(beta * v % p, p)
                )
                denominator = ratio * shape_b(u, p)
                value = add_solved_alpha_weight(
                    p,
                    suborder,
                    logs,
                    beta,
                    numerator,
                    denominator,
                )
                if (-1 - ratio * u - beta * v) % p == 0:
                    overlap += value
                else:
                    exclusive += value
    return exclusive, overlap


def line_pair_overlap_domain(p: int) -> List[Tuple[int, int]]:
    domain = []
    for value in range(1, p):
        if (1 + value) % p == 0:
            continue
        if shape_b(value, p) == 0:
            continue
        domain.append((infinity_shape_ratio(p, value), (1 + value) % p))
    return domain


def weighted_line_pair_overlap_energy_sum(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> int:
    domain = line_pair_overlap_domain(p)
    total = 0
    for target_f, target_h in domain:
        for source_f, source_h in domain:
            total += (
                quotient_centering_weight(
                    p,
                    suborder,
                    logs,
                    target_f * pow(source_f, -1, p),
                )
                * quotient_centering_weight(
                    p,
                    suborder,
                    logs,
                    target_h * pow(source_h, -1, p),
                )
            )
    return total


def weighted_line_pair_overlap_spectral_audit(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> Tuple[int, float]:
    total = 0.0
    max_ratio = 0.0
    root = cmath.exp(2j * math.pi / suborder)
    for first_exponent in range(1, suborder):
        for second_exponent in range(1, suborder):
            character_sum = 0j
            for first_value, second_value in line_pair_overlap_domain(p):
                character_sum += root ** (
                    first_exponent * logs[first_value]
                    + second_exponent * logs[second_value]
                )
            total += abs(character_sum) ** 2
            max_ratio = max(max_ratio, abs(character_sum) / math.sqrt(p))
    expected = weighted_line_pair_overlap_energy_sum(p, suborder, logs)
    if abs(total - expected) > 1000 * TOLERANCE:
        raise AssertionError((p, suborder, total, expected))
    if max_ratio > 3 + 1000 * TOLERANCE:
        raise AssertionError((p, suborder, max_ratio))
    return round(total), round(max_ratio, 10)


def target_line_domain(p: int) -> List[Tuple[int, int]]:
    domain = []
    for value in range(1, p):
        target_v = (-1 - value) % p
        if target_v == 0:
            continue
        if shape_b(value, p) == 0:
            continue
        target_quotient = (-infinity_shape_ratio(p, value)) % p
        domain.append((target_quotient, target_v))
    return domain


def source_open_domain(p: int) -> List[Tuple[int, int]]:
    domain = []
    for u in range(1, p):
        inverse_u = pow(u, -1, p)
        for v in range(1, p):
            if (-1 - u - v) % p == 0:
                continue
            a_value = shape_a(u, v, p)
            if a_value == 0:
                continue
            domain.append((a_value * inverse_u % p, v))
    return domain


def weighted_target_line_spectral_pairing_audit(
    p: int,
    suborder: int,
    logs: Dict[int, int],
    moment: int,
    overlap_energy: int,
    target_line: int,
) -> Tuple[int, int, int, float]:
    total = 0j
    line_energy = 0.0
    source_energy = 0.0
    root = cmath.exp(2j * math.pi / suborder)
    target_domain = target_line_domain(p)
    source_domain = source_open_domain(p)
    for first_exponent in range(1, suborder):
        for second_exponent in range(1, suborder):
            line_sum = 0j
            for quotient, target_v in target_domain:
                line_sum += root ** (
                    first_exponent * logs[quotient]
                    + second_exponent * logs[target_v]
                )
            source_sum = 0j
            for quotient, source_v in source_domain:
                source_sum += root ** (
                    -first_exponent * logs[quotient]
                    - second_exponent * logs[source_v]
                )
            total += line_sum * source_sum
            line_energy += abs(line_sum) ** 2
            source_energy += abs(source_sum) ** 2
    if abs(total.imag) > 1000 * TOLERANCE:
        raise AssertionError((p, suborder, total))
    rounded_total = round(total.real)
    rounded_line_energy = round(line_energy)
    rounded_source_energy = round(source_energy)
    if rounded_total != target_line:
        raise AssertionError((p, suborder, rounded_total, target_line))
    if rounded_line_energy != overlap_energy:
        raise AssertionError((p, suborder, rounded_line_energy, overlap_energy))
    if rounded_source_energy != moment:
        raise AssertionError((p, suborder, rounded_source_energy, moment))
    cauchy_bound = math.sqrt(overlap_energy * moment)
    if abs(target_line) > cauchy_bound + 1000 * TOLERANCE:
        raise AssertionError((p, suborder, target_line, cauchy_bound))
    ratio = abs(target_line) / cauchy_bound if cauchy_bound else 0.0
    return (
        rounded_total,
        rounded_line_energy,
        rounded_source_energy,
        round(ratio, 10),
    )


def closed_boundary_moment_bounds(
    p: int,
    suborder: int,
    moment: int,
    projective_error: int,
    overlap_energy: int,
) -> Tuple[float, float]:
    projective_positive = max(projective_error, 0)
    exact_bound = (
        math.sqrt(projective_positive)
        + math.sqrt(overlap_energy)
    ) ** 2
    conductor_overlap_bound = 9 * (suborder - 1) * (suborder - 1) * p
    conductor_bound = (
        math.sqrt(projective_positive)
        + math.sqrt(conductor_overlap_bound)
    ) ** 2
    if moment > exact_bound + 1000 * TOLERANCE:
        raise AssertionError((p, suborder, moment, exact_bound))
    if moment > conductor_bound + 1000 * TOLERANCE:
        raise AssertionError((p, suborder, moment, conductor_bound))
    return (
        round(moment / exact_bound, 10) if exact_bound else 0.0,
        round(moment / conductor_bound, 10) if conductor_bound else 0.0,
    )


def weighted_target_line_formula_sum(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> int:
    total = 0
    for beta in range(1, p):
        inverse_beta = pow(beta, -1, p)
        for ratio in range(1, p):
            for u in range(1, p):
                v = (-1 - ratio * u) * inverse_beta % p
                if ratio_surface_boundary_label(p, beta, ratio, u, v) != (
                    "target_line"
                ):
                    continue
                constant = ratio_surface_affine_value(p, 0, beta, ratio, u, v)
                linear = (
                    ratio_surface_affine_value(p, 1, beta, ratio, u, v)
                    - constant
                ) % p
                total += add_solved_alpha_weight(
                    p,
                    suborder,
                    logs,
                    beta,
                    -constant,
                    linear,
                )
    return total


def weighted_surviving_boundary_formula_sums(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> Tuple[int, int, int]:
    return (
        weighted_infinity_formula_sum(p, suborder, logs),
        weighted_source_line_formula_sum(p, suborder, logs),
        weighted_target_line_formula_sum(p, suborder, logs),
    )


def weighted_projective_error_sum(
    p: int,
    suborder: int,
    logs: Dict[int, int],
) -> Tuple[int, int, int]:
    total = 0
    singular_count = 0
    zero_conic_count = 0
    for alpha in range(1, p):
        alpha_weight = quotient_centering_weight(p, suborder, logs, alpha)
        for beta in range(1, p):
            weight = alpha_weight * quotient_centering_weight(
                p,
                suborder,
                logs,
                beta,
            )
            for ratio in range(1, p):
                determinant = ratio_surface_doubled_projective_determinant(
                    p,
                    alpha,
                    beta,
                    ratio,
                )
                if determinant != 0:
                    continue
                singular_count += 1
                coefficients = ratio_surface_conic_coefficients(
                    p,
                    alpha,
                    beta,
                    ratio,
                )
                if all(coefficient == 0 for coefficient in coefficients):
                    zero_conic_count += 1
                projective_count = ratio_surface_projective_point_count(
                    p,
                    alpha,
                    beta,
                    ratio,
                )
                total += weight * (projective_count - (p + 1))
    return total, singular_count, zero_conic_count


def projective_excess_unit(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> int:
    coefficients = ratio_surface_conic_coefficients(p, alpha, beta, ratio)
    projective_count = ratio_surface_projective_point_count(
        p,
        alpha,
        beta,
        ratio,
    )
    excess = projective_count - (p + 1)
    if excess % p != 0:
        raise AssertionError((p, alpha, beta, ratio, excess))
    unit = excess // p
    if all(coefficient == 0 for coefficient in coefficients):
        if unit != p:
            raise AssertionError((p, alpha, beta, ratio, unit))
    elif unit not in (-1, 0, 1):
        raise AssertionError((p, alpha, beta, ratio, unit))
    coefficient_discriminants = tuple(
        discriminant % p for discriminant in binary_discriminants(coefficients)
    )
    formula_discriminants = ratio_surface_binary_discriminants(
        p,
        alpha,
        beta,
        ratio,
    )
    if coefficient_discriminants != formula_discriminants:
        raise AssertionError(
            (
                p,
                alpha,
                beta,
                ratio,
                coefficient_discriminants,
                formula_discriminants,
            )
        )
    discriminant_unit = projective_excess_unit_from_discriminants(
        p,
        coefficients,
    )
    if discriminant_unit != unit:
        raise AssertionError(
            (p, alpha, beta, ratio, unit, discriminant_unit, coefficients)
        )
    return unit


def ratio_surface_binary_discriminants(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> Tuple[int, int, int]:
    a = alpha
    b = beta
    r = ratio
    return (
        r * (
            -3 * a * a * r
            + 4 * a * b * b
            - 2 * a * b * r
            + 4 * a * r * r
            - 3 * b * b * r
        ) % p,
        r * (
            -3 * a * a * r
            + 4 * a * r * r
            - 2 * a * r
            + 4 * a
            - 3 * r
        ) % p,
        (
            -3 * a * a * r * r
            + 4 * a * b * b * r
            - 2 * a * b * r
            + 4 * a * r
            - 3 * b * b
        ) % p,
    )


def binary_discriminants(
    coefficients: Tuple[int, int, int, int, int, int],
) -> Tuple[int, int, int]:
    uu, uv, vv, u_linear, v_linear, constant = coefficients
    return (
        uv * uv - 4 * uu * vv,
        u_linear * u_linear - 4 * uu * constant,
        v_linear * v_linear - 4 * vv * constant,
    )


def quadratic_resultant(
    p: int,
    left: Tuple[int, int, int],
    right: Tuple[int, int, int],
) -> int:
    a, b, c = left
    d, e, f = right
    return (
        a * a * f * f
        - a * b * e * f
        + a * c * e * e
        - 2 * a * c * d * f
        + b * b * d * f
        - b * c * d * e
        + c * c * d * d
    ) % p


def projective_excess_unit_from_discriminants(
    p: int,
    coefficients: Tuple[int, int, int, int, int, int],
) -> int:
    if all(coefficient % p == 0 for coefficient in coefficients):
        return p
    classes = [
        legendre(discriminant, p)
        for discriminant in binary_discriminants(coefficients)
        if discriminant % p != 0
    ]
    if not classes:
        return 0
    first = classes[0]
    if any(value != first for value in classes):
        raise AssertionError((p, coefficients, classes))
    return first


def projective_excess_chart(
    p: int,
    coefficients: Tuple[int, int, int, int, int, int],
) -> Tuple[str, int]:
    if all(coefficient % p == 0 for coefficient in coefficients):
        return "zero", p
    labels = ("uv", "u1", "v1")
    for label, discriminant in zip(labels, binary_discriminants(coefficients)):
        if discriminant % p != 0:
            return label, legendre(discriminant, p)
    return "rank1", 0


def ratio_surface_lower_alpha_kernel(p: int, alpha: int, ratio: int) -> int:
    a = alpha
    r = ratio
    return (-a * a * r + 3 * a * r * r - 4 * a * r + 3 * a - r) % p


def ratio_surface_lower_beta_kernel(p: int, beta: int, ratio: int) -> int:
    b = beta
    r = ratio
    return (
        3 * b * b * r
        - 2 * b * b
        + 3 * b * r * r
        - 8 * b * r
        + 3 * b
        - 2 * r * r
        + 3 * r
    ) % p


def ratio_surface_beta_coefficients(
    p: int,
    alpha: int,
    ratio: int,
) -> Tuple[int, int, int]:
    a = alpha
    r = ratio
    return (
        (3 * a * a * r - 3 * a * r * r + a * r - 3 * a + 2 * r) % p,
        (-a * r * (a - 1) * (r + 1)) % p,
        (
            a
            * r
            * (-2 * a * a * r + 3 * a * r * r - a * r + 3 * a - 3 * r)
        )
        % p,
    )


def ratio_surface_beta_branch_factor(p: int, alpha: int, ratio: int) -> int:
    a = alpha
    r = ratio
    return (-8 * a * a * r + 9 * a * r * r - 2 * a * r + 9 * a - 8 * r) % p


def ratio_surface_beta_branch_factor_derivatives(
    p: int,
    alpha: int,
    ratio: int,
) -> Tuple[int, int]:
    a = alpha
    r = ratio
    return (
        (-16 * a * r + 9 * r * r - 2 * r + 9) % p,
        (-8 * a * a + 18 * a * r - 2 * a - 8) % p,
    )


def ratio_surface_beta_middle_factor(p: int, alpha: int, ratio: int) -> int:
    a = alpha
    r = ratio
    return (-3 * a * a * r + 4 * a * r * r - 2 * a * r + 4 * a - 3 * r) % p


def ratio_surface_beta_middle_factor_derivatives(
    p: int,
    alpha: int,
    ratio: int,
) -> Tuple[int, int]:
    a = alpha
    r = ratio
    return (
        (-6 * a * r + 4 * r * r - 2 * r + 4) % p,
        (-3 * a * a + 8 * a * r - 2 * a - 3) % p,
    )


def ratio_surface_beta_zero_factor(p: int, alpha: int, ratio: int) -> int:
    a = alpha
    r = ratio
    return (-2 * a * a * r + 3 * a * r * r - a * r + 3 * a - 3 * r) % p


def ratio_surface_uv_discriminant_at_beta_zero(
    p: int,
    alpha: int,
    ratio: int,
) -> int:
    a = alpha
    r = ratio
    return a * r * r * (-3 * a + 4 * r) % p


def ratio_surface_uv_discriminant_at_beta_infinity(
    p: int,
    alpha: int,
    ratio: int,
) -> int:
    a = alpha
    r = ratio
    return r * (4 * a - 3 * r) % p


def ratio_surface_uv_sign_coefficients(
    p: int,
    alpha: int,
    ratio: int,
) -> Tuple[int, int, int]:
    a = alpha
    r = ratio
    return (
        (4 * a - 3 * r) % p,
        (-2 * a * r) % p,
        (-3 * a * a * r + 4 * a * r * r) % p,
    )


def ratio_surface_uv_sign_square_numerators(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> Tuple[int, int]:
    a = alpha
    b = beta
    r = ratio
    middle_numerator = (
        a * a * r
        + a * b * r
        - 2 * a * b
        - 2 * a * r * r
        + a * r
        + b * r
    ) % p
    branch_numerator = (
        r
        * (2 * a * b + a * r - 3 * a - 3 * b * r + b + 2 * r)
    ) % p
    return middle_numerator, branch_numerator


def ratio_surface_slope_blowup_strict_factors(
    p: int,
    alpha: int,
    slope: int,
) -> Dict[str, int]:
    a = alpha
    t = slope
    return {
        "A": (
            -3 * a * a * t * t
            + 3 * a * a * t
            + 3 * a * t * t
            - 5 * a * t
            + 3 * a
            + 2 * t
            - 2
        )
        % p,
        "Q": (
            3 * a * a * t * t
            - 2 * a * a * t
            - 3 * a * t * t
            + 5 * a * t
            - 2 * a
            - 3 * t
            + 3
        )
        % p,
        "K": (3 * a * t * t - a * t + t - 1) % p,
        "diag": (1 - t) % p,
        "M": (4 * a * t * t - 3 * a * t + 3 * t - 3) % p,
        "H": (9 * a * t * t - 8 * a * t + 8 * t - 8) % p,
    }


def ratio_surface_slope_blowup_strict_derivatives(
    p: int,
    alpha: int,
    slope: int,
) -> Dict[str, Tuple[int, int]]:
    a = alpha
    t = slope
    return {
        "A": (
            (-6 * a * t * t + 6 * a * t + 3 * t * t - 5 * t + 3) % p,
            (-(a - 1) * (6 * a * t - 3 * a + 2)) % p,
        ),
        "Q": (
            ((3 * t - 2) * (2 * a * t - t + 1)) % p,
            ((a - 1) * (6 * a * t - 2 * a + 3)) % p,
        ),
        "K": (
            (t * (3 * t - 1)) % p,
            (6 * a * t - a + 1) % p,
        ),
        "diag": (0, -1 % p),
        "M": (
            (t * (4 * t - 3)) % p,
            (8 * a * t - 3 * a + 3) % p,
        ),
        "H": (
            (t * (9 * t - 8)) % p,
            (2 * (9 * a * t - 4 * a + 4)) % p,
        ),
    }


def ratio_surface_slope_blowup_pair_support(
    p: int,
    first: str,
    second: str,
    slope: int,
) -> int:
    t = slope
    pair = (first, second)
    support = {
        ("A", "Q"): t * t * (t - 1) * (6 * t * t - 10 * t + 5),
        ("A", "K"): t * t * (t - 1) * (t + 1) * (3 * t - 2),
        ("A", "diag"): (t - 1) * (t - 1),
        ("A", "M"): t * t * (t - 1) * (2 * t - 3) * (2 * t - 3),
        ("A", "H"): t * t * (t - 1) * (3 * t - 2) * (3 * t - 2),
        ("Q", "K"): t * t * (t - 1) * (2 * t - 1) * (3 * t + 1),
        ("Q", "diag"): (t - 1) * (t - 1),
        ("Q", "M"): t * t * (t - 1) * (2 * t - 1) * (2 * t - 1),
        ("Q", "H"): t * t * (t - 1) * (3 * t - 4) * (3 * t - 4),
        ("K", "diag"): 1 - t,
        ("K", "M"): 5 * t * t * (t - 1),
        ("K", "H"): 15 * t * t * (t - 1),
        ("diag", "M"): 1 - t,
        ("diag", "H"): 1 - t,
        ("M", "H"): 5 * t * t * (t - 1),
    }[pair]
    return support % p


def ratio_surface_reciprocal_blowup_strict_factors(
    p: int,
    ratio: int,
    reciprocal_slope: int,
) -> Dict[str, int]:
    r = ratio
    s = reciprocal_slope
    return {
        "A": (
            3 * r * r * s * s
            - 3 * r * r * s
            - 3 * r * s * s
            + 7 * r * s
            - 3 * r
            - 3 * s
            + 3
        )
        % p,
        "Q": (
            -2 * r * r * s * s
            + 3 * r * r * s
            + 2 * r * s * s
            - 5 * r * s
            + 3 * r
            + 3 * s
            - 3
        )
        % p,
        "K": (-r * s * s + 3 * r * s - 3 * s + 3) % p,
        "diag": (s - 1) % p,
        "M": (-3 * r * s * s + 4 * r * s - 4 * s + 4) % p,
        "H": (-8 * r * s * s + 9 * r * s - 9 * s + 9) % p,
    }


def ratio_surface_reciprocal_blowup_strict_derivatives(
    p: int,
    ratio: int,
    reciprocal_slope: int,
) -> Dict[str, Tuple[int, int]]:
    r = ratio
    s = reciprocal_slope
    return {
        "A": (
            (6 * r * s * s - 6 * r * s - 3 * s * s + 7 * s - 3) % p,
            (6 * r * r * s - 3 * r * r - 6 * r * s + 7 * r - 3) % p,
        ),
        "Q": (
            (-(2 * s - 3) * (2 * r * s - s + 1)) % p,
            (-4 * r * r * s + 3 * r * r + 4 * r * s - 5 * r + 3) % p,
        ),
        "K": (
            (-s * (s - 3)) % p,
            (-2 * r * s + 3 * r - 3) % p,
        ),
        "diag": (0, 1 % p),
        "M": (
            (-s * (3 * s - 4)) % p,
            (-2 * (3 * r * s - 2 * r + 2)) % p,
        ),
        "H": (
            (-s * (8 * s - 9)) % p,
            (-16 * r * s + 9 * r - 9) % p,
        ),
    }


def ratio_surface_reciprocal_blowup_pair_support(
    p: int,
    first: str,
    second: str,
    reciprocal_slope: int,
) -> int:
    s = reciprocal_slope
    pair = (first, second)
    support = {
        ("A", "Q"): 3 * s * s * s * (s - 1) * (5 * s * s - 10 * s + 6),
        ("A", "K"): 3 * s * s * (s - 1) * (s + 1) * (2 * s - 3),
        ("A", "diag"): (s - 1) * (s - 1),
        ("A", "M"): s * s * (s - 1) * (3 * s - 2) * (3 * s - 2),
        ("A", "H"): 6 * s * s * (s - 1) * (2 * s - 3) * (2 * s - 3),
        ("Q", "K"): -3 * s * s * (s - 2) * (s - 1) * (s + 3),
        ("Q", "diag"): (s - 1) * (s - 1),
        ("Q", "M"): 3 * s * s * (s - 2) * (s - 2) * (s - 1),
        ("Q", "H"): 3 * s * s * (s - 1) * (4 * s - 3) * (4 * s - 3),
        ("K", "diag"): s - 1,
        ("K", "M"): -5 * s * s * (s - 1),
        ("K", "H"): -15 * s * s * (s - 1),
        ("diag", "M"): s - 1,
        ("diag", "H"): s - 1,
        ("M", "H"): -5 * s * s * (s - 1),
    }[pair]
    return support % p


def ratio_surface_branch_m_param(p: int, slope: int) -> Tuple[int, int]:
    denominator = slope * (4 * slope - 3) % p
    if denominator == 0:
        return (0, 0)
    alpha = -3 * (slope - 1) * pow(denominator, -1, p) % p
    ratio_denominator = (4 * slope - 3) % p
    ratio = (
        -4
        * slope
        * (slope - 1)
        * pow(ratio_denominator, -1, p)
    ) % p
    return alpha, ratio


def ratio_surface_branch_h_param(p: int, slope: int) -> Tuple[int, int]:
    denominator = slope * (9 * slope - 8) % p
    if denominator == 0:
        return (0, 0)
    alpha = -8 * (slope - 1) * pow(denominator, -1, p) % p
    ratio_denominator = (9 * slope - 8) % p
    ratio = (
        -9
        * slope
        * (slope - 1)
        * pow(ratio_denominator, -1, p)
    ) % p
    return alpha, ratio


def ratio_surface_beta_discriminant(p: int, alpha: int, ratio: int) -> int:
    quadratic, linear, constant = ratio_surface_beta_coefficients(
        p,
        alpha,
        ratio,
    )
    return (linear * linear - 4 * quadratic * constant) % p


def ratio_surface_beta_derivative(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> int:
    quadratic, linear, _ = ratio_surface_beta_coefficients(
        p,
        alpha,
        ratio,
    )
    return (2 * quadratic * beta + linear) % p


def ratio_surface_beta_normalized_y(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> int:
    quadratic, linear, _ = ratio_surface_beta_coefficients(
        p,
        alpha,
        ratio,
    )
    return (2 * quadratic * beta + linear) % p


def ratio_surface_beta_from_normalized_y(
    p: int,
    alpha: int,
    normalized_y: int,
    ratio: int,
) -> int:
    quadratic, linear, _ = ratio_surface_beta_coefficients(
        p,
        alpha,
        ratio,
    )
    return (normalized_y - linear) * pow(2 * quadratic, -1, p) % p


def ratio_surface_beta_normalized_y_roots(
    p: int,
    alpha: int,
    ratio: int,
) -> List[int]:
    discriminant = ratio_surface_beta_discriminant(p, alpha, ratio)
    return [value for value in range(p) if value * value % p == discriminant]


def ratio_surface_beta_vertical_branch_polynomial(
    p: int,
    alpha: int,
    ratio: int,
) -> int:
    return (
        alpha
        * ratio_surface_beta_middle_factor(p, alpha, ratio)
        * ratio_surface_beta_branch_factor(p, alpha, ratio)
    ) % p


def ratio_surface_beta_vertical_branch_derivative(
    p: int,
    alpha: int,
    ratio: int,
) -> int:
    middle = ratio_surface_beta_middle_factor(p, alpha, ratio)
    branch = ratio_surface_beta_branch_factor(p, alpha, ratio)
    middle_alpha_derivative = ratio_surface_beta_middle_factor_derivatives(
        p,
        alpha,
        ratio,
    )[0]
    branch_alpha_derivative = ratio_surface_beta_branch_factor_derivatives(
        p,
        alpha,
        ratio,
    )[0]
    return (
        middle * branch
        + alpha * middle_alpha_derivative * branch
        + alpha * middle * branch_alpha_derivative
    ) % p


def ratio_surface_beta_vertical_pencil_bad_factor(p: int, ratio: int) -> int:
    r = ratio
    return (r - 1) * (r * r + r + 1) * (9 * r * r + 14 * r + 9) % p


def ratio_surface_beta_vertical_boundary_support(
    p: int,
    label: str,
    ratio: int,
) -> int:
    r = ratio
    support = {
        "A": (r - 1) * (r + 1),
        "Q": (r - 1) * (r + 1),
        "K": r - 1,
        "diag": r - 1,
        "B": (r - 1) * (r + 1),
    }[label]
    return support % p


def ratio_surface_beta_vertical_boundary_value(
    p: int,
    label: str,
    alpha: int,
    ratio: int,
) -> int:
    if label == "A":
        return ratio_surface_beta_coefficients(p, alpha, ratio)[0]
    if label == "Q":
        return ratio_surface_beta_zero_factor(p, alpha, ratio)
    if label == "K":
        return ratio_surface_lower_alpha_kernel(p, alpha, ratio)
    if label == "diag":
        return (alpha - ratio) % p
    if label == "B":
        return (alpha - 1) * (ratio + 1) % p
    raise AssertionError(label)


def ratio_surface_projective_beta_root_count(
    p: int,
    alpha: int,
    ratio: int,
) -> int:
    quadratic, linear, constant = ratio_surface_beta_coefficients(
        p,
        alpha,
        ratio,
    )
    count = int(quadratic == 0)
    for beta in range(p):
        if (quadratic * beta * beta + linear * beta + constant) % p == 0:
            count += 1
    return count


def ratio_surface_affine_beta_roots(
    p: int,
    alpha: int,
    ratio: int,
) -> List[int]:
    return [
        beta
        for beta in range(1, p)
        if ratio_surface_delta(p, alpha, beta, ratio) == 0
    ]


def ratio_surface_beta_pushforward_good(
    p: int,
    alpha: int,
    ratio: int,
) -> bool:
    quadratic, _, constant = ratio_surface_beta_coefficients(
        p,
        alpha,
        ratio,
    )
    return (
        quadratic != 0
        and constant != 0
        and ratio_surface_beta_discriminant(p, alpha, ratio) != 0
        and (alpha - ratio) % p != 0
        and ratio_surface_lower_alpha_kernel(p, alpha, ratio) != 0
    )


def ratio_surface_beta_ratio_resonance(
    p: int,
    alpha: int,
    ratio: int,
    beta_ratio: int,
) -> int:
    quadratic, linear, constant = ratio_surface_beta_coefficients(
        p,
        alpha,
        ratio,
    )
    return (
        beta_ratio * linear * linear
        - quadratic * constant * (1 + beta_ratio) * (1 + beta_ratio)
    ) % p


def verify_ratio_surface_beta_ratio_resonance() -> List[
    Tuple[int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        max_count = 0
        max_ratio = 0
        split_pair_checks = 0
        for beta_ratio in range(1, p):
            count = 0
            for alpha in range(1, p):
                for ratio in range(1, p):
                    if not ratio_surface_beta_pushforward_good(p, alpha, ratio):
                        continue
                    if (
                        ratio_surface_beta_ratio_resonance(
                            p,
                            alpha,
                            ratio,
                            beta_ratio,
                        )
                        == 0
                    ):
                        count += 1
            if count > max_count:
                max_count = count
                max_ratio = beta_ratio
            if beta_ratio == p - 1 and count > 2 * (p - 1):
                raise AssertionError((p, beta_ratio, count, "minus-one"))
        if max_count > 4 * (p - 1):
            raise AssertionError((p, max_ratio, max_count))

        for alpha in range(1, p):
            for ratio in range(1, p):
                if not ratio_surface_beta_pushforward_good(p, alpha, ratio):
                    continue
                if legendre(ratio_surface_beta_discriminant(p, alpha, ratio), p) != 1:
                    continue
                roots = ratio_surface_affine_beta_roots(p, alpha, ratio)
                if len(roots) != 2:
                    raise AssertionError((p, alpha, ratio, roots))
                root_ratio = roots[0] * pow(roots[1], -1, p) % p
                inverse_ratio = pow(root_ratio, -1, p)
                if ratio_surface_beta_ratio_resonance(
                    p,
                    alpha,
                    ratio,
                    root_ratio,
                ) != 0:
                    raise AssertionError((p, alpha, ratio, roots, root_ratio))
                if ratio_surface_beta_ratio_resonance(
                    p,
                    alpha,
                    ratio,
                    inverse_ratio,
                ) != 0:
                    raise AssertionError((p, alpha, ratio, roots, inverse_ratio))
                split_pair_checks += 1
        checked.append((p, max_ratio, max_count, split_pair_checks))
    return checked


def verify_ratio_surface_beta_quotient_energy() -> List[
    Tuple[int, int, int, int, int, int, float]
]:
    checked: List[Tuple[int, int, int, int, int, int, float]] = []
    for p, suborder in RATIO_SURFACE_CASES:
        logs = log_table(p)
        table = character_table(p, logs)
        lift = (p - 1) // suborder
        kernel_size = (p - 1) // suborder
        split_count = 0
        same_quotient_count = 0
        exact_energy = 0.0
        for alpha in range(1, p):
            for ratio in range(1, p):
                if not ratio_surface_beta_pushforward_good(p, alpha, ratio):
                    continue
                if legendre(ratio_surface_beta_discriminant(p, alpha, ratio), p) != 1:
                    continue
                roots = ratio_surface_affine_beta_roots(p, alpha, ratio)
                if len(roots) != 2:
                    raise AssertionError((p, suborder, alpha, ratio, roots))
                root_ratio = roots[0] * pow(roots[1], -1, p) % p
                same_quotient = int(logs[root_ratio] % suborder == 0)
                same_quotient_count += same_quotient
                split_count += 1
                for exponent in range(1, suborder):
                    phi = table[lift * exponent]
                    exact_energy += abs(phi[roots[0]] + phi[roots[1]]) ** 2
        formula_energy = (
            (2 * suborder - 4) * split_count
            + 2 * suborder * same_quotient_count
        )
        if abs(exact_energy - formula_energy) > 1000 * TOLERANCE:
            raise AssertionError((p, suborder, exact_energy, formula_energy))
        quotient_collision_bound = 4 * (p - 1) * kernel_size
        if same_quotient_count > quotient_collision_bound:
            raise AssertionError(
                (p, suborder, same_quotient_count, quotient_collision_bound)
            )
        energy_bound = (
            (2 * suborder - 4) * (p - 1) * (p - 1)
            + 2 * suborder * quotient_collision_bound
        )
        if formula_energy > energy_bound:
            raise AssertionError((p, suborder, formula_energy, energy_bound))
        checked.append(
            (
                p,
                suborder,
                split_count,
                same_quotient_count,
                round(formula_energy),
                energy_bound,
                round(formula_energy / ((p - 1) * (p - 1)), 10),
            )
        )
    return checked


def verify_ratio_surface_beta_etale_cover() -> List[Tuple[int, int, int, int, int]]:
    checked: List[Tuple[int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        good_base_count = 0
        split_base_count = 0
        nonsplit_base_count = 0
        root_checks = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                if not ratio_surface_beta_pushforward_good(p, alpha, ratio):
                    continue
                good_base_count += 1
                discriminant = ratio_surface_beta_discriminant(p, alpha, ratio)
                if discriminant == 0:
                    raise AssertionError((p, alpha, ratio, "branch"))
                root_class = legendre(discriminant, p)
                if root_class == -1:
                    nonsplit_base_count += 1
                    if ratio_surface_affine_beta_roots(p, alpha, ratio):
                        raise AssertionError((p, alpha, ratio, "nonsplit"))
                    continue
                split_base_count += 1
                roots = ratio_surface_affine_beta_roots(p, alpha, ratio)
                if len(roots) != 2:
                    raise AssertionError((p, alpha, ratio, roots))
                for beta in roots:
                    derivative = ratio_surface_beta_derivative(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    if derivative == 0:
                        raise AssertionError((p, alpha, beta, ratio, "ramified"))
                    if derivative * derivative % p != discriminant:
                        raise AssertionError(
                            (p, alpha, beta, ratio, derivative, discriminant)
                        )
                    root_checks += 1
        if good_base_count != split_base_count + nonsplit_base_count:
            raise AssertionError((p, good_base_count, split_base_count))
        checked.append(
            (
                p,
                good_base_count,
                split_base_count,
                nonsplit_base_count,
                root_checks,
            )
        )
    return checked


def verify_ratio_surface_beta_square_root_normalization() -> Tuple[
    List[Tuple[int, int, int, int, int]],
    List[Tuple[int, int, int, int, int, float]],
]:
    algebraic_checked: List[Tuple[int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        good_base_count = 0
        split_base_count = 0
        beta_to_y_checks = 0
        y_to_beta_checks = 0
        numerator_nonzero_checks = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                if not ratio_surface_beta_pushforward_good(p, alpha, ratio):
                    continue
                good_base_count += 1
                quadratic, linear, _ = ratio_surface_beta_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                discriminant = ratio_surface_beta_discriminant(
                    p,
                    alpha,
                    ratio,
                )
                beta_roots = ratio_surface_affine_beta_roots(
                    p,
                    alpha,
                    ratio,
                )
                y_roots = ratio_surface_beta_normalized_y_roots(
                    p,
                    alpha,
                    ratio,
                )
                if legendre(discriminant, p) == -1:
                    if beta_roots or y_roots:
                        raise AssertionError((p, alpha, ratio, "nonsplit"))
                    continue
                split_base_count += 1
                if len(beta_roots) != 2 or len(y_roots) != 2:
                    raise AssertionError((p, alpha, ratio, beta_roots, y_roots))
                y_from_beta = sorted(
                    ratio_surface_beta_normalized_y(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    for beta in beta_roots
                )
                if y_from_beta != sorted(y_roots):
                    raise AssertionError((p, alpha, ratio, y_from_beta, y_roots))
                beta_to_y_checks += len(beta_roots)
                for y_value in y_roots:
                    beta = ratio_surface_beta_from_normalized_y(
                        p,
                        alpha,
                        y_value,
                        ratio,
                    )
                    if beta not in beta_roots:
                        raise AssertionError((p, alpha, ratio, y_value, beta))
                    if (
                        ratio_surface_beta_normalized_y(
                            p,
                            alpha,
                            beta,
                            ratio,
                        )
                        != y_value
                    ):
                        raise AssertionError((p, alpha, ratio, y_value, beta))
                    if (y_value - linear) % p != 2 * quadratic * beta % p:
                        raise AssertionError((p, alpha, ratio, y_value, beta))
                    if (y_value - linear) % p == 0:
                        raise AssertionError((p, alpha, ratio, y_value, beta))
                    y_to_beta_checks += 1
                    numerator_nonzero_checks += 1
        algebraic_checked.append(
            (
                p,
                good_base_count,
                split_base_count,
                beta_to_y_checks,
                numerator_nonzero_checks,
            )
        )

    trace_checked: List[Tuple[int, int, int, int, int, float]] = []
    for p, psi_exponent, phi_exponent in PUSHFORWARD_TRACE_CASES:
        logs = log_table(p)
        table = character_table(p, logs)
        psi = table[psi_exponent]
        phi = table[phi_exponent]
        good_base_count = 0
        normalized_point_checks = 0
        max_error = 0.0
        for alpha in range(1, p):
            for ratio in range(1, p):
                if not ratio_surface_beta_pushforward_good(p, alpha, ratio):
                    continue
                good_base_count += 1
                quadratic, linear, _ = ratio_surface_beta_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                beta_roots = ratio_surface_affine_beta_roots(
                    p,
                    alpha,
                    ratio,
                )
                y_roots = ratio_surface_beta_normalized_y_roots(
                    p,
                    alpha,
                    ratio,
                )
                base_twist = (
                    psi[alpha]
                    * legendre(
                        ratio
                        * ratio_surface_beta_middle_factor(p, alpha, ratio),
                        p,
                    )
                )
                beta_trace = base_twist * sum(phi[beta] for beta in beta_roots)
                normalized_trace = (
                    base_twist
                    * phi[pow(2 * quadratic, -1, p)]
                    * sum(phi[(y_value - linear) % p] for y_value in y_roots)
                )
                error = abs(beta_trace - normalized_trace)
                max_error = max(max_error, error)
                if error > 1000 * TOLERANCE:
                    raise AssertionError(
                        (
                            p,
                            psi_exponent,
                            phi_exponent,
                            alpha,
                            ratio,
                            beta_trace,
                            normalized_trace,
                        )
                    )
                normalized_point_checks += len(y_roots)
        trace_checked.append(
            (
                p,
                psi_exponent,
                phi_exponent,
                good_base_count,
                normalized_point_checks,
                round(max_error, 12),
            )
        )

    return algebraic_checked, trace_checked


def verify_ratio_surface_beta_vertical_pencil_ledger() -> List[
    Tuple[int, int, int, int, int, int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int, int, int, int, int, int]] = []
    boundary_labels = ("A", "Q", "K", "diag", "B")
    for p in LOWER_CHART_PRIMES:
        if p <= 5:
            continue
        bad_ratio_count = 0
        generic_ratio_count = 0
        generic_singular_roots = 0
        boundary_hits: Dict[str, int] = {label: 0 for label in boundary_labels}
        formula_checks = 0
        for ratio in range(1, p):
            if 24 * ratio * ratio % p == 0:
                raise AssertionError((p, ratio, "vertical_leading_coefficient"))
            bad_ratio = (
                ratio_surface_beta_vertical_pencil_bad_factor(p, ratio) == 0
            )
            bad_ratio_count += int(bad_ratio)
            generic_ratio_count += int(not bad_ratio)
            for alpha in range(p):
                branch_value = ratio_surface_beta_vertical_branch_polynomial(
                    p,
                    alpha,
                    ratio,
                )
                if branch_value != 0:
                    continue
                branch_derivative = ratio_surface_beta_vertical_branch_derivative(
                    p,
                    alpha,
                    ratio,
                )
                if branch_derivative == 0:
                    if not bad_ratio:
                        raise AssertionError(
                            (p, alpha, ratio, "unlisted_vertical_branch_collision")
                        )
                    generic_singular_roots += int(not bad_ratio)
                for label in boundary_labels:
                    if (
                        ratio_surface_beta_vertical_boundary_value(
                            p,
                            label,
                            alpha,
                            ratio,
                        )
                        != 0
                    ):
                        continue
                    boundary_hits[label] += 1
                    if (
                        ratio_surface_beta_vertical_boundary_support(
                            p,
                            label,
                            ratio,
                        )
                        != 0
                    ):
                        raise AssertionError(
                            (
                                p,
                                alpha,
                                ratio,
                                label,
                                "unlisted_vertical_branch_boundary",
                            )
                        )
                formula_checks += 1
        checked.append(
            (
                p,
                bad_ratio_count,
                generic_ratio_count,
                generic_singular_roots,
                boundary_hits["A"],
                boundary_hits["Q"],
                boundary_hits["K"],
                boundary_hits["diag"],
                boundary_hits["B"],
                formula_checks,
            )
        )
    return checked


def verify_ratio_surface_beta_pushforward_trace() -> List[
    Tuple[int, int, int, int, int, int, float]
]:
    checked: List[Tuple[int, int, int, int, int, int, float]] = []
    for p, psi_exponent, phi_exponent in PUSHFORWARD_TRACE_CASES:
        logs = log_table(p)
        table = character_table(p, logs)
        psi = table[psi_exponent]
        phi = table[phi_exponent]
        direct = 0j
        pushforward = 0j
        exceptional = 0j
        good_base_count = 0
        good_point_count = 0
        exceptional_point_count = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                roots = ratio_surface_affine_beta_roots(p, alpha, ratio)
                main_roots = [
                    beta
                    for beta in roots
                    if ratio_surface_binary_discriminants(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )[0] != 0
                ]
                direct += psi[alpha] * sum(
                    legendre(
                        ratio_surface_binary_discriminants(
                            p,
                            alpha,
                            beta,
                            ratio,
                        )[0],
                        p,
                    )
                    * phi[beta]
                    for beta in main_roots
                )
                if ratio_surface_beta_pushforward_good(p, alpha, ratio):
                    good_base_count += 1
                    if len(main_roots) not in (0, 2):
                        raise AssertionError((p, alpha, ratio, main_roots))
                    if not main_roots:
                        continue
                    signs = [
                        legendre(
                            ratio_surface_binary_discriminants(
                                p,
                                alpha,
                                beta,
                                ratio,
                            )[0],
                            p,
                        )
                        for beta in main_roots
                    ]
                    if signs[0] != signs[1]:
                        raise AssertionError((p, alpha, ratio, main_roots, signs))
                    good_point_count += len(main_roots)
                    pushforward += (
                        psi[alpha]
                        * signs[0]
                        * sum(phi[beta] for beta in main_roots)
                    )
                    continue
                exceptional_point_count += len(main_roots)
                exceptional += psi[alpha] * sum(
                    legendre(
                        ratio_surface_binary_discriminants(
                            p,
                            alpha,
                            beta,
                            ratio,
                        )[0],
                        p,
                    )
                    * phi[beta]
                    for beta in main_roots
                )
        if exceptional_point_count > 20 * (p - 1):
            raise AssertionError((p, exceptional_point_count))
        error = abs(direct - pushforward - exceptional)
        if error > 1000 * TOLERANCE:
            raise AssertionError(
                (p, psi_exponent, phi_exponent, direct, pushforward, exceptional)
            )
        checked.append(
            (
                p,
                psi_exponent,
                phi_exponent,
                good_base_count,
                good_point_count,
                exceptional_point_count,
                round(error, 12),
            )
        )
    return checked


def verify_ratio_surface_exceptional_root_bound() -> List[
    Tuple[int, int, int, int, int, int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int, int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        infinity_base_count = 0
        zero_base_count = 0
        branch_base_count = 0
        diagonal_base_count = 0
        lower_alpha_base_count = 0
        nonvertical_exceptional_root_count = 0
        vertical_tail_count = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                is_vertical = (alpha, ratio) == (1, 1)
                quadratic, _, constant = ratio_surface_beta_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                discriminant = ratio_surface_beta_discriminant(
                    p,
                    alpha,
                    ratio,
                )
                lower_kernel = ratio_surface_lower_alpha_kernel(
                    p,
                    alpha,
                    ratio,
                )
                if not is_vertical:
                    infinity_base_count += int(quadratic == 0)
                    zero_base_count += int(constant == 0)
                    branch_base_count += int(discriminant == 0)
                    diagonal_base_count += int((alpha - ratio) % p == 0)
                    lower_alpha_base_count += int(lower_kernel == 0)
                for beta in ratio_surface_affine_beta_roots(p, alpha, ratio):
                    coefficients = ratio_surface_conic_coefficients(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    chart, _ = projective_excess_chart(p, coefficients)
                    discriminants = ratio_surface_binary_discriminants(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    if chart == "zero" or discriminants[0] == 0:
                        continue
                    if ratio_surface_beta_pushforward_good(p, alpha, ratio):
                        continue
                    if is_vertical:
                        vertical_tail_count += 1
                    else:
                        nonvertical_exceptional_root_count += 1
        if infinity_base_count > 2 * (p - 1):
            raise AssertionError((p, "A_beta", infinity_base_count))
        if zero_base_count > 2 * (p - 1):
            raise AssertionError((p, "C_beta", zero_base_count))
        if branch_base_count > 4 * (p - 1):
            raise AssertionError((p, "D_beta", branch_base_count))
        if diagonal_base_count > p - 1:
            raise AssertionError((p, "diagonal", diagonal_base_count))
        if lower_alpha_base_count > 2 * (p - 1):
            raise AssertionError((p, "K_alpha", lower_alpha_base_count))
        root_bound = (
            infinity_base_count
            + zero_base_count
            + branch_base_count
            + 2 * diagonal_base_count
            + 2 * lower_alpha_base_count
        )
        if root_bound > 14 * (p - 1):
            raise AssertionError((p, root_bound))
        if nonvertical_exceptional_root_count > root_bound:
            raise AssertionError(
                (p, nonvertical_exceptional_root_count, root_bound)
            )
        if vertical_tail_count != p - 2:
            raise AssertionError((p, vertical_tail_count))
        checked.append(
            (
                p,
                infinity_base_count,
                zero_base_count,
                branch_base_count,
                diagonal_base_count,
                lower_alpha_base_count,
                nonvertical_exceptional_root_count,
                vertical_tail_count,
                root_bound,
                14 * (p - 1),
            )
        )
    return checked


def verify_ratio_surface_beta_pushforward_determinant() -> List[
    Tuple[int, int, int, int, int, float]
]:
    checked: List[Tuple[int, int, int, int, int, float]] = []
    for p, psi_exponent, phi_exponent in PUSHFORWARD_TRACE_CASES:
        logs = log_table(p)
        table = character_table(p, logs)
        psi = table[psi_exponent]
        phi = table[phi_exponent]
        split_fiber_count = 0
        determinant_checks = 0
        max_error = 0.0
        for alpha in range(1, p):
            for ratio in range(1, p):
                if not ratio_surface_beta_pushforward_good(p, alpha, ratio):
                    continue
                if legendre(ratio_surface_beta_discriminant(p, alpha, ratio), p) != 1:
                    continue
                roots = ratio_surface_affine_beta_roots(p, alpha, ratio)
                if len(roots) != 2:
                    raise AssertionError((p, alpha, ratio, roots))
                quadratic, _, constant = ratio_surface_beta_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                beta_product = roots[0] * roots[1] % p
                expected_product = constant * pow(quadratic, -1, p) % p
                if beta_product != expected_product:
                    raise AssertionError(
                        (p, alpha, ratio, roots, beta_product, expected_product)
                    )
                signs = [
                    legendre(
                        ratio_surface_binary_discriminants(
                            p,
                            alpha,
                            beta,
                            ratio,
                        )[0],
                        p,
                    )
                    for beta in roots
                ]
                if signs[0] != signs[1] or signs[0] == 0:
                    raise AssertionError((p, alpha, ratio, roots, signs))
                sheet_product = (
                    psi[alpha]
                    * signs[0]
                    * phi[roots[0]]
                    * psi[alpha]
                    * signs[1]
                    * phi[roots[1]]
                )
                base_determinant = psi[alpha] * psi[alpha] * phi[expected_product]
                error = abs(sheet_product - base_determinant)
                max_error = max(max_error, error)
                if error > 1000 * TOLERANCE:
                    raise AssertionError(
                        (
                            p,
                            psi_exponent,
                            phi_exponent,
                            alpha,
                            ratio,
                            sheet_product,
                            base_determinant,
                        )
                    )
                split_fiber_count += 1
                determinant_checks += 1
        checked.append(
            (
                p,
                psi_exponent,
                phi_exponent,
                split_fiber_count,
                determinant_checks,
                round(max_error, 12),
            )
        )
    return checked


def verify_ratio_surface_full_trace_reduction() -> List[
    Tuple[int, int, int, int, int, int, int, float, int]
]:
    checked: List[Tuple[int, int, int, int, int, int, int, float, int]] = []
    for p, psi_exponent, phi_exponent in PUSHFORWARD_TRACE_CASES:
        logs = log_table(p)
        table = character_table(p, logs)
        psi = table[psi_exponent]
        phi = table[phi_exponent]
        direct = 0j
        zero = 0j
        lower = 0j
        good = 0j
        grouped_good = 0j
        exceptional = 0j
        zero_count = 0
        lower_count = 0
        good_base_count = 0
        good_point_count = 0
        exceptional_point_count = 0
        nonvertical_exceptional_point_count = 0
        vertical_exceptional = 0j
        for alpha in range(1, p):
            for ratio in range(1, p):
                roots = ratio_surface_affine_beta_roots(p, alpha, ratio)
                is_good_base = ratio_surface_beta_pushforward_good(
                    p,
                    alpha,
                    ratio,
                )
                good_roots: List[Tuple[int, int]] = []
                if is_good_base:
                    good_base_count += 1
                for beta in roots:
                    coefficients = ratio_surface_conic_coefficients(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    chart, unit = projective_excess_chart(p, coefficients)
                    term = unit * psi[alpha] * phi[beta]
                    direct += term
                    if chart == "zero":
                        zero_count += 1
                        zero += term
                        if (alpha, beta, ratio, unit) != (1, 1, 1, p):
                            raise AssertionError(
                                (p, alpha, beta, ratio, chart, unit)
                            )
                        continue

                    discriminants = ratio_surface_binary_discriminants(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    if discriminants[0] == 0:
                        lower_count += 1
                        lower += term
                        continue

                    if is_good_base:
                        if unit != legendre(discriminants[0], p):
                            raise AssertionError(
                                (p, alpha, beta, ratio, unit, discriminants)
                            )
                        good_point_count += 1
                        good_roots.append((beta, unit))
                        good += term
                        continue

                    exceptional_point_count += 1
                    if (alpha, ratio) == (1, 1):
                        vertical_exceptional += term
                    else:
                        nonvertical_exceptional_point_count += 1
                    exceptional += term

                if not is_good_base or not good_roots:
                    continue
                if len(good_roots) != 2:
                    raise AssertionError((p, alpha, ratio, good_roots))
                signs = [unit for _, unit in good_roots]
                if signs[0] != signs[1]:
                    raise AssertionError((p, alpha, ratio, good_roots))
                grouped_good += psi[alpha] * signs[0] * sum(
                    phi[beta] for beta, _ in good_roots
                )

        error = abs(direct - zero - lower - good - exceptional)
        if error > 1000 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    psi_exponent,
                    phi_exponent,
                    direct,
                    zero,
                    lower,
                    good,
                    exceptional,
                )
            )
        grouped_error = abs(good - grouped_good)
        if grouped_error > 1000 * TOLERANCE:
            raise AssertionError((p, psi_exponent, phi_exponent, grouped_error))
        if zero_count != 1:
            raise AssertionError((p, psi_exponent, phi_exponent, zero_count))
        if lower_count > 5 * (p - 1):
            raise AssertionError((p, psi_exponent, phi_exponent, lower_count))
        if nonvertical_exceptional_point_count > 14 * (p - 1):
            raise AssertionError(
                (
                    p,
                    psi_exponent,
                    phi_exponent,
                    nonvertical_exceptional_point_count,
                )
            )
        if abs(zero + vertical_exceptional) > p + 1000 * TOLERANCE:
            raise AssertionError(
                (p, psi_exponent, phi_exponent, zero, vertical_exceptional)
            )
        bad_bound = p + lower_count + nonvertical_exceptional_point_count
        if abs(zero + lower + exceptional) > bad_bound + 1000 * TOLERANCE:
            raise AssertionError(
                (p, psi_exponent, phi_exponent, zero, lower, exceptional)
            )
        if bad_bound > p + 19 * (p - 1):
            raise AssertionError((p, psi_exponent, phi_exponent, bad_bound))
        checked.append(
            (
                p,
                psi_exponent,
                phi_exponent,
                good_base_count,
                good_point_count,
                lower_count,
                exceptional_point_count,
                round(error + grouped_error, 12),
                bad_bound,
            )
        )
    return checked


def verify_ratio_surface_quotient_trace_reduction() -> List[
    Tuple[int, int, int, int, int, float, float, float, float, float, float]
]:
    checked: List[
        Tuple[int, int, int, int, int, float, float, float, float, float, float]
    ] = []
    for p, suborder in RATIO_SURFACE_CASES:
        logs = log_table(p)
        direct_matrix = [[0 for _ in range(suborder)] for _ in range(suborder)]
        zero_matrix = [[0 for _ in range(suborder)] for _ in range(suborder)]
        lower_matrix = [[0 for _ in range(suborder)] for _ in range(suborder)]
        good_matrix = [[0 for _ in range(suborder)] for _ in range(suborder)]
        exceptional_matrix = [
            [0 for _ in range(suborder)] for _ in range(suborder)
        ]
        zero_count = 0
        lower_count = 0
        good_point_count = 0
        exceptional_point_count = 0
        nonvertical_exceptional_point_count = 0
        for alpha in range(1, p):
            alpha_label = logs[alpha] % suborder
            for ratio in range(1, p):
                roots = ratio_surface_affine_beta_roots(p, alpha, ratio)
                is_good_base = ratio_surface_beta_pushforward_good(
                    p,
                    alpha,
                    ratio,
                )
                for beta in roots:
                    beta_label = logs[beta] % suborder
                    coefficients = ratio_surface_conic_coefficients(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    chart, unit = projective_excess_chart(p, coefficients)
                    direct_matrix[alpha_label][beta_label] += unit
                    if chart == "zero":
                        zero_count += 1
                        zero_matrix[alpha_label][beta_label] += unit
                        if (alpha, beta, ratio, unit) != (1, 1, 1, p):
                            raise AssertionError(
                                (p, suborder, alpha, beta, ratio, chart, unit)
                            )
                        continue

                    discriminants = ratio_surface_binary_discriminants(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    if discriminants[0] == 0:
                        lower_count += 1
                        lower_matrix[alpha_label][beta_label] += unit
                        continue

                    if is_good_base:
                        good_point_count += 1
                        good_matrix[alpha_label][beta_label] += unit
                        continue

                    exceptional_point_count += 1
                    if (alpha, ratio) != (1, 1):
                        nonvertical_exceptional_point_count += 1
                    exceptional_matrix[alpha_label][beta_label] += unit

        if zero_count != 1:
            raise AssertionError((p, suborder, zero_count))
        if lower_count > 5 * (p - 1):
            raise AssertionError((p, suborder, lower_count))
        if nonvertical_exceptional_point_count > 14 * (p - 1):
            raise AssertionError(
                (p, suborder, nonvertical_exceptional_point_count)
            )
        bad_bound = p + lower_count + nonvertical_exceptional_point_count
        if bad_bound > p + 19 * (p - 1):
            raise AssertionError((p, suborder, bad_bound))

        max_bad_two_sided_ratio = 0.0
        max_good_two_sided_ratio = 0.0
        max_good_beta2_ratio = 0.0
        max_good_left_principal_ratio = 0.0
        max_total_two_sided_ratio = 0.0
        max_recomposition_error = 0.0
        good_spectral_energy = 0.0
        root = cmath.exp(2j * math.pi / suborder)
        for left_character in range(suborder):
            for right_character in range(1, suborder):
                direct = 0j
                zero = 0j
                lower = 0j
                good = 0j
                exceptional = 0j
                for left in range(suborder):
                    for right in range(suborder):
                        character_value = root ** (
                            left_character * left
                            + right_character * right
                        )
                        direct += direct_matrix[left][right] * character_value
                        zero += zero_matrix[left][right] * character_value
                        lower += lower_matrix[left][right] * character_value
                        good += good_matrix[left][right] * character_value
                        exceptional += (
                            exceptional_matrix[left][right] * character_value
                        )
                error = abs(direct - zero - lower - good - exceptional)
                max_recomposition_error = max(max_recomposition_error, error)
                bad = zero + lower + exceptional
                if abs(bad) > bad_bound + 1000 * TOLERANCE:
                    raise AssertionError(
                        (p, suborder, left_character, right_character)
                    )
                max_good_beta2_ratio = max(max_good_beta2_ratio, abs(good) / p)
                if left_character == 0:
                    max_good_left_principal_ratio = max(
                        max_good_left_principal_ratio,
                        abs(good) / p,
                    )
                else:
                    max_bad_two_sided_ratio = max(
                        max_bad_two_sided_ratio,
                        abs(bad) / p,
                    )
                    max_good_two_sided_ratio = max(
                        max_good_two_sided_ratio,
                        abs(good) / p,
                    )
                    max_total_two_sided_ratio = max(
                        max_total_two_sided_ratio,
                        abs(direct) / p,
                    )
                    good_spectral_energy += abs(good) ** 2
        if max_recomposition_error > 1000 * TOLERANCE:
            raise AssertionError((p, suborder, max_recomposition_error))

        good_row_sums = [sum(row) for row in good_matrix]
        good_column_sums = [
            sum(good_matrix[row][column] for row in range(suborder))
            for column in range(suborder)
        ]
        good_total = sum(good_row_sums)
        good_centered_frobenius_sq = 0.0
        for row in range(suborder):
            for column in range(suborder):
                centered = (
                    good_matrix[row][column]
                    - good_row_sums[row] / suborder
                    - good_column_sums[column] / suborder
                    + good_total / (suborder * suborder)
                )
                good_centered_frobenius_sq += centered * centered
        if abs(
            good_spectral_energy / (suborder * suborder)
            - good_centered_frobenius_sq
        ) > 1000 * TOLERANCE:
            raise AssertionError(
                (p, suborder, good_spectral_energy, good_centered_frobenius_sq)
            )
        good_centered_frobenius_ratio = (
            math.sqrt(good_centered_frobenius_sq) / p
        )

        checked.append(
            (
                p,
                suborder,
                good_point_count,
                lower_count,
                exceptional_point_count,
                round(max_bad_two_sided_ratio, 10),
                round(max_good_two_sided_ratio, 10),
                round(max_good_beta2_ratio, 10),
                round(max_good_left_principal_ratio, 10),
                round(good_centered_frobenius_ratio, 10),
                round(max_total_two_sided_ratio, 10),
            )
        )
    return checked


def verify_ratio_surface_beta_kummer_conductor_ledger() -> List[
    Tuple[int, int, int, int, int, int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int, int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        beta_zero_count = 0
        beta_linear_intersection = 0
        uv_zero_intersection = 0
        infinity_intersection = 0
        branch_m_intersection = 0
        branch_h_intersection = 0
        diagonal_intersection = 0
        lower_alpha_intersection = 0
        formula_checks = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                quadratic, _, constant = ratio_surface_beta_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                zero_factor = ratio_surface_beta_zero_factor(p, alpha, ratio)
                if constant != alpha * ratio * zero_factor % p:
                    raise AssertionError((p, alpha, ratio, constant, zero_factor))
                discriminants = ratio_surface_binary_discriminants(
                    p,
                    alpha,
                    0,
                    ratio,
                )
                beta_zero_uv = ratio_surface_uv_discriminant_at_beta_zero(
                    p,
                    alpha,
                    ratio,
                )
                if discriminants[0] != beta_zero_uv:
                    raise AssertionError(
                        (p, alpha, ratio, discriminants[0], beta_zero_uv)
                    )
                formula_checks += 1
                if zero_factor != 0:
                    continue
                beta_zero_count += 1
                if (alpha - 1) * (ratio + 1) % p == 0:
                    beta_linear_intersection += 1
                    if (
                        (ratio - 1) * (ratio + 1) % p != 0
                        or (alpha - 1) * (alpha + 3) * (2 * alpha + 1) % p
                        != 0
                    ):
                        raise AssertionError((p, alpha, ratio, "B_beta"))
                if beta_zero_uv == 0:
                    uv_zero_intersection += 1
                    if (2 * ratio - 3) % p != 0 or (alpha - 2) % p != 0:
                        raise AssertionError((p, alpha, ratio, "d_uv"))
                if quadratic == 0:
                    infinity_intersection += 1
                    if (
                        (ratio - 1) * (3 * ratio * ratio + 4 * ratio + 3) % p
                        != 0
                        or (alpha - 1) * (alpha + 1) % p != 0
                    ):
                        raise AssertionError((p, alpha, ratio, "A_beta"))
                if ratio_surface_beta_middle_factor(p, alpha, ratio) == 0:
                    branch_m_intersection += 1
                    if (
                        (ratio - 1) * (ratio + 1) % p != 0
                        or (alpha - 1) * (alpha + 3) % p != 0
                    ):
                        raise AssertionError((p, alpha, ratio, "M"))
                if ratio_surface_beta_branch_factor(p, alpha, ratio) == 0:
                    branch_h_intersection += 1
                    if (
                        (ratio - 1) * (ratio + 1) % p != 0
                        or (alpha - 1) * (2 * alpha + 1) % p != 0
                    ):
                        raise AssertionError((p, alpha, ratio, "H"))
                if (alpha - ratio) % p == 0:
                    diagonal_intersection += 1
                    if (alpha - 1) % p != 0 or (ratio - 1) % p != 0:
                        raise AssertionError((p, alpha, ratio, "diagonal"))
                if ratio_surface_lower_alpha_kernel(p, alpha, ratio) == 0:
                    lower_alpha_intersection += 1
                    if (
                        (ratio - 1)
                        * (2 * ratio - 3)
                        * (3 * ratio - 2)
                        % p
                        != 0
                        or (alpha - 1) * (alpha - 2) % p != 0
                    ):
                        raise AssertionError((p, alpha, ratio, "K_alpha"))
        if beta_zero_count > 2 * (p - 1):
            raise AssertionError((p, beta_zero_count))
        for count in (
            beta_linear_intersection,
            uv_zero_intersection,
            infinity_intersection,
            branch_m_intersection,
            branch_h_intersection,
            diagonal_intersection,
            lower_alpha_intersection,
        ):
            if count > 3:
                raise AssertionError((p, count))
        checked.append(
            (
                p,
                beta_zero_count,
                beta_linear_intersection,
                uv_zero_intersection,
                infinity_intersection,
                branch_m_intersection,
                branch_h_intersection,
                diagonal_intersection,
                lower_alpha_intersection,
                formula_checks,
            )
        )
    return checked


def verify_ratio_surface_beta_infinity_conductor_ledger() -> List[
    Tuple[int, int, int, int, int, int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int, int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        beta_infinity_count = 0
        beta_linear_intersection = 0
        beta_zero_intersection = 0
        uv_infinity_intersection = 0
        branch_m_intersection = 0
        branch_h_intersection = 0
        diagonal_intersection = 0
        lower_alpha_intersection = 0
        formula_checks = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                quadratic, _, _ = ratio_surface_beta_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                infinity_uv = ratio_surface_uv_discriminant_at_beta_infinity(
                    p,
                    alpha,
                    ratio,
                )
                formula_checks += 1
                if quadratic != 0:
                    continue
                beta_infinity_count += 1
                if (alpha - 1) * (ratio + 1) % p == 0:
                    beta_linear_intersection += 1
                    if (
                        (ratio - 1) * (ratio + 1) % p != 0
                        or (alpha - 1) * (alpha + 2) * (3 * alpha + 1) % p
                        != 0
                    ):
                        raise AssertionError((p, alpha, ratio, "B_beta"))
                if ratio_surface_beta_zero_factor(p, alpha, ratio) == 0:
                    beta_zero_intersection += 1
                    if (
                        (ratio - 1) * (3 * ratio * ratio + 4 * ratio + 3) % p
                        != 0
                        or (alpha - 1) * (alpha + 1) % p != 0
                    ):
                        raise AssertionError((p, alpha, ratio, "C_beta"))
                if infinity_uv == 0:
                    uv_infinity_intersection += 1
                    if (3 * ratio - 2) % p != 0 or (2 * alpha - 1) % p != 0:
                        raise AssertionError((p, alpha, ratio, "d_uv_infinity"))
                if ratio_surface_beta_middle_factor(p, alpha, ratio) == 0:
                    branch_m_intersection += 1
                    if (
                        (ratio - 1) * (ratio + 1) % p != 0
                        or (alpha - 1) * (3 * alpha + 1) % p != 0
                    ):
                        raise AssertionError((p, alpha, ratio, "M"))
                if ratio_surface_beta_branch_factor(p, alpha, ratio) == 0:
                    branch_h_intersection += 1
                    if (
                        (ratio - 1) * (ratio + 1) % p != 0
                        or (alpha - 1) * (alpha + 2) % p != 0
                    ):
                        raise AssertionError((p, alpha, ratio, "H"))
                if (alpha - ratio) % p == 0:
                    diagonal_intersection += 1
                    if (alpha - 1) % p != 0 or (ratio - 1) % p != 0:
                        raise AssertionError((p, alpha, ratio, "diagonal"))
                if ratio_surface_lower_alpha_kernel(p, alpha, ratio) == 0:
                    lower_alpha_intersection += 1
                    if (
                        (ratio - 1)
                        * (2 * ratio - 3)
                        * (3 * ratio - 2)
                        % p
                        != 0
                        or (alpha - 1) * (2 * alpha - 1) % p != 0
                    ):
                        raise AssertionError((p, alpha, ratio, "K_alpha"))
        if beta_infinity_count > 2 * (p - 1):
            raise AssertionError((p, beta_infinity_count))
        for count in (
            beta_linear_intersection,
            beta_zero_intersection,
            uv_infinity_intersection,
            branch_m_intersection,
            branch_h_intersection,
            diagonal_intersection,
            lower_alpha_intersection,
        ):
            if count > 3:
                raise AssertionError((p, count))
        checked.append(
            (
                p,
                beta_infinity_count,
                beta_linear_intersection,
                beta_zero_intersection,
                uv_infinity_intersection,
                branch_m_intersection,
                branch_h_intersection,
                diagonal_intersection,
                lower_alpha_intersection,
                formula_checks,
            )
        )
    return checked


def verify_ratio_surface_uv_sign_divisor_deleted() -> List[
    Tuple[int, int, int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        resultant_zero_count = 0
        diagonal_support_count = 0
        lower_support_count = 0
        common_root_count = 0
        good_common_root_count = 0
        formula_checks = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                beta_coefficients = ratio_surface_beta_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                sign_coefficients = ratio_surface_uv_sign_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                resultant = quadratic_resultant(
                    p,
                    beta_coefficients,
                    sign_coefficients,
                )
                lower_kernel = ratio_surface_lower_alpha_kernel(
                    p,
                    alpha,
                    ratio,
                )
                expected = (
                    alpha
                    * alpha
                    * ratio
                    * ratio
                    * (alpha - ratio)
                    * (alpha - ratio)
                    * lower_kernel
                    * lower_kernel
                ) % p
                if resultant != expected:
                    raise AssertionError(
                        (p, alpha, ratio, resultant, expected)
                    )
                formula_checks += 1
                if resultant == 0:
                    resultant_zero_count += 1
                    diagonal_support_count += int((alpha - ratio) % p == 0)
                    lower_support_count += int(lower_kernel == 0)
                    if (alpha - ratio) % p != 0 and lower_kernel != 0:
                        raise AssertionError(
                            (p, alpha, ratio, "unsupported_resultant_zero")
                        )
                common_roots = 0
                for beta in range(p):
                    beta_value = (
                        beta_coefficients[0] * beta * beta
                        + beta_coefficients[1] * beta
                        + beta_coefficients[2]
                    ) % p
                    sign_value = (
                        sign_coefficients[0] * beta * beta
                        + sign_coefficients[1] * beta
                        + sign_coefficients[2]
                    ) % p
                    if beta_value == 0 and sign_value == 0:
                        common_roots += 1
                if common_roots:
                    common_root_count += common_roots
                    if (alpha - ratio) % p != 0 and lower_kernel != 0:
                        raise AssertionError(
                            (p, alpha, ratio, common_roots, "unsupported")
                        )
                    if ratio_surface_beta_pushforward_good(p, alpha, ratio):
                        good_common_root_count += common_roots
        if good_common_root_count != 0:
            raise AssertionError((p, good_common_root_count))
        checked.append(
            (
                p,
                resultant_zero_count,
                diagonal_support_count,
                lower_support_count,
                common_root_count,
                good_common_root_count,
                formula_checks,
            )
        )
    return checked


def verify_ratio_surface_uv_sign_base_squareclass() -> List[
    Tuple[int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        good_split_count = 0
        root_checks = 0
        middle_squareclass_matches = 0
        branch_squareclass_matches = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                if not ratio_surface_beta_pushforward_good(p, alpha, ratio):
                    continue
                if legendre(ratio_surface_beta_discriminant(p, alpha, ratio), p) != 1:
                    continue
                middle_factor = ratio_surface_beta_middle_factor(
                    p,
                    alpha,
                    ratio,
                )
                branch_factor = ratio_surface_beta_branch_factor(
                    p,
                    alpha,
                    ratio,
                )
                if middle_factor == 0 or branch_factor == 0:
                    raise AssertionError((p, alpha, ratio, "branch_on_good"))
                roots = ratio_surface_affine_beta_roots(p, alpha, ratio)
                if len(roots) != 2:
                    raise AssertionError((p, alpha, ratio, roots))
                good_split_count += 1
                for beta in roots:
                    uv_sign = ratio_surface_binary_discriminants(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )[0]
                    middle_numerator, branch_numerator = (
                        ratio_surface_uv_sign_square_numerators(
                            p,
                            alpha,
                            beta,
                            ratio,
                        )
                    )
                    if (
                        middle_factor * middle_factor * uv_sign
                        - ratio * middle_factor * middle_numerator * middle_numerator
                    ) % p != 0:
                        raise AssertionError(
                            (
                                p,
                                alpha,
                                beta,
                                ratio,
                                "middle_squareclass",
                            )
                        )
                    if (
                        branch_factor * branch_factor * uv_sign
                        - alpha * branch_factor * branch_numerator * branch_numerator
                    ) % p != 0:
                        raise AssertionError(
                            (
                                p,
                                alpha,
                                beta,
                                ratio,
                                "branch_squareclass",
                            )
                        )
                    if legendre(uv_sign, p) != legendre(
                        ratio * middle_factor,
                        p,
                    ):
                        raise AssertionError(
                            (p, alpha, beta, ratio, "middle_character")
                        )
                    if legendre(uv_sign, p) != legendre(
                        alpha * branch_factor,
                        p,
                    ):
                        raise AssertionError(
                            (p, alpha, beta, ratio, "branch_character")
                        )
                    middle_squareclass_matches += 1
                    branch_squareclass_matches += 1
                    root_checks += 1
        checked.append(
            (
                p,
                good_split_count,
                root_checks,
                middle_squareclass_matches,
                branch_squareclass_matches,
            )
        )
    return checked


def verify_ratio_surface_beta_projection() -> List[
    Tuple[int, int, int, int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        vertical_count = 0
        branch_base_count = 0
        infinity_base_count = 0
        zero_beta_base_count = 0
        split_main_pair_count = 0
        split_lower_pair_count = 0
        nonsplit_base_count = 0
        conjugate_sign_checks = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                quadratic, linear, constant = ratio_surface_beta_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                for beta in range(p):
                    delta_value = ratio_surface_delta(p, alpha, beta, ratio)
                    beta_value = (
                        quadratic * beta * beta + linear * beta + constant
                    ) % p
                    if delta_value != beta_value:
                        raise AssertionError((p, alpha, beta, ratio))
                discriminant = ratio_surface_beta_discriminant(
                    p,
                    alpha,
                    ratio,
                )
                expected_discriminant = (
                    alpha
                    * ratio
                    * ratio_surface_beta_middle_factor(p, alpha, ratio)
                    * ratio_surface_beta_branch_factor(p, alpha, ratio)
                ) % p
                if discriminant != expected_discriminant:
                    raise AssertionError(
                        (p, alpha, ratio, discriminant, expected_discriminant)
                    )
                if (quadratic, linear, constant) == (0, 0, 0):
                    if (alpha, ratio) != (1, 1):
                        raise AssertionError((p, alpha, ratio, "vertical"))
                    vertical_count += 1
                    continue
                projective_count = ratio_surface_projective_beta_root_count(
                    p,
                    alpha,
                    ratio,
                )
                expected_count = 1 + legendre(discriminant, p)
                if projective_count != expected_count:
                    raise AssertionError(
                        (p, alpha, ratio, projective_count, expected_count)
                    )
                branch_base_count += int(discriminant == 0)
                infinity_base_count += int(quadratic == 0)
                zero_beta_base_count += int(constant == 0)
                if discriminant == 0 or quadratic == 0 or constant == 0:
                    continue
                if legendre(discriminant, p) == -1:
                    nonsplit_base_count += 1
                    continue
                roots = [
                    beta
                    for beta in range(1, p)
                    if ratio_surface_delta(p, alpha, beta, ratio) == 0
                ]
                if len(roots) != 2:
                    raise AssertionError((p, alpha, ratio, roots))
                signs = [
                    legendre(
                        ratio_surface_binary_discriminants(
                            p,
                            alpha,
                            beta,
                            ratio,
                        )[0],
                        p,
                    )
                    for beta in roots
                ]
                if 0 in signs:
                    split_lower_pair_count += 1
                    continue
                split_main_pair_count += 1
                conjugate_sign_checks += 1
                if signs[0] != signs[1]:
                    raise AssertionError((p, alpha, ratio, roots, signs))
        if vertical_count != 1:
            raise AssertionError((p, vertical_count))
        for count in (
            branch_base_count,
            infinity_base_count,
            zero_beta_base_count,
            split_lower_pair_count,
        ):
            if count > 4 * (p - 1):
                raise AssertionError((p, count))
        checked.append(
            (
                p,
                branch_base_count,
                infinity_base_count,
                zero_beta_base_count,
                split_main_pair_count,
                split_lower_pair_count,
                nonsplit_base_count,
                conjugate_sign_checks,
            )
        )
    return checked


def verify_ratio_surface_branch_geometry() -> List[
    Tuple[int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        m_points = {
            (alpha, ratio)
            for alpha in range(1, p)
            for ratio in range(1, p)
            if ratio_surface_beta_middle_factor(p, alpha, ratio) == 0
        }
        h_points = {
            (alpha, ratio)
            for alpha in range(1, p)
            for ratio in range(1, p)
            if ratio_surface_beta_branch_factor(p, alpha, ratio) == 0
        }
        m_param_points = {(1, 1)}
        h_param_points = {(1, 1)}
        for slope in range(p):
            alpha, ratio = ratio_surface_branch_m_param(p, slope)
            if alpha != 0 and ratio != 0:
                m_param_points.add((alpha, ratio))
            alpha, ratio = ratio_surface_branch_h_param(p, slope)
            if alpha != 0 and ratio != 0:
                h_param_points.add((alpha, ratio))
        if m_points != m_param_points:
            raise AssertionError((p, "M", m_points ^ m_param_points))
        if h_points != h_param_points:
            raise AssertionError((p, "H", h_points ^ h_param_points))
        intersection = m_points & h_points
        if p != 5 and intersection != {(1, 1)}:
            raise AssertionError((p, intersection))
        checked.append(
            (
                p,
                len(m_points),
                len(h_points),
                len(intersection),
                int(intersection == {(1, 1)}),
            )
        )
    return checked


def verify_ratio_surface_branch_smoothness() -> List[
    Tuple[int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        m_point_count = 0
        h_point_count = 0
        m_singular_count = 0
        h_singular_count = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                if ratio_surface_beta_middle_factor(p, alpha, ratio) == 0:
                    m_point_count += 1
                    if (
                        ratio_surface_beta_middle_factor_derivatives(
                            p,
                            alpha,
                            ratio,
                        )
                        == (0, 0)
                    ):
                        m_singular_count += 1
                        if (alpha, ratio) != (1, 1):
                            raise AssertionError((p, "M", alpha, ratio))
                if ratio_surface_beta_branch_factor(p, alpha, ratio) == 0:
                    h_point_count += 1
                    if (
                        ratio_surface_beta_branch_factor_derivatives(
                            p,
                            alpha,
                            ratio,
                        )
                        == (0, 0)
                    ):
                        h_singular_count += 1
                        if (alpha, ratio) != (1, 1):
                            raise AssertionError((p, "H", alpha, ratio))
        if m_singular_count != 1 or h_singular_count != 1:
            raise AssertionError((p, m_singular_count, h_singular_count))
        checked.append(
            (
                p,
                m_point_count,
                h_point_count,
                m_singular_count,
                h_singular_count,
            )
        )
    return checked


def verify_ratio_surface_slope_blowup_boundary_ledger() -> List[
    Tuple[int, int, int, int, int]
]:
    pairs = (
        ("A", "Q"),
        ("A", "K"),
        ("A", "diag"),
        ("A", "M"),
        ("A", "H"),
        ("Q", "K"),
        ("Q", "diag"),
        ("Q", "M"),
        ("Q", "H"),
        ("K", "diag"),
        ("K", "M"),
        ("K", "H"),
        ("diag", "M"),
        ("diag", "H"),
        ("M", "H"),
    )
    checked: List[Tuple[int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        identity_checks = 0
        pair_intersections = 0
        pair_counts = {pair: 0 for pair in pairs}
        open_pair_counts = {pair: 0 for pair in pairs}
        for alpha in range(p):
            for slope in range(p):
                ratio = (1 + slope * (alpha - 1)) % p
                exceptional = (alpha - 1) % p
                strict = ratio_surface_slope_blowup_strict_factors(
                    p,
                    alpha,
                    slope,
                )
                quadratic, _, constant = ratio_surface_beta_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                if quadratic != exceptional * strict["A"] % p:
                    raise AssertionError((p, alpha, slope, "A", quadratic))
                if (
                    ratio_surface_beta_zero_factor(p, alpha, ratio)
                    != exceptional * strict["Q"] % p
                ):
                    raise AssertionError((p, alpha, slope, "Q"))
                if (
                    ratio_surface_lower_alpha_kernel(p, alpha, ratio)
                    != exceptional * exceptional * strict["K"] % p
                ):
                    raise AssertionError((p, alpha, slope, "K"))
                if (alpha - ratio) % p != exceptional * strict["diag"] % p:
                    raise AssertionError((p, alpha, slope, "diag"))
                if (
                    ratio_surface_beta_middle_factor(p, alpha, ratio)
                    != exceptional * exceptional * strict["M"] % p
                ):
                    raise AssertionError((p, alpha, slope, "M"))
                if (
                    ratio_surface_beta_branch_factor(p, alpha, ratio)
                    != exceptional * exceptional * strict["H"] % p
                ):
                    raise AssertionError((p, alpha, slope, "H"))
                if constant != alpha * ratio * (
                    ratio_surface_beta_zero_factor(p, alpha, ratio)
                ) % p:
                    raise AssertionError((p, alpha, slope, "C_beta"))
                identity_checks += 7

                for pair in pairs:
                    if strict[pair[0]] != 0 or strict[pair[1]] != 0:
                        continue
                    pair_counts[pair] += 1
                    pair_intersections += 1
                    if ratio_surface_slope_blowup_pair_support(
                        p,
                        pair[0],
                        pair[1],
                        slope,
                    ) != 0:
                        raise AssertionError((p, alpha, slope, pair))
                    if alpha != 0 and ratio != 0:
                        open_pair_counts[pair] += 1
        max_pair_count = max(pair_counts.values())
        max_open_pair_count = max(open_pair_counts.values())
        if max_pair_count > 3:
            raise AssertionError((p, pair_counts))
        if max_open_pair_count > 2:
            raise AssertionError((p, open_pair_counts))
        checked.append(
            (
                p,
                identity_checks,
                pair_intersections,
                max_pair_count,
                max_open_pair_count,
            )
        )
    return checked


def verify_ratio_surface_reciprocal_blowup_boundary_ledger() -> List[
    Tuple[int, int, int, int, int]
]:
    pairs = (
        ("A", "Q"),
        ("A", "K"),
        ("A", "diag"),
        ("A", "M"),
        ("A", "H"),
        ("Q", "K"),
        ("Q", "diag"),
        ("Q", "M"),
        ("Q", "H"),
        ("K", "diag"),
        ("K", "M"),
        ("K", "H"),
        ("diag", "M"),
        ("diag", "H"),
        ("M", "H"),
    )
    checked: List[Tuple[int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        identity_checks = 0
        pair_intersections = 0
        pair_counts = {pair: 0 for pair in pairs}
        open_pair_counts = {pair: 0 for pair in pairs}
        for ratio in range(p):
            for reciprocal_slope in range(p):
                alpha = (1 + reciprocal_slope * (ratio - 1)) % p
                exceptional = (ratio - 1) % p
                strict = ratio_surface_reciprocal_blowup_strict_factors(
                    p,
                    ratio,
                    reciprocal_slope,
                )
                quadratic, _, constant = ratio_surface_beta_coefficients(
                    p,
                    alpha,
                    ratio,
                )
                if quadratic != exceptional * strict["A"] % p:
                    raise AssertionError(
                        (p, ratio, reciprocal_slope, "A", quadratic)
                    )
                if (
                    ratio_surface_beta_zero_factor(p, alpha, ratio)
                    != exceptional * strict["Q"] % p
                ):
                    raise AssertionError((p, ratio, reciprocal_slope, "Q"))
                if (
                    ratio_surface_lower_alpha_kernel(p, alpha, ratio)
                    != exceptional * exceptional * strict["K"] % p
                ):
                    raise AssertionError((p, ratio, reciprocal_slope, "K"))
                if (alpha - ratio) % p != exceptional * strict["diag"] % p:
                    raise AssertionError((p, ratio, reciprocal_slope, "diag"))
                if (
                    ratio_surface_beta_middle_factor(p, alpha, ratio)
                    != exceptional * exceptional * strict["M"] % p
                ):
                    raise AssertionError((p, ratio, reciprocal_slope, "M"))
                if (
                    ratio_surface_beta_branch_factor(p, alpha, ratio)
                    != exceptional * exceptional * strict["H"] % p
                ):
                    raise AssertionError((p, ratio, reciprocal_slope, "H"))
                if constant != alpha * ratio * (
                    ratio_surface_beta_zero_factor(p, alpha, ratio)
                ) % p:
                    raise AssertionError((p, ratio, reciprocal_slope, "C_beta"))
                identity_checks += 7

                for pair in pairs:
                    if strict[pair[0]] != 0 or strict[pair[1]] != 0:
                        continue
                    pair_counts[pair] += 1
                    pair_intersections += 1
                    if ratio_surface_reciprocal_blowup_pair_support(
                        p,
                        pair[0],
                        pair[1],
                        reciprocal_slope,
                    ) != 0:
                        raise AssertionError(
                            (p, ratio, reciprocal_slope, pair)
                        )
                    if alpha != 0 and ratio != 0:
                        open_pair_counts[pair] += 1
        max_pair_count = max(pair_counts.values())
        max_open_pair_count = max(open_pair_counts.values())
        if max_pair_count > 4:
            raise AssertionError((p, pair_counts))
        if max_open_pair_count > 3:
            raise AssertionError((p, open_pair_counts))
        checked.append(
            (
                p,
                identity_checks,
                pair_intersections,
                max_pair_count,
                max_open_pair_count,
            )
        )
    return checked


def verify_ratio_surface_blowup_strict_transform_smoothness() -> List[
    Tuple[int, int, int, int, int]
]:
    names = ("A", "Q", "K", "diag", "M", "H")
    checked: List[Tuple[int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        finite_singular_count = 0
        reciprocal_singular_count = 0
        finite_by_component = {name: 0 for name in names}
        reciprocal_by_component = {name: 0 for name in names}

        for alpha in range(p):
            for slope in range(p):
                strict = ratio_surface_slope_blowup_strict_factors(
                    p,
                    alpha,
                    slope,
                )
                derivatives = ratio_surface_slope_blowup_strict_derivatives(
                    p,
                    alpha,
                    slope,
                )
                for name in names:
                    if strict[name] == 0 and derivatives[name] == (0, 0):
                        finite_singular_count += 1
                        finite_by_component[name] += 1

        for ratio in range(p):
            for reciprocal_slope in range(p):
                strict = ratio_surface_reciprocal_blowup_strict_factors(
                    p,
                    ratio,
                    reciprocal_slope,
                )
                derivatives = ratio_surface_reciprocal_blowup_strict_derivatives(
                    p,
                    ratio,
                    reciprocal_slope,
                )
                for name in names:
                    if strict[name] == 0 and derivatives[name] == (0, 0):
                        reciprocal_singular_count += 1
                        reciprocal_by_component[name] += 1

        if p == 5:
            if finite_by_component != {
                "A": 1,
                "Q": 1,
                "K": 0,
                "diag": 0,
                "M": 0,
                "H": 0,
            }:
                raise AssertionError((p, "finite", finite_by_component))
            if reciprocal_by_component != {
                "A": 1,
                "Q": 1,
                "K": 0,
                "diag": 0,
                "M": 0,
                "H": 0,
            }:
                raise AssertionError((p, "reciprocal", reciprocal_by_component))
        elif finite_singular_count != 0 or reciprocal_singular_count != 0:
            raise AssertionError(
                (
                    p,
                    finite_singular_count,
                    reciprocal_singular_count,
                    finite_by_component,
                    reciprocal_by_component,
                )
            )

        checked.append(
            (
                p,
                finite_singular_count,
                reciprocal_singular_count,
                max(finite_by_component.values()),
                max(reciprocal_by_component.values()),
            )
        )
    return checked


def verify_ratio_surface_blowup_boundary_incidence() -> List[
    Tuple[int, int, int, int, int, int, int, int, int]
]:
    names = ("A", "Q", "K", "diag", "M", "H")
    pairs = tuple(
        (names[first_index], names[second_index])
        for first_index in range(len(names))
        for second_index in range(first_index + 1, len(names))
    )
    finite_expected_tangencies = {
        ("A", "M"): lambda p, a, t: (3 * a + 1) % p == 0
        and (2 * t - 3) % p == 0,
        ("A", "H"): lambda p, a, t: (a + 2) % p == 0
        and (3 * t - 2) % p == 0,
        ("Q", "M"): lambda p, a, t: (a + 3) % p == 0
        and (2 * t - 1) % p == 0,
        ("Q", "H"): lambda p, a, t: (2 * a + 1) % p == 0
        and (3 * t - 4) % p == 0,
        ("Q", "diag"): lambda p, a, t: a % p == 0 and (t - 1) % p == 0,
    }
    reciprocal_expected_tangencies = {
        ("A", "M"): lambda p, r, s: (r + 1) % p == 0
        and (3 * s - 2) % p == 0,
        ("A", "H"): lambda p, r, s: (r + 1) % p == 0
        and (2 * s - 3) % p == 0,
        ("Q", "M"): lambda p, r, s: (r + 1) % p == 0
        and (s - 2) % p == 0,
        ("Q", "H"): lambda p, r, s: (r + 1) % p == 0
        and (4 * s - 3) % p == 0,
        ("Q", "diag"): lambda p, r, s: r % p == 0 and (s - 1) % p == 0,
    }

    def tangent(
        p: int,
        first_derivative: Tuple[int, int],
        second_derivative: Tuple[int, int],
    ) -> bool:
        return (
            first_derivative[0] * second_derivative[1]
            - first_derivative[1] * second_derivative[0]
        ) % p == 0

    checked: List[Tuple[int, int, int, int, int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        finite_tangent_count = 0
        finite_open_tangent_count = 0
        finite_triple_count = 0
        finite_open_triple_count = 0
        finite_max_components = 0
        finite_tangent_by_pair = {pair: 0 for pair in pairs}

        for alpha in range(p):
            for slope in range(p):
                ratio = (1 + slope * (alpha - 1)) % p
                strict = ratio_surface_slope_blowup_strict_factors(
                    p,
                    alpha,
                    slope,
                )
                derivatives = ratio_surface_slope_blowup_strict_derivatives(
                    p,
                    alpha,
                    slope,
                )
                zero_components = tuple(
                    name for name in names if strict[name] == 0
                )
                finite_max_components = max(
                    finite_max_components,
                    len(zero_components),
                )
                if len(zero_components) >= 3:
                    finite_triple_count += 1
                    if alpha != 0 and ratio != 0:
                        finite_open_triple_count += 1
                    if p > 5 and (alpha, slope) != (0, 1):
                        raise AssertionError((p, "finite_triple", alpha, slope))
                for first_index, first in enumerate(zero_components):
                    for second in zero_components[first_index + 1 :]:
                        if not tangent(p, derivatives[first], derivatives[second]):
                            continue
                        pair = (first, second)
                        finite_tangent_count += 1
                        finite_tangent_by_pair[pair] += 1
                        if alpha != 0 and ratio != 0:
                            finite_open_tangent_count += 1
                        if p > 5 and not finite_expected_tangencies.get(
                            pair,
                            lambda *_: False,
                        )(p, alpha, slope):
                            raise AssertionError(
                                (p, "finite_tangent", pair, alpha, slope)
                            )

        reciprocal_tangent_count = 0
        reciprocal_open_tangent_count = 0
        reciprocal_triple_count = 0
        reciprocal_open_triple_count = 0
        reciprocal_max_components = 0
        reciprocal_tangent_by_pair = {pair: 0 for pair in pairs}

        for ratio in range(p):
            for reciprocal_slope in range(p):
                alpha = (1 + reciprocal_slope * (ratio - 1)) % p
                strict = ratio_surface_reciprocal_blowup_strict_factors(
                    p,
                    ratio,
                    reciprocal_slope,
                )
                derivatives = ratio_surface_reciprocal_blowup_strict_derivatives(
                    p,
                    ratio,
                    reciprocal_slope,
                )
                zero_components = tuple(
                    name for name in names if strict[name] == 0
                )
                reciprocal_max_components = max(
                    reciprocal_max_components,
                    len(zero_components),
                )
                if len(zero_components) >= 3:
                    reciprocal_triple_count += 1
                    if alpha != 0 and ratio != 0:
                        reciprocal_open_triple_count += 1
                    if p > 5 and (ratio, reciprocal_slope) != (0, 1):
                        raise AssertionError(
                            (p, "reciprocal_triple", ratio, reciprocal_slope)
                        )
                for first_index, first in enumerate(zero_components):
                    for second in zero_components[first_index + 1 :]:
                        if not tangent(p, derivatives[first], derivatives[second]):
                            continue
                        pair = (first, second)
                        reciprocal_tangent_count += 1
                        reciprocal_tangent_by_pair[pair] += 1
                        if alpha != 0 and ratio != 0:
                            reciprocal_open_tangent_count += 1
                        if p > 5 and not reciprocal_expected_tangencies.get(
                            pair,
                            lambda *_: False,
                        )(p, ratio, reciprocal_slope):
                            raise AssertionError(
                                (
                                    p,
                                    "reciprocal_tangent",
                                    pair,
                                    ratio,
                                    reciprocal_slope,
                                )
                            )

        if p > 5:
            expected_tangent_pairs = {
                ("A", "M"),
                ("A", "H"),
                ("Q", "M"),
                ("Q", "H"),
                ("Q", "diag"),
            }
            for pair in pairs:
                expected_count = int(pair in expected_tangent_pairs)
                if finite_tangent_by_pair[pair] != expected_count:
                    raise AssertionError((p, "finite_pair", pair))
                if reciprocal_tangent_by_pair[pair] != expected_count:
                    raise AssertionError((p, "reciprocal_pair", pair))
            if (
                finite_tangent_count,
                finite_open_tangent_count,
                finite_triple_count,
                finite_open_triple_count,
                finite_max_components,
            ) != (5, 4, 1, 0, 6):
                raise AssertionError((p, "finite_counts"))
            if (
                reciprocal_tangent_count,
                reciprocal_open_tangent_count,
                reciprocal_triple_count,
                reciprocal_open_triple_count,
                reciprocal_max_components,
            ) != (5, 4, 1, 0, 6):
                raise AssertionError((p, "reciprocal_counts"))
        else:
            if (
                finite_tangent_count,
                finite_open_tangent_count,
                finite_triple_count,
                finite_open_triple_count,
                finite_max_components,
            ) != (17, 13, 3, 2, 6):
                raise AssertionError((p, "finite_p5_counts"))
            if (
                reciprocal_tangent_count,
                reciprocal_open_tangent_count,
                reciprocal_triple_count,
                reciprocal_open_triple_count,
                reciprocal_max_components,
            ) != (16, 12, 3, 2, 6):
                raise AssertionError((p, "reciprocal_p5_counts"))

        checked.append(
            (
                p,
                finite_tangent_count,
                finite_open_tangent_count,
                finite_triple_count,
                finite_open_triple_count,
                reciprocal_tangent_count,
                reciprocal_open_tangent_count,
                reciprocal_triple_count,
                reciprocal_open_triple_count,
            )
        )
    return checked


def verify_ratio_surface_lower_chart_collapse() -> List[
    Tuple[int, int, int, int, int, int]
]:
    checked: List[Tuple[int, int, int, int, int, int]] = []
    for p in LOWER_CHART_PRIMES:
        uv_count = 0
        lower_count = 0
        diagonal_count = 0
        residual_count = 0
        zero_count = 0
        for alpha in range(1, p):
            for beta in range(1, p):
                for ratio in range(1, p):
                    if ratio_surface_delta(p, alpha, beta, ratio) != 0:
                        continue
                    discriminants = ratio_surface_binary_discriminants(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )
                    if discriminants[0] != 0:
                        uv_count += 1
                        continue
                    lower_count += 1
                    diagonal = alpha == ratio and beta == ratio
                    residual = (
                        ratio_surface_lower_alpha_kernel(p, alpha, ratio) == 0
                        and ratio_surface_lower_beta_kernel(p, beta, ratio) == 0
                    )
                    if not (diagonal or residual):
                        raise AssertionError((p, alpha, beta, ratio))
                    diagonal_count += int(diagonal)
                    residual_count += int(residual)
                    if (alpha, beta, ratio) == (1, 1, 1):
                        zero_count += 1
                        continue
                    if discriminants[1] == 0:
                        raise AssertionError(
                            (p, alpha, beta, ratio, discriminants)
                        )
        if lower_count > 5 * (p - 1):
            raise AssertionError((p, lower_count))
        if zero_count != 1:
            raise AssertionError((p, zero_count))
        checked.append(
            (
                p,
                uv_count,
                lower_count,
                diagonal_count,
                residual_count,
                zero_count,
            )
        )
    return checked


def weighted_projective_singular_matrix_audit(
    p: int,
    suborder: int,
    logs: Dict[int, int],
    projective_error: int,
) -> Tuple[int, float, float, float, float, Tuple[int, int, int, int, int]]:
    matrix = [[0 for _ in range(suborder)] for _ in range(suborder)]
    chart_counts = {
        "zero": 0,
        "rank1": 0,
        "uv": 0,
        "u1": 0,
        "v1": 0,
    }
    for alpha in range(1, p):
        alpha_label = logs[alpha] % suborder
        for beta in range(1, p):
            beta_label = logs[beta] % suborder
            for ratio in range(1, p):
                determinant = ratio_surface_doubled_projective_determinant(
                    p,
                    alpha,
                    beta,
                    ratio,
                )
                if determinant != 0:
                    continue
                coefficients = ratio_surface_conic_coefficients(
                    p,
                    alpha,
                    beta,
                    ratio,
                )
                chart, chart_unit = projective_excess_chart(p, coefficients)
                chart_counts[chart] += 1
                exact_unit = projective_excess_unit(
                    p,
                    alpha,
                    beta,
                    ratio,
                )
                if chart_unit != exact_unit:
                    raise AssertionError(
                        (p, suborder, alpha, beta, ratio, chart, chart_unit)
                    )
                matrix[alpha_label][beta_label] += exact_unit

    quotient_weights = [suborder - 1] + [-1 for _ in range(1, suborder)]
    weighted_units = sum(
        quotient_weights[left]
        * quotient_weights[right]
        * matrix[left][right]
        for left in range(suborder)
        for right in range(suborder)
    )
    if p * weighted_units != projective_error:
        raise AssertionError((p, suborder, p * weighted_units, projective_error))

    row_sums = [sum(row) for row in matrix]
    column_sums = [
        sum(matrix[row][column] for row in range(suborder))
        for column in range(suborder)
    ]
    total = sum(row_sums)
    centered_frobenius_sq = 0.0
    max_entry_ratio = 0.0
    for row in range(suborder):
        for column in range(suborder):
            centered = (
                matrix[row][column]
                - row_sums[row] / suborder
                - column_sums[column] / suborder
                + total / (suborder * suborder)
            )
            centered_frobenius_sq += centered * centered
            max_entry_ratio = max(max_entry_ratio, abs(matrix[row][column]) / p)
    centered_frobenius = math.sqrt(centered_frobenius_sq)
    weight_norm_sq = suborder * (suborder - 1)
    cauchy_bound = p * weight_norm_sq * centered_frobenius
    if abs(projective_error) > cauchy_bound + 1000 * TOLERANCE:
        raise AssertionError((p, suborder, projective_error, cauchy_bound))
    bound_ratio = abs(projective_error) / cauchy_bound if cauchy_bound else 0.0

    spectral_sum = 0j
    spectral_energy = 0.0
    max_spectral_ratio = 0.0
    root = cmath.exp(2j * math.pi / suborder)
    for left_character in range(1, suborder):
        for right_character in range(1, suborder):
            coefficient = 0j
            for left in range(suborder):
                for right in range(suborder):
                    coefficient += matrix[left][right] * root ** (
                        left_character * left
                        + right_character * right
                    )
            spectral_sum += coefficient
            spectral_energy += abs(coefficient) ** 2
            max_spectral_ratio = max(max_spectral_ratio, abs(coefficient) / p)
    if abs(spectral_sum.real - weighted_units) > 1000 * TOLERANCE:
        raise AssertionError((p, suborder, spectral_sum, weighted_units))
    if abs(spectral_sum.imag) > 1000 * TOLERANCE:
        raise AssertionError((p, suborder, spectral_sum))
    if abs(spectral_energy / (suborder * suborder) - centered_frobenius_sq) > (
        1000 * TOLERANCE
    ):
        raise AssertionError(
            (p, suborder, spectral_energy, centered_frobenius_sq)
        )
    return (
        weighted_units,
        round(centered_frobenius / p, 10),
        round(max_entry_ratio, 10),
        round(bound_ratio, 10),
        round(max_spectral_ratio, 10),
        (
            chart_counts["zero"],
            chart_counts["rank1"],
            chart_counts["uv"],
            chart_counts["u1"],
            chart_counts["v1"],
        ),
    )


def verify_weighted_projective_decomposition() -> List[
    Tuple[
        int,
        int,
        int,
        int,
        int,
        int,
        Tuple[int, ...],
        int,
        int,
        Tuple[int, float],
        Tuple[int, int, Tuple[int, float]],
        Tuple[int, int, int, float],
        Tuple[float, float],
        Tuple[int, float, float, float, float, Tuple[int, int, int, int, int]],
    ]
]:
    checked: List[
        Tuple[
            int,
            int,
            int,
            int,
            int,
            int,
            Tuple[int, ...],
            int,
            int,
            Tuple[int, float],
            Tuple[int, int, Tuple[int, float]],
            Tuple[int, int, int, float],
            Tuple[float, float],
            Tuple[int, float, float, float, float, Tuple[int, int, int, int, int]],
        ]
    ] = []
    for p, suborder in RATIO_SURFACE_CASES:
        logs = log_table(p)
        _, _, _, _, moment = open_suborder_coset_moment(p, suborder, logs)
        projective_error, singular_count, zero_conic_count = (
            weighted_projective_error_sum(p, suborder, logs)
        )
        singular_matrix = weighted_projective_singular_matrix_audit(
            p,
            suborder,
            logs,
            projective_error,
        )
        boundary_error = projective_error - moment
        boundary_parts = weighted_boundary_partition_sum(p, suborder, logs)
        if sum(boundary_parts) != boundary_error:
            raise AssertionError((p, suborder, boundary_parts, boundary_error))
        vanishing_labels = ("u0", "v0", "source_a0", "target_a0")
        for label in vanishing_labels:
            value = boundary_parts[BOUNDARY_LABELS.index(label)]
            if value != 0:
                raise AssertionError((p, suborder, label, value))
        surviving_formulas = weighted_surviving_boundary_formula_sums(
            p,
            suborder,
            logs,
        )
        expected_survivors = (
            boundary_parts[BOUNDARY_LABELS.index("infinity")],
            boundary_parts[BOUNDARY_LABELS.index("source_line")],
            boundary_parts[BOUNDARY_LABELS.index("target_line")],
        )
        if surviving_formulas != expected_survivors:
            raise AssertionError((p, suborder, surviving_formulas, expected_survivors))
        infinity_reduced = weighted_infinity_autocorrelation_sum(
            p,
            suborder,
            logs,
        )
        if infinity_reduced != expected_survivors[0]:
            raise AssertionError((p, suborder, infinity_reduced, expected_survivors))
        infinity_energy = weighted_infinity_fiber_energy_sum(
            p,
            suborder,
            logs,
        )
        if infinity_energy != infinity_reduced:
            raise AssertionError((p, suborder, infinity_energy, infinity_reduced))
        infinity_spectral = weighted_infinity_spectral_audit(
            p,
            suborder,
            logs,
        )
        if (p - 1) * infinity_spectral[0] != infinity_reduced:
            raise AssertionError((p, suborder, infinity_spectral, infinity_reduced))
        source_exclusive, line_overlap = weighted_source_line_split_formula_sums(
            p,
            suborder,
            logs,
        )
        if source_exclusive + line_overlap != expected_survivors[1]:
            raise AssertionError((p, suborder, source_exclusive, line_overlap))
        if source_exclusive != expected_survivors[2]:
            raise AssertionError((p, suborder, source_exclusive, expected_survivors))
        overlap_energy = weighted_line_pair_overlap_energy_sum(
            p,
            suborder,
            logs,
        )
        if overlap_energy != line_overlap:
            raise AssertionError((p, suborder, overlap_energy, line_overlap))
        overlap_spectral = weighted_line_pair_overlap_spectral_audit(
            p,
            suborder,
            logs,
        )
        if overlap_spectral[0] != line_overlap:
            raise AssertionError((p, suborder, overlap_spectral, line_overlap))
        target_pairing = weighted_target_line_spectral_pairing_audit(
            p,
            suborder,
            logs,
            moment,
            line_overlap,
            expected_survivors[2],
        )
        closed_boundary = (
            infinity_reduced
            + line_overlap
            + 2 * expected_survivors[2]
        )
        if closed_boundary != boundary_error:
            raise AssertionError((p, suborder, closed_boundary, boundary_error))
        closed_moment = projective_error - closed_boundary
        if closed_moment != moment:
            raise AssertionError((p, suborder, closed_moment, moment))
        closed_bounds = closed_boundary_moment_bounds(
            p,
            suborder,
            moment,
            projective_error,
            line_overlap,
        )
        if zero_conic_count != 1:
            raise AssertionError((p, suborder, zero_conic_count))
        if singular_count > 3 * (p - 1) * (p - 1):
            raise AssertionError((p, suborder, singular_count))
        checked.append(
            (
                p,
                suborder,
                moment,
                projective_error,
                boundary_error,
                singular_count,
                boundary_parts,
                infinity_reduced,
                infinity_energy,
                infinity_spectral,
                (source_exclusive, line_overlap, overlap_spectral),
                target_pairing,
                closed_bounds,
                singular_matrix,
            )
        )
    return checked


def verify_weighted_ratio_surface_centering() -> List[Tuple[int, int, int]]:
    checked: List[Tuple[int, int, int]] = []
    for p, suborder in RATIO_SURFACE_CASES:
        logs = log_table(p)
        support_count, _, _, _, moment = open_suborder_coset_moment(
            p,
            suborder,
            logs,
        )
        weighted_moment = weighted_ratio_surface_centered_moment(
            p,
            suborder,
            logs,
        )
        if weighted_moment != moment:
            raise AssertionError((p, suborder, weighted_moment, moment))
        weight_sum = sum(
            quotient_centering_weight(p, suborder, logs, value)
            for value in range(1, p)
        )
        if weight_sum != 0:
            raise AssertionError((p, suborder, weight_sum))
        checked.append((p, suborder, support_count, moment))
    return checked


def verify_quotient_conic_centered_bounds() -> List[
    Tuple[int, int, int, int, float]
]:
    checked: List[Tuple[int, int, int, int, float]] = []
    for p in ADMISSIBLE_OPEN_AUDIT_PRIMES:
        logs = log_table(p)
        order = p - 1
        for suborder in range(2, order + 1):
            if order % suborder != 0:
                continue
            if admissible_filter_formula(suborder) == 0:
                continue
            (
                support_count,
                joint_energy,
                x_energy,
                v_energy,
                moment,
            ) = open_suborder_coset_moment(p, suborder, logs)
            if suborder * x_energy < support_count * support_count:
                raise AssertionError((p, suborder, "x-cauchy"))
            if suborder * v_energy < support_count * support_count:
                raise AssertionError((p, suborder, "v-cauchy"))
            joint_bound = quotient_conic_joint_energy_bound(p, suborder)
            if joint_energy > joint_bound:
                raise AssertionError((p, suborder, joint_energy, joint_bound))
            moment_bound = quotient_conic_centered_moment_bound(p, suborder)
            if moment > moment_bound:
                raise AssertionError((p, suborder, moment, moment_bound))
            checked.append(
                (
                    p,
                    suborder,
                    moment,
                    moment_bound,
                    round(math.sqrt(moment_bound) / ((suborder - 1) * p), 10),
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
    ratio_surface_lower_chart_checked = (
        verify_ratio_surface_lower_chart_collapse()
    )
    ratio_surface_beta_projection_checked = (
        verify_ratio_surface_beta_projection()
    )
    ratio_surface_beta_etale_cover_checked = (
        verify_ratio_surface_beta_etale_cover()
    )
    ratio_surface_beta_square_root_normalization_checked = (
        verify_ratio_surface_beta_square_root_normalization()
    )
    ratio_surface_beta_vertical_pencil_checked = (
        verify_ratio_surface_beta_vertical_pencil_ledger()
    )
    ratio_surface_branch_geometry_checked = (
        verify_ratio_surface_branch_geometry()
    )
    ratio_surface_branch_smoothness_checked = (
        verify_ratio_surface_branch_smoothness()
    )
    ratio_surface_slope_blowup_boundary_checked = (
        verify_ratio_surface_slope_blowup_boundary_ledger()
    )
    ratio_surface_reciprocal_blowup_boundary_checked = (
        verify_ratio_surface_reciprocal_blowup_boundary_ledger()
    )
    ratio_surface_blowup_smoothness_checked = (
        verify_ratio_surface_blowup_strict_transform_smoothness()
    )
    ratio_surface_blowup_incidence_checked = (
        verify_ratio_surface_blowup_boundary_incidence()
    )
    ratio_surface_beta_pushforward_checked = (
        verify_ratio_surface_beta_pushforward_trace()
    )
    ratio_surface_exceptional_root_bound_checked = (
        verify_ratio_surface_exceptional_root_bound()
    )
    ratio_surface_beta_pushforward_determinant_checked = (
        verify_ratio_surface_beta_pushforward_determinant()
    )
    ratio_surface_full_trace_reduction_checked = (
        verify_ratio_surface_full_trace_reduction()
    )
    ratio_surface_quotient_trace_reduction_checked = (
        verify_ratio_surface_quotient_trace_reduction()
    )
    ratio_surface_beta_kummer_conductor_checked = (
        verify_ratio_surface_beta_kummer_conductor_ledger()
    )
    ratio_surface_beta_infinity_conductor_checked = (
        verify_ratio_surface_beta_infinity_conductor_ledger()
    )
    ratio_surface_uv_sign_divisor_checked = (
        verify_ratio_surface_uv_sign_divisor_deleted()
    )
    ratio_surface_uv_sign_base_squareclass_checked = (
        verify_ratio_surface_uv_sign_base_squareclass()
    )
    ratio_surface_beta_ratio_resonance_checked = (
        verify_ratio_surface_beta_ratio_resonance()
    )
    ratio_surface_beta_quotient_energy_checked = (
        verify_ratio_surface_beta_quotient_energy()
    )
    quotient_conic_centered_bound_checked = (
        verify_quotient_conic_centered_bounds()
    )
    weighted_ratio_surface_centering_checked = (
        verify_weighted_ratio_surface_centering()
    )
    weighted_projective_decomposition_checked = (
        verify_weighted_projective_decomposition()
    )
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
        f"ratio_surface_lower_chart_checked="
        f"{ratio_surface_lower_chart_checked}",
        f"ratio_surface_beta_projection_checked="
        f"{ratio_surface_beta_projection_checked}",
        f"ratio_surface_beta_etale_cover_checked="
        f"{ratio_surface_beta_etale_cover_checked}",
        f"ratio_surface_beta_square_root_normalization_checked="
        f"{ratio_surface_beta_square_root_normalization_checked}",
        f"ratio_surface_beta_vertical_pencil_checked="
        f"{ratio_surface_beta_vertical_pencil_checked}",
        f"ratio_surface_branch_geometry_checked="
        f"{ratio_surface_branch_geometry_checked}",
        f"ratio_surface_branch_smoothness_checked="
        f"{ratio_surface_branch_smoothness_checked}",
        f"ratio_surface_slope_blowup_boundary_checked="
        f"{ratio_surface_slope_blowup_boundary_checked}",
        f"ratio_surface_reciprocal_blowup_boundary_checked="
        f"{ratio_surface_reciprocal_blowup_boundary_checked}",
        f"ratio_surface_blowup_smoothness_checked="
        f"{ratio_surface_blowup_smoothness_checked}",
        f"ratio_surface_blowup_incidence_checked="
        f"{ratio_surface_blowup_incidence_checked}",
        f"ratio_surface_beta_pushforward_checked="
        f"{ratio_surface_beta_pushforward_checked}",
        f"ratio_surface_exceptional_root_bound_checked="
        f"{ratio_surface_exceptional_root_bound_checked}",
        f"ratio_surface_beta_pushforward_determinant_checked="
        f"{ratio_surface_beta_pushforward_determinant_checked}",
        f"ratio_surface_full_trace_reduction_checked="
        f"{ratio_surface_full_trace_reduction_checked}",
        f"ratio_surface_quotient_trace_reduction_checked="
        f"{ratio_surface_quotient_trace_reduction_checked}",
        f"ratio_surface_beta_kummer_conductor_checked="
        f"{ratio_surface_beta_kummer_conductor_checked}",
        f"ratio_surface_beta_infinity_conductor_checked="
        f"{ratio_surface_beta_infinity_conductor_checked}",
        f"ratio_surface_uv_sign_divisor_checked="
        f"{ratio_surface_uv_sign_divisor_checked}",
        f"ratio_surface_uv_sign_base_squareclass_checked="
        f"{ratio_surface_uv_sign_base_squareclass_checked}",
        f"ratio_surface_beta_ratio_resonance_checked="
        f"{ratio_surface_beta_ratio_resonance_checked}",
        f"ratio_surface_beta_quotient_energy_checked="
        f"{ratio_surface_beta_quotient_energy_checked}",
        f"quotient_conic_centered_bound_checked="
        f"{quotient_conic_centered_bound_checked}",
        f"weighted_ratio_surface_centering_checked="
        f"{weighted_ratio_surface_centering_checked}",
        f"weighted_projective_decomposition_checked="
        f"{weighted_projective_decomposition_checked}",
        f"collapsed_four_p_obstruction_checked="
        f"{collapsed_four_p_obstruction_checked}",
    )


if __name__ == "__main__":
    main()
