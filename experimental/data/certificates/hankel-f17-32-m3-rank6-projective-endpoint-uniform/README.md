# F17^32 M3 Rank-6 Projective Endpoint Uniform Theorem

Status: PROVED / AUDIT.

This packet proves that the projective endpoint part of the rank-6 boundary is
not a prefix-support artifact.  For every agreement

```text
385 <= A <= 426,
```

let `j=512-A`.  For any disjoint supports

```text
|X| = j+1,   |Y| = 6,   X,Y subset H,
```

and any nonzero weights, define

```text
u_m = sum_{x in X} a_x x^m,
v_m = sum_{y in Y} b_y y^m.
```

Then `rank H(v)=6`, and the projective split-locator endpoint `[0:1]` is
genuinely nonempty.  Choose any seven surviving base nodes `R subset X`; the
locator with roots `Y union (X\R)` has degree `j`, divides `X^512-1`, kills
`H(v)`, and has `H(u)ell != 0` by a seven-node weighted Vandermonde argument.

The many possible locators witness the same projective slope parameter
`[0:1]`; this proves endpoint nonemptiness, not multiple projective parameters.
It does not compute finite affine root tables.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_projective_endpoint_uniform.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json
```
