# A385 Pair-Core Rank Test

This packet records the external-evaluation rank-test normal form for the
separated `A=385` rank-6 no-fixed-core pair-core frontier.

At `A=385`, the low-degree transfer has a five-dimensional `Q`-space.  A pair
of finite classes sharing an external core `E` spans a two-dimensional
`Q`-line, so every evaluation row `ev_s(Q)=L_Q(s)` for `s in E` lies in the
three-dimensional annihilator of that line.  Therefore any pair-core survivor
must have

```text
rank M_E <= 3.
```

For the pressure-forced core size `|E|>=24`, this says every `4 x 4` minor of
the `24 x 5` external-evaluation matrix must vanish.  This is a normal form,
not a closure: split-locator divisibility, quotient payment, and
noncontainment remain separate gates.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_pair_core_rank_test.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-pair-core-rank-test/f17_32_n512_k256_m3_rank6_a385_pair_core_rank_test.json
```
