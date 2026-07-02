# Hankel Rank-6 A385 Pair-Core Quotient Reduction

Status: PROVED / AUDIT.

This note records the next reduction after the `A=385` no-fixed-core pressure
packet.

The pressure packet proves that any remaining separated `A=385` rank-6
projective over-budget survivor, after fixed-core synthesis, must contain two
finite split-locator classes whose external root sets share a common core
`E` of size at least `24`.

At `A=385`,

```text
j = 127,        m = 128,        h = 5.
```

Let the two classes be represented by low-degree transfer parameters `Q0` and
`Q1`, and write their transferred locators as `L_Q0` and `L_Q1`.  The transfer
map

```text
Q -> L_Q
```

is linear.  Therefore every `Q` in the projective line `<Q0,Q1>` also satisfies
`L_Q(s)=0` for every `s in E`.

Put

```text
C_E(T) = prod_{s in E} (T-s).
```

Since `E` is external to the base support, this common factor does not come
from a fixed base-root core.  Since every `L_Q` on the line has degree `<128`
and vanishes on all of `E`, every locator in the pair line factors as

```text
L_Q = C_E R_Q,        deg R_Q < 128-|E|.
```

For the two original finite split-locator classes, the split-locator gate says
that, after normalization, `L_Q` is a monic degree-127 divisor of `X^512-1`.
Thus the corresponding quotients are degree `127-|E|` divisors of

```text
(X^512-1)/C_E.
```

At the forced core size `|E|>=24`, the ambient quotient family has vector
dimension at most

```text
128-24 = 104,
```

and the two actual split quotient members have degree at most

```text
127-24 = 103.
```

So the remaining no-fixed-core frontier is no longer an unconstrained
occupancy problem: it reduces to excluding or paying a projective quotient
pencil containing two distinct full-split quotient members of degree at most
`103`.

The companion rank-test note

```text
experimental/notes/m1/hankel_rank6_a385_pair_core_rank_test.md
```

rephrases this quotient-pencil target as a concrete external-evaluation rank
condition: a `24`-point common external core must make the corresponding
`24 x 5` evaluation matrix have rank at most `3`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_pair_core_quotient_reduction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-pair-core-quotient-reduction/f17_32_n512_k256_m3_rank6_a385_pair_core_quotient_reduction.json
```

Nonclaims:

```text
no closure of the no-fixed-core A=385 frontier;
no proof that the large pair-core quotient pencil is empty;
no proof that the large pair-core quotient pencil is paid;
no overlapping-support rank-6 classification;
no proof that the projective endpoint is unpaid;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
