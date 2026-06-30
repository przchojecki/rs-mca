# F17^32 M3 extension-denominator audit

Status: **AUDIT**.

This note records the denominator convention for the synthetic top-window
line-value packet

```text
RS[F_17^32,H,256], |H|=512, 421 <= A <= 426.
```

The source line-value lift gives functions `f,g:H -> F_17^32`.  In the
repository encoding, base-field elements of `F_17` are exactly the encoded
integers `0..16`.  The checked audit verifies:

```text
f values: 512/512 base-field values, 0 nonzero values
g values: 512/512 non-base values, 512 nonzero values
```

Thus the line is genuinely extension-valued.  Even though the zero slope used
by the subtraction sidecar is itself the base-field element `0`, the finite
affine slope sampler for this packet is the full ambient line field
`F_17^32`.  The support-wise MCA denominator is therefore

```text
q_line = |F_17^32| = 17^32,
floor(q_line / 2^128) = 6.
```

Using the base-field denominator `17` would be the wrong object.  This is the
small F1 accounting point: field-valued line packets must print which field is
used for the slope sampler before their numerators are compared to a
`2^-128` budget.

The checked audit is:

```text
experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/
```

Next step: repeat this denominator audit for any actual-row or Prime192 v9
packet before combining tangent, quotient, and aperiodic ledgers.
