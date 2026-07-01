# F17^32 M3 Rank-6 Separated Six-Spike Closure

Status: PROVED / AUDIT.

This packet closes a support- and weight-uniform separated rank-6 family in the
tall part of the M3 window:

```text
388 <= A <= 426.
```

Let `j=512-A` and `t=A-256`.  For any disjoint supports

```text
|X| = j+1,   |Y| = 6,   X,Y subset H,
```

and any nonzero weights, define

```text
u_m = sum_{x in X} a_x x^m,
v_m = sum_{y in Y} b_y y^m.
```

For `z=0`, the finite Hankel block has support `X` of size `j+1`.  For
`z!=0`, it has support `X union Y` of size `j+7`; in this range `t>=j+7`.
The weighted Vandermonde factorization therefore gives full column rank
`j+1` for every finite slope.  Thus the canonical finite root table is empty.

The companion endpoint-uniform packet supplies the genuine split-locator
endpoint `[0:1]`, so the projective contribution of this family is exactly
one slope parameter, within the projective budget `6`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_separated_six_spike_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-separated-six-spike-closure/f17_32_n512_k256_m3_rank6_separated_six_spike_closure.json
```

Nonclaims:

```text
does not cover A=385,386,387;
does not classify arbitrary rank-6 Hankel pencils;
does not handle overlapping base and direction supports;
does not prove endpoint payment by quotient, tangent, or extension ledgers.
```
