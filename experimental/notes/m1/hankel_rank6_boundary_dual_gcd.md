# Hankel Rank-6 Boundary Dual GCD

Status: PROVED / COMPUTATIONAL.

This note records the finite-root closure for the rank-6
prefix-plus-six-spikes family at the three agreements where the direct
Vandermonde rank proof is not tall enough:

```text
A = 385, 386, 387.
```

For this family, the base support has size `j+1` and the direction support has
six nodes, so the support union has size

```text
m = j + 7.
```

At `A=388` and above, `t>=m`, and finite nonzero slopes are excluded directly
by full-support Vandermonde rank.  At `A=385,386,387`, the deficits

```text
d = m - t
```

are respectively `5,3,1`.  The finite-root question is still small.

Let `S=X union Y` be the support union.  Let `K=ker V_t(S)`, so
`dim K=d`, and let `C=Eval_{<=j}(S)`, which has codimension `6`.  For a
finite nonzero slope write `u=1/z`.  A rank-drop slope exists exactly when

```text
K intersect diag(1 on X, u on Y) C
```

is nonzero.  Equivalently, for a `6 x m` parity-check matrix `P` for `C`, the
`6 x d` pencil

```text
P diag(1 on X, u on Y) K
```

drops column rank.

The verifier uses the standard barycentric description of Vandermonde
nullspaces: for `m` distinct nodes, barycentric weights times
`1,x,...,x^{d-1}` span the nullspace of the first `m-d` moment rows.  It then
computes the gcd of all `d x d` minors of the `6 x d` pencil.  The gcd is
constant for all three boundary agreements.  Hence there are no finite
nonzero canonical roots, even after scalar extension.  The slope `z=0` is full
rank by the base-support Vandermonde block.

Combined with the direct Vandermonde argument for `388<=A<=426`, this upgrades
the rank-6 projective witness family to the full regular M3 window
`385<=A<=426`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_dual_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-dual-gcd/f17_32_n512_k256_m3_rank6_boundary_dual_gcd.json
```

This is a finite-root closure for this synthetic family only.  It does not
classify arbitrary rank-6 Hankel pencils and does not pay the projective
endpoint.
