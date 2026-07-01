# Hankel Rank-6 Barycentric Exact Root Table

Status: PROVED / AUDIT.

This note closes the boundary barycentric separated rank-6 family left by the
ambient obstruction and split-filter notes.  Work at

```text
A = 385, 386, 387,
j = 512-A,       t = A-256,       m = j+1.
```

Let `X,Y` be disjoint with

```text
|X| = m,       |Y| = 6,       S = X union Y,
```

and define barycentric residues

```text
omega_s = 1 / prod_{r in S, r != s} (s-r).
```

Use `a_x=omega_x` and `b_y=omega_y`.  For a finite slope `z`, a kernel
polynomial `L` of degree `<m` satisfies

```text
sum_{x in X} omega_x L(x) x^e
  + z sum_{y in Y} omega_y L(y) y^e = 0,
0 <= e < t.
```

The dual Vandermonde nullspace on `S` says there is a polynomial `Q` with

```text
deg Q < |S|-t
```

such that

```text
L(x) = Q(x)          for x in X,
z L(y) = Q(y)        for y in Y.
```

Because `|X|=m` and `deg(L-Q)<m`, the first set of equations forces `L=Q`.
Then on `Y`,

```text
(z-1)L(y) = 0.
```

If `z!=1`, the polynomial `L=Q` has degree `< |S|-t <= 5` and vanishes on the
six distinct direction nodes, hence `L=0`, contradiction.  Therefore no
finite root other than `z=1` exists.  Conversely, at `z=1`, every nonzero
`Q` of degree `< |S|-t` gives a kernel polynomial, so `z=1` is present with
kernel dimension `|S|-t` (`5,3,1`).

The companion split-filter note proves this `z=1` kernel contains no monic
degree-`j` divisor of `X^512-1`.  Thus the finite support-wise split-locator
contribution is zero.  The endpoint-uniform theorem supplies the single
projective endpoint `[0:1]`.  Hence this barycentric boundary family has
support-wise projective total exactly `1`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_barycentric_exact_root_table.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-exact-root-table/f17_32_n512_k256_m3_rank6_barycentric_exact_root_table.json
```

Nonclaims:

```text
no arbitrary boundary rank-6 classification;
no non-barycentric weight classification;
no overlapping-support closure;
no endpoint payment theorem.
```
