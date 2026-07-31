#!/usr/bin/env sage
"""Exact replay of the near-aligned negative (1,1,2) q-slice deletion.

The computation is over QQ(b,c,d).  It reconstructs the negative source
form on each of the three rank-drop loci retained by the parent packet,
proves that all three give the same monic residual quartic, and verifies
the factor identity which forces a forbidden label collision.
"""

import hashlib
import json

B = PolynomialRing(QQ, names=("b", "c", "d"))
b0, c0, d0 = B.gens()
K = B.fraction_field()
b, c, d = map(K, (b0, c0, d0))
W_ring = PolynomialRing(K, "W")
W = W_ring.gen()
a = K(2)
w = 1 / c


def edge(left, right):
    return vector(K, (left * right, -(left + right), 1))


def evaluation(point):
    return matrix(
        K,
        (
            (1, point, point**2, 0),
            (0, 0, 0, 1 - point**2),
            (-point**2, -point, -1, 0),
        ),
    )


def reconstruct(template):
    q0, q1 = c * d, -(c + d)
    f = q0 + w
    g = -1 - w * q0
    m = q1 * (1 + w)
    z = -(f + m * a - g * a**2) / (g - m * a - f * a**2)
    v_at_z = vector(K, (f + g * z, m * (1 - z), -(g + f * z)))
    linear_1 = v_at_z[2]
    linear_0 = v_at_z[1] + a * v_at_z[2]
    assert v_at_z[0] + a * linear_0 == 0

    if template == "fixed-moving":
        first, second = edge(a, 1 / a), edge(a, b)
        right, left = 1 / a, b
    elif template == "moving-moving":
        first, second = edge(a, b), edge(a, 1 / b)
        right, left = b, 1 / b
    else:
        raise ValueError(template)
    target = (
        (linear_0 + left * linear_1) * first
        + (linear_0 + right * linear_1) * second
    ) / (left - right)

    at_w, at_z = evaluation(w), evaluation(z)
    matrix_full = matrix(
        K,
        (
            at_w[0] - q0 * at_w[2],
            at_w[1] - q1 * at_w[2],
            *at_z.rows(),
        ),
    )
    rhs_full = vector(K, (0, 0, *target))
    solution = matrix_full.matrix_from_rows(range(4)).solve_right(rhs_full[:4])
    consistency = (matrix_full * solution - rhs_full)[4]
    x0, x1, x2, x3 = solution
    u = vector(
        W_ring,
        (
            x0 + x1 * W + x2 * W**2,
            x3 * (1 - W**2),
            -x2 - x1 * W - x0 * W**2,
        ),
    )
    v = vector(
        W_ring,
        (
            f + g * W,
            m * (1 - W),
            -(g + f * W),
        ),
    )
    residuals = []
    for root in (c, d):
        u_root = sum(u[index] * root**index for index in range(3))
        v_root = sum(v[index] * root**index for index in range(3))
        quotient, remainder = (u_root**2 - W * v_root**2).quo_rem(
            (W - w) ** 2
        )
        assert remainder == 0
        residuals.append(quotient)
    return consistency, residuals[0] * residuals[1]


P = c * d - 2 * c - 2 * d + 1
Q = 2 * c * d - c - d + 2
loci = (
    ("fixed-moving:B", "fixed-moving", -Q / P),
    ("moving-moving:B", "moving-moving", -Q / P),
    ("moving-moving:C", "moving-moving", -P / Q),
)


def substitute_b(value, b_value):
    hom = B.hom([b_value, c, d], K)
    if isinstance(value, W_ring.element_class):
        return W_ring(
            [
                hom(coefficient.numerator()) / hom(coefficient.denominator())
                for coefficient in value
            ]
        )
    return hom(value.numerator()) / hom(value.denominator())


monic_residuals = []
leading_coefficients = []
consistency_hashes = {}
for name, template, b_value in loci:
    consistency, residual = reconstruct(template)
    consistency_value = substitute_b(consistency, b_value)
    assert consistency_value == 0
    consistency_hashes[name] = hashlib.sha256(
        str(consistency_value).encode()
    ).hexdigest()
    residual_value = substitute_b(residual, b_value)
    assert residual_value.degree() == 4
    leading_coefficients.append(residual_value[4])
    monic_residuals.append(residual_value / residual_value[4])

assert monic_residuals[0] == monic_residuals[1] == monic_residuals[2]
R = monic_residuals[0]

Lambda = 4 * c**2 * d - 2 * c**2 - c * d - c - 2 * d + 4
A = 5 * c * d - 4 * c - 4 * d + 5
E = (
    c * d * w
    + 4 * c * d
    - 2 * c * w
    - 2 * c
    - 2 * d * w
    - 2 * d
    + 4 * w
    + 1
)
assert Lambda == c * E
expected_leading = (
    (c - 1) ** 2
    * (d - 1) ** 2
    * (d + 1) ** 2
    * (c * d - 1) ** 4
    * Lambda**4
    / ((c + 1) ** 2 * A**4)
)
assert all(value == expected_leading for value in leading_coefficients)

# Certify the chosen rows (0,1,2,3): their only non-parent factor is c+d.
q0_default, q1_default = c * d, -(c + d)
f_default = q0_default + w
g_default = -1 - w * q0_default
m_default = q1_default * (1 + w)
z_default = -(
    f_default + m_default * a - g_default * a**2
) / (
    g_default - m_default * a - f_default * a**2
)
at_w_default, at_z_default = evaluation(w), evaluation(z_default)
matrix_default = matrix(
    K,
    (
        at_w_default[0] - q0_default * at_w_default[2],
        at_w_default[1] - q1_default * at_w_default[2],
        *at_z_default.rows(),
    ),
)
default_minor = matrix_default.matrix_from_rows((0, 1, 2, 3)).det()
expected_default_minor = (
    3
    * (d - 2)
    * (2 * d - 1)
    * (c - 2)
    * (c + d)
    * (2 * c - 1)
    * (c - 1) ** 4
    * (c + 1) ** 4
    * (c * d - 1)
    * A
    / (c**4 * Lambda**4)
)
assert default_minor == expected_default_minor

# The default 4x4 solver minor has one removable c+d factor.  On d=-c,
# rows (0,1,2,4) give this nonzero admissible-chart minor instead.
d_alt = -c
q0_alt, q1_alt = c * d_alt, -(c + d_alt)
f_alt = q0_alt + w
g_alt = -1 - w * q0_alt
m_alt = q1_alt * (1 + w)
z_alt = -(
    f_alt + m_alt * a - g_alt * a**2
) / (
    g_alt - m_alt * a - f_alt * a**2
)
at_w_alt, at_z_alt = evaluation(w), evaluation(z_alt)
matrix_alt = matrix(
    K,
    (
        at_w_alt[0] - q0_alt * at_w_alt[2],
        at_w_alt[1] - q1_alt * at_w_alt[2],
        *at_z_alt.rows(),
    ),
)
alternate_minor = matrix_alt.matrix_from_rows((0, 1, 2, 4)).det()
expected_alternate_minor = (
    15
    * (c - 2)
    * (c - 1) ** 2
    * (c + 1) ** 6
    * (c + 2)
    * (2 * c - 1)
    * (2 * c + 1)
    * (c**2 + 1)
    / (c**4 * (4 * c**2 + 5 * c + 4) ** 4)
)
assert alternate_minor == expected_alternate_minor
hom_d_alt = B.hom([b, c, -c], K)
lambda_alt = hom_d_alt(Lambda.numerator()) / hom_d_alt(Lambda.denominator())
assert lambda_alt == -(c - 1) * (4 * c**2 + 5 * c + 4)

Phi = (
    16 * c**4 * d**4
    - 9 * c**4 * d**3
    - 8 * c**3 * d**4
    + 28 * c**4 * d**2
    - 30 * c**3 * d**3
    - 15 * c**2 * d**4
    - 24 * c**4 * d
    - 14 * c**3 * d**2
    + 51 * c**2 * d**3
    + 4 * c * d**4
    + 4 * c**4
    + 12 * c**3 * d
    - 30 * c**2 * d**2
    + 12 * c * d**3
    + 4 * d**4
    + 4 * c**3
    + 51 * c**2 * d
    - 14 * c * d**2
    - 24 * d**3
    - 15 * c**2
    - 30 * c * d
    + 28 * d**2
    - 8 * c
    - 9 * d
    + 16
)
Psi = (
    16 * c**4 * d**4
    - 23 * c**4 * d**3
    - 8 * c**3 * d**4
    + 12 * c**4 * d**2
    + 22 * c**3 * d**3
    - 15 * c**2 * d**4
    - 8 * c**4 * d
    + 6 * c**3 * d**2
    + 33 * c**2 * d**3
    + 4 * c * d**4
    + 4 * c**4
    - 20 * c**3 * d
    - 30 * c**2 * d**2
    - 20 * c * d**3
    + 4 * d**4
    + 4 * c**3
    + 33 * c**2 * d
    + 6 * c * d**2
    - 8 * d**3
    - 15 * c**2
    + 22 * c * d
    + 12 * d**2
    - 8 * c
    - 23 * d
    + 16
)

target = ((W - 1 / d) * (W - d)) ** 2
claimed_difference = (
    2 * Phi / (d * Lambda**2) * (W + W**3)
    - Phi * Psi / (d**2 * Lambda**4) * W**2
)
assert R - target == claimed_difference
assert R(1 / d) == Phi**2 / (d**4 * Lambda**4)


def polynomial_hash(value):
    numerator = B(value.numerator())
    return hashlib.sha256(str(numerator).encode()).hexdigest()


result = {
    "schema": "kb-mca-v4-m2-diagonal-112-near-negative-qslice-sage-v1",
    "loci": [name for name, _, _ in loci],
    "consistency_zero": True,
    "common_monic_residual": True,
    "lambda_is_c_times_parent_E": True,
    "leading_coefficient_identity": True,
    "default_minor_factorization": True,
    "removable_minor_coverage": True,
    "lambda_sha256": polynomial_hash(Lambda),
    "phi_sha256": polynomial_hash(Phi),
    "psi_sha256": polynomial_hash(Psi),
    "evaluation_identity": "R(1/d)=Phi^2/(d^4*Lambda^4)",
    "difference_identity": True,
    "terminal": "DELETED_BY_FORBIDDEN_XI_TAU_ELL_COLLISION",
}
encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
result["payload_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
print(json.dumps(result, sort_keys=True))
