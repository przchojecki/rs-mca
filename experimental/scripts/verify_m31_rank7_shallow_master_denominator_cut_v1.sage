#!/usr/bin/env sage
"""Independent Sage replay for the M31 rank-seven master cut."""

from itertools import combinations


N = ZZ(2)^21
K = ZZ(2)^20
A = ZZ(1_116_023)
R = N - A
W = A - K
L = ZZ(15_775_933)
TARGET = L - 1
Q_PROFILE = W + 1
D6_MIN = N - K + 6
T0_TURN = ZZ(1_177_354)


def need(condition, label):
    if not condition:
        raise RuntimeError(label)


def falling(value, length):
    return prod(value - offset for offset in range(length))


def affine_slice_cap(rank, degree):
    return binomial(R - degree + W + rank, rank) // binomial(W + rank, rank)


small_caps = {
    dimension: affine_slice_cap(dimension, W + dimension)
    for dimension in range(1, 6)
}
need(
    small_caps == {
        1: 14,
        2: 211,
        3: 3_077,
        4: 44_769,
        5: 651_202,
    },
    "small fixed-G caps",
)
proper_max = affine_slice_cap(6, W + 6)
need(proper_max == 9_471_941, "proper fixed-G maximum")


def full_slice_cap(union_size):
    return affine_slice_cap(7, union_size)


need(full_slice_cap(328_677) == 15_776_081, "fixed-G adjacent failure")
need(full_slice_cap(328_678) == 15_775_927, "fixed-G first exclusion")
need(full_slice_cap(354_972) == 12_158_497, "fixed-G residual endpoint")


def affine_fiber_cap(dimension):
    return binomial(N - K + dimension, dimension) // binomial(
        W + dimension, dimension
    )


def raw_q6_cap(union_size, fiber_dimension):
    fixed = L * union_size * prod(
        W + index for index in range(fiber_dimension + 1, 6)
    )
    numerator = affine_fiber_cap(fiber_dimension) * falling(
        R + union_size, 7 - fiber_dimension
    )
    return numerator // fixed - (W + 6)


def q6_envelope(union_size):
    raw = min(raw_q6_cap(union_size, k) for k in range(1, 6))
    return min(raw, union_size - W - 7)


def pi_profile(d6, layer):
    return (d6 - R + layer) * prod(W + index + layer for index in range(1, 6))


def old_support(d6):
    return QQ(falling(d6, 6)) / pi_profile(d6, 0)


def old_layer(d6, union_size):
    layer = R + union_size - d6
    return QQ(falling(d6, 7)) / (Q_PROFILE * pi_profile(d6, layer))


def harmonic_layer(d6, union_size):
    layer = R + union_size - d6
    need(1 <= layer <= Q_PROFILE, "harmonic layer")
    return QQ(falling(d6, 6) * (R + union_size - Q_PROFILE - 6)) / (
        Q_PROFILE * pi_profile(d6, layer)
    )


def old_majorant(union_size, d6_max):
    bounds = [
        old_support(D6_MIN)
        + old_layer(min(T0_TURN, d6_max), union_size)
    ]
    if d6_max >= T0_TURN:
        bounds.append(old_support(d6_max) + old_layer(d6_max, union_size))
    return max(bounds)


def refined_majorant(union_size):
    d6_max = D6_MIN + q6_envelope(union_size)
    first_harmonic = R + union_size - Q_PROFILE
    bounds = []
    old_max = min(d6_max, first_harmonic - 1)
    if old_max >= D6_MIN:
        bounds.append(old_majorant(union_size, old_max))
    harmonic_min = max(D6_MIN, first_harmonic)
    if harmonic_min <= d6_max:
        if harmonic_min <= T0_TURN:
            low_endpoint = min(T0_TURN, d6_max)
            bounds.append(
                old_support(harmonic_min)
                + harmonic_layer(low_endpoint, union_size)
            )
        if max(harmonic_min, T0_TURN) <= d6_max:
            bounds.append(
                old_support(d6_max) + harmonic_layer(d6_max, union_size)
            )
    need(bounds, "nonempty refined majorant")
    return max(bounds), d6_max, R + union_size - d6_max


paid = []
records = {}
for union_size in range(354_972, 354_999):
    bound, d6_max, layer = refined_majorant(ZZ(union_size))
    floor_bound = floor(bound)
    if floor_bound <= TARGET:
        paid.append(union_size)
    if union_size in (354_972, 354_973, 354_998):
        records[union_size] = (floor_bound, d6_max, layer)

need(paid == list(range(354_973, 354_999)), "harmonic paid interval")
need(
    records == {
        354_972: (15_776_055, 1_270_586, 65_515),
        354_973: (15_775_843, 1_270_586, 65_516),
        354_998: (15_768_132, 1_270_576, 65_551),
    },
    "harmonic threshold records",
)


# Independent exact convexity controls.  The second derivative identity
# f''=f*((sum 1/(a_i+z))^2+sum 1/(a_i+z)^2) is strictly positive.
S.<z> = PolynomialRing(QQ)
for a_values in ((1,), (1, 3), (2, 4, 7), (3, 5, 8, 11)):
    Pz = prod(z + a for a in a_values)
    reciprocal = 1 / Pz
    second = reciprocal * (
        sum(1 / (z + a) for a in a_values)^2
        + sum(1 / (z + a)^2 for a in a_values)
    )
    need(
        (reciprocal.derivative(2) - second).numerator() == 0,
        "reciprocal second derivative identity",
    )
    for e in range(1, 7):
        for Q in range(e, 9):
            p0 = prod(ZZ(a) for a in a_values)
            pe = prod(ZZ(a + e) for a in a_values)
            x_dual = QQ(1) / (e * p0) - QQ(Q - e) / (e * Q * pe)
            y_dual = QQ(1) / (Q * pe)
            need(x_dual >= 0 and y_dual > 0, "dual signs")
            for b in range(e + 1):
                pb = prod(ZZ(a + b) for a in a_values)
                lhs = (
                    x_dual * (e - b) * pb
                    + y_dual * (Q - e + b) * pb
                )
                need(lhs >= 1, "dual feasibility")


# Exact GF(13) master-denominator orientation control.  With V=H0=1,
# choosing equal-degree split G|A0 and H|L0 and b=G-H realizes the canonical
# full-gcd relation.  The family varies G and its exact lcm is A0.
F = GF(13)
PR.<x> = PolynomialRing(F)
s0_roots = [F(value) for value in range(0, 6)]
e0_roots = [F(value) for value in range(6, 11)]
A0 = prod(x - alpha for alpha in s0_roots)
L0 = prod(x - alpha for alpha in e0_roots)
V = PR(1)
H0 = PR(1)


def locator(roots):
    return prod(x - alpha for alpha in roots)


pairs = []
for degree in range(1, 6):
    for s_indices in combinations(range(len(s0_roots)), degree):
        G = locator(s0_roots[index] for index in s_indices)
        for e_indices in combinations(range(len(e0_roots)), degree):
            H = locator(e0_roots[index] for index in e_indices)
            b = G - H
            need(b != 0 and b.degree() < degree, "toy degree gate")
            need(gcd(b, G) == 1, "toy coprimality")
            need(gcd(L0, G - b * V).monic() == H.monic(), "toy full gcd")
            pairs.append((G.monic(), b, H.monic()))

P_master = lcm([entry[0] for entry in pairs])
need(P_master.monic() == A0.monic(), "toy exact lcm")
g_master = P_master.degree()
M_master = P_master * L0
Y_master = P_master * H0
f_values = []
codewords = []

for G, b, H in pairs:
    Q = (P_master // G).monic()
    f = Q * b
    need(f.degree() < g_master, "toy master degree")
    need(
        gcd(M_master, Y_master - f).monic() == (Q * H).monic(),
        "toy master gcd",
    )
    Q_back = gcd(P_master, f).monic()
    G_back = (P_master // Q_back).monic()
    b_back = f // Q_back
    need(G_back == G and b_back == b, "toy inverse")
    f_values.append(f)
    codewords.append((A0 // G) * b)

need(len(set(codewords)) == len(pairs), "toy canonical distinctness")
for alpha in s0_roots:
    need(any(f(alpha) != 0 for f in f_values), "toy no common planted zero")

coefficient_rows = [
    [f[index] for index in range(g_master)]
    for f in f_values
]
toy_rank = Matrix(F, coefficient_rows).rank()
need(toy_rank == g_master, "toy global rank")

slice_ranks = []
for G in sorted(set(entry[0] for entry in pairs), key=str):
    slice_rows = []
    for pair_index, (G_i, _b_i, _H_i) in enumerate(pairs):
        if G_i == G:
            f = f_values[pair_index]
            slice_rows.append([f[index] for index in range(g_master)])
    slice_rank = Matrix(F, slice_rows).rank()
    need(slice_rank <= toy_rank - 1, "toy proper-slice rank loss")
    slice_ranks.append(slice_rank)


print("M31_RANK7_SHALLOW_MASTER_DENOMINATOR_CUT_SAGE_V1")
print("proper_slice_maximum=%s" % proper_max)
print("full_slice_transition=328677:15776081,328678:15775927")
print("harmonic_paid_range=354973..354998")
print("harmonic_transition=354972:15776055,354973:15775843")
print("toy_pairs=%s" % len(pairs))
print("toy_global_rank=%s" % toy_rank)
print("toy_max_proper_slice_rank=%s" % max(slice_ranks))
print("PASS")
