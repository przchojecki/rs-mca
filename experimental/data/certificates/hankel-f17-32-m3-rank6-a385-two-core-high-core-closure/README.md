# F17^32 M3 Rank-6 A385 Two-Core High-Core Closure

Status: PROVED / AUDIT.

This packet composes the A385 fixed two-core moving-slope incidence packet, the
high-core quotient normal form, and the conic product-collapse packet.  It adds
the line product-collapse analogue and the punctured projective tangent tail.

The line product collapse proves that two forced external roots on a line
component force either a common-root pencil or product without modular
reduction.  In both cases a degree-`127` split locator needs external forced
core size at least `123`, so the high-core line range `71<=e_G<=122` is closed.

The punctured tangent tail gives at most `128-e_G` projective bad slopes after
puncturing the forced external core, hence it is projective-budget safe for
`e_G>=122`.  Together with the earlier incidence and conic product-collapse
packets, this closes all separated fixed two-core line/conic high-core
moving-slope components.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_high_core_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-high-core-closure/f17_32_n512_k256_m3_rank6_a385_two_core_high_core_closure.json
```
