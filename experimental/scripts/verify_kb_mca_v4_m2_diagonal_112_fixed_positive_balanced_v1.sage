#!/usr/bin/env sage
"""Exact replay of one fixed-moving aligned-positive balanced representative.

The script reconstructs the parent source form over QQ, derives the four
q-slice projective equations for root distribution (1,1), and classifies
the quadratic-in-b relation by its leading coefficient.  Every division is
guarded by an explicit coefficient-zero chart and a named Rabinowitsch
localizer.  All ideal computations are native over GF(2130706433).

The fixed internal assignment is {{2,1/2},{2,b}} in
J0={2,1/2,b,1/b}.  The other seven fixed-moving assignments are separate
exact systems and remain open; complete-system covariance is not claimed.
The script also makes no claim about moving-moving, near-positive,
exceptional, or row-level cases.
"""

import hashlib
import json
import re
from pathlib import Path

P0 = 2130706433
F = GF(P0)
SINGULAR_SOURCE = Path(
    "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.sing"
).read_text()


def singular_expression(name):
    matches = re.findall(
        r"poly\s+" + re.escape(name) + r"\s*=\s*(.*?);",
        SINGULAR_SOURCE,
        flags=re.DOTALL,
    )
    assert len(matches) == 1
    return re.sub(r"\s+", "", matches[0]).replace("^", "**")

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


def metric(value):
    value = value.parent()(value)
    return {
        "degree": int(value.total_degree()),
        "degrees": [int(value.degree(g)) for g in value.parent().gens()],
        "terms": int(len(value.monomials())),
        "sha256": hashlib.sha256(str(value).encode()).hexdigest(),
    }


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


# Parent source-facet reconstruction.
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

# Fixed-moving internal assignment ({2,1/2},{2,b}).
first, second = edge(a, 1 / a), edge(a, bK)
target_internal = (
    (linear_0 + bK * linear_1) * first
    + (linear_0 + (1 / a) * linear_1) * second
) / (bK - 1 / a)
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


target_balanced = (W - 1 / cK) * (W - 1 / dK)


def projective_equations(observed):
    return (
        primitive_numerator(
            observed[0] * target_balanced[2]
            - observed[2] * target_balanced[0]
        ),
        primitive_numerator(
            observed[1] * target_balanced[2]
            - observed[2] * target_balanced[1]
        ),
    )


c_eq = projective_equations(residual_at(cK))
d_eq = projective_equations(residual_at(dK))


def essential_quadratic(value):
    candidates = [h for h, _ in value.factor() if h.degree(b) == 2]
    assert len(candidates) == 1
    return primitive(candidates[0])


qC_R = essential_quadratic(c_eq[0])
qD_R = essential_quadratic(d_eq[0])
assert metric(qC_R) == {
    "degree": 12,
    "degrees": [2, 4, 4, 2],
    "terms": 197,
    "sha256": "89ac6b1c752f14da89fb1c9f2e3dca3a438fbd87fb7bcbc927a03c943e1a0212",
}
assert metric(qD_R) == {
    "degree": 12,
    "degrees": [2, 4, 4, 2],
    "terms": 197,
    "sha256": "bcee3e9dd49ebc1957ed817f0c16d8b302c89ed51626c9dbbbd53724efdcf7ba",
}
assert metric(c_eq[1])["sha256"] == (
    "163673f99d8078515ab0b0845a2e77f617a627507e78474b70b4bb844d381367"
)
assert metric(d_eq[1])["sha256"] == (
    "7a219b3ebff0b4162c6533209bc2402e8f80f5f0899bcd45435c820df5f88582"
)

# The leading coefficient L partitions all b charts.
def b_coefficient(value, exponent):
    return sum(
        coefficient * c**monomial[1] * d**monomial[2] * w**monomial[3]
        for monomial, coefficient in R(value).dict().items()
        if monomial[0] == exponent
    )


L_R, M_R, N_R = [
    R(b_coefficient(qC_R, exponent)) for exponent in (2, 1, 0)
]
assert qC_R == L_R * b**2 + M_R * b + N_R
assert metric(L_R) == {
    "degree": 10,
    "degrees": [0, 4, 4, 2],
    "terms": 69,
    "sha256": "1d10dcd6da3f56234773ef8067f1471d636ed43d71dca825576554e5fe05bd8e",
}

# A deliberately small subset of the retained parent open set.  Unit-ideal
# emptiness after this localization is stronger than after the full parent
# localizer.
DR = PolynomialRing(
    F, names=("t", "b", "c", "d", "w"), order="degrevlex"
)
tD, bD, cD, dD, wD = DR.gens()


def to_DR(value):
    value = R(value)
    return sum(
        F(coefficient)
        * bD**monomial[0]
        * cD**monomial[1]
        * dD**monomial[2]
        * wD**monomial[3]
        for monomial, coefficient in value.dict().items()
    )


E1 = (
    4 * cD * dD * wD
    - cD * dD
    - 2 * cD * wD
    - 2 * dD * wD
    + 2 * cD
    + 2 * dD
    + wD
    - 4
)
E2 = (
    cD * dD * wD
    - 4 * cD * dD
    - 2 * cD * wD
    - 2 * dD * wD
    + 2 * cD
    + 2 * dD
    + 4 * wD
    - 1
)
Aparent = 5 * cD * dD - 4 * cD - 4 * dD + 5
Hbasic = (
    bD
    * cD
    * dD
    * wD
    * E1
    * E2
    * (bD - 1)
    * (bD + 1)
    * (cD - 1)
    * (cD + 1)
    * (dD - 1)
    * (dD + 1)
    * (wD - 1)
    * (wD + 1)
    * Aparent
    * (cD * dD - 1)
    * (bD - 2)
    * (2 * bD - 1)
    * (cD - dD)
)
leading_zero = DR.ideal(
    to_DR(L_R),
    to_DR(qC_R),
    to_DR(qD_R),
    to_DR(c_eq[1]),
    to_DR(d_eq[1]),
    tD * Hbasic - 1,
)
G_leading_zero = leading_zero.groebner_basis(
    algorithm="singular:slimgb"
)
assert list(G_leading_zero) == [DR(1)]
# The coefficient-zero subchart of the now-linear qC relation is included.
linear_zero = leading_zero + DR.ideal(to_DR(M_R), to_DR(N_R))
assert list(
    linear_zero.groebner_basis(algorithm="singular:slimgb")
) == [DR(1)]

# A second ordinary terminal appears after the first qD pivot: cd=w^2.
# It is not a parent unit and must be charted separately.  Work in the
# original four-equation system and invert both Hbasic and L.
incidence_branch = DR.ideal(
    to_DR(qC_R),
    to_DR(qD_R),
    to_DR(c_eq[1]),
    to_DR(d_eq[1]),
    cD * dD - wD**2,
    tD
    * Hbasic
    * (cD - 2)
    * (2 * cD - 1)
    * (dD - 2)
    * (2 * dD - 1)
    * to_DR(L_R)
    - 1,
)
assert list(
    incidence_branch.groebner_basis(algorithm="singular:slimgb")
) == [DR(1)]

# Compact d=w^2/c form used by the independent Singular/Wolfram replays.
TI = PolynomialRing(QQ, names=("b", "c", "w"), order="degrevlex")
bI, cI, wI = TI.gens()
KI = TI.fraction_field()
incidence_substitution = R.hom([bI, cI, wI**2 / cI, wI], KI)


def incidence_factors(value):
    cleared = TI(incidence_substitution(value).numerator())
    return list(cleared.factor())


qC_incidence_factors = incidence_factors(qC_R)
qD_incidence_factors = incidence_factors(qD_R)
assert [(str(h), int(e)) for h, e in qC_incidence_factors[:-1]] == [
    ("w - 1", 1),
    ("c - 1", 1),
    ("c + 1", 1),
    ("2*b - 1", 1),
    ("w^2 - 2*c", 1),
    ("2*w^2 - c", 1),
]
assert [(str(h), int(e)) for h, e in qD_incidence_factors[:-1]] == [
    ("w - 1", 1),
    ("c - 2", 1),
    ("2*c - 1", 1),
    ("2*b - 1", 1),
    ("w^2 - c", 1),
    ("w^2 + c", 1),
]
qC_incidence = qC_incidence_factors[-1][0]
qD_incidence = qD_incidence_factors[-1][0]
L_incidence_factors = incidence_factors(L_R)
ell_incidence = L_incidence_factors[-1][0]
assert metric(qC_incidence)["sha256"] == (
    "14d979e5e87e8c63e28417bef8ca2bfa5278cde9fb2004f2ca0e0d6ac87f4589"
)
assert metric(qD_incidence)["sha256"] == (
    "dcff91b87a60d0f9ae50f39b549602cd13d7b3176b9a1a88fe1b308e2ef2dc02"
)
assert metric(ell_incidence)["sha256"] == (
    "c245ad66f003f08ab8dd7d4ac6bf1b8ff501768dfb55954faa47180922a70388"
)
incidence_locals = {
    "b": bI,
    "c": cI,
    "w": wI,
    **{"c" + str(k): cI**k for k in range(2, 5)},
    **{"w" + str(k): wI**k for k in range(2, 6)},
}
assert TI(sage_eval(
    singular_expression("qc"), locals=incidence_locals
)) == qC_incidence
assert TI(sage_eval(
    singular_expression("qd"), locals=incidence_locals
)) == qD_incidence
assert TI(sage_eval(
    singular_expression("ell"), locals=incidence_locals
)) == ell_incidence
e1_incidence = (
    4 * cI * wI**3
    - cI * wI**2
    - 2 * cI**2 * wI
    - 2 * wI**3
    + 2 * cI**2
    + 2 * wI**2
    + cI * wI
    - 4 * cI
)
e2_incidence = (
    cI * wI**3
    - 4 * cI * wI**2
    - 2 * cI**2 * wI
    - 2 * wI**3
    + 2 * cI**2
    + 2 * wI**2
    + 4 * cI * wI
    - cI
)
arec_incidence = (
    5 * cI * wI**2 - 4 * cI**2 - 4 * wI**2 + 5 * cI
)
hmiss_incidence = (
    bI
    * cI
    * wI
    * e1_incidence
    * e2_incidence
    * (bI - 1)
    * (bI + 1)
    * (cI - 1)
    * (cI + 1)
    * (wI**2 - cI)
    * (wI**2 + cI)
    * (wI - 1)
    * (wI + 1)
    * arec_incidence
    * (wI**2 - 1)
    * (bI - 2)
    * (2 * bI - 1)
    * (cI**2 - wI**2)
    * (cI - 2)
    * (2 * cI - 1)
    * (wI**2 - 2 * cI)
    * (2 * wI**2 - cI)
    * ell_incidence
)
incidence_locals.update({
    "ell": ell_incidence,
    "e1": e1_incidence,
    "e2": e2_incidence,
    "arec": arec_incidence,
})
assert TI(sage_eval(
    singular_expression("hmiss"), locals=incidence_locals
)) == hmiss_incidence

# L != 0: reduce the other three equations in K0[b]/(qC).
S = PolynomialRing(QQ, names=("c", "d", "w"), order="degrevlex")
cS, dS, wS = S.gens()
K0 = S.fraction_field()
PB = PolynomialRing(K0, "beta")
beta = PB.gen()
to_PB = R.hom([beta, cS, dS, wS], PB)
qC = PB(to_PB(qC_R)).monic()


def reduce_beta(value):
    return PB(to_PB(value)).mod(qC)


remainders = [
    reduce_beta(qD_R),
    reduce_beta(c_eq[1]),
    reduce_beta(d_eq[1]),
]
assert [value.degree() for value in remainders] == [1, 1, 1]
pivot_A, pivot_B = remainders[0][0], remainders[0][1]


def primitive_S_numerator(value):
    value = S(value.numerator())
    value = S(value / value.content())
    return -value if value.leading_coefficient() < 0 else value


def compatibility(value):
    return primitive_S_numerator(
        value[0] * pivot_B - value[1] * pivot_A
    )


b_solution = -pivot_A / pivot_B
q_terminal = primitive_S_numerator(qC(b_solution))
slice_terminal = [compatibility(value) for value in remainders[1:]]


def largest_nondeclared_factor(value):
    declared = {
        "c", "d", "w", "c - 1", "c + 1", "d - 1", "d + 1",
        "w - 1", "w + 1", "c - d", "-c + d", "c*d - 1",
        "5*c*d - 4*c - 4*d + 5",
        "c*d*w - 4*c*d - 2*c*w - 2*d*w + 2*c + 2*d + 4*w - 1",
    }
    factors = [
        h for h, _ in value.factor()
        if str(h) not in declared and str(-h) not in declared
    ]
    assert factors
    return max(factors, key=lambda h: h.total_degree())


# Assert the complete terminal factorization before selecting the retained
# component.  The two parent units and w=1 are discharged by Hbasic; the
# nonunit incidence factor cd=w^2 was deleted above.
A_S = 5 * cS * dS - 4 * cS - 4 * dS + 5
q_factorization_object = q_terminal.factor()
q_factorization = list(q_factorization_object)
assert [(str(h), int(e)) for h, e in q_factorization[:-1]] == [
    ("w - 1", 2),
    ("-c*d + w^2", 1),
    ("c*d - 1", 1),
    ("5*c*d - 4*c - 4*d + 5", 2),
]
assert len(q_factorization) == 5
q_essential = q_factorization[-1][0]
assert q_factorization[-1][1] == 1
assert q_terminal == (
    q_factorization_object.unit()
    * (wS - 1) ** 2
    * (wS**2 - cS * dS)
    * (cS * dS - 1)
    * A_S**2
    * q_essential
)
slice_essential = [
    largest_nondeclared_factor(value) for value in slice_terminal
]
swap = S.hom([dS, cS, wS], S)
assert swap(slice_essential[0]) == slice_essential[1]

# Symmetric coordinates s=c+d, p=cd.  The swap pair A+cB and A+dB
# becomes A=B=0 because c-d is a named unit.
SP = PolynomialRing(QQ, names=("s", "p", "w"), order="degrevlex")
sP, pP, wP = SP.gens()
KP = SP.fraction_field()
PC = PolynomialRing(KP, "chi")
chi = PC.gen()
to_PC = S.hom([chi, sP - chi, wP], PC)
c_relation = chi**2 - sP * chi + pP


def c_pair(value):
    remainder = PC(to_PC(value)).mod(c_relation)
    assert remainder.degree() <= 1
    return SP(remainder[0]), SP(remainder[1])


q_pair = c_pair(q_essential)
slice_pair = c_pair(slice_essential[0])
assert q_pair[1] == 0
Qsym, Asym, Bsym = q_pair[0], slice_pair[0], slice_pair[1]
assert metric(Qsym)["sha256"] == (
    "27345df84a941f9892be25b62fd5104a41392d14b40c003be36fab41b9f020e8"
)
assert metric(Asym)["sha256"] == (
    "720eec95a329975e0df2ea1533648af0dbb2254f726b11131acc090e1386d140"
)
assert metric(Bsym)["sha256"] == (
    "412b6a1290d0b0cafb5795b6591c15b94a1f7aefedd641b1fd0d6abcad7c43c6"
)
symmetric_locals = {
    "s": sP,
    "p": pP,
    "w": wP,
    **{"s" + str(k): sP**k for k in range(2, 6)},
    **{"p" + str(k): pP**k for k in range(2, 7)},
    **{"w" + str(k): wP**k for k in range(2, 5)},
}
assert SP(sage_eval(
    singular_expression("Q"), locals=symmetric_locals
)) == Qsym
assert SP(sage_eval(
    singular_expression("A"), locals=symmetric_locals
)) == Asym
assert SP(sage_eval(
    singular_expression("B"), locals=symmetric_locals
)) == Bsym

SF = PolynomialRing(F, names=("s", "p", "w"), order="degrevlex")
sF, pF, wF = SF.gens()


def SP_to_SF(value):
    return sum(
        F(coefficient)
        * sF**monomial[0]
        * pF**monomial[1]
        * wF**monomial[2]
        for monomial, coefficient in SP(value).dict().items()
    )


qF, aF, bF = map(SP_to_SF, (Qsym, Asym, Bsym))
named_units = {
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
    "reconstruction": 5 * pF - 4 * sF + 5,
}
Hsym = prod(named_units.values())
assert SF(sage_eval(
    singular_expression("H"),
    locals={
        "s": sF,
        "p": pF,
        "w": wF,
        **{"s" + str(k): sF**k for k in range(2, 6)},
        **{"p" + str(k): pF**k for k in range(2, 7)},
        **{"w" + str(k): wF**k for k in range(2, 5)},
    },
)) == Hsym
SL = PolynomialRing(
    F, names=("t", "s", "p", "w"), order="degrevlex"
)
tL, sL, pL, wL = SL.gens()
lift_sym = SF.hom([sL, pL, wL], SL)
support_ideal = SL.ideal(
    lift_sym(qF),
    lift_sym(aF),
    lift_sym(bF),
    tL * lift_sym(Hsym) - 1,
)
G_support = support_ideal.groebner_basis(algorithm="singular:slimgb")
assert support_ideal.dimension() == 1
assert support_ideal.reduce((pL + wL) ** 2) == 0
assert support_ideal.reduce((5 * sL + 4 * wL - 4) ** 2) == 0

# Ordinary first-pivot chart: retain the ordered root c and invert the
# actual qD remainder coefficient and every introduced denominator.
O = PolynomialRing(
    F, names=("t", "c", "s", "p", "w"), order="degrevlex"
)
tO, cO, sO, pO, wO = O.gens()
SCD = PolynomialRing(QQ, names=("c", "d", "w"))
cQ, dQ, wQ = SCD.gens()
pivot_B_fraction = SCD.fraction_field()(pivot_B)


def SCD_to_O(value):
    value = SCD(value)
    return sum(
        F(coefficient)
        * cO**monomial[0]
        * (sO - cO)**monomial[1]
        * wO**monomial[2]
        for monomial, coefficient in value.dict().items()
    )


sym_to_O = SF.hom([sO, pO, wO], O)
pivot_num_O = SCD_to_O(pivot_B_fraction.numerator())
pivot_den_O = SCD_to_O(pivot_B_fraction.denominator())
ordinary = O.ideal(
    sym_to_O(qF),
    sym_to_O(aF),
    sym_to_O(bF),
    cO**2 - sO * cO + pO,
    tO * sym_to_O(Hsym) * pivot_num_O * pivot_den_O - 1,
)
assert list(
    ordinary.groebner_basis(algorithm="singular:slimgb")
) == [O(1)]

# The first pivot vanishes on the only retained support.  Specialize to
# p=-w, s=4(1-w)/5 and exhaust the three possible linear remainders.
Fw = FunctionField(F, "omega")
omega = Fw.gen()
PX = PolynomialRing(Fw, "X")
X = PX.gen()
ss = Fw(4) * (1 - omega) / 5
Curve = PX.quotient(X**2 - ss * X - omega, "chi")
chiC = Curve.gen()
dC = Curve(ss) - chiC


def qq_to_F(value):
    value = QQ(value)
    return F(value.numerator()) / F(value.denominator())


def eval_S_poly(value):
    value = S(value)
    return sum(
        Curve(qq_to_F(coefficient))
        * chiC**monomial[0]
        * dC**monomial[1]
        * Curve(omega)**monomial[2]
        for monomial, coefficient in value.dict().items()
    )


def eval_K0(value):
    return eval_S_poly(value.numerator()) / eval_S_poly(value.denominator())


qC_curve = [eval_K0(qC[index]) for index in range(3)]
remainder_curve = [
    (eval_K0(value[0]), eval_K0(value[1])) for value in remainders
]
assert [
    (A == 0, B == 0) for A, B in remainder_curve
] == [(True, True), (False, False), (False, False)]
second_A, second_B = remainder_curve[1]
second_b = -second_A / second_B


def extension_pair(value):
    coefficients = value.list() + [Fw(0), Fw(0)]
    assert all(entry == 0 for entry in coefficients[2:])
    return coefficients[0], coefficients[1]


def cleared_pair(value):
    A, B = extension_pair(value)
    return (
        A.numerator() * B.denominator(),
        B.numerator() * A.denominator(),
        A.denominator() * B.denominator(),
    )


TF = PolynomialRing(F, names=("c", "w"), order="lex")
cT, wT = TF.gens()


def Fw_to_T(value):
    return sum(
        coefficient * wT**degree
        for degree, coefficient in value.dict().items()
    )


def curve_equation(value):
    A, B, denominator = cleared_pair(value)
    return (
        Fw_to_T(A) + cT * Fw_to_T(B),
        Fw_to_T(denominator),
    )


sT = F(4) * (1 - wT) / 5
curve_relation = cT**2 - sT * cT - wT
curve_named = (
    wT
    * (wT**2 - 1)
    * (sT**2 + 4 * wT)
    * (5 * (-wT) - 4 * sT + 5)
)
second_A_eq, second_A_den = curve_equation(second_A)
second_B_eq, second_B_den = curve_equation(second_B)
second_degenerate_localizer = curve_named * second_A_den * second_B_den
CU = PolynomialRing(F, names=("t", "c", "w"), order="degrevlex")
tU, cU, wU = CU.gens()
lift_curve = TF.hom([cU, wU], CU)
second_degenerate = CU.ideal(
    lift_curve(curve_relation),
    lift_curve(second_A_eq),
    lift_curve(second_B_eq),
    tU * lift_curve(second_degenerate_localizer) - 1,
)
assert list(
    second_degenerate.groebner_basis(algorithm="singular:slimgb")
) == [CU(1)]

qC_value = sum(qC_curve[index] * second_b**index for index in range(3))
third_value = remainder_curve[2][0] + remainder_curve[2][1] * second_b
qC_eq, qC_den = curve_equation(qC_value)
third_eq, third_den = curve_equation(third_value)
second_B_num_eq, second_B_num_den = curve_equation(second_B)
ordinary_curve_localizer = (
    curve_named
    * qC_den
    * third_den
    * second_B_num_den
    * second_B_num_eq
)
curve_ordinary = CU.ideal(
    lift_curve(curve_relation),
    lift_curve(qC_eq),
    lift_curve(third_eq),
    tU * lift_curve(ordinary_curve_localizer) - 1,
)
assert list(
    curve_ordinary.groebner_basis(algorithm="singular:slimgb")
) == [CU(1)]

result = {
    "schema": "kb-mca-v4-m2-diagonal-112-fixed-positive-balanced-sage-v1",
    "assignment": "{{2,1/2},{2,b}}",
    "assignment_quantifier": "SINGLE_NORMALIZED_REPRESENTATIVE",
    "prime": int(P0),
    "root_distribution_deleted": [int(1), int(1)],
    "leading_zero_unit": True,
    "linear_coefficient_zero_unit": True,
    "incidence_cd_eq_w2_unit": True,
    "incidence_compact_hashes": {
        "qC": metric(qC_incidence)["sha256"],
        "qD": metric(qD_incidence)["sha256"],
        "ell": metric(ell_incidence)["sha256"],
    },
    "q_terminal_factor_count": int(len(q_factorization)),
    "q_terminal_factor_unit": int(q_factorization_object.unit()),
    "support_dimension": int(support_ideal.dimension()),
    "support_radical_equations": ["p=-w", "5*s+4*w-4=0"],
    "first_pivot_ordinary_unit": True,
    "curve_first_pivot_zero": True,
    "second_pivot_coefficient_zero_unit": True,
    "second_pivot_ordinary_unit": True,
    "localizer_names": list(named_units),
}
encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
print(json.dumps(result, sort_keys=True))
print("payload_sha256=" + hashlib.sha256(encoded).hexdigest())
print("PASS REPRESENTATIVE_ONLY")
