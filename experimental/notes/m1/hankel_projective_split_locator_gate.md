# Hankel Projective Split-Locator Gate

Status: PROVED / AUDIT.

This note records the support-wise filter that must be applied to ambient
projective-infinity endpoints in the F17^32 M3 window.

For the pinned row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426,
```

write

```text
j = 512 - A,    t = A - 256.
```

The ambient projective chart for the homogenized Hankel pencil is

```text
H_{t,j}(v) ell = 0,     H_{t,j}(u) ell != 0.
```

The first equation says that `[0:1]` is an ambient rank-drop endpoint.  The
second equation is the same-support noncontainment test.  Neither equation by
itself says that `ell` is the locator of an actual subset of the RS domain.

The support-wise split-locator endpoint condition is:

```text
L(X) = sum_{b=0}^j ell_b X^b
```

normalizes to a monic degree-`j` divisor of `X^512-1`.

The row descriptor records `H` as the powers of an exact order-512 generator in
`F_17^32`.  Since `17` does not divide `512`, the derivative of `X^512-1` is
nonzero on every domain point.  Hence `X^512-1` is squarefree, and its monic
degree-`j` divisors are exactly the locators of `j`-element subsets of `H`.

Consequently, an ambient projective kernel vector contributes to the
support-wise MCA numerator only after passing both gates:

```text
L(X) | X^512-1,       H_{t,j}(u) ell != 0.
```

If `H(u)ell=H(v)ell=0`, the same support is contained in both endpoints and the
projective chart does not contribute a noncontained split-locator witness.

For the rank-6 boundary highlighted by the M4 projective-budget split, this is
the important accounting point.  A rank-6 direction block has ambient
projective kernel dimension

```text
j+1-6,
```

which ranges from `81` at `A=426` to `122` at `A=385`.  That large ambient
kernel should not be counted as endpoint evidence until it is intersected with
the finite split-locator divisor gate.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_m3_projective_split_locator_gate.py \
  --check experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/f17_32_n512_k256_m3_projective_split_locator_gate.json
```

This packet does not prove endpoint payment or emptiness for rank-6 buckets,
and it does not compute any finite affine root table.  It only records the
projective split-locator gate that future endpoint packets must pass.
