#!/usr/bin/env sage
"""Exact replay of the moving--moving aligned-positive balanced deletion.

The script starts from the five-row source reconstruction over QQ.  It
derives the four projective q-slice equations for the balanced root pattern,
descends them to

    y=b+b^-1,  s=c+d,  p=cd,

and independently reconstructs the two necessary full-quotient parity
constraints.  The complete first-match partition is then checked over the
deployed characteristic GF(2130706433).  Every localization is by the
displayed product of named parent/selector factors; no generic saturation is
used.

This proves only the canonical moving--moving assignment
({2,b},{2,1/b}) with aligned-positive balanced (1,1) target empty.  No
covariance to the other three moving--moving assignments is used or claimed.
It is not a K3 or KoalaBear-row closure.
"""

import hashlib
import json

P0 = ZZ(2130706433)
FF = GF(P0)


def sha(value):
    return hashlib.sha256(str(value).encode()).hexdigest()


def metric(value):
    value = value.parent()(value)
    return {
        "degree": int(value.total_degree()),
        "degrees": [int(value.degree(g)) for g in value.parent().gens()],
        "terms": int(len(value.monomials())),
        "sha256": sha(value),
    }


def primitive_in(ring, value):
    value = ring(value)
    if not value:
        return value
    value = ring(value / value.content())
    return -value if value.leading_coefficient() < 0 else value


# ---------------------------------------------------------------------------
# 1. Rebuild the representative moving--moving source reconstruction.
# ---------------------------------------------------------------------------

R = PolynomialRing(QQ, names=("b", "c", "d", "w"), order="degrevlex")
b, c, d, w = R.gens()
K = R.fraction_field()
bK, cK, dK, wK = map(K, R.gens())
a = K(2)


def primitive_R(value):
    return primitive_in(R, value)


def primitive_numerator_R(value):
    return primitive_R(value.numerator())


def edge(left, right):
    return vector(K, (left * right, -(left + right), 1))


def evaluation(point):
    return matrix(
        K,
        (
            (1, point, point**2, 0, 0),
            (0, 0, 0, 1 + point**2, point),
            (point**2, point, 1, 0, 0),
        ),
    )


KW = PolynomialRing(K, "W")
W = KW.gen()
q0, q1 = cK * dK, -(cK + dK)
f, g, m = q0 - wK, 1 - wK * q0, q1 * (1 - wK)
v = vector(KW, (f + g * W, m * (1 + W), g + f * W))
va = v[0] + a * v[1] + a**2 * v[2]
z = -va[0] / va[1]
vz = vector(K, (entry(z) for entry in v))
assert vz[0] + a * vz[1] + a**2 * vz[2] == 0
linear_1 = vz[2]
linear_0 = vz[1] + a * vz[2]

# Representative unordered source-star pair ({2,b},{2,1/b}).
first, second = edge(a, bK), edge(a, 1 / bK)
right, left = bK, 1 / bK
target_internal = (
    (linear_0 + left * linear_1) * first
    + (linear_0 + right * linear_1) * second
) / (left - right)
at_w, at_z = evaluation(wK), evaluation(z)
coefficient_matrix = matrix(
    K,
    (
        at_w[0] - q0 * at_w[2],
        at_w[1] - q1 * at_w[2],
        *at_z.rows(),
    ),
)
source_A_R = 5 * c * d - 4 * c - 4 * d + 5
source_E_R = c * d * w - 4 * c * d - 2 * c * w - 2 * d * w + 2 * c + 2 * d + 4 * w - 1
source_D_R = 4 * c * d * w - c * d - 2 * c * w - 2 * d * w + 2 * c + 2 * d + w - 4
assert z == -K(source_D_R) / K(source_E_R)
determinant_fraction = K(coefficient_matrix.det())
expected_det_numerator = (
    (d - 2) ** 2
    * (2 * d - 1) ** 2
    * (c - 2) ** 2
    * (2 * c - 1) ** 2
    * (w - 1) ** 5
    * (w + 1) ** 5
    * source_A_R
    * (c * d - 1) ** 2
)
assert primitive_R(determinant_fraction.numerator()) == primitive_R(
    expected_det_numerator
)
assert primitive_R(determinant_fraction.denominator()) == source_E_R**6
x = coefficient_matrix.solve_right(vector(K, (0, 0, *target_internal)))
assert coefficient_matrix * x == vector(K, (0, 0, *target_internal))
u = vector(
    KW,
    (
        x[0] + x[1] * W + x[2] * W**2,
        x[3] * (1 + W**2) + x[4] * W,
        x[2] + x[1] * W + x[0] * W**2,
    ),
)


def residual_at(root):
    u_root = sum(u[index] * root**index for index in range(3))
    v_root = sum(v[index] * root**index for index in range(3))
    divisor = (W - wK) ** 2
    assert divisor.is_monic()
    quotient, remainder = (u_root**2 - W * v_root**2).quo_rem(divisor)
    assert remainder == 0
    return quotient


target_balanced = (W - 1 / cK) * (W - 1 / dK)
assert target_balanced[2] == 1


def projective_equations(observed):
    raw = (
        K(observed[0] - observed[2] * target_balanced[0]),
        K(observed[1] - observed[2] * target_balanced[1]),
    )
    equations = []
    audits = []
    for value in raw:
        cleared = R(value.numerator())
        denominator = R(value.denominator())
        equation = primitive_R(cleared)
        # One scalar is applied to the complete cleared coefficient vector.
        # In particular no coefficient is independently normalized.
        scalar = K(equation) / K(cleared)
        assert scalar.numerator().is_constant()
        assert scalar.denominator().is_constant()
        assert K(equation) == scalar * K(denominator) * value
        equations.append(equation)
        audits.append((denominator, QQ(scalar)))
    return tuple(equations), tuple(audits)


c_equations, c_clear_audit = projective_equations(residual_at(cK))
d_equations, d_clear_audit = projective_equations(residual_at(dK))
raw_equations = (*c_equations, *d_equations)
raw_clear_audit = (*c_clear_audit, *d_clear_audit)
expected_c_denominator = (
    c
    * d
    * (w - 1) ** 2
    * (w + 1) ** 2
    * (d - 2) ** 2
    * (2 * d - 1) ** 2
    * (b - 1) ** 2
    * (b + 1) ** 2
    * source_A_R**2
)
expected_d_denominator = (
    c
    * d
    * (w - 1) ** 2
    * (w + 1) ** 2
    * (c - 2) ** 2
    * (2 * c - 1) ** 2
    * (b - 1) ** 2
    * (b + 1) ** 2
    * source_A_R**2
)
assert [
    primitive_R(denominator) for denominator, _ in raw_clear_audit
] == [
    primitive_R(expected_c_denominator),
    primitive_R(expected_c_denominator),
    primitive_R(expected_d_denominator),
    primitive_R(expected_d_denominator),
]
assert [str(scalar) for _, scalar in raw_clear_audit] == [
    "1/79766443076872509863361",
    "-1/282429536481",
    "1/79766443076872509863361",
    "-1/282429536481",
]
expected_raw_hashes = [
    "8f73e1d4bdda3fc3262e042d35cb714d541f827978638a6ecaf630b5731b93f7",
    "984a41f0ac99fda8a192fd20d0ee7f8f14be2a43b52105ec44cc80eb58c16a8f",
    "42e8416d1c217567e1a67a1a38ddc9069043d72238e997cacc4dc0a3bbcd9be0",
    "dd1b7d639bbbfe61c56db298f970cf4a3f5020c71bc6c15fda146ced5c18ea5e",
]
assert [sha(value) for value in raw_equations] == expected_raw_hashes


def inverse_b(poly):
    degree = poly.degree(b)
    return primitive_R(poly(b=1 / b) * b**degree)


def essential_product(equation):
    factors = [
        primitive_R(factor) ** exponent
        for factor, exponent in equation.factor()
        if factor.degree(b) > 0
    ]
    return primitive_R(prod(factors, R(1)))


essential_products = [essential_product(eq) for eq in raw_equations]
expected_dropped = [
    (c * d - 1) * source_E_R**2,
    R(1),
    (c * d - 1) * source_E_R**2,
    R(1),
]
for equation, essential, dropped in zip(
    raw_equations, essential_products, expected_dropped
):
    # Dropping parent factors is one whole-polynomial factorization, never
    # an independent normalization of constant/linear coefficients.
    assert primitive_R(essential * dropped) == equation


# Descend reciprocal polynomials from b to y=b+b^-1.
C = PolynomialRing(QQ, names=("y", "c", "d", "w"), order="degrevlex")
yC, cC, dC, wC = C.gens()
KC = C.fraction_field()
PB = PolynomialRing(KC, "beta")
beta_var = PB.gen()
to_PB = R.hom([beta_var, cC, dC, wC], PB)


def palindromic_to_y(poly):
    poly = primitive_R(poly)
    degree = poly.degree(b)
    assert degree % 2 == 0 and inverse_b(poly) == poly
    half = degree // 2
    univariate = PB(to_PB(poly))
    coefficients = [C(univariate[index]) for index in range(degree + 1)]
    assert all(
        coefficients[index] == coefficients[degree - index]
        for index in range(degree + 1)
    )
    chebyshev = [C(2), yC]
    for index in range(2, half + 1):
        chebyshev.append(yC * chebyshev[-1] - chebyshev[-2])
    result = coefficients[half]
    for index in range(1, half + 1):
        result += coefficients[half + index] * chebyshev[index]
    return C(result)


y_forms = [palindromic_to_y(value) for value in essential_products]
assert [sha(value) for value in y_forms] == [
    "8e92cfbc760fd54f7fe706386dfbc7122a190bcf00d075239c705591068cf9b5",
    "3fc856f61bdf4f2b4d20d977c9617f1c1685731b9400b133ae530eead32e6bbe",
    "7595f1d1daacf440a97a5656a50c6924991c8276d8bec329d7e2f71b6bbe043f",
    "9bc77a19ce66548373ee4e3f2a8d35b3b8dcf8d52da1f30b36b3cbbc207059c4",
]

# Reduce both ordered roots through X^2-sX+p.  Paired c,d equations and
# c!=d are exactly equivalent to vanishing of the constant and X parts.
S = PolynomialRing(QQ, names=("y", "s", "p", "w"), order="degrevlex")
yS, sS, pS, wS = S.gens()
XS = PolynomialRing(S, "root")
root = XS.gen()
to_XS = C.hom([yS, root, sS - root, wS], XS)
root_relation = root**2 - sS * root + pS
assert root_relation.is_monic()
remainders = [to_XS(value).mod(root_relation) for value in y_forms]
swap_root = XS.hom([sS - root], XS)
assert swap_root(remainders[0]).mod(root_relation) == remainders[2]
assert swap_root(remainders[1]).mod(root_relation) == remainders[3]
A0, B0 = S(remainders[0][0]), S(remainders[0][1])
A1, B1 = S(remainders[1][0]), S(remainders[1][1])

expected_qslice_metrics = {
    "A0": {
        "degree": 10,
        "degrees": [2, 6, 6, 2],
        "terms": 211,
        "sha256": "80c87dadfe17314095dcac33916b12551010101861ea35231e7c3d19a48183fb",
    },
    "B0": {
        "degree": 9,
        "degrees": [2, 4, 5, 2],
        "terms": 134,
        "sha256": "e0d4d5529c2b8e3f00ea62d2aa99e57e14309ff162f8a5876b05d60fd663b8a8",
    },
    "A1": {
        "degree": 15,
        "degrees": [2, 9, 9, 4],
        "terms": 780,
        "sha256": "594b1e0cc8128e0189f9419ffe311d1d279a739e4238702faa92c5114f80a490",
    },
    "B1": {
        "degree": 14,
        "degrees": [2, 7, 8, 4],
        "terms": 581,
        "sha256": "1762587b9591de809265a7d517b3aa4ad7fc4a5663393a23d0277379e45a84ad",
    },
}
assert {
    name: metric(value)
    for name, value in (("A0", A0), ("B0", B0), ("A1", A1), ("B1", B1))
} == expected_qslice_metrics


# ---------------------------------------------------------------------------
# 1.1 Projective compactification control and forced-ramified first match.
# ---------------------------------------------------------------------------

def basis_sha256(basis):
    return hashlib.sha256("\n".join(map(str, basis)).encode()).hexdigest()


def nilpotence_records(ring, basis, localizer, maximum):
    records = []
    remainder = ring(1)
    for exponent in range(1, maximum + 1):
        remainder = (remainder * localizer).reduce(basis)
        records.append(
            {
                "exponent": exponent,
                "zero": bool(remainder == 0),
                "record": metric(remainder),
            }
        )
        if remainder == 0:
            break
    return records


# The canonical source assignment has b nonzero and hence finite affine
# y=b+b^-1.  The projective closure is nevertheless audited as a defensive
# control.  Since every q-slice equation has degree two in affine y, its value
# at [Y:Z]=[1:0] is exactly its y^2 coefficient.  Crucially w is not inverted.
# This control is not load-bearing and does not transport to other assignments.
RINF = PolynomialRing(FF, names=("s", "p", "w"), order="degrevlex")
sI, pI, wI = RINF.gens()


def leading_y_coefficient(value):
    value = S(value)
    assert value.degree(yS) == 2
    answer = RINF(0)
    for monomial, coefficient in value.dict().items():
        exponent_y, exponent_s, exponent_p, exponent_w = monomial
        if exponent_y == 2:
            answer += (
                FF(coefficient)
                * sI**exponent_s
                * pI**exponent_p
                * wI**exponent_w
            )
    return answer


yinf_generator_names = ("A0_y2", "B0_y2", "A1_y2", "B1_y2")
yinf_generators = [
    leading_y_coefficient(value) for value in (A0, B0, A1, B1)
]
expected_yinf_generator_metrics = {
    "A0_y2": {
        "degree": 8,
        "degrees": [4, 6, 2],
        "terms": 72,
        "sha256": "eaa8ecedd16472ef17d2650fa933ec4932ddc2c8c70b1eaf63fbfc889a487d2d",
    },
    "B0_y2": {
        "degree": 7,
        "degrees": [3, 5, 2],
        "terms": 44,
        "sha256": "57a370968b5e5da315ee12dbfb7179913eb7a9e61da62af67235de12fb0cd502",
    },
    "A1_y2": {
        "degree": 13,
        "degrees": [7, 9, 4],
        "terms": 252,
        "sha256": "f36fffc6bc4151ecf3603a04932130eae311d3499c835f6e50f8956ad1d76877",
    },
    "B1_y2": {
        "degree": 12,
        "degrees": [6, 8, 4],
        "terms": 182,
        "sha256": "eb9ff31d007f782587f59aa6c7dd21074b608cbc91fed83926e997c38a90a7a0",
    },
}
assert {
    name: metric(value)
    for name, value in zip(yinf_generator_names, yinf_generators)
} == expected_yinf_generator_metrics
yinf_basis = list(
    RINF.ideal(yinf_generators).groebner_basis(algorithm="singular:slimgb")
)
assert len(yinf_basis) == 23
assert RINF.ideal(yinf_basis).dimension() == 1
assert basis_sha256(yinf_basis) == (
    "988d28d187d8668c9a14bfef2368e195ec443fe8d98cc449752ce9399be07289"
)
yinf_localizer_factors = [
    ("nonzero_core", pI),
    ("distinct_core", sI**2 - 4 * pI),
    ("core_not_reciprocal", pI - 1),
    ("core_not_plus_one", 1 - sI + pI),
    ("core_not_minus_one", 1 + sI + pI),
    ("core_not_two", 4 - 2 * sI + pI),
    ("core_not_half", 1 - 2 * sI + 4 * pI),
    ("moving_not_fixed", wI**2 - 1),
    ("moving_not_core", wI**2 - sI * wI + pI),
    ("moving_inverse_not_core", 1 - sI * wI + pI * wI**2),
    ("reconstruction_A", 5 * pI - 4 * sI + 5),
    (
        "reconstruction_E",
        -2 * sI * wI
        + pI * wI
        + 2 * sI
        - 4 * pI
        + 4 * wI
        - 1,
    ),
]
H_yinf = prod((factor for _, factor in yinf_localizer_factors), RINF(1))
yinf_remainders = nilpotence_records(RINF, yinf_basis, H_yinf, 2)
assert yinf_remainders == [
    {
        "exponent": 1,
        "zero": False,
        "record": {
            "degree": 12,
            "degrees": [7, 11, 7],
            "terms": 214,
            "sha256": "62d9e0da9c13fb9c83cb9080463b1228a5da51c8045286be8fca7bf18fb51c0b",
        },
    },
    {
        "exponent": 2,
        "zero": True,
        "record": {
            "degree": -1,
            "degrees": [-1, -1, -1],
            "terms": 0,
            "sha256": "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9",
        },
    },
]
RINF_T = PolynomialRing(
    FF, names=("s", "p", "w", "t"), order="degrevlex"
)
sIT, pIT, wIT, tIT = RINF_T.gens()
to_RINF_T = RINF.hom([sIT, pIT, wIT], RINF_T)
yinf_rabinowitsch_basis = list(
    RINF_T.ideal(
        [to_RINF_T(value) for value in yinf_generators]
        + [tIT * to_RINF_T(H_yinf) - 1]
    ).groebner_basis(algorithm="singular:slimgb")
)
assert yinf_rabinowitsch_basis == [RINF_T(1)]


# The remaining affine-y locus splits next at w=0.  Parity is not used here:
# the four exact q-slice equations already make the valid-label localization
# empty.  Omitting factors that become constants or duplicates at w=0 makes
# this localizer weaker, hence the conclusion stronger.
RW0 = PolynomialRing(FF, names=("y", "s", "p"), order="degrevlex")
y0, s0, p0 = RW0.gens()


def specialize_w_zero(value):
    specialized = S(value).subs({wS: 0})
    answer = RW0(0)
    for monomial, coefficient in S(specialized).dict().items():
        exponent_y, exponent_s, exponent_p, exponent_w = monomial
        assert exponent_w == 0
        answer += (
            FF(coefficient)
            * y0**exponent_y
            * s0**exponent_s
            * p0**exponent_p
        )
    return answer


w0_generator_names = ("A0", "B0", "A1", "B1")
w0_generators = [
    specialize_w_zero(value) for value in (A0, B0, A1, B1)
]
expected_w0_generator_metrics = {
    "A0": {
        "degree": 8,
        "degrees": [2, 6, 6],
        "terms": 74,
        "sha256": "8defe2bf2497853b3fe0892acadba8cf4c78c5857ce62e649f0ebe6d65462dac",
    },
    "B0": {
        "degree": 7,
        "degrees": [2, 4, 5],
        "terms": 48,
        "sha256": "1efc4d5300563528c06cb80eb13a65e51d8373ad554bddcf6c073cba97e7448d",
    },
    "A1": {
        "degree": 11,
        "degrees": [2, 9, 9],
        "terms": 154,
        "sha256": "75aaa5b5a764b87e7c290515016089f912874c95f5b9a2f0a678be55abf394df",
    },
    "B1": {
        "degree": 10,
        "degrees": [2, 7, 8],
        "terms": 119,
        "sha256": "11cf57939097174326d3a31e5c4a19ea68328988ee01bf0b9fae4f13480bdd4e",
    },
}
assert {
    name: metric(value)
    for name, value in zip(w0_generator_names, w0_generators)
} == expected_w0_generator_metrics
w0_basis = list(
    RW0.ideal(w0_generators).groebner_basis(algorithm="singular:slimgb")
)
assert len(w0_basis) == 24
assert RW0.ideal(w0_basis).dimension() == 1
assert basis_sha256(w0_basis) == (
    "cc74d01fc4c41b8ace5c23f78a26ce4991450e7c0430eaa42dea0f8bf0042dd2"
)
w0_localizer_factors = [
    ("nonzero_core", p0),
    ("distinct_core", s0**2 - 4 * p0),
    ("core_not_reciprocal", p0 - 1),
    ("core_not_plus_one", 1 - s0 + p0),
    ("core_not_minus_one", 1 + s0 + p0),
    ("core_not_two", 4 - 2 * s0 + p0),
    ("core_not_half", 1 - 2 * s0 + 4 * p0),
    ("reconstruction_A", 5 * p0 - 4 * s0 + 5),
    ("reconstruction_E_at_w0", 2 * s0 - 4 * p0 - 1),
]
H_w0 = prod((factor for _, factor in w0_localizer_factors), RW0(1))
w0_remainders = nilpotence_records(RW0, w0_basis, H_w0, 3)
assert w0_remainders == [
    {
        "exponent": 1,
        "zero": False,
        "record": {
            "degree": 10,
            "degrees": [4, 8, 10],
            "terms": 151,
            "sha256": "0ab4b29eb2fbcc56b9fb6a88ff17dbd147545d5e90e601373db988776df405b1",
        },
    },
    {
        "exponent": 2,
        "zero": False,
        "record": {
            "degree": 20,
            "degrees": [4, 8, 20],
            "terms": 221,
            "sha256": "c2609c094eb529764bbbd9c110a4334d5129c92c6b331dcb9bff972b642cb418",
        },
    },
    {
        "exponent": 3,
        "zero": True,
        "record": {
            "degree": -1,
            "degrees": [-1, -1, -1],
            "terms": 0,
            "sha256": "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9",
        },
    },
]
RW0_T = PolynomialRing(
    FF, names=("y", "s", "p", "t"), order="degrevlex"
)
y0T, s0T, p0T, t0T = RW0_T.gens()
to_RW0_T = RW0.hom([y0T, s0T, p0T], RW0_T)
w0_rabinowitsch_basis = list(
    RW0_T.ideal(
        [to_RW0_T(value) for value in w0_generators]
        + [t0T * to_RW0_T(H_w0) - 1]
    ).groebner_basis(algorithm="singular:slimgb")
)
assert w0_rabinowitsch_basis == [RW0_T(1)]


def factor_by_hash(poly, target):
    matches = [
        S(factor)
        for factor, _ in S(poly).factor()
        if sha(S(factor)) == target
    ]
    assert len(matches) == 1
    return matches[0]


L2 = factor_by_hash(
    B0, "771d6d8f80f86a15adc308b063e2aae551943d22e190ea6cb180623fa041f81b"
)
F5 = factor_by_hash(
    B0, "f8313e4ce2a50bd863cbf7c938f84b12608733766d6a2a484fd572e169318d88"
)
F11 = factor_by_hash(
    B1, "d13f4d8b197a74b5c5a0d12a17a63cb14bd2954367dfed05a8d4b4e7b326c2cc"
)
set_y_zero = S.hom([S(0), sS, pS, wS], S)
set_y_one = S.hom([S(1), sS, pS, wS], S)
beta_QQ = S(set_y_zero(F5))
alpha_QQ = S(set_y_one(F5) - beta_QQ)
assert F5 == alpha_QQ * yS + beta_QQ
source_A_S = -4 * sS + 5 * pS + 5
assert B0 == -source_A_S * (wS - 1) * L2 * F5
assert B1 == -source_A_S * (wS - 1) * (pS - 1) * F11


# ---------------------------------------------------------------------------
# 2. Independently derive the exact symmetric parity constraints.
# ---------------------------------------------------------------------------

def build_parity_constraints():
    # Canonical b is finite and nonzero, so y is affine.  This chart is
    # reached only after the affine-y w=0 q-slice chart is deleted; thus w is
    # nonzero.  The y=infinity calculation above is only a non-load-bearing
    # compactification control.
    # The imported source interface also has A,E,D nonzero: A and E make
    # reconstruction regular, while z=-D/E and the internal source point
    # z being nonzero give D!=0.  These are precisely the divisions below.
    field = S.fraction_field()
    yF, sF, pF, wF = map(field, S.gens())
    two = field(2)

    def clear_fraction(value):
        value = field(value)
        cleared = S(value.numerator())
        denominator = S(value.denominator())
        equation = primitive_in(S, cleared)
        scalar = field(equation) / field(cleared)
        assert scalar.numerator().is_constant()
        assert scalar.denominator().is_constant()
        assert field(equation) == scalar * field(denominator) * value
        return equation, (denominator, QQ(scalar))

    def eval_matrix(point):
        return matrix(
            field,
            (
                (1, point, point**2, 0, 0),
                (0, 0, 0, 1 + point**2, point),
                (point**2, point, 1, 0, 0),
            ),
        )

    FW = PolynomialRing(field, "Wq")
    Wq = FW.gen()
    ff = pF - wF
    gg = 1 - wF * pF
    mm = -sF * (1 - wF)
    vv = vector(FW, (ff + gg * Wq, mm * (1 + Wq), gg + ff * Wq))
    v_two = vv[0] + two * vv[1] + two**2 * vv[2]
    zz = -v_two[0] / v_two[1]
    vz_local = vector(field, (entry(zz) for entry in vv))
    linear_one = vz_local[2]
    linear_zero = vz_local[1] + two * vz_local[2]

    # If delta=b-b^-1, delta times the original target is the negative of
    # this symmetric numerator.
    numerator_target = vector(
        field,
        (
            two * (yF * linear_zero + 2 * linear_one),
            -(
                (2 * two + yF) * linear_zero
                + (two * yF + 2) * linear_one
            ),
            2 * linear_zero + yF * linear_one,
        ),
    )
    scaled_target = -numerator_target
    at_w_local, at_z_local = eval_matrix(wF), eval_matrix(zz)
    matrix_local = matrix(
        field,
        (
            at_w_local[0] - pF * at_w_local[2],
            at_w_local[1] + sF * at_w_local[2],
            *at_z_local.rows(),
        ),
    )
    solution = matrix_local.solve_right(
        vector(field, (0, 0, *scaled_target))
    )
    ubar = vector(
        FW,
        (
            solution[0] + solution[1] * Wq + solution[2] * Wq**2,
            solution[3] * (1 + Wq**2) + solution[4] * Wq,
            solution[2] + solution[1] * Wq + solution[0] * Wq**2,
        ),
    )

    FL = PolynomialRing(field, "lam")
    lam = FL.gen()
    FLT = PolynomialRing(FL, "T")
    T = FLT.gen()

    def endpoint_poly(coefficients, source_index):
        return sum(
            FL(coefficients[index][source_index]) * T**index
            for index in range(3)
        )

    U0 = endpoint_poly(ubar, 0)
    V0 = endpoint_poly(vv, 0)
    H0 = U0 + lam * V0

    def pair_norm(trace, product):
        quadratic = T**2 - FL(trace) * T + FL(product)
        assert quadratic.is_monic()
        remainder = H0.mod(quadratic)
        const = remainder[0]
        coeff = remainder[1] if remainder.degree() == 1 else FL(0)
        return FL(
            const**2
            + const * coeff * FL(trace)
            + coeff**2 * FL(product)
        )

    def eval_T(poly, value):
        return FL(poly(T=FL(value)))

    parity_J_product = (
        eval_T(H0, two)
        * eval_T(H0, 1 / two)
        * pair_norm(yF, 1)
        * pair_norm(sF, pF)
    )
    parity_I_product = (
        pair_norm(sF / pF, 1 / pF)
        * eval_T(H0, wF)
        * eval_T(H0, 1 / wF)
        * eval_T(H0, zz)
        * eval_T(H0, 1 / zz)
    )
    parity_J, audit_J = clear_fraction(parity_J_product[1])
    parity_I, audit_I = clear_fraction(parity_I_product[1])
    return (parity_J, parity_I), (audit_J, audit_I)


(parity_J, parity_I), parity_clear_audit = build_parity_constraints()
D_S = -2 * sS * wS + 4 * pS * wS + 2 * sS - pS + wS - 4
E_S = -2 * sS * wS + pS * wS + 2 * sS - 4 * pS + 4 * wS - 1
core_not_two_S = -2 * sS + pS + 4
core_not_half_S = -2 * sS + 4 * pS + 1
expected_parity_J_denominator = (
    core_not_two_S**3
    * core_not_half_S**3
    * (pS - 1) ** 3
    * (wS - 1) ** 4
    * source_A_S**5
    * (wS + 1) ** 5
)
expected_parity_I_denominator = (
    wS**2
    * pS**2
    * (pS - 1) ** 3
    * source_A_S**5
    * core_not_two_S**5
    * core_not_half_S**5
    * (wS - 1) ** 5
    * (wS + 1) ** 5
    * D_S**2
)
assert primitive_in(S, parity_clear_audit[0][0]) == primitive_in(
    S, expected_parity_J_denominator
)
assert primitive_in(S, parity_clear_audit[1][0]) == primitive_in(
    S, expected_parity_I_denominator
)
assert [str(scalar) for _, scalar in parity_clear_audit] == [
    "2/16423203268260658146231467800709255289",
    "1/17455927136175424851782794958953454680082898",
]
P25, rem_J = parity_J.quo_rem(wS**2 * D_S * L2 * E_S**6)
P46, rem_I = parity_I.quo_rem(E_S**3)
assert rem_J == 0 and rem_I == 0
assert metric(P25) == {
    "degree": 25,
    "degrees": [6, 14, 14, 6],
    "terms": 5048,
    "sha256": "1a1685279f4e80a86eaf399153051a4c7f7ccc691a2d63c33791d5980174a8d3",
}
assert metric(P46) == {
    "degree": 46,
    "degrees": [5, 25, 25, 17],
    "terms": 35534,
    "sha256": "725c9adcb6d74e93868675be71a65b0321f79bdaf895ba3e571acdad4dac4696",
}


# ---------------------------------------------------------------------------
# 3. Exact deployed-field branch partition.
# ---------------------------------------------------------------------------

TQ = PolynomialRing(QQ, names=("s", "p", "w"), order="degrevlex")
sQ, pQ, wQ = TQ.gens()
TF = PolynomialRing(FF, names=("s", "p", "w"), order="degrevlex")
sF, pF, wF = TF.gens()


def primitive_TQ(value):
    return primitive_in(TQ, value)


def clear_y(value, numerator, denominator):
    value = S(value)
    degree_y = value.degree(yS)
    raw_answer = TQ(0)
    for monomial, coefficient in value.dict().items():
        ky, ks, kp, kw = monomial
        raw_answer += (
            QQ(coefficient)
            * TQ(numerator) ** ky
            * TQ(denominator) ** (degree_y - ky)
            * sQ**ks
            * pQ**kp
            * wQ**kw
        )
    answer = primitive_TQ(raw_answer)
    fraction = TQ.fraction_field()
    # Directly replay the identity on every q-slice line.  The very large
    # parity factors use the identical termwise construction above, but a
    # second fraction-field expansion would be needlessly superlinear.
    if len(value.monomials()) <= 1000:
        substitution = S.hom(
            [
                fraction(TQ(numerator)) / fraction(TQ(denominator)),
                fraction(sQ),
                fraction(pQ),
                fraction(wQ),
            ],
            fraction,
        )
        assert fraction(raw_answer) == (
            fraction(TQ(denominator)) ** degree_y * substitution(value)
        )
    scalar = fraction(answer) / fraction(raw_answer)
    assert scalar.numerator().is_constant()
    assert scalar.denominator().is_constant()
    return answer


def to_TF(value):
    return sum(
        FF(coefficient)
        * sF**monomial[0]
        * pF**monomial[1]
        * wF**monomial[2]
        for monomial, coefficient in TQ(value).dict().items()
    )


def to_SF(value, ring):
    yy, ss, pp, ww = ring.gens()
    return sum(
        FF(coefficient)
        * yy**monomial[0]
        * ss**monomial[1]
        * pp**monomial[2]
        * ww**monomial[3]
        for monomial, coefficient in S(value).dict().items()
    )


def factor_TQ_by_hash(poly, target):
    matches = [
        TQ(factor)
        for factor, _ in TQ(poly).factor()
        if sha(TQ(factor)) == target
    ]
    assert len(matches) == 1
    return matches[0]


def reduced_product(basis, factors):
    value = basis[0].parent()(1)
    for factor in factors:
        value = (value * factor).reduce(basis)
    return value


parent_units = {
    "nonzero_core": pF,
    "distinct_core": sF**2 - 4 * pF,
    "core_not_reciprocal": pF - 1,
    "core_not_plus_one": 1 - sF + pF,
    "core_not_minus_one": 1 + sF + pF,
    "core_not_two": 4 - 2 * sF + pF,
    "core_not_half": 1 - 2 * sF + 4 * pF,
    "moving_nonzero": wF,
    "moving_not_fixed": wF**2 - 1,
    "moving_not_core": wF**2 - sF * wF + pF,
    "moving_inverse_not_core": 1 - sF * wF + pF * wF**2,
    "reconstruction_A": 5 * pF - 4 * sF + 5,
    "reconstruction_E": (
        -2 * sF * wF + pF * wF + 2 * sF - 4 * pF + 4 * wF - 1
    ),
}

# 3.1 L2=0.  The coefficient chart p+1=0 gives p=-1,s=0 and the
# repeated/fixed core q(T)=T^2-1.  Off it, substitute y=2s/(p+1).
L2_reduced = [
    clear_y(value, 2 * sQ, pQ + 1) for value in (A0, A1, F11)
]
w2_minus_p = factor_TQ_by_hash(
    L2_reduced[0],
    "c5393ae5aa25e821dd34893ef498f217912ddba2d8072579410fcbf5559a8209",
)
H9 = factor_TQ_by_hash(
    L2_reduced[1],
    "ba9d20be089a0a1543ff4ee10fdb13042429350704d542a7f9f59d7dbde7604f",
)
Rlin_QQ = factor_TQ_by_hash(
    L2_reduced[2],
    "0d4cf385ad76ac449dd31f35a4af919d254b75779486d3e7696bf8d8cf090d0c",
)
core_plus_QQ = -sQ + pQ + 1
core_minus_QQ = sQ + pQ + 1
source_A_QQ = -4 * sQ + 5 * pQ + 5
assert L2_reduced[0] == (
    (pQ - 1)
    * source_A_QQ**2
    * core_plus_QQ**2
    * core_minus_QQ**2
    * w2_minus_p
)
assert L2_reduced[1] == (
    core_plus_QQ
    * core_minus_QQ
    * source_A_QQ**2
    * (pQ - 1) ** 2
    * H9
)
assert L2_reduced[2] == (
    Rlin_QQ
    * core_plus_QQ
    * (wQ - 1)
    * pQ
    * core_minus_QQ
    * source_A_QQ**2
    * (wQ + 1) ** 2
    * (pQ - 1) ** 2
)
L2_generators = list(map(to_TF, (w2_minus_p, H9, Rlin_QQ)))
L2_basis = list(
    TF.ideal(L2_generators).groebner_basis(algorithm="singular:slimgb")
)
assert len(L2_basis) == 3 and TF.ideal(L2_basis).dimension() == 0
P46_L2_QQ = clear_y(P46, 2 * sQ, pQ + 1)
P46_L2_remainder = to_TF(P46_L2_QQ).reduce(L2_basis)
assert metric(P46_L2_remainder) == {
    "degree": 7,
    "degrees": [0, 6, 1],
    "terms": 12,
    "sha256": "ae2e03fcbb73ab177ddf992966aab46dc1e575cb14377830b0c287831295294f",
}
L2_P46_basis = list(
    TF.ideal(L2_basis + [P46_L2_remainder]).groebner_basis(
        algorithm="singular:slimgb"
    )
)
assert len(L2_P46_basis) == 3 and TF.ideal(L2_P46_basis).dimension() == 0
no_s = [value for value in L2_P46_basis if value.degree(sF) == 0]
linear_w = [value for value in no_s if value.degree(wF) == 1]
assert len(linear_w) == 1 and (wF**2 - pF) in L2_P46_basis
coefficient_w = TF(0)
constant_w = TF(0)
for monomial, coefficient in linear_w[0].dict().items():
    _, exponent_p, exponent_w = monomial
    term = FF(coefficient) * pF**exponent_p
    if exponent_w:
        coefficient_w += term
    else:
        constant_w += term
p_eliminant = TF(constant_w**2 - pF * coefficient_w**2)
eliminant_leading_scalar = p_eliminant.leading_coefficient()
assert eliminant_leading_scalar != 0
p_eliminant /= eliminant_leading_scalar
assert metric(p_eliminant) == {
    "degree": 10,
    "degrees": [0, 10, 0],
    "terms": 9,
    "sha256": "b25564c21bd8301474e7928fd11bd992475890b99233ab6718e885ecf03f7366",
}
assert p_eliminant == (
    pF**2
    * (pF + 1) ** 4
    * (pF - 1) ** 2
    * (pF - 4)
    * (pF - FF(1) / 4)
)
L2_units = dict(parent_units)
L2_units = {"L2_coefficient": pF + 1, **L2_units}
H_L2 = reduced_product(L2_P46_basis, L2_units.values())
assert H_L2 == 0

# 3.2 F5 coefficient-zero chart alpha=beta=0.
SF4 = PolynomialRing(
    FF, names=("y", "s", "p", "w"), order="degrevlex"
)
y4, s4, p4, w4 = SF4.gens()
alpha4 = to_SF(alpha_QQ, SF4)
beta4 = to_SF(beta_QQ, SF4)
alpha_zero_generators = [
    alpha4,
    beta4,
    to_SF(A0, SF4),
    to_SF(A1, SF4),
    to_SF(F11, SF4),
]
alpha_zero_basis = list(
    SF4.ideal(alpha_zero_generators).groebner_basis(
        algorithm="singular:slimgb"
    )
)
assert len(alpha_zero_basis) == 24
assert SF4.ideal(alpha_zero_basis).dimension() == 2
alpha_zero_units = [
    y4 * (p4 + 1) - 2 * s4,
    p4,
    s4**2 - 4 * p4,
    p4 - 1,
    1 - s4 + p4,
    1 + s4 + p4,
    4 - 2 * s4 + p4,
    1 - 2 * s4 + 4 * p4,
    w4,
    w4**2 - 1,
    w4**2 - s4 * w4 + p4,
    1 - s4 * w4 + p4 * w4**2,
    5 * p4 - 4 * s4 + 5,
    -2 * s4 * w4 + p4 * w4 + 2 * s4 - 4 * p4 + 4 * w4 - 1,
]
H_alpha_zero = reduced_product(alpha_zero_basis, alpha_zero_units)
assert H_alpha_zero == 0

# 3.3 F5 coefficient-nonzero charts.  Substitute y=-beta/alpha and retain
# the three primitive q-slice factors G7,G15,G9.
S_to_TQ = S.hom([TQ(0), sQ, pQ, wQ], TQ)
alpha_TQ = TQ(S_to_TQ(alpha_QQ))
beta_TQ = TQ(S_to_TQ(beta_QQ))
F5_reduced = [
    clear_y(value, -beta_TQ, alpha_TQ) for value in (A0, A1, F11)
]
G7_QQ = factor_TQ_by_hash(
    F5_reduced[0],
    "27345df84a941f9892be25b62fd5104a41392d14b40c003be36fab41b9f020e8",
)
G15_QQ = factor_TQ_by_hash(
    F5_reduced[1],
    "fc60106eafded78b78b6549ba16eb23d152f2ef9759abd6b297e993f1dea79b3",
)
G9_QQ = factor_TQ_by_hash(
    F5_reduced[2],
    "73fb7784c21706e1824cbbc52ac374f7c8341b302447e6705c216676ab0cac8e",
)
assert F5_reduced[0] == (
    source_A_QQ**2
    * core_plus_QQ**2
    * (wQ - 1) ** 2
    * core_minus_QQ**2
    * G7_QQ
)
assert F5_reduced[1] == (
    core_plus_QQ
    * core_minus_QQ
    * source_A_QQ**2
    * (wQ - 1) ** 2
    * G15_QQ
)
assert F5_reduced[2] == (
    Rlin_QQ
    * core_plus_QQ
    * (wQ - 1)
    * (wQ + 1)
    * pQ
    * core_minus_QQ
    * source_A_QQ**2
    * G9_QQ
)
G7, G15, G9 = map(to_TF, (G7_QQ, G15_QQ, G9_QQ))
F5_base_basis = list(
    TF.ideal(G7, G15, G9).groebner_basis(algorithm="singular:slimgb")
)
assert len(F5_base_basis) == 38
assert TF.ideal(F5_base_basis).dimension() == 1

P25_F5_QQ = clear_y(P25, -beta_TQ, alpha_TQ)
P46_F5_QQ = clear_y(P46, -beta_TQ, alpha_TQ)
P25_remainder = to_TF(P25_F5_QQ).reduce(F5_base_basis)
P46_remainder = to_TF(P46_F5_QQ).reduce(F5_base_basis)
assert metric(P25_remainder) == {
    "degree": 13,
    "degrees": [11, 12, 9],
    "terms": 368,
    "sha256": "d320c59d012bb6c3d8287c7f83ec9dd3e0977faeff61528c401b316e0333a0ce",
}
assert metric(P46_remainder) == {
    "degree": 13,
    "degrees": [11, 12, 9],
    "terms": 368,
    "sha256": "a0f77109edc5d92ab670dabddfe35a6116012e65e8845fed72aadf3a43a29406",
}
F5_P25_basis = list(
    TF.ideal(F5_base_basis + [P25_remainder]).groebner_basis(
        algorithm="singular:slimgb"
    )
)
assert len(F5_P25_basis) == 35
assert TF.ideal(F5_P25_basis).dimension() == 1

alpha_F = to_TF(alpha_TQ)
beta_F = to_TF(beta_TQ)
D_F = -2 * sF * wF + 4 * pF * wF + 2 * sF - pF + wF - 4
R_F = -5 * sF + 4 * pF + 4
L2_numerator_F = -beta_F * (pF + 1) - 2 * sF * alpha_F
common_F5_units = dict(parent_units)
common_F5_units.update(
    {
        "F5_coefficient": alpha_F,
        "other_B0_factor": L2_numerator_F,
    }
)
generic_units = dict(common_F5_units)
generic_units.update(
    {
        "J_parity_prefactor": D_F,
        "other_F11_factor": R_F,
    }
)
H_generic = reduced_product(F5_P25_basis, generic_units.values())
assert H_generic != 0
assert (H_generic**2).reduce(F5_P25_basis) == 0


def boundary_summary(generators, units, expected_size, expected_dimension):
    basis = list(
        TF.ideal(generators).groebner_basis(algorithm="singular:slimgb")
    )
    assert len(basis) == expected_size
    assert TF.ideal(basis).dimension() == expected_dimension
    H = reduced_product(basis, units.values())
    assert H == 0
    return basis


# First-match order off L2 and alpha=0:
# D=0,R=0; D=0,R!=0,G9=0; D!=0,R=0; D!=0,R!=0,G9=0.
D0_R0_basis = boundary_summary(
    [G7, G15, D_F, R_F],
    dict(common_F5_units),
    4,
    0,
)
D0_G9_units = dict(common_F5_units)
D0_G9_units["other_F11_factor"] = R_F
D0_G9_basis = boundary_summary(
    [G7, G15, G9, D_F],
    D0_G9_units,
    9,
    1,
)
R0_DNZ_units = dict(common_F5_units)
R0_DNZ_units["J_parity_prefactor"] = D_F
R0_DNZ_basis = boundary_summary(
    [G7, G15, R_F],
    R0_DNZ_units,
    2,
    1,
)

result = {
    "schema": "kb-mca-v4-m2-diagonal-112-moving-positive-balanced-sage-v1",
    "prime": int(P0),
    "representative_edges": [["2", "b"], ["2", "1/b"]],
    "assignment_scope": {
        "canonical_only": True,
        "covariance_used": False,
        "other_three_moving_moving_assignments": "OPEN_SEPARATE_EXACT_SYSTEMS",
    },
    "repair_audit_inputs": {
        "projective_y_infinity_payload_sha256": (
            "16cd5144eb45c930e48d02388c658c7aee19d4e60956421e83bb0a485a7e28e8"
        ),
        "finite_y_w_zero_payload_sha256": (
            "e507788efd3bd9be3bd04b14a40e70cbf34acec0eadc24044a3294d057027980"
        ),
        "status": "independently_rederived_in_packet",
    },
    "root_distribution_deleted": [1, 1],
    "source_incidence": {
        "identity": "z=-D/E",
        "parent_nonzero": ["E", "A", "D"],
        "rationale": {
            "E": "source_incidence_denominator",
            "A": "source_reconstruction_determinant",
            "D": "z_nonzero_and_E_nonzero",
        },
    },
    "partition_order": [
        "finite_y_w_zero_qslice",
        "finite_y_w_nonzero_L2",
        "finite_y_w_nonzero_F5_alpha_zero",
        "finite_y_w_nonzero_F5_D0_R0",
        "finite_y_w_nonzero_F5_D0_G9",
        "finite_y_w_nonzero_F5_R0_DNZ",
        "finite_y_w_nonzero_F5_generic_P25",
    ],
    "raw_projective_hashes": expected_raw_hashes,
    "qslice_metrics": expected_qslice_metrics,
    "normalization_audit": {
        "coefficientwise_normalization_used": False,
        "residual_divisor": "monic_(W-w)^2",
        "root_reduction_divisor": "monic_X^2-sX+p",
        "projective_target_pivot": "monic_W^2_coefficient_1",
        "raw_line_scaling": "one_common_nonzero_QQ_scalar_per_cleared_line",
        "raw_clear_scalars": [
            str(scalar) for _, scalar in raw_clear_audit
        ],
        "source_determinant_numerator_factors": [
            "(d-2)^2",
            "(2d-1)^2",
            "(c-2)^2",
            "(2c-1)^2",
            "(w-1)^5",
            "(w+1)^5",
            "A",
            "(p-1)^2",
        ],
        "source_determinant_denominator": "E^6",
        "raw_denominator_patterns": [
            "cd(w-1)^2(w+1)^2(d-2)^2(2d-1)^2(b-1)^2(b+1)^2A^2",
            "cd(w-1)^2(w+1)^2(c-2)^2(2c-1)^2(b-1)^2(b+1)^2A^2",
        ],
        "dropped_qslice_parent_factors": [
            "(p-1)E^2",
            "1",
            "(p-1)E^2",
            "1",
        ],
        "substitution_clearances": {
            "L2": "(p+1)^degree_y",
            "F5": "alpha^degree_y",
        },
        "parity_line_scaling": "one_common_nonzero_QQ_scalar_per_cleared_line",
        "parity_clear_scalars": [
            str(scalar) for _, scalar in parity_clear_audit
        ],
        "parity_denominator_patterns": [
            "core2^3 corehalf^3 (p-1)^3 (w-1)^4 A^5 (w+1)^5",
            "w^2 p^2 (p-1)^3 A^5 core2^5 corehalf^5 (w-1)^5 (w+1)^5 D^2",
        ],
        "eliminant_normalization": "one_nonzero_deployed_field_scalar",
        "projective_y_chart": {
            "homogeneous_coordinates": "[Y:Z]",
            "affine_coordinate": "y=Y/Z",
            "infinity_value": "coefficient_of_y^2",
            "qslice_y_degree": 2,
            "role": "non_load_bearing_compactification_control",
        },
    },
    "factor_metrics": {
        "L2": metric(L2),
        "F5": metric(F5),
        "F11": metric(F11),
        "alpha": metric(alpha_QQ),
        "beta": metric(beta_QQ),
        "G7": metric(G7_QQ),
        "G15": metric(G15_QQ),
        "G9": metric(G9_QQ),
        "P25": metric(P25),
        "P46": metric(P46),
    },
    "charts": {
        "projective_y_infinity": {
            "scope": "canonical_projective_compactification_without_inverting_w",
            "load_bearing": False,
            "generators": expected_yinf_generator_metrics,
            "basis_size": len(yinf_basis),
            "basis_sha256": basis_sha256(yinf_basis),
            "dimension": int(RINF.ideal(yinf_basis).dimension()),
            "localizer_factors": [
                {"name": name, "polynomial": str(factor)}
                for name, factor in yinf_localizer_factors
            ],
            "localizer_remainders": yinf_remainders,
            "localizer_nilpotence": 2,
            "rabinowitsch_basis_size": len(yinf_rabinowitsch_basis),
            "rabinowitsch_unit_ideal": (
                yinf_rabinowitsch_basis == [RINF_T(1)]
            ),
            "terminal": "CONTROL_EMPTY_BY_QSLICE",
        },
        "finite_y_w_zero": {
            "scope": "canonical_assignment_affine_y_w_equals_zero",
            "generators": expected_w0_generator_metrics,
            "basis_size": len(w0_basis),
            "basis_sha256": basis_sha256(w0_basis),
            "dimension": int(RW0.ideal(w0_basis).dimension()),
            "localizer_factors": [
                {"name": name, "polynomial": str(factor)}
                for name, factor in w0_localizer_factors
            ],
            "localizer_remainders": w0_remainders,
            "localizer_nilpotence": 3,
            "rabinowitsch_basis_size": len(w0_rabinowitsch_basis),
            "rabinowitsch_unit_ideal": (
                w0_rabinowitsch_basis == [RW0_T(1)]
            ),
            "terminal": "EMPTY_BY_QSLICE_BEFORE_PARITY",
        },
        "L2_coefficient_zero": {
            "scope": "canonical_assignment_finite_y_w_nonzero",
            "terminal": "PARENT_COLLISION_q_equals_T2_minus_1",
        },
        "L2_P46": {
            "scope": "canonical_assignment_finite_y_w_nonzero",
            "dimension": int(TF.ideal(L2_P46_basis).dimension()),
            "basis_size": len(L2_P46_basis),
            "localizer_nilpotence": 1,
            "P46_remainder": metric(P46_L2_remainder),
            "p_eliminant": metric(p_eliminant),
        },
        "F5_alpha_zero": {
            "scope": "canonical_assignment_finite_y_w_nonzero",
            "dimension": int(SF4.ideal(alpha_zero_basis).dimension()),
            "basis_size": len(alpha_zero_basis),
            "localizer_nilpotence": 1,
        },
        "F5_D0_R0": {
            "scope": "canonical_assignment_finite_y_w_nonzero",
            "dimension": int(TF.ideal(D0_R0_basis).dimension()),
            "basis_size": len(D0_R0_basis),
            "localizer_nilpotence": 1,
        },
        "F5_D0_G9": {
            "scope": "canonical_assignment_finite_y_w_nonzero",
            "dimension": int(TF.ideal(D0_G9_basis).dimension()),
            "basis_size": len(D0_G9_basis),
            "localizer_nilpotence": 1,
        },
        "F5_R0_DNZ": {
            "scope": "canonical_assignment_finite_y_w_nonzero",
            "dimension": int(TF.ideal(R0_DNZ_basis).dimension()),
            "basis_size": len(R0_DNZ_basis),
            "localizer_nilpotence": 1,
        },
        "F5_generic_P25": {
            "scope": "canonical_assignment_finite_y_w_nonzero",
            "dimension": int(TF.ideal(F5_P25_basis).dimension()),
            "basis_size": len(F5_P25_basis),
            "localizer_nonzero": True,
            "localizer_nilpotence": 2,
            "P25_remainder": metric(P25_remainder),
            "P46_remainder_unused": metric(P46_remainder),
        },
    },
    "parity_usage": {
        "L2": "P46",
        "F5_generic": "P25",
        "F5_boundaries": "q-slice only",
        "scope": "canonical_assignment_finite_y_w_nonzero_with_A_E_D_nonzero",
        "low_squared_quotient_used": False,
    },
    "verdict": (
        "CANONICAL_MOVING_MOVING_ALIGNED_POSITIVE_BALANCED_1_1_EMPTY"
    ),
}
encoded = json.dumps(
    result, sort_keys=True, separators=(",", ":"), default=int
).encode()
print(json.dumps(result, sort_keys=True, default=int))
print("payload_sha256=" + hashlib.sha256(encoded).hexdigest())
print("PASS")
