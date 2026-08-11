#!/usr/bin/env sage
"""Independent Sage replay for the support-wise two-anchor repair."""

from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# Exact deployed arithmetic and the abstract actual-record construction.
n = Integer(2)^21
K = Integer(2)^20
m = Integer(1116048)
w = m - K
dmin = n - K + 1
require(w == 67472, "KoalaBear w")
require(2*w == 134944, "KoalaBear charge")
require(3*w == 202416 and 3*w < dmin, "KoalaBear distance guard")
require(dmin - 3*w == 846161, "KoalaBear distance margin")
require(n-w == 2029680 and n-w >= m, "common support")
require(m-1 >= K, "same-witness root guard")


# Exhaust the quotient by codeword-pair translations for RS[GF(7),6,3].
F = GF(7)
n0, K0, m0 = 6, 3, 4
w0 = m0 - K0
D = list(F)[:n0]
columns = [vector(F, [1, x, x^2]) for x in D]


def span_tuples(indices):
    if not indices:
        return {tuple(F(0) for _ in range(n0-K0))}
    result = set()
    for coeffs in product(F, repeat=len(indices)):
        value = vector(F, n0-K0)
        for coefficient, index in zip(coeffs, indices):
            value += coefficient * columns[index]
        result.add(tuple(value))
    return result


planes = [span_tuples(pair) for pair in combinations(range(n0), n0-m0)]
near = {tuple(F(0) for _ in range(n0-K0))}
for i in range(n0):
    near.update(span_tuples((i,)))

syndromes = [tuple(F(x) for x in values) for values in product(range(7), repeat=n0-K0)]
maximum = 0
pair_count = 0
for su in syndromes:
    vu = vector(F, su)
    for sv in syndromes:
        vv = vector(F, sv)
        pair_count += 1
        count = 0
        for z in F:
            word = tuple(vu + z*vv)
            if word not in near:
                continue
            bad = any(
                word in plane and not (su in plane and sv in plane)
                for plane in planes
            )
            count += Integer(bad)
        maximum = max(maximum, count)

require(pair_count == 7^6 == 117649, "toy syndrome-pair census")
require(maximum == 2*w0 == 2, "toy two-anchor maximum")


# A literal small common-support counterexample, using the same deployed shape.
# Coordinates 0 and 1 are E; slopes 0 and 1; the pair is zero off E.
u = vector(F, [0, -1, 0, 0, 0, 0])
v = vector(F, [1, 1, 0, 0, 0, 0])
common = [2, 3, 4, 5]
require(all(u[x] == 0 and v[x] == 0 for x in common), "toy common support")
for slope, endpoint in [(F(0), 0), (F(1), 1)]:
    S = [endpoint, 2, 3, 4]
    word = u + slope*v
    require(all(word[x] == 0 for x in S), "toy bad-slope explanation")
    require(sum(1 for x in S if v[x] == 0) >= K0, "toy noncontainment roots")
    require(v[endpoint] == 1, "toy noncontainment endpoint")

print("Sage support-wise two-anchor replay")
print("  KoalaBear charge:", 2*w)
print("  exhaustive toy syndrome pairs:", pair_count)
print("  exact toy maximum:", maximum)
print("RESULT: PASS")
