#!/usr/bin/env python3
"""Verify finite instances of the F1 fixed-rate extension-line obstruction."""

from __future__ import annotations

import argparse
import itertools
import json
from math import comb
from math import isqrt
from typing import Any


Element = tuple[int, int]
Poly = list[Element]


SIGMA_ONE_CASES = (
    {"p": 5, "k": 2},
    {"p": 7, "k": 3},
    {"p": 11, "k": 5},
    {"p": 13, "k": 6},
)

SIGMA_TWO_CASES = (
    {"p": 7, "k": 2},
    {"p": 11, "k": 4},
    {"p": 13, "k": 5},
)

SIGMA_THREE_CASES = (
    {"p": 13, "k": 3},
    {"p": 17, "k": 5},
    {"p": 19, "k": 6},
)

SIGMA_THREE_COUNT_CASES = (
    {"p": 29, "k": 14},
    {"p": 37, "k": 18},
    {"p": 47, "k": 23},
    {"p": 59, "k": 29},
    {"p": 31, "k": 7},
    {"p": 41, "k": 10},
    {"p": 53, "k": 13},
)

FIXED_SIGMA_COUNT_CASES = (
    {"p": 17, "k": 4, "sigma": 4},
    {"p": 19, "k": 7, "sigma": 4},
    {"p": 23, "k": 8, "sigma": 4},
    {"p": 17, "k": 3, "sigma": 5},
    {"p": 19, "k": 4, "sigma": 5},
    {"p": 23, "k": 6, "sigma": 5},
)

SLOW_SLACK_BOUND_CASES = (
    {"p": 1009, "k": 504, "sigma": 3},
    {"p": 10007, "k": 5003, "sigma": 4},
    {"p": 65537, "k": 32768, "sigma": 4},
)

EXTENSION_DEGREE_BOUND_CASES = (
    {"p": 1009, "k": 504, "sigma": 3, "degrees": (2, 3, 4)},
    {"p": 65537, "k": 32768, "sigma": 4, "degrees": (2, 3, 4)},
)

MINIMAL_DEGREE_TEMPLATE_CASES = (
    {"p": 7, "k": 3, "sigma": 1, "alpha_degree": 3},
    {"p": 17, "k": 8, "sigma": 2, "alpha_degree": 3},
    {"p": 11, "k": 5, "sigma": 1, "alpha_degree": 4},
)

MINIMAL_DEGREE_BOUND_CASES = (
    {"p": 1009, "k": 504, "sigma": 3, "alpha_degree": 3},
    {"p": 10007, "k": 5003, "sigma": 4, "alpha_degree": 3},
    {"p": 1009, "k": 504, "sigma": 2, "alpha_degree": 4},
)


def base(value: int, p: int) -> Element:
    return (value % p, 0)


def add(x: Element, y: Element, p: int) -> Element:
    return ((x[0] + y[0]) % p, (x[1] + y[1]) % p)


def neg(x: Element, p: int) -> Element:
    return ((-x[0]) % p, (-x[1]) % p)


def sub(x: Element, y: Element, p: int) -> Element:
    return add(x, neg(y, p), p)


def mul(x: Element, y: Element, p: int, d: int) -> Element:
    return ((x[0] * y[0] + d * x[1] * y[1]) % p, (x[0] * y[1] + x[1] * y[0]) % p)


def pow_el(x: Element, exponent: int, p: int, d: int) -> Element:
    result = base(1, p)
    value = x
    e = exponent
    while e:
        if e & 1:
            result = mul(result, value, p, d)
        value = mul(value, value, p, d)
        e >>= 1
    return result


def inv(x: Element, p: int, d: int) -> Element:
    norm = (x[0] * x[0] - d * x[1] * x[1]) % p
    if norm == 0:
        raise ZeroDivisionError(x)
    norm_inv = pow(norm, -1, p)
    return ((x[0] * norm_inv) % p, (-x[1] * norm_inv) % p)


def div(x: Element, y: Element, p: int, d: int) -> Element:
    return mul(x, inv(y, p, d), p, d)


def is_nonsquare(value: int, p: int) -> bool:
    return pow(value, (p - 1) // 2, p) == p - 1


def least_nonsquare(p: int) -> int:
    for value in range(2, p):
        if is_nonsquare(value, p):
            return value
    raise ValueError(f"no nonsquare found for p={p}")


def trim(poly: Poly) -> Poly:
    while len(poly) > 1 and poly[-1] == (0, 0):
        poly.pop()
    return poly


def poly_add(left: Poly, right: Poly, p: int) -> Poly:
    size = max(len(left), len(right))
    result = [(0, 0)] * size
    for index in range(size):
        a = left[index] if index < len(left) else (0, 0)
        b = right[index] if index < len(right) else (0, 0)
        result[index] = add(a, b, p)
    return trim(result)


def poly_sub(left: Poly, right: Poly, p: int) -> Poly:
    return poly_add(left, [neg(coef, p) for coef in right], p)


def poly_mul(left: Poly, right: Poly, p: int, d: int) -> Poly:
    result = [(0, 0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = add(result[i + j], mul(a, b, p, d), p)
    return trim(result)


def poly_eval(poly: Poly, x: Element, p: int, d: int) -> Element:
    value = (0, 0)
    for coef in reversed(poly):
        value = add(mul(value, x, p, d), coef, p)
    return value


def monomial(degree: int, p: int) -> Poly:
    return [(0, 0)] * degree + [base(1, p)]


def locator(points: tuple[int, ...], p: int, d: int) -> Poly:
    poly = [base(1, p)]
    for point in points:
        poly = poly_mul(poly, [neg(base(point, p), p), base(1, p)], p, d)
    return poly


def divide_by_x_minus_alpha(poly: Poly, alpha: Element, p: int, d: int) -> Poly:
    if len(poly) <= 1:
        if poly == [(0, 0)]:
            return [(0, 0)]
        raise ValueError("constant polynomial cannot be divided by X-alpha here")
    quotient = [(0, 0)] * (len(poly) - 1)
    quotient[-1] = poly[-1]
    for index in range(len(poly) - 2, 0, -1):
        quotient[index - 1] = add(poly[index], mul(alpha, quotient[index], p, d), p)
    remainder = add(poly[0], mul(alpha, quotient[0], p, d), p)
    if remainder != (0, 0):
        raise AssertionError(f"nonzero division remainder {remainder}")
    return trim(quotient)


def interpolate(xs: tuple[int, ...], ys: list[Element], p: int, d: int) -> Poly:
    result: Poly = [(0, 0)]
    for i, xi in enumerate(xs):
        basis: Poly = [base(1, p)]
        denominator = base(1, p)
        for j, xj in enumerate(xs):
            if i == j:
                continue
            basis = poly_mul(basis, [neg(base(xj, p), p), base(1, p)], p, d)
            denominator = mul(denominator, sub(base(xi, p), base(xj, p), p), p, d)
        scale = div(ys[i], denominator, p, d)
        term = [mul(scale, coef, p, d) for coef in basis]
        result = poly_add(result, term, p)
    return trim(result)


def sigma_one_slope(
    support: tuple[int, ...], a: int, alpha: Element, p: int, d: int
) -> tuple[Element, Poly, Poly]:
    loc = locator(support, p, d)
    q_poly = poly_sub(monomial(a, p), loc, p)
    z_value = poly_eval(q_poly, alpha, p, d)
    numerator = q_poly[:]
    numerator[0] = sub(numerator[0], z_value, p)
    witness_poly = divide_by_x_minus_alpha(numerator, alpha, p, d)
    return z_value, q_poly, witness_poly


def line_value(x_value: int, z_value: Element, a: int, alpha: Element, p: int, d: int) -> Element:
    numerator = sub(pow_el(base(x_value, p), a, p, d), z_value, p)
    return div(numerator, sub(base(x_value, p), alpha, p), p, d)


def direction_value(x_value: int, alpha: Element, p: int, d: int) -> Element:
    return neg(inv(sub(base(x_value, p), alpha, p), p, d), p)


def support_has_direction_explanation(
    support: tuple[int, ...], k: int, alpha: Element, p: int, d: int
) -> bool:
    sample = support[:k]
    values = [direction_value(point, alpha, p, d) for point in sample]
    candidate = interpolate(sample, values, p, d)
    return all(
        poly_eval(candidate, base(point, p), p, d) == direction_value(point, alpha, p, d)
        for point in support
    )


def support_sum(support: tuple[int, ...], p: int) -> int:
    return sum(support) % p


def elementary_symmetric(points: tuple[int, ...], degree: int, p: int) -> int:
    total = 0
    for selection in itertools.combinations(points, degree):
        product = 1
        for point in selection:
            product = (product * point) % p
        total = (total + product) % p
    return total


def has_prefix_vanishing(support: tuple[int, ...], sigma: int, p: int) -> bool:
    return all(
        elementary_symmetric(support, degree, p) == 0
        for degree in range(1, sigma)
    )


def locator_base(points: tuple[int, ...], p: int) -> list[int]:
    poly = [1]
    for point in points:
        next_poly = [0] * (len(poly) + 1)
        for degree, coef in enumerate(poly):
            next_poly[degree] = (next_poly[degree] - point * coef) % p
            next_poly[degree + 1] = (next_poly[degree + 1] + coef) % p
        poly = next_poly
    return poly


def ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)


def ceil_sqrt(value: int) -> int:
    root = isqrt(value)
    return root if root * root == value else root + 1


def character_tail_lower_bound(
    p: int, k: int, sigma: int, alpha_degree: int = 2
) -> dict[str, int]:
    n = p - 1
    a = k + sigma
    block_size = sigma + alpha_degree - 1
    tail_size = k - alpha_degree + 1
    if not (
        1 <= sigma < p
        and 2 <= alpha_degree
        and 0 <= tail_size
        and block_size <= a <= n
    ):
        raise ValueError(
            "bad character-bound parameters "
            f"p={p}, k={k}, sigma={sigma}, alpha_degree={alpha_degree}, a={a}"
        )

    random_model_numerator = comb(n, a)
    if sigma == 1:
        weil_radius = 0
        error_bound = 0
        support_lower_bound = random_model_numerator
    else:
        m = sigma - 1
        weil_radius = (m - 1) * ceil_sqrt(p) + 1
        error_bound = (p**m - 1) * comb(a + weil_radius, a)
        support_lower_numerator = random_model_numerator - error_bound
        support_lower_bound = (
            ceil_div(support_lower_numerator, p**m)
            if support_lower_numerator > 0
            else 0
        )

    tail_denominator = comb(n, tail_size)
    tail_numerator_lower = support_lower_bound * comb(a, block_size)
    tail_lower_bound = (
        ceil_div(tail_numerator_lower, tail_denominator)
        if tail_numerator_lower
        else 0
    )
    return {
        "weil_radius": weil_radius,
        "random_model_numerator": random_model_numerator,
        "character_error_bound": error_bound,
        "support_lower_bound": support_lower_bound,
        "tail_lower_bound": tail_lower_bound,
        "tail_denominator": tail_denominator,
        "tail_numerator_lower": tail_numerator_lower,
        "block_size": block_size,
        "tail_size": tail_size,
    }


def prefix_vanishing_counts(p: int, sigma: int) -> list[int]:
    width = sigma - 1
    if width < 0 or width >= p - 1:
        raise ValueError(f"bad prefix-count parameters p={p}, sigma={sigma}")
    zero_state = (0,) * width
    states: list[dict[tuple[int, ...], int]] = [dict() for _ in range(p)]
    states[0][zero_state] = 1
    max_size = 0
    for point in range(1, p):
        for size in range(max_size, -1, -1):
            for state, count in list(states[size].items()):
                old_state = (1,) + state
                new_state = list(state)
                for degree in range(1, width + 1):
                    new_state[degree - 1] = (
                        new_state[degree - 1]
                        + point * old_state[degree - 1]
                    ) % p
                key = tuple(new_state)
                states[size + 1][key] = states[size + 1].get(key, 0) + count
        max_size += 1
    return [states[size].get(zero_state, 0) for size in range(p)]


def sigma_three_prefix_counts(p: int) -> list[int]:
    states: list[dict[tuple[int, int], int]] = [dict() for _ in range(p)]
    states[0][(0, 0)] = 1
    max_size = 0
    for point in range(1, p):
        for size in range(max_size, -1, -1):
            for (e1_value, e2_value), count in list(states[size].items()):
                new_key = (
                    (e1_value + point) % p,
                    (e2_value + point * e1_value) % p,
                )
                states[size + 1][new_key] = states[size + 1].get(new_key, 0) + count
        max_size += 1
    return [states[size].get((0, 0), 0) for size in range(p)]


def verify_sigma_one_case(p: int, k: int) -> dict[str, Any]:
    d = least_nonsquare(p)
    alpha = (0, 1)
    domain = tuple(range(1, p))
    n = len(domain)
    a = k + 1
    if not (2 <= a <= n):
        raise ValueError(f"bad parameters p={p}, k={k}, a={a}, n={n}")

    all_supports = list(itertools.combinations(domain, a))
    bad_slopes: set[Element] = set()
    for support in all_supports:
        z_value, _, witness_poly = sigma_one_slope(support, a, alpha, p, d)
        if len(witness_poly) > k:
            raise AssertionError("witness polynomial degree is too high")
        for point in support:
            lhs = poly_eval(witness_poly, base(point, p), p, d)
            rhs = line_value(point, z_value, a, alpha, p, d)
            if lhs != rhs:
                raise AssertionError("line point is not explained on support")
        if support_has_direction_explanation(support, k, alpha, p, d):
            raise AssertionError("direction unexpectedly explained on support")
        bad_slopes.add(z_value)

    tail = domain[: a - 2]
    pair_points = tuple(point for point in domain if point not in tail)
    pair_slopes: dict[Element, tuple[int, int]] = {}
    for x_value, y_value in itertools.combinations(pair_points, 2):
        support = tuple(sorted(tail + (x_value, y_value)))
        z_value, _, _ = sigma_one_slope(support, a, alpha, p, d)
        if z_value in pair_slopes:
            raise AssertionError("pair-slice injectivity failed")
        pair_slopes[z_value] = (x_value, y_value)

    lower_bound = comb(p - a + 1, 2)
    density_num = len(pair_slopes)
    checks = {
        "all_supports_bad": len(all_supports) == comb(p - 1, a),
        "pair_slice_count_matches_bound": density_num == lower_bound,
        "pair_slopes_are_distinct": len(pair_slopes) == lower_bound,
        "extension_numerator_beats_base_p_when_applicable": (
            lower_bound > p if p - a + 1 >= 6 else True
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(f"failed checks for p={p}: {', '.join(failed)}")

    return {
        "p": p,
        "nonsquare_d": d,
        "field": f"F_{p}[alpha]/(alpha^2-{d})",
        "n": n,
        "k": k,
        "agreement_a": a,
        "delta": f"{n-a}/{n}",
        "all_support_count": len(all_supports),
        "distinct_slopes_from_all_supports": len(bad_slopes),
        "fixed_tail": list(tail),
        "pair_slice_bad_slope_count": density_num,
        "proved_lower_bound": lower_bound,
        "base_field_trivial_numerator": p,
        "extension_field_size": p * p,
        "mca_density_lower_bound": f"{lower_bound}/{p*p}",
        "checks": checks,
    }


def verify_sigma_three_count_case(p: int, k: int) -> dict[str, Any]:
    n = p - 1
    sigma = 3
    a = k + sigma
    if not (4 <= a <= n):
        raise ValueError(f"bad sigma-three count parameters p={p}, k={k}, a={a}")

    counts = sigma_three_prefix_counts(p)
    for size, value in enumerate(counts):
        if value != counts[n - size]:
            raise AssertionError("sigma-three complement symmetry failed")

    support_count = counts[a]
    expected_denominator = p * p
    expected_numerator = comb(n, a)
    scaled_error = abs(
        expected_denominator * support_count
        - expected_numerator
        - (p - 1) * ((-1) ** a)
    )
    integer_gauss_bound = p * (p - 1) * comb(a + ceil_sqrt(p), a)
    tail_denominator = comb(n, k - 1)
    tail_numerator = support_count * comb(a, sigma + 1)
    tail_lower_bound = ceil_div(tail_numerator, tail_denominator)

    checks = {
        "prefix_count_is_positive": support_count > 0,
        "complement_symmetry_holds": True,
        "character_error_bound_holds": scaled_error <= integer_gauss_bound,
        "averaged_tail_lower_bound_is_positive": tail_lower_bound > 0,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(
            f"failed sigma-three count checks for p={p}: {', '.join(failed)}"
        )

    return {
        "p": p,
        "n": n,
        "k": k,
        "sigma": sigma,
        "agreement_a": a,
        "prefix_vanishing_support_count": support_count,
        "random_model_numerator": expected_numerator,
        "random_model_denominator": expected_denominator,
        "scaled_character_error": scaled_error,
        "integer_gauss_error_bound": integer_gauss_bound,
        "tail_average_numerator": tail_numerator,
        "tail_average_denominator": tail_denominator,
        "proved_tail_bad_slope_lower_bound": tail_lower_bound,
        "extension_field_size": p * p,
        "mca_density_lower_bound": f"{tail_lower_bound}/{p*p}",
        "checks": checks,
    }


def verify_fixed_sigma_count_case(p: int, k: int, sigma: int) -> dict[str, Any]:
    n = p - 1
    a = k + sigma
    if not (2 <= sigma < p and sigma + 1 <= a <= n):
        raise ValueError(
            f"bad fixed-sigma count parameters p={p}, k={k}, sigma={sigma}, a={a}"
        )

    counts = prefix_vanishing_counts(p, sigma)
    for size, value in enumerate(counts):
        if value != counts[n - size]:
            raise AssertionError("fixed-sigma complement symmetry failed")

    support_count = counts[a]
    m = sigma - 1
    scaled_error = abs((p**m) * support_count - comb(n, a))
    weil_radius = (m - 1) * ceil_sqrt(p) + 1
    integer_weil_bound = (p**m - 1) * comb(a + weil_radius, a)
    tail_denominator = comb(n, k - 1)
    tail_numerator = support_count * comb(a, sigma + 1)
    tail_lower_bound = ceil_div(tail_numerator, tail_denominator)

    checks = {
        "prefix_count_is_positive": support_count > 0,
        "complement_symmetry_holds": True,
        "fixed_sigma_character_bound_holds": scaled_error <= integer_weil_bound,
        "averaged_tail_lower_bound_is_positive": tail_lower_bound > 0,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(
            f"failed fixed-sigma count checks for p={p}: {', '.join(failed)}"
        )

    return {
        "p": p,
        "n": n,
        "k": k,
        "sigma": sigma,
        "agreement_a": a,
        "prefix_vanishing_support_count": support_count,
        "scaled_character_error": scaled_error,
        "integer_weil_error_bound": integer_weil_bound,
        "tail_average_numerator": tail_numerator,
        "tail_average_denominator": tail_denominator,
        "proved_tail_bad_slope_lower_bound": tail_lower_bound,
        "extension_field_size": p * p,
        "mca_density_lower_bound": f"{tail_lower_bound}/{p*p}",
        "checks": checks,
    }


def verify_slow_slack_bound_case(p: int, k: int, sigma: int) -> dict[str, Any]:
    n = p - 1
    a = k + sigma
    if not (2 <= sigma < p and sigma + 1 <= a <= n):
        raise ValueError(
            f"bad slow-slack parameters p={p}, k={k}, sigma={sigma}, a={a}"
        )

    bound = character_tail_lower_bound(p, k, sigma)
    support_lower_bound = bound["support_lower_bound"]
    tail_lower_bound = bound["tail_lower_bound"]

    checks = {
        "character_lower_bound_is_positive": support_lower_bound > 0,
        "averaged_tail_lower_bound_is_positive": tail_lower_bound > 0,
        "tail_lower_bound_beats_base_numerator": tail_lower_bound > p,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(
            f"failed slow-slack checks for p={p}: {', '.join(failed)}"
        )

    return {
        "p": p,
        "n": n,
        "k": k,
        "sigma": sigma,
        "agreement_a": a,
        "weil_radius": bound["weil_radius"],
        "random_model_numerator_bits": (
            bound["random_model_numerator"].bit_length()
        ),
        "character_error_bound_bits": bound["character_error_bound"].bit_length(),
        "certified_support_lower_bound_bits": support_lower_bound.bit_length(),
        "certified_tail_bad_slope_lower_bound": tail_lower_bound,
        "base_field_trivial_numerator": p,
        "extension_field_size": p * p,
        "mca_density_lower_bound": f"{tail_lower_bound}/{p*p}",
        "checks": checks,
    }


def verify_extension_degree_bound_case(
    p: int, k: int, sigma: int, degrees: tuple[int, ...]
) -> dict[str, Any]:
    n = p - 1
    a = k + sigma
    bound = character_tail_lower_bound(p, k, sigma)
    tail_lower_bound = bound["tail_lower_bound"]
    degree_rows = []
    for degree in degrees:
        if degree < 2:
            raise ValueError(f"extension degree must be at least 2: {degree}")
        extension_size = p**degree
        degree_rows.append(
            {
                "extension_degree": degree,
                "extension_field_size": extension_size,
                "bad_slope_numerator_lower_bound": tail_lower_bound,
                "mca_density_lower_bound": f"{tail_lower_bound}/{extension_size}",
                "base_transfer_density": f"{p}/{extension_size}",
                "numerator_gain_over_base": f"{tail_lower_bound}/{p}",
            }
        )

    checks = {
        "bad_slope_numerator_is_positive": tail_lower_bound > 0,
        "bad_slope_numerator_beats_base": tail_lower_bound > p,
        "all_degrees_use_same_bad_slope_numerator": all(
            row["bad_slope_numerator_lower_bound"] == tail_lower_bound
            for row in degree_rows
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(
            f"failed extension-degree checks for p={p}: {', '.join(failed)}"
        )

    return {
        "p": p,
        "n": n,
        "k": k,
        "sigma": sigma,
        "agreement_a": a,
        "certified_tail_bad_slope_lower_bound": tail_lower_bound,
        "base_field_trivial_numerator": p,
        "extension_degree_rows": degree_rows,
        "checks": checks,
    }


def verify_minimal_degree_bound_case(
    p: int, k: int, sigma: int, alpha_degree: int
) -> dict[str, Any]:
    n = p - 1
    a = k + sigma
    bound = character_tail_lower_bound(p, k, sigma, alpha_degree)
    tail_lower_bound = bound["tail_lower_bound"]
    quadratic_bound = character_tail_lower_bound(p, k, sigma, 2)
    checks = {
        "bad_slope_numerator_is_positive": tail_lower_bound > 0,
        "degree_amplifies_quadratic_bound": (
            tail_lower_bound >= quadratic_bound["tail_lower_bound"]
        ),
        "tail_lower_bound_beats_base_numerator": tail_lower_bound > p,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(
            f"failed minimal-degree checks for p={p}: {', '.join(failed)}"
        )

    return {
        "p": p,
        "n": n,
        "k": k,
        "sigma": sigma,
        "agreement_a": a,
        "alpha_degree": alpha_degree,
        "block_size": bound["block_size"],
        "tail_size": bound["tail_size"],
        "certified_tail_bad_slope_lower_bound": tail_lower_bound,
        "quadratic_tail_bad_slope_lower_bound": (
            quadratic_bound["tail_lower_bound"]
        ),
        "base_field_trivial_numerator": p,
        "checks": checks,
    }


def verify_minimal_degree_template_case(
    p: int, k: int, sigma: int, alpha_degree: int
) -> dict[str, Any]:
    domain = tuple(range(1, p))
    n = len(domain)
    a = k + sigma
    block_size = sigma + alpha_degree - 1
    tail_size = k - alpha_degree + 1
    if not (0 <= tail_size and block_size <= a <= n):
        raise ValueError(
            "bad minimal-degree template parameters "
            f"p={p}, k={k}, sigma={sigma}, alpha_degree={alpha_degree}, a={a}"
        )

    admissible_supports = [
        support
        for support in itertools.combinations(domain, a)
        if has_prefix_vanishing(support, sigma, p)
    ]
    if not admissible_supports:
        raise AssertionError("minimal-degree template found no supports")

    tail_to_blocks: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for support in admissible_supports:
        for block in itertools.combinations(support, block_size):
            tail = tuple(point for point in support if point not in block)
            tail_to_blocks.setdefault(tail, []).append(block)

    best_tail, best_blocks = max(
        tail_to_blocks.items(), key=lambda item: len(item[1])
    )
    tails_count = comb(n, tail_size)
    decomposition_count = len(admissible_supports) * comb(a, block_size)
    if len(best_blocks) * tails_count < decomposition_count:
        raise AssertionError("best tail is below the minimal-degree average")

    high_reference: tuple[int, ...] | None = None
    low_keys: dict[tuple[int, ...], tuple[int, ...]] = {}
    for block in best_blocks:
        support = tuple(sorted(best_tail + block))
        if not has_prefix_vanishing(support, sigma, p):
            raise AssertionError("best-tail block is not admissible")
        loc = locator_base(block, p)
        high_key = tuple(loc[alpha_degree:])
        low_key = tuple(loc[:alpha_degree])
        if high_reference is None:
            high_reference = high_key
        elif high_key != high_reference:
            raise AssertionError("high coefficients are not fixed by the tail")
        if low_key in low_keys:
            raise AssertionError("minimal-degree block injectivity failed")
        low_keys[low_key] = block

    checks = {
        "admissible_supports_exist": bool(admissible_supports),
        "best_tail_meets_average_bound": (
            len(best_blocks) * tails_count >= decomposition_count
        ),
        "high_coefficients_are_fixed": high_reference is not None,
        "low_coefficient_keys_are_distinct": len(low_keys) == len(best_blocks),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(
            f"failed minimal-degree template checks for p={p}: {', '.join(failed)}"
        )

    return {
        "p": p,
        "n": n,
        "k": k,
        "sigma": sigma,
        "alpha_degree": alpha_degree,
        "agreement_a": a,
        "block_size": block_size,
        "tail_size": tail_size,
        "admissible_support_count": len(admissible_supports),
        "best_tail": list(best_tail),
        "best_tail_block_count": len(best_blocks),
        "average_lower_bound_numerator": decomposition_count,
        "average_lower_bound_denominator": tails_count,
        "checks": checks,
    }


def verify_fixed_slack_template_case(p: int, k: int, sigma: int) -> dict[str, Any]:
    d = least_nonsquare(p)
    alpha = (0, 1)
    domain = tuple(range(1, p))
    n = len(domain)
    a = k + sigma
    block_size = sigma + 1
    if not (block_size <= a <= n):
        raise ValueError(
            f"bad fixed-slack parameters p={p}, k={k}, sigma={sigma}, a={a}"
        )

    all_supports = list(itertools.combinations(domain, a))
    admissible_supports = [
        support for support in all_supports if has_prefix_vanishing(support, sigma, p)
    ]
    if not admissible_supports:
        raise AssertionError("fixed-slack template found no admissible supports")

    bad_slopes: set[Element] = set()
    tail_to_blocks: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for support in admissible_supports:
        z_value, q_poly, witness_poly = sigma_one_slope(support, a, alpha, p, d)
        if len(q_poly) > k + 1:
            raise AssertionError("admissible Q polynomial degree is too high")
        if len(witness_poly) > k:
            raise AssertionError("admissible witness polynomial degree is too high")
        for point in support:
            lhs = poly_eval(witness_poly, base(point, p), p, d)
            rhs = line_value(point, z_value, a, alpha, p, d)
            if lhs != rhs:
                raise AssertionError("fixed-slack line point is not explained")
        if support_has_direction_explanation(support, k, alpha, p, d):
            raise AssertionError("fixed-slack direction unexpectedly explained")
        bad_slopes.add(z_value)

        for block in itertools.combinations(support, block_size):
            tail = tuple(point for point in support if point not in block)
            tail_to_blocks.setdefault(tail, []).append(block)

    best_tail, best_blocks = max(
        tail_to_blocks.items(), key=lambda item: len(item[1])
    )
    tails_count = comb(p - 1, k - 1)
    decomposition_count = len(admissible_supports) * comb(a, block_size)
    if len(best_blocks) * tails_count < decomposition_count:
        raise AssertionError("best tail is below the fixed-slack average")

    block_slopes: dict[Element, tuple[int, ...]] = {}
    for block in best_blocks:
        support = tuple(sorted(best_tail + block))
        if not has_prefix_vanishing(support, sigma, p):
            raise AssertionError("best-tail block does not satisfy prefix vanishing")
        z_value, _, _ = sigma_one_slope(support, a, alpha, p, d)
        if z_value in block_slopes:
            raise AssertionError("fixed-slack block-slice injectivity failed")
        block_slopes[z_value] = block

    checks = {
        "admissible_supports_exist": bool(admissible_supports),
        "all_admissible_supports_bad": bool(admissible_supports),
        "best_tail_meets_average_bound": (
            len(best_blocks) * tails_count >= decomposition_count
        ),
        "best_tail_block_slopes_are_distinct": (
            len(block_slopes) == len(best_blocks)
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(
            f"failed fixed-slack checks for p={p}: {', '.join(failed)}"
        )

    return {
        "p": p,
        "nonsquare_d": d,
        "field": f"F_{p}[alpha]/(alpha^2-{d})",
        "n": n,
        "k": k,
        "sigma": sigma,
        "agreement_a": a,
        "delta": f"{n-a}/{n}",
        "admissible_support_count": len(admissible_supports),
        "distinct_slopes_from_admissible_supports": len(bad_slopes),
        "best_tail": list(best_tail),
        "best_tail_block_size": block_size,
        "best_tail_block_count": len(best_blocks),
        "average_lower_bound_numerator": decomposition_count,
        "average_lower_bound_denominator": tails_count,
        "extension_field_size": p * p,
        "checks": checks,
    }


def verify_sigma_two_case(p: int, k: int) -> dict[str, Any]:
    d = least_nonsquare(p)
    alpha = (0, 1)
    domain = tuple(range(1, p))
    n = len(domain)
    a = k + 2
    if not (3 <= a <= n):
        raise ValueError(f"bad sigma-two parameters p={p}, k={k}, a={a}, n={n}")

    all_supports = list(itertools.combinations(domain, a))
    zero_sum_supports = [
        support for support in all_supports if support_sum(support, p) == 0
    ]
    zero_sum_formula = (comb(p - 1, a) + (p - 1) * ((-1) ** a)) // p
    if len(zero_sum_supports) != zero_sum_formula:
        raise AssertionError("zero-sum support count formula failed")

    bad_slopes: set[Element] = set()
    tail_to_triples: dict[tuple[int, ...], list[tuple[int, int, int]]] = {}
    for support in zero_sum_supports:
        z_value, q_poly, witness_poly = sigma_one_slope(support, a, alpha, p, d)
        if len(q_poly) > k + 1:
            raise AssertionError("zero-sum Q polynomial degree is too high")
        if len(witness_poly) > k:
            raise AssertionError("sigma-two witness polynomial degree is too high")
        for point in support:
            lhs = poly_eval(witness_poly, base(point, p), p, d)
            rhs = line_value(point, z_value, a, alpha, p, d)
            if lhs != rhs:
                raise AssertionError("sigma-two line point is not explained")
        if support_has_direction_explanation(support, k, alpha, p, d):
            raise AssertionError("sigma-two direction unexpectedly explained")
        bad_slopes.add(z_value)

        for triple in itertools.combinations(support, 3):
            tail = tuple(point for point in support if point not in triple)
            tail_to_triples.setdefault(tail, []).append(triple)

    best_tail, best_triples = max(
        tail_to_triples.items(), key=lambda item: len(item[1])
    )
    tails_count = comb(p - 1, k - 1)
    decomposition_count = len(zero_sum_supports) * comb(a, 3)
    if len(best_triples) * tails_count < decomposition_count:
        raise AssertionError("best tail is below the averaged lower bound")

    tail_sum = support_sum(best_tail, p)
    triple_slopes: dict[Element, tuple[int, int, int]] = {}
    for triple in best_triples:
        if (tail_sum + support_sum(triple, p)) % p != 0:
            raise AssertionError("best-tail triple is not zero-sum with tail")
        support = tuple(sorted(best_tail + triple))
        z_value, _, _ = sigma_one_slope(support, a, alpha, p, d)
        if z_value in triple_slopes:
            raise AssertionError("sigma-two triple-slice injectivity failed")
        triple_slopes[z_value] = triple

    checks = {
        "zero_sum_formula_matches": len(zero_sum_supports) == zero_sum_formula,
        "all_zero_sum_supports_bad": bool(zero_sum_supports),
        "best_tail_meets_average_bound": (
            len(best_triples) * tails_count >= decomposition_count
        ),
        "best_tail_triple_slopes_are_distinct": (
            len(triple_slopes) == len(best_triples)
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(
            f"failed sigma-two checks for p={p}: {', '.join(failed)}"
        )

    return {
        "p": p,
        "nonsquare_d": d,
        "field": f"F_{p}[alpha]/(alpha^2-{d})",
        "n": n,
        "k": k,
        "agreement_a": a,
        "delta": f"{n-a}/{n}",
        "zero_sum_support_count": len(zero_sum_supports),
        "zero_sum_formula_count": zero_sum_formula,
        "distinct_slopes_from_zero_sum_supports": len(bad_slopes),
        "best_tail": list(best_tail),
        "best_tail_triple_count": len(best_triples),
        "average_lower_bound_numerator": decomposition_count,
        "average_lower_bound_denominator": tails_count,
        "extension_field_size": p * p,
        "checks": checks,
    }


def compute_report() -> dict[str, Any]:
    sigma_one_cases = [verify_sigma_one_case(**case) for case in SIGMA_ONE_CASES]
    sigma_two_cases = [verify_sigma_two_case(**case) for case in SIGMA_TWO_CASES]
    sigma_three_cases = [
        verify_fixed_slack_template_case(sigma=3, **case)
        for case in SIGMA_THREE_CASES
    ]
    sigma_three_count_cases = [
        verify_sigma_three_count_case(**case)
        for case in SIGMA_THREE_COUNT_CASES
    ]
    fixed_sigma_count_cases = [
        verify_fixed_sigma_count_case(**case)
        for case in FIXED_SIGMA_COUNT_CASES
    ]
    slow_slack_bound_cases = [
        verify_slow_slack_bound_case(**case)
        for case in SLOW_SLACK_BOUND_CASES
    ]
    extension_degree_bound_cases = [
        verify_extension_degree_bound_case(**case)
        for case in EXTENSION_DEGREE_BOUND_CASES
    ]
    minimal_degree_template_cases = [
        verify_minimal_degree_template_case(**case)
        for case in MINIMAL_DEGREE_TEMPLATE_CASES
    ]
    minimal_degree_bound_cases = [
        verify_minimal_degree_bound_case(**case)
        for case in MINIMAL_DEGREE_BOUND_CASES
    ]
    return {
        "status": "PASS",
        "proof_status": "FINITE_MODEL_CHECK / COUNTEREXAMPLE_SANITY",
        "claim": (
            "For sigma=1 and a=k+1, the extension-valued line "
            "(x^a-z)/(x-alpha) has at least binom(p-a+1,2) support-wise "
            "MCA-bad slopes over F_{p^2}; for sigma=2 and a=k+2, zero-sum "
            "supports give a tail with the averaged number of distinct bad "
            "triple slopes; the note proves a fixed-sigma character bound for "
            "the general prefix-vanishing template, and sigma=3 finite cases "
            "check exact dynamic support counts. The same character-bound "
            "formula gives finite slow-slack certificates where the forced "
            "extension numerator already exceeds the base-field numerator, "
            "with the same numerator over every extension degree. If alpha has "
            "higher base-field degree, the fixed-tail injectivity block can be "
            "enlarged and the numerator grows like the corresponding power of p."
        ),
        "sigma_one_cases": sigma_one_cases,
        "sigma_two_cases": sigma_two_cases,
        "sigma_three_template_cases": sigma_three_cases,
        "sigma_three_count_cases": sigma_three_count_cases,
        "fixed_sigma_count_cases": fixed_sigma_count_cases,
        "slow_slack_bound_cases": slow_slack_bound_cases,
        "extension_degree_bound_cases": extension_degree_bound_cases,
        "minimal_degree_template_cases": minimal_degree_template_cases,
        "minimal_degree_bound_cases": minimal_degree_bound_cases,
    }


def print_report(report: dict[str, Any]) -> None:
    print("f1_fixed_rate_extension_counterexample: PASS")
    for case in report["sigma_one_cases"]:
        print(
            "sigma=1 p={p} k={k} a={agreement_a} "
            "lower_bound={proved_lower_bound} "
            "density={mca_density_lower_bound} "
            "distinct_all={distinct_slopes_from_all_supports}".format(**case)
        )
    for case in report["sigma_two_cases"]:
        print(
            "sigma=2 p={p} k={k} a={agreement_a} "
            "zero_sum={zero_sum_support_count} "
            "best_tail_triples={best_tail_triple_count}".format(**case)
        )
    for case in report["sigma_three_template_cases"]:
        print(
            "sigma=3 p={p} k={k} a={agreement_a} "
            "admissible={admissible_support_count} "
            "best_tail_blocks={best_tail_block_count}".format(**case)
        )
    for case in report["sigma_three_count_cases"]:
        print(
            "sigma=3-count p={p} k={k} a={agreement_a} "
            "G={prefix_vanishing_support_count} "
            "tail_lower={proved_tail_bad_slope_lower_bound} "
            "density={mca_density_lower_bound}".format(**case)
        )
    for case in report["fixed_sigma_count_cases"]:
        print(
            "sigma={sigma}-count p={p} k={k} a={agreement_a} "
            "G={prefix_vanishing_support_count} "
            "tail_lower={proved_tail_bad_slope_lower_bound} "
            "density={mca_density_lower_bound}".format(**case)
        )
    for case in report["slow_slack_bound_cases"]:
        print(
            "slow-slack p={p} sigma={sigma} k={k} a={agreement_a} "
            "tail_lower={certified_tail_bad_slope_lower_bound} "
            "base_numerator={base_field_trivial_numerator} "
            "density={mca_density_lower_bound}".format(**case)
        )
    for case in report["extension_degree_bound_cases"]:
        degrees = ",".join(
            str(row["extension_degree"])
            for row in case["extension_degree_rows"]
        )
        print(
            "extension-degree p={p} sigma={sigma} "
            "tail_lower={certified_tail_bad_slope_lower_bound} "
            "base_numerator={base_field_trivial_numerator} "
            "degrees={degrees}".format(**case, degrees=degrees)
        )
    for case in report["minimal_degree_template_cases"]:
        print(
            "minimal-degree-template r={alpha_degree} p={p} "
            "sigma={sigma} k={k} a={agreement_a} "
            "blocks={best_tail_block_count}".format(**case)
        )
    for case in report["minimal_degree_bound_cases"]:
        print(
            "minimal-degree-bound r={alpha_degree} p={p} "
            "sigma={sigma} k={k} tail_lower={certified_tail_bad_slope_lower_bound} "
            "quadratic_tail={quadratic_tail_bad_slope_lower_bound}".format(**case)
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()
    report = compute_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
