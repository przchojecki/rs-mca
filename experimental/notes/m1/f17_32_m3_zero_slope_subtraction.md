# F17^32 M3 zero-slope subtraction

Status: **AUDIT** for one synthetic v9 packet.

This note records the first small M4-style subtraction test attached to the M3
regular-window work.  It applies only to the fixed synthetic top-window packet

```text
RS[F_17^32,H,256], |H|=512, 421 <= A <= 426.
```

The source packet proves that every listed agreement bucket has regular-minor
root union `{0}`.  The line-value lift proves that the same syndrome pencil is
realized by values `f,g:H -> F_17^32` with `f=0`.  Therefore the finite slope
`z=0` makes the line word `f+z g` equal to the zero Reed-Solomon codeword.
This root is a tangent/common-code-line root, not residual aperiodic evidence.

The checked sidecar is:

```text
experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/
```

For each `A=421..426`, it verifies

```text
regular roots before removed ledgers: {0}
tangent roots removed:               {0}
quotient roots removed:              empty
extension roots removed:             empty
residual aperiodic roots:            empty
```

This is not an M4 row table.  The useful point is narrower: the table exercises
the no-double-counting convention on an actual v9 root-count packet and makes
clear that the synthetic top-window root should be paid by the tangent ledger
before any aperiodic numerator is reported.

Next step: repeat the same subtraction discipline for actual `F_17^32` row
pencils, then add quotient-image roots and Prime192 scanner rows only when
there are v9 root-count packets to combine with those ledgers.
