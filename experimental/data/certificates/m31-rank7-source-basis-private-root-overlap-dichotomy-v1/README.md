# M31 rank-seven source-basis private-root/overlap dichotomy v1

This packet sharpens the unique \(Q=147\,595,\ k=4\,981\) residual from
the fixed-mismatch recurrence.  It pays any branch with a common direction
zero and any branch with a projective evaluation line of size at least five.
For a seven-member actual source basis, it then proves the exact trichotomy

\[
z>0,\qquad |S_{\rm line}|\ge5,\qquad\text{or}\qquad
\deg\gcd(G_i,G_j)\ge16\,903
\]

for some basis pair.  The final high-overlap component is explicitly unpaid.

Replay:

```bash
python3 experimental/scripts/verify_m31_rank7_source_basis_private_root_overlap_dichotomy_v1.py --check
python3 -O experimental/scripts/verify_m31_rank7_source_basis_private_root_overlap_dichotomy_v1.py --check
python3 experimental/scripts/verify_m31_rank7_source_basis_private_root_overlap_dichotomy_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_rank7_source_basis_private_root_overlap_dichotomy_v1.py --tamper-selftest
python3 experimental/scripts/verify_m31_rank7_source_basis_private_root_overlap_dichotomy_v1_independent.py
sage experimental/scripts/verify_m31_rank7_source_basis_private_root_overlap_dichotomy_v1.sage
```

The packet does not pay \(Q=147\,595\), assign a v4 owner, move the active
ledger, treat rank at least eight, or close the M31 LIST row.
