# A385 Pair-Core Quotient Reduction

This packet records a local reduction for the separated `A=385` rank-6
no-fixed-core frontier.

It consumes the no-fixed-core pressure packet and proves that the forced pair
of finite classes sharing at least `24` external roots spans a projective
`Q`-line on which every transferred locator factors through the common
external core:

```text
L_Q = C_E R_Q.
```

At the guaranteed core size, the ambient quotient family has vector dimension
at most `104`, and the two actual split quotient members have degree at most
`103`.  The packet is a reduction to a quotient-pencil target, not a closure of
the no-fixed-core branch.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_pair_core_quotient_reduction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-pair-core-quotient-reduction/f17_32_n512_k256_m3_rank6_a385_pair_core_quotient_reduction.json
```
