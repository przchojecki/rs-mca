# F17^32 M3 Rank-6 Boundary Low-Degree Transfer

Status: PROVED / AUDIT.

This packet gives the exact search object for separated rank-6 finite roots at
the boundary agreements

```text
A in {385,386,387}.
```

For arbitrary disjoint supports `|X|=j+1`, `|Y|=6` and arbitrary nonzero
weights `a_x,b_y`, write `S=X union Y`, `h=|S|-t`.  Then

```text
h = 5, 3, 1
```

respectively.  Every finite ambient root is represented by a nonzero
polynomial `Q` with `deg Q < h`.  Given `Q`, interpolate the unique
degree-`<j+1` polynomial `L_Q` from

```text
a_x L_Q(x) = Omega_x Q(x)       (x in X),
```

where `Omega_s` is the barycentric residue on `S`.  A finite root exists
exactly when the six equations

```text
z b_y L_Q(y) = Omega_y Q(y)     (y in Y)
```

are consistent for a single scalar `z`.  After that, `L_Q` still has to pass
the null-polynomial split-locator gate.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_low_degree_transfer.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json
```

Nonclaims:

```text
does not solve the Q-consistency equations for arbitrary weights;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment;
does not replace exact root tables for non-barycentric boundary strata.
```
