# KoalaBear equality-wall ternary-secant/circuit route cut v1

This directory contains the exact 225-coordinate-type certificate for an
abstract 69-record \(\mathbf F_p\)-valued carrier family at the
KoalaBear-scale equality-wall profile.  The values are viewed inside
\(\mathbf F_{p^6}\) by scalar extension, which preserves the verified
Hamming weights and base-field ranks.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_kb_mca_v4_equality_wall_ternary_secant_circuit_route_cut_v1.py --check
python3 -O experimental/scripts/verify_kb_mca_v4_equality_wall_ternary_secant_circuit_route_cut_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_equality_wall_ternary_secant_circuit_route_cut_v1.py --tamper-selftest
sage experimental/scripts/verify_kb_mca_v4_equality_wall_ternary_secant_circuit_route_cut_v1.sage
```

The certificate proves an exact countermodel only to the coarse inference
from support cardinalities, affine/secant rank, every selected-pair and
projective ternary-secant distance check, exchange, bounded circuits,
no-singleton atoms, and circuit restriction ranks to cap 68.

It does not certify the distance of every arbitrary linear combination in
the eight-dimensional secant span.  It also does not construct an actual
GRS evaluation subcode, locator/source polynomials, a received line, a
complete selector, a bad slope, a same-record owner, or any ledger payment.
Its architecture, exhaustive partition, and active `U_paid` fields are
explicitly null.  The certificate is bound instead to the current upstream
workboard, consolidated K3 status, and four-row exact-completion authority.
The full KoalaBear row and its 405-case residual remain open.
