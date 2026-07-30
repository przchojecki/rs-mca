#!/usr/bin/env sage
"""Exact replay of one fixed-moving aligned-positive identity representative.

Starting from the parent source-facet reconstruction over QQ, this fixes
J0={2,1/2,b,1/b}, J1={c,d}, and the single internal assignment
{{2,1/2},{2,b}}.  It derives the four factor branches for root distribution
(2,0).  Named localized Groebner computations guard every division.  The
ordinary branches end in declared label collisions or in a
deployed-characteristic component on which both full quotient identities
have explicit Bezout-unit mismatches.

This is representative-only.  The other seven fixed-moving assignments are
separate exact systems.  Complete-system covariance is not claimed:
endpoint-only transport preserves the observed residual side but not the
aligned target, while diagonal W transport preserves the target but not the
observed residual/source W divisor.  This script also makes no claim about
any balanced (1,1), moving-moving, or near-aligned system.
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


# Identity-doubled root distribution (2,0).
c_eq = projective_equations(residual_at(cK), target_quadratic(2))
d_eq = projective_equations(residual_at(dK), target_quadratic(0))
c_linear_factors = [h for h, _ in c_eq[0].factor() if h.degree(b) == 1]
d_linear_factors = [h for h, _ in d_eq[0].factor() if h.degree(b) == 1]
assert len(c_linear_factors) == len(d_linear_factors) == 2

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


# Four named coefficient-zero charts.  On c-choice zero, c-w is an
# ordinary-branch unit because that branch is deleted by the w=c collision.
c_degenerate_checks = []
for c_choice in (0, 1):
    c_factor = c_linear_factors[c_choice]
    c_constant_R = R(c_factor.subs({b: 0}))
    c_linear_R = R(c_factor.subs({b: 1}) - c_constant_R)
    for d_choice in (0, 1):
        localizer = Hbasic * ((c - w) if c_choice == 0 else R(1))
        ideal = DR.ideal(
            to_DR(c_constant_R),
            to_DR(c_linear_R),
            to_DR(d_linear_factors[d_choice]),
            to_DR(c_eq[1]),
            to_DR(d_eq[1]),
            tt * to_DR(localizer) - 1,
        )
        assert ideal.groebner_basis() == [DR(1)]
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


# c-choice zero is deleted before selecting d: the second c equation
# contains the forbidden equal-label factor (w-c)^2 and only declared units.
_, _, _, substitute_zero = branch_for_c_choice(0)
c_choice_zero_equation = substitute_zero(c_eq[1])
A = 5 * cS * dS - 4 * cS - 4 * dS + 5
c_choice_zero_expected = (
    cS
    * (wS - cS) ** 2
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


# c1/d0: the retained ordinary factor is (c+d)^2.  On d=-c, the solved
# b is 1/2, colliding with a fixed label.
T0, KT0, w0, red0 = audit_branch(0)
c0, d0 = T0.gens()
factors0 = {str(factor): exponent for factor, exponent in red0[1].factor()}
assert factors0["c + d"] == 2
rho0 = S.hom([c0, d0, w0], KT0)
b0 = rho0(b_solution.numerator()) / rho0(b_solution.denominator())
assert T0((b0 - QQ(1) / 2).numerator())(c0, -c0) == 0
assert T0((b0 - QQ(1) / 2).denominator())(c0, -c0) != 0

# c1/d1: remove only displayed parent units and retain E0,E1.
T1, KT1, w1, red1 = audit_branch(1)
c1, d1 = T1.gens()
E0_terminal = red1[0] // (c1 * d1 - 1) ** 2
known1 = (
    d1
    * (d1 - 2) ** 2
    * (2 * d1 - 1) ** 2
    * (c1 + 1) ** 2
    * (c1 - 1) ** 6
    * (c1 * d1 - 1) ** 2
    * (5 * c1 * d1 - 4 * c1 - 4 * d1 + 5) ** 2
)
E1_terminal = red1[1] // known1

f6T = (
    9 * c1**6
    - 82 * c1**5
    + 119 * c1**4
    - 156 * c1**3
    + 119 * c1**2
    - 82 * c1
    + 9
)
f8T = (
    324 * c1**8
    - 5328 * c1**7
    + 29617 * c1**6
    - 77552 * c1**5
    + 106134 * c1**4
    - 77552 * c1**3
    + 29617 * c1**2
    - 5328 * c1
    + 324
)
f10T = (
    36 * c1**10
    - 352 * c1**9
    + 1741 * c1**8
    - 5266 * c1**7
    + 9871 * c1**6
    - 12124 * c1**5
    + 9871 * c1**4
    - 5266 * c1**3
    + 1741 * c1**2
    - 352 * c1
    + 36
)
resultant_c = E0_terminal.resultant(E1_terminal, d1)
expected_resultant = (
    3486784401
    * (c1 - 2) ** 4
    * (2 * c1 - 1) ** 4
    * (c1 - 1) ** 10
    * (c1 + 1) ** 10
    * f6T
    * f8T
    * f10T
)
assert resultant_c == expected_resultant

Fp = GF(P0)
L = PolynomialRing(Fp, names=("dd", "cc"), order="lex")
dd, cc = L.gens()


def to_L(value):
    value = T1(value)
    return sum(
        Fp(coefficient) * cc**monomial[0] * dd**monomial[1]
        for monomial, coefficient in value.dict().items()
    )


components = {}
for name, factor in (("f6", f6T), ("f8", f8T), ("f10", f10T)):
    components[name] = L.ideal(
        to_L(E0_terminal), to_L(E1_terminal), to_L(factor)
    )
assert components["f6"].reduce(dd * cc - 1) == 0
assert components["f6"].reduce(to_L(w1.numerator() - w1.denominator())) == 0
assert components["f10"].reduce(dd - cc) == 0

# Reconstruct both complete quotient identities on f8.
FpC = PolynomialRing(Fp, "xx")
xx = FpC.gen()
f8C = FpC([Fp(coefficient) for coefficient in f8T.univariate_polynomial()])
A8 = FpC.quotient(f8C, "alpha")
alpha = A8.gen()
f8_basis = components["f8"].groebner_basis()
assert len(f8_basis) == 2
linear_d = next(value for value in f8_basis if value.degree(dd) == 1)
coeff_d = sum(
    Fp(coefficient) * alpha**monomial[1]
    for monomial, coefficient in linear_d.dict().items()
    if monomial[0] == 1
)
const_d = sum(
    Fp(coefficient) * alpha**monomial[1]
    for monomial, coefficient in linear_d.dict().items()
    if monomial[0] == 0
)
dA = -const_d / coeff_d


def eval_T_poly(value):
    value = T1(value)
    return sum(
        Fp(coefficient) * alpha**monomial[0] * dA**monomial[1]
        for monomial, coefficient in value.dict().items()
    )


def eval_T_fraction(value):
    denominator = eval_T_poly(T1(value.denominator()))
    assert denominator
    return eval_T_poly(T1(value.numerator())) / denominator


wA = eval_T_fraction(w1)
rho1 = S.hom([c1, d1, w1], KT1)
b1 = rho1(b_solution.numerator()) / rho1(b_solution.denominator())
bA = eval_T_fraction(b1)
sigma1 = R.hom([b1, c1, d1, w1], KT1)
z1 = sigma1(z.numerator()) / sigma1(z.denominator())
zA = eval_T_fraction(z1)


def eval_R_poly(value):
    value = R(value)
    return sum(
        Fp(coefficient)
        * bA**monomial[0]
        * alpha**monomial[1]
        * dA**monomial[2]
        * wA**monomial[3]
        for monomial, coefficient in value.dict().items()
    )


def eval_R_fraction(value):
    denominator = eval_R_poly(R(value.denominator()))
    assert denominator
    return eval_R_poly(R(value.numerator())) / denominator


AY = PolynomialRing(A8, "Y")
Y = AY.gen()
uA = [
    AY([eval_R_fraction(coefficient) for coefficient in value])
    for value in u
]
vA = [
    AY([eval_R_fraction(coefficient) for coefficient in value])
    for value in v
]


def g_at(label):
    ua = sum(uA[i] * label**i for i in range(3))
    va = sum(vA[i] * label**i for i in range(3))
    return ua**2 - Y * va**2


def locator(values):
    result = AY(1)
    for value in values:
        result *= Y - value
    return result


j_labels = (A8(2), A8(1) / 2, bA, 1 / bA, alpha, dA)
i_labels = (1 / alpha, 1 / dA, wA, 1 / wA, zA, 1 / zA)
k_labels = (wA, zA, 1 / zA, 1 / alpha, 1 / dA)
r_labels = (1 / wA, *j_labels)
qA = locator((alpha, dA))
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

expected_witnesses = {
    "J": {
        "mismatch": [
            482954018,
            1996723265,
            47079281,
            913730111,
            915891061,
            1812515029,
            763829210,
            9883900,
        ],
        "bezout_f8": [
            1050548741,
            177769301,
            1055326069,
            1301926167,
            1415812154,
            1258221600,
            1606439928,
        ],
        "bezout_mismatch": [
            162121279,
            343401622,
            1095838264,
            1916788299,
            901744177,
            1465118481,
            885094218,
            29628355,
        ],
    },
    "I": {
        "mismatch": [
            467867406,
            1278816008,
            1198218452,
            795930408,
            413622875,
            1507080347,
            1359907050,
            829611936,
        ],
        "bezout_f8": [
            728891986,
            1711384843,
            1704323271,
            1339492114,
            986262926,
            227124627,
            1820761540,
        ],
        "bezout_mismatch": [
            1963273613,
            197424372,
            2109338360,
            1768858959,
            338011691,
            1809782485,
            644748967,
            880556468,
        ],
    },
}

witnesses = {}
for side, (observed, expected) in pairs.items():
    degree = max(observed.degree(), expected.degree())
    mismatch = observed[1] * expected[degree] - expected[1] * observed[degree]
    representative = FpC(mismatch.lift())
    gcd_value, bezout_f8, bezout_mismatch = xgcd(f8C, representative)
    unit = gcd_value[0]
    bezout_f8 /= unit
    bezout_mismatch /= unit
    gcd_value /= unit
    assert gcd_value == 1
    witnesses[side] = {
        "mismatch": [int(value) for value in representative],
        "bezout_f8": [int(value) for value in bezout_f8],
        "bezout_mismatch": [int(value) for value in bezout_mismatch],
    }
assert witnesses == expected_witnesses

result = {
    "schema": "kb-mca-v4-m2-diagonal-112-fixed-positive-identity-sage-v1",
    "assignment": "{{2,1/2},{2,b}}",
    "assignment_scope": "SINGLE_NORMALIZED_REPRESENTATIVE",
    "complete_system_covariance": "NOT_CLAIMED",
    "other_fixed_moving_assignments": "OPEN_SEPARATE_EXACT_SYSTEMS",
    "prime": int(P0),
    "initial_b_degenerate_splits_deleted": int(len(c_degenerate_checks)),
    "later_w_degenerate_splits_deleted": int(2),
    "c_choice_zero_d_choices_deleted": int(2),
    "c1_d0_collision": "b=1/2",
    "c1_d1_components": ["f6:cd=1,w=1", "f8:quotient-mismatch", "f10:d=c"],
    "representative_root_distributions_deleted": [[int(2), int(0)]],
    "representative_root_distributions_open": [[int(1), int(1)]],
}
encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
print(json.dumps(result, sort_keys=True))
print("payload_sha256=" + hashlib.sha256(encoded).hexdigest())
print("PASS")
