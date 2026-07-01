# Hankel Rank-6 Boundary Barycentric Obstruction

Status: COUNTEREXAMPLE / PROVED.

This note records the obstruction to extending the separated six-spike tall
closure support/weight-uniformly to the boundary agreements

```text
A = 385, 386, 387.
```

Work in

```text
C = RS[F_17^32,H,256],    |H| = 512,
j = 512-A,                t = A-256,
```

and take any disjoint supports

```text
|X| = j+1,     |Y| = 6,     S = X union Y.
```

For these boundary agreements,

```text
|S|-t = 5, 3, 1
```

respectively.  Define barycentric residues on `S` by

```text
omega_s = 1 / prod_{r in S, r != s} (s-r).
```

These residues are nonzero because the support nodes are distinct.  The
standard partial-fraction identity gives

```text
sum_{s in S} omega_s s^e = 0        for 0 <= e <= |S|-2.
```

Use the separated weights

```text
a_x = omega_x,    b_y = omega_y.
```

At finite slope `z=1`, the constant locator `ell(T)=1` satisfies

```text
(H(u+v)ell)_e = sum_{s in S} omega_s s^e = 0
```

for all rows `0 <= e < t`, since `t <= |S|-1`.  Hence `z=1` is a finite
rank-drop slope.  At `z=0`, the base block has support `X` of size `j+1` with
nonzero weights and `t>=j+1`, so it has full column rank by weighted
Vandermonde factorization.  Thus this is a genuine finite-root obstruction,
not a degenerate zero-base case.

The endpoint-uniform theorem applies to the same nonzero separated weights,
so `[0:1]` is also present.  This does not make the family unsafe: the packet
only proves a lower bound of one finite slope plus the endpoint.  Its role is
to show that the tall closure beginning at `A=388` is sharp, and that
`A=385,386,387` require a boundary-specific finite-root classification or a
paid-root argument.

The companion split-filter note

```text
experimental/notes/m1/hankel_rank6_barycentric_split_filter.md
```

shows that this displayed ambient root is not itself a support-wise
split-locator witness: its kernel consists only of polynomials of degree
`< |S|-t`, while the split-locator gate requires degree `j`.

The exact-root companion

```text
experimental/notes/m1/hankel_rank6_barycentric_exact_root_table.md
```

then proves the ambient finite root table of the same barycentric family is
exactly `{1}`.  Thus, after the split filter, the finite support-wise
contribution is zero and the only support-wise projective contribution in
this family is the endpoint `[0:1]`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_barycentric_obstruction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-barycentric-obstruction/f17_32_n512_k256_m3_rank6_boundary_barycentric_obstruction.json
```

Nonclaims:

```text
no exact finite root count for the barycentric weights;
no over-budget MCA lower bound;
no overlapping-support rank-6 classification;
no contradiction with the prefix/unit-weight boundary dual-gcd closure.
```
