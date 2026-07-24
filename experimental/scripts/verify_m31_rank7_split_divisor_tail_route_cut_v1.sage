#!/usr/bin/env sage
"""Independent Sage replay for the GF(31) full-gcd prefix-fiber fixture.

This is a small-field exact control.  It is not a lift to the deployed
Mersenne-31 row.
"""

from itertools import combinations
import hashlib
import json


F = GF(31)
R.<X> = PolynomialRing(F)


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def locator(roots):
    result = R.one()
    for root in roots:
        result *= X - F(root)
    return result


P_ROOTS = tuple(range(8))
L_ROOTS = tuple(range(8, 31))
RESTORER_ROOTS = (8, 9, 10, 11, 12, 13, 28, 30)

P = locator(P_ROOTS)
L = locator(L_ROOTS)
M = P * L

require(P.gcd(L) == 1, "P and L coprime")
require(P.degree() == 8 and L.degree() == 23, "split degrees")
require(sum(P_ROOTS) % 31 == 28, "P root sum")

tail_subsets = [
    roots
    for roots in combinations(L_ROOTS, 7)
    if sum(roots) % 31 == 28
]
require(len(tail_subsets) == 7864, "prefix-fiber cardinality")

tail_messages = []
for roots in tail_subsets:
    H = locator(roots)
    f = P - X * H
    require(f.degree() < 7, "tail message degree")
    require(P.gcd(f).monic() == X, "tail planted gcd")
    require(L.gcd(P - f).monic() == H, "tail evaluation gcd")
    require(M.gcd(P - f).monic() == X * H, "tail full gcd")
    tail_messages.append(f)

require(len(set(tail_messages)) == 7864, "tail messages distinct")

H0 = locator(RESTORER_ROOTS)
f0 = P - H0
require(sum(RESTORER_ROOTS) % 31 == 28, "restorer root sum")
require(f0.degree() < 7, "restorer message degree")
require(P.gcd(f0) == 1, "restorer planted gcd")
require(L.gcd(P - f0).monic() == H0, "restorer evaluation gcd")
require(M.gcd(P - f0).monic() == H0, "restorer full gcd")
require(f0 not in set(tail_messages), "restorer distinct")

family = tail_messages + [f0]
coefficient_matrix = matrix(
    F,
    [[f[index] for index in range(7)] for f in family],
)
require(coefficient_matrix.rank() == 7, "exact linear rank")
require(
    all(any(f(F(root)) != 0 for f in family) for root in P_ROOTS),
    "no common zero on P",
)

# Every tail recovers G=P/X, while the restorer recovers G=P.  Hence the
# denominator lcm is exactly P.
G_tail = P // X
G_restorer = P
require(lcm(G_tail, G_restorer).monic() == P, "master lcm restored")

# Negative control: changing the final restorer root from 30 to 29 breaks
# the shared one-coefficient prefix and therefore the degree gate.
bad_restorer = locator((8, 9, 10, 11, 12, 13, 28, 29))
require((P - bad_restorer).degree() == 7, "restorer mutation rejected")

record = {
    "schema": "m31-rank7-split-divisor-tail-gf31-sage-replay-v1",
    "field_prime": int(31),
    "tail_count": int(len(tail_messages)),
    "restorer_count": int(1),
    "total_list_size": int(len(family)),
    "deficit_histogram": {"0": int(1), "1": int(len(tail_messages))},
    "linear_rank": int(coefficient_matrix.rank()),
    "agreement": int(8),
    "message_dimension": int(7),
    "every_full_gcd_exact": True,
    "master_lcm_restored": True,
    "no_common_zero_on_P": True,
    "mutation_rejected": True,
    "scope": "EXACT_GF31_SOURCE_FIXTURE_NOT_DEPLOYED_M31",
}
encoded = json.dumps(
    record, sort_keys=True, separators=(",", ":"), ensure_ascii=True
).encode("ascii")
record["payload_sha256"] = hashlib.sha256(encoded).hexdigest()
print(json.dumps(record, sort_keys=True, separators=(",", ":")))
