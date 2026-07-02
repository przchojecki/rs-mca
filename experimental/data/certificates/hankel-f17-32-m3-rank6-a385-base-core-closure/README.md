# F17^32 M3 Rank-6 A385 Base-Core Closure

Status: PROVED / AUDIT.

This packet closes the separated `A=385` rank-6 branch with a fixed forced
base split-root core of size at least four.  Since the low-degree transfer has
`deg Q<5`, four common base roots collapse the projective `Q`-space from `P^4`
to a single point.  The direction equations then give at most one finite
noncontained slope, and the endpoint adds at most one projective parameter.

Conclusion:

```text
fixed four-base-core branch projective total <= 2 <= 6.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_base_core_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-base-core-closure/f17_32_n512_k256_m3_rank6_a385_base_core_closure.json
```

Nonclaims:

```text
does not close A=385 branches without a common forced four-point base core;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment;
does not produce a row-level M3 safe-side bound.
```
