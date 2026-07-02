# F17^32 M3 Rank-6 A385 Fixed-Core Synthesis

Status: PROVED / AUDIT.

This packet composes the separated `A=385` rank-6 fixed-core packets into one
frontier statement.  It verifies that every branch with a fixed forced base
core of size at least two is projective-budget safe.

The consumed packets are the fixed four-core closure, fixed three-core
quadratic cut, fixed three-core residual closure, and the fixed two-core
conic-pair/component/global/slope-free/moving-slope/high-core chain.

The remaining A385 frontier is outside this fixed-core hypothesis: branches
without a fixed two-point base core, moving-core/no-common-core behavior,
overlapping support, and row-level M3 synthesis.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_fixed_core_synthesis.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-fixed-core-synthesis/f17_32_n512_k256_m3_rank6_a385_fixed_core_synthesis.json
```
