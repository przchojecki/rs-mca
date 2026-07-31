#!/usr/bin/env python3
"""Saturate one aligned positive forced-ramified c2 (1,1,2) chart.

Proof status: PROVED when all six pinned packet cases pass.
Reproducibility: deterministic exact SymPy arithmetic; no random seed.
JSON certificate: owned by the saturated-112 q-slice packet verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
SYMMETRIC = (
    HERE / "kb_mca_v4_m2_u2_saturated_112_positive_qslice_core_v1.py"
)
DEPLOYED_PRIME = 2130706433


def load_symmetric():
    spec = importlib.util.spec_from_file_location("positive_symmetric", SYMMETRIC)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load corrected q-slice generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def divide_known(poly, variables, factors):
    """Remove only exact factors already included in the open-set product."""
    result = sp.Poly(poly, *variables, domain=sp.QQ).primitive()[1]
    for factor in factors:
        divisor = sp.Poly(factor, *variables, domain=sp.QQ)
        while sp.rem(result, divisor) == 0:
            result = result.exquo(divisor)
    return result


def integer_expression(poly):
    return poly.clear_denoms(convert=True)[1].as_expr()


def digest(polys, variables):
    payload = []
    for value in polys:
        poly = sp.Poly(value, *variables, modulus=DEPLOYED_PRIME).monic()
        payload.append(poly.terms())
    return hashlib.sha256(repr(payload).encode("ascii")).hexdigest()


def is_unit_basis(basis, variables):
    if len(basis.polys) != 1:
        return False
    return sp.Poly(
        basis.polys[0].as_expr(), *variables, modulus=DEPLOYED_PRIME
    ).total_degree() == 0


def raw_ramified_system(template, allocation):
    symmetric = load_symmetric()
    variables, odd, coefficients, _, relative_scale = (
        symmetric.reconstruct_fraction_free(template)
    )
    p, t, b, w = variables
    scale = sp.Symbol("lambda_scale")

    symmetric.audit_reconstruction(
        template, variables, coefficients, relative_scale
    )
    equations = symmetric.ramified_allocation_equations(
        allocation, (p, t, b, w, scale), coefficients, relative_scale
    )
    normalization = sp.Poly(equations[-1].as_expr(), scale)
    require(normalization.degree() == 1, "scale normalization is not linear")
    scale_value = sp.cancel(-normalization.nth(0) / normalization.nth(1))

    alpha = p + 2 * t + 4
    fixed_expected = 3 * (2 * b - 1) * (p - 1) * alpha
    moving_expected = (
        -3 * (b - 1) * (b + 1) * (p - 1)
        * alpha * (5 * p + 4 * t + 5)
    )
    expected = fixed_expected if template == "fixed-moving" else moving_expected
    require(sp.cancel(scale_value - expected) == 0, "scale factorization")

    reduced = []
    for equation in equations[:-1]:
        specialized = sp.cancel(equation.as_expr().subs(scale, scale_value))
        numerator, denominator = sp.fraction(specialized)
        require(denominator != 0 and not denominator.free_symbols, "denominator")
        poly = sp.Poly(numerator, b, p, t, domain=sp.QQ)
        collision_square = sp.Poly((p - 1) ** 2, b, p, t, domain=sp.QQ)
        require(sp.rem(poly, collision_square) == 0, "missing p=1 factor")
        poly = poly.exquo(collision_square)
        factors = (
            (2 * b - 1, p, p - 1, alpha)
            if template == "fixed-moving"
            else (p, p - 1, alpha)
        )
        reduced.append(divide_known(poly.as_expr(), (b, p, t), factors))
    return symmetric, (p, t, b), coefficients, scale_value, reduced


def fixed_saturation(allocation):
    _, (p, t, b), _, scale_value, reduced = raw_ramified_system(
        "fixed-moving", allocation
    )
    u = sp.Symbol("saturation_inverse")
    alpha = p + 2 * t + 4
    beta = 4 * p + 2 * t + 1
    incidence = 5 * p + 4 * t + 5
    forbidden = (
        b * (b - 2) * (2 * b - 1) * (b - 1) * (b + 1)
        * p * (p - 1) * (p - t + 1) * (p + t + 1)
        * alpha * beta * incidence * (t * t - 4 * p)
        * (b * b + t * b + p) * (1 + t * b + p * b * b)
    )
    integer_polys = [integer_expression(poly) for poly in reduced]
    variables = (u, b, p, t)
    basis = sp.groebner(
        [*integer_polys, u * forbidden - 1],
        *variables,
        order="grevlex",
        modulus=DEPLOYED_PRIME,
    )
    require(is_unit_basis(basis, variables), "fixed saturation is not unit")
    print(
        "KB_C2_112_ALIGNED_POSITIVE_RAMIFIED_SATURATION_PASS "
        f"template=fixed-moving allocation={allocation} "
        f"scale={sp.factor(scale_value)} basis=unit "
        f"digest={digest([*integer_polys, forbidden], (b, p, t))}"
    )


def trace_reduce(poly, b, trace, p, t):
    field = sp.QQ.frac_field(p, t)
    as_b = sp.Poly(poly.as_expr(), b, domain=field)
    require(as_b.degree() == 4, "moving b-degree")
    require(
        all(sp.cancel(as_b.nth(index) - as_b.nth(4 - index)) == 0
            for index in range(5)),
        "moving equation is not reciprocal",
    )
    reduced = sp.cancel(
        as_b.nth(4) * (trace * trace - 2)
        + as_b.nth(3) * trace
        + as_b.nth(2)
    )
    numerator, denominator = sp.fraction(reduced)
    require(denominator != 0, "trace denominator")
    return sp.Poly(numerator, trace, p, t, domain=sp.QQ).primitive()[1]


def moving_saturation(allocation):
    _, (p, t, b), _, scale_value, reduced = raw_ramified_system(
        "moving-moving", allocation
    )
    trace = sp.Symbol("trace")
    u = sp.Symbol("saturation_inverse")
    traced = [trace_reduce(poly, b, trace, p, t) for poly in reduced]

    alpha = p + 2 * t + 4
    beta = 4 * p + 2 * t + 1
    incidence = 5 * p + 4 * t + 5
    endpoint_orbit_collision = (
        p * (trace * trace - 2)
        + t * (1 + p) * trace
        + 1 + t * t + p * p
    )
    forbidden = (
        (trace - 2) * (trace + 2) * (2 * trace - 5)
        * p * (p - 1) * (p - t + 1) * (p + t + 1)
        * alpha * beta * incidence * (t * t - 4 * p)
        * endpoint_orbit_collision
    )
    integer_polys = [integer_expression(poly) for poly in traced]
    variables = (u, trace, p, t)
    basis = sp.groebner(
        [*integer_polys, u * forbidden - 1],
        *variables,
        order="grevlex",
        modulus=DEPLOYED_PRIME,
    )
    require(is_unit_basis(basis, variables), "moving saturation is not unit")
    print(
        "KB_C2_112_ALIGNED_POSITIVE_RAMIFIED_SATURATION_PASS "
        f"template=moving-moving allocation={allocation} "
        f"scale={sp.factor(scale_value)} trace_descent=true basis=unit "
        f"digest={digest([*integer_polys, forbidden], (trace, p, t))}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "template", choices=("fixed-moving", "moving-moving")
    )
    parser.add_argument(
        "allocation", choices=("same", "swap", "mixed")
    )
    args = parser.parse_args()
    if args.template == "fixed-moving":
        fixed_saturation(args.allocation)
    else:
        moving_saturation(args.allocation)


if __name__ == "__main__":
    main()
