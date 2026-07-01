# F17^32 M3 Low-Rank-2 Family Certificate

This directory contains a deterministic audit certificate for the synthetic
rank-2 low-rank update family across the whole M3 regular non-tangent window

```text
385 <= A <= 426
```

of `RS[F_17^32,H,256]`.

For each agreement, let `r=j+1=513-A`.  The certificate uses the first `r`
descriptor-domain nodes as the square base `X`, and the next two descriptor
nodes as the update set `Y`.  The replayed determinant is

```text
Delta_r(Z)=det(H_X) det(I+ZK),
K_ab=sum_i L_i(y_a)L_i(y_b),
```

where the `L_i` are the Lagrange basis polynomials on `X`.  Thus every row in
the family has degree at most `2`, independent of the prefix minor size.  The
certificate records the 42 compressed kernels and determinant coefficients,
cross-checking the `A=426` endpoint against the existing exact-root v9 packet.

The aggregate regular root bound for this synthetic family is therefore `84`,
compared with the generic degree-bound sum `4515` for the same agreement
window.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank2_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-family/f17_32_n512_k256_m3_low_rank2_family_certificate.json
```

Non-claims: this is a synthetic syndrome-pencil family certificate, not a
worst-case MCA row bound, not a worst-case root table over `F_17^32`, and not a
quotient/tangent subtraction ledger.  Roots are not enumerated here; the rows
are degree-bound-only charts.
