#!/usr/bin/env python3
"""Exact aligned q-slice replay on a genuine negative factor locus.

The endpoint is normalized to 2.  On B=0, solve b rationally in c,d and
reconstruct the negative source form from three target/forced equations.
The remaining forced equation and the q-slice coefficient mismatches are
then exact rational identities in c,d,w.  Keep every stage bounded and emit
progress before potentially expensive polynomial normalization.

Proof status: AUDIT helper for a pinned PROVED packet.
Reproducibility: deterministic exact SymPy arithmetic; no random seed.
JSON certificate: owned by the saturated-112 q-slice packet verifier.
"""

import argparse

import sympy as sp


def edge(left, right):
    return sp.Matrix([left * right, -(left + right), 1])


def reconstruct(template):
    c, d, w, W = sp.symbols("c d w W", nonzero=True)
    a = sp.Rational(2)
    p = c * d - 2 * c - 2 * d + 1
    q = 2 * c * d - c - d + 2
    b = sp.cancel(-q / p)  # B=0

    q0, q1 = c * d, -(c + d)
    f = q0 + w
    g = -1 - w * q0
    m = q1 * (1 + w)
    v = sp.Matrix([f + g * W, m * (1 - W), -(g + f * W)])
    numerator = f + m * a - g * a**2
    denominator = g - m * a - f * a**2
    z = sp.cancel(-numerator / denominator)
    vz = v.subs(W, z)
    l1 = vz[2]
    l0 = vz[1] + a * l1

    if template == "fixed-moving":
        first, second = edge(a, 1 / a), edge(a, b)
        r, s = 1 / a, b
    else:
        first, second = edge(a, b), edge(a, 1 / b)
        r, s = b, 1 / b
    target = sp.Matrix([
        sp.cancel(value)
        for value in (((l0 + s * l1) * first
                       + (l0 + r * l1) * second) / (s - r))
    ])

    # U_0(z)=target_0, U_2(z)=target_2, and the first forced-q row
    # determine x_0,x_1,x_2.  The middle target determines x_3.
    matrix = sp.Matrix([
        [1, z, z**2],
        [-z**2, -z, -1],
        [1 + q0 * w**2, w * (1 + q0), w**2 + q0],
    ])
    rhs = sp.Matrix([target[0], target[2], 0])
    determinant = sp.factor(matrix.det())
    numerators = [matrix.copy() for _ in range(3)]
    for column in range(3):
        numerators[column][:, column] = rhs
    x0, x1, x2 = [sp.cancel(item.det() / determinant)
                  for item in numerators]
    x3 = sp.cancel(target[1] / (1 - z**2))

    u = sp.Matrix([
        x0 + x1 * W + x2 * W**2,
        x3 * (1 - W**2),
        -(x2 + x1 * W + x0 * W**2),
    ])
    forced_residual = sp.factor(sp.together(
        u[1].subs(W, w) - q1 * u[2].subs(W, w)
    ))
    return (c, d, w, W), z, u, v, forced_residual


def qslice(template, eliminate):
    (c, d, w, W), z, u, v, forced_residual = reconstruct(template)
    if forced_residual != 0:
        raise RuntimeError(f"remaining forced row failed: {forced_residual}")
    print(f"template={template} forced_row=PASS", flush=True)

    field = sp.QQ.frac_field(c, d, w)
    u_root = sum(u[index] * c**index for index in range(3))
    v_root = sum(v[index] * c**index for index in range(3))
    u_poly = sp.Poly(u_root, W, domain=field)
    v_poly = sp.Poly(v_root, W, domain=field)
    norm = u_poly**2 - sp.Poly(W, W, domain=field) * v_poly**2
    residual, remainder = norm.div(sp.Poly((W - w)**2, W, domain=field))
    if not remainder.is_zero:
        raise RuntimeError("forced square division failed at c")
    if residual.degree() != 2:
        raise RuntimeError("unexpected residual degree at c")
    print(f"template={template} root=c residual_degree=2", flush=True)

    # Every input expression is symmetric in c,d.  Reuse the first quotient
    # under the simultaneous swap instead of repeating the expansion at d.
    swap = {c: d, d: c}
    conjugate = sp.Poly.from_list(
        [coefficient.xreplace(swap) for coefficient in residual.all_coeffs()],
        gens=W,
        domain=field,
    )
    observed = (residual * conjugate).monic()
    expected = sp.Poly(
        (W - 1 / c)**2 * (W - 1 / d)**2,
        W,
        domain=field,
    ).monic()
    differences = observed - expected
    constant = sp.factor(differences.nth(0))
    expected_constant = (c * d - 1) * (c * d + 1) / (c**2 * d**2)
    if sp.cancel(constant - expected_constant) != 0:
        raise RuntimeError(f"constant mismatch changed: {constant}")
    print(f"template={template} constant_mismatch={constant}", flush=True)

    # Admissibility gives cd!=1, so passage forces cd=-1.  Factor the
    # remaining coefficient mismatches on that exact specialization.
    specialized = {}
    for degree in range(1, 4):
        value = sp.cancel(differences.nth(degree).subs(d, -1 / c))
        numerator, denominator = sp.fraction(value)
        specialized[degree] = sp.Poly(numerator, w, domain=sp.QQ.frac_field(c))
        print(
            f"template={template} cd_minus_one_W_degree={degree} "
            f"w_degree={specialized[degree].degree()}",
            flush=True,
        )
    outer_coefficient_difference = sp.factor(
        (differences.nth(1) - differences.nth(3)).subs(d, -1 / c)
    )
    expected_outer_difference = 4 * (c**2 - 1) / c
    if sp.cancel(outer_coefficient_difference - expected_outer_difference) != 0:
        raise RuntimeError(
            f"outer coefficient difference changed: {outer_coefficient_difference}"
        )
    print(
        f"template={template} cd_minus_one_m1_minus_m3="
        f"{outer_coefficient_difference}",
        flush=True,
    )
    if not eliminate:
        return

    print(f"template={template} elimination=START", flush=True)
    outer_sum = sp.factor(
        specialized[1].as_expr() + specialized[3].as_expr()
    )
    outer_difference = sp.factor(
        specialized[1].as_expr() - specialized[3].as_expr()
    )
    print(f"template={template} outer_sum={outer_sum}", flush=True)
    print(
        f"template={template} outer_difference={outer_difference}",
        flush=True,
    )
    r13 = sp.Poly(
        sp.resultant(specialized[1].as_expr(), specialized[3].as_expr(), w),
        c,
        domain=sp.QQ,
    )
    print(
        f"template={template} resultant_13={sp.factor(r13.as_expr())}",
        flush=True,
    )
    r12 = sp.Poly(
        sp.resultant(specialized[1].as_expr(), specialized[2].as_expr(), w),
        c,
        domain=sp.QQ,
    )
    common = sp.gcd(r13, r12)
    print(
        f"template={template} resultant_12_degree={r12.degree()} "
        f"resultant_gcd={sp.factor(common.as_expr())}",
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("template", choices=("fixed-moving", "moving-moving"))
    parser.add_argument("--eliminate", action="store_true")
    args = parser.parse_args()
    qslice(args.template, args.eliminate)


if __name__ == "__main__":
    main()
