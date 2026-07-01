# F17^32 M3 Rank-6 Boundary Barycentric Obstruction

Status: COUNTEREXAMPLE / PROVED.

This packet shows that the separated six-spike tall closure is sharp at the
left boundary.  For

```text
A in {385,386,387},
```

the support/weight-uniform empty finite-root statement is false.

Let `j=512-A`, `t=A-256`, and choose arbitrary disjoint supports

```text
|X| = j+1,   |Y| = 6,   S = X union Y.
```

Set barycentric residues

```text
omega_s = 1 / prod_{r in S, r != s} (s-r),
```

and use `a_x=omega_x`, `b_y=omega_y`.  Then the constant locator `ell=1`
lies in the kernel of `H(u+v)`, because

```text
sum_{s in S} omega_s s^e = 0,   0 <= e <= |S|-2,
```

and the three boundary agreements satisfy `t <= |S|-1`.  Thus `z=1` is a
finite rank-drop slope.  The endpoint-uniform packet also gives the
projective endpoint `[0:1]`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_barycentric_obstruction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-barycentric-obstruction/f17_32_n512_k256_m3_rank6_boundary_barycentric_obstruction.json
```

Nonclaims:

```text
does not compute the exact finite root count for these weights;
does not produce an over-budget support-wise MCA lower bound;
does not classify overlapping-support rank-6 pencils;
does not refute the prefix/unit-weight boundary dual-gcd closure.
```
