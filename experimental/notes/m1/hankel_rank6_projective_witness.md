# Hankel Rank-6 Projective Witness

Status: PROVED / AUDIT for this synthetic family.

This note records a rank-6 endpoint witness inside the F17^32 M3 regular
window.  It is meant to sharpen the rank-6 boundary, not to close it.

For

```text
C = RS[F_17^32,H,256],    |H| = 512,
```

and exact agreement `A`, set

```text
j = 512 - A,    t = A - 256.
```

The packet covers

```text
385 <= A <= 426.
```

The finite-root proof has two parts.  For `388<=A<=426`, it is the direct
Vandermonde rank argument below.  For `A=385,386,387`, the companion boundary
dual-gcd packet proves that the small finite-root pencil has constant gcd, so
there are no finite nonzero canonical roots there either.

Let `x_0,x_1,...` be the descriptor-domain ordering.  Define the synthetic
syndromes

```text
u_m = sum_{i=0}^j x_i^m,
v_m = sum_{i=j+1}^{j+6} x_i^m.
```

Then the direction block has rank exactly `6`:

```text
H(v) = V_t(Y) V_{j+1}(Y)^T,
Y = {x_{j+1},...,x_{j+6}}.
```

Both Vandermonde factors have rank `6`.

For finite slopes, `z=0` gives the full-rank base block on `j+1` distinct
nodes.  For `z!=0` and `388<=A<=426`, the Hankel block factors through the
`j+7` distinct nodes `X union Y`.  Since `t>=j+7`, the left Vandermonde is
injective, and the right Vandermonde has full column rank `j+1`.

The remaining agreements `A=385,386,387` have deficits `5,3,1`.  The boundary
dual-gcd packet rewrites the finite nonzero slope condition using `u=1/z` as a
`6 x d` pencil on Vandermonde kernel and parity bases, then checks that the
gcd of all maximal minors is constant.  Thus those three agreements also have
empty finite canonical root table, even after scalar extension.

At projective infinity, choose the monic locator with roots

```text
Y union {x_0,...,x_{j-7}}.
```

This has degree `j` and divides `X^512-1`.  It vanishes on every direction
node, so `H(v)ell=0`.  The surviving base nodes are

```text
x_{j-6},...,x_j,
```

seven distinct nodes.  If `H(u)ell` were zero, the first seven rows would give
an invertible 7x7 Vandermonde system forcing the seven nonzero locator values
on those nodes to vanish.  Thus `H(u)ell!=0`, and the projective endpoint
`[0:1]` is a genuine support-wise split-locator witness.

Consequence: the rank-6 projective endpoint is not merely an ambient artifact.
It can occur in a Hankel-realizable family.  Therefore the remaining rank-6
M4 boundary cannot be closed by endpoint emptiness from Hankel realizability
alone; it needs endpoint payment, exact finite root-table refinement, or a
sharper Hankel-specific classification.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_projective_witness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/f17_32_n512_k256_m3_rank6_projective_witness.json

python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_dual_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-dual-gcd/f17_32_n512_k256_m3_rank6_boundary_dual_gcd.json
```

Nonclaims:

```text
no arbitrary rank-6 Hankel-pencil classification;
no simultaneous six-finite-roots plus projective-endpoint example;
no endpoint quotient/extension payment statement;
not a worst-case support-wise MCA row bound.
```
