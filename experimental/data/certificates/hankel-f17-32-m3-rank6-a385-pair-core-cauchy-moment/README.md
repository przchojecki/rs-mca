# A385 Pair-Core Cauchy-Moment Normal Form

This packet unpacks the `A=385` no-fixed-core pair-core rank-test rows.

For base support `X`, base weights `W_x=Omega_x/a_x`, and
`P_X(T)=prod_{x in X}(T-x)`, the external-evaluation row
`ev_s(Q)=L_Q(s)` in the degree-`<5` `Q`-basis has coordinates

```text
c_r(s)=P_X(s) sum_{x in X} W_x x^r/((s-x)P_X'(x)).
```

Since `P_X(s)` is nonzero for external `s`, the rank test is equivalent to the
same test on the reduced Cauchy-moment rows

```text
d_r(s)=sum_{x in X} W_x x^r/((s-x)P_X'(x)).
```

Thus a pressure-forced pair-core survivor requires a `24 x 5` reduced
Cauchy-moment matrix of rank at most `3`, with every `4 x 4` minor expanded by
the recorded Cauchy-Binet formula.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_pair_core_cauchy_moment.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-pair-core-cauchy-moment/f17_32_n512_k256_m3_rank6_a385_pair_core_cauchy_moment.json
```
