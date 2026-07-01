# F17^32 M3 Rank-6 Barycentric Split-Locator Filter

Status: PROVED / AUDIT.

This packet refines the boundary barycentric obstruction at

```text
A in {385,386,387}.
```

The barycentric packet shows that `z=1` is an ambient finite rank-drop root for
chosen nonzero separated weights on `S=X union Y`.  This packet shows that the
displayed root is filtered out by the split-locator gate: its kernel
polynomials are exactly the low-degree polynomials

```text
deg Q < |S|-t,
```

with dimensions `5,3,1` respectively.  A support-wise split locator must be a
monic degree-`j` divisor of `X^512-1`, so no degree-`j` split locator lies in
this kernel.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_barycentric_split_filter.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-split-filter/f17_32_n512_k256_m3_rank6_barycentric_split_filter.json
```

Nonclaims:

```text
does not classify every finite root of the barycentric weights;
does not classify arbitrary boundary rank-6 pencils;
does not close overlapping-support strata;
does not prove endpoint payment.
```
