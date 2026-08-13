#!/usr/bin/env sage
"""Exact GF(17) same-record cancellation control for the common-core route cut."""

F = GF(17)
P.<X> = PolynomialRing(F)

D = [F(x) for x in [1, 9, 13, 15, 16, 8, 4, 2]]
gammas = [F(x) for x in [0, 1, 4, 7, 2]]
supports = [
    {F(x) for x in [1, 15, 16, 8, 4, 2]},
    {F(x) for x in [1, 9, 13, 15, 16, 8]},
    {F(x) for x in [1, 13, 15, 16, 4, 2]},
    {F(x) for x in [1, 9, 15, 16, 4, 2]},
    {F(x) for x in [1, 9, 13, 15, 8, 4]},
]
h = [
    P(0),
    P(0),
    P([9, 13, 8, 4]),
    P([3, 10, 14, 7]),
    P([11, 8, 9, 6]),
]
r0_values = [0, 16, 6, 0, 0, 0, 0, 0]
r1_values = [0, 1, 11, 0, 0, 0, 5, 12]
r0 = {x: F(v) for x, v in zip(D, r0_values)}
r1 = {x: F(v) for x, v in zip(D, r1_values)}


def interpolate(points, values):
    out = P(0)
    for i, xi in enumerate(points):
        basis = P(1)
        denom = F(1)
        for j, xj in enumerate(points):
            if i != j:
                basis *= X - xj
                denom *= xi - xj
        out += values[i] * basis / denom
    return out


for i, gamma in enumerate(gammas):
    maximal = {
        x for x in D if h[i](x) == r0[x] + gamma * r1[x]
    }
    assert maximal == supports[i]

core = set.intersection(*supports)
assert core == {F(1), F(15)}
G = prod(X - x for x in core)
assert G == X^2 + X + F(15)

core_list = sorted(core, key=int)
a0 = interpolate(core_list, [r0[x] for x in core_list])
a1 = interpolate(core_list, [r1[x] for x in core_list])
assert a0 == 0 and a1 == 0

Dprime = [x for x in D if x not in core]
r0p = {x: (r0[x] - a0(x)) / G(x) for x in Dprime}
r1p = {x: (r1[x] - a1(x)) / G(x) for x in Dprime}
hp = []

for i, gamma in enumerate(gammas):
    numerator = h[i] - a0 - gamma * a1
    quotient, remainder = numerator.quo_rem(G)
    assert remainder == 0
    assert quotient.degree() < 2 or quotient == 0
    hp.append(quotient)
    reduced_support = supports[i] - core
    maximal_reduced = {
        x for x in Dprime if quotient(x) == r0p[x] + gamma * r1p[x]
    }
    assert maximal_reduced == reduced_support
    assert len(reduced_support) == 4

    # A word on four points is in RS[4,2] iff its degree-<4 interpolant
    # actually has degree <2.  At least one coordinate word must fail.
    pts = sorted(reduced_support, key=int)
    p0 = interpolate(pts, [r0p[x] for x in pts])
    p1 = interpolate(pts, [r1p[x] for x in pts])
    assert not (p0.degree() < 2 and p1.degree() < 2)

    # Literal inverse on the identical explanation state.
    lifted = a0 + gamma * a1 + G * quotient
    assert lifted == h[i]

assert (len(Dprime), 2, 4) == (6, 2, 4)
assert (4 - 2, 6 - 2, 6 - 4) == (2, 4, 2)
assert (6 - 4, 8 - 4, 8 - 6) == (2, 4, 2)

print("PASS GF17 common-core cancellation")
print(f"core={sorted(map(int, core))} G={G}")
print("row=(8,4,6)->(6,2,4) slopes=5 same_support_noncontainment=True")
