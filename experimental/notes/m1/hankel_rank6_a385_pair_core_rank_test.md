# Hankel Rank-6 A385 Pair-Core Rank Test

Status: PROVED / AUDIT.

This note sharpens the large pair-core target from

```text
experimental/notes/m1/hankel_rank6_a385_pair_core_quotient_reduction.md
```

into an external-evaluation rank test.

At `A=385`, the separated rank-6 boundary transfer has

```text
j = 127,        m = 128,        h = 5.
```

Thus the auxiliary `Q`-space has vector dimension `5`, or projective dimension
`4`.  For each external subgroup point `s`, define the linear functional

```text
ev_s(Q) = L_Q(s)
```

on this five-dimensional `Q`-space.

If two finite classes share an external root core `E`, their projective
`Q`-line `U` satisfies

```text
ev_s|_U = 0        for every s in E.
```

Equivalently, if `M_E` is the `|E| x 5` matrix whose rows are the external
evaluation functionals `ev_s`, then

```text
rowspan(M_E) subset U^perp.
```

Since `U` has vector dimension `2`, its annihilator has vector dimension

```text
5 - 2 = 3.
```

Therefore any pair-core survivor must satisfy

```text
rank M_E <= 3.
```

Conversely, `rank M_E <= 3` gives `dim ker M_E >= 2`, hence at least one
projective `Q`-line whose transferred locators vanish on `E`.  This converse is
only a linear common-core statement: it does not prove that the kernel line has
two split-locator classes, quotient divisors, or finite noncontainment.

The no-fixed-core pressure packet guarantees `|E|>=24` for any remaining
projective over-budget survivor.  The next closure target can therefore be
stated concretely:

```text
No separated A=385 no-fixed-core survivor exists unless there is a
24-point external set E with rank M_E <= 3, and the kernel line contains
two distinct full-split quotient members passing the noncontainment gate.
```

Equivalently, every `4 x 4` minor of the `24 x 5` external-evaluation matrix
must vanish.

This also explains why the fixed two-core line product-collapse theorem cannot
be reused directly.  In the fixed two-core residual, the `Q`-space has vector
dimension `3`, so a projective line has a one-dimensional annihilator; two
forced external roots make their evaluation functionals proportional, which is
the input to the existing product-collapse dichotomy.  Here the ambient
no-fixed-core `Q`-space has vector dimension `5`, so the same projective line
has a three-dimensional annihilator.  Even `24` forced roots only give the
rank-`<=3` condition unless an additional theorem collapses that rank-three
span.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_pair_core_rank_test.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-pair-core-rank-test/f17_32_n512_k256_m3_rank6_a385_pair_core_rank_test.json
```

Nonclaims:

```text
no closure of the no-fixed-core A=385 frontier;
no proof that rank<=3 external evaluation cores of size 24 are impossible;
no proof that rank<=3 external evaluation cores of size 24 are paid;
no split-locator witness from the linear converse;
no overlapping-support rank-6 classification;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
