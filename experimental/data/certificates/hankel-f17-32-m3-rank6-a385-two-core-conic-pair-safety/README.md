# F17^32 M3 Rank-6 A385 Two-Core Conic-Pair Safety

Status: PROVED / AUDIT.

This packet closes the separated `A=385` rank-6 branch with a fixed forced
base split-root core of size two, provided two residual direction-consistency
conics on the remaining projective `Q`-plane have no common component.  Bezout
gives at most four compatible `Q`-classes; each compatible non-slope-free class
gives at most one finite slope, and the endpoint adds at most one projective
parameter.

Conclusion:

```text
fixed two-core no-common-component branch projective total <= 5 <= 6.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_conic_pair_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-conic-pair-safety/f17_32_n512_k256_m3_rank6_a385_two_core_conic_pair_safety.json
```

Nonclaims:

```text
does not close the fixed two-core common-component residual;
does not close moving-core or no-common-core A=385 branches;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment;
does not produce a row-level M3 safe-side bound.
```
