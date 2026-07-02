# F17^32 M3 Rank-6 A385 Three-Core Quadratic Cut

Status: PROVED / AUDIT.

This packet closes the separated `A=385` rank-6 branch with a fixed forced
base split-root core of size three, provided at least one pairwise
direction-consistency equation restricts to a nonzero binary quadratic on the
remaining projective `Q`-line.  The nonzero quadratic gives at most two
projective `Q`-classes; each compatible non-slope-free class gives at most one
finite slope, and the endpoint adds at most one projective parameter.

Conclusion:

```text
fixed three-core nonzero-quadratic branch projective total <= 3 <= 6.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_three_core_quadratic_cut.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-three-core-quadratic-cut/f17_32_n512_k256_m3_rank6_a385_three_core_quadratic_cut.json
```

Nonclaims:

```text
does not close the ratio-identically-consistent fixed three-core Q-line residual;
does not close moving-core or no-common-core A=385 branches;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment;
does not produce a row-level M3 safe-side bound.
```
