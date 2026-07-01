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
the family has degree at most `2`, independent of the prefix minor size.

The certificate now applies the rank-2 discriminant gate to every row.  Of the
42 quadratics, 20 split over `F_17^32` and 22 have nonsquare discriminant, so
the exact finite-root total is `40`.  The certificate records the compressed
kernels, determinant coefficients, split-linear or nonsquare quadratic
certificates, and cross-checks the `A=426` endpoint against the existing
exact-root v9 packet.

The aggregate degree cap for this synthetic family is `84`, compared with the
generic degree-bound sum `4515` for the same agreement window; the exact
finite-root count is `40`.

The projective endpoint is also audited using the original regular-minor
projective convention.  Since the update direction has rank `2 < j+1`, the
top-degree coefficient `det H(v)` is zero and this regular minor does not
exclude `[0:1]`.  Thus infinity contributes one projective parameter in every
row; each agreement has `1` or `3` projective regular roots, still below the
budget numerator `6`.

The finite roots are also compared with the common-code-line tangent ledger.
For a finite root `z`, the full syndrome has zeroth moment

```text
Syn_0(u+zv)=|X|+2z.
```

All 40 finite roots have this witness nonzero, so none of them are paid by the
common-code-line tangent branch.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank2_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-family/f17_32_n512_k256_m3_low_rank2_family_certificate.json
```

Non-claims: this is a synthetic syndrome-pencil family certificate, not a
worst-case MCA row bound, not a worst-case root table over arbitrary
`F_17^32` row data, and not a quotient/tangent subtraction ledger.  The budget
comparison is regular-root accounting before removed-ledger subtraction.
Quotient-image overlap is not audited here.
