#!/usr/bin/env python3
"""Exact near-aligned positive projective-boundary q-slice exclusion.

Proof status: PROVED when all seven pinned packet cases pass.
Reproducibility: deterministic exact SymPy arithmetic; no random seed.
JSON certificate: owned by the saturated-112 q-slice packet verifier.
"""

from __future__ import annotations

import argparse
import hashlib

import sympy as sp


DEPLOYED_PRIME = 2130706433


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return sp.Matrix([left * right, -left - right, 1])


def divide_known(poly, variables, factors):
    result = sp.Poly(poly, *variables, domain=sp.QQ).primitive()[1]
    for factor in factors:
        divisor = sp.Poly(factor, *variables, domain=sp.QQ)
        while sp.rem(result, divisor) == 0:
            result = result.exquo(divisor)
    return result


def integer_expression(poly):
    return poly.clear_denoms(convert=True)[1].as_expr()


def unit_basis(basis, variables):
    return (
        len(basis.polys) == 1
        and sp.Poly(
            basis.polys[0].as_expr(), *variables, modulus=DEPLOYED_PRIME
        ).total_degree() == 0
    )


def digest(polys, variables):
    payload = []
    for value in polys:
        payload.append(
            sp.Poly(value, *variables, modulus=DEPLOYED_PRIME).monic().terms()
        )
    return hashlib.sha256(repr(payload).encode("ascii")).hexdigest()


def residual_after_w2(expression, W):
    numerator, denominator = sp.fraction(sp.cancel(expression))
    quotient, remainder = sp.div(sp.Poly(numerator, W), sp.Poly(W**2, W))
    require(remainder.is_zero, "forced W^2 division")
    return sp.cancel(quotient.as_expr() / denominator)


def reconstruct(template):
    b, d, W = sp.symbols("b d W", nonzero=True)
    a = sp.Rational(2)
    z = sp.cancel((d - 2) / (2 - 4 * d))
    V = sp.Matrix([-d, 1 + W, -d * W])
    at_z = V.subs(W, z)
    ell_1 = at_z[2]
    ell_0 = at_z[1] + a * ell_1

    if template == "fixed-moving":
        first, second = edge(a, 1 / a), edge(a, b)
        r, s = 1 / a, b
    else:
        first, second = edge(a, b), edge(a, 1 / b)
        r, s = b, 1 / b
    target = sp.Matrix([
        sp.cancel(value)
        for value in (
            ((ell_0 + s * ell_1) * first
             + (ell_0 + r * ell_1) * second) / (s - r)
        )
    ])

    coefficients = sp.symbols("x0:5")
    x0, x1, x2, x3, x4 = coefficients
    U_raw = sp.Matrix([
        x0 + x1 * W + x2 * W**2,
        x3 * (1 + W**2) + x4 * W,
        x2 + x1 * W + x0 * W**2,
    ])
    equations = [
        x2,
        x0 + d * x3,
        *(U_raw[index].subs(W, z) - target[index] for index in range(3)),
    ]
    matrix, right = sp.linear_eq_to_matrix(equations, coefficients)
    solution = [sp.cancel(value) for value in matrix.inv(method="DM") * right]
    U = sp.Matrix([
        sp.cancel(value.subs(dict(zip(coefficients, solution))))
        for value in U_raw
    ])

    require(sp.cancel(U[2].subs(W, 0)) == 0, "infinity q-root")
    require(
        sp.cancel(U[0].subs(W, 0) + d * U[1].subs(W, 0)) == 0,
        "finite q-root",
    )
    require(all(
        sp.cancel(U[index].subs(W, z) - target[index]) == 0
        for index in range(3)
    ), "internal reconstruction")

    U_d = sp.cancel(U[0] + d * U[1] + d**2 * U[2])
    V_d = sp.expand(V[0] + d * V[1] + d**2 * V[2])
    finite_residual = residual_after_w2(U_d**2 - W * V_d**2, W)
    infinity_residual = residual_after_w2(U[2]**2 - W * V[2]**2, W)
    product = sp.Poly(
        sp.cancel(finite_residual * infinity_residual), W,
        domain=sp.QQ.frac_field(b, d),
    )
    require(product.degree() == 4, "projective q-slice degree")
    return (b, d, W), solution, product


def common_factors(b, d, moving):
    factors = [
        b, b - 2, 2 * b - 1, b - 1, b + 1,
        d, d - 2, 2 * d - 1, d - 1, d + 1,
        d - b, b * d - 1, 5 * d - 4,
    ]
    if moving:
        factors.append(b * b * d - 2 * b + d)
    return factors


def coefficient_equations(product, xi, variables):
    b, d, W = variables
    target = sp.Poly(
        (W - 1 / xi) ** 2 * (W - 1 / d) ** 2,
        W,
        domain=sp.QQ.frac_field(b, d),
    )
    result = []
    for degree in range(4):
        value = sp.cancel(
            product.nth(degree) - product.nth(4) * target.nth(degree)
        )
        numerator, _ = sp.fraction(value)
        result.append(sp.Poly(numerator, b, d, domain=sp.QQ).primitive()[1])
    return result


def trace_reduce(poly, b, trace, d):
    as_b = sp.Poly(poly.as_expr(), b, domain=sp.QQ.frac_field(d))
    degree = as_b.degree()
    require(degree % 2 == 0, "trace degree")
    require(all(
        sp.cancel(as_b.nth(index) - as_b.nth(degree - index)) == 0
        for index in range(degree + 1)
    ), "nonreciprocal moving equation")
    middle = degree // 2
    traces = [sp.Integer(2), trace]
    for _ in range(2, middle + 1):
        traces.append(sp.expand(trace * traces[-1] - traces[-2]))
    reduced = as_b.nth(middle)
    for offset in range(1, middle + 1):
        reduced += as_b.nth(middle + offset) * traces[offset]
    numerator, _ = sp.fraction(sp.cancel(reduced))
    return sp.Poly(numerator, trace, d, domain=sp.QQ).primitive()[1]


def direct_saturation(template, xi_name):
    variables, _, product = reconstruct(template)
    b, d, _ = variables
    xi = {"a": sp.Rational(2), "tau-a": sp.Rational(1, 2), "other": b}[
        xi_name
    ]
    moving = template == "moving-moving"
    factors = common_factors(b, d, moving)
    equations = coefficient_equations(product, xi, variables)
    equations = [divide_known(value, (b, d), factors) for value in equations]
    inverse = sp.Symbol("saturation_inverse")
    forbidden = sp.prod(factors)
    integer_polys = [integer_expression(value) for value in equations]
    basis = sp.groebner(
        [*integer_polys, inverse * forbidden - 1],
        inverse, b, d,
        order="grevlex",
        modulus=DEPLOYED_PRIME,
    )
    require(unit_basis(basis, (inverse, b, d)), "direct saturation")
    print(
        "KB_C2_112_NEAR_POSITIVE_PROJECTIVE_PASS "
        f"template={template} xi={xi_name} chart=direct basis=unit "
        f"digest={digest([*integer_polys, forbidden], (b, d))}"
    )


def trace_saturation(xi_name):
    variables, _, product = reconstruct("moving-moving")
    b, d, _ = variables
    xi = sp.Rational(2) if xi_name == "a" else sp.Rational(1, 2)
    factors = common_factors(b, d, True)
    equations = coefficient_equations(product, xi, variables)
    equations = [divide_known(value, (b, d), factors) for value in equations]
    trace = sp.Symbol("trace")
    traced = [trace_reduce(value, b, trace, d) for value in equations]
    inverse = sp.Symbol("saturation_inverse")
    forbidden = (
        (trace - 2) * (trace + 2) * (2 * trace - 5)
        * d * (d - 2) * (2 * d - 1) * (d - 1) * (d + 1)
        * (5 * d - 4) * (d * d - d * trace + 1) * (d * trace - 2)
    )
    integer_polys = [integer_expression(value) for value in traced]
    basis = sp.groebner(
        [*integer_polys, inverse * forbidden - 1],
        inverse, trace, d,
        order="grevlex",
        modulus=DEPLOYED_PRIME,
    )
    require(unit_basis(basis, (inverse, trace, d)), "trace saturation")
    print(
        "KB_C2_112_NEAR_POSITIVE_PROJECTIVE_PASS "
        f"template=moving-moving xi={xi_name} chart=trace basis=unit "
        f"digest={digest([*integer_polys, forbidden], (trace, d))}"
    )


def other_branch(sign):
    variables, solution, product = reconstruct("moving-moving")
    b, d, _ = variables
    x0, x1, x2, x3, x4 = solution
    factors = common_factors(b, d, True)
    equations = coefficient_equations(product, b, variables)

    finite_constant = sp.cancel(x1 * (1 + d * d) + d * x4)
    finite_leading = sp.cancel(x2 + d * x3 + d * d * x0)
    branch = sp.cancel(
        b * d * finite_constant * x1 - sign * finite_leading * x0
    )
    branch_numerator, _ = sp.fraction(branch)
    selected = [sp.Poly(branch_numerator, b, d, domain=sp.QQ)]
    selected.extend(equations[index] for index in (1, 2, 3))
    selected = [divide_known(value, (b, d), factors) for value in selected]

    inverse = sp.Symbol("saturation_inverse")
    forbidden = sp.prod(factors)
    integer_polys = [integer_expression(value) for value in selected]
    basis = sp.groebner(
        [*integer_polys, inverse * forbidden - 1],
        inverse, b, d,
        order="grevlex",
        modulus=DEPLOYED_PRIME,
    )
    require(unit_basis(basis, (inverse, b, d)), "other-xi branch saturation")
    print(
        "KB_C2_112_NEAR_POSITIVE_PROJECTIVE_PASS "
        f"template=moving-moving xi=other chart=constant-sign-{sign:+d} "
        f"basis=unit digest={digest([*integer_polys, forbidden], (b, d))}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("template", choices=("fixed-moving", "moving-moving"))
    parser.add_argument("--xi", required=True, choices=("a", "tau-a", "other"))
    parser.add_argument("--sign", type=int, choices=(-1, 1))
    args = parser.parse_args()

    if args.template == "fixed-moving":
        require(args.sign is None, "fixed sign branch")
        direct_saturation(args.template, args.xi)
    elif args.xi in ("a", "tau-a"):
        require(args.sign is None, "trace sign branch")
        trace_saturation(args.xi)
    else:
        require(args.sign is not None, "other-xi requires sign")
        other_branch(args.sign)


if __name__ == "__main__":
    main()
