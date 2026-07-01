# F17^32 M3 Rank-6 A387 Separated Boundary Safety

Status: PROVED / AUDIT.

This packet closes the arbitrary-weight separated rank-6 boundary branch at

```text
A = 387.
```

For any disjoint supports `|X|=j+1`, `|Y|=6` and any nonzero weights, the
low-degree transfer has

```text
h = |X union Y| - t = 1.
```

Thus the projective auxiliary `Q`-space is a single point.  The six direction
equations are either inconsistent or determine one finite slope.  Therefore
there is at most one finite ambient root, hence at most one finite split-locator
root after the split-locator gate.  The endpoint-uniform theorem supplies the
single projective endpoint `[0:1]`, so the support-wise projective total is at
most

```text
1 + 1 = 2 <= 6.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a387_separated_boundary_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a387-separated-boundary-safety/f17_32_n512_k256_m3_rank6_a387_separated_boundary_safety.json
```

Nonclaims:

```text
does not cover A=385 or A=386;
does not classify overlapping-support rank-6 pencils;
does not decide whether the possible finite root exists for a given weight set;
does not prove endpoint payment.
```
