#!/usr/bin/env sage
"""Exact replay of one fixed-moving aligned-positive crossed representative.

The replay starts from the parent source-facet reconstruction over QQ.  It
fixes J0={2,1/2,b,1/b}, J1={c,d}, and the single internal assignment
{{2,1/2},{2,b}}.  It derives all four factor branches for the crossed root
distribution (0,2), deletes the two c-choice-zero branches by a product of
declared chart units, and sends the two remaining branches to H8 and H9.
H8 forces a label collision.  H9 is decomposed natively over the deployed
characteristic; its only noncollision component fails both full quotient
identities.

This is representative-only.  The other seven fixed-moving assignments
are separate exact systems.  Complete-system covariance is not claimed:
endpoint-only transport preserves the observed residual side but not the
aligned target, while diagonal W transport preserves the target but not the
observed residual/source W divisor.  No claim is made here about the
separately derived (2,0) system.
"""

import hashlib
import json

P0 = 2130706433

R = PolynomialRing(QQ, names=("b", "c", "d", "w"), order="degrevlex")
b, c, d, w = R.gens()
K = R.fraction_field()
bK, cK, dK, wK = map(K, (b, c, d, w))
a = K(2)


def primitive(value):
    value = R(value)
    value = R(value / value.content())
    return -value if value.leading_coefficient() < 0 else value


def primitive_numerator(value):
    return primitive(value.numerator())


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

# Fixed-moving positive internal assignment ({2,1/2},{2,b}).
first, second = edge(a, 1 / a), edge(a, bK)
right, left = 1 / a, bK
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
    ur = sum(u[i] * root**i for i in range(3))
    vr = sum(v[i] * root**i for i in range(3))
    quotient, remainder = (ur**2 - W * vr**2).quo_rem((W - wK) ** 2)
    assert remainder == 0
    return quotient


def target_quadratic(multiplicity):
    return (W - 1 / cK) ** multiplicity * (W - 1 / dK) ** (
        2 - multiplicity
    )


def projective_equations(observed, expected):
    return (
        primitive_numerator(
            observed[0] * expected[2] - observed[2] * expected[0]
        ),
        primitive_numerator(
            observed[1] * expected[2] - observed[2] * expected[1]
        ),
    )


# Root distribution (0,2).
c_eq = projective_equations(residual_at(cK), target_quadratic(0))
d_eq = projective_equations(residual_at(dK), target_quadratic(2))
c_linear_factors = [h for h, _ in c_eq[0].factor() if h.degree(b) == 1]
d_linear_factors = [h for h, _ in d_eq[0].factor() if h.degree(b) == 1]
assert len(c_linear_factors) == len(d_linear_factors) == 2

# Named admissible-locus product used only for the two linear-solve
# degeneracy guards below.  Proving emptiness after inverting this smaller
# product is stronger than using every parent label difference.
E1 = (
    4 * c * d * w
    - c * d
    - 2 * c * w
    - 2 * d * w
    + 2 * c
    + 2 * d
    + w
    - 4
)
E2 = (
    c * d * w
    - 4 * c * d
    - 2 * c * w
    - 2 * d * w
    + 2 * c
    + 2 * d
    + 4 * w
    - 1
)
A_R = 5 * c * d - 4 * c - 4 * d + 5
Hbasic = (
    b
    * c
    * d
    * w
    * E1
    * E2
    * (b - 1)
    * (b + 1)
    * (c - 1)
    * (c + 1)
    * (d - 1)
    * (d + 1)
    * (w - 1)
    * (w + 1)
    * A_R
    * (c * d - 1)
    * (b - 2)
)

DR = PolynomialRing(
    GF(P0), names=("tt", "bb", "cc", "dd", "ww"), order="degrevlex"
)
tt, bb, cc0, dd0, ww = DR.gens()


def to_DR(value):
    value = R(value)
    return sum(
        GF(P0)(coefficient)
        * bb**monomial[0]
        * cc0**monomial[1]
        * dd0**monomial[2]
        * ww**monomial[3]
        for monomial, coefficient in value.dict().items()
    )


# If the selected c-factor has both b coefficient and constant term zero,
# division by its b coefficient is unavailable.  For all four c/d choices
# the exact named localization is nevertheless empty.  This is a finite
# Rabinowitsch check, not a generic saturation.
c_degenerate_checks = []
for c_choice in (0, 1):
    c_factor = c_linear_factors[c_choice]
    c_constant_R = R(c_factor.subs({b: 0}))
    c_linear_R = R(c_factor.subs({b: 1}) - c_constant_R)
    for d_choice in (0, 1):
        localizer = Hbasic * ((d - w) if c_choice == 0 else R(1))
        ideal = DR.ideal(
            to_DR(c_constant_R),
            to_DR(c_linear_R),
            to_DR(d_linear_factors[d_choice]),
            to_DR(c_eq[1]),
            to_DR(d_eq[1]),
            tt * to_DR(localizer) - 1,
        )
        basis = ideal.groebner_basis()
        assert basis == [DR(1)]
        c_degenerate_checks.append((c_choice, d_choice))
assert c_degenerate_checks == [(0, 0), (0, 1), (1, 0), (1, 1)]

S = PolynomialRing(QQ, names=("c", "d", "w"), order="degrevlex")
cS, dS, wS = S.gens()
KS = S.fraction_field()
at_b0 = R.hom([KS(0), cS, dS, wS], KS)
at_b1 = R.hom([KS(1), cS, dS, wS], KS)


def branch_for_c_choice(choice):
    c_factor = c_linear_factors[choice]
    b_constant = at_b0(c_factor)
    b_linear = at_b1(c_factor) - b_constant
    assert b_linear
    b_solution = -b_constant / b_linear
    sub_b = R.hom([b_solution, cS, dS, wS], KS)

    def substitute(value):
        value = sub_b(value)
        result = S(value.numerator())
        result = S(result / result.content())
        return -result if result.leading_coefficient() < 0 else result

    return b_solution, b_linear, sub_b, substitute


# The c-choice-zero branch is impossible before either d choice is selected.
# The second c-root projective equation becomes exactly this product of
# parent nonzero units, up to sign.
b_choice_zero, _, _, substitute_zero = branch_for_c_choice(0)
c_choice_zero_equation = substitute_zero(c_eq[1])
A = 5 * cS * dS - 4 * cS - 4 * dS + 5
c_choice_zero_expected = (
    dS
    * (wS - dS) ** 2
    * (wS - 1) ** 2
    * (wS + 1) ** 2
    * (dS - 2) ** 2
    * (2 * dS - 1) ** 2
    * (cS - 1) ** 2
    * (cS + 1) ** 2
    * A**2
    * (cS * dS - 1) ** 4
)
assert c_choice_zero_equation == c_choice_zero_expected
assert len(d_linear_factors) == 2  # both d choices are killed by this row

# The c-choice-one branch leaves exactly two d choices, H8 and H9.
b_solution, b_linear_choice_one, sub_b_choice_one, substitute_b = (
    branch_for_c_choice(1)
)
branch_common = (substitute_b(c_eq[1]), substitute_b(d_eq[1]))


def essential_factor(value):
    return max((h for h, _ in value.factor()), key=lambda h: h.total_degree())


def audit_branch(d_choice):
    first_eq = substitute_b(d_linear_factors[d_choice])
    essentials = [
        essential_factor(first_eq),
        essential_factor(branch_common[0]),
        essential_factor(branch_common[1]),
    ]
    assert essentials[0].degree(wS) == 1
    T = PolynomialRing(QQ, names=("c", "d"), order="degrevlex")
    cT, dT = T.gens()
    KT = T.fraction_field()
    at_w0 = S.hom([cT, dT, KT(0)], KT)
    at_w1 = S.hom([cT, dT, KT(1)], KT)
    w_const = at_w0(essentials[0])
    w_linear = at_w1(essentials[0]) - w_const
    assert w_linear

    # The simultaneous w coefficient/constant-zero split cannot be divided
    # by w_linear.  Replay its exact named localization before solving.
    DS = PolynomialRing(
        GF(P0), names=("tt", "cc", "dd", "ww"), order="degrevlex"
    )
    ttS, ccS, ddS, wwS = DS.gens()

    def to_DS(value):
        value = S(value)
        return sum(
            GF(P0)(coefficient)
            * ccS**monomial[0]
            * ddS**monomial[1]
            * wwS**monomial[2]
            for monomial, coefficient in value.dict().items()
        )

    h_sub = sub_b_choice_one(Hbasic)
    h_local = (
        S(h_sub.numerator())
        * S(h_sub.denominator())
        * S(b_linear_choice_one.numerator())
        * S(b_linear_choice_one.denominator())
    )
    w_degenerate_ideal = DS.ideal(
        to_DS(T(w_const)),
        to_DS(T(w_linear)),
        to_DS(essentials[1]),
        to_DS(essentials[2]),
        ttS * to_DS(h_local) - 1,
    )
    assert w_degenerate_ideal.groebner_basis() == [DS(1)]

    w_solution = -w_const / w_linear
    sub_w = S.hom([cT, dT, w_solution], KT)

    def reduce_w(value):
        value = T(sub_w(value).numerator())
        value = T(value / value.content())
        return -value if value.leading_coefficient() < 0 else value

    return T, KT, w_solution, [reduce_w(value) for value in essentials[1:]]


# H8: after parent localization the second reduced equation retains only
# c+d.  On d=-c the solved source label is w=c, a forbidden collision.
T8, KT8, w8, red8 = audit_branch(0)
c8, d8 = T8.gens()
h8_factorization = red8[1].factor()
h8_factors = {str(factor): exponent for factor, exponent in h8_factorization}
assert h8_factors == {
    "c": 1,
    "-c + d": 2,
    "d - 2": 2,
    "d + 1": 2,
    "2*d - 1": 2,
    "c - 2": 2,
    "c - 1": 2,
    "c + d": 2,
    "2*c - 1": 2,
    "c*d - 1": 2,
    "5*c*d - 4*c - 4*d + 5": 2,
}
w8_num = T8(w8.numerator())
w8_den = T8(w8.denominator())
assert w8_num(c8, -c8) == 10 * c8**2 * (c8 - 1)
assert w8_den(c8, -c8) == 10 * c8 * (c8 - 1)
assert (w8_num - c8 * w8_den)(c8, -c8) == 0
assert red8[0](c8, -c8) == (
    400
    * c8**3
    * (c8 - 1) ** 2
    * (c8 + 1) ** 2
    * (c8**2 - 5 * c8 + 1) ** 2
)

# H9: remove the displayed parent units and retain two equations e0,e1.
T9, KT9, w9, red9 = audit_branch(1)
c9, d9 = T9.gens()
e0 = red9[0] // (c9 * d9 - 1) ** 2
known1 = (
    c9
    * (d9 - 2) ** 2
    * (2 * d9 - 1) ** 2
    * (c9 + 1) ** 2
    * (c9 * d9 - 1) ** 2
    * (5 * c9 * d9 - 4 * c9 - 4 * d9 + 5) ** 2
)
e1 = red9[1] // known1
h9 = 100 * c9**4 - 504 * c9**3 + 817 * c9**2 - 504 * c9 + 100

# Recompute the terminal ideal natively over the deployed prime.
Fp = GF(P0)
L = PolynomialRing(Fp, names=("dd", "cc"), order="lex")
dd, cc = L.gens()


def to_L(value):
    value = T9(value)
    return sum(
        Fp(coefficient) * cc**monomial[0] * dd**monomial[1]
        for monomial, coefficient in value.dict().items()
    )


gb_mod = L.ideal(to_L(e0), to_L(e1)).groebner_basis()
assert len(gb_mod) == 3
q2L = cc**2 - 14 * cc + 1
q6L = (
    4 * cc**6
    - 112 * cc**5
    + 317 * cc**4
    - 430 * cc**3
    + 317 * cc**2
    - 112 * cc
    + 4
)
hL = 100 * cc**4 - 504 * cc**3 + 817 * cc**2 - 504 * cc + 100
expected_eliminant = (
    (2 * cc - 1) ** 3
    * (cc - 2) ** 3
    * q2L
    * q6L
    * hL
)
assert (
    gb_mod[-1] / gb_mod[-1].leading_coefficient()
    == expected_eliminant / expected_eliminant.leading_coefficient()
)

for component, collision in (
    (q2L, dd * cc - 1),
    (q6L, dd - cc),
):
    ideal = L.ideal(to_L(e0), to_L(e1), component)
    assert ideal.reduce(collision) == 0

h_relation = 375 * dd - 1600 * cc**3 + 6664 * cc**2 - 7241 * cc + 1400
assert L.ideal(to_L(e0), to_L(e1), hL).reduce(h_relation) == 0

# Reconstruct the full quotient on the only noncollision component h9.
QX = PolynomialRing(QQ, "xx")
xx = QX.gen()
KX = QX.fraction_field()
d_relation = (
    QQ(64) / 15 * xx**3
    - QQ(6664) / 375 * xx**2
    + QQ(7241) / 375 * xx
    - QQ(56) / 15
)
to_x = T9.hom([xx, d_relation], KX)
w_x = to_x(w9.numerator()) / to_x(w9.denominator())
rho = S.hom([c9, d9, w9], KT9)
b9 = rho(b_solution.numerator()) / rho(b_solution.denominator())
b_x = to_x(b9.numerator()) / to_x(b9.denominator())
sigma = R.hom([b9, c9, d9, w9], KT9)
z9 = sigma(z.numerator()) / sigma(z.denominator())
z_x = to_x(z9.numerator()) / to_x(z9.denominator())

FpX = PolynomialRing(Fp, "xx")
xxp = FpX.gen()
hmod = FpX(QX(to_x(h9)))
AA = FpX.quotient(hmod, "alpha")
alpha = AA.gen()


def qpoly_to_fp(poly):
    poly = QX(poly)
    return FpX(
        {
            exponent: Fp(coefficient)
            for exponent, coefficient in poly.dict().items()
        }
    )


def kx_to_A(value):
    numerator = AA(qpoly_to_fp(value.numerator()))
    denominator_poly = qpoly_to_fp(value.denominator())
    assert gcd(denominator_poly, hmod) == 1
    return numerator * AA(denominator_poly).inverse_of_unit()


def eval_R_fraction(value):
    phi = R.hom([b_x, xx, to_x(d9), w_x], KX)
    return kx_to_A(phi(value.numerator()) / phi(value.denominator()))


AY = PolynomialRing(AA, "Y")
Y = AY.gen()
uA = [AY([eval_R_fraction(coefficient) for coefficient in value]) for value in u]
vA = [AY([eval_R_fraction(coefficient) for coefficient in value]) for value in v]
cA = alpha
dA = kx_to_A(to_x(d9))
wA = kx_to_A(w_x)
bA = kx_to_A(b_x)
zA = kx_to_A(z_x)


def g_at(label):
    ua = sum(uA[i] * label**i for i in range(3))
    va = sum(vA[i] * label**i for i in range(3))
    return ua**2 - Y * va**2


def locator(values):
    result = AY(1)
    for value in values:
        result *= Y - value
    return result


j_labels = (AA(2), AA(1) / 2, bA, 1 / bA, cA, dA)
i_labels = (1 / cA, 1 / dA, wA, 1 / wA, zA, 1 / zA)
k_labels = (wA, zA, 1 / zA, 1 / cA, 1 / dA)
r_labels = (1 / wA, *j_labels)
qA = locator((cA, dA))
pairs = {
    "J": (
        prod(g_at(label) for label in j_labels),
        locator(k_labels) ** 4 * qA**2,
    ),
    "I": (
        qA**2 * prod(g_at(label) for label in i_labels),
        locator(r_labels) ** 4,
    ),
}

mismatch_records = {}
for side, (observed, expected) in pairs.items():
    degree = max(observed.degree(), expected.degree())
    mismatch = observed[1] * expected[degree] - expected[1] * observed[degree]
    representative = FpX(mismatch.lift())
    gcd_value, bezout_h, bezout_m = xgcd(hmod, representative)
    assert gcd_value == 1
    assert bezout_h * hmod + bezout_m * representative == 1
    mismatch_records[side] = {
        "mismatch": [int(value) for value in representative],
        "bezout_h": [int(value) for value in bezout_h],
        "bezout_mismatch": [int(value) for value in bezout_m],
    }

expected_mismatch_records = {
    "J": {
        "mismatch": [1265012543, 2079603121, 44715398, 1153095255],
        "bezout_h": [1378984398, 161871344, 481856514],
        "bezout_mismatch": [
            1355798505,
            577218842,
            1092963338,
            2108730127,
        ],
    },
    "I": {
        "mismatch": [1474202438, 1474392606, 1373289511, 1777964224],
        "bezout_h": [450536384, 1582407299, 134274715],
        "bezout_mismatch": [
            1149576513,
            264697898,
            1366419164,
            1452206296,
        ],
    },
}
assert mismatch_records == expected_mismatch_records

result = {
    "schema": "kb-mca-v4-m2-diagonal-112-fixed-positive-crossed-sage-v1",
    "prime": int(P0),
    "c_linear_degenerate_splits_deleted": int(len(c_degenerate_checks)),
    "c_choice_zero_d_choices_deleted": int(2),
    "H8_collision": "w=c",
    "H9_groebner_size": int(len(gb_mod)),
    "H9_eliminant_degree": int(gb_mod[-1].degree(cc)),
    "H9_full_quotient_mismatches_units": sorted(mismatch_records),
    "root_distributions_deleted": [[int(0), int(2)]],
    "root_distributions_open": [[int(1), int(1)], [int(2), int(0)]],
    "w_linear_degenerate_splits_deleted": int(2),
}
encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
print(json.dumps(result, sort_keys=True))
print("payload_sha256=" + hashlib.sha256(encoded).hexdigest())
print("PASS")
