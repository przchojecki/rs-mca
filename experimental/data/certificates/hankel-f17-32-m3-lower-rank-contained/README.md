# F17^32 M3 Lower-Rank Contained Branch

Status: PROVED / AUDIT for zero-`u` weighted power-sum syndromes with support
rank `r <= j`.

This directory classifies the lower-rank boundary of the M3 weighted
power-sum branch over

```text
385 <= A <= 426.
```

For exact agreement `A`, write `j=512-A` and let

```text
u_m = 0,
v_m = sum_{i=1}^r w_i x_i^m,
```

where the `x_i` are distinct descriptor-domain points, all nonzero weights
`w_i` lie in `F_17^32`, and `0 <= r <= j`.

Then `H(v)` has rank at most `r`, so every `(j+1)x(j+1)` maximal minor of

```text
H(u) + Z H(v) = Z H(v)
```

vanishes.  The regular bucket is therefore singular.

This singularity is not a new aperiodic residual.  For any slope and any
agreement-at-least-`A` support `W`, an explaining degree-`<256` codeword has at
least

```text
|W \ S| >= A-r >= A-j = 2A-512 >= 258 > 256
```

zeros outside the rank support `S`; hence the explaining codeword is zero.
Thus the agreement support is contained in `D\S`, where both line generators
are zero codeword restrictions.  The branch contributes zero support-wise
noncontained aperiodic slopes after the contained/common-code-line filter.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_lower_rank_contained.py \
  --write experimental/data/certificates/hankel-f17-32-m3-lower-rank-contained/f17_32_n512_k256_m3_lower_rank_contained.json

python3 experimental/scripts/verify_f17_32_m3_lower_rank_contained.py \
  --check experimental/data/certificates/hankel-f17-32-m3-lower-rank-contained/f17_32_n512_k256_m3_lower_rank_contained.json
```
