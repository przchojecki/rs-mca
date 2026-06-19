#!/usr/bin/env python3
"""Verify the M1 depth-two line-conic resonance reduction."""

from __future__ import annotations

import cmath
import math
from typing import Dict, Iterable, List, Tuple


EXHAUSTIVE_PRIMES = (17, 31)
MOMENT_PRIMES = (5, 7, 11, 17, 31)
FILTER_ORDERS = tuple(range(2, 41))
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


def support_size_formula(p: int) -> int:
    return p * p - 3 * p + 3 + 3 * legendre(-3, p)


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


def v_marginal_size_formula(p: int, v: int) -> int:
    if v % p == 0:
        return 0
    delta = -3 * v * v - 2 * v - 3
    return p - 2 - legendre(delta, p) + int(shape_b(v, p) == 0)


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


def direct_full_character_moments(p: int) -> Tuple[int, int, int]:
    logs = log_table(p)
    table = character_table(p, logs)
    core_moment = 0.0
    nonprincipal_core_moment = 0.0
    line_moment = 0.0
    for eta_exponent in range(p - 1):
        eta = table[eta_exponent]
        eta_inv = table[(-eta_exponent) % (p - 1)]
        for nu_exponent in range(p - 1):
            nu = table[nu_exponent]
            core_value = abs(direct_core(p, eta_inv, nu, eta)) ** 2
            core_moment += core_value
            if eta_exponent != 0 and nu_exponent != 0:
                nonprincipal_core_moment += core_value
            line_moment += abs(line_correction(p, eta_inv, nu, eta)) ** 2
    return round(core_moment), round(line_moment), round(nonprincipal_core_moment)


def verify_second_moments() -> List[Tuple[int, int, int, int]]:
    checked: List[Tuple[int, int, int, int]] = []
    for p in MOMENT_PRIMES:
        collision_count = direct_core_collision_count(p)
        expected_collision_count = core_collision_formula(p)
        if collision_count != expected_collision_count:
            raise AssertionError((p, collision_count, expected_collision_count))
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
        core_moment, line_moment, nonprincipal_moment = direct_full_character_moments(p)
        expected_core_moment = (p - 1) * (p - 1) * expected_collision_count
        expected_line_moment = (p - 1) * (p - 1) * expected_line_support_count
        expected_nonprincipal_moment = nonprincipal_core_moment_formula(p)
        if core_moment != expected_core_moment:
            raise AssertionError((p, core_moment, expected_core_moment))
        if line_moment != expected_line_moment:
            raise AssertionError((p, line_moment, expected_line_moment))
        if nonprincipal_moment != expected_nonprincipal_moment:
            raise AssertionError(
                (p, nonprincipal_moment, expected_nonprincipal_moment)
            )
        verify_principal_rows(p)
        checked.append(
            (
                p,
                expected_collision_count,
                expected_line_support_count,
                expected_nonprincipal_moment,
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
    singular_checked: List[int] = []
    lambda_map_checked = 0
    lambda_twist_checked: List[Tuple[int, int, int]] = []
    twisted_discriminant_checked: List[Tuple[int, int, int]] = []
    twisted_line_twist_checked: List[Tuple[int, int, int, int, int]] = []
    twisted_line_deck_checked: List[Tuple[int, int, float, float, float]] = []
    twisted_line_kernel_moment_checked: List[Tuple[int, int, float, float]] = []
    twisted_line_fiber_checked = 0
    split_hypergeometric_checked = 0
    filter_checked = verify_admissible_filter_counts()
    twist_nontrivial_checked = verify_admissible_twist_nontriviality()
    moment_checked = verify_second_moments()
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
        f"twisted_line_kernel_moment_checked="
        f"{twisted_line_kernel_moment_checked}",
        f"twisted_line_fiber_checked={twisted_line_fiber_checked}",
        f"split_hypergeometric_checked={split_hypergeometric_checked}",
        f"filter_checked={filter_checked[0]}..{filter_checked[-1]}",
        f"twist_nontrivial_checked={twist_nontrivial_checked[0]}.."
        f"{twist_nontrivial_checked[-1]}",
        f"moment_checked={moment_checked}",
    )


if __name__ == "__main__":
    main()
