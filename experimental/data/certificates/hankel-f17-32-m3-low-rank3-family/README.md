# F17^32 M3 Rank-3 Low-Rank Family

This directory contains a deterministic all-window certificate for a synthetic
rank-3 low-rank update family across the M3 regular non-tangent window

```text
RS[F_17^32,H,256], |H|=512, 385 <= A <= 426.
```

For each agreement `A`, let `r=j+1=513-A`.  The certificate uses the first
`r` descriptor-domain nodes as the square base `X` and the next three
descriptor-domain nodes as the update set `Y`.  The low-rank determinant lemma
gives

```text
Delta_r(Z)=det(H_X) det(I+ZK),  K_ab=sum_i L_i(y_a)L_i(y_b),
```

so every row has degree at most `3`.  The verifier computes the exact number
of finite `F_17^32` roots by the Frobenius gcd

```text
gcd(Delta_r(Z), Z^q - Z).
```

Across the 42 agreements, the exact finite-root total is `42` under degree cap
`126`: 12 rows have no finite roots, 24 rows have one finite root, and 6 rows
have three finite roots.  The projective endpoint `[0:1]` is empty in every
row, so each agreement has at most 3 projective regular roots against budget
numerator 6.  The common-code-line tangent overlap is also zero: evaluating the
Frobenius gcd at the only possible slope from `Syn_0(u+zv)=|X|+3z` is nonzero
for every row.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank3_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank3-family/f17_32_n512_k256_m3_low_rank3_family_certificate.json
```

Non-claims: this is a synthetic family only, not an actual `F_17^32` prize-row
table, not a universal M3 row bound, and not a quotient-image subtraction
audit.  The six split-cubic rows are exact count certificates, not expanded
root lists.
