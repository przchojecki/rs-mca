#!/usr/bin/env sage
"""Independent Sage replay of the guarded GF(11) core-owner collision."""

import itertools
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
manifest = json.loads((root / "experimental/data/certificates/kb-mca-v4-guarded-record-local-core-owner-route-cut-v1/manifest.json").read_text())
fixture = manifest["fixture"]
F = GF(fixture["field"])
R.<X> = PolynomialRing(F)
D = [F(x) for x in fixture["domain"]]
k = fixture["k"]
m = fixture["m"]
w = fixture["w"]
u = [F(x) for x in fixture["received_line"]["u"]]
v = [F(x) for x in fixture["received_line"]["v"]]


def interpolate(points, values):
    return R.lagrange_polynomial(list(zip(points, values)))


supports = {}
polys = {}
minima = []
for item in fixture["explanations"]:
    slope = F(item["slope"])
    poly = sum(F(c) * X^i for i, c in enumerate(item["coefficients"]))
    word = [a + slope * b for a, b in zip(u, v)]
    support = tuple(int(D[i]) for i in range(len(D)) if poly(D[i]) == word[i])
    assert support == tuple(item["maximal_support"])

    found = set()
    for seed in itertools.combinations(range(len(D)), k):
        candidate = interpolate([D[i] for i in seed], [word[i] for i in seed])
        if sum(candidate(x) == value for x, value in zip(D, word)) >= m:
            found.add(candidate)
    assert found == {poly}
    indices = [fixture["domain"].index(x) for x in support]
    up = interpolate([D[i] for i in indices], [u[i] for i in indices])
    vp = interpolate([D[i] for i in indices], [v[i] for i in indices])
    assert up.degree() >= k or vp.degree() >= k

    for s in range(6):
        matrix = Matrix(F, [
            [value * x^j for j in range(s + 1)]
            + [-x^j for j in range(s + k)]
            for x, value in zip(D, word)
        ])
        if matrix.rank() < matrix.ncols():
            minima.append(s)
            break
    assert minima[-1] == w + 1
    complement = [x for x in D if int(x) not in support]
    locator = prod(X - x for x in complement)
    numerator = locator * poly
    s_k = max(locator.degree(), numerator.degree() - (k - 1))
    assert s_k <= len(complement)
    supports[int(slope)] = set(support)
    polys[int(slope)] = poly

slopes = sorted(supports)
cores = []
for record in itertools.combinations(slopes, fixture["critical_order"]):
    core = set(fixture["domain"])
    for slope in record:
        core &= supports[slope]
    assert core
    cores.append(tuple(sorted(core)))
assert sorted(cores) == sorted([(8, 10), (10,), (10,), (10,), (5, 10), (10,), (10,)])
global_core = set(fixture["domain"])
for support in supports.values():
    global_core &= support
assert global_core == {10}

g0, g1 = slopes[0], slopes[1]
direction = (polys[g1] - polys[g0]) / F(g1 - g0)
assert any(polys[g] != polys[g0] + F(g - g0) * direction for g in slopes)

# Sharp root-count boundary for Theorem 4.2: degree three realizes four
# 3-wise-intersecting supports with empty total core; degree two cannot have
# the three required distinct off-diagonal roots.
F5 = GF(5)
R5.<Z> = PolynomialRing(F5)
labels = list(range(4))
sharp_supports = [set(labels) - {i} for i in labels]
assert not set.intersection(*sharp_supports)
assert all(set.intersection(*chosen) for chosen in itertools.combinations(sharp_supports, 3))
for i in labels:
    error = prod(Z - F5(j) for j in labels if j != i)
    assert error.degree() == 3
    assert error(F5(i)) != 0
    assert all(error(F5(j)) == 0 for j in labels if j != i)

# Degree-three analogue of the 31-overlap source-change factorization.
F7 = GF(7)
R7.<Z7> = PolynomialRing(F7)
overlap = [F7(0), F7(1), F7(2)]
overlap_locator = prod(Z7 - a for a in overlap)
base = [F7(1) + F7(4)*Z7 + F7(2)*Z7^3,
        F7(3) + Z7 + F7(6)*Z7^2]
direction = [F7(2), F7(5)]
changed = [base[i] + direction[i]*overlap_locator for i in range(2)]
assert all(changed[i](a) == base[i](a) for i in range(2) for a in overlap)
new_scalar = overlap_locator(F7(3))
assert new_scalar != 0
assert [changed[i](F7(3)) - base[i](F7(3)) for i in range(2)] == [new_scalar*d for d in direction]

R0 = 1048576
d0 = 67472
t0 = 981104
best_ray = (-1, -1)
for q in range(3, 1048577):
    n_short = R0 + q
    m_short = d0 + q
    cap = q - 1
    quotient, remainder = divmod(m_short, cap)
    xi = binomial(m_short, 2) - quotient*binomial(cap, 2) - binomial(remainder, 2)
    ray_bound = (n_short // q)*(t0 + 1) + 31*binomial(n_short, 2)//xi
    if ray_bound > best_ray[0]:
        best_ray = (ray_bound, q)
assert best_ray == (342921713716, 3)

lineray_caps = [binomial(981104 + a, a) for a in range(5)]
assert lineray_caps == [1, 981105, 481284001065,
                        157397034144292985, 38605872343809750481845]
assert lineray_caps[3] + 134975 <= 274980728111395087 < lineray_caps[4] + 134975
assert 274980728111395087 - 134975 - lineray_caps[3] == 117583693966967127

print("KB_MCA_V4_GUARDED_CORE_OWNER_SAGE_PASS slopes=7 records=7 d1=%s global_core=%s coherent_fence_sharp_degree=3 overlap_ray_scalar=%s guarded_ray_max=%s@q=%s lineray_last_paid_rank=3" % (minima, sorted(global_core), new_scalar, best_ray[0], best_ray[1]))
