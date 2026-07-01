# F17^32 M3 Rank-5 Low-Rank Budget Family

This directory contains a deterministic all-window budget certificate for the
synthetic rank-5 low-rank family in the M3 regular window
`385 <= A <= 426`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank5_budget_family.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank5-budget-family/f17_32_n512_k256_m3_low_rank5_budget_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank5_budget_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank5-budget-family/f17_32_n512_k256_m3_low_rank5_budget_family_certificate.json
```

For each agreement, the certificate uses the first `j+1` descriptor-domain
nodes as the square base and the next five descriptor-domain nodes as the
low-rank update.  It replays the compressed Lagrange-kernel determinant

```text
Delta_r(Z)=det(H_X) det(I+ZK)
```

using Newton identities from traces of powers of `K`, and verifies that every
row has degree exactly `5`.  Exact finite roots are not enumerated because the
v4 low-rank packet gate already makes the degree bound budget-sufficient at the
projective cutoff: at most five finite roots plus the one corrected projective
infinity point gives at most six projective regular roots, exactly the M3
projective budget numerator.

Non-claims: this is a synthetic family only, not a universal row table, not a
quotient/tangent subtraction table, and not an exact finite-root enumeration.
