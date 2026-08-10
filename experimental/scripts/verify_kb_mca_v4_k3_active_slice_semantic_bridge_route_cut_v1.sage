#!/usr/bin/env sage
"""Independent Sage replay of the direct-coordinate carrier countermodel."""

import json


P = 2130706433
N = 2^21
ZETA = 1213133211


def require(condition, message):
    if not condition:
        raise AssertionError(message)


SELECTED = [
    (106253, 2130600181),
    (1369722, 2129336712),
    (3779040, 2126927394),
    (8509390, 2122197044),
    (10074554, 2120631880),
    (10557358, 2120149076),
    (12609353, 2118097081),
    (14292086, 2116414348),
    (14535750, 2116170684),
    (15465656, 2115240778),
    (15916705, 2114789729),
    (16063573, 2114642861),
    (17060445, 2113645989),
    (18308266, 2112398168),
    (18560217, 2112146217),
    (19146956, 2111559478),
    (23803083, 2106903351),
    (24600315, 2106106119),
    (24695656, 2106010778),
    (25420300, 2105286134),
    (26886517, 2103819917),
    (32424981, 2098281453),
    (33558404, 2097148030),
    (33587235, 2097119199),
    (33762591, 2096943843),
    (33877430, 2096829004),
    (34423271, 2096283163),
    (35880750, 2094825684),
    (37630638, 2093075796),
    (37955085, 2092751349),
    (38255910, 2092450524),
    (38823503, 2091882931),
    (41058570, 2089647864),
    (41999211, 2088707223),
    (42650444, 2088055990),
    (42971510, 2087734924),
]


F = GF(P)
require(F.cardinality() == P and P.is_prime(), "base field")
zeta = F(ZETA)
require(zeta.multiplicative_order() == N, "carrier generator order")

D = set()
x = F(1)
for _ in range(N):
    D.add(ZZ(x))
    x *= zeta
require(x == 1 and len(D) == N, "deployed carrier")

pairs = []
for x0 in sorted(D):
    y0 = ZZ((F(1) - F(x0)))
    if x0 < y0 and y0 in D:
        pairs.append((x0, y0))
require(len(pairs) == 1071, "carrier tau-pair census")
require(pairs[:36] == SELECTED, "canonical selected pairs")

R.<T> = PolynomialRing(F)
h = T * (1 - T)
tau_T = 1 - T
require(tau_T(tau_T) == T, "tau order two")
require(h(tau_T) == h, "h invariant")

outer_values = [F(x0) * (1 - F(x0)) for x0, _ in SELECTED]
require(len(set(outer_values)) == 36, "outer values distinct")
active_values = outer_values[:30]
source_values = outer_values[30:]
require(set(active_values).isdisjoint(source_values), "active/source disjoint")

V = prod(h - value for value in active_values)
A = prod(h - value for value in source_values)
direct_V = prod((T - F(x0)) * (T - F(y0)) for x0, y0 in SELECTED[:30])
direct_A = prod((T - F(x0)) * (T - F(y0)) for x0, y0 in SELECTED[30:])

require(V == direct_V and A == direct_A, "complete-fiber products")
require(V.degree() == 60 and V.is_monic(), "V degree/monic")
require(A.degree() == 12 and A.is_monic(), "A degree/monic")
require(V.is_squarefree() and A.is_squarefree(), "squarefree")
require(gcd(V, A) == 1, "coprime")
require(all(locator.degree() == 2 for locator in [h - v for v in source_values]),
        "source locators in W=<1,h>")

RY.<Y> = PolynomialRing(F)
Pout = prod(Y - value for value in active_values)
Qout = prod(Y - value for value in source_values)
require(Pout(h) == V and Qout(h) == A, "outer composition")
require(V * A^5 == Pout(h) * Qout(h)^5, "rational composition cross-product")

# Direct carrier failure.
require(ZZ(1) in D and ZZ(0) not in D, "carrier witness membership")
require(ZZ(F(1) - F(1)) == 0, "tau(1)=0")
require(F(N) != 0, "root-polynomial coefficient contradiction")

# Scope-preserving conjugacy disclosure: g=t-1/2 sends tau to -t.
half = F(1) / F(2)
U = T + half                     # g^{-1}(T)
conjugated = (1 - U) - half      # g(tau(g^{-1}(T)))
require(conjugated == -T, "conjugacy to negation")
require(F(-1) in [zeta^(N//2)], "minus one in D")
require({ZZ(-F(v)) for v in D} == D, "negation preserves D")

print(json.dumps({
    "status": "SAGE_PASS_DIRECT_COORDINATE_ROUTE_CUT",
    "p": int(P),
    "carrier_order": int(N),
    "tau_pairs": int(len(pairs)),
    "selected_fibers": int(len(SELECTED)),
    "active_degree": int(V.degree()),
    "source_degree": int(A.degree()),
    "tau_preserves_D": False,
    "conjugated_negation_preserves_D": True,
    "actual_MCA_counterexample": False,
    "ledger_movement": int(0),
}, sort_keys=True))
