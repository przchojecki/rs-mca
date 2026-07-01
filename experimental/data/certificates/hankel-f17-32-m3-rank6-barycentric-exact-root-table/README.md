# F17^32 M3 Rank-6 Barycentric Exact Root Table

Status: PROVED / AUDIT.

This packet closes the boundary barycentric separated rank-6 family at

```text
A in {385,386,387}.
```

For arbitrary disjoint supports `|X|=j+1`, `|Y|=6`, set
`S=X union Y` and choose barycentric weights on `S`.  The exact ambient finite
root table is

```text
{1}.
```

The root `z=1` has kernel dimension `|S|-t` (`5,3,1` respectively), but the
split-filter packet proves this kernel contains no monic degree-`j` divisor of
`X^512-1`.  Hence the finite support-wise split-locator contribution is `0`.
The endpoint-uniform packet supplies the single projective endpoint `[0:1]`,
so this family has support-wise projective total `1`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_barycentric_exact_root_table.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-exact-root-table/f17_32_n512_k256_m3_rank6_barycentric_exact_root_table.json
```

Nonclaims:

```text
does not classify arbitrary boundary rank-6 pencils;
does not classify non-barycentric boundary weights;
does not close overlapping-support strata;
does not prove endpoint payment.
```
