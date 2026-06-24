#!/usr/bin/env python3
"""Verify finite instances of the F1 fixed-rate extension-line obstruction."""

from __future__ import annotations

import argparse
import itertools
import json
from math import comb
from typing import Any


Element = tuple[int, int]
Poly = list[Element]


CASES = (
    {"p": 5, "k": 2},
    {"p": 7, "k": 3},
    {"p": 11, "k": 5},
    {"p": 13, "k": 6},
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


def verify_case(p: int, k: int) -> dict[str, Any]:
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


def compute_report() -> dict[str, Any]:
    cases = [verify_case(**case) for case in CASES]
    return {
        "status": "PASS",
        "proof_status": "FINITE_MODEL_CHECK / COUNTEREXAMPLE_SANITY",
        "claim": (
            "For sigma=1 and a=k+1, the extension-valued line "
            "(x^a-z)/(x-alpha) has at least binom(p-a+1,2) support-wise "
            "MCA-bad slopes over F_{p^2}."
        ),
        "cases": cases,
    }


def print_report(report: dict[str, Any]) -> None:
    print("f1_fixed_rate_extension_counterexample: PASS")
    for case in report["cases"]:
        print(
            "p={p} k={k} a={agreement_a} lower_bound={proved_lower_bound} "
            "density={mca_density_lower_bound} "
            "distinct_all={distinct_slopes_from_all_supports}".format(**case)
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
