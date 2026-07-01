# Hankel Rank-6 Barycentric Split-Locator Filter

Status: PROVED / AUDIT.

The boundary barycentric obstruction shows that the support/weight-uniform
empty finite-root statement fails at

```text
A = 385, 386, 387.
```

This note records the next filter: the displayed ambient root `z=1` is not
itself a support-wise split-locator witness.

Let

```text
j = 512-A,     t = A-256,     m = j+1,
|X| = m,       |Y| = 6,       S = X union Y.
```

The barycentric construction uses

```text
omega_s = 1 / prod_{r in S, r != s} (s-r),
a_x = omega_x,     b_y = omega_y.
```

At `z=1`, a polynomial `L` of degree `<m` lies in the ambient Hankel kernel iff

```text
sum_{s in S} omega_s L(s) s^e = 0       for 0 <= e < t.
```

The dual Vandermonde description says the nullspace of the first `t` rows on
`S` is exactly

```text
{ omega_s Q(s) : deg Q < |S|-t }.
```

Thus `L(s)=Q(s)` for all `s in S`, with `deg Q < |S|-t`.  Since

```text
|S| = j+7 > j >= deg(L-Q),
```

the polynomial `L-Q` has too many roots unless `L=Q`.  Therefore the entire
ambient kernel at the barycentric root consists of polynomials of degree

```text
< |S|-t = 5, 3, 1
```

for `A=385,386,387`, respectively.

The null-polynomial split-locator gate requires a monic degree-`j` divisor of
`X^512-1`.  Because every kernel polynomial at the displayed barycentric root
has degree `< |S|-t << j`, that root has no degree-`j` split-locator witness.

Consequently, the barycentric packet is a genuine sharpness obstruction for
ambient finite-root tables, but its displayed root is filtered before becoming
a support-wise MCA witness.  The boundary still needs exact root tables or
paid-root audits for other possible roots and other weight strata.

The companion exact-root note

```text
experimental/notes/m1/hankel_rank6_barycentric_exact_root_table.md
```

proves that for the same barycentric family there are no other finite ambient
roots: the ambient root table is exactly `{1}`.  Combined with this filter and
the endpoint-uniform theorem, that barycentric boundary family has
support-wise projective total exactly `1`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_barycentric_split_filter.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-split-filter/f17_32_n512_k256_m3_rank6_barycentric_split_filter.json
```

Nonclaims:

```text
no exact full root table for the barycentric weights;
no arbitrary boundary rank-6 classification;
no overlapping-support closure;
no endpoint payment theorem.
```
