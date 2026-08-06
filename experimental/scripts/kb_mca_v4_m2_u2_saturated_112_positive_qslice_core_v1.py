#!/usr/bin/env python3
"""Exact raw ideals for the aligned positive q-slice.

The endpoint roots occur only through ``p=cd`` and ``t=-(c+d)``.  The
fraction-free reconstructed U vector differs from the V normalization by a
known rational scalar ``L/D``.  A new variable ``lambda_scale`` and the
equation ``D*lambda_scale-L=0`` retain that normalization without expanding
large common factors.

Each emitted ideal is exact but unresolved.  It consists of four equations
for one residual-factor allocation and the normalization equation; it is not
an aligned-positive deletion certificate.

Proof status: AUDIT helper, not a standalone deletion theorem.
Reproducibility: deterministic exact SymPy arithmetic; no random seed.
JSON certificate: owned by the saturated-112 q-slice packet verifier.
"""

import argparse

import sympy as sp


def reduce_pair(left, right, p, t):
    """Multiply linear representatives modulo T^2+tT+p."""
    a0, a1 = left
    b0, b1 = right
    return (
        sp.expand(a0 * b0 - p * a1 * b1),
        sp.expand(a0 * b1 + a1 * b0 - t * a1 * b1),
    )


def add_pair(left, right):
    return tuple(sp.expand(a + b) for a, b in zip(left, right))


def scale_pair(scalar, pair):
    return tuple(sp.expand(scalar * value) for value in pair)


def reconstruct_fraction_free(template):
    """Return a primitive U vector and its exact scale relative to V."""
    p, t, b, w = sp.symbols("p t b w", nonzero=True)
    alpha = p + 2 * t + 4
    beta = 1 + 2 * t + 4 * p
    z_numerator = w * beta - alpha
    z_denominator = beta - w * alpha

    f = p - w
    g = 1 - w * p
    m = t * (1 - w)
    l1 = sp.expand(g * z_denominator + f * z_numerator)
    l0 = sp.expand(m * (z_denominator + z_numerator) + 2 * l1)

    if template == "fixed-moving":
        target0 = 2 * (1 + 2 * b) * l0 + 4 * b * l1
        target1 = -(2 * b + 9) * l0 - 2 * (1 + 3 * b) * l1
        target2 = 4 * l0 + (2 * b + 1) * l1
    else:
        target0 = 2 * (b**2 + 1) * l0 + 4 * b * l1
        target1 = -(b**2 + 4 * b + 1) * l0 - 2 * (b**2 + b + 1) * l1
        target2 = 2 * b * l0 + (b**2 + 1) * l1
    target0, target1, target2 = map(sp.expand, (target0, target1, target2))

    d2 = z_denominator**2
    nd = z_numerator * z_denominator
    n2 = z_numerator**2
    e = 1 - p * w**2
    h = w * (1 - p)
    j = w**2 - p
    rhs0 = target0 * d2
    rhs2 = target2 * d2

    determinant = sp.expand(
        (d2 - n2) * (nd * (j + e) - h * (d2 + n2))
    )
    x0 = sp.expand(rhs0 * (nd * j - d2 * h)
                   + rhs2 * (n2 * h - nd * j))
    x1 = sp.expand(rhs2 * (d2 * j - n2 * e)
                   - rhs0 * (n2 * j - d2 * e))
    x2 = sp.expand(rhs2 * (nd * e - d2 * h)
                   + rhs0 * (n2 * h - nd * e))

    u2_at_w = sp.expand(x2 + w * x1 + w**2 * x0)
    middle_rhs0 = target1 * d2 * determinant
    middle_rhs1 = t * u2_at_w
    middle_determinant = sp.expand(
        w * (d2 + n2) - nd * (1 + w**2)
    )
    x3 = sp.expand(w * middle_rhs0 - nd * middle_rhs1)
    x4 = sp.expand((d2 + n2) * middle_rhs1
                   - (1 + w**2) * middle_rhs0)
    x0, x1, x2 = (sp.expand(middle_determinant * value)
                  for value in (x0, x1, x2))

    common = ((p - 1) * (w - 1)**4 * (w + 1)**4
              * alpha * beta * z_denominator**2)
    if template == "fixed-moving":
        common *= 5 * p + 4 * t + 5
    ring_variables = (b, w, p, t)
    common_poly = sp.Poly(common, *ring_variables)
    primitive = tuple(
        sp.Poly(value, *ring_variables).exquo(common_poly).as_expr()
        for value in (x0, x1, x2, x3, x4)
    )

    edge_scale = (2 * b - 1 if template == "fixed-moving"
                  else -(b - 1) * (b + 1))
    relative_scale = sp.cancel(
        edge_scale * z_denominator * determinant * middle_determinant / common
    )
    scale_numerator, scale_denominator = map(
        sp.expand, sp.fraction(relative_scale)
    )
    return ((p, t, b, w), (f, g, m), primitive,
            (z_numerator, z_denominator),
            (scale_numerator, scale_denominator))


def audit_reconstruction(template, variables, coefficients, relative_scale):
    """Compare U and its relative scale with an independent exact solve."""
    p, t, b, w = variables
    a = sp.Rational(2)
    c, d, b_value, w_value = map(sp.Rational, (3, 7, 5, 11))
    substitutions = {
        p: c * d,
        t: -(c + d),
        b: b_value,
        w: w_value,
    }
    f = c * d - w_value
    g = 1 - w_value * c * d
    m = -(c + d) * (1 - w_value)
    z = sp.cancel(-(f + m * a + g * a**2)
                  / (g + m * a + f * a**2))
    v_at_z = sp.Matrix([f + g * z, m * (1 + z), g + f * z])
    l1 = v_at_z[2]
    l0 = v_at_z[1] + a * l1

    def edge(left, right):
        return sp.Matrix([left * right, -(left + right), 1])

    if template == "fixed-moving":
        first, second = edge(a, 1 / a), edge(a, b_value)
        r, s = 1 / a, b_value
    else:
        first, second = edge(a, b_value), edge(a, 1 / b_value)
        r, s = b_value, 1 / b_value
    target = ((l0 + s * l1) * first + (l0 + r * l1) * second) / (s - r)

    def evaluation(point):
        return (
            sp.Matrix([1, point, point**2, 0, 0]).T,
            sp.Matrix([0, 0, 0, 1 + point**2, point]).T,
            sp.Matrix([point**2, point, 1, 0, 0]).T,
        )

    at_w = evaluation(w_value)
    at_z = evaluation(z)
    matrix = sp.Matrix.vstack(
        at_w[0] - c * d * at_w[2],
        at_w[1] + (c + d) * at_w[2],
        *at_z,
    )
    direct = matrix.inv(method="DM") * sp.Matrix([0, 0, *target])
    generated = sp.Matrix([
        value.subs(substitutions) for value in coefficients
    ])
    pivot = next(index for index, value in enumerate(direct) if value != 0)
    ratio = sp.cancel(generated[pivot] / direct[pivot])
    expected_ratio = sp.cancel(
        relative_scale[0].subs(substitutions)
        / relative_scale[1].subs(substitutions)
    )
    if ratio != expected_ratio or generated[pivot] == 0 or any(
        sp.expand(generated[index] * direct[pivot]
                  - generated[pivot] * direct[index]) != 0
        for index in range(5)
    ):
        raise RuntimeError(f"{template} fraction-free reconstruction mismatch")

    # Independently divide the endpoint norms and compare their three
    # residual coefficients with the compact quadratic-pair formulas.
    x0, x1, x2, x3, x4 = generated
    scaled_f, scaled_g, scaled_m = (ratio * value for value in (f, g, m))
    leading = (x2 - c * d * x0, x3 + (c + d) * x0)
    constant = (x0 - c * d * x2, x3 + (c + d) * x2)
    gamma = (scaled_g - c * d * scaled_f,
             scaled_m + (c + d) * scaled_f)
    leading_square = scale_pair(
        w_value**2, reduce_pair(leading, leading, c * d, -(c + d))
    )
    constant_square = reduce_pair(constant, constant, c * d, -(c + d))
    leading_constant = reduce_pair(leading, constant, c * d, -(c + d))
    gamma_square = reduce_pair(gamma, gamma, c * d, -(c + d))
    middle = add_pair(scale_pair(-2 * w_value, leading_constant),
                      scale_pair(-w_value**2, gamma_square))
    W = sp.Symbol("W")
    for root in (c, d):
        u_at_root = (
            x0 + root * x3 + root**2 * x2
            + (x1 + root * x4 + root**2 * x1) * W
            + (x2 + root * x3 + root**2 * x0) * W**2
        )
        v_at_root = (
            scaled_f + root * scaled_m + root**2 * scaled_g
            + (scaled_g + root * scaled_m + root**2 * scaled_f) * W
        )
        norm = sp.Poly(sp.expand(u_at_root**2 - W * v_at_root**2), W)
        residual, remainder = norm.div(sp.Poly((W - w_value)**2, W))
        predicted = [
            pair[0] + root * pair[1]
            for pair in (leading_square, middle, constant_square)
        ]
        observed = [w_value**2 * residual.nth(index) for index in (2, 1, 0)]
        if not remainder.is_zero or any(
            sp.expand(left - right) != 0
            for left, right in zip(predicted, observed)
        ):
            raise RuntimeError(f"{template} residual normalization mismatch")


def allocation_pairs(allocation, p, t, leading_square, middle,
                     constant_square):
    """Route two residual quadratics to one of the three UFD allocations."""
    root = (sp.Integer(0), sp.Integer(1))
    root_square = (-p, -t)
    if allocation == "same":
        first = add_pair(reduce_pair(root, middle, p, t),
                         scale_pair(2, leading_square))
        second = add_pair(reduce_pair(root_square, constant_square, p, t),
                          scale_pair(-1, leading_square))
    elif allocation == "swap":
        first = add_pair(scale_pair(p, middle),
                         scale_pair(2, reduce_pair(root, leading_square, p, t)))
        second = add_pair(scale_pair(p**2, constant_square),
                          scale_pair(-1, reduce_pair(
                              root_square, leading_square, p, t)))
    else:
        first = add_pair(scale_pair(p, middle),
                         scale_pair(-t, leading_square))
        second = add_pair(scale_pair(p, constant_square),
                          scale_pair(-1, leading_square))
    return (*first, *second)


def make_polynomials(expressions, variables, allocation, ramified):
    p, t, b, w, scale = variables
    ring_variables = (b, w, scale, p, t)
    equations = [sp.Poly(value, *ring_variables) for value in expressions]
    shapes = [
        (item.total_degree(), item.degree(b), item.degree(w),
         item.degree(scale), len(item.terms()))
        for item in equations
    ]
    print(
        f"allocation={allocation} ramified={ramified} "
        f"equation_shapes={shapes}",
        flush=True,
    )
    return equations


def allocation_equations(allocation, variables, odd, coefficients,
                         relative_scale):
    """Build one exact unramified five-equation ideal."""
    p, t, _, w, scale = variables
    f, g, m = odd
    x0, _, x2, x3, _ = coefficients
    leading = (sp.expand(x2 - p * x0), sp.expand(x3 - t * x0))
    constant = (sp.expand(x0 - p * x2), sp.expand(x3 - t * x2))
    gamma = scale_pair(
        scale, (sp.expand(g - p * f), sp.expand(m - t * f))
    )
    leading_square = scale_pair(w**2, reduce_pair(leading, leading, p, t))
    constant_square = reduce_pair(constant, constant, p, t)
    leading_constant = reduce_pair(leading, constant, p, t)
    gamma_square = reduce_pair(gamma, gamma, p, t)
    middle = add_pair(scale_pair(-2 * w, leading_constant),
                      scale_pair(-w**2, gamma_square))
    scale_numerator, scale_denominator = relative_scale
    normalization = sp.expand(scale_denominator * scale - scale_numerator)
    expressions = allocation_pairs(
        allocation, p, t, leading_square, middle, constant_square
    )
    return make_polynomials(
        (*expressions, normalization), variables, allocation, False
    )


def ramified_allocation_equations(allocation, variables, coefficients,
                                  relative_scale):
    """Build one exact repaired w=0 five-equation ideal."""
    p, t, b, w, scale = variables
    specialized = [sp.Poly(value.subs(w, 0), b, p, t, domain=sp.QQ)
                   for value in coefficients]
    coefficient_content = specialized[0]
    for value in specialized[1:]:
        coefficient_content = sp.gcd(coefficient_content, value)
    x0, x1, x2, x3, x4 = [value.as_expr() for value in specialized]
    print(
        f"ramified_coefficient_content="
        f"{sp.factor(coefficient_content.as_expr())}",
        flush=True,
    )

    leading = (sp.expand(x2 - p * x0), sp.expand(x3 - t * x0))
    linear = (sp.expand((1 - p) * x1), sp.expand(x4 - t * x1))
    gamma = scale_pair(scale, (1 - p**2, t * (1 - p)))
    leading_square = reduce_pair(leading, leading, p, t)
    constant_square = reduce_pair(linear, linear, p, t)
    leading_linear = reduce_pair(leading, linear, p, t)
    gamma_square = reduce_pair(gamma, gamma, p, t)
    middle = add_pair(scale_pair(2, leading_linear),
                      scale_pair(-1, gamma_square))
    scale_numerator, scale_denominator = (
        sp.expand(value.subs(w, 0)) for value in relative_scale
    )
    normalization = sp.expand(scale_denominator * scale - scale_numerator)
    expressions = allocation_pairs(
        allocation, p, t, leading_square, middle, constant_square
    )
    return make_polynomials(
        (*expressions, normalization), variables, allocation, True
    )


def run(template, allocation, ramified):
    (base_variables, odd, coefficients, (z_numerator, z_denominator),
     relative_scale) = reconstruct_fraction_free(template)
    p, t, b, w = base_variables
    scale = sp.Symbol("lambda_scale", nonzero=True)
    variables = (p, t, b, w, scale)
    audit_reconstruction(template, base_variables, coefficients, relative_scale)
    print(f"template={template} fraction_free_reconstruction=PASS", flush=True)
    print(f"z_numerator={sp.factor(z_numerator)}", flush=True)
    print(f"z_denominator={sp.factor(z_denominator)}", flush=True)
    allocations = (("same", "swap", "mixed")
                   if allocation == "all" else (allocation,))
    for name in allocations:
        if ramified:
            ramified_allocation_equations(
                name, variables, coefficients, relative_scale
            )
        else:
            allocation_equations(
                name, variables, odd, coefficients, relative_scale
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("template", choices=("fixed-moving", "moving-moving"))
    parser.add_argument(
        "--allocation", required=True,
        choices=("same", "swap", "mixed", "all")
    )
    parser.add_argument("--ramified", action="store_true")
    args = parser.parse_args()
    run(args.template, args.allocation, args.ramified)


if __name__ == "__main__":
    main()
