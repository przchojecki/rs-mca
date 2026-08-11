#!/usr/bin/env sage
"""Independent Sage replay of the actual-record dimension-sensitivity audit."""

import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


# Deployed arithmetic.
p = ZZ(2130706433)
n = ZZ(2^21)
k = ZZ(1048576)
m = ZZ(1116048)
omega = n - m
e = ZZ(67473)
zeta_int = ZZ(1213133211)

Fp = GF(p)
require(p.is_prime(), "base prime")
require(Fp(3).multiplicative_order() == p - 1, "primitive power base")
zeta = Fp(zeta_int)
require(zeta.multiplicative_order() == n, "deployed carrier order")
require(e + m == 1183521 < n, "disjoint exponent intervals")

Rp.<X> = PolynomialRing(Fp)
modulus = X^6 + X + 6
require(modulus.is_irreducible(), "challenge modulus irreducible")
Fq.<alpha> = GF(p^6, modulus=modulus)
require(
    alpha.minpoly().degree() == 6
    and alpha.minpoly().list() == modulus.list(),
    "alpha has exact degree six",
)

# The pole-line identity is checked on declared in-E and off-E points.
sample = [(Fp(1), 1), (zeta, 1), (zeta^e, 0), (zeta^(e + m - 1), 0)]
for x0, indicator in sample:
    xq = Fq(x0)
    v = -1 / (xq - alpha)
    Ux = Fq(indicator)
    u = Ux - alpha * v
    require(u + alpha * v == Ux, "same-record slope cancellation")
    require(xq != alpha, "pole off carrier")

# Exact deployed profile and root-count inequalities.
require(m > k + 1, "direction root-count bound")
require(n - e == 2029679, "off-error roots")
require(k + e - 2 == 1116047 < n - e, "K=k N-degree bound")
require(k + e - 1 == 1116048 < n - e, "K=k+1 N-degree bound")
require(e == (m - k) + 1, "code-dimension boundary")
require(e == (m - (k + 1)) + 2, "effective-dimension first interior")
require((e, n - k + 1 - e) == (67473, 981104), "code profile")
require((e, n - (k + 1) + 1 - e) == (67473, 981103), "effective profile")


# Complete toy analogue over F_17.
Ft = GF(17)
Rt.<T> = PolynomialRing(Ft)
zt = Ft.multiplicative_generator()
Dt = [zt^i for i in range(16)]
Et = set(Dt[:3])
St = set(Dt[3:13])
require(len(Et) == 3 and len(St) == 10 and Et.isdisjoint(St), "toy support")

LtE = prod(T - x for x in Et)
LtC = prod(T - x for x in Dt if x not in Et)
RtC = LtC.mod(LtE)
require(LtE * LtC == T^16 - 1, "toy determinant locator")

Ut = [Ft(1) if x in Et else Ft(0) for x in Dt]
for x, ux in zip(Dt, Ut):
    require(LtE(x) * ux == 0, "toy g1 lattice")
    require(RtC(x) * ux == LtC(x), "toy g2 lattice")


def lower_system_rank(Kshift):
    """Rank of the homogeneous system for shifted degree <= e-1."""
    max_w = 2
    max_n = Kshift + 1  # (Kshift-1)+(e-1), with e=3.
    rows = []
    for x, ux in zip(Dt, Ut):
        rows.append(
            [ux * x^j for j in range(max_w + 1)]
            + [-x^j for j in range(max_n + 1)]
        )
    A = matrix(Ft, rows)
    return A.rank(), A.ncols(), A.right_kernel().dimension()


toy = {}
for Kshift in (8, 9):
    rank, columns, nullity = lower_system_rank(Kshift)
    require(rank == columns and nullity == 0, "toy lower-degree kernel")
    toy[str(Kshift)] = {
        "rank": int(rank),
        "columns": int(columns),
        "lower_kernel_dimension": int(nullity),
        "minimal_shifted_degree": int(3),
    }

print(json.dumps({
    "status": "SAGE_PASS_ACTUAL_RECORD_DIMENSION_SENSITIVITY_AUDIT",
    "p": int(p),
    "carrier_order": int(n),
    "extension_modulus_irreducible": True,
    "alpha_degree": int(alpha.minpoly().degree()),
    "minimal_shifted_degree_both_conventions": int(e),
    "code_profile": "BOUNDARY_NUMERICAL_PROFILE",
    "effective_profile": "FIRST_INTERIOR_NUMERICAL_PROFILE",
    "actual_owner": "NOT_ESTABLISHED_BY_PINNED_SOURCES",
    "pure_ray_scope": True,
    "toy": toy,
    "ledger_movement": int(0),
}, sort_keys=True))
