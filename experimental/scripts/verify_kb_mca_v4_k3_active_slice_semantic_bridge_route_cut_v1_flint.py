#!/usr/bin/env python3
"""Independent python-flint replay of the K3 carrier countermodel."""

import hashlib
import json

from flint import fmpz, fmpz_mod_poly_ctx


P = 2_130_706_433
N = 2_097_152
ZETA = 1_213_133_211

SELECTED = [
    (106253, 2130600181), (1369722, 2129336712),
    (3779040, 2126927394), (8509390, 2122197044),
    (10074554, 2120631880), (10557358, 2120149076),
    (12609353, 2118097081), (14292086, 2116414348),
    (14535750, 2116170684), (15465656, 2115240778),
    (15916705, 2114789729), (16063573, 2114642861),
    (17060445, 2113645989), (18308266, 2112398168),
    (18560217, 2112146217), (19146956, 2111559478),
    (23803083, 2106903351), (24600315, 2106106119),
    (24695656, 2106010778), (25420300, 2105286134),
    (26886517, 2103819917), (32424981, 2098281453),
    (33558404, 2097148030), (33587235, 2097119199),
    (33762591, 2096943843), (33877430, 2096829004),
    (34423271, 2096283163), (35880750, 2094825684),
    (37630638, 2093075796), (37955085, 2092751349),
    (38255910, 2092450524), (38823503, 2091882931),
    (41058570, 2089647864), (41999211, 2088707223),
    (42650444, 2088055990), (42971510, 2087734924),
]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def canonical_digest(coefficients):
    raw = json.dumps(
        [int(c) for c in coefficients], separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


require(pow(ZETA, N, P) == 1 and pow(ZETA, N // 2, P) == P - 1,
        "exact carrier generator order")
roots = [x for pair in SELECTED for x in pair]
require(len(set(roots)) == 72, "selected roots distinct")
require(all(pow(x, N, P) == 1 for x in roots), "selected roots in carrier")
require(all((1 - x) % P == y for x, y in SELECTED), "tau pairs")
require(pow(1, N, P) == 1 and pow(0, N, P) != 1, "literal carrier witness")

R = fmpz_mod_poly_ctx(P)
T = R.gen()
h = T * (1 - T)
outer_values = [(x * (1 - x)) % P for x, _ in SELECTED]
require(len(set(outer_values)) == 36, "outer values distinct")

Y = T
Pout = R.one()
Qout = R.one()
for value in outer_values[:30]:
    Pout *= Y - value
for value in outer_values[30:]:
    Qout *= Y - value

V = Pout.compose(h)
A = Qout.compose(h)
direct_V = R.one()
direct_A = R.one()
for x, y in SELECTED[:30]:
    direct_V *= (T - x) * (T - y)
for x, y in SELECTED[30:]:
    direct_A *= (T - x) * (T - y)

require(V == direct_V and A == direct_A, "complete-fiber products")
require(V.degree() == 60 and V.is_monic(), "V degree/monic")
require(A.degree() == 12 and A.is_monic(), "A degree/monic")
require(V.is_squarefree() and A.is_squarefree(), "squarefree")
require(V.gcd(A) == R.one(), "coprime")
require(V * A**5 == Pout.compose(h) * Qout.compose(h)**5,
        "rational composition")
require(h.compose(1 - T) == h, "deck invariance")

# g(T)=T-1/2, so g*tau*g^-1=-T.  Negation preserves the even-order D.
half = pow(2, P - 2, P)
conjugated = (1 - (T + half)) - half
require(conjugated == -T, "conjugacy disclosure")
require(pow(ZETA, N // 2, P) == P - 1, "minus one in D")

digests = {
    "outer_active": canonical_digest(Pout.coeffs()),
    "outer_source": canonical_digest(Qout.coeffs()),
    "V_act": canonical_digest(V.coeffs()),
    "A": canonical_digest(A.coeffs()),
}

print(json.dumps({
    "status": "FLINT_PASS_DIRECT_COORDINATE_ROUTE_CUT",
    "p": int(fmpz(P)),
    "carrier_order": N,
    "selected_fibers": len(SELECTED),
    "active_degree": V.degree(),
    "source_degree": A.degree(),
    "coefficient_digests": digests,
    "tau_preserves_D": False,
    "conjugated_negation_preserves_D": True,
    "actual_MCA_counterexample": False,
    "ledger_movement": 0,
}, sort_keys=True))
