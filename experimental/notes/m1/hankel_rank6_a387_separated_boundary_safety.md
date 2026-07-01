# Hankel Rank-6 A387 Separated Boundary Safety

Status: PROVED / AUDIT.

This note closes one boundary agreement for the separated rank-6 branch with
arbitrary nonzero weights:

```text
A = 387.
```

Work with disjoint supports

```text
|X| = j+1,     |Y| = 6,     j = 512-387 = 125,
t = 387-256 = 131.
```

Then

```text
|X union Y| - t = (126+6)-131 = 1.
```

By the low-degree transfer theorem, every finite ambient root is represented by
a nonzero auxiliary polynomial `Q` with

```text
deg Q < 1.
```

Projectively, this is a single `Q`-class.  For that class, the six
direction-node consistency equations

```text
z b_y L_Q(y) = Omega_y Q(y)      (y in Y)
```

are either inconsistent or determine a single finite scalar `z`.  Hence the
ambient finite root count is at most `1`.  The null-polynomial split-locator
gate can only remove finite ambient roots, so the finite support-wise
split-locator count is also at most `1`.

The endpoint-uniform theorem supplies one projective endpoint `[0:1]` for the
same separated supports and nonzero weights.  Thus the total support-wise
projective contribution in this branch is at most

```text
1 finite + 1 endpoint = 2 <= 6.
```

So the arbitrary-weight separated rank-6 branch at `A=387` is projective-safe
without endpoint payment or quotient/extension subtraction.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a387_separated_boundary_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a387-separated-boundary-safety/f17_32_n512_k256_m3_rank6_a387_separated_boundary_safety.json
```

Nonclaims:

```text
no claim for A=385 or A=386;
no overlapping-support rank-6 classification;
no assertion that the possible finite root exists for all weights;
no endpoint payment theorem.
```
