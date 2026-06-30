# Regular-Minor Common-GCD Gate

This directory contains a small proof/audit certificate for a sharper regular
bucket gate.

In a regular overdetermined bucket, a bad regular slope makes the full Hankel
matrix have rank at most `j`.  Therefore every maximal `(j+1) x (j+1)` minor
vanishes at that slope.  For any audited family of maximal row-set minors, the
bad regular slopes are contained in the finite-field roots of the gcd of their
determinant polynomials.

The replay uses the `F_17`, `n=16`, `k=8` regular-minor toy and all contiguous
maximal row sets.  It shows that common-gcd roots can be strictly sharper than
a single prefix-minor root table.

Run:

```sh
python3 experimental/scripts/verify_m1_regular_minor_gcd_gate.py \
  --check experimental/data/certificates/regular-minor-gcd-gate/f17_n16_k8_regular_minor_gcd_gate_certificate.json
```

Non-claims: this does not prove an F17^32 row bound, and a gcd from a proper
minor family can still have false positives unless the family is rank-complete.
