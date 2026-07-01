# F17^32 M3 Rank-6 Boundary Dual GCD

Status: PROVED / COMPUTATIONAL.

This packet closes the three boundary agreements left outside the direct
rank-6 Vandermonde proof:

```text
A = 385, 386, 387.
```

For the prefix-plus-six-spikes family, the support union has size `m=j+7`.
At these three agreements, `t<m`, so finite nonzero root emptiness is not a
plain full-support Vandermonde rank statement.

The verifier uses the exact dual formulation.  Let `u=1/z` for finite
nonzero slopes.  If `K=ker V_t(S)` has dimension `d=m-t`, and `C` is the
degree-`<=j` evaluation code on the support union `S`, finite rank drop is
equivalent to the `6 x d` pencil

```text
P diag(1 on X, u on Y) K
```

dropping column rank, where `P` is a parity-check basis for `C`.  For
`A=385,386,387`, the dimensions `d` are `5,3,1`.  The verifier computes the
gcd of all maximal minors in `u`; in each case the gcd is constant, so there
are no finite nonzero roots over `F_17^32` or over scalar extensions.  The
finite root `z=0` is full rank by the base Vandermonde block.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_dual_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-dual-gcd/f17_32_n512_k256_m3_rank6_boundary_dual_gcd.json
```
