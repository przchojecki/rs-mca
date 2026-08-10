#!/usr/bin/env python3
"""Independent FLINT replay of the actual-record dimension-sensitivity audit."""

import hashlib
import json

from flint import fmpz, fmpz_mod_poly_ctx, nmod_mat


P = 2_130_706_433
N = 2_097_152
K = 1_048_576
M = 1_116_048
E = 67_473
ZETA = 1_213_133_211


def require(condition, message):
    if not condition:
        raise AssertionError(message)


require(pow(3, (P - 1) // 2, P) != 1, "generator 2-primary order")
require(pow(3, (P - 1) // 127, P) != 1, "generator 127-primary order")
require(pow(ZETA, N, P) == 1, "zeta^n")
require(pow(ZETA, N // 2, P) == P - 1, "exact carrier order")
require(E + M == 1_183_521 < N, "support intervals disjoint")
require(N - E > K + E - 1, "both root bounds")

R = fmpz_mod_poly_ctx(P)
X = R.gen()
modulus = X**6 + X + 6
require(modulus.is_irreducible(), "degree-six challenge modulus")

require(E == M - K + 1, "code boundary")
require(E == M - (K + 1) + 2, "effective first interior")
code_d2 = N - K + 1 - E
effective_d2 = N - (K + 1) + 1 - E
require((code_d2, effective_d2) == (981_104, 981_103), "row profiles")

# FLINT owns the exact huge binomial computation in this replay.
supports = fmpz.bin_uiui(N - E, M)
supports_int = int(supports)
raw = supports_int.to_bytes((supports_int.bit_length() + 7) // 8, "big")
require(supports_int.bit_length() == 2_015_083, "support bit length")
require(len(raw) == 251_886, "support byte length")
require(
    hashlib.sha256(raw).hexdigest()
    == "4d11045a6ab54a207e0c6ed148104a40f426f2ab4e5ef5e65453f1eca4710678",
    "support SHA-256",
)
require(supports % P == 864_013_898, "support residue p")
require(supports % 1_000_000_007 == 180_951_258, "support residue 1e9+7")
require(supports % 4_294_967_291 == 633_477_545, "support residue 2^32-5")


# Independent toy lower-kernel rank calculation over F_17.
pt = 17
zt = 3
Dt = [pow(zt, i, pt) for i in range(16)]
Et = set(Dt[:3])
Ut = [1 if x in Et else 0 for x in Dt]


def toy_lower_matrix(Kshift):
    max_w = 2
    max_n = Kshift + 1
    rows = []
    for x, ux in zip(Dt, Ut):
        rows.append(
            [(ux * pow(x, j, pt)) % pt for j in range(max_w + 1)]
            + [(-pow(x, j, pt)) % pt for j in range(max_n + 1)]
        )
    return nmod_mat(rows, pt)


toy_ranks = {}
for shift in (8, 9):
    A = toy_lower_matrix(shift)
    require(A.rank() == A.ncols(), "toy lower-degree kernel")
    toy_ranks[str(shift)] = {"rank": A.rank(), "columns": A.ncols()}

print(json.dumps({
    "status": "FLINT_PASS_ACTUAL_RECORD_DIMENSION_SENSITIVITY_AUDIT",
    "p": int(fmpz(P)),
    "carrier_order": N,
    "extension_modulus_irreducible": True,
    "minimal_shifted_degree_both_conventions": E,
    "code_d2": code_d2,
    "effective_d2": effective_d2,
    "code_profile": "BOUNDARY_NUMERICAL_PROFILE",
    "effective_profile": "FIRST_INTERIOR_NUMERICAL_PROFILE",
    "actual_owner": "NOT_ESTABLISHED_BY_PINNED_SOURCES",
    "support_fingerprint_sha256": hashlib.sha256(raw).hexdigest(),
    "toy_ranks": toy_ranks,
    "pure_ray_scope": True,
    "ledger_movement": 0,
}, sort_keys=True))
