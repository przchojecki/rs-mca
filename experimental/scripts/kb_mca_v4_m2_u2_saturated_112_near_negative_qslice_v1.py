#!/usr/bin/env python3
"""Inspect the near-aligned q-slice on the genuine negative B locus.

Proof status: PROVED when all pinned packet cases pass.
Reproducibility: deterministic exact SymPy arithmetic; no random seed.
JSON certificate: owned by the saturated-112 q-slice packet verifier.
"""

from __future__ import annotations

import argparse

import sympy as sp

from kb_mca_v4_m2_u2_saturated_112_negative_qslice_core_v1 import reconstruct


CHARACTERISTIC = 2130706433


def primitive_numerator(value, *variables):
    numerator = sp.fraction(sp.cancel(value))[0]
    return sp.Poly(numerator, *variables, domain=sp.QQ).primitive()[1]


def residue_gcd(polynomials, parameter, variable, factor):
    factor = sp.Poly(factor, parameter, domain=sp.QQ).monic()
    if factor.degree() == 1:
        root = -factor.nth(0)
        values = [
            sp.Poly(value.as_expr().subs(parameter, root), variable, domain=sp.QQ)
            for value in polynomials
        ]
        label = str(root)
    else:
        root = sp.CRootOf(factor.as_expr(), 0)
        values = [
            sp.Poly(
                value.as_expr().subs(parameter, root),
                variable,
                extension=root,
            )
            for value in polynomials
        ]
        label = str(factor.as_expr())
    common = values[0]
    for value in values[1:]:
        common = sp.gcd(common, value)
    return label, common.monic()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "template", choices=("fixed-moving", "moving-moving")
    )
    parser.add_argument(
        "--xi", choices=("all", "a", "tau-a", "other"), default="all"
    )
    parser.add_argument("--eliminate", action="store_true")
    parser.add_argument("--fibers", action="store_true")
    parser.add_argument("--modular-saturate", action="store_true")
    parser.add_argument("--compare-templates", action="store_true")
    args = parser.parse_args()

    (c, d, w, W), z, u, v, forced_residual = reconstruct(args.template)
    if forced_residual != 0:
        raise RuntimeError("remaining forced row")
    if args.compare_templates:
        other_name = (
            "moving-moving"
            if args.template == "fixed-moving"
            else "fixed-moving"
        )
        _, other_z, other_u, other_v, other_forced = reconstruct(other_name)
        if other_forced != 0 or sp.cancel(z - other_z) != 0:
            raise RuntimeError("template incidence")
        if not all(sp.cancel(left + right) == 0
                   for left, right in zip(u, other_u)):
            raise RuntimeError("template U sign")
        if not all(sp.cancel(left - right) == 0
                   for left, right in zip(v, other_v)):
            raise RuntimeError("template V equality")
        print(
            "KB_C2_112_NEAR_NEGATIVE_TEMPLATE_EQUIVALENCE_PASS "
            "same_z=true U_opposite=true V_equal=true G_equal=true",
            flush=True,
        )
        return

    q0 = c * d
    minor = sp.Matrix([
        [1, z, z**2],
        [-z**2, -z, -1],
        [1 + q0 * w**2, w * (1 + q0), w**2 + q0],
    ]).det()
    e = (
        c * d * w + 4 * c * d - 2 * c * w - 2 * c
        - 2 * d * w - 2 * d + 4 * w + 1
    )
    a_factor = 5 * c * d - 4 * c - 4 * d + 5
    expected_minor = (
        3 * (c - 2) * (2 * c - 1) * (d - 2) * (2 * d - 1)
        * (w - 1) ** 3 * (w + 1) ** 3
        * (c * d - 1) * (c * d + 1) * a_factor / e**4
    )
    if sp.cancel(minor - expected_minor) != 0:
        raise RuntimeError("reconstruction minor")
    print(
        f"template={args.template} reconstruction_minor=FACTORED",
        flush=True,
    )

    field = sp.QQ.frac_field(c, d, w)
    u_root = sum(u[index] * c**index for index in range(3))
    v_root = sum(v[index] * c**index for index in range(3))
    norm = (
        sp.Poly(u_root, W, domain=field) ** 2
        - sp.Poly(W, W, domain=field)
        * sp.Poly(v_root, W, domain=field) ** 2
    )
    residual, remainder = norm.div(
        sp.Poly((W - w) ** 2, W, domain=field)
    )
    if not remainder.is_zero or residual.degree() != 2:
        raise RuntimeError("forced square quotient")
    swap = {c: d, d: c}
    conjugate = sp.Poly.from_list(
        [coefficient.xreplace(swap) for coefficient in residual.all_coeffs()],
        gens=W,
        domain=field,
    )
    observed = (residual * conjugate).monic()
    if sp.cancel(observed.nth(0) - 1) != 0:
        raise RuntimeError("observed constant")
    print(
        f"template={args.template} observed_constant=1",
        flush=True,
    )

    p = c * d - 2 * c - 2 * d + 1
    q = 2 * c * d - c - d + 2
    b = sp.cancel(-q / p)
    xi_values = {
        "a": sp.Rational(2),
        "tau-a": sp.Rational(1, 2),
        "other": b,
    }
    for name, xi in xi_values.items():
        if args.xi != "all" and name != args.xi:
            continue
        expected = sp.Poly(
            (W - 1 / xi) ** 2 * (W - 1 / d) ** 2,
            W,
            domain=field,
        ).monic()
        mismatch = observed - expected
        expected_constant = sp.cancel(1 / (xi**2 * d**2))
        if sp.cancel(mismatch.nth(0) - (1 - expected_constant)) != 0:
            raise RuntimeError(f"constant mismatch: {name}")
        print(
            f"template={args.template} xi={name} "
            f"constant_numerator="
            f"{sp.factor(primitive_numerator(mismatch.nth(0), c, d).as_expr())}",
            flush=True,
        )

        specialization = (
            {d: sp.Rational(-1, 2)}
            if name == "a"
            else {d: sp.Rational(-2)}
            if name == "tau-a"
            else None
        )
        if specialization is not None:
            specialized = [
                primitive_numerator(
                    mismatch.nth(degree).subs(specialization), c, w
                )
                for degree in range(1, 4)
            ]
            factors = [
                sp.factor(value.as_expr()) for value in specialized
            ]
            common = sp.gcd(*specialized).primitive()[1]
            print(
                f"template={args.template} xi={name} minus_branch="
                f"d={specialization[d]} factors={factors} "
                f"common={sp.factor(common.as_expr())}",
                flush=True,
            )
            if args.eliminate:
                r13 = sp.Poly(
                    sp.resultant(
                        specialized[0].as_expr(),
                        specialized[2].as_expr(), w,
                    ),
                    c, domain=sp.QQ,
                ).primitive()[1]
                r12 = sp.Poly(
                    sp.resultant(
                        specialized[0].as_expr(),
                        specialized[1].as_expr(), w,
                    ),
                    c, domain=sp.QQ,
                ).primitive()[1]
                projection = sp.gcd(r13, r12).primitive()[1]
                print(
                    f"template={args.template} xi={name} "
                    f"resultant_degrees=({r13.degree()},{r12.degree()}) "
                    f"projection={sp.factor(projection.as_expr())}",
                    flush=True,
                )
                if args.fibers:
                    for factor, _ in sp.factor_list(
                        projection.as_expr()
                    )[1]:
                        label, fiber = residue_gcd(
                            specialized, c, w, factor
                        )
                        print(
                            f"template={args.template} xi={name} "
                            f"fiber={label} w_gcd_degree={fiber.degree()} "
                            f"w_gcd={fiber.as_expr()}",
                            flush=True,
                        )
            if args.modular_saturate:
                inverse = sp.symbols("inverse")
                saturated = sp.groebner(
                    [
                        *(value.as_expr() for value in specialized),
                        inverse * (w - 1) * (w + 1) - 1,
                    ],
                    inverse, w, c,
                    order="lex", modulus=CHARACTERISTIC,
                )
                unit = (
                    len(saturated.polys) == 1
                    and saturated.polys[0].as_expr() == 1
                )
                print(
                    f"template={args.template} xi={name} "
                    f"modular_forbidden_saturation_unit={unit}",
                    flush=True,
                )
                if not unit:
                    raise RuntimeError(f"modular survivor: {name}")
            continue

        # On the other-xi minus branch, xi*d=-1 and B=0 are imposed
        # simultaneously.  Substitute b=-1/d into B=b*p+q first.
        branch = primitive_numerator(q - p / d, c, d)
        c_value = sp.cancel((d**2 - 4*d + 1) / (2 * (d**2 - d + 1)))
        if sp.cancel(branch.as_expr().subs(c, c_value)) != 0:
            raise RuntimeError("other-xi minus branch")
        reduced = [
            primitive_numerator(
                mismatch.nth(degree).subs(c, c_value), d, w
            )
            for degree in range(1, 4)
        ]
        common = sp.gcd(*reduced).primitive()[1]
        print(
            f"template={args.template} xi=other minus_branch="
            f"{sp.factor(branch.as_expr())} "
            f"reduced_degrees="
            f"{[tuple(value.degree(x) for x in (d, w)) for value in reduced]} "
            f"common={sp.factor(common.as_expr())}",
            flush=True,
        )
        if args.eliminate:
            r13 = sp.Poly(
                sp.resultant(
                    reduced[0].as_expr(), reduced[2].as_expr(), w
                ),
                d, domain=sp.QQ,
            ).primitive()[1]
            r12 = sp.Poly(
                sp.resultant(
                    reduced[0].as_expr(), reduced[1].as_expr(), w
                ),
                d, domain=sp.QQ,
            ).primitive()[1]
            projection = sp.gcd(r13, r12).primitive()[1]
            print(
                f"template={args.template} xi=other "
                f"resultant_degrees=({r13.degree()},{r12.degree()}) "
                f"projection={sp.factor(projection.as_expr())}",
                flush=True,
            )
            if args.fibers:
                for factor, _ in sp.factor_list(projection.as_expr())[1]:
                    label, fiber = residue_gcd(reduced, d, w, factor)
                    print(
                        f"template={args.template} xi=other "
                        f"fiber={label} w_gcd_degree={fiber.degree()} "
                        f"w_gcd={fiber.as_expr()}",
                        flush=True,
                    )
        if args.modular_saturate:
            inverse = sp.symbols("inverse")
            forbidden = (
                d * (d - 1) * (d + 1) * (d + 2)
                * (w - 1) * (w + 1)
            )
            saturated = sp.groebner(
                [
                    *(value.as_expr() for value in reduced),
                    inverse * forbidden - 1,
                ],
                inverse, w, d,
                order="lex", modulus=CHARACTERISTIC,
            )
            unit = (
                len(saturated.polys) == 1
                and saturated.polys[0].as_expr() == 1
            )
            print(
                f"template={args.template} xi=other "
                f"modular_forbidden_saturation_unit={unit}",
                flush=True,
            )
            if not unit:
                raise RuntimeError("modular survivor: other")


if __name__ == "__main__":
    main()
